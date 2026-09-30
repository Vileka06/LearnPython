/* ==========================================================================
   PySimple Learn - the dashboard.
   All your progress lives in localStorage, so everything on this page is
   worked out here in the browser from that one saved object.
   ========================================================================== */
(function () {
  "use strict";

  var PS = window.PySimple;
  if (!PS) return;

  var $ = PS.$, $$ = PS.$$, store = PS.store;

  var DATA = {};
  try {
    DATA = JSON.parse($("#dashData").textContent);
  } catch (e) {
    return;  // nothing sensible to draw
  }

  var titleOf = {};
  DATA.topics.forEach(function (t) { titleOf[t.slug] = t.title; });

  function text(node, value) { if (node) node.textContent = value; }

  function plural(n, one, many) { return n + " " + (n === 1 ? one : many); }

  /* ------------------------------------------------------------- render */
  function render() {
    var state = store.get();
    var done = state.done;
    var total = DATA.total;
    var finished = done.length;
    var percent = total ? Math.round((finished / total) * 100) : 0;

    // ----------------------------------------------------------- headline
    text($("#statXp"), String(state.xp || 0));
    text($("#statStreak"), String(state.streak || 0));
    text($("#statRuns"), String(state.runs || 0));
    text($("#statQuiz"), String(store.perfectCount()));

    var summary;
    if (finished === 0) {
      summary = "No topics finished yet. The first one takes about three minutes.";
    } else if (finished === total) {
      summary = "Every topic finished, " + plural(store.perfectCount(), "quick check", "quick checks") +
                " aced. That is the whole site done.";
    } else {
      summary = plural(finished, "topic", "topics") + " of " + total + " finished, " +
                plural(state.streak || 0, "day", "days") + " in a row. " +
                plural(total - finished, "topic", "topics") + " to go.";
    }
    text($("#dashSummary"), summary);

    // ------------------------------------------------------------- ring
    text($("#ringPercent"), percent + "%");
    text($("#ringSub"), finished + " / " + total);
    var bar = $("#ringBar");
    if (bar) {
      var circumference = 2 * Math.PI * 52;
      bar.style.strokeDasharray = circumference;
      bar.style.strokeDashoffset = circumference - (circumference * percent) / 100;
    }
    text($("#ringNote"), noteFor(finished, total, state));

    // ------------------------------------------------------------- rank
    renderRank(state);

    // ------------------------------------------------------- skill bars
    renderSkillBars(state);

    // ---------------------------------------------------------- up next
    renderUpNext(state);

    // ----------------------------------------------------------- tracks
    renderTracks(state);

    // ----------------------------------------------------------- badges
    renderBadges(state);

    // ---------------------------------------------------------- mastery
    renderMastery(state);
  }

  function noteFor(finished, total, state) {
    if (finished === 0) return "Nothing finished yet. Start with the first topic.";
    if (finished === total) return "All done. Try the quizzes again to top up your score.";
    var perfect = store.perfectCount();
    if (perfect === 0) return "Pass a quick check to start building real mastery.";
    if (perfect < finished) return perfect + " quick checks aced. " + (finished - perfect) + " still to test.";
    return "Every topic you finished, you also aced. Well done.";
  }

  /* ---------------------------------------------------------------- rank */
  function renderRank(state) {
    var xp = state.xp || 0;
    var ranks = DATA.ranks || [];
    var current = ranks[0];
    var following = null;

    ranks.forEach(function (rank) {
      if (xp >= rank.min) current = rank;
    });
    ranks.forEach(function (rank) {
      if (!following && rank.min > xp) following = rank;
    });

    text($("#rankName"), current.name);
    text($("#rankBlurb"), current.blurb);

    var percent, nextLine;
    if (following) {
      var span = following.min - current.min;
      percent = span ? Math.round(((xp - current.min) / span) * 100) : 100;
      percent = Math.max(0, Math.min(100, percent));
      var needed = following.min - xp;
      nextLine = needed + " XP to " + following.name;
    } else {
      percent = 100;
      nextLine = "Top rank reached";
    }

    var fill = $("#rankFill");
    if (fill) fill.style.width = percent + "%";
    text($("#rankNext"), nextLine);
  }

  /* ---------------------------------------------------------- skill map */
  function renderSkillBars(state) {
    var holder = $("#skillBars");
    if (!holder) return;
    holder.innerHTML = "";

    DATA.groups.forEach(function (group) {
      var done = group.slugs.filter(function (s) { return state.done.indexOf(s) !== -1; }).length;
      var pct = group.slugs.length ? Math.round((done / group.slugs.length) * 100) : 0;

      var row = document.createElement("div");
      row.className = "skill-row";

      var name = document.createElement("span");
      name.className = "skill-name";
      name.textContent = group.name;

      var bar = document.createElement("span");
      bar.className = "skill-bar";
      var fill = document.createElement("span");
      fill.className = "skill-fill";
      fill.style.width = pct + "%";
      bar.appendChild(fill);

      var value = document.createElement("span");
      value.className = "skill-pct";
      value.textContent = done + "/" + group.slugs.length;

      row.appendChild(name);
      row.appendChild(bar);
      row.appendChild(value);
      holder.appendChild(row);
    });
  }

  /* ------------------------------------------------------------ up next */
  function renderUpNext(state) {
    var holder = $("#nextGrid");
    if (!holder) return;
    holder.innerHTML = "";

    var suggestions = [];

    // 1. the first thing on your current track that is not finished
    DATA.tracks.forEach(function (track) {
      var next = track.slugs.filter(function (s) { return state.done.indexOf(s) === -1; })[0];
      if (next) suggestions.push({ slug: next, why: "Next on the " + track.name + " path" });
    });

    // 2. something you have finished but never been tested on
    state.done.forEach(function (slug) {
      if (!state.quiz[slug]) suggestions.push({ slug: slug, why: "Finished, but not tested yet" });
    });

    // 3. a weak spot: a topic you have opened a few times but never finished
    DATA.topics.forEach(function (topic) {
      if (state.done.indexOf(topic.slug) !== -1) return;
      if (state.seen.indexOf(topic.slug) !== -1) {
        suggestions.push({ slug: topic.slug, why: "You opened this one before" });
      }
    });

    // 4. anything else, in order
    DATA.topics.forEach(function (topic) {
      if (state.done.indexOf(topic.slug) === -1) {
        suggestions.push({ slug: topic.slug, why: "Not started" });
      }
    });

    // Keep the first mention of each topic, take three
    var seen = {};
    var picks = [];
    suggestions.forEach(function (item) {
      if (picks.length >= 3) return;
      if (seen[item.slug]) return;
      seen[item.slug] = true;
      picks.push(item);
    });

    if (!picks.length) {
      var done = document.createElement("p");
      done.className = "next-empty";
      done.textContent = "Every topic is finished. Re-read the ones that feel shakiest.";
      holder.appendChild(done);
      return;
    }

    picks.forEach(function (pick) {
      var topic = DATA.topics.filter(function (t) { return t.slug === pick.slug; })[0] || {};
      var card = document.createElement("a");
      card.className = "next-card";
      card.href = "/topic/" + pick.slug;

      var why = document.createElement("span");
      why.className = "next-why";
      why.textContent = pick.why;

      var name = document.createElement("strong");
      name.className = "next-name";
      name.textContent = topic.title || pick.slug;

      var desc = document.createElement("span");
      desc.className = "next-desc";
      desc.textContent = topic.summary || "";

      var arrow = document.createElement("span");
      arrow.className = "next-arrow";
      arrow.textContent = "->";

      card.appendChild(why);
      card.appendChild(name);
      card.appendChild(desc);
      card.appendChild(arrow);
      holder.appendChild(card);
    });
  }

  /* ------------------------------------------------------------- tracks */
  function renderTracks(state) {
    DATA.tracks.forEach(function (track) {
      var card = document.querySelector('.track-card[data-track="' + track.id + '"]');
      if (!card) return;

      var finished = track.slugs.filter(function (s) { return state.done.indexOf(s) !== -1; }).length;
      var perfect = track.slugs.filter(function (s) { return state.quiz[s] === 100; }).length;
      var pct = track.slugs.length ? Math.round((finished / track.slugs.length) * 100) : 0;
      var mastery = track.slugs.length
        ? Math.round(((finished + perfect) / (track.slugs.length * 2)) * 100)
        : 0;

      text($("[data-role='pct']", card), pct + "%");
      text($("[data-role='count']", card),
        finished + " of " + track.slugs.length + " done" +
        (perfect ? " - " + perfect + " aced" : ""));

      var fill = $("[data-role='fill']", card);
      if (fill) fill.style.width = pct + "%";
      var marker = $("[data-role='mastery']", card);
      if (marker) marker.style.left = mastery + "%";

      card.classList.toggle("is-complete", finished === track.slugs.length);
    });
  }

  /* ------------------------------------------------------------- badges */
  function renderBadges(state) {
    var holder = $("#badgeGrid");
    if (!holder) return;
    holder.innerHTML = "";

    var earned = 0;

    DATA.badges.forEach(function (badge) {
      var info = store.badgeProgress(badge, DATA);
      if (info.earned) earned++;

      var card = document.createElement("div");
      card.className = "badge" + (info.earned ? " is-earned" : "");

      var face = document.createElement("span");
      face.className = "badge-face";
      face.style.setProperty("--hue", badge.hue);
      face.textContent = info.earned ? badge.mark : "?";
      if (info.earned) face.setAttribute("aria-hidden", "true");

      var body = document.createElement("span");
      body.className = "badge-body";

      var name = document.createElement("strong");
      name.className = "badge-name";
      name.textContent = badge.name;

      var desc = document.createElement("span");
      desc.className = "badge-desc";
      desc.textContent = info.earned ? badge.desc : progressLine(badge, info);

      body.appendChild(name);
      body.appendChild(desc);

      card.appendChild(face);
      card.appendChild(body);

      if (!info.earned && info.need > 1) {
        var mini = document.createElement("span");
        mini.className = "badge-mini";
        var miniFill = document.createElement("span");
        miniFill.style.width = info.percent + "%";
        mini.appendChild(miniFill);
        card.appendChild(mini);
      }

      holder.appendChild(card);
    });

    text($("#badgeCount"), String(earned));
    holder.classList.toggle("has-none", earned === 0);
  }

  function progressLine(badge, info) {
    if (info.need > 1) return info.have + " of " + info.need + " - " + badge.desc;
    return badge.desc;
  }

  /* ------------------------------------------------------------ mastery */
  function renderMastery(state) {
    var holder = $("#masteryGrid");
    if (!holder) return;
    holder.innerHTML = "";

    var rows = DATA.topics.map(function (topic) {
      var isDone = state.done.indexOf(topic.slug) !== -1;
      var best = state.quiz[topic.slug] || 0;
      var points = (isDone ? 1 : 0) + (best === 100 ? 1 : 0);
      return { topic: topic, done: isDone, best: best, points: points };
    });

    rows.sort(function (a, b) {
      if (b.points !== a.points) return b.points - a.points;
      if (b.best !== a.best) return b.best - a.best;
      return a.topic.number - b.topic.number;
    });

    var strongest = rows.slice(0, 5);
    var weakest = rows.slice(-5).reverse();

    makeColumn(holder, "Solid", strongest, true);
    makeColumn(holder, "Worth another look", weakest, false);
  }

  function makeColumn(holder, title, rows, good) {
    var column = document.createElement("div");
    column.className = "mastery-col";

    var heading = document.createElement("p");
    heading.className = "mastery-title" + (good ? " is-good" : " is-soft");
    heading.textContent = title;
    column.appendChild(heading);

    var list = document.createElement("ul");
    list.className = "mastery-list";

    rows.forEach(function (row) {
      var item = document.createElement("li");
      item.className = "mastery-item";

      var link = document.createElement("a");
      link.href = "/topic/" + row.topic.slug;
      link.className = "mastery-link";

      var name = document.createElement("span");
      name.className = "mastery-name";
      name.textContent = row.topic.title;

      var tag = document.createElement("span");
      tag.className = "mastery-tag";
      if (row.best === 100) { tag.textContent = "aced"; tag.classList.add("is-perfect"); }
      else if (row.best) { tag.textContent = row.best + "%"; }
      else if (row.done) { tag.textContent = "done"; }
      else { tag.textContent = "open"; }

      link.appendChild(name);
      link.appendChild(tag);
      item.appendChild(link);
      list.appendChild(item);
    });

    column.appendChild(list);
    holder.appendChild(column);
  }

  /* ------------------------------------------------------- reset button */
  function setUpReset() {
    var button = $("#resetProgress");
    if (!button) return;

    button.addEventListener("click", function () {
      if (!window.confirm("Clear all your progress, XP, badges and streaks? This cannot be undone.")) return;
      store.clear();
    });
  }

  /* ------------------------------------------------------------- start */
  function start() {
    setUpReset();
    store.onChange(render);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();

/* ==========================================================================
   PySimple Learn - shared helpers.
   Loaded before the other scripts on every page. Keeps one copy of your
   progress in localStorage and tells the rest of the site when it changes.
   ========================================================================== */
(function (global) {
  "use strict";

  var KEYS = {
    theme: "pysimple-theme",
    progress: "pysimple-progress",
    code: "pysimple-code",
    search: "pysimple-last-search"
  };

  /* XP awarded for each thing you do. */
  var XP = {
    topic: 20,
    run: 5,
    quiz: 30,
    quizPerfect: 20,
    streakDay: 10
  };

  function $(sel, root) { return (root || document).querySelector(sel); }
  function $all(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function read(key, fallback) {
    try {
      var raw = localStorage.getItem(key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) { return fallback; }
  }

  function write(key, value) {
    try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private mode */ }
  }

  function today() {
    var d = new Date();
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  }

  function yesterday() {
    var d = new Date();
    d.setDate(d.getDate() - 1);
    return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate());
  }

  function pad(n) { return (n < 10 ? "0" : "") + n; }

  /* --------------------------------------------------------- the store */
  function blank() {
    return {
      done: [],      // slugs of finished topics
      seen: [],      // slugs of topics opened
      quiz: {},      // slug -> best percent
      xp: 0,
      runs: 0,
      runDays: [],   // days on which you ran any code, for the streak
      streak: 0,
      lastActive: ""
    };
  }

  function load() {
    var p = read(KEYS.progress, null);
    var fresh = blank();

    // Fold in anything from the older, simpler save format.
    var legacy = read("pysimple-done", null);
    if (Array.isArray(legacy)) fresh.done = legacy;

    if (!p || typeof p !== "object") return fresh;

    Object.keys(fresh).forEach(function (key) {
      if (p[key] !== undefined && p[key] !== null) fresh[key] = p[key];
    });
    if (!Array.isArray(fresh.done)) fresh.done = [];
    if (!Array.isArray(fresh.seen)) fresh.seen = [];
    if (!Array.isArray(fresh.runDays)) fresh.runDays = [];
    if (typeof fresh.quiz !== "object" || !fresh.quiz) fresh.quiz = {};
    if (typeof fresh.xp !== "number") fresh.xp = 0;
    if (typeof fresh.runs !== "number") fresh.runs = 0;
    if (typeof fresh.streak !== "number") fresh.streak = 0;

    return fresh;
  }

  var state = load();

  /* Anyone can subscribe, so the sidebar, top bar and dashboard all react. */
  var listeners = [];

  function notify() {
    listeners.forEach(function (fn) {
      try { fn(state); } catch (e) { /* one broken listener must not stop the rest */ }
    });
  }

  function save() {
    write(KEYS.progress, state);
    notify();
  }

  /* ------------------------------------------------------------ streak */
  function touchStreak() {
    var day = today();
    if (state.lastActive === day) return 0;   // already counted today

    var gained = state.lastActive === yesterday() ? 1 : 0;
    if (state.lastActive === yesterday()) {
      state.streak = (state.streak || 0) + 1;
    } else {
      state.streak = 1;
    }
    state.lastActive = day;
    return gained ? XP.streakDay : 0;
  }

  /* --------------------------------------------------------- the verbs */
  var Store = {
    keys: KEYS,
    xp: XP,

    get: function () { return state; },

    onChange: function (fn) {
      listeners.push(fn);
      fn(state);
    },

    addXp: function (amount) {
      state.xp = Math.max(0, (state.xp || 0) + amount);
    },

    /* A topic counts as seen as soon as its page opens. */
    markSeen: function (slug) {
      if (!slug || state.seen.indexOf(slug) !== -1) return;
      state.seen.push(slug);
      save();
    },

    /* Marking a topic done is worth XP, and keeps the streak alive. */
    setDone: function (slug, isDone) {
      var at = state.done.indexOf(slug);
      var was = at !== -1;

      if (isDone && !was) {
        state.done.push(slug);
        Store.addXp(XP.topic);
        Store.addXp(touchStreak());
      } else if (!isDone && was) {
        state.done.splice(at, 1);
        Store.addXp(-XP.topic);
      }
      save();
    },

    isDone: function (slug) { return state.done.indexOf(slug) !== -1; },

    /* One run per topic per day, so a long session is not worth farming. */
    noteRun: function (slug) {
      var day = today();
      if (state.runDays.indexOf(day) === -1) state.runDays.push(day);
      state.runs = (state.runs || 0) + 1;
      Store.addXp(XP.run);
      Store.addXp(touchStreak());
      save();
    },

    /* Only a better score counts, and only a first pass pays out. */
    recordQuiz: function (slug, percent) {
      var best = state.quiz[slug] || 0;
      if (percent <= best) return { best: best, improved: false, xp: 0 };

      state.quiz[slug] = percent;
      var gained = XP.quiz + (percent === 100 ? XP.quizPerfect : 0);
      Store.addXp(gained);
      Store.addXp(touchStreak());
      save();
      return { best: percent, improved: true, xp: gained };
    },

    quizBest: function (slug) { return state.quiz[slug] || 0; },

    perfectCount: function () {
      return Object.keys(state.quiz).filter(function (slug) {
        return state.quiz[slug] === 100;
      }).length;
    },

    clear: function () {
      state = blank();
      try { localStorage.removeItem("pysimple-done"); } catch (e) { /* ignore */ }
      save();
    }
  };

  /* ------------------------------------------------------ badge rules */
  /* Turns a rule string from data/achievements.py into a yes/no answer. */
  Store.badgeEarned = function (badge, data) {
    var rule = badge.rule || "";
    var parts = rule.split(":");
    var kind = parts[0];
    var value = parts[1];

    if (kind === "done") {
      var need = rule.indexOf("%") !== -1
        ? Math.ceil((data.total * parseFloat(value)) / 100)
        : parseInt(value, 10);
      return state.done.length >= need;
    }
    if (kind === "quiz") {
      if (value === "track") {
        return (data.tracks || []).some(function (track) {
          return track.slugs.every(function (slug) {
            return state.quiz[slug] === 100;
          });
        });
      }
      return Store.perfectCount() >= parseInt(value, 10);
    }
    if (kind === "run") return (state.runs || 0) >= parseInt(value, 10);
    if (kind === "streak") return (state.streak || 0) >= parseInt(value, 10);
    if (kind === "xp") return (state.xp || 0) >= parseInt(value, 10);
    if (kind === "explore") return (state.seen || []).length >= parseInt(value, 10);

    if (kind === "group") {
      var group = (data.groups || []).filter(function (g) { return g.name === value; })[0];
      if (!group) return false;
      return group.slugs.every(function (slug) { return state.done.indexOf(slug) !== -1; });
    }
    if (kind === "track") {
      var track = (data.tracks || []).filter(function (t) { return t.id === value; })[0];
      if (!track) return false;
      return track.slugs.every(function (slug) { return state.done.indexOf(slug) !== -1; });
    }

    return false;
  };

  /* The shape a badge is in right now, for showing a lock or a tick. */
  Store.badgeProgress = function (badge, data) {
    if (Store.badgeEarned(badge, data)) return { earned: true, percent: 100, have: 1, need: 1 };

    var rule = badge.rule || "";
    var parts = rule.split(":");
    var kind = parts[0];
    var raw = parts[1];
    var have, need;

    if (kind === "done") {
      need = rule.indexOf("%") !== -1 ? Math.ceil((data.total * parseFloat(raw)) / 100) : parseInt(raw, 10);
      have = state.done.length;
    } else if (kind === "quiz" && raw !== "track") {
      need = parseInt(raw, 10); have = Store.perfectCount();
    } else if (kind === "run") {
      need = parseInt(raw, 10); have = state.runs || 0;
    } else if (kind === "streak") {
      need = parseInt(raw, 10); have = state.streak || 0;
    } else if (kind === "xp") {
      need = parseInt(raw, 10); have = state.xp || 0;
    } else if (kind === "explore") {
      need = parseInt(raw, 10); have = (state.seen || []).length;
    } else {
      return { earned: false, percent: 0, have: 0, need: 0 };
    }

    have = Math.min(have, need);
    return { earned: false, percent: Math.round((have / need) * 100), have: have, need: need };
  };

  /* --------------------------------------------------------- exports */
  global.PySimple = {
    $: $,
    $$: $all,
    read: read,
    write: write,
    store: Store,
    today: today
  };
})(window);

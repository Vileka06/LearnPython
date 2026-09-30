/* ==========================================================================
   PySimple Learn - the small amount of JavaScript every page needs.
   1. theme toggle       2. sidebar + search
   3. progress marks     4. code editor   5. syntax colours
   The saved progress itself lives in store.js, which is loaded first.
   ========================================================================== */
(function () {
  "use strict";

  var PS = window.PySimple;
  if (!PS) return;

  var $ = PS.$, $$ = PS.$$, store = PS.store;
  var KEYS = PS.store.keys;

  /* --------------------------------------------------------- 1. theme */
  function setUpTheme() {
    var button = $("#themeBtn");
    if (!button) return;

    button.addEventListener("click", function () {
      var next = document.documentElement.getAttribute("data-theme") === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      PS.write(KEYS.theme, next);
    });
  }

  /* --------------------------------------------------- 2. sidebar + search */
  function setUpSidebar() {
    var sidebar = $("#sidebar");
    var menuBtn = $("#menuBtn");
    var backdrop = $("#backdrop");
    if (!sidebar || !menuBtn) return;

    function setOpen(open) {
      sidebar.classList.toggle("is-open", open);
      if (backdrop) backdrop.hidden = !open;
      menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    }

    menuBtn.addEventListener("click", function () {
      setOpen(!sidebar.classList.contains("is-open"));
    });

    if (backdrop) backdrop.addEventListener("click", function () { setOpen(false); });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") setOpen(false);
    });

    // Close the menu after tapping a topic on a small screen.
    sidebar.addEventListener("click", function (event) {
      if (event.target.closest(".nav-link") && window.innerWidth <= 900) setOpen(false);
    });
  }

  function setUpSearch() {
    var input = $("#topSearch");
    var sidebar = $("#sidebar");
    if (!input || !sidebar) return;

    var links = $$(".nav-link", sidebar);
    var groups = $$(".nav-group", sidebar);
    var empty = $("#navEmpty");

    // Remember what you were last looking for, so the search box is not empty
    // every time you come back.
    var saved = PS.read(KEYS.search, "");
    if (saved) { input.value = saved; filter(saved); }

    function firstVisible() {
      return links.filter(function (link) { return !link.parentNode.hidden; })[0];
    }

    function filter(query) {
      var needle = String(query || "").trim().toLowerCase();
      var shown = 0;

      links.forEach(function (link) {
        var haystack = (link.dataset.title + " " + link.dataset.summary + " " + link.dataset.group).toLowerCase();
        var match = !needle || haystack.indexOf(needle) !== -1;
        link.parentNode.hidden = !match;
        if (match) shown++;
      });

      groups.forEach(function (group) {
        group.hidden = !$$(".nav-link", group).some(function (link) { return !link.parentNode.hidden; });
      });

      if (empty) empty.hidden = shown !== 0;
    }

    input.addEventListener("input", function () {
      filter(input.value);
      PS.write(KEYS.search, input.value);
    });

    input.addEventListener("keydown", function (event) {
      if (event.key !== "Enter") return;
      var first = firstVisible();
      if (first) first.click();
    });

    // "/" jumps to the search box, the way most code editors behave.
    document.addEventListener("keydown", function (event) {
      var typing = /^(INPUT|TEXTAREA)$/.test(event.target.tagName);
      if (event.key === "/" && !typing) {
        event.preventDefault();
        input.focus();
        input.select();
      }
    });
  }

  /* ------------------------------------------------------ 3. progress */
  function setUpProgress() {
    // A topic page counts as "seen" straight away.
    var lessonButton = $(".js-done");
    var slug = lessonButton ? lessonButton.dataset.slug : null;

    if (slug) {
      store.markSeen(slug);
      lessonButton.addEventListener("click", function () {
        store.setDone(slug, !store.isDone(slug));
      });
    }

    // Repaint the ticks, the counters and the bar whenever anything changes.
    store.onChange(function (state) {
      $$("[data-slug]").forEach(function (node) {
        var tag = node.classList;
        if (!tag.contains("nav-link") && !tag.contains("card") && !tag.contains("done-btn")) return;
        tag.toggle("is-done", state.done.indexOf(node.dataset.slug) !== -1);
      });

      var total = $$(".nav-link").length;
      var unique = uniqueDone(state.done);
      var percent = total ? (unique / total) * 100 : 0;

      var fill = $("#progressFill");
      if (fill) fill.style.width = percent + "%";

      ["#doneCount", "#doneCountHome"].forEach(function (sel) {
        var node = $(sel);
        if (node) node.textContent = String(unique);
      });

      if (lessonButton) {
        var isDone = state.done.indexOf(slug) !== -1;
        var label = $(".done-label", lessonButton);
        lessonButton.classList.toggle("is-done", isDone);
        if (label) label.textContent = isDone ? "Done - click to undo" : "Mark this topic as done";
      }

      // Show a best-score chip on any topic that has been quizzed.
      $$("[data-quiz-score]").forEach(function (node) {
        var score = state.quiz[node.dataset.quizScore];
        node.hidden = !score;
        if (score) {
          node.textContent = score + "%";
          node.classList.toggle("is-perfect", score === 100);
        }
      });
    });
  }

  function uniqueDone(list) {
    var seen = {};
    var count = 0;
    list.forEach(function (slug) {
      if (!seen[slug]) { seen[slug] = true; count++; }
    });
    return count;
  }

  /* ---------------------------------------------- 5. syntax colouring */
  var KEYWORDS = [
    "False", "None", "True", "and", "as", "assert", "async", "await", "break",
    "class", "continue", "def", "del", "elif", "else", "except", "finally",
    "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal",
    "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"
  ];

  function escapeHtml(text) {
    return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlight(source) {
    var out = "";
    var i = 0;

    while (i < source.length) {
      var rest = source.slice(i);

      // a comment runs to the end of the line
      var comment = rest.match(/^#[^\n]*/);
      if (comment) {
        out += '<span class="t-com">' + escapeHtml(comment[0]) + "</span>";
        i += comment[0].length;
        continue;
      }

      // a triple-quoted string
      var triple = rest.match(/^(?:[rRbBfF]{0,2})(?:"""[\s\S]*?"""|'''[\s\S]*?''')/);
      if (triple) {
        out += '<span class="t-str">' + escapeHtml(triple[0]) + "</span>";
        i += triple[0].length;
        continue;
      }

      // a quoted string, with an optional prefix such as f or r
      var str = rest.match(/^(?:[rRbBfFuU]{0,2})(["'])(?:\\.|(?!\1)[^\\])*\1/);
      if (str) {
        out += '<span class="t-str">' + escapeHtml(str[0]) + "</span>";
        i += str[0].length;
        continue;
      }

      // a number
      var num = rest.match(/^\d[\d_]*\.?\d*(?:[eE][+-]?\d+)?/);
      if (num) {
        out += '<span class="t-num">' + escapeHtml(num[0]) + "</span>";
        i += num[0].length;
        continue;
      }

      // a word: a keyword, a function name, or just a name
      var word = rest.match(/^[A-Za-z_][A-Za-z_0-9]*/);
      if (word) {
        var w = word[0];
        var after = rest.slice(w.length);
        if (KEYWORDS.indexOf(w) !== -1) {
          out += '<span class="t-key">' + w + "</span>";
        } else if (/^\s*\(/.test(after)) {
          out += '<span class="t-fn">' + w + "</span>";
        } else {
          out += escapeHtml(w);
        }
        i += w.length;
        continue;
      }

      // punctuation and operators
      var op = rest.match(/^[+\-*/%=<>!~^&|]+/);
      if (op) {
        out += '<span class="t-op">' + escapeHtml(op[0]) + "</span>";
        i += op[0].length;
        continue;
      }

      out += escapeHtml(source.charAt(i));
      i += 1;
    }

    return out;
  }

  function colourCodeBlocks() {
    $$("pre.code > code[data-code]").forEach(function (block) {
      if (block.dataset.coloured) return;
      block.innerHTML = highlight(block.textContent);
      block.dataset.coloured = "1";
    });
  }

  /* ------------------------------------------------- 4. code editor */
  function setUpEditor() {
    var editor = $("[data-editor]");
    if (!editor) return;

    var area = $("#codeArea", editor);
    var gutter = $("#gutter", editor);
    var runBtn = $(".js-run", editor);
    var resetBtn = $(".js-reset", editor);
    var stdinArea = $("#stdinArea", editor);
    var status = $("#consoleStatus");
    var consoleBody = $("#consoleBody");

    var doneButton = $(".js-done");
    var slug = (doneButton ? doneButton.dataset.slug : null) || "scratch";
    var original = area.value;
    var codeKey = KEYS.code + ":" + slug;

    var savedCode = PS.read(codeKey, null);
    if (typeof savedCode === "string") area.value = savedCode;

    function lineNumbers() {
      var count = area.value.split("\n").length;
      var html = "";
      for (var n = 1; n <= count; n++) html += "<div>" + n + "</div>";
      gutter.innerHTML = html;
    }

    function save() { PS.write(codeKey, area.value); }

    area.addEventListener("input", function () { lineNumbers(); save(); });
    area.addEventListener("scroll", function () { gutter.scrollTop = area.scrollTop; });

    // Tab inserts four spaces instead of leaving the box, Shift+Tab outdents.
    area.addEventListener("keydown", function (event) {
      if (event.key === "Tab") {
        event.preventDefault();
        var start = area.selectionStart;
        var end = area.selectionEnd;
        area.value = area.value.slice(0, start) + "    " + area.value.slice(end);
        area.selectionStart = area.selectionEnd = start + 4;
        lineNumbers();
        save();
      } else if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
        event.preventDefault();
        run();
      }
    });

    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        area.value = original;
        lineNumbers();
        save();
      });
    }

    function copy(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).catch(function () {});
        return;
      }
      var helper = document.createElement("textarea");
      helper.value = text;
      helper.setAttribute("readonly", "");
      helper.style.position = "absolute";
      helper.style.left = "-9999px";
      document.body.appendChild(helper);
      helper.select();
      try { document.execCommand("copy"); } catch (e) { /* nothing we can do */ }
      document.body.removeChild(helper);
    }

    $$(".js-copy").forEach(function (button) {
      button.addEventListener("click", function () {
        var inEditor = button.closest(".editor");
        var box = inEditor || button.closest(".codebox");
        var text = inEditor ? area.value : (($("code", box) || {}).textContent || "");
        copy(text);
        var label = button.textContent;
        button.textContent = "Copied";
        setTimeout(function () { button.textContent = label; }, 1400);
      });
    });

    function say(text, isError) {
      consoleBody.textContent = text;
      consoleBody.classList.toggle("is-error", Boolean(isError));
      status.classList.toggle("is-error", Boolean(isError));
      status.classList.remove("is-running");
      status.textContent = isError ? "error" : "finished";
    }

    function run() {
      var code = area.value.trim();
      if (!code) { say("There is no code to run yet.", true); return; }

      runBtn.disabled = true;
      status.classList.remove("is-error");
      status.classList.add("is-running");
      status.textContent = "running...";
      consoleBody.classList.remove("is-error");
      consoleBody.textContent = "";

      fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: code, input: stdinArea ? stdinArea.value : "" })
      })
        .then(function (response) { return response.json(); })
        .then(function (data) {
          if (data.ok) {
            say(data.output === "" ? "(your code finished but printed nothing)" : data.output, false);
            store.noteRun(slug);
            runBtn.classList.add("is-done");
            setTimeout(function () { runBtn.classList.remove("is-done"); }, 900);
          } else {
            say((data.stdout ? data.stdout + "\n\n" : "") + data.error, true);
          }
        })
        .catch(function () {
          say("Could not reach the server. Check that app.py is still running.", true);
        })
        .then(function () { runBtn.disabled = false; });
    }

    runBtn.addEventListener("click", run);
    lineNumbers();
  }

  /* ------------------------------------------------------------- start */
  function start() {
    setUpTheme();
    setUpSidebar();
    setUpSearch();
    setUpProgress();
    colourCodeBlocks();
    setUpEditor();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();

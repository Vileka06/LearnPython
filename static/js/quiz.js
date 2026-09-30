/* ==========================================================================
   PySimple Learn - the "Quick check" quiz at the bottom of every lesson.
   The questions come from the server without their answer key, and the
   marking happens on the server too, so nothing is spoiled by looking at
   the page source.
   ========================================================================== */
(function () {
  "use strict";

  var PS = window.PySimple;
  if (!PS) return;

  var $ = PS.$, store = PS.store;

  var root = $("#quiz");
  if (!root) return;

  var slug = root.dataset.slug;
  var body = $("#quizBody");
  var list = $("#quizList");
  var step = $("#quizStep");
  var submit = $("#quizSubmit");
  var resultBox = $("#quizResult");
  var percentOut = $("#quizPercent");
  var detailOut = $("#quizDetail");
  var verdictOut = $("#quizVerdict");
  var again = $("#quizAgain");
  var bestOut = $("#quizBest");

  var total = parseInt(body.dataset.count, 10) || 0;
  var questions = [];
  var answers = [];

  /* --------------------------------------------------------------- best */
  function showBest() {
    var best = store.quizBest(slug);
    if (!best) return;
    bestOut.hidden = false;
    bestOut.textContent = best === 100
      ? "Best score so far: 100% - perfect."
      : "Best score so far: " + best + "%. Have another go to beat it.";
  }

  /* -------------------------------------------------------------- build */
  function build(items) {
    questions = items;
    answers = new Array(items.length).fill(null);
    list.innerHTML = "";
    body.hidden = false;
    resultBox.hidden = true;

    items.forEach(function (item, index) {
      var item_ = document.createElement("li");
      item_.className = "quiz-item";

      /* A fieldset + legend is what a screen reader uses to say which
         question the upcoming radio buttons belong to. */
      var field = document.createElement("fieldset");
      field.className = "quiz-fieldset";

      var q = document.createElement("legend");
      q.className = "quiz-q";
      q.textContent = (index + 1) + ". " + item.q;
      field.appendChild(q);

      var options = document.createElement("div");
      options.className = "quiz-options";

      item.options.forEach(function (text, optionIndex) {
        var label = document.createElement("label");
        label.className = "quiz-option";

        var input = document.createElement("input");
        input.type = "radio";
        input.name = "q" + index;
        input.value = String(optionIndex);
        input.addEventListener("change", function () {
          answers[index] = optionIndex;
          updateStep();
        });

        var mark = document.createElement("span");
        mark.className = "quiz-dot";
        mark.setAttribute("aria-hidden", "true");

        var word = document.createElement("span");
        word.className = "quiz-word";
        word.textContent = text;

        label.appendChild(input);
        label.appendChild(mark);
        label.appendChild(word);
        options.appendChild(label);
      });

      field.appendChild(options);
      item_.appendChild(field);
      list.appendChild(item_);
    });

    updateStep();
  }

  function updateStep() {
    var answered = answers.filter(function (a) { return a !== null; }).length;
    step.textContent = answered + " of " + total + " answered";
    submit.disabled = answered !== total;
  }

  /* ------------------------------------------------------------- check */
  function check() {
    submit.disabled = true;
    submit.textContent = "Checking...";

    fetch("/api/quiz/" + slug + "/answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answers: answers })
    })
      .then(function (response) { return response.json(); })
      .then(function (data) {
        if (!data.ok) throw new Error(data.error || "Something went wrong.");
        showResult(data);
      })
      .catch(function (error) {
        step.textContent = error.message;
        submit.disabled = false;
        submit.textContent = "Check my answers";
      });
  }

  function showResult(data) {
    body.hidden = true;
    resultBox.hidden = false;

    percentOut.textContent = data.percent + "%";
    detailOut.textContent = data.correct + " of " + data.total + " right";
    resultBox.classList.toggle("is-perfect", data.percent === 100);

    verdictOut.textContent = verdictFor(data.percent);

    // Mark every option so a wrong answer shows why it was wrong.
    data.results.forEach(function (row) {
      var item = list.children[row.index];
      if (!item) return;
      var labels = item.querySelectorAll(".quiz-option");
      labels.forEach(function (label, optionIndex) {
        if (optionIndex === row.correct_option) {
          label.classList.add("is-right");
        } else if (optionIndex === row.given) {
          label.classList.add("is-wrong");
        }
        var input = label.querySelector("input");
        if (input) input.disabled = true;
      });

      var note = document.createElement("p");
      note.className = "quiz-why" + (row.right ? " is-right" : " is-wrong");
      note.textContent = (row.right ? "Correct. " : "Not quite. ") + row.why;
      item.appendChild(note);
    });

    var outcome = store.recordQuiz(slug, data.percent);
    if (outcome.improved && outcome.xp) {
      verdictOut.textContent += "  +" + outcome.xp + " XP";
    }
    showBest();
  }

  function verdictFor(percent) {
    if (percent === 100) return "Every question right. This one is properly stuck.";
    if (percent >= 67) return "Most of it right. Read the two you missed, then try once more.";
    if (percent >= 34) return "Halfway there. Worth re-reading the examples above.";
    return "Have another read of the lesson, then come back. Nobody gets this first time.";
  }

  /* ------------------------------------------------------------- start */
  function start() {
    showBest();
    submit.addEventListener("click", check);
    again.addEventListener("click", function () {
      resultBox.hidden = true;
      submit.textContent = "Check my answers";
      body.hidden = false;
      build(questions);
      window.scrollTo({ top: root.offsetTop - 80, behavior: "smooth" });
    });

    fetch("/api/quiz/" + slug)
      .then(function (response) { return response.json(); })
      .then(function (data) { build(data.questions); })
      .catch(function () {
        body.hidden = true;
        step.textContent = "The quiz could not be loaded. Try refreshing the page.";
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();

"""PySimple Learn - a small Flask app for learning Python from scratch.

Run it with:

    python app.py

Then open http://127.0.0.1:5000 in your browser.
"""

import os
import subprocess
import sys
import tempfile
import threading
import time

from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
)

from data import achievements as badges
from data import quizzes
from data import topics as content
from data import tracks as learning_tracks

app = Flask(__name__)

# ---------------------------------------------------------------- settings
RUN_CODE_ENABLED = os.environ.get("PYSIMPLE_RUN_CODE", "1") == "1"
CODE_TIME_LIMIT = 8           # seconds a snippet may run
CODE_SIZE_LIMIT = 20000       # characters of source we accept
OUTPUT_SIZE_LIMIT = 20000     # characters of output we return
STARTUP_WARMUP = os.environ.get("PYSIMPLE_WARMUP", "1") == "1"


def warm_up_libraries():
    """Import the lesson libraries once, in the background.

    The first time matplotlib is imported it builds a font cache, which can
    take the best part of half a minute. Doing it here, while nobody is
    waiting, means the Matplotlib lesson's Run button just works.
    """
    if not STARTUP_WARMUP or not RUN_CODE_ENABLED:
        return

    def worker():
        started = time.time()
        for name in ("numpy", "pandas", "matplotlib.pyplot"):
            try:
                __import__(name)
            except Exception:
                return  # the library is not installed, that is fine
        print(f"Lesson libraries ready in {time.time() - started:.1f}s")

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()


def dashboard_data():
    """Everything the dashboard needs, in one dict.

    The dashboard does its own counting in the browser, because your progress
    only ever lives in this browser's localStorage. This just hands over the
    topic list, the groups, the tracks and the badges.
    """
    return {
        "total": len(content.TOPIC_LIST),
        "topics": [
            {
                "slug": t["slug"],
                "title": t["title"],
                "summary": t["summary"],
                "group": t["group"],
                "number": t["number"],
            }
            for t in content.TOPIC_LIST
        ],
        "groups": [
            {"name": g["name"], "slugs": [t["slug"] for t in g["topics"]]}
            for g in content.grouped_topics()
        ],
        "tracks": [
            {
                "id": t["id"],
                "name": t["name"],
                "tagline": t["tagline"],
                "blurb": t["blurb"],
                "slugs": t["slugs"],
            }
            for t in learning_tracks.TRACKS
        ],
        "badges": badges.ACHIEVEMENTS,
        "ranks": badges.RANKS,
    }


# ------------------------------------------------------------------ pages
def page_base(**extra):
    """Everything every page needs, so the routes stay short."""
    base = {
        "groups": content.grouped_topics(),
        "topics": content.TOPIC_LIST,
        "total": len(content.TOPIC_LIST),
        "run_code_enabled": RUN_CODE_ENABLED,
    }
    base.update(extra)
    return base


@app.route("/")
def home():
    """The front page: a short intro plus every topic as a card."""
    return render_template("home.html", page_title="Learn Python", **page_base())


@app.route("/dashboard")
def dashboard():
    """Your progress, ranks, badges and the next things to learn."""
    return render_template(
        "dashboard.html",
        page_title="Dashboard",
        dash_data=dashboard_data(),
        tracks=learning_tracks.TRACKS,
        badges=badges.ACHIEVEMENTS,
        **page_base()
    )


@app.route("/topic/<slug>")
def topic(slug):
    """One lesson page."""
    lesson = content.TOPIC_BY_SLUG.get(slug)
    if lesson is None:
        abort(404)

    following = content.next_slug(slug)
    following_topic = content.TOPIC_BY_SLUG.get(following) if following else None
    earlier = content.prev_slug(slug)
    earlier_topic = content.TOPIC_BY_SLUG.get(earlier) if earlier else None

    return render_template(
        "topic.html",
        page_title=lesson["title"],
        lesson=lesson,
        quiz=quizzes.QUIZZES.get(slug),
        track=learning_tracks.track_of(slug),
        next_topic=following_topic,
        prev_topic=earlier_topic,
        **page_base()
    )


# ------------------------------------------------------------------- api
@app.route("/api/dashboard")
def api_dashboard():
    """The same data the dashboard page embeds, for anything that wants JSON."""
    return jsonify(dashboard_data())


@app.route("/api/quiz/<slug>")
def api_quiz(slug):
    """The quick check for one topic, so the answer key never sits in the HTML."""
    questions = quizzes.QUIZZES.get(slug)
    if questions is None:
        return jsonify({"ok": False, "error": "No quiz for that topic."}), 404

    # Send the questions without the answer index, then check answers here.
    return jsonify(
        {
            "slug": slug,
            "questions": [
                {
                    "q": q["q"],
                    "options": q["options"],
                    "why": q["why"],
                }
                for q in questions
            ],
        }
    )


@app.route("/api/quiz/<slug>/answer", methods=["POST"])
def api_quiz_answer(slug):
    """Mark a finished quiz and hand back the score."""
    questions = quizzes.QUIZZES.get(slug)
    if questions is None:
        return jsonify({"ok": False, "error": "No quiz for that topic."}), 404

    payload = request.get_json(silent=True) or {}
    given = payload.get("answers", [])
    if not isinstance(given, list):
        return jsonify({"ok": False, "error": "No answers were sent."}), 400
    if len(given) != len(questions):
        return (
            jsonify(
                {
                    "ok": False,
                    "error": f"This quiz has {len(questions)} questions "
                    f"but {len(given)} answers were sent.",
                }
            ),
            400,
        )

    results = []
    correct = 0
    for index, question in enumerate(questions):
        pick = given[index] if index < len(given) else None
        right = pick is not None and pick == question["answer"]
        if right:
            correct += 1
        results.append(
            {
                "index": index,
                "given": pick,
                "correct_option": question["answer"],
                "right": right,
                "why": question["why"],
            }
        )

    total = len(questions)
    percent = round(correct / total * 100) if total else 0
    return jsonify(
        {
            "ok": True,
            "slug": slug,
            "correct": correct,
            "total": total,
            "percent": percent,
            "results": results,
        }
    )


@app.route("/api/search")
def api_search():
    """Search topics. Used by the sidebar when JavaScript is on."""
    query = request.args.get("q", "")
    results = content.search_topics(query)
    return jsonify(
        {
            "query": query,
            "count": len(results),
            "topics": [
                {
                    "title": t["title"],
                    "slug": t["slug"],
                    "summary": t["summary"],
                    "group": t["group"],
                }
                for t in results
            ],
        }
    )


@app.route("/api/sidebar")
def api_sidebar():
    """The full topic list, so the search box can filter without a reload."""
    return jsonify(
        {
            "groups": [
                {
                    "name": group["name"],
                    "topics": [
                        {
                            "title": t["title"],
                            "slug": t["slug"],
                            "summary": t["summary"],
                            "number": t["number"],
                        }
                        for t in group["topics"]
                    ],
                }
                for group in content.grouped_topics()
            ],
            "total": len(content.TOPIC_LIST),
        }
    )


@app.route("/api/run", methods=["POST"])
def api_run():
    """Run a beginner's snippet and hand back whatever it printed.

    Each snippet runs in its own throwaway process and its own temporary
    folder, with a short time limit. That is plenty for a learning site you
    run on your own machine, but it is NOT a security sandbox - so if you
    ever put this on the open internet, switch the runner off by starting
    the app with  PYSIMPLE_RUN_CODE=0  and put a real sandbox in front of it.
    """
    if not RUN_CODE_ENABLED:
        return (
            jsonify({"ok": False, "error": "The code runner is switched off on this server."}),
            503,
        )

    payload = request.get_json(silent=True) or {}
    source = payload.get("code", "")
    sample_input = payload.get("input", "")

    if not isinstance(source, str) or not source.strip():
        return jsonify({"ok": False, "error": "There is no code to run."}), 400

    if len(source) > CODE_SIZE_LIMIT:
        return (
            jsonify({"ok": False, "error": "That snippet is too long to run here."}),
            400,
        )

    source = source.replace("\r\n", "\n")

    # input() reads from stdin. With no sample data we hand it blank lines so
    # it simply returns an empty string instead of crashing on end of file.
    stdin_text = sample_input if sample_input.strip() else "\n" * 50

    with tempfile.TemporaryDirectory() as workdir:
        # MPLBACKEND=Agg makes plt.show() a no-op, so a chart lesson does not
        # sit there waiting for somebody to close a window.
        run_env = dict(os.environ)
        run_env["MPLBACKEND"] = "Agg"
        run_env["PYTHONIOENCODING"] = "utf-8"
        run_env["PYTHONDONTWRITEBYTECODE"] = "1"

        try:
            finished = subprocess.run(
                [sys.executable, "-I", "-B", "-c", source],
                input=stdin_text,
                capture_output=True,
                text=True,
                timeout=CODE_TIME_LIMIT,
                cwd=workdir,
                env=run_env,
            )
        except subprocess.TimeoutExpired:
            return jsonify(
                {
                    "ok": False,
                    "error": f"Your code was still going after {CODE_TIME_LIMIT} seconds, "
                    "so we stopped it. The usual cause is a loop that never ends - "
                    "check that a while loop eventually makes its condition false.",
                }
            )
        except OSError as exc:
            return jsonify({"ok": False, "error": f"Could not start Python: {exc}"}), 500

    stdout = finished.stdout[:OUTPUT_SIZE_LIMIT]
    stderr = finished.stderr[:OUTPUT_SIZE_LIMIT]

    if finished.returncode != 0:
        return jsonify(
            {
                "ok": False,
                "error": stderr.strip() or "Your code stopped with an error.",
                "stdout": stdout,
            }
        )

    return jsonify({"ok": True, "output": stdout, "error": ""})


# ----------------------------------------------------------------- errors
@app.errorhandler(404)
def not_found(_error):
    return render_template(
        "not_found.html",
        page_title="Page not found",
        **page_base()
    ), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    warm_up_libraries()
    print(f"PySimple Learn is running at http://127.0.0.1:{port}")
    app.run(debug=True, port=port)

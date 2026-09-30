# PySimple Learn

A small, clean website for learning Python from scratch. Short lessons, clear
examples with their real output, a code box you can run in the browser, a
progress bar that remembers what you finished, and a dashboard that turns that
progress into XP, ranks, badges and a plan for what to learn next.

Only HTML, CSS, JavaScript and Flask. No build step, no framework, no
JavaScript libraries, no database.

## Run it

```bash
python3 -m venv .venv          # a private folder for this project's packages
source .venv/bin/activate       # on Windows: .venv\Scripts\activate

pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser.

On macOS something else often sits on port 5000. If the browser cannot connect,
pick another one:

```bash
PORT=5055 python app.py
```

### Optional: the data libraries

The NumPy, Pandas and Matplotlib lessons are much more fun if their code can
actually run. These three are not required to start the site:

```bash
pip install numpy pandas matplotlib
```

The first matplotlib run builds a font cache, which takes a while. `app.py` does
that in the background at startup, so it is ready before you reach that lesson.

## What is in each lesson

Every topic has the same seven parts, in the same order:

1. **What this is about** - the idea in plain words
2. **Syntax** - the shape of the code you are about to write
3. **Examples** - two or three, each with its real output
4. **Try it yourself** - an editor with a Run button
5. **Output** - what your code printed, or what went wrong
6. **Small practice** - one question, a hint, and an answer
7. **Quick check** - three multiple-choice questions, marked by the server
8. **Previous / Next** - straight on to the next topic

## The dashboard

**/dashboard** is your home base. It reads one saved object out of
localStorage and works out everything from it.

- **Overall ring** - how much of the 34 topics you have finished
- **Rank** - Newcomer, Explorer, Coder, Pythonista, Debugger, Python Master
- **Skill map** - a bar per topic group, so you can see the gaps
- **Up next** - three suggestions, preferring the next unfinished topic on
  your track, then anything you finished but never tested, then a weak spot
- **Your three paths** - Beginner, Intermediate and Advanced, each with its own
  progress and a mastery marker
- **Badges** - 24 of them, locked ones showing how far along you are
- **Where you are strongest** - your top five and the five worth revisiting

### XP

| You do this | You get |
| --- | --- |
| Mark a topic as done | 20 |
| Run a snippet (once per topic per day) | 5 |
| Finish a quick check | 30 |
| Ace a quick check (100%) | +20 |
| Learn on a new day while you have a streak | 10 |

### Badges

Badges are data, not code. Each one in `data/achievements.py` has a tiny rule
string such as `done:10`, `quiz:5` or `track:beginner`, which `store.js`
checks against your saved progress. Adding a badge never means touching any
other file.

## Project layout

```
app.py                 Flask routes, the code runner and quiz marking
data/
  topics.py            all 34 lessons, as plain data
  tracks.py            the Beginner / Intermediate / Advanced paths
  quizzes.py           102 questions, three per topic
  achievements.py      XP ranks and the badge rules
templates/
  base.html            the shell: header, sidebar, footer
  home.html            the front page
  topic.html           one lesson
  dashboard.html       your progress
  not_found.html       the 404 page
static/
  css/style.css        one stylesheet, light and dark
  js/store.js          the saved progress everyone else reads
  js/main.js           theme, search, ticks, code editor
  js/dashboard.js      rings, ranks, badges, suggestions
  js/quiz.js           the quick check
  img/favicon.svg
```

All the lesson content lives in `data/topics.py`. To add a topic, copy an
existing dict and fill in the parts, add its slug to a track in `data/tracks.py`,
and add three questions in `data/quizzes.py`. Nothing else needs touching - the
sidebar, search, Previous/Next buttons, progress bar, dashboard, skill map and
badges all read from those files.

### Where your progress lives

One object in localStorage under `pysimple-progress`. Your finished topics, XP,
streak, run count and best quiz scores all live there together, and
`store.js` is the only file that writes to it. It never leaves your browser -
there is no account and no server-side record.

## Handy things

| You want to | Do this |
| --- | --- |
| Search quickly | press <kbd>/</kbd> |
| Run your code | press <kbd>Ctrl</kbd> + <kbd>Enter</kbd> |
| Switch light / dark | the button in the top right |
| Reset the lesson editor | the **Reset** button |
| Save your progress | it is automatic, in this browser only |

## About the code runner

Your code runs in a separate Python process, in a throwaway temporary folder,
with an 8 second time limit, so a runaway loop cannot hang the site.

That is plenty for running this on your own machine. **It is not a security
sandbox.** If you ever put this on the open internet, start it with
`PYSIMPLE_RUN_CODE=0` to switch the runner off, and put a real sandbox in
front of it.

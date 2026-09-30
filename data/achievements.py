"""XP ranks and the badges on the dashboard.

XP is earned by doing the thing, not by sitting on the page:
    +20  mark a topic as done
    +30  finish a topic's quick check
    +20  bonus for a perfect quiz score
    +5   run a snippet (once per topic, per day)
    +10  for every day in a learning streak

The badge "rules" below are tiny strings that the browser checks against your
saved progress, so adding a badge never means touching any other file.

Rule forms:
    done:N      mark N topics as done
    quiz:N      get a perfect score on N quizzes
    run:N       run a snippet N times
    streak:N    learn N days in a row
    xp:N        reach N XP
    group:NAME  finish every topic in a sidebar group
    track:ID    finish every topic in a learning track
    explore:N   open N different topics
"""

RANKS = [
    {"id": "newcomer", "name": "Newcomer", "min": 0, "up": 60,
     "blurb": "You have opened the book. That is the hard part over."},
    {"id": "explorer", "name": "Explorer", "min": 60, "up": 180,
     "blurb": "Variables, loops and lists are starting to look obvious."},
    {"id": "coder", "name": "Coder", "min": 180, "up": 400,
     "blurb": "You can write a small program start to finish without copying."},
    {"id": "pythonista", "name": "Pythonista", "min": 400, "up": 750,
     "blurb": "Functions, files and libraries are tools you reach for naturally."},
    {"id": "debugger", "name": "Debugger", "min": 750, "up": 1200,
     "blurb": "You read error messages as information, not as threats."},
    {"id": "master", "name": "Python Master", "min": 1200, "up": None,
     "blurb": "Everything on this site is now just a refresher."},
]


ACHIEVEMENTS = [
    # --- first steps
    {"id": "first-steps", "name": "First Steps", "mark": "1", "hue": 145,
     "desc": "Mark your first topic as done.",
     "rule": "done:1"},
    {"id": "high-five", "name": "High Five", "mark": "5", "hue": 145,
     "desc": "Finish 5 topics.",
     "rule": "done:5"},
    {"id": "double-digits", "name": "Double Digits", "mark": "10", "hue": 150,
     "desc": "Finish 10 topics.",
     "rule": "done:10"},
    {"id": "quarter-way", "name": "Quarter Way", "mark": "25%", "hue": 150,
     "desc": "Finish a quarter of all 34 topics.",
     "rule": "done:9"},
    {"id": "half-way", "name": "Halfway There", "mark": "50%", "hue": 152,
     "desc": "Finish 17 topics.",
     "rule": "done:17"},
    {"id": "grand-finish", "name": "Grand Finish", "mark": "100%", "hue": 152,
     "desc": "Finish every single topic.",
     "rule": "done:34"},

    # --- tracks and groups
    {"id": "track-beginner", "name": "Ground Solid", "mark": "B", "hue": 140,
     "desc": "Finish the whole Beginner track.",
     "rule": "track:beginner"},
    {"id": "track-intermediate", "name": "Getting Clever", "mark": "I", "hue": 160,
     "desc": "Finish the whole Intermediate track.",
     "rule": "track:intermediate"},
    {"id": "track-advanced", "name": "Full Stack of Python", "mark": "A", "hue": 168,
     "desc": "Finish the whole Advanced track.",
     "rule": "track:advanced"},
    {"id": "group-basics", "name": "First Steps Done", "mark": "G", "hue": 145,
     "desc": "Finish every topic in Getting Started.",
     "rule": "group:Getting Started"},
    {"id": "group-collections", "name": "Boxed In", "mark": "C", "hue": 155,
     "desc": "Finish every topic in Collections.",
     "rule": "group:Collections"},

    # --- running code
    {"id": "first-run", "name": "It Runs", "mark": "R", "hue": 150,
     "desc": "Run your first snippet.",
     "rule": "run:1"},
    {"id": "tinkerer", "name": "Tinkerer", "mark": "10", "hue": 152,
     "desc": "Run code 10 times.",
     "rule": "run:10"},
    {"id": "lab-coat", "name": "Lab Coat", "mark": "50", "hue": 155,
     "desc": "Run code 50 times.",
     "rule": "run:50"},
    {"id": "curious", "name": "Curious Mind", "mark": "25", "hue": 158,
     "desc": "Open 25 different topics.",
     "rule": "explore:25"},

    # --- quizzes
    {"id": "first-check", "name": "Checked", "mark": "Q", "hue": 158,
     "desc": "Finish your first quick check.",
     "rule": "quiz:1"},
    {"id": "sharp-shooter", "name": "Sharp Shooter", "mark": "5", "hue": 160,
     "desc": "Get a perfect score on 5 quick checks.",
     "rule": "quiz:5"},
    {"id": "quiz-master", "name": "Quiz Master", "mark": "12", "hue": 165,
     "desc": "Get a perfect score on 12 quick checks.",
     "rule": "quiz:12"},
    {"id": "flawless", "name": "Flawless", "mark": "100", "hue": 168,
     "desc": "Ace every quick check in one track you have finished.",
     "rule": "quiz:track"},

    # --- streaks and xp
    {"id": "streak-3", "name": "Three in a Row", "mark": "3", "hue": 145,
     "desc": "Learn 3 days in a row.",
     "rule": "streak:3"},
    {"id": "streak-7", "name": "Full Week", "mark": "7", "hue": 150,
     "desc": "Learn 7 days in a row.",
     "rule": "streak:7"},
    {"id": "streak-30", "name": "Month of Code", "mark": "30", "hue": 155,
     "desc": "Learn 30 days in a row.",
     "rule": "streak:30"},
    {"id": "xp-500", "name": "Point Five Hundred", "mark": "500", "hue": 160,
     "desc": "Reach 500 XP.",
     "rule": "xp:500"},
    {"id": "xp-1000", "name": "Four Digits", "mark": "1K", "hue": 165,
     "desc": "Reach 1000 XP.",
     "rule": "xp:1000"},
]


def rank_for(xp):
    """The rank you are in, plus the next one and how far you are towards it."""
    xp = max(0, int(xp or 0))
    current = RANKS[0]
    for rank in RANKS:
        if xp >= rank["min"]:
            current = rank
    following = None
    for rank in RANKS:
        if rank["min"] > xp:
            following = rank
            break

    if following:
        span = following["min"] - current["min"]
        percent = round((xp - current["min"]) / span * 100) if span else 100
        percent = max(0, min(100, percent))
        needed = following["min"] - xp
    else:
        percent = 100
        needed = 0

    return {
        "current": current,
        "next": following,
        "percent": percent,
        "needed": needed,
    }

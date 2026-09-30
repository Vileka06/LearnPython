"""The three learning tracks on the dashboard.

A track is just an ordered list of topic slugs, so moving a topic between
Beginner and Intermediate is a one-word change here. The dashboard reads
these to draw the path, the progress rings and the "mastery" score.
"""

TRACKS = [
    {
        "id": "beginner",
        "name": "Beginner",
        "tagline": "The building blocks",
        "blurb": "Everything you need to write your first program. Start here if "
                 "you have never used Python, or if variables and loops still feel "
                 "like guesswork.",
        "slugs": [
            "introduction",
            "syntax",
            "comments",
            "variables",
            "data-types",
            "numbers",
            "casting",
            "strings",
            "booleans",
            "operators",
            "lists",
            "if-else",
            "user-input",
            "try-except",
        ],
    },
    {
        "id": "intermediate",
        "name": "Intermediate",
        "tagline": "Shaping real programs",
        "blurb": "The tools you reach for once a script does more than one thing: "
                 "grouping data, reusing code, reading files and working with text.",
        "slugs": [
            "tuples",
            "sets",
            "dictionaries",
            "while-loops",
            "for-loops",
            "functions",
            "modules",
            "dates",
            "math",
            "file-handling",
            "json",
            "regex",
            "lambda",
        ],
    },
    {
        "id": "advanced",
        "name": "Advanced",
        "tagline": "Bigger ideas",
        "blurb": "Objects, the tools that hold a project together, and the libraries "
                 "that turn data into something worth looking at.",
        "slugs": [
            "classes",
            "inheritance",
            "pip",
            "virtual-environment",
            "numpy",
            "pandas",
            "matplotlib",
        ],
    },
]


def track_of(slug):
    """Which track does this topic belong to? Returns None if it is not listed."""
    for track in TRACKS:
        if slug in track["slugs"]:
            return track
    return None


def all_slugs():
    """Every slug that has been placed on a track."""
    return [slug for track in TRACKS for slug in track["slugs"]]


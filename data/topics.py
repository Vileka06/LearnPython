"""All PySimple Learn lesson content lives here.

Each topic is a plain dict so it is easy to read and edit.
Nothing in this file is fancy Python - it is just data.

Shape of a topic:
    {
        "title":      str,          # shown in the sidebar
        "group":      str,          # sidebar section name
        "summary":    str,          # one short line, used on the home page
        "intro":      [str, ...],   # simple explanation, one string per paragraph
        "syntax":     str or None,  # the generic pattern
        "examples":   [ { "title", "code", "output" } ],
        "practice":   { "question", "hint", "answer" },
        "search":     [str, ...],   # extra words the search box should match
    }
"""

import textwrap


def code(text):
    """Clean up a code block written in this file."""
    return textwrap.dedent(text).strip("\n")


def _ex(title, code_text, output, terminal=False):
    """One example. terminal=True means the code is a shell command, not Python."""
    return {
        "title": title,
        "code": code(code_text),
        "output": code(output),
        "terminal": terminal,
    }


def _practice(question, hint, answer):
    return {
        "question": question,
        "hint": hint,
        "answer": code(answer),
    }


GROUPS = [
    "Getting Started",
    "Text & Logic",
    "Collections",
    "Conditions & Loops",
    "Functions",
    "Objects",
    "Tools & Libraries",
]

TOPICS = [
    # ---------------------------------------------------------------- basics
    {
        "title": "Introduction",
        "group": "Getting Started",
        "summary": "What Python is, and how to run your first line of code.",
        "intro": [
            "Python is a programming language: you write instructions in plain text, "
            "and Python follows them. It is used for websites, games, data analysis, "
            "automation and AI - but it all starts with one line at a time.",
            "Python is <em>case sensitive</em>, so <code>print</code> and <code>Print</code> "
            "are not the same. It also cares about indentation, which is how Python knows "
            "which lines belong together.",
            "The <code>print()</code> function displays something on the screen. It is the "
            "first thing you should get comfortable with, because you can use it to see "
            "what your code is actually doing.",
        ],
        "syntax": code("""
            print("Hello, world!")
        """),
        "examples": [
            _ex("Say hello", 'print("Hello, world!")', "Hello, world!"),
            _ex("Print several lines", 'print("I am learning Python.")\nprint("It is fun.")',
                "I am learning Python.\nIt is fun."),
            _ex("Numbers work too", "print(10 + 5)", "15"),
        ],
        "practice": _practice(
            "Print your own name on one line, then print your favourite colour on the next line.",
            "Call print() twice.",
            'print("Your name here")\nprint("blue")',
        ),
        "search": ["hello world", "first program", "begin", "start", "basics"],
    },
    {
        "title": "Syntax",
        "group": "Getting Started",
        "summary": "The basic rules Python expects from your code.",
        "intro": [
            "Syntax simply means <em>the rules of the language</em>. Python is strict about "
            "a few small things, and once you learn them the error messages make much more sense.",
            "Most lines are <code>statement</code>s. A line that gives a variable no spaces "
            "around <code>=</code> (no equality check) and spaces around <code>==</code> "
            "(a comparison). Indentation of four spaces marks a block of code.",
        ],
        "syntax": code("""
            # rule 1: case sensitive
            Name = "Vicky"          # ok
            print(name)              # Error! name is different from Name

            # rule 2: indentation
            if True:
                print("inside the block")

            # rule 3: no semicolons needed
            a = 1
            b = 2
        """),
        "examples": [
            _ex("No semicolons needed", 'a = 10\nb = 20\ntotal = a + b\nprint(total)', "30"),
            _ex("Indentation marks a block",
                'temperature = 30\nif temperature > 25:\n    print("It is warm")',
                "It is warm"),
            _ex("Case matters", 'fruit = "apple"\nprint(FRUIT)', "NameError: name 'FRUIT' is not defined"),
        ],
        "practice": _practice(
            "Create the variable <code>score</code> with the value 42 and print it.",
            "One line: score = 42, then print(score).",
            "score = 42\nprint(score)",
        ),
        "search": ["rules", "indentation", "case sensitive", "semicolon"],
    },
    {
        "title": "Comments",
        "group": "Getting Started",
        "summary": "Notes for humans that Python ignores completely.",
        "intro": [
            "A comment is a note you leave in your code for yourself or for other people. "
            "Python skips over it, so it changes nothing about your program.",
            "A comment starts with <code>#</code> and continues to the end of the line. "
            "Comments are one of the easiest habits to build, and they save you a lot of "
            "confusion later.",
        ],
        "syntax": code("""
            # this is a single line comment

            # you can also write a longer note
            # across several lines

            print("Comments are ignored")  # this part is ignored too
        """),
        "examples": [
            _ex("Single line comment", '# Store the price\nprice = 49\nprint(price)', "49"),
            _ex("Comment at the end of a line",
                'x = 5  # x starts at 5\nx = x * 2  # then we double it\nprint(x)', "10"),
            _ex("Ignore a line while learning",
                '# print("this one is switched off")\nprint("this one runs")', "this one runs"),
        ],
        "practice": _practice(
            "Add a comment above a line that prints <code>\"Saved!\"</code> and a second "
            "comment after it on the same line.",
            "Both comments start with #. One is on its own line, one is at the end.",
            '# Preparing the message\nprint("Saved!")  # always show the message',
        ),
        "search": ["hash", "note", "hashbang"],
    },
    {
        "title": "Variables",
        "group": "Getting Started",
        "summary": "Named boxes that hold values while your program runs.",
        "intro": [
            "A variable is a name for a value. Instead of writing <code>365</code> over and "
            "over, you write <code>days_in_year</code> once and reuse the name.",
            "You create a variable with <code>=</code>. Python figures out the type from the "
            "value, so you never have to declare it. Names should be short, lowercase and "
            "descriptive.",
        ],
        "syntax": code("""
            name = "Vicky"          # text
            age = 20                # whole number
            height = 1.65           # decimal number
            student = True          # yes / no

            print(name, age, height, student)
        """),
        "examples": [
            _ex("Create and print", 'name = "Vicky"\nage = 20\nprint(name)\nprint(age)',
                "Vicky\n20"),
            _ex("Change a value later", 'score = 0\nscore = score + 10\nprint(score)', "10"),
            _ex("Many names in one line", "a, b, c = 1, 2, 3\nprint(a, b, c)", "1 2 3"),
        ],
        "practice": _practice(
            "Make a variable called <code>city</code> holding your city, and a variable called "
            "<code>population</code> holding any number. Print both in one line.",
            "Two assignments, then print(city, population).",
            'city = "London"\npopulation = 9000000\nprint(city, population)',
        ),
        "search": ["assignment", "equals", "naming", "store"],
    },
    {
        "title": "Data Types",
        "group": "Getting Started",
        "summary": "The kinds of values Python can hold.",
        "intro": [
            "Every value in Python has a <em>type</em>. A name, a number and a yes/no answer "
            "are different types, and Python treats each one differently.",
            "The built-in types you will use most are <code>str</code> (text), <code>int</code> "
            "and <code>float</code> (numbers), <code>bool</code> (yes/no) and the collection "
            "types <code>list</code>, <code>tuple</code>, <code>set</code> and <code>dict</code>.",
            "The <code>type()</code> function tells you what you are holding.",
        ],
        "syntax": code("""
            name = "Vicky"     # str  - text
            age = 20           # int  - whole number
            height = 1.65      # float - decimal number
            student = True     # bool - True or False
            hobbies = ["chess", "cycling"]   # list

            print(type(age))   # <class 'int'>
        """),
        "examples": [
            _ex("Check the type", 'print(type("hello"))\nprint(type(10))\nprint(type(3.5))\nprint(type(True))',
                "<class 'str'>\n<class 'int'>\n<class 'float'>\n<class 'bool'>"),
            _ex("Text vs number sizes",
                'print(len("hello"))   # characters in the text\nprint(len([10, 20, 30]))   # items in the list',
                "5\n3"),
        ],
        "practice": _practice(
            "Create one value of each of these types and print their types: a name, an age, a height.",
            "str, int and float - then call type() on each one.",
            'name = "Sam"\nage = 30\nheight = 1.8\nprint(type(name))\nprint(type(age))\nprint(type(height))',
        ),
        "search": ["str", "int", "float", "bool", "type()", "classes of data"],
    },
    {
        "title": "Numbers",
        "group": "Getting Started",
        "summary": "Whole numbers, decimals and the maths you can do on them.",
        "intro": [
            "Python has two everyday number types. <code>int</code> is a whole number such as 5, "
            "and <code>float</code> is a decimal such as 5.0. You can mix them freely.",
            "There is also <code>complex</code> for maths with imaginary numbers, but you can "
            "leave that for later. Use <code>//</code> for a whole-number answer and "
            "<code>%</code> for the remainder.",
        ],
        "syntax": code("""
            a = 10          # int
            b = 3.5         # float

            print(a + b)    # 13.5   add
            print(a - b)    # 6.5    subtract
            print(a * b)    # 35.0   multiply
            print(a / b)    # 2.85   divide (always gives float)
            print(a // b)   # 2.0    divide, drop the decimals
            print(a % b)    # 3.0    remainder
            print(a ** 2)   # 100    power
        """),
        "examples": [
            _ex("The basics", "print(7 + 3)\nprint(7 - 3)\nprint(7 * 3)", "10\n4\n21"),
            _ex("Divisions and remainders",
                "print(17 / 4)\nprint(17 // 4)\nprint(17 % 4)", "4.25\n4\n1"),
            _ex("Rounding a decimal", "print(round(3.14159, 2))\nprint(round(2.5))", "3.14\n2"),
        ],
        "practice": _practice(
            "Two pizzas cost 24 pounds. Print how much one costs, using a division.",
            "Use / to divide, and name the result how you like.",
            "total = 24\nprint(total / 2)",
        ),
        "search": ["int", "float", "arithmetic", "math operators", "modulo", "power"],
    },
    {
        "title": "Casting",
        "group": "Getting Started",
        "summary": "Turning one type of value into another type.",
        "intro": [
            "Casting means <em>converting</em> a value from one type to another. It is how you "
            "turn the text someone typed into a number you can add up.",
            "Use <code>int()</code>, <code>float()</code> and <code>str()</code>. Casting text "
            "that is not a real number raises a <code>ValueError</code>, which is why "
            "<code>input()</code> needs help.",
        ],
        "syntax": code("""
            print(int("50") + 5)      # 55   (text becomes a number)
            print(float("3.5") * 2)   # 7.0
            print(str(99) + " bottles")  # 99 bottles (number becomes text)
        """),
        "examples": [
            _ex("Text to number",
                'age_text = "21"\nage = int(age_text)\nprint(age + 1)', "22"),
            _ex("Number to text",
                'score = 100\nprint("You scored " + str(score))', "You scored 100"),
            _ex("Input always gives text",
                'number = int(input("Number: "))\nprint(number * 2)', "Number: 5\n10"),
        ],
        "practice": _practice(
            "Turn the text <code>\"9.5\"</code> into a float, then multiply it by 2 and print the result.",
            "float() converts the text, then * 2 multiplies it.",
            'value = float("9.5")\nprint(value * 2)',
        ),
        "search": ["convert", "type conversion", "int()", "float()", "str()"],
    },

    # ------------------------------------------------------ text and logic
    {
        "title": "Strings",
        "group": "Text & Logic",
        "summary": "Working with text: joining, slicing and cleaning it.",
        "intro": [
            "A string is text held in quotes. Single or double quotes both work, and they mean "
            "exactly the same thing.",
            "Strings have their own little language. Indexing starts at 0, negative indexes "
            "count from the end, and slicing <code>[start:stop]</code> grabs a piece. There are "
            "also handy methods such as <code>upper()</code>, <code>strip()</code> and "
            "<code>split()</code>.",
        ],
        "syntax": code("""
            text = "Python"

            print(text.upper())       # PYTHON
            print(text[0])            # P        (first character)
            print(text[-1])           # n        (last character)
            print(text[1:4])          # yth      (characters 1, 2, 3)
            print(len(text))          # 6        (how many characters)
            print(text + " rocks")    # Python rocks
            print(f"I love {text}")   # f-strings put values inside text
        """),
        "examples": [
            _ex("Slicing a word",
                'word = "banana"\nprint(word[:3])\nprint(word[3:])\nprint(word[1:5])',
                "ban\nana\nanan"),
            _ex("Cleaning user text",
                'raw = "   Vicky   "\nprint(raw.strip())\nprint(raw.strip().lower())',
                "Vicky\nvicky"),
            _ex("Splitting and joining",
                'tags = "python, code, learn".split(", ")\nprint(tags)\nprint("-".join(tags))',
                "['python', 'code', 'learn']\npython-code-learn"),
        ],
        "practice": _practice(
            "Take the text <code>\"  Hello World  \"</code>, remove the extra spaces, and print "
            "it in capital letters.",
            "Chain two methods: .strip() then .upper().",
            'raw = "  Hello World  "\nprint(raw.strip().upper())',
        ),
        "search": ["text", "f-string", "slice", "index", "upper", "lower", "strip", "split", "join"],
    },
    {
        "title": "Booleans",
        "group": "Text & Logic",
        "summary": "The two values True and False used for decisions.",
        "intro": [
            "A boolean is simply <code>True</code> or <code>False</code> - capital T and F. "
            "They answer yes/no questions and drive the <code>if</code> statements you will "
            "write next.",
            "Comparisons produce booleans. Be careful with <code>=</code> (assign) versus "
            "<code>==</code> (compare).",
        ],
        "syntax": code("""
            print(5 > 3)        # True
            print(5 == 3)       # False   (same value?)
            print(5 != 3)       # True    (different values?)

            is_raining = True
            print(is_raining)   # True
        """),
        "examples": [
            _ex("Comparisons give booleans",
                "print(10 > 20)\nprint(10 >= 10)\nprint(\"a\" == \"a\")", "False\nTrue\nTrue"),
            _ex("Boolean variables",
                'logged_in = True\nif logged_in:\n    print("Welcome back!")', "Welcome back!"),
            _ex("Not is the opposite", "print(not True)\nprint(not (3 > 5))", "False\nTrue"),
        ],
        "practice": _practice(
            "Print whether the number 15 is greater than 10, and print the opposite of the "
            "statement <code>3 == 3</code>.",
            "One comparison, then wrap the second in not.",
            "print(15 > 10)\nprint(not (3 == 3))",
        ),
        "search": ["true", "false", "yes no", "comparison", "not"],
    },
    {
        "title": "Operators",
        "group": "Text & Logic",
        "summary": "The symbols Python uses to compare and combine values.",
        "intro": [
            "Operators are the symbols that do the work. There are three families worth knowing "
            "on day one: <strong>arithmetic</strong> (+, -, *, /), <strong>comparison</strong> "
            "(==, !=, &lt;, &gt;) and <strong>logical</strong> (and, or, not).",
            "<code>and</code> needs both sides to be true, <code>or</code> needs only one. "
            "Python also supports <code>+=</code> style shortcuts that update a variable in place.",
        ],
        "syntax": code("""
            x = 10
            y = 3

            print(x + y, x - y, x * y, x / y)    # arithmetic
            print(x > y, x == y, x != y)          # comparison

            print(x > 5 and y < 5)   # True
            print(x > 50 or y < 5)   # True
            print(not x == y)        # True

            x += 5      # same as x = x + 5
            print(x)     # 15
        """),
        "examples": [
            _ex("Arithmetic", "a, b = 12, 4\nprint(a + b, a - b, a * b, a / b)", "16 8 48 3.0"),
            _ex("Comparison", "print(5 == 5.0)\nprint(3 > 7)\nprint(3 <= 3)", "True\nFalse\nTrue"),
            _ex("Logical", "age = 22\nprint(age >= 18 and age <= 65)", "True"),
        ],
        "practice": _practice(
            "You are 16 years old. Use <code>and</code> to print whether you are both under 18 "
            "and over 10.",
            "Join two comparisons with and.",
            "age = 16\nprint(age < 18 and age > 10)",
        ),
        "search": ["arithmetic", "comparison", "logical", "and", "or", "not", "symbols"],
    },

    # -------------------------------------------------------- collections
    {
        "title": "Lists",
        "group": "Collections",
        "summary": "An ordered, changeable group of values.",
        "intro": [
            "A list holds several values in order, written in square brackets and separated by "
            "commas. A list can hold any mix of types and you can change it after you make it.",
            "Items are found by position starting at 0, positions can be negative to count from "
            "the end, and slices work the same way as in strings. The list has a long list of "
            "handy <em>methods</em> like <code>append()</code> and <code>sort()</code>.",
        ],
        "syntax": code("""
            fruits = ["apple", "banana", "cherry"]

            fruits.append("date")      # add to the end
            print(fruits[0])           # apple
            print(fruits[-1])          # date
            print(len(fruits))         # 4
            fruits[1] = "blueberry"    # change an item
            print(fruits)
        """),
        "examples": [
            _ex("Build and add",
                'scores = [10, 20, 30]\nscores.append(40)\nprint(scores)',
                "[10, 20, 30, 40]"),
            _ex("Change, remove, insert",
                'letters = ["b", "d", "e"]\nletters[0] = "c"\nletters.remove("d")\nletters.insert(1, "z")\nprint(letters)',
                "['c', 'z', 'e']"),
            _ex("Sum and average",
                "marks = [60, 70, 80, 90]\nprint(sum(marks))\nprint(sum(marks) / len(marks))",
                "300\n75.0"),
        ],
        "practice": _practice(
            "Make a list of three fruits. Add a fourth to the end, then print the whole list "
            "and its length.",
            "Start with a list, call .append(), then print both the list and len().",
            'fruits = ["apple", "banana", "cherry"]\nfruits.append("date")\nprint(fruits)\nprint(len(fruits))',
        ),
        "search": ["array", "collection", "append", "index", "slice"],
    },
    {
        "title": "Tuples",
        "group": "Collections",
        "summary": "An ordered group you cannot change after making it.",
        "intro": [
            "A tuple looks like a list but uses round brackets. The big difference is that a "
            "tuple is <em>immutable</em> - once it exists you cannot add, remove or change items.",
            "That is useful for things that should not move, like a fixed position, a date, or "
            "a dictionary key. Unpacking is the nicest part: you can put the values straight "
            "into variables in one line.",
        ],
        "syntax": code("""
            point = (3, 5)
            colours = ("red", "green", "blue")

            print(point[0])        # 3
            print(len(colours))    # 3

            x, y = point           # unpacking
            print(x, y)            # 3 5

            point[0] = 10          # Error! tuples cannot be changed
        """),
        "examples": [
            _ex("Unpacking", "name, age, city = (\"Vicky\", 20, \"Leeds\")\nprint(name)\nprint(age, city)",
                "Vicky\n20 Leeds"),
            _ex("One value needs a comma",
                'single = (5,)\nprint(type(single))', "<class 'tuple'>"),
            _ex("Swapping values", "a, b = 1, 2\na, b = b, a\nprint(a, b)", "2 1"),
        ],
        "practice": _practice(
            "Create a tuple holding three colours and print only the second one.",
            "Use round brackets, then index 1.",
            'colours = ("red", "green", "blue")\nprint(colours[1])',
        ),
        "search": ["immutable", "unpacking", "brackets", "fixed"],
    },
    {
        "title": "Sets",
        "group": "Collections",
        "summary": "An unordered group with no duplicates.",
        "intro": [
            "A set is written with curly brackets. It keeps values in no particular order and, "
            "very usefully, it never keeps the same value twice.",
            "Sets are the right tool when you want to compare two groups: you can ask what is "
            "in both, what is only in one, and what is in either.",
            "Because the order is not guaranteed, the printed result can come out in a "
            "different sequence each time. That is not a bug - it is simply how sets work. If "
            "you want a predictable order, wrap the result in <code>sorted()</code>.",
        ],
        "syntax": code("""
            tags = {"python", "code", "python"}   # the duplicate is dropped
            print(tags)                  # only one "python" survives

            a = {1, 2, 3}
            b = {3, 4, 5}

            print(a & b)   # 3        in both
            print(a | b)   # 1 2 3 4 5   in either
            print(a - b)   # 1 2      only in a
        """),
        "examples": [
            _ex("Duplicates disappear",
                'numbers = [1, 2, 2, 3, 3, 3]\nprint(set(numbers))', "{1, 2, 3}"),
            _ex("Find common items",
                'mine = {"tea", "code", "walk"}\nyours = {"code", "walk", "music"}\nprint(sorted(mine & yours))',
                "['code', 'walk']"),
            _ex("Add and discard",
                'letters = {"a", "b"}\nletters.add("c")\nletters.discard("a")\nprint(sorted(letters))',
                "['b', 'c']"),
        ],
        "practice": _practice(
            "Make two sets of colours and print the colours that appear in both of them.",
            "Use & between the two sets.",
            'mine = {"red", "blue", "green"}\nyours = {"blue", "green", "pink"}\nprint(mine & yours)',
        ),
        "search": ["unique", "curly brackets", "set operations", "no duplicates"],
    },
    {
        "title": "Dictionaries",
        "group": "Collections",
        "summary": "Key and value pairs - like a tiny contact book.",
        "intro": [
            "A dictionary stores <em>pairs</em>: a <code>key</code> you look something up by, "
            "and a <code>value</code> you get back. Keys are unique, values can repeat.",
            "You reach a value with square brackets, and unlike a list there is no numeric "
            "position. A <code>.get()</code> lookup with a fallback stops a missing key from "
            "crashing your program.",
        ],
        "syntax": code("""
            person = {"name": "Vicky", "age": 20, "city": "Leeds"}

            print(person["name"])        # Vicky
            person["job"] = "student"    # add a new pair
            print(person.get("age"))     # 20
            print(person.get("email", "no email saved"))

            for key, value in person.items():
                print(key, "->", value)
        """),
        "examples": [
            _ex("Counting letters",
                'counts = {}\nfor letter in "banana":\n    counts[letter] = counts.get(letter, 0) + 1\nprint(counts)',
                "{'b': 1, 'a': 3, 'n': 2}"),
            _ex("Keys, values and membership",
                'fruit = {"name": "apple", "colour": "red"}\nprint(fruit.keys())\nprint(fruit.values())\nprint("colour" in fruit)',
                "dict_keys(['name', 'colour'])\ndict_values(['apple', 'red'])\nTrue"),
            _ex("Updating and removing",
                'settings = {"theme": "light", "volume": 5}\nsettings["theme"] = "dark"\nsettings.pop("volume")\nprint(settings)',
                "{'theme': 'dark'}"),
        ],
        "practice": _practice(
            "Create a dictionary with your name and your age, then print just the name.",
            "Keys in quotes, colon between key and value.",
            'me = {"name": "Vicky", "age": 20}\nprint(me["name"])',
        ),
        "search": ["dict", "key value", "items", "get", "mapping"],
    },

    # ------------------------------------------------ conditions and loops
    {
        "title": "If Else",
        "group": "Conditions & Loops",
        "summary": "Choose what happens next based on a question.",
        "intro": [
            "An <code>if</code> statement runs a block only when a condition is true. Add "
            "<code>elif</code> for extra checks and <code>else</code> for everything left over.",
            "Indentation is what defines the block. Colons end the condition, and Python is "
            "strict about the four spaces after them.",
        ],
        "syntax": code("""
            age = 20

            if age >= 18:
                print("You can vote")
            elif age >= 13:
                print("You are a teenager")
            else:
                print("You are a child")
        """),
        "examples": [
            _ex("Pass or fail",
                "score = 72\nif score >= 50:\n    print(\"Passed\")\nelse:\n    print(\"Try again\")",
                "Passed"),
            _ex("Several branches",
                "temp = 28\nif temp > 30:\n    print(\"Hot\")\nelif temp > 20:\n    print(\"Warm\")\nelse:\n    print(\"Cool\")",
                "Warm"),
            _ex("One-line shortcut",
                'status = "pass"\nmessage = "Great!" if status == "pass" else "Keep going"\nprint(message)',
                "Great!"),
        ],
        "practice": _practice(
            "Ask for a number and print <code>\"Positive\"</code>, <code>\"Zero\"</code> or "
            "<code>\"Negative\"</code> depending on what was typed.",
            "Use input() plus int(), then if / elif / else.",
            """n = int(input("Number: "))
if n > 0:
    print("Positive")
elif n == 0:
    print("Zero")
else:
    print("Negative")""",
        ),
        "search": ["condition", "branch", "elif", "conditional", "indentation"],
    },
    {
        "title": "While Loops",
        "group": "Conditions & Loops",
        "summary": "Repeat as long as something stays true.",
        "intro": [
            "A <code>while</code> loop keeps running its block for as long as the condition is "
            "true. When the condition becomes false, it stops.",
            "The danger is forgetting to change something inside the loop. If the condition "
            "never changes you get an <em>infinite loop</em>, and only Ctrl+C will stop it. "
            "Always make sure the condition moves towards being false.",
        ],
        "syntax": code("""
            count = 1

            while count <= 5:
                print(count)
                count = count + 1      # without this, it never ends

            # break leaves straight away, continue skips to the next round
            while True:
                if count > 10:
                    break
                count += 1
        """),
        "examples": [
            _ex("Count 1 to 3",
                "n = 1\nwhile n <= 3:\n    print(n)\n    n += 1", "1\n2\n3"),
            _ex("A countdown",
                "n = 3\nwhile n > 0:\n    print(n)\n    n -= 1\nprint(\"Liftoff!\")",
                "3\n2\n1\nLiftoff!"),
            _ex("Leaving early with break",
                "n = 0\nwhile True:\n    n += 1\n    if n == 3:\n        break\nprint(n)", "3"),
        ],
        "practice": _practice(
            "Start at 5 and count down to 1, printing each number, then print <code>\"Done\"</code>.",
            "while n > 0, then n -= 1 inside the loop.",
            "n = 5\nwhile n > 0:\n    print(n)\n    n -= 1\nprint(\"Done\")",
        ),
        "search": ["repeat", "loop", "break", "continue", "infinite"],
    },
    {
        "title": "For Loops",
        "group": "Conditions & Loops",
        "summary": "Step through a group of things, one at a time.",
        "intro": [
            "A <code>for</code> loop visits each item in a sequence - a list, a string, a range "
            "- and runs the block once per item. You do not manage a counter yourself.",
            "<code>range()</code> is the usual way to loop a set number of times. "
            "<code>range(5)</code> gives 0 to 4; <code>range(2, 8)</code> gives 2 to 7; "
            "<code>range(0, 10, 2)</code> counts 0, 2, 4, 6, 8.",
        ],
        "syntax": code("""
            for name in ["ana", "ben", "cai"]:
                print(name)

            for i in range(3):        # 0, 1, 2
                print(i)

            for char in "hi":
                print(char)
        """),
        "examples": [
            _ex("Loop over a list",
                'fruits = ["apple", "banana", "cherry"]\nfor fruit in fruits:\n    print("I like", fruit)',
                "I like apple\nI like banana\nI like cherry"),
            _ex("Count with range",
                "for i in range(1, 4):\n    print(i, i * i)", "1 1\n2 4\n3 9"),
            _ex("Add up a list",
                "numbers = [4, 5, 6]\ntotal = 0\nfor n in numbers:\n    total += n\nprint(total)", "15"),
        ],
        "practice": _practice(
            "Print the numbers 1, 2, 3, 4 - but use a <code>for</code> loop and <code>range</code>.",
            "range(1, 5) gives 1 up to 4.",
            "for i in range(1, 5):\n    print(i)",
        ),
        "search": ["iterate", "loop", "range", "each item"],
    },

    # ---------------------------------------------------------- functions
    {
        "title": "Functions",
        "group": "Functions",
        "summary": "Reusable blocks of code you name and call.",
        "intro": [
            "A function is a named block of code. You define it once with <code>def</code> and "
            "call it whenever you need it. It keeps long programs organised and stops you "
            "repeating yourself.",
            "<code>Parameters</code> are the names in the brackets, and <code>arguments</code> "
            "are the values you pass in. If you do not say <code>return</code>, the function "
            "gives back <code>None</code>.",
        ],
        "syntax": code("""
            def greet(name):
                return "Hello, " + name

            message = greet("Vicky")   # call it
            print(message)

            def add(a, b=10):         # b is optional
                return a + b

            print(add(5))              # 15
            print(add(5, 3))           # 8
        """),
        "examples": [
            _ex("No arguments",
                "def say_hi():\n    print(\"Hi there!\")\n\nsay_hi()\nsay_hi()", "Hi there!\nHi there!"),
            _ex("Arguments and a return value",
                "def area(width, height):\n    return width * height\n\nprint(area(3, 4))\nprint(area(10, 2))",
                "12\n20"),
            _ex("A default value",
                "def greet(name, greeting=\"Hello\"):\n    return f\"{greeting}, {name}!\"\n\nprint(greet(\"Vicky\"))\nprint(greet(\"Vicky\", \"Good morning\"))",
                "Hello, Vicky!\nGood morning, Vicky!"),
        ],
        "practice": _practice(
            "Write a function called <code>double</code> that takes a number and returns it "
            "doubled. Print <code>double(4)</code>.",
            "def, an argument, and return the value times 2.",
            "def double(n):\n    return n * 2\n\nprint(double(4))",
        ),
        "search": ["def", "return", "argument", "parameter", "reusable", "call"],
    },
    {
        "title": "Lambda",
        "group": "Functions",
        "summary": "A tiny one-line function for small jobs.",
        "intro": [
            "A <code>lambda</code> is a function written on one line. It has no name, so you "
            "normally give it one: <code>square = lambda n: n * n</code>.",
            "Use it when the function is short and you plan to pass it straight into something "
            "like <code>sorted()</code>. For anything longer, a normal <code>def</code> is "
            "clearer.",
        ],
        "syntax": code("""
            square = lambda n: n * n
            print(square(5))            # 25

            add = lambda a, b: a + b
            print(add(2, 3))            # 5

            numbers = [4, 1, 8, 3]
            print(sorted(numbers, key=lambda n: -n))   # biggest first
        """),
        "examples": [
            _ex("Square a number", "square = lambda n: n * n\nprint(square(5))", "25"),
            _ex("Sort by length",
                'words = ["pear", "fig", "banana"]\nprint(sorted(words, key=lambda w: len(w)))',
                "['fig', 'pear', 'banana']"),
            _ex("Two arguments",
                "add = lambda a, b: a + b\nprint(add(2, 3))", "5"),
        ],
        "practice": _practice(
            "Write a lambda that triples a number, then print the result for 7.",
            'cube = lambda n: n * 3, then print(cube(7)).',
            "cube = lambda n: n * 3\nprint(cube(7))",
        ),
        "search": ["anonymous", "one line function", "short function", "sort key"],
    },

    # ------------------------------------------------------------ objects
    {
        "title": "Classes",
        "group": "Objects",
        "summary": "Blueprints for making your own objects with data and behaviour.",
        "intro": [
            "A class is a blueprint. It describes what every object of that kind should know "
            "and be able to do. <code>__init__</code> runs when an object is made and sets up "
            "its data - think of a car's dashboard being filled in.",
            "<code>self</code> means 'this particular object'. It is how methods read and write "
            "the values stored on the object.",
        ],
        "syntax": code("""
            class Dog:
                def __init__(self, name, age):
                    self.name = name      # data
                    self.age = age

                def bark(self):           # behaviour
                    return self.name + " says woof"

                def birthday(self):
                    self.age += 1

            rex = Dog("Rex", 4)
            print(rex.name)          # Rex
            print(rex.bark())        # Rex says woof
            rex.birthday()
            print(rex.age)           # 5
        """),
        "examples": [
            _ex("A simple class",
                'class Cat:\n    def __init__(self, name):\n        self.name = name\n    def speak(self):\n        return self.name + " says meow"\n\nmimi = Cat("Mimi")\nprint(mimi.speak())',
                "Mimi says meow"),
            _ex("A rectangle that measures itself",
                "class Rectangle:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n    def area(self):\n        return self.w * self.h\n\nr = Rectangle(3, 4)\nprint(r.area())",
                "12"),
            _ex("A counter with state",
                "class Counter:\n    def __init__(self):\n        self.count = 0\n    def add(self):\n        self.count += 1\n        return self.count\n\nc = Counter()\nprint(c.add())\nprint(c.add())",
                "1\n2"),
        ],
        "practice": _practice(
            "Make a class <code>Book</code> that stores a title, and give it a method "
            "<code>show()</code> that prints the title.",
            "__init__ takes self and the title; the method returns or prints it.",
            "class Book:\n    def __init__(self, title):\n        self.title = title\n    def show(self):\n        print(\"Title:\", self.title)\n\nb = Book(\"Python Basics\")\nb.show()",
        ),
        "search": ["object", "oop", "init", "self", "method", "attribute", "blueprint"],
    },
    {
        "title": "Inheritance",
        "group": "Objects",
        "summary": "Make a new class that reuses another class.",
        "intro": [
            "Inheritance lets you build a specialised class on top of an existing one. The new "
            "class gets everything the parent has, and you add or change what you need.",
            "Use <code>super().__init__()</code> to run the parent's setup first. This keeps "
            "shared code in one place instead of copying it.",
        ],
        "syntax": code("""
            class Animal:
                def __init__(self, name):
                    self.name = name
                def speak(self):
                    return "..."

            class Dog(Animal):          # Dog is an Animal
                def __init__(self, name, breed):
                    super().__init__(name)   # set up the parent
                    self.breed = breed
                def speak(self):            # replace the parent version
                    return self.name + " says woof"

            rex = Dog("Rex", "Collie")
            print(rex.name)      # Rex
            print(rex.speak())    # Rex says woof
        """),
        "examples": [
            _ex("A child class",
                'class Animal:\n    def speak(self):\n        return "..."\n\nclass Bird(Animal):\n    def speak(self):\n        return "tweet"\n\nprint(Bird().speak())',
                "tweet"),
            _ex("Adding to the parent",
                "class Vehicle:\n    def __init__(self, wheels):\n        self.wheels = wheels\n\nclass Bike(Vehicle):\n    def describe(self):\n        return f\"A bike with {self.wheels} wheels\"\n\nprint(Bike(2).describe())",
                "A bike with 2 wheels"),
            _ex("Checking the family",
                "class A:\n    pass\n\nclass B(A):\n    pass\n\nprint(issubclass(B, A))", "True"),
        ],
        "practice": _practice(
            "Make a parent class <code>Shape</code> with a <code>name</code>, and a child class "
            "<code>Square</code> that adds an <code>side</code> and an <code>area()</code> method.",
            "Call super().__init__() in the child, then multiply side by itself.",
            "class Shape:\n    def __init__(self, name):\n        self.name = name\n\nclass Square(Shape):\n    def __init__(self, side):\n        super().__init__(\"square\")\n        self.side = side\n    def area(self):\n        return self.side * self.side\n\ns = Square(4)\nprint(s.name, s.area())",
        ),
        "search": ["child class", "parent", "super", "subclass", "extend", "override"],
    },

    # ------------------------------------------------- tools and libraries
    {
        "title": "Modules",
        "group": "Tools & Libraries",
        "summary": "Borrow code that other people already wrote.",
        "intro": [
            "A module is a Python file that ends in <code>.py</code>. You can split a big "
            "program into modules to keep things tidy, and you can also use the modules that "
            "come with Python.",
            "<code>import</code> brings the whole module in, and <code>from ... import</code> "
            "brings in just the part you want. Check <code>module.__name__</code> to see the "
            "name a file is known by.",
        ],
        "syntax": code("""
            import math
            print(math.sqrt(16))          # 4.0

            from math import pi           # just one piece
            print(pi)

            import random
            print(random.randint(1, 6))   # a dice roll

            # your own files work the same way
            # import my_helpers
        """),
        "examples": [
            _ex("Use a built-in module",
                "import math\nprint(math.floor(3.7))\nprint(math.ceil(3.2))", "3\n4"),
            _ex("Import one thing",
                "from math import sqrt, floor\nprint(sqrt(81))\nprint(floor(6.9))", "9.0\n6"),
            _ex("Random numbers",
                "import random\nprint(random.choice([\"rock\", \"paper\", \"scissors\"]))\nprint(random.randint(1, 10))",
                "Output is different every time"),
        ],
        "practice": _practice(
            "Import the <code>math</code> module and print the square root of 144.",
            "import math, then math.sqrt(144).",
            "import math\nprint(math.sqrt(144))",
        ),
        "search": ["import", "library", "file", "stdlib", "from"],
    },
    {
        "title": "Dates",
        "group": "Tools & Libraries",
        "summary": "Work with today's date, times and time zones.",
        "intro": [
            "Dates are handled by the <code>datetime</code> module. A <code>date</code> holds "
            "year, month and day; a <code>datetime</code> also holds the time down to "
            "microseconds.",
            "Format a date by writing a pattern. <code>%Y</code> is the year, <code>%m</code> "
            "the month, <code>%d</code> the day and <code>%H:%M</code> the time in 24-hour "
            "clock.",
        ],
        "syntax": code("""
            from datetime import datetime, date

            today = date.today()
            print(today)                 # 2026-09-28
            print(today.year, today.month, today.day)

            now = datetime.now()
            print(now.strftime("%d/%m/%Y %H:%M"))
        """),
        "examples": [
            _ex("Today's date",
                "from datetime import date\ntoday = date.today()\nprint(today)\nprint(today.year)",
                "The current date, then the year"),
            _ex("Formatting a date",
                'from datetime import datetime\nd = datetime(2026, 3, 14, 15, 9)\nprint(d.strftime("%d %B %Y"))\nprint(d.strftime("%H:%M"))',
                "14 March 2026\n15:09"),
            _ex("The difference between two dates",
                "from datetime import date\nstart = date(2026, 1, 1)\nend = date(2026, 3, 1)\nprint((end - start).days)",
                "59"),
        ],
        "practice": _practice(
            "Print today's date written as year-month-day, like <code>2026-09-28</code>.",
            "strftime with the pattern \"%Y-%m-%d\".",
            "from datetime import date\nprint(date.today().strftime(\"%Y-%m-%d\"))",
        ),
        "search": ["datetime", "time", "strftime", "today", "clock"],
    },
    {
        "title": "Math",
        "group": "Tools & Libraries",
        "summary": "Everyday maths functions built into Python.",
        "intro": [
            "The <code>math</code> module has the maths you would otherwise reach for a "
            "calculator to do: square roots, powers, rounding, trigonometry and constants like pi.",
            "Also useful: <code>math.ceil()</code> always rounds up, <code>math.floor()</code> "
            "always rounds down, and <code>round()</code> goes to the nearest.",
        ],
        "syntax": code("""
            import math

            print(math.sqrt(25))     # 5.0
            print(math.ceil(4.1))     # 5    up
            print(math.floor(4.9))    # 4    down
            print(math.pi)            # 3.14159...
            print(math.pow(2, 10))    # 1024.0
            print(math.factorial(5))  # 120
        """),
        "examples": [
            _ex("Rounding the right way",
                "import math\nprint(math.ceil(3.2))\nprint(math.floor(3.8))\nprint(round(3.5))", "4\n3\n4"),
            _ex("Roots and powers",
                "import math\nprint(math.sqrt(50))\nprint(math.pow(3, 4))", "7.0710678118654755\n81.0"),
            _ex("Largest, smallest and distance",
                "import math\nprint(max(3, 9, 4))\nprint(min(3, 9, 4))\nprint(math.dist((0, 0), (3, 4)))",
                "9\n3\n5.0"),
        ],
        "practice": _practice(
            "Import <code>math</code> and print the square root of 2, rounded to 3 decimal places.",
            "round(math.sqrt(2), 3)",
            "import math\nprint(round(math.sqrt(2), 3))",
        ),
        "search": ["sqrt", "pi", "ceil", "floor", "rounding", "power"],
    },
    {
        "title": "JSON",
        "group": "Tools & Libraries",
        "summary": "Read and write data as text, in the JSON format.",
        "intro": [
            "JSON is a plain-text way of storing data. Nearly every web API speaks it. It looks "
            "a bit like a Python dictionary, but it uses double quotes and "
            "<code>true</code>/<code>false</code>/<code>null</code>.",
            "<code>json.loads()</code> turns JSON text into Python data and "
            "<code>json.dumps()</code> turns Python data into JSON text. Only dictionaries and "
            "lists can be converted - not sets or custom classes.",
        ],
        "syntax": code("""
            import json

            text = '{"name": "Vicky", "age": 20}'
            data = json.loads(text)          # JSON -> Python
            print(data["name"])              # Vicky

            back = json.dumps(data, indent=2)  # Python -> JSON
            print(back)
        """),
        "examples": [
            _ex("Turn text into a dictionary",
                'import json\ntext = \'{"name": "Sam", "age": 30}\'\ndata = json.loads(text)\nprint(data["age"])',
                "30"),
            _ex("Turn a dictionary into text",
                "import json\ndata = {\"colour\": \"red\", \"size\": \"large\"}\nprint(json.dumps(data))",
                '{"colour": "red", "size": "large"}'),
            _ex("Readable output",
                "import json\ndata = {\"a\": 1, \"b\": 2}\nprint(json.dumps(data, indent=2))",
                '{\n  "a": 1,\n  "b": 2\n}'),
        ],
        "practice": _practice(
            "Turn the text <code>'{\"city\": \"Leeds\"}'</code> into Python and print the value "
            "stored under <code>city</code>.",
            "json.loads() then dictionary indexing.",
            "import json\ndata = json.loads('{\"city\": \"Leeds\"}')\nprint(data[\"city\"])",
        ),
        "search": ["loads", "dumps", "api", "javascript object notation"],
    },
    {
        "title": "RegEx",
        "group": "Tools & Libraries",
        "summary": "Search text for patterns.",
        "intro": [
            "A regular expression, shortened to regex, is a small language for describing text "
            "patterns. The <code>re</code> module uses them to search, split and replace.",
            "The most useful patterns are <code>\\d</code> (a digit), <code>\\w</code> (a letter, "
            "digit or underscore), <code>\\s</code> (any space) and a dot <code>.</code> (any "
            "single character). Put <code>^</code> at the start and <code>$</code> at the end "
            "to match the whole string.",
        ],
        "syntax": code("""
            import re

            text = "Order 1234 is ready"

            print(re.search(r"\\d+", text).group())   # first digits: 1234
            print(re.findall(r"\\d+", text))          # every match
            print(re.sub(r"\\d", "*", text))          # replace

            print(bool(re.match(r"^\\d{5}$", "90210")))  # exactly 5 digits
        """),
        "examples": [
            _ex("Find all the numbers",
                'import re\ntext = "I have 2 cats and 13 dogs"\nprint(re.findall(r"\\d+", text))',
                "['2', '13']"),
            _ex("Replace text",
                'import re\nprint(re.sub(r"cat", "dog", "the cat sat"))', "the dog sat"),
            _ex("Check a pattern",
                'import re\nprint(re.match(r"^[A-Z]\\w+@\\w+\\.com$", "Vicky@mail.com") is not None)\nprint(re.match(r"^[A-Z]\\w+@\\w+\\.com$", "vicky@mail.com") is not None)\nprint(re.match(r"^[A-Z]\\w+@\\w+\\.com$", "nope") is not None)',
                "True\nFalse\nFalse"),
        ],
        "practice": _practice(
            "Print every word that starts with the letter <code>p</code> in the sentence "
            "<code>\"python is pretty pleasant\"</code>.",
            're.findall with the pattern r"\\bp\\w+".',
            'import re\nprint(re.findall(r"\\bp\\w+", "python is pretty pleasant"))',
        ),
        "search": ["regex", "pattern", "regular expression", "search", "findall", "sub", "match"],
    },
    {
        "title": "PIP",
        "group": "Tools & Libraries",
        "summary": "Install extra packages that other people have written.",
        "intro": [
            "PIP is the package installer that comes with Python. Thousands of ready-made "
            "packages are one command away, and you will almost certainly need them.",
            "You rarely need to learn these commands inside Python - you type them in your "
            "terminal. But it helps to know what they do.",
        ],
        "syntax": code("""
            # in your terminal (not inside Python)

            pip install requests          # install a package
            pip list                      # what is installed
            pip show requests             # details about one package
            pip install --upgrade requests
            pip uninstall requests
        """),
        "examples": [
            _ex("Install a package", "pip install requests",
                "Successfully installed requests-2.32.0", terminal=True),
            _ex("List what is installed", "pip list",
                "Package      Version\n---------- -------\nflask       3.0.3", terminal=True),
            _ex("Save and reuse your packages",
                "pip freeze > requirements.txt", "Writes a list to requirements.txt", terminal=True),
        ],
        "starter": code("""
            # These commands live in your terminal, not in Python.
            # Inside Python you can check what a package gives you:

            import flask
            print("Flask is installed:", flask.__name__)

            # Or read a package's version like this:
            from importlib.metadata import version
            print("Flask version:", version("flask"))
        """),
        "practice": _practice(
            "In your terminal, install the <code>requests</code> package and then check that it "
            "is there with <code>pip show requests</code>.",
            "These run in the terminal, not in a Python file.",
            "pip install requests\npip show requests",
        ),
        "search": ["pip", "install", "package", "requirements", "terminal", "pypi"],
    },
    {
        "title": "Try Except",
        "group": "Tools & Libraries",
        "summary": "Handle errors so your program keeps going.",
        "intro": [
            "Things go wrong: a file is missing, someone types letters into a number box, the "
            "network drops. Without a plan, any of those stops your program dead.",
            "<code>try</code> runs a risky block and <code>except</code> catches the error so "
            "you can do something sensible instead. You can name the error type, or catch "
            "everything with a bare <code>except:</code>.",
        ],
        "syntax": code("""
            try:
                number = int(input("Type a number: "))
                print("You typed", number)
            except ValueError:
                print("That was not a number, sorry!")
            else:
                print("That worked fine.")

            # several error types
            try:
                value = 10 / 0
            except ZeroDivisionError:
                print("You cannot divide by zero.")
        """),
        "examples": [
            _ex("Catch a bad number",
                "try:\n    print(int(\"hello\"))\nexcept ValueError:\n    print(\"Not a number\")",
                "Not a number"),
            _ex("Catch a missing key",
                "data = {\"name\": \"Vicky\"}\ntry:\n    print(data[\"age\"])\nexcept KeyError:\n    print(\"No age saved\")",
                "No age saved"),
            _ex("A finally block that always runs",
                "try:\n    print(\"working\")\nexcept Exception:\n    print(\"failed\")\nfinally:\n    print(\"always printed\")",
                "working\nalways printed"),
        ],
        "practice": _practice(
            "Try to turn the text <code>\"abc\"</code> into a number. If it fails, print "
            "<code>\"Failed\"</code>.",
            "Wrap int() in try, and catch ValueError.",
            "try:\n    print(int(\"abc\"))\nexcept ValueError:\n    print(\"Failed\")",
        ),
        "search": ["error", "exception", "handling", "valueerror", "try catch", "finally"],
    },
    {
        "title": "User Input",
        "group": "Tools & Libraries",
        "summary": "Ask the person using your program for information.",
        "intro": [
            "<code>input()</code> pauses and waits for someone to type something, then hands "
            "back whatever they typed.",
            "The important detail: input always comes back as <em>text</em>. If you want a "
            "number you must wrap it in <code>int()</code> or <code>float()</code>, and it is "
            "kind to use <code>try/except</code> in case they type letters.",
        ],
        "syntax": code("""
            name = input("What is your name? ")
            print("Hello, " + name)

            age = int(input("How old are you? "))
            print("Next year you will be", age + 1)

            # tidy and safe in one go
            text = input("Type a number: ").strip()
            try:
                print(float(text) * 2)
            except ValueError:
                print("That was not a number.")
        """),
        "examples": [
            _ex("Ask for text", 'name = input("Name? ")\nprint("Hi", name)',
                "Name? Vicky\nHi Vicky"),
            _ex("Ask for a number",
                'age = int(input("Age? "))\nprint("Next year:", age + 1)', "Age? 20\nNext year: 21"),
            _ex("Never crash on bad input",
                'raw = input("Number? ")\ntry:\n    print(int(raw) ** 2)\nexcept ValueError:\n    print("Not a number")',
                "Number? 5\n25"),
        ],
        "practice": _practice(
            "Ask for a city, then print a sentence that includes it.",
            'city = input("City? ") then use an f-string.',
            'city = input("City? ")\nprint(f"Welcome to {city}!")',
        ),
        "search": ["input", "ask user", "prompt", "scanf", "read line"],
    },
    {
        "title": "File Handling",
        "group": "Tools & Libraries",
        "summary": "Save data to a file and read it back later.",
        "intro": [
            "Variables disappear when a program stops. Files are how you make data last, so you "
            "can read it tomorrow.",
            "<code>open()</code> gives you a handle, and the mode decides what you can do: "
            "<code>\"r\"</code> read, <code>\"w\"</code> write (this wipes the file first), "
            "<code>\"a\"</code> append, <code>\"x\"</code> create only if it is not there. "
            "The <code>with</code> block closes the file for you automatically - always prefer it.",
        ],
        "syntax": code("""
            # writing
            with open("notes.txt", "w") as file:
                file.write("first line\\n")
                file.write("second line\\n")

            # reading
            with open("notes.txt", "r") as file:
                content = file.read()          # all of it
                print(content)

            with open("notes.txt") as file:
                for line in file:              # one line at a time
                    print(line.strip())
        """),
        "examples": [
            _ex("Write then read a file",
                'with open("hello.txt", "w") as f:\n    f.write("Hello file!")\n\nwith open("hello.txt") as f:\n    print(f.read())',
                "Hello file!"),
            _ex("Add to the end",
                'with open("log.txt", "a") as f:\n    f.write("added a line\\n")\n\nwith open("log.txt") as f:\n    print(len(f.readlines()), "lines")',
                "1 lines"),
            _ex("Handle a missing file",
                'try:\n    with open("nope.txt") as f:\n        print(f.read())\nexcept FileNotFoundError:\n    print("That file does not exist")',
                "That file does not exist"),
        ],
        "practice": _practice(
            "Write the line <code>\"Python is fun\"</code> into a file called "
            "<code>myfile.txt</code>, then read it back and print it.",
            "Use open() twice with a with block, once with \"w\" and once with \"r\".",
            'with open("myfile.txt", "w") as f:\n    f.write("Python is fun")\n\nwith open("myfile.txt") as f:\n    print(f.read())',
        ),
        "search": ["open", "read", "write", "append", "with", "file", "io"],
    },
    {
        "title": "Virtual Environment",
        "group": "Tools & Libraries",
        "summary": "Keep each project's packages separate and tidy.",
        "intro": [
            "A virtual environment is a private folder for one project. The packages you "
            "install inside it are invisible to your other projects, so you can use version 1 "
            "of a library here and version 2 there without any conflict.",
            "Each project gets one environment, and you recreate it on any new computer. It is "
            "the difference between code that works today and code that still works next month.",
        ],
        "syntax": code("""
            # in your terminal

            python -m venv myenv          # create it

            # Windows:      myenv\\Scripts\\activate
            # macOS/Linux:  source myenv/bin/activate

            pip install flask              # packages go here, not globally
            pip freeze > requirements.txt  # save the list

            deactivate                      # leave when you are done
        """),
        "examples": [
            _ex("Create and activate",
                "python -m venv myenv\nsource myenv/bin/activate",
                "A folder called myenv appears and (myenv) shows in your prompt", terminal=True),
            _ex("Use it and leave",
                "pip install flask\npython app.py\ndeactivate",
                "Work happens with the folder active", terminal=True),
        ],
        "starter": code("""
            # The commands above run in your terminal.
            # This is what an environment looks like from inside Python:

            import sys
            import os

            print("Python is running from:", sys.executable)
            print("Is it a virtual environment?", sys.prefix != sys.base_prefix)
            print("Working folder:", os.getcwd())
        """),
        "practice": _practice(
            "Create a virtual environment called <code>practice</code>, switch it on, and install "
            "<code>flask</code> inside it.",
            "Remember the activate command differs on Windows and macOS/Linux.",
            "python -m venv practice\nsource practice/bin/activate\npip install flask",
        ),
        "search": ["venv", "venv module", "isolated", "dependencies", "activate", "env"],
    },
    {
        "title": "NumPy",
        "group": "Tools & Libraries",
        "summary": "Fast maths on whole tables of numbers.",
        "intro": [
            "NumPy is the workhorse of Python data work. Its <code>ndarray</code> holds a whole "
            "grid of numbers in memory, and it does operations across all of them in one line.",
            "The big win is speed: NumPy loops in fast C code, so a calculation on a million "
            "numbers finishes in a blink. It is also the foundation that Pandas is built on.",
        ],
        "syntax": code("""
            import numpy as np

            numbers = np.array([1, 2, 3, 4])
            print(numbers * 2)        # every item doubled: [2 4 6 8]
            print(numbers.sum())     # 10

            grid = np.array([[1, 2], [3, 4]])
            print(grid.shape)        # (2, 2)  two rows of two
            print(np.array([1, 2, 3]).mean())   # 2.0
        """),
        "examples": [
            _ex("Whole-array maths",
                "import numpy as np\nn = np.array([1, 2, 3, 4, 5])\nprint(n * 10)\nprint(n.sum())\nprint(n.mean())",
                "[10 20 30 40 50]\n15\n3.0"),
            _ex("Shapes and sizes",
                "import numpy as np\ng = np.array([[1, 2, 3], [4, 5, 6]])\nprint(g.shape)\nprint(g[0])",
                "(2, 3)\n[1 2 3]"),
            _ex("Slicing like a list",
                "import numpy as np\nn = np.array([10, 20, 30, 40, 50])\nprint(n[1:3])\nprint(n[n > 25])",
                "[20 30]\n[30 40 50]"),
        ],
        "practice": _practice(
            "Make a NumPy array of the numbers 1 to 5 and print its largest value and its total.",
            "np.array([...]), then .max() and .sum().",
            "import numpy as np\nn = np.array([1, 2, 3, 4, 5])\nprint(n.max())\nprint(n.sum())",
        ),
        "search": ["numpy", "array", "ndarray", "vector", "matrix", "np"],
    },
    {
        "title": "Pandas",
        "group": "Tools & Libraries",
        "summary": "Tables of data - like a spreadsheet you can program.",
        "intro": [
            "Pandas is built on NumPy and gives you a <code>DataFrame</code>: a table with rows "
            "and named columns, a bit like an Excel sheet in code. This is the tool you reach "
            "for when cleaning or analysing real data.",
            "You can build one from a dictionary, pick a column with square brackets, add new "
            "columns, filter rows, and get a quick summary with <code>describe()</code>.",
        ],
        "syntax": code("""
            import pandas as pd

            data = {"name": ["Vicky", "Sam", "Ana"], "age": [20, 25, 31]}
            df = pd.DataFrame(data)

            print(df)              # the whole table
            print(df["age"])       # one column
            print(df["age"].mean())  # a number from it
        """),
        "examples": [
            _ex("Build and read a table",
                'import pandas as pd\ndf = pd.DataFrame({"name": ["Vicky", "Sam"], "age": [20, 25]})\nprint(df)\nprint(df["age"].mean())',
                "    name  age\n0  Vicky   20\n1    Sam   25\n22.5"),
            _ex("Filter rows",
                'import pandas as pd\ndf = pd.DataFrame({"name": ["Vicky", "Sam", "Ana"], "age": [20, 25, 31]})\nprint(df[df["age"] > 21])',
                "  name  age\n1  Sam   25\n2  Ana   31"),
            _ex("Add a column and summarise",
                'import pandas as pd\ndf = pd.DataFrame({"score": [50, 80, 70]})\ndf["passed"] = df["score"] >= 60\nprint(df["passed"].tolist())\nprint("best score:", df["score"].max())',
                "[False, True, True]\nbest score: 80"),
        ],
        "practice": _practice(
            "Build a table with a <code>name</code> column and an <code>age</code> column for "
            "three people, then print the average age.",
            "pd.DataFrame({...}) then .mean() on the age column.",
            'import pandas as pd\ndf = pd.DataFrame({"name": ["Vicky", "Sam", "Ana"], "age": [20, 25, 31]})\nprint(df["age"].mean())',
        ),
        "search": ["pandas", "dataframe", "table", "csv", "spreadsheet", "analysis", "pd"],
    },
    {
        "title": "Matplotlib",
        "group": "Tools & Libraries",
        "summary": "Draw charts that turn numbers into pictures.",
        "intro": [
            "Matplotlib is Python's main drawing library. You give it numbers and a label for "
            "each axis, and it draws a chart.",
            "The usual pattern: <code>plot()</code> the data, <code>xlabel()</code> and "
            "<code>ylabel()</code> to say what the axes mean, <code>title()</code> to name the "
            "chart, then <code>show()</code> to open the window. <code>plt</code> is the "
            "shorthand almost everyone uses.",
        ],
        "syntax": code("""
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3], [2, 4, 6])
            plt.xlabel("Week")
            plt.ylabel("Hours")
            plt.title("Study time")
            plt.show()
        """),
        "examples": [
            _ex("A line chart",
                "import matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3, 4], [10, 25, 18, 32])\nplt.title(\"Sales\")\nplt.xlabel(\"Month\")\nplt.ylabel(\"Amount\")\nplt.show()",
                "Nothing is printed.\nA window opens with a line going up and down."),
            _ex("A simple bar chart",
                "import matplotlib.pyplot as plt\n\nfruits = [\"apple\", \"banana\", \"cherry\"]\ncounts = [5, 8, 3]\nplt.bar(fruits, counts)\nplt.title(\"Fruit in the basket\")\nplt.show()",
                "Nothing is printed.\nA window opens with three bars."),
            _ex("Saving a chart to a file",
                "import matplotlib.pyplot as plt\n\nplt.plot([1, 2, 3], [3, 2, 1])\nplt.savefig(\"chart.png\")\nprint(\"Saved chart.png\")",
                "Saved chart.png"),
        ],
        "practice": _practice(
            "Draw a bar chart of three countries with a value for each, give it a title, and "
            "show it.",
            "plt.bar(names, values), then plt.title() and plt.show().",
            "import matplotlib.pyplot as plt\n\nplt.bar([\"UK\", \"FR\", \"DE\"], [10, 20, 15])\nplt.title(\"Numbers per country\")\nplt.show()",
        ),
        "search": ["matplotlib", "plt", "plot", "chart", "graph", "pyplot", "bar", "visualise"],
    },
]


# --------------------------------------------------------------- lookups
def _slug(title):
    return title.lower().replace(" ", "-")


TOPIC_LIST = []
for _index, _topic in enumerate(TOPICS, start=1):
    _item = dict(_topic)
    _item["slug"] = _slug(_topic["title"])
    _item["number"] = _index
    _item["keywords"] = [k.lower() for k in _topic.get("search", [])]
    TOPIC_LIST.append(_item)

TOPIC_BY_SLUG = {t["slug"]: t for t in TOPIC_LIST}


def grouped_topics():
    """Topics split into their sidebar sections, in order."""
    groups = []
    for name in GROUPS:
        items = [t for t in TOPIC_LIST if t["group"] == name]
        if items:
            groups.append({"name": name, "topics": items})
    return groups


def next_slug(slug):
    """The topic after this one, or None at the end."""
    slugs = [t["slug"] for t in TOPIC_LIST]
    if slug not in slugs:
        return None
    position = slugs.index(slug)
    if position + 1 < len(slugs):
        return slugs[position + 1]
    return None


def prev_slug(slug):
    """The topic before this one, or None at the start."""
    slugs = [t["slug"] for t in TOPIC_LIST]
    if slug not in slugs:
        return None
    position = slugs.index(slug)
    if position > 0:
        return slugs[position - 1]
    return None


def search_topics(query):
    """Simple case-insensitive search across titles, summaries and keywords."""
    query = (query or "").strip().lower()
    if not query:
        return []

    results = []
    for topic in TOPIC_LIST:
        haystack = " ".join(
            [topic["title"], topic["summary"], topic["group"], " ".join(topic["keywords"])]
        ).lower()
        if query in haystack:
            results.append(topic)

    # exact title starts go to the top, the rest keep sidebar order
    results.sort(key=lambda t: (0 if t["title"].lower().startswith(query) else 1, t["number"]))
    return results

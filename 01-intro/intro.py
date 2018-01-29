# COMPSCI 365/590F
# Spring 2018
# Marc Liberatore
# Assignment 01

# This assignment consists of a sequence of function declarations; the
# functions are  unimplemented, and it's your job to implement them.
#
# The functions are not a comprehensive review of every part of Python
# you'll need in the course, but they are a reasonable set of examples
# of some of the simpler Python concepts you'll need for the "real"
# assignments later. If you're fluent in Python you should be able to
# zip through this very quickly; if not, it will give you a small
# amount of practice and help you spot areas where you might need
# to review.
#
# To check your answers, I've included a small set of unit tests in
# the file `test_intro.py`. You can run that file at the command
# line directly, for example:
#
#    python test_intro.py
#
# You might have to spell this slightly differently (for example,
# `python3 test_intro.py` or `python3.6 test_intro.py`) depending upon
# how you installed Python and your OS and package manager's defaults.
# Or you can use your IDE to run the tests if it supports the
# Python standard library's `unittest` module.
#
# The unit tests in this assignment are not intended to be a comprehensive
# test suite, nor are they deliberately designed to try to "catch" you
# if you try to game them. If you don't know how to pass one of them,
# don't just hardcode the answer the unit test is looking for. Ask a classmate
# or on the Piazza forums for help. My goal is for you to learn, not suffer
# unnecessarily!
#
# If you want to check your code at the command line, you can add function calls
# to the main() method and it will execute (note that the only non-`def`,
# non-`import` lines of code in this file invoke main(), which is good
# practice in Python for various reasons). You can also work at the `python` or
# `ipython` REPL, or in Jupyter, or in a console in your IDE, etc.
#
# If you've never used a language with a REPL (an interactive read-eval-print loop)
# before, I strongly, strongly recommend you get IPython working and try it out.
# It makes learning a language, and writing code, much easier for most people.
#
# Generally, don't worry about error handling or exception catching. I won't
# usually test your code on invalid inputs in the course, and if I plan
# to, I'll make it clear what behavior I expect.
#
# And in this assignment in particular, don't worry about edge cases. It will
# be clear in future assignments when I want you to do so.


def logged_in():
    """Return the string 'I have logged into both the Edlab and Gradescope.'"""
    # Right now, this method does nothing (`pass`).
    # What should it do? Read the docstring above.
    # It should return the given string. Change it to do so (once you've
    # actually logged into both, of course!).
    pass


def add(x, y):
    """Return the sum of x and y."""
    pass


def divide(x, y, truncate=False):
    """Return the result of dividing x by y. Trunate to an integer if t
    runcate is True, otherwise return a floating point value."""
    # Note that arguments to functions can be optional if you specify a
    # default value. But the caller could override this value (see
    # the tests for examples.)
    pass


def value_equal(x, y):
    """Return True iff x and y are equal in value (but not necessarily
    the same object) -- roughly equivalent to`.equals()` in Java."""
    pass


def memory_equal(x, y):
    """Return True iff x and y point to the same object in memory --
    roughly equivalent to `==` in Java."""
    pass


def hello(x):
    """
    Return the string 'Hello x', where x is substituted into the string.
    For example:

    >>> hello('Marc')
    'Hello Marc'
    """
    pass


def nth(s, n):
    """Return the nth item of the sequence s (zero-indexed)."""
    pass


def subsequence(s, start, end):
    """Return the subsequence of the items at index start (inclusive)
    to end (exclusive) in sequence s."""
    pass


def last(s):
    """Return the last item in the sequence."""
    pass


def append_to(l, e):
    """Append e to the list l."""
    pass


def sum_of(s):
    """Return the sum of the integers in the sequence s."""
    pass


def all_even(s):
    """Return true iff every element in s is an even integer (or s is empty)."""
    pass


def lookup(d, k):
    """Return the value associated with the key k in the dictionary d."""
    pass


def insert(d, k, v):
    """Associate the key k with the value v in the dictionary d.
    Overwrite any previous value associated with k."""
    pass


def read_all(filename):
    """Returns the contents of the given file, opened in default (text) mode."""
    pass

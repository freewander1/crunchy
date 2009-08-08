#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
all_tests.py

Runs a series of tests contained in text files, using the doctest framework.
All the tests are asssumed to be located in the "src/tests" sub-directory.
'''

import doctest
import os
import random
import sys
from doctest import OutputChecker
from os.path import realpath
from optparse import OptionParser

parser = OptionParser()
parser.add_option("--det", dest="det",
                  action="store_true",
                  help="Run the tests deterministically")
parser.add_option("--nose", dest="nose",
                  action="store_true",
                  help="Turns into a thin wrapper over nosetests")
options, args = parser.parse_args()

# Sometime we want to ignore Crunchy's output as it may be in a
# unpredictable language, based on user's preferences.
#
# Define a new doctest directive to ignore the output of a given test
# and monkeypatch OutputChecker with it.
original_check_output = OutputChecker.check_output
IGNORE_OUTPUT = doctest.register_optionflag("IGNORE_OUTPUT")
class MyOutputChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if optionflags & IGNORE_OUTPUT:
            return True
        return original_check_output(self, want, got, optionflags)

doctest.OutputChecker = MyOutputChecker

test_path = realpath(os.path.dirname(__file__))
test_path = realpath(os.path.join(test_path, '../src/tests'))
test_files = [os.path.join(test_path, f)
              for f in os.listdir(test_path)
              if f.startswith("test_") and f.endswith(".rst")]
sys.path.insert(0, realpath(os.path.join(test_path, '../..')))

# Turn into nosetests if asked.
if options.nose:
    from nose.core import run
    argv = ['-w', test_path,
            '--exclude=how_to.rst',
            '--with-doctest',
            '--doctest-extension=.rst',
            '-v']
    run(argv=argv)
    raise SystemExit()

# do the test in somewhat arbitrary order in order to try and
# ensure true independence.
if not options.det:
    random.shuffle(test_files)

sep = os.path.sep

nb_files = 0
total_tests = 0
total_failures = 0
files_with_failures = 0
all_files_with_failures = []

#TODO: add a command line option to replace this
include_only = []

#TODO: add a command line option to replace this
excluded = ["test_colourize.rst"] # now obsolete

#TODO: add a command line option (clean?) that would remove all .pyc
# files before testing.
#TODO: add a command line option that would remove the current .crunchy
# directory to start unit tests from the point of view of a new user.


for t in test_files:
    irrelevant, name = os.path.split(t)

    if name in excluded:
        continue

    if include_only:
        if name not in include_only:
            continue

    failure, nb_tests = doctest.testfile(t, module_relative=False)
    total_tests += nb_tests
    total_failures += failure
    if failure > 0:
        files_with_failures += 1
        all_files_with_failures.append((failure, t))

    print "%d failures in %d tests in file: %s"%(failure, nb_tests, t)
    nb_files += 1

print "-"*50
print "%d failures in %d tests in %s files out of %s." % (total_failures,
                                total_tests, files_with_failures, nb_files)
for info in all_files_with_failures:
    print "%3d failures in %s" % (info)

# Note that the number of tests, as identified by the doctest module
# is equal to the number of commands entered at the interpreter
# prompt; so this number is normally much higher than the number
# of test.

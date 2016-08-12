"""
Defines the Command Line Interface or texty.
"""
import argparse
import datetime
import re
import sys

import json
from json import JSONDecodeError
from pkg_resources import resource_string

try:
    from .ProblemSetManager import (
        ProblemSetManager,
        get_headers,
        )
except SystemError:
    from ProblemSetManager import (
        ProblemSetManager,
        get_headers,
        )

PSM = None


def get_parser():
    """Return the parser for texty.

    References the file 'parser_arguments.json', which should be in the
    same directory as this file.
    """
    config = resource_string(__name__, 'parser_arguments.json')
    jparse = None
    try:
        jparse = json.loads(config.decode('utf-8'))
    except JSONDecodeError:
        print('Unable to parse JSON cofiguration.')
        sys.exit(2)
    if jparse is None:
        return
    parser = argparse.ArgumentParser(description=jparse['description'])
    for argument in jparse['arguments']:
        option_string = argument.pop('option_string')
        parser.add_argument(option_string, **argument)
    return parser

ARGS = get_parser().parse_args()


def get_default_filename():
    """Get the default filename for the commands."""
    filename = ''
    with open(".reviewerDefault", 'r') as fin:
        filename = fin.readline().strip()
    return filename

def set_default_filename():
    """Set the default filename (No file extension)."""
    if ARGS.set_default:
        with open(".reviewerDefault", 'w') as fin:
            fin.write(ARGS.set_default)


def get_filename():
    """ Get the filename """
    if ARGS.f:
        return ARGS.f.split('.')[0]
    else:
        return get_default_filename()


def get_problem_set_manager(filename):
    """Get the ProblemSetManager."""
    if filename is not None and ARGS.H:
        psm = ProblemSetManager(filename, 'txt')
    elif filename is not None:
        psm = ProblemSetManager(filename)
    else:
        psm = None
    return psm


def _splitproblem(string):
    reg = re.compile('[0-9]+')
    return reg.findall(string)


def add_problem_set(psm):
    """Add a ProblemSet"""
    if ARGS.a:
        for problem_set in ARGS.a:
            prob = _splitproblem(problem_set)
            if len(prob) == 3:
                prob.append(0)
            psm.add_problem(prob)


def print_problem_sets(psm):
    """Print the ProblemSets"""
    if ARGS.l:
        print(psm)

def mark_problem_correct(psm):
    """Mark the given problems correct."""
    if ARGS.c:
        for correct in ARGS.c:
            try:
                prob = _splitproblem(correct)
                psm.mark_right(int(prob[0]), int(prob[1]), int(prob[2]))
            except IndexError:
                print("Problem not in problem set!")


def mark_problem_incorrect(psm):
    """Mark the given problems incorrect."""
    if ARGS.i:
        for incorrect in ARGS.i:
            try:
                prob = _splitproblem(incorrect)
                psm.mark_wrong(int(prob[0]), int(prob[1]), int(prob[2]))
            except IndexError:
                print("Problem not in problem set!")


def sort_save_and_close(psm, filename, timestamp):
    """Sort, save, and close the ProblemSetManager."""
    if psm is not None:
        if ARGS.t:
            psm.save_problems(filename + '_' + timestamp + '.txt')
        elif ARGS.hsave:
            psm.save_problems()
        elif ARGS.H and any([ARGS.i, ARGS.c, ARGS.s, ARGS.a]):
            psm.save_to_pickle()
        elif any([ARGS.i, ARGS.c, ARGS.s, ARGS.a]):
            psm.save_to_pickle()


def print_random_problems(psm):
    """Print the random problems requested from the user."""
    if ARGS.r and psm is not None:
        custom_filter = lambda x: True
        if ARGS.o and not ARGS.e:
            custom_filter = lambda x: (x & 1) == 1
        elif ARGS.e and not ARGS.o:
            custom_filter = lambda x: (x & 1) == 0
        print(get_headers())
        for _ in range(int(ARGS.r)):
            rand_prob_set = psm.random_problem_set_weighted()
            print(rand_prob_set.str_rand_problem(custom_filter))

def print_all_problem_sets(psm):
    """Print all of the Problem Sets."""
    if ARGS.p and psm is not None:
        print(psm.get_headers())
        for problem_set in psm.problem_sets:
            print(problem_set)


def print_descriptive_statistics(psm):
    """Print descriptive statistics for the ProblemSets."""
    if ARGS.statistics and psm is not None:
        stats = psm.get_stats()
        if stats['total'] != 0:
            correct = float(stats['right']) / float(stats['total']) * 100
        else:
            correct = '0 '
        print('#--------DESCRIPTIVE STATISTICS FOR ' + psm.filename +
              '-----------#')
        print('\tTotal Reviewed:\t\t%d' % stats['total'])
        print('\tPercent Right:\t\t' + str(correct)[:4] + '%')
        print('\tTotal Correct:\t\t%d' % stats['right'])
        print('\tTotal Incorrect:\t%d' % stats['wrong'])

def _main():
    set_default_filename()
    filename = get_filename()
    psm = get_problem_set_manager(filename)
    timestamp = str(datetime.date.today())

    add_problem_set(psm)
    print_problem_sets(psm)
    mark_problem_correct(psm)
    mark_problem_incorrect(psm)
    sort_save_and_close(psm, filename, timestamp)
    print_random_problems(psm)
    print_all_problem_sets(psm)
    print_descriptive_statistics(psm)

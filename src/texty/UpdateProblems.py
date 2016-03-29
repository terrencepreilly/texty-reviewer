import argparse
import datetime
import re

try:
    from .ProblemSetManager import ProblemSetManager
except SystemError:
    from ProblemSetManager import ProblemSetManager


def set_default_filename(new_default):
    with open(".reviewerDefault", 'w') as fin:
        fin.write(new_default)


def get_default_filename():
    filename = ''
    with open(".reviewerDefault", 'r') as fin:
        filename = fin.readline().strip()
    return filename


def _main():
    parser = argparse.ArgumentParser(description='A utility for reviewing\
        textbook problems, and tracking progress in textbooks.')

    parser.add_argument('-a', nargs='*',
        help="""Add a new problem set to this group in the format
                chapter.section:problems.  For example, 2.1.39 would be
                section 1 of chapter 2, with 39 problems.""")
    parser.add_argument('-c', nargs='*',
        help="""The problem gotten correct in the format
                chapter.section:problem.  For example, 6.5:15 would be
                problem 15 from section 5 of chapter 6. When a problem is
                marked correct, automatically saves.""")
    parser.add_argument('-e', action='store_true',
        help="""When generating random problems, only generate even
                problems.""")
    parser.add_argument('-f', nargs='?',
        help="""The filename for the book being reviewed.""")
    parser.add_argument('-H', action='store_true',
        help="""Load from human readable format. (Will not load file
                history.)""")
    parser.add_argument('--hsave', action='store_true',
        help="""Save in a human readable format. (Will not save file
                history.)""")
    parser.add_argument('-i', nargs='*',
        help="""The problem gotten incorrect in the format
                chapter.section:problem.  For example, 6.5:15 would be
                problem 15 from section 5 of chapter 6.  When a problem
                is marked incorrect, automatically saves.""")
    parser.add_argument('-l', action='store_true',
        help="""Print all of the current problem sets.""")
    parser.add_argument('-o', action='store_true',
        help="""When generating random problems, only generate odd
                problems.""")
    parser.add_argument('-p', action='store_true',
        help="""Print the list of problem sets.""")
    parser.add_argument('-r', nargs='?',
        help="""Generate R random problems, weighted.""")
    parser.add_argument('-s', action='store_true',
        help="""Force save without marking any correct or incorrect.""")
    parser.add_argument('--set-default', nargs='?',
        help="""Set the default file to work on.""")
    parser.add_argument('--statistics', action='store_true',
        help="""Display review statistics on the given file.""")
    parser.add_argument('-t', action='store_true',
        help="""Adds a timestamp to the filename. (Note: the file name
                must include some extension, e.g.: .txt)""")
    args = parser.parse_args()

    if args.set_default:
        set_default_filename(args.set_default)

    # ---------------GET THE FILENAME-------------------------------- #
    filename = None
    if args.f:
        filename = args.f.split('.')[0]
    else:
        filename = get_default_filename()

    # ---------------OPEN PROBLEMSETMANAGER-------------------------- #
    if filename is not None and args.H:
        psm = ProblemSetManager(filename, 'txt')
    elif filename is not None:
        psm = ProblemSetManager(filename)
    else:
        psm = None
    timestamp = str(datetime.date.today())

    # ---------------ADD PROBLEMSET---------------------------------- #
    def splitproblem(s):
        r = re.compile('\d+')
        return r.findall(s)

    if args.a:
        for p in args.a:
            prob = splitproblem(p)
            if len(prob) == 3:
                prob.append(0)
            psm.add_problem(prob)

    # ---------------LIST-------------------------------------------- #
    if args.l:
        print(psm)

    # ---------------MARK CORRECT------------------------------------ #
    if args.c:
        for p in args.c:
            try:
                prob = splitproblem(p)
                psm.mark_right(int(prob[0]), int(prob[1]), int(prob[2]))
            except IndexError:
                print("Problem not in problem set!")

    # ---------------MARK INCORRECT---------------------------------- #
    if args.i:
        for p in args.i:
            try:
                prob = splitproblem(p)
                psm.mark_wrong(int(prob[0]), int(prob[1]), int(prob[2]))
            except IndexError:
                print("Problem not in problem set!")

    # ---------------SORT, SAVE, AND CLOSE--------------------------- #
    if psm is not None:
        if args.t:
            psm.save_problems(filename + '_' + timestamp + '.txt')
        elif args.hsave:
            psm.save_problems()
        elif args.H and any([args.i, args.c, args.s, args.a]):
            psm.save_to_pickle()
        elif any([args.i, args.c, args.s, args.a]):
            psm.save_to_pickle()

    # ---------------PRINT RANDOM PROBLEMS--------------------------- #
    class Problem_Filters(object):

        def odds(x): return (x & 1) == 1

        def evens(x): return (x & 1) == 0

        def all(x): return True


    if args.r and psm is not None:
        custom_filter = Problem_Filters.all
        if (args.o and not args.e):
            custom_filter = Problem_Filters.odds
        elif (args.e and not args.o):
            custom_filter = Problem_Filters.evens
        print(psm.get_headers())
        for i in range(int(args.r)):
            rand_prob_set = psm.random_problem_set_weighted()
            print(rand_prob_set.str_rand_problem(custom_filter))


    # ---------------PRINT ALL PROBLEM SETS-------------------------- #
    if args.p and psm is not None:
        print(psm.get_headers())
        for ps in psm.problem_sets:
            print(ps)

    # ---------------DISPLAY DESCRIPTIVE STATISTICS------------------ #
    if args.statistics and psm is not None:
        stats = psm.get_stats()
        if stats['total'] != 0:
            p = float(stats['right']) / float(stats['total']) * 100
        else:
            p = '0 '
        print('#--------DESCRIPTIVE STATISTICS FOR ' + psm.filename +
              '-----------#')
        print('\tTotal Reviewed:\t\t%d' % stats['total'])
        print('\tPercent Right:\t\t' + str(p)[:4] + '%')
        print('\tTotal Correct:\t\t%d' % stats['right'])
        print('\tTotal Incorrect:\t%d' % stats['wrong'])

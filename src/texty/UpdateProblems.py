import argparse
import datetime

from .ProblemSetManager import ProblemSetManager


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

    parser.add_argument('-f', nargs='?',
        help="""The filename for the book being reviewed.""")
    parser.add_argument('-c', nargs='*',
        help="""The problem gotten correct in the format
                chapter.section:problem.  For example, 6.5:15 would be
                problem 15 from section 5 of chapter 6.""")
    parser.add_argument('-i', nargs='*',
        help="""The problem gotten incorrect in the format
                chapter.section:problem.  For example, 6.5:15 would be
                problem 15 from section 5 of chapter 6.""")
    parser.add_argument('--set-default', nargs='?',
        help="""Set the default file to work on.""")
    parser.add_argument('-t', action='store_true',
        help="""Adds a timestamp to the filename. (Note: the file name
                must include some extension, e.g.: .txt)""")
    parser.add_argument('-r', nargs='?',
        help="""Generate R random problems, weighted.""")
    parser.add_argument('-o', action='store_true',
        help="""When generating random problems, only generate odd
                problems.""")
    parser.add_argument('-e', action='store_true',
        help="""When generating random problems, only generate even
                problems.""")
    parser.add_argument('-p', action='store_true',
        help="""Print the list of problem sets.""")
    parser.add_argument('--statistics', action='store_true',
        help="""Display review statistics on the given file.""")
    args = parser.parse_args()

    if args.set_default:
        set_default_filename(args.set_default)

    # ---------------GET THE FILENAME-------------------------------- #
    filename = None
    if args.f:
        filename = args.f
    else:
        filename = get_default_filename()

    # ---------------OPEN PROBLEMSETMANAGER-------------------------- #
    psm = ProblemSetManager(filename) if filename is not None else None
    timestamp = str(datetime.date.today())


    def splitproblem(s):
        return s.split(':')[0].split('.')

    # ---------------MARK CORRECT------------------------------------ #
    if args.c:
        for p in args.c:
            try:
                prob = splitproblem(p)
                psm.mark_right(int(prob[0]), int(prob[1]))
            except:
                print("Problem not in problem set!")

    # ---------------MARK INCORRECT---------------------------------- #
    if args.i:
        for p in args.i:
            try:
                prob = splitproblem(p)
                psm.mark_wrong(int(prob[0]), int(prob[1]))
            except:
                print("Problem not in problem set!")

    # ---------------SORT, SAVE, AND CLOSE--------------------------- #
    if psm is not None and (args.i or args.c):  # only save if marking
        psm.sort_by_quotient()
        if args.c or args.i:
            if args.t:
                psm.save_problems(filename.split('.')[0] + '_' +
                                  timestamp + '.' + filename.split('.')[1])
            else:
                psm.save_problems(filename)

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
        p = float(stats['right']) / float(stats['total']) * 100
        print('\n#--------DESCRIPTIVE STATISTICS FOR ' + psm.filename +
              '-----------#')
        print('\tTotal Reviewed:\t\t%d' % stats['total'])
        print('\tPercent Right:\t\t' + str(p)[:4] + '%')
        print('\tTotal Correct:\t\t%d' % stats['right'])
        print('\tTotal Incorrect:\t%d' % stats['wrong'])

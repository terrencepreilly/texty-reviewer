"""
Defines the ProblemSetManager.
"""

import math
import random
import pickle
import sys

from .ProblemSet import ProblemSet

def get_headers():
    """Get the key describing the problem_sets."""
    return 'ch.\tsect.\tprob.\tpage\tright\twrong'


class ProblemSetManager(object):
    """Loads ProblemSets and performs operations on them.

    Attributes:
        filename: (str) The name of the file where this problem set is
            stored. (Without the suffix.
        rand: (Random) An instance of Random.
        problem_sets: (list<ProblemSet>) This manager's ProblemSets.
    """

    def __init__(self, filename="default", filetype='txy'):
        """Return a ProblemSetManager.

        If filetype is equal to 'txt', it will treat it as plain text.
        If it is a 'txy', this will treat it as a pickled ProblemSetManager
        instance.  Otherwise, it will create an empty instance.

        Keyword Arguments
            filename: The name of the file containing ProblemSet
                definitions.
        """
        self.filename = filename
        if filetype == 'txt':
            self.problem_sets = [a for a in self.load_problems()]
        elif filetype == 'txy':
            self.problem_sets = self.load_from_pickle()
        else:
            self.problem_sets = list()
        self.rand = random.Random()

    def add_problem(self, problem_set):
        """Add the given ProblemSet to the problem_sets.

        Args:
            problem_set: Either an instance of ProblemSet, or a list
                of arguments to initialize a ProblemSet.
        """
        if problem_set is ProblemSet:
            self.problem_sets.append(problem_set)
        else:
            self.problem_sets.append(ProblemSet(*problem_set))

    def remove_problem(self, problem_set):
        problem = problem_set
        if problem is not ProblemSet:
            problem = ProblemSet(*map(int, problem))
        index = -1
        for i, ps in enumerate(self.problem_sets):
            if ps == problem:
                index = i
                break
        if index == -1:
            print(
                "Unable to find problem {}".format(
                    problem
                ),
                file=sys.stderr,
            )
        else:
            self.problem_sets.pop(index)

    def replace_problem(self,
                        old_problem_set,
                        new_prolem_set):
        old = old_problem_set
        if old is not ProblemSet:
            old = ProblemSet(*map(int, old))
        new = new_prolem_set
        if new is not ProblemSet:
            new = ProblemSet(*map(int, new))
            
        index  = -1
        for i, ps in enumerate(self.problem_sets):
            if ps == old:
                index = i
                break
        if index == -1:
            print(
                'Original problem {} not found.'.format(
                    old
                ),
                file=sys.stderr,
            )
            return
            
        self.problem_sets[index] = new

    def load_problems(self):
        """Load the ProblemSets defined in the filename.

        Yields:
            The next ProblemSet defined in the file.
        """
        with open(self.filename + '.txt', 'r') as fin:
            lines = [a.strip() for a in fin.readlines()]
            key = lines[0]
            lines = lines[1:]

            for line in lines:
                problem_set = ProblemSet()
                problem_set.init_line(line, key)
                yield problem_set.normalize()

    def save_problems(self, ofilename=None):
        """Save a string representation of the ProblemSets.

        Args:
            ofilename: The name of the output file.
        """
        if ofilename is None:
            ofilename = self.filename + '.txt'
        with open(ofilename, 'w') as fout:
            print(ofilename)
            fout.write("chapter\tsection\tproblems\tpage\tright\twrong\n")
            for problem_set in self.problem_sets:
                fout.write(str(problem_set) + '\n')

    def load_from_pickle(self):
        """Load problem_sets from a pickle dump."""
        ret = None
        with open(self.filename + '.txy', 'rb') as fin:
            ret = pickle.load(fin)
        return [x.normalize() for x in ret]

    def save_to_pickle(self):
        """Save problem_sets to a pickle dump."""
        with open(self.filename + '.txy', 'wb') as fout:
            pickle.dump(self.problem_sets, fout)

    def sort(self):
        """Sort problem_sets using the compare method ProblemSet.__cmp__"""
        self.problem_sets.sort()

    def sort_by_quotient(self):
        """Sort problem_sets according to ProblemSet.quotient."""
        self.problem_sets = [(-1*a.quotient(), a) for a in self.problem_sets]
        self.problem_sets.sort()
        self.problem_sets = [a[1] for a in self.problem_sets]

    def index(self, chapter, section):
        """Return the index of this chapter and section.

        Args:
            chapter: The chapter of the ProblemSet wanted.
            section: The section of the problemSet wanted.
        """
        return self.problem_sets.index(ProblemSet(chapter, section))

    def mark_wrong(self, chapter, section, problem):
        """Increment the wrong counter on the designated ProblemSet.

        Args:
            chapter: The chapter of the ProblemSet wanted.
            section: The section of the problemSet wanted.
        """
        self.problem_sets[self.index(chapter, section)].mark_wrong(problem)

    def mark_right(self, chapter, section, problem):
        """Increment the wrong counter on the designated ProblemSet.

        Args:
            chapter: The chapter of the ProblemSet wanted.
            section: The section of the problemSet wanted.
        """
        self.problem_sets[self.index(chapter, section)].mark_right(problem)

    def weighted_num(self, mean, sigma):
        """Return a number weighted arount mu with stdev. of sigma.

        Return a random, weighted number normally distributed
        around mu with a standard deviation of sigma.

        Args:
            mean: The average value of the variable.
            sigmam: The standard deviation of the distribution.
        """
        return int(math.log(self.rand.lognormvariate(mean, sigma)))

    def trimmed_weighted_num(self, mean, sigma, minimum, maximum):
        """Return a number weighted around mu and trimmed.

        Return a random, weighted number normally distributed
        around mu with a standard deviation of sigma, trimmed to be
        between minimum and maximum.

        Args:
            mu: The average value of the variable.
            sigma: The standard deviation of the distribution.
            minimum: The smallest value the variable can take.
            maximum: The largest value the variable can take.
        """
        xvar = self.weighted_num(mean, sigma)
        if xvar < minimum or xvar > maximum:
            return self.trimmed_weighted_num(mean, sigma, minimum, maximum)
        return xvar

    def random_problem_set_weighted(self):
        """Get a random ProblemSet.

        Return a random ProblemSet, weighted by its position in problem_sets.
        """
        minimum = 1
        maximum = len(self.problem_sets) - 1
        mean = .8 * maximum
        sigma = .3 * maximum
        pnum = self.trimmed_weighted_num(mean, sigma, minimum, maximum)
        return self.problem_sets[int(pnum)]

    def __str__(self):
        return (get_headers() +
                '\n' +
                '\n'.join([str(p) for p in self.problem_sets]))

    def get_stats(self):
        """Get descriptive statistics for these problem_sets.

        Returns:
            A dictionary of descriptive statistics for the problem_sets.
            The dictionary's keys are 'right' (the number right), 'wrong'
            (the number wrong), and 'total' (the number of answers total.)
        """
        stats = dict()
        stats['right'] = sum(map(lambda x: x.right, self.problem_sets))
        stats['wrong'] = sum(map(lambda x: x.wrong, self.problem_sets))
        stats['total'] = stats['right'] + stats['wrong']
        return stats

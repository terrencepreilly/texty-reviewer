import math
import random

from .ProblemSet import ProblemSet


class ProblemSetManager(object):
    """Loads ProblemSets and performs operations on them."""

    def __init__(self, filename="Stats_Problems.txt"):
        """Return a ProblemSetManager.

        Keyword Arguments
        filename -- The name of the file containing ProblemSet
             definitions.
        """
        self.filename = filename
        self.problem_sets = [a for a in self.load_problems()]
        self.rand = random.Random()

    def load_problems(self):
        """Load the ProblemSets defined in the filename."""
        with open(self.filename, 'r') as fin:
            lines = [a.strip() for a in fin.readlines()]
            key = lines[0]
            lines = lines[1:]

            for line in lines:
                ps = ProblemSet()
                ps.init_line(line, key)
                yield ps

    def sort(self):
        """Sorts the ProblemSets using the compare method
        ProblemSet.__cmp__
        """

        self.problem_sets.sort()

    def sort_by_quotient(self):
        """Sorts problems according to ProblemSet.quotient, which is
                right - wrong.
         """
        self.problem_sets = [(-1*a.quotient(), a) for a in self.problem_sets]
        self.problem_sets.sort()
        self.problem_sets = [a[1] for a in self.problem_sets]

    def index(self, chapter, section):
        """Return the index of this chapter and section.

        Keyword arguments:
        chapter -- The chapter of the ProblemSet wanted.
        section -- The section of the problemSet wanted.
        """
        return self.problem_sets.index(ProblemSet(chapter, section))

    def mark_wrong(self, chapter, section):
        """Increment the wrong counter on the designated ProblemSet.

        Keyword arguments:
        chapter -- The chapter of the ProblemSet wanted.
        section -- The section of the problemSet wanted.
        """
        self.problem_sets[self.index(chapter, section)].mark_wrong()

    def mark_right(self, chapter, section):
        """Increment the wrong counter on the designated ProblemSet.

        Keyword arguments:
        chapter -- The chapter of the ProblemSet wanted.
        section -- The section of the problemSet wanted.
        """
        self.problem_sets[self.index(chapter, section)].mark_right()

    def weighted_num(self, mu, sigma):
        """Return a random, weighted number normally distributed
                around mu with a standard deviation of sigma.

        Keyword arguments:
        mu -- The average value of the variable.
        sigmam -- The standard deviation of the distribution.
        """
        return int(math.log(self.rand.lognormvariate(mu, sigma)))

    def trimmed_weighted_num(self, mu, sigma, minimum, maximum):
        """Return a random, weighted number normally distributed
                around mu with a standard deviation of sigma, trimmed to be
                between minimum and maximum.

        Keyword arguments:
        mu -- The average value of the variable.
        sigma -- The standard deviation of the distribution.
        minimum -- The smallest value the variable can take.
        maximum -- The largest value the variable can take.
        """
        x = self.weighted_num(mu, sigma)
        if x < minimum or x > maximum:
            return self.trimmed_weighted_num(mu, sigma, minimum, maximum)
        return x

    def random_problem_set_weighted(self):
        """Return a random problem set, weighted by its position in
                the ProblemSet list.
                """
        minimum = 0
        maximum = len(self.problem_sets) - 1
        mu = .8 * maximum
        sigma = .3 * maximum
        pnum = self.trimmed_weighted_num(mu, sigma, minimum, maximum)
        return self.problem_sets[int(pnum)]

    def save_problems(self, ofilename="save.txt"):
        """Save a string representation of the ProblemSets.

        Keyword arguments:
        ofilename -- The name of the output file.
        """
        fout = open(ofilename, 'w')
        fout.write("chapter\tsection\tproblems\tpage\tright\twrong\n")
        for ps in self.problem_sets:
            fout.write(str(ps) + '\n')
        fout.close()

    def get_headers(self):
        """Get the header string."""
        return 'ch.\tsect.\tprob.\tpage\tright\twrong'

    def get_stats(self):
        """Return a dictionary containing descriptive statistics. """
        d = dict()
        d['right'] = sum(map(lambda x: x.right, self.problem_sets))
        d['wrong'] = sum(map(lambda x: x.wrong, self.problem_sets))
        d['total'] = d['right'] + d['wrong']
        return d

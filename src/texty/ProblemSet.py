import datetime
import random


class ProblemSet(object):
    """Represents a set of problems from a particular section and
        chapter of a book.
        """

    def __init__(self, chapter=0, section=0, problems=0,
                 page=0, right=0, wrong=0):
        """Initialize a ProblemSet, setting all parameters by
        default to 0.

        Keyword Arguments:
        chapter -- The chapter of this set of problems.
        section -- The section in the chapter.
        problems -- The number of problems present.
        page -- The page in the book where the problems are found.
        right -- The number of times problems in this set have
                    been answered correctly.
        wrong -- The number of times problems in this set have
                    been answered incorretly.
        """
        self.chapter = chapter
        self.section = section
        self.problems = problems
        self.page = page
        self.right = right
        self.wrong = wrong
        self.history = list()

    def init_line(self, line,
                  key="chapter\tsection\tproblems\tpage\tright\twrong"):
        """Initialize a ProblemSet, defining chapter, section,
                problems, page, right, and wrong in a single, tab-
                separated string.

        Keyword arguments:
        line -- The line containing the ProblemSet definition
                    (a tabseparated string defined in key.
        key -- The key for parsing the line.  Must contain the
                    words chapter, section, problems, page, right, and
                    wrong.
        """
        d = dict()
        sline = [int(a) for a in line.split('\t')]
        skey = [a.strip() for a in key.split('\t')]
        for k in range(len(skey)):
            d[skey[k]] = sline[k]
        self.chapter = d["chapter"]
        self.section = d["section"]
        self.problems = d["problems"]
        self.page = d["page"]
        self.right = d["right"]
        self.wrong = d["wrong"]
        self.history = list()

    def mark_wrong(self, problem):
        """Mark the given problem wrong."""
        self.wrong += 1
        self.history.append((
            str(datetime.datetime.now()),
            -1,
            problem
            ))

    def mark_right(self, problem):
        """Mark the given problem right."""
        self.right += 1
        self.history.append((
            str(datetime.datetime.now()),
            1,
            problem
            ))

    def get_history(self):
        """ Return a list of correct and incorrect completed problems.

        The format for each item in the list is a tuple containing the
        timestamp, whether it was correct or incorrect, and the problem
        number. """
        return self.history

    def __lt__(self, ps):
        """Compare two problem sets by chapter, then section.

        Keyword arguments:
        ps -- Another ProblemSet.
        """
        if self.chapter == ps.chapter:
            return self.section < ps.section
        return self.chapter < ps.chapter

    def __eq__(self, ps):
        """Compare two problem sets, return True if they are
           the same. (I.e. Have the same chapter and section.

        Keyword arguments:
        ps -- Another ProblemSet.
        """
        return (self.chapter == ps.chapter) and (self.section == ps.section)

    def quotient(self):
        """Returns the number right minus the number wrong for
                this problem.
                """
        return self.right - self.wrong

    def __str__(self):
        """Return a string representation of this problem set."""
        retlist = [str(a) for a in [self.chapter, self.section,
                                    self.problems, self.page,
                                    self.right, self.wrong]]
        return '\t'.join(retlist)

    def str_rand_problem(self, custom_filter):
        """Return a random problem within this problem set."""
        ret = self.__str__().split('\t')
        prob_range = range(int(ret[2]))
        i = random.choice(list(filter(custom_filter, prob_range)))
        ret[2] = str(i)
        return '\t'.join(ret)

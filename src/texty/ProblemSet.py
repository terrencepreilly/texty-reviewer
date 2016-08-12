"""
This module contains the ProblemSet class, a representation of a
set of problems.
"""
import datetime
import random


class ProblemSet(object):
    """Represents a group of problems to be reviewed.

    A group of problems, typically at the end of a section, which should
    be reviewed.  Includes their history and the number of times the user
    has gotten them wrong or right.

    Attributes:
        chapter: (int) The chapter from which this problem came.
        section: (int) The section from which this problem came.
        problems: (int) The  number of problems in this section.
        page: (int) the page number where the problems start.
        right: (int) The number of times the user has gotten this problem
            correct.
        wrong: (int) The number of times the user has gotten this problem
            wrong.
        history: (list<tuple>) The history of the answers to this problem.
    """

    def __init__(self, chapter=0, section=0, problems=0,
                 page=0, right=0, wrong=0):
        """Initialize a ProblemSet, setting all parameters by default to 0.

        Args:
            chapter: The chapter of this set of problems.
            section: The section in the chapter.
            problems: The number of problems present.
            page: The page in the book where the problems are found.
            right: The number of times problems in this set have
                been answered correctly.
            wrong: The number of times problems in this set have
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

        Args:
            line: The line containing the ProblemSet definition. Should
                be a list of tab-separated integers matching the key.
            key: A tab-separated list of items in a String.  Must contain
                the words 'chapter', 'section', 'problems', 'page',
                'right', and 'wrong'.
        """
        dkey = dict()
        sline = [int(a) for a in line.split('\t')]
        skey = [a.strip() for a in key.split('\t')]
        for k in range(len(skey)):
            dkey[skey[k]] = sline[k]
        self.chapter = dkey["chapter"]
        self.section = dkey["section"]
        self.problems = dkey["problems"]
        self.page = dkey["page"]
        self.right = dkey["right"]
        self.wrong = dkey["wrong"]
        self.history = list()

    def mark_wrong(self, problem):
        """Mark the given problem wrong."""
        if problem < 0 or problem > self.problems:
            raise IndexError
        self.wrong += 1
        self.history.append((
            str(datetime.datetime.now()),
            -1,
            problem
            ))

    def mark_right(self, problem):
        """Mark the given problem right."""
        if problem < 0 or problem > self.problems:
            raise IndexError
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
        number.
        """
        return self.history

    def __lt__(self, ps):
        """Compare two problem sets by chapter, then section.

        Args:
            ps: Another ProblemSet.
        """
        if self.chapter == ps.chapter:
            return self.section < ps.section
        return self.chapter < ps.chapter

    def __eq__(self, ps):
        """Return True if the two problem sets are the same.

        Two problem sets are the same if they have the same chapter and
        section.

        Args:
            ps: Another ProblemSet.
        """
        return (self.chapter == ps.chapter) and (self.section == ps.section)

    def quotient(self):
        """Return the number right minus the number wrong for this problem."""
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

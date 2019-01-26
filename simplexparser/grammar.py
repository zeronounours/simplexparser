#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# for python2 & python3 compatibility
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import *

# some objects to describe a grammar

class GrammarError(Exception): pass

class E(object):
    """Defines a grammar expression

    Used in the definition of grammar
    """
    __slots__ = ["symbols", "cur", "tokens"]
    def __init__(self, *args):
        self.symbols = args
        self.reset()

    def reset(self):
        """ reset the parsing context """
        self.cur = 0
        self.tokens = []

    def is_complete(self):
        """ Check whether the full expression has matched """
        return self.cur == len(self.symbols)

    def match(self, tok):
        """ Feed an extra token to match

        Feed an extra token and update the matched values

        Return
        ------
        a tuple (`match`, `remain`).
        `match` is:
            True -- if the token matched the expression
            False -- if the token did not match
        `remain` is a list of unparsed tokens, when `match` is False
        """
        sym = self.symbols[self.cur]
        # first check quantifier greedy matching
        if isinstance(sym, Q):
            if

class Q(object):
    """Defines a quantifier for grammar expressions

    Used to quantify parts of grammar expresions
    """
    __slots__ = ["expression", "min", "max", "tokens"]
    def __init__(self, exp, min_or_q, max=None):
        """Initialise a quantifier

        A quantifier as several ways to be initialized. With the
        regex equivalent, it is:
          - ?               Q(E(…), "?")
          - *               Q(E(…), "*")
          - +               Q(E(…), "+")
          - {N}             Q(E(…), N, N)
          - {,M}            Q(E(…), 0, M)
          - {N,}            Q(E(…), N)
          - {N,M}           Q(E(…), N, M)
        """
        self.expression = exp
        # parse min_or_q and max as decribed in the docstring
        if isinstance(min_or_q, str):
            if min_or_q == "?":
                self.min = 0
                self.max = 1
            elif min_or_q == "*":
                self.min = 0
                self.max = None
            elif min_or_q == "+":
                self.min = 1
                self.max = None
            else:
                raise GrammarError("Unknown quantifier '%s'" % min_or_q)
        elif isinstance(min_or_q, int):
            self.min = min_or_q
            self.max = max
        else:
            raise GrammarError("Invalid type for quantifier '%s'" % \
                               type(min_or_q))
        self.tokens = []

    def is_complete(self):
        """ Check whether the quantifier has fully matched """
        return self.min <= len(self.tokens) <= self.max

    def match(self, tok):
        """ Feed an extra token to match

        Feed an extra token and update the matched values

        Return
        ------
        a tuple (`match`, `remain`).
        `match` is:
            True -- if the token matched the expression
            False -- if the token did not match
        `remain` is a list of unparsed tokens, when `match` is False
        """
        # for quantifier match, it delegates to the expression at most
        # `max` times.
        # if the expression fully match, tokens are saved
        if len(self.tokens) == self.max:
            return False, [tok]

        m, r = self.expression.match(tok)
        if m
            # check whether the expression is complete and save tokens
            if self.expression.is_complete():
                self.tokens.append(self.expression.tokens)
                self.expression.reset()
            # continue to match
            return True
        else:
            # stop to match
            return False, r


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

class ParseError(Exception): pass

class Parser(object):
    """ Simple Recursive Descent parser

    This class implement a simple RD parser for LL(1) grammar only.
    Any other kind of grammar may cause unexpected results
    """
    def __init__(self, lexer, grammar):
        """ Create a grammar parser.

        Arguments
        ---------
        lexer -- Lexer instance to use as input
        grammar -- A list of rules
                Each entry is a rule which is a tuple
                (`symbol`, `expression`, `action`)
                `symbol` is the name of a nonterminal symbol to be
                defined.
                `expression` is one of the expression which defines
                the `symbol`. If additional expressions can define the
                same symbol, additional rules with identical `symbol`
                must be defined.
                `action` is the method to call upon expression matches.
                It can be None if no action is associated.

                For instance the grammar:
                    STMT :      (EXPR "\n")+

                    EXPR :      TERM "+" EXPR
                            |   TERM "-" EXPR
                            |   TERM

                    TERM :      NUMBER
                            |   "(" EXPR ")"

                must be represented as such:
                    [
                        ("STMT", E(Q(E("EXPR", "\n"), "+")), None),

                        ("EXPR", E("TERM", "+", "EXPR"),     None),
                        ("EXPR", E("TERM", "-", "EXPR"),     None),
                        ("EXPR", E("TERM"),                  None),

                        ("TERM", E("NUMBER"),                None),
                        ("TERM", E("(", "EXPR", ")"),        None),
                    ]

                The associated lexer should yield all terminal
                symbols:
                    "\n", "+", "-", "(", ")" and "NUMBER"

                The `action` method is called with the following
                arguments:
                    symbols -- list of matched symbols
                    parser_tree -- list of nonterminal symbols
                            currently being parsed
                The method must return the value to replace the
                nonterminal symbol with.

        Note
        ----
        Caution with the provided grammar! This parser only support
        LL(1) grammar. Other kind of grammar, including left-recursive
        grammar will end up in a infinite recursion!
        There are no watchdogs to prevent such infinite recursion. Just
        be careful with what you are parsing.
        """
        self.lexer = lexer
        self.grammar = grammar
        self.cur_token = None
        self.parser_tree = []

    def _error(self, msg):
        raise ParseError(msg)

    def _get_next_token(self):
        try:
            self.cur_token = self.lexer.token()

            if self.cur_token is None:
                self.cur_token = lexer.Token(None, None, None)
        except LexerError as e:
            self._error('Lexer error at position %d' % e.pos)

    def parse(self, text, main):
        """ Parse the given text and execute associated actions

        Parse some text with the currently configured grammar and
        execute given actions on nonterminal symbol matching

        Arguments
        ---------
        text -- the text to parse with the grammar
        main -- main nonterminal symbol to start parsing with

        Exceptions
        ----------
        ParseError -- can be raised in case of parsing errors.
        """
        self.lexer.input(text)
        self._get_next_token()
        return self._stmt()


    def _parse_nonterminal(self, name):
        """ Parse a new nonterminal symbol given its name

        Arguments
        ---------
        name -- name of the nonterminal symbol to parse
        """
        # create a new parsed symbols context
        parsed_symbols



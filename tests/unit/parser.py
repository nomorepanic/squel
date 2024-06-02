# -*- coding: utf-8 -*-
import os

from lark import Lark

from pytest import fixture

from squel.grammar import Grammar
from squel.indenter import CustomIndenter
from squel.parser import Parser
from squel.transformer import Transformer


@fixture
def parser():
    return Parser()


def test_parser_init(parser):
    assert parser.algo == 'lalr'
    assert parser.ebnf_file is None


def test_parser_init_algo():
    parser = Parser(algo='algo')
    assert parser.algo == 'algo'


def test_parser_init_ebnf_file():
    parser = Parser(ebnf_file='alternative.ebnf')
    assert parser.ebnf_file == 'alternative.ebnf'


def test_parser_indenter(patch, parser):
    patch.init(CustomIndenter)
    assert isinstance(parser.indenter(), CustomIndenter)


def test_parser_transfomer(patch, parser):
    patch.init(Transformer)
    assert isinstance(parser.transformer(), Transformer)


def test_parser_default_ebnf(patch):
    patch.object(os, 'path')
    result = Parser.default_ebnf()
    args = (os.path.dirname(), '..', 'grammar', 'postgres.ebnf')
    os.path.join.assert_called_with(*args)
    os.path.realpath.assert_called_with(os.path.join())
    assert result == os.path.realpath()


def test_parser_lark(patch, parser):
    patch.object(Grammar, 'grammar')
    patch.many(Parser, ['indenter', 'default_ebnf'])
    patch.init(Lark)
    result = parser.lark()
    Grammar.grammar.assert_called_with(Parser.default_ebnf())
    kwargs = {'parser': parser.algo, 'postlex': Parser.indenter()}
    Lark.__init__.assert_called_with(Grammar.grammar(), **kwargs)
    assert isinstance(result, Lark)


def test_parser_lark_ebnf(patch, parser):
    patch.object(Grammar, 'grammar')
    patch.object(Parser, 'indenter')
    patch.init(Lark)
    parser.ebnf_file = 'grammar.ebnf'
    parser.lark()
    Grammar.grammar.assert_called_with('grammar.ebnf')


def test_parser_parse(patch, parser):
    patch.many(Parser, ['lark', 'transformer'])
    result = parser.parse('source')
    Parser.lark().parse.assert_called_with('source\n')
    Parser.transformer().transform.assert_called_with(Parser.lark().parse())
    assert result == Parser.transformer().transform()

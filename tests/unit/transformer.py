# -*- coding: utf-8 -*-
from lark import Transformer as LarkTransformer

from pytest import mark

from squel.transformer import Transformer
from squel.tree import Tree


def test_transformer():
    assert issubclass(Transformer, LarkTransformer)


@mark.parametrize('rule', ['start', 'line', 'block', 'column', 'property'])
def test_transformer_rules(rule):
    transformer = Transformer()
    result = getattr(transformer, rule)(['matches'])
    assert isinstance(result, Tree)
    assert result.data == rule
    assert result.children == ['matches']

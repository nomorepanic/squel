# -*- coding: utf-8 -*-
import io

from squel.app import Squel
from squel.parser import Parser


def test_app_squel_parse(patch):
    patch.object(io, 'open')
    patch.init(Parser)
    patch.object(Parser, 'parse')
    result = Squel.parse('path')
    io.open.assert_called_with('path', 'r')
    Parser.parse.assert_called_with(io.open().__enter__().read())
    assert result == Parser.parse()

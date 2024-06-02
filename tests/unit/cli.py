# -*- coding: utf-8 -*-
import click
from click.testing import CliRunner

from pytest import fixture

from squel.app import Squel
from squel.cli import Cli


@fixture
def runner():
    return CliRunner()


def test_cli_parse(patch, runner):
    patch.object(click, 'echo')
    patch.object(Squel, 'parse')
    result = runner.invoke(Cli.parse, ['path'])
    Squel.parse.assert_called_with('path')
    click.echo.assert_called_with(Squel.parse())
    assert result.exit_code == 0

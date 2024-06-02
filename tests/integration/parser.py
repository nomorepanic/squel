from squel.parser import Parser
from squel.tree import Tree


def test_parse_empty_string():
    assert Parser().parse('') == Tree('start', [])

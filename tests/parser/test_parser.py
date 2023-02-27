"""Parser Tests"""

import pytest

from farialimer.parser.b3parser import B3Parser as Parser
from tests.helpers import _get_testfiles


@pytest.mark.parametrize("provider, spec, path", _get_testfiles())
def test_parse_load_without_issues(provider, spec, path):
    """Load a sample file and parse it without issues"""
    parser = Parser(provider)
    content = parser.read_file(path)

    result = parser.parse(content, spec=spec)

    assert len(result) > 0

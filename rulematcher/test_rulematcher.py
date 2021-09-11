import pytest

from .rulematcher import singlerulematcher


def test_rule_matcher_no_rule_registered():
    add = singlerulematcher()
    with pytest.raises(NotImplementedError):
        add(1, 2)

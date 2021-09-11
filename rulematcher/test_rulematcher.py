import pytest

from .rulematcher import singlerulematcher


def test_rule_matcher_no_rule_registered():
    add = singlerulematcher()
    with pytest.raises(NotImplementedError):
        add(1, 2)


def test_rule_matcher_one_matching_strategy():
    add = singlerulematcher()

    @add.register_strategy()
    def add_integers(a, b):
        if type(a) == type(b) == int:
            return a + b

    assert add(1, 2) == 3


def test_multiple_rulematchers_dont_interfere():
    # TODO
    ...

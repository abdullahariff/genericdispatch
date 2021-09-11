import inspect
import pytest
from .stringmatcher import stringmatcher


def test_calling_decorated_function_returns_default():
    @stringmatcher
    def do_thing(match):
        return f"{match} thing"

    assert do_thing("foo") == "foo thing"


def test_registering_a_matcher_but_no_match_found():
    @stringmatcher
    def do_thing(match):
        return "default match"

    @do_thing.register("matchme!")
    def _(match):
        return "I match!"

    assert do_thing("foo") == "default match"
    assert do_thing("doesnt match") == "default match"


def test_matching_a_registered_matcher():
    @stringmatcher
    def do_thing(match):
        return "default match"

    @do_thing.register("matchme!")
    def _(match):
        return f"I match {match}"

    assert do_thing("foo") == "default match"
    assert do_thing("matchme!") == "I match matchme!"


def test_always_uses_default_matcher_docstring():
    @stringmatcher
    def do_thing(match):
        """
    This is my docstring.
    """
        return "default match"

    @do_thing.register("matchme!")
    def _(match):
        "This is some other docstring"
        return "I match!"

    assert inspect.getdoc(do_thing) == "This is my docstring."


def test_registering_same_match_twice_fails():
    @stringmatcher
    def do_thing(match):
        return "default match"

    @do_thing.register("matchme!")
    def _(match):
        return "I match!"

    with pytest.raises(ValueError) as exc:

        @do_thing.register("matchme!")
        def _(match):
            return "I also match"


def test_register_multiple_matches_to_single_function():
    @stringmatcher
    def do_thing(match):
        return "default match"

    @do_thing.register("matchme!")
    @do_thing.register("match again")
    def _(match):
        return f"I match {match}!"

    assert do_thing("matchme!") == "I match matchme!!"
    assert do_thing("match again") == "I match match again!"


def test_other_arguments_passed_through():
    @stringmatcher
    def do_thing(_, something):
        return f"default match {something}"

    @do_thing.register("matchme!")
    def _(_, something, keyword="myword"):
        return f"I match {something} with {keyword}!"

    assert do_thing("nomatch", "thing") == "default match thing"
    assert do_thing("matchme!", "other thing") == "I match other thing with myword!"
    assert (
        do_thing("matchme!", "other thing", keyword="password")
        == "I match other thing with password!"
    )


def test_with_other_types_of_hashable_objects():
    @stringmatcher
    def do_thing(_):
        raise NotImplementedError(f"No match found for {_}")

    @do_thing.register(56)
    def _(_):
        return "I'm an integer"

    @do_thing.register(("fat", 123))
    def _(_):
        return "I'm a tuple"

    assert do_thing(56) == "I'm an integer"
    assert do_thing(("fat", 123)) == "I'm a tuple"

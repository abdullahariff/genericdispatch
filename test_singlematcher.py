import inspect
import pytest
from .singlematcher import singlematcher

def test_calling_decorated_function_returns_default():
  @singlematcher
  def do_thing(match):
    return "thing"
  
  assert do_thing("foo") == "thing"
  
def test_registering_a_matcher_but_no_match_found():
  @singlematcher
  def do_thing(match):
    return "default match"

  @do_thing.register("matchme!")
  def _(match):
    return "I match!"
  
  assert do_thing("foo") == "default match"
  assert do_thing("doesnt match") == "default match"


def test_matching_a_registered_matcher():
  @singlematcher
  def do_thing(match):
    return "default match"

  @do_thing.register("matchme!")
  def _(match):
    return "I match!"
  
  assert do_thing("foo") == "default match"
  assert do_thing("matchme!") == "I match!"


def test_always_uses_default_matcher_docstring():
  @singlematcher
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
  @singlematcher
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
  @singlematcher
  def do_thing(match):
    return "default match"

  @do_thing.register("matchme!")
  @do_thing.register("match again")
  def _(match):
    return "I match!"

  assert do_thing("matchme!") == "I match!"
  assert do_thing("match again") == "I match!"

def test_other_arguments_passed_through():
  ...  # TODO
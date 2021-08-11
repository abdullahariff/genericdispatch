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
  
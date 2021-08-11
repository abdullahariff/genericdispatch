from functools import wraps

def singlematcher(default_func):
  """Single-dispatch matcher function decorator.
  
  Like functools.singledispatch, but matches identity instead of type.
  Transforms a function into a generic function, which can have different
  behaviours depending upon the identity of the first argument. The decorated
  function acts as the default implementation, and additional
  implementations can be registered using the .register() attribute of the
  generic function.

  Any hashable object may be registered as a match.
  """
  registry = {}
  
  @wraps(default_func)
  def wrapper(matching_arg, *args, **kwargs):
    try:
      matched_func = registry[matching_arg]
    except KeyError:
      matched_func = default_func
    return matched_func(matching_arg, *args, **kwargs)

  def register(match):
    def decorator(func):
      if match in registry:
        raise ValueError(
          f"Cannot register {func!r} to matcher '{match}', "
          f"already registered to {registry[match]!r}"
        )
      registry[match] = func
      return func
    return decorator

  wrapper.register = register
    
  return wrapper
    
    

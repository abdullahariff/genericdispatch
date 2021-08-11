from functools import wraps

def singlematcher(default_func):
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
    
    

from functools import wraps

def singlematcher(default_func):
  registry = {}
  
  @wraps(default_func)
  def wrapper(arg):
    try:
      matched_func = registry[arg]
    except KeyError:
      return default_func(arg)

  def register(match):
    def decorator(func):
      registry[match] = func
      return func
    return decorator

  wrapper.register = register
    
  return wrapper
    
    

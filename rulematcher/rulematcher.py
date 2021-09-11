from functools import wraps


def singlerulematcher():
    register = {"strategy": None}

    def func(*args, **kwargs):
        if register["strategy"]:
            return register["strategy"](*args, **kwargs)
        raise NotImplementedError

    def register_strategy():
        def decorator(strategy_func):
            register["strategy"] = strategy_func

        return decorator

    func.register_strategy = register_strategy

    return func

from functools import wraps


def singlerulematcher():
    registry = {"strategy": None, "rule": None}

    def func(*args, **kwargs):
        if registry["strategy"]:
            return registry["strategy"](*args, **kwargs)
        raise NotImplementedError

    def register_strategy(rule):
        registry["rule"] = rule

        def decorator(strategy_func):
            registry["strategy"] = strategy_func

        return decorator

    func.register_strategy = register_strategy

    return func

from functools import wraps


class NoMatchingRuleFound(Exception):
    ...


def singlerulematcher():
    registry = {"strategy": None, "rule": None}

    def func(a, b):
        rule = registry["rule"]
        strategy = registry["strategy"]
        if registry and rule and rule(a, b):
            return registry["strategy"](a, b)
        raise NoMatchingRuleFound

    def register_strategy(rule):
        registry["rule"] = rule

        def decorator(strategy_func):
            registry["strategy"] = strategy_func

        return decorator

    func.register_strategy = register_strategy

    return func

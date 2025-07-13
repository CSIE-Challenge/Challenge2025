import os


def is_auto_invoked() -> bool:
    return os.environ.get("IS_CHALLENGE_GAME_PROCESS") == "TRUE"


def enforce_type(name, obj, *args):
    if not isinstance(obj, args):
        types = " | ".join(list(map(lambda x: x.__name__, args)))
        raise TypeError(f"[API Server] Error: {name} must be type {types}")


def enforce_condition(condition_str, var, condition_fn):
    if not condition_fn(var):
        raise ValueError(f"[API Server] Error: condition violated: {condition_str}")

"""Some utilities."""


def is_first_visit(request):
    """Assumes that requests without any cookies are first-time requests (to be used for inlining critical css later)."""
    return len(request.COOKIES) == 0


def conditional_decorator(dec, condition: bool):
    """Conditionally applies decorator.

    Args:
        dec: the original decorator
        condition (bool): the condition

    """

    def decorator(func):
        if not condition:
            # Return the function unchanged, not decorated.
            return func
        return dec(func)

    return decorator

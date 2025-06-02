def division(a, b):
    if not (isinstance(a, int) and isinstance(b, int)):
        raise TypeError('Both a and b must be integers.')
    return a / b
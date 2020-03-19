import doctest
import itertools


def cabbage():
    """
    >>> g = cabbage()
    >>> next(g)
    100
    >>> next(g)
    200
    >>> next(g)
    100
    """
    for i in itertools.count():
        if i % 2 == 0:
            yield 100
        else:
            yield 200


if __name__ == '__main__':
    doctest.testmod()

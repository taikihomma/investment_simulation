import itertools
import random


def simple_cabbage():
    """ 毎月100円と200円を繰り返すキャベツ
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


def random_cabbage():
    """ 毎月100円から200円の間をランダムで価格変動するキャベツ
    """
    # シードの設定
    random.seed(0)
    for i in itertools.count():
        yield random.randint(100, 200)


if __name__ == '__main__':
    pass

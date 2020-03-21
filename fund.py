import itertools
import pandas as pd
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


def gen_fund_data(df, offset):
    df.sort_index(ascending=False, inplace=True)
    df = df.iloc[offset:, :]
    for row in df.itertuples():
        yield float(row[2].replace(",", ""))


def sp500(offset):
    """ S&P500指数の8年分データ(2012/3-2020/3) """
    yield from gen_fund_data(pd.read_csv("datas/S&P500_2012-2020.csv"), offset)


def topix(offset):
    """ TOPIX指数の8年分データ(2012/3-2020/3) """
    yield from gen_fund_data(pd.read_csv("datas/TOPIX_2012-2020.csv"), offset)

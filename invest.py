import fund
import matplotlib.pyplot as plt


class Invest(object):
    """投資戦略の基本クラス"""
    def __init__(self):
        self.payment = 0.0
        self.income = 0.0
        self.buy_unit = 0.0
        self.sell_unit = 0.0
        self.cost_per_unit = []
        self.total = []
        self.name = "Invest Method"

    def update_data(self, payment, income, buy_unit, sell_unit, now_price):
        """毎月の売買の結果を更新"""
        self.payment += payment
        self.income += income
        self.buy_unit += buy_unit
        self.sell_unit += sell_unit
        self.total.append((self.buy_unit - self.sell_unit) * now_price + self.income - self.payment)
        try:
            self.cost_per_unit.append(self.payment / self.buy_unit)
        except ZeroDivisionError:
            self.cost_per_unit.append(0.0)

    def __repr__(self):
        try:
            return f'[{self.name}]\tpay:{self.payment}\tin:{self.income}\tbuy:{self.buy_unit}\tsell:{self.sell_unit}\t' \
                   f'ave:{self.cost_per_unit[-1]}\tttl:{self.total[-1]}'
        except IndexError:
            return "all 0"

    def plot_data(self, axL, axR):
        axL.plot(self.cost_per_unit, label=self.name)
        axR.plot(self.total, label=self.name)


class BuyFixedUnit(Invest):
    """買い付け口数一定の戦略"""
    def __init__(self, unit):
        super().__init__()
        self.unit = unit
        self.name = "FixedUnit"

    def buy(self, now_price):
        # 一定口数を買い付ける
        buy_unit = self.unit
        payment = now_price * buy_unit
        sell_unit = 0.0
        income = 0.0
        self.update_data(payment, income, buy_unit, sell_unit, now_price)


class BuyFixedPrice(Invest):
    """ドルコスト平均法の戦略"""
    def __init__(self, price):
        super().__init__()
        self.price = price
        self.name = "FixedPrice"

    def buy(self, now_price):
        # ドルコスト平均法で買い付け(一定額を購入する)
        try:
            buy_unit = self.price / now_price
        except ZeroDivisionError:
            buy_unit = 0.0
        payment = now_price * buy_unit
        sell_unit = 0.0
        income = 0.0
        self.update_data(payment, income, buy_unit, sell_unit, now_price)


class BuyFixedValue(Invest):
    """バリュー平均法の戦略"""
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.name = "FixedValue"
        self.month = 0

    def buy(self, now_price):
        # 一定価値となるように買いまたは売りを行う
        self.month += 1
        now_assets = now_price * (self.buy_unit - self.sell_unit)
        target_assets = self.month * self.value
        diff_assets = target_assets - now_assets
        payment, buy_unit, sell_unit, income = 0.0, 0.0, 0.0, 0.0

        # 目標価値に未達⇒買い
        if diff_assets > 0:
            payment = diff_assets
            buy_unit = payment / now_price
        # 目標価格に到達⇒売り
        elif diff_assets < 0:
            income = -diff_assets
            sell_unit = income / now_price
        self.update_data(payment, income, buy_unit, sell_unit, now_price)


if __name__ == '__main__':
    a = BuyFixedUnit(5.0)
    b = BuyFixedPrice(750.0)
    c = BuyFixedValue(750.0)
    price_list = []
    for i, p in enumerate(fund.cabbage()):
        a.buy(p)
        b.buy(p)
        c.buy(p)
        price_list.append(p)
        if i >= 59:
            break
    fig, (axL, axR) = plt.subplots(ncols=2)
    axL.plot(price_list, label="price")
    a.plot_data(axL, axR)
    b.plot_data(axL, axR)
    c.plot_data(axL, axR)
    axL.legend()
    axR.legend()
    axL.set_title("cost_per_unit")
    axR.set_title("total_assets")
    axL.set_xlabel("months")
    axR.set_xlabel("months")
    plt.show()

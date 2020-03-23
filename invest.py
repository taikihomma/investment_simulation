import matplotlib.pyplot as plt


class Invest(object):
    """投資戦略の基本クラス"""
    def __init__(self):
        self.payment = 0.0
        self.income = 0.0
        self.buy_unit = 0.0
        self.sell_unit = 0.0
        self.cost_per_unit = []
        self.income_per_unit = []
        self.total = []
        self.name = "Invest Method"

    def init_sell(self):
        pass

    def buy_spot(self, now_price, unit):
        """ スポット購入 """
        self.buy_unit = unit
        self.payment = now_price * unit

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
        try:
            self.income_per_unit.append(self.income / self.sell_unit)
        except ZeroDivisionError:
            self.income_per_unit.append(0.0)

    def continue_buy(self, payment, max_cash):
        return (payment + self.payment - self.income) <= max_cash

    def continue_sell(self, unit):
        return (unit + self.sell_unit - self.buy_unit) <= 0

    def __repr__(self):
        try:
            return f'[{self.name}]\tpay:{self.payment}\tin:{self.income}\tbuy:{self.buy_unit}\tsell:{self.sell_unit}\t' \
                   f'ave:{self.cost_per_unit[-1]}\tttl:{self.total[-1]}'
        except IndexError:
            return "all 0"

    def show_buy_result(self, axL, axR):
        axL.plot(self.cost_per_unit, label=self.name)
        axR.plot(self.total, label=self.name)

    def show_sell_result(self, axL, axR):
        axL.plot(self.income_per_unit, label=self.name)
        axR.plot(self.total, label=self.name)


class BuyFixedAmount(Invest):
    """買い付け口数一定の戦略"""
    def __init__(self, amount):
        super().__init__()
        self.amount = amount
        self.name = "FixedAmount"

    def buy(self, now_price, max_cash):
        # 一定口数を買い付ける
        buy_unit = self.amount
        payment = now_price * buy_unit
        if not self.continue_buy(payment, max_cash):
            buy_unit, payment = 0.0, 0.0
        sell_unit = 0.0
        income = 0.0
        self.update_data(payment, income, buy_unit, sell_unit, now_price)

    def sell(self, now_price):
        # 一定口数を売り付ける
        sell_unit = self.amount
        income = now_price * sell_unit
        if not self.continue_sell(sell_unit):
            sell_unit, income = 0.0, 0.0
        payment = 0.0
        buy_unit = 0.0
        self.update_data(payment, income, buy_unit, sell_unit, now_price)


class BuyFixedPrice(Invest):
    """ドルコスト平均法の戦略"""
    def __init__(self, price):
        super().__init__()
        self.price = price
        self.name = "FixedPrice"

    def buy(self, now_price, max_cash):
        # ドルコスト平均法で買い付け(一定額を購入する)
        try:
            buy_unit = self.price / now_price
        except ZeroDivisionError:
            buy_unit = 0.0
        payment = now_price * buy_unit
        if not self.continue_buy(payment, max_cash):
            buy_unit, payment = 0.0, 0.0
        sell_unit = 0.0
        income = 0.0
        self.update_data(payment, income, buy_unit, sell_unit, now_price)

    def sell(self, now_price):
        # ドルコスト平均法で売り付ける
        try:
            sell_unit = self.price / now_price
        except ZeroDivisionError:
            sell_unit = 0.0
        income = now_price * sell_unit
        if not self.continue_sell(sell_unit):
            sell_unit, income = 0.0, 0.0
        payment = 0.0
        buy_unit = 0.0
        self.update_data(payment, income, buy_unit, sell_unit, now_price)


class BuyFixedValue(Invest):
    """バリュー平均法の戦略"""
    def __init__(self, value):
        super().__init__()
        self.value = value
        self.name = "FixedValue"
        self.month = 0
        self.init_value = 0

    def init_sell(self):
        self.init_value = self.payment

    def buy(self, now_price, max_cash):
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
            if not self.continue_buy(payment, max_cash):
                payment, buy_unit = 0.0, 0.0
        # 目標価格に到達⇒売り
        elif diff_assets < 0:
            income = -diff_assets
            sell_unit = income / now_price
        self.update_data(payment, income, buy_unit, sell_unit, now_price)

    def sell(self, now_price):
        # 一定価値となるように買いまたは売りを行う
        self.month += 1
        now_assets = now_price * (self.buy_unit - self.sell_unit)
        target_assets = self.init_value - (self.month * self.value)
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
            if not self.continue_sell(sell_unit):
                sell_unit, income = 0.0, 0.0
        self.update_data(payment, income, buy_unit, sell_unit, now_price)


class BuyWeightedPrice(BuyFixedPrice):
    """ドルコスト平均法+重みづけ戦略"""
    def __init__(self, price, weight):
        super().__init__(price)
        self.weight = weight
        self.name = "WeightedPrice"

    def buy(self, now_price, max_cash):
        # 重みづけドルコスト平均法で買い付け(平均購入単価と現在価格の差から重みづけした金額を購入する)
        try:
            additional_rate = now_price / self.cost_per_unit[-1]
            additional_rate = (1 - additional_rate)
            additional_rate *= self.weight
        except (IndexError, ZeroDivisionError):
            additional_rate = 0
        finally:
            additional_rate += 1
            if additional_rate < 0:
                additional_rate = 0

        try:
            buy_unit = self.price / now_price * additional_rate
        except ZeroDivisionError:
            buy_unit = 0.0
        payment = now_price * buy_unit
        if not self.continue_buy(payment, max_cash):
            buy_unit, payment = 0.0, 0.0
        sell_unit = 0.0
        income = 0.0
        self.update_data(payment, income, buy_unit, sell_unit, now_price)


def buy_simulation(amount, price, value, fund_generator, month, max_cash):
    """ 投資シミュレーション 指定された条件で投資を実行して結果を確認する """
    strategies = [BuyFixedAmount(amount), BuyFixedPrice(price), BuyFixedValue(value), BuyWeightedPrice(price, 1)]
    price_list = []
    for i, price in enumerate(fund_generator, start=1):
        for strategy in strategies:
            strategy.buy(price, max_cash)
        price_list.append(price)
        if i >= month:
            break
    print(*strategies, sep="\n")
    fig, (axL, axR) = plt.subplots(ncols=2)
    for strategy in strategies:
        strategy.show_buy_result(axL, axR)
    axL.plot(price_list, label="price")
    axL.legend()
    axR.legend()
    axL.set_title("cost_per_unit")
    axR.set_title("total_assets")
    axL.set_xlabel("months")
    axR.set_xlabel("months")


def sell_simulation(amount, price, value, fund_generator, month, unit):
    """ 投資シミュレーション 指定された条件で投資を実行して結果を確認する """
    strategies = [BuyFixedAmount(amount), BuyFixedPrice(price), BuyFixedValue(value)]
    price_list = []
    for i, price in enumerate(fund_generator, start=1):
        for strategy in strategies:
            if i == 1:
                # 最初に一括買い付けを実施
                strategy.buy_spot(price, unit)
                strategy.init_sell()
            strategy.sell(price)
        price_list.append(price)
        if i >= month:
            break
    print(*strategies, sep="\n")
    fig, (axL, axR) = plt.subplots(ncols=2)
    for strategy in strategies:
        strategy.show_sell_result(axL, axR)
    axL.plot(price_list, label="price")
    axL.legend()
    axR.legend()
    axL.set_title("cost_per_unit")
    axR.set_title("total_assets")
    axL.set_xlabel("months")
    axR.set_xlabel("months")

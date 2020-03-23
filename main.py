import fund
import invest
import matplotlib.pyplot as plt


def buy_simulation_main():
    print("case 1")
    invest.buy_simulation(5, 750, 750, fund.simple_cabbage(), 60, 40000)
    print("case 2")
    invest.buy_simulation(5, 750, 750, fund.random_cabbage(), 60, 40000)
    print("case 3")
    invest.buy_simulation(1, 1876, 1876, fund.sp500(0), 60, 90000)
    print("case 4")
    invest.buy_simulation(1, 2500, 2500, fund.sp500(36), 60, 120000)
    print("case 5")
    invest.buy_simulation(1, 1250, 1250, fund.topix(0), 60, 70000)
    print("case 6")
    invest.buy_simulation(1, 1574, 1574, fund.topix(36), 60, 90000)
    plt.show()


def sell_simulation_main():
    print("case 1")
    invest.sell_simulation(5, 750, 750, fund.simple_cabbage(), 60, 200)
    print("case 2")
    invest.sell_simulation(5, 750, 750, fund.random_cabbage(), 60, 200)
    print("case 3")
    invest.sell_simulation(1, 1876, 1876, fund.sp500(0), 60, 50)
    print("case 4")
    invest.sell_simulation(1, 2500, 2500, fund.sp500(36), 60, 50)
    print("case 5")
    invest.sell_simulation(1, 1250, 1250, fund.topix(0), 60, 57)
    print("case 6")
    invest.sell_simulation(1, 1574, 1574, fund.topix(36), 60, 57)
    plt.show()


def main():
    # buy_simulation_main()
    sell_simulation_main()


if __name__ == '__main__':
    main()

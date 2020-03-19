import fund
import invest
import matplotlib.pyplot as plt


def main():
    invest.invest_simulation(5, 750, 750, fund.simple_cabbage(), 60)
    invest.invest_simulation(5, 750, 750, fund.random_cabbage(), 60)
    plt.show()


if __name__ == '__main__':
    main()

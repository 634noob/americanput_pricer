from math import *
from utils import *
import numpy as np


class AmericanPutOption:
    def __init__(self, T, rf, spot, strike, vol):
        self.T = T
        self.rf = rf
        self.spot = spot
        self.strike = strike
        self.vol = vol
        # print(self)

    def __str__(self):
        str_repr = "This is an american put option with the following attributes: \n"
        str_repr += "*" * 61 + "\n"
        str_repr += "Time to maturity: ".ljust(55) + (str(self.T) + "Y").rjust(5) + "\n"
        str_repr += "Risk free interest rate(in percentages per annum): ".ljust(55) + str(self.rf).rjust(5) + "\n"
        str_repr += "Sport price: ".ljust(55) + str(self.spot).rjust(5) + "\n"
        str_repr += "Strike: ".ljust(55) + str(self.strike).rjust(5) + "\n"
        str_repr += "Volatility: ".ljust(55) + str(self.vol).rjust(5) + "\n"
        str_repr += "*" * 61 + "\n"
        return str_repr

    def american_put_generic(self, n_step, bs):
        dt = self.T / n_step
        u, d, p = get_udp(self.vol, dt, self.rf)
        ratio_ud = u / d
        df = exp(-self.rf * dt)
        q = 1 - p
        last_lowest = self.spot * (d ** n_step)
        price_a = np.array([last_lowest * (ratio_ud ** i) for i in range(n_step + 1)])
        strike = self.strike * np.ones(n_step + 1)
        payoff_a = put_payoff(price_a, strike)
        v = payoff_a
        while len(v) > 1:
            # last_lowest = last_lowest / d
            price_a = price_a[:-1] / d
            strike = strike[:-1]
            payoff_a = put_payoff(price_a, strike)
            if len(v) == n_step + 1:
                if bs:
                    european_price_a = np.array([df * black(xi / df, self.strike, self.vol, dt, 0) for xi in price_a])
                    v = np.maximum(european_price_a, payoff_a)
                else:
                    v = np.maximum(([p] * v[1:] + [q] * v[0:-1]) * df, payoff_a)
            else:
                v = np.maximum(([p] * v[1:] + [q] * v[0:-1]) * df, payoff_a)
        return v[0]

    def american_put_binomial(self, n_step):
        return self.american_put_generic(n_step, 0)

    def american_put_bbs(self, n_step):
        return self.american_put_generic(n_step, 1)

    def american_put_bbsr(self, n_step):
        return 2 * self.american_put_bbs(2 * n_step) - self.american_put_bbs(n_step)


if __name__ == "__main__":
    T = 0.5
    S0 = 100
    rf = 0.05
    N = 20
    vol = 0.3
    K = 90
    american_call = AmericanPutOption(T, rf, S0, K, vol)
    print("The price under normal binomial tree is: ".ljust(70), american_call.american_put_binomial(N))
    print("The price under binomial BS tree is: ".ljust(70), american_call.american_put_bbs(N))
    print("The price under binomial BS tree with Richardson extrapolation is: ".ljust(70),
          american_call.american_put_bbsr(N))

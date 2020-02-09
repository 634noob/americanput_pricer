from src.utils import *
import numpy as np


class AmericanPutOption:
    def __init__(self, T, rf, spot, strike, vol):
        try:
            assert T > 0
            self.T = float(T)
            assert rf > 0
            self.rf = float(rf)
            self.spot = float(spot)
            self.strike = float(strike)
            assert vol > 0
            self.vol = float(vol)
        except ValueError:
            print('Error passing Options parameters')

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

    def american_put_lsmc(self, n_step, n_sim):
        dt = self.T / n_step
        df = exp(-self.rf * dt)

        def mcprice_matrix(seed=123):
            """ Returns MC price matrix rows: time columns: price-path simulation """

            np.random.seed(seed)
            m_mcprice_matrix = np.zeros((n_step + 1, n_sim), dtype=np.float64)
            m_mcprice_matrix[0, :] = self.spot
            for t in range(1, n_step + 1):
                brownian = np.random.standard_normal(n_sim // 2)
                brownian = np.concatenate((brownian, -brownian))
                m_mcprice_matrix[t, :] = (m_mcprice_matrix[t - 1, :] * np.exp((self.rf - self.vol ** 2 / 2.) * dt

                                                                              + self.vol * brownian * np.sqrt(dt)))
            return m_mcprice_matrix

        m_mcprice_matrix = mcprice_matrix()

        def MCpayoff():
            """Returns the inner-value of American Option"""
            payoff = np.maximum(self.strike - m_mcprice_matrix, np.zeros((n_step + 1, n_sim), dtype=np.float64))
            return payoff

        m_mcpayoff = MCpayoff()

        def value_vector():
            value_matrix = np.zeros_like(m_mcpayoff)
            value_matrix[-1, :] = m_mcpayoff[-1, :]
            for t in range(n_step - 1, 0, -1):
                mask = m_mcprice_matrix[t, :] < self.strike
                regression = np.polyfit(m_mcprice_matrix[t, mask], value_matrix[t + 1, mask] * df, 2)
                continuation_value = np.polyval(regression, m_mcprice_matrix[t, mask])
                value_matrix[t, mask] = np.where(m_mcpayoff[t, mask] > continuation_value, m_mcpayoff[t, mask],
                                                 value_matrix[t + 1, mask] * df)
                mask = ~mask
                value_matrix[t, mask] = value_matrix[t + 1, mask] * df

            return value_matrix[1, :] * df

        def price():
            return np.sum(value_vector()) / float(n_sim)

        return price()


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
    print("The price under lsmc is: ".ljust(70), american_call.american_put_lsmc(N, 100000))

from math import sqrt
from math import exp
import numpy as np
from scipy.stats import norm


def black(f, k, sigma, t, call):
    stddev = sigma * sqrt(t)
    d1 = np.log(f / k) / stddev + 0.5 * stddev
    d2 = d1 - stddev
    p = f * norm.cdf(d1) - k * norm.cdf(d2)
    if call != 1:
        p = p - (f - k)
    return p


def put_payoff(price, strike):
    return np.maximum(strike - price, 0)


def get_udp(vol, dt, rf):
    u = exp(vol * sqrt(dt))
    d = exp(-vol * sqrt(dt))
    p = (exp(rf * dt) - d) / (u - d)
    return u, d, p

from src.american_put import *
import numpy as np
import matplotlib.pyplot as plt

# Parameters
T = 0.5
S0 = 100
rf = 0.05
vol = 0.3
K = 90
american_call = AmericanPutOption(T, rf, S0, K, vol)  # Initialize the american put
print(american_call)  # Print the american attributes
n_steps = np.array([n + 2 for n in range(100)])
price_a = np.array([american_call.american_put_binomial(N) for N in n_steps])
price_b = np.array([american_call.american_put_bbs(N) for N in n_steps])
price_c = np.array([american_call.american_put_bbsr(N) for N in n_steps])

# n_sims = np.array([n*100 for n in range(1001) if n > 0])
# print(n_sims)
# plt.subplot(3, 1, 1)
plt.ylabel('American Put Price')
plt.xlabel('N steps')
plt.plot(n_steps, price_a, "b-", linewidth=0.5, label="Binomial")
# plt.subplot(3, 1, 2)
plt.plot(n_steps, price_b, "g-", linewidth=0.5, label="BBS")
# plt.subplot(3, 1, 3)
plt.plot(n_steps, price_c, "r-", linewidth=0.5, label="BBSR")
plt.hlines(y=3.345, linestyles='--', xmin=0, xmax=100)
plt.legend(loc='upper right')

plt.show()

# americanput_pricer
amrican put option pricer. Using Binomial tree, BBS and BBSR methods
## BBS: binomial black-scholes
The bbs method will calculate the price at N-1 using the BS formula for European put option, which is to replace the discounted expectation of price at N.
## BBSR
BBBSR use Richardson extrapolation on top of BBS. The expression is simply: 2*V(0.5h)-V(h)

## LSMC
least square montecarlo is a monte carlo method for american put pricing, see at [LSMC]https://en.wikipedia.org/wiki/Monte_Carlo_methods_for_option_pricing
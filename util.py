import numpy as np

import truevalues


def euler(x, v, poly, dt):
    y, dydx, d2ydx2, alpha, r = truevalues.trvalues(poly, x)
    acc = v_prime(v, alpha)
    vn = v + dt * acc
    xn = x + dt * v * np.cos(alpha)
    return xn, vn, acc, alpha, r


def v_prime(v, alpha, c=0.0041, m=0.0302, g=9.8214675):
    return (5/7) * (g * np.sin(alpha) - (c * v) / m)


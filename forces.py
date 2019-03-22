import numpy as np
import matplotlib.pyplot as plt
from fys import euler


def force_normal(x_start, poly: np.array, v_start=0, n=20000):
    def force(alpha, v, r, m=0.0302, g=9.8214675):
        return m * g * np.cos(alpha) + m * (v ** 2 / r)

    xn = x_start
    vn = v_start
    dt = 20 / n
    fns = []
    xs = []
    for i in range(n):
        xn, vn, acc, alpha, r, y = euler(xn, vn, poly, dt=dt)
        fns.append(force(alpha, vn, r))
        xs.append(xn)

    return fns, xs


def force_friction(x_start, poly: np.array, v_start=0, n=20000):
    def force(acc, m=0.0302):
        return (2 / 5) * m * acc

    xn = x_start
    vn = v_start
    dt = 20 / n
    ffs = []
    xs = []
    for i in range(n):
        xn, vn, acc, alpha, r, y = euler(xn, vn, poly, dt=dt)
        ffs.append(force(acc))
        xs.append(xn)

    return ffs, xs

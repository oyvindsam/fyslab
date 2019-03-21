import matplotlib as matplotlib
import numpy as np
import matplotlib.pyplot as plt

import truevalues


def v_prime(v, alpha, c=0.0041, m=0.0302, g=9.8214675):
    return (5/7) * (g * np.sin(alpha) - (c * v) / m)


def euler(x, v, poly, dt):
    alpha = truevalues.trvalues(poly, x)[3]
    acc = v_prime(v, alpha)
    vn = v + dt * acc
    xn = x + dt * v * np.cos(alpha)
    return xn, vn, acc, alpha


def force(acc, m=0.0302):
    return (2/5) * m * acc


def force_friction(x_start, poly: np.array, v_start=0, n=20000):
    xn = x_start
    vn = v_start
    dt = 20 / n
    ffs = []
    xs = []
    for i in range(n):
        xn, vn, acc, alpha = euler(xn, vn, poly, dt=dt)
        ffs.append(force(acc))
        xs.append(xn)

    print(ffs)
    # t = np.linspace(0, 20, n)
    # plt.figure()
    # plt.title("optimized curve trail ")
    # plt.plot(t, ffs, label="ffs")
    # plt.plot(t, xs)
    # plt.legend()
    #
    # plt.grid()
    # plt.show()

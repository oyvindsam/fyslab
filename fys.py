import numpy as np
from scipy.optimize import curve_fit

import truevalues


def euler(x, v, poly, dt):
    y, dydx, d2ydx2, alpha, r = truevalues.trvalues(poly, x)
    acc = v_prime(v, alpha)
    vn = v + dt * acc
    xn = x + dt * v * np.cos(alpha)
    return xn, vn, acc, alpha, r, y


def v_prime(v, alpha, c=0.0041, m=0.0302, g=9.8214675):
    return (5/7) * (g * np.sin(alpha) - (c * v) / m)


def potential(max_cor: np.array, pot_delta):
    def mgh(h):
        return 0.0302 * 9.8214675 * h

    ts, ys = max_cor[:, [0]].flatten(), max_cor[:, [2]].flatten()
    potentials = []
    for i in range(0, len(max_cor)):
        if pot_delta:
            potentials.append((ts[i+1], mgh(ys[i]) - mgh(ys[i])))
        else:
            potentials.append((ts[i], mgh(ys[i])))

    return np.array(potentials)



def half_life(pot_energy:np.array):
    xdata, ydata = pot_energy[:,[0]].flatten(), pot_energy[:,[1]].flatten()  # time, potential energy
    p_init = ydata[0]

    def half_func(time: np.array, t_half):
        f = p_init * (1 / 2) ** (time / t_half)
        return f

    fit, covar = curve_fit(half_func, xdata, ydata)

    return fit, covar


#def gauss_pot(heights, )
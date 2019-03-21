import os
import numpy as np
from scipy.optimize import curve_fit

import iptrack as ip
import truevalues as tv


data_folder = "data/"
out_folder = "out/"


def save_data(filename, string):
    f = open(out_folder + filename, "w+")
    f.write(string)
    f.close()

# Returns dict{'filename': (tracker_data: np.array, iptrack: np.array)}
def get_data():
    data = {}  # 'filename': string -> (tracker_data, iptrack_data): tuple
    for filename in os.listdir(os.getcwd() + "/" + data_folder):
        data[filename] = ip.iptrack(data_folder + filename)

    return data

# input: tracker data for one file
# returns max_cor: np.array [[xcor ycor]]
def extract_maxvalues(coordinates: np.array):
    data = coordinates

    # compare values before and after current value to check if current is the topmost.
    def checkrange(data, n, i):
        for k in range(i - n, i + n):
            if data[k][2] > data[i][2]:
                return False
        return True

    # get the index of the point with the highest y-value in the first 15 elements
    max_index = np.argmax(np.max(data[:15, [2]], axis=1))
    x_max, y_max = data[max_index][1], data[max_index][2]
    max_cor = np.array([(x_max, y_max)])  # initialize array

    # we already have the highest coordinates, so just start at index 20.
    for i in range(20, len(data)-1):
        if checkrange(data, 5, i):
            max_cor = np.append(max_cor, [(data[i][1], data[i][2])], axis=0)
    return max_cor

def curvefit(max_cor: np.array):

    # used in scipy.optimize.curve_fit()
    def curvefit_func(x_max: np.array, a, b):
        return a * np.exp(-b * x_max)

    # covert x- and y-values to 1 dim arrays
    xdata, ydata = max_cor[:,[0]].flatten(), max_cor[:,[1]].flatten()

    # use scipy function. values in fit corresponds to 'a' and 'b' in curvefit_func()
    fit, covar = curve_fit(curvefit_func, xdata, ydata)
    return fit, covar

def acc(alpha, c, v, m):
    g = 9.8214675
    acc = (5/7) * g * np.sin(alpha) - (c * v / m)
    return acc

def euler(coordinates, iptrack, h):
    xn = coordinates[0][1]  # startx
    vn = 0

    approx = np.array([(xn, 0.)])

    for i in range(10):
        tvs = tv.trvalues(iptrack, xn)
        y, dydx, d2ydx2, alpha, R = tvs


        # TODO: whaaat ----------------------------------
        vn = vn + h*acc(alpha, )
        xn = xn + abs(vn1) * np.cos(alpha)
        yn = y + h*dydx
        # -----------------------------------------------

        print("\ntvs: ", tvs)
        print("\nvn1: %s\nxn: %s\nyn: %s" % (vn1, xn, yn))

        approx = np.append(approx, [(xn, yn)], axis=0)

def potential(coordinates):
    def mgh(h):
        return 0.0302 * 9.8214675 * h

    ys = coordinates[:,[1][0]]
    potentials = []
    for i in range(1, len(coordinates)):
        potentials.append(mgh(ys[i-1]) - mgh(ys[i]))

    return potentials


if __name__ == "__main__":
    print("whoop \n\n")

    CURVEFIT = False
    EULER = False
    POTENTIAL = True
    m = 0.0302

    data = get_data()
    filenames = data.keys()

    if CURVEFIT:
        for filename in filenames:
            print(filename)
            tracker_data = data[filename][0]
            maxvalues = extract_maxvalues(tracker_data)

            fit, covar = curvefit(maxvalues)
            #std = np.sqrt(np.diag(covar))
            a, b = fit[0], fit[1]

            c = 2*m*b

            s = """%s\na: %s\nb: %s\nc: %s\ncovar: %s 
            
            """ % (filename, a, b, c, covar)

            print("\n\nA: %s\nb: %s\nc: %s " % (fit[0], fit[1], c))
            print("covar: ", covar.__str__())

            save_data(filename + "_curvefit", s)

    if EULER:
        filename = '51.txt'
        #for filename in filenames:
        print(filename)
        tracker_data = data[filename][0]
        iptrack = data[filename][1]
        maxvalues = extract_maxvalues(tracker_data)
        approx = euler(maxvalues, iptrack, 0.001)

        print(approx)

    if POTENTIAL:
        for filename in filenames:
            print(filename)
            tracker_data = data[filename][0]
            maxvalues = extract_maxvalues(tracker_data)

            pots = potential(maxvalues)
            print("potentials: ", pots)



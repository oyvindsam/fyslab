import os
import numpy as np
from scipy.optimize import curve_fit

import iptrack as ip
import truevalues as tv


data_folder = "data/"
out_folder = "out/"


# Returns dict{'filename': (data: np.array, polyfit: np.array)}
def get_iptrack():
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


def euler(max_values):
    for filename, data in get_iptrack().items():
        print("\n" + filename)
        x_start = data[0][0][1]

        iptrack = data[1]

        print("x: ", x_start)
        print("iptrack: ", iptrack)

        tvs = tv.trvalues(iptrack, x_start)

        print("tv: ", tvs)


if __name__ == "__main__":
    print("whoop \n\n")

    iptrack_data = get_iptrack()
    filenames = iptrack_data.keys()

    for filename in filenames:
        print(filename)
        tracker_data = iptrack_data[filename][0]
        maxvalues = extract_maxvalues(tracker_data)

        fit, covar = curvefit(maxvalues)
        a, b = fit[0], fit[1]

        print("\n\nA: %s\nb: %s " % (fit[0], fit[1]))
        print("covar: ", covar)


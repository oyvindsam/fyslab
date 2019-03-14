import os
import numpy as np
from scipy.optimize import curve_fit

import iptrack as ip
import truevalues as tv


data_folder = "data/"
out_folder = "out/"


# Returns list<np.array>
def get_iptrack():
    data = {}  # 'filename': string -> (tracker_data, iptrack_data): tuple
    for filename in os.listdir(os.getcwd() + "/" + data_folder):
        data[filename] = ip.iptrack(data_folder + filename)

    return data


def curvefit(coordinates: np.array):

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
    max_cor = np.array([(x_max, y_max)])

    # we already have the highest coordinates, so just start at 20.
    for i in range(20, len(data) -5):
        if checkrange(data, 5, i):
            max_cor = np.append(max_cor, [(data[i][1], data[i][2])], axis=0)

    return max_cor


#b = curvefit

def euler():
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
    n = iptrack_data.keys()


    for filename, data in iptrack_data.items():
        print(filename)
        print(curvefit(data[0]))


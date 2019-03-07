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


def curvefit():

    def checkrange(data):
        if data[i - 5][2] < data[i][2] \
               and data[i - 4][2] < data[i][2] \
               and data[i - 3][2] < data[i][2] \
               and data[i - 2][2] < data[i][2] \
               and data[i - 1][2] < data[i][2] \
               and data[i + 1][2] < data[i][2] \
               and data[i + 2][2] < data[i][2] \
               and data[i + 3][2] < data[i][2] \
               and data[i + 4][2] < data[i][2] \
               and data[i + 5][2] < data[i][2]:
            return True

    for filename, data in get_iptrack().items():
        print(filename)
        data = data[0]
        x_max, y_max = data[0][1], data[0][2]
        max_cor = np.array([(x_max, y_max)])

        for i in range(5, len(data) -5):

            if (checkrange(data)):
                max_cor = np.append(max_cor, [(data[i][1], data[i][2])], axis=0)

        print("maxcor: ", max_cor)
        print(len(max_cor))


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

    curvefit()
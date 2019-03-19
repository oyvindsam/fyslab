import os
import numpy as np
from scipy.optimize import curve_fit

import iptrack as ip
import truevalues as tv


data_folder = "data/"
out_folder = "out/"


def extract_x_y_time(filename, t = False, x = False, y = False):
    f = open(filename, "r")
    l = f.readlines()
    f.close()
    x_y_t_list = []
    for i in range(2,len(l)):
        x_y_t_list.append(l[i].strip("\n").split("\t"))
    if t:
        t_list =[]
        for line in x_y_t_list:
            t_list.append(float(line[0]))
    if x:
        x_list = []
        for line in  x_y_t_list:
            x_list.append(float(line[1]))
    if y:
        y_list = []
        for line in x_y_t_list:
            y_list.append(float(line[2]))
    if t and x and y:
        return t_list,x_list,y_list
    if t and x:
        return t_list,x_list
    if t and y:
        return t_list,y_list
    if x and y:
        return x_list,y_list
    if t:
        return t_list
    if x:
        return x_list
    if y:
        return y_list



for value in (extract_x_y_time("data/45.txt",False,False,True)):
    print(value)


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
    t_max, y_max = data[max_index][0], data[max_index][2]
    max_cor = np.array([(t_max, y_max)])  # initialize array

    # we already have the highest coordinates, so just start at index 20.
    for i in range(20, len(data)-1):
        if checkrange(data, 5, i):
            max_cor = np.append(max_cor, [(data[i][0], data[i][1])], axis=0)
    return max_cor

"""
data = get_data()
filenames = data.keys()

for filename in filenames:
    max_string = ""
    print(filename)
    tracker_data = data[filename][0]
    maxvalues = extract_maxvalues(tracker_data)
    max_string += str(maxvalues)
    save_data("time_ycoor" + filename,max_string)
"""

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






if __name__ == "__main__":
    print("whoop \n\n")

    CURVEFIT = False
    EULER = False
    m = 0.0302

    data = get_data()
    filenames = data.keys()

    if CURVEFIT:
        for filename in filenames:
            print(filename)
            tracker_data = data[filename][0]
            maxvalues = extract_maxvalues(tracker_data)
            save_data("toppunkter_" + filename, maxvalues.__str__())

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




"""callculate loss in potential energy for each oscillation:"""

# From one trail: creates a list of y-coordiantes for the top point of each oscillation
# returns list of heights: [height_of_oscillation1, height_of_oscillation2, ...]
def get_data(filename):
    ys = []                                 # will store coordinates
    f = open("out/" + filename, "r")
    l = f.readlines()
    for element in l:
        ys.append(round(float(element[15:25]), 5))   # character 15-25 on each line is y-coordinate
    return ys


# returns list containing data from each trail of experiment: [trail1, trail2, trail3...]
# trail1 = [height_of_oscillation1, height_of_oscillation2, ...]
# trail2 = [oscillation1, oscillation2, ...]
def collect_all_tops():
    list_of_tops = []
    for filename in os.listdir(os.getcwd() + "/out"):
        if "toppunkter" in filename:
            top = get_data(filename)
            list_of_tops.append(top)
    return list_of_tops


"""calculate average height of each top point in all trails of experiment"""


# for each trail of the experiment: take the average height of each oscillation
# argument: list_of_ys = list of trails returned from  method collect_all_tops
# returns: [avg_height_oscillation1, avg_height_oscillation2, avg_height_oscillation2]
def avg_top_y_coords(list_of_trails):
    avg_heights = []
    number_of_oscillations = len(list_of_trails[0])
    number_of_trails = len(list_of_trails)
    for oscillation_number in range(number_of_oscillations):
        sum = 0
        for trail_number in range(number_of_trails):
            sum += list_of_trails[trail_number][oscillation_number]
        avg_heights.append(round(sum/number_of_trails, 5))
    return avg_heights



def avg_heights_to_file():
    avg_heights_string = ""
    avg_list = avg_top_y_coords(collect_all_tops())
    for i in range(len(avg_list)):
        avg_heights_string += "[average height of oscillation no " + str(i) + ": " + str(avg_list[i]) + "\n"
    f = open("out/avg_height_per_oscillation", "w+")
    f.write(avg_heights_string)
    f.close()




"""Calculate Standard deviations in the measurement of top points """

#Takes arguments:
#                   list_of_trails: returned from method collect_all_tops()
#                   list_of_average_heights: retrurned from method avg_top_y_coords(collect_all_tops))
#returns:
#                   list of float values representing standard deviations of each oscillations:
#                   [standard_deviation_oscillation1, standard_deviation_oscillation2, ...]


def standard_dev_heights(list_of_trails, list_of_average_heigths):

    standard_deviations = []
    number_of_oscillations = len(list_of_trails[0])
    number_of_trails = len(list_of_trails)

    for oscillation_number in range(number_of_oscillations):

        # standard deviation = sqrt(variance)
        # variance = sum of deviations from mean squared over N
        sums_of_mean_deviations_squared = 0

        for trail_number in range(number_of_trails):
            sums_of_mean_deviations_squared += (list_of_trails[trail_number][oscillation_number] -
                                                list_of_average_heigths[oscillation_number]) ** 2

        standard_deviation = np.sqrt((1 / (number_of_trails - 1)) * sums_of_mean_deviations_squared)
        standard_deviations.append(round(standard_deviation, 5))
    return standard_deviations

"""feil i gjennomsnitt av høydene
mean_errors = []
for standard_deviation in standard_dev_heights(collect_all_tops(), avg_top_y_coords(collect_all_tops())):
    feil_i_gjennomsnitt = round(standard_deviation / np.sqrt(10), 5)
    print(feil_i_gjennomsnitt)
"""

"""save standard deviations to file: (does not include "standard deviation for oscillation number i:")
std_dev_string = ""
for oscillation in standard_dev_heights(collect_all_tops(), avg_top_y_coords(collect_all_tops())):
    std_dev_string += str(oscillation) + "\n"
save_data("standard_deviations_for_top_y_measurements.txt",std_dev_string)
"""


# takes argument:
# ydata = list of average y coordinates of top points: returned from method avg_top_y_coords()
# ydata_errors = list returned from standard_dev_heights
# boolean energies, errors. If energies = True calculate potential energies,
# if errors = true calculate error in potential energy
def calculate_pot_energy(ydata, ydata_errors = None, energies = False, errors = False):
    m = 0.0302
    g = 9.8214675
    m_error = 0.001
    g_error = 0.0000004
    if energies:
        pot_energies = []
        for i in range(len(ydata)):
            h = ydata[i]
            pot_energies.append(round(m * g * h, 5))
        return pot_energies
    if errors:
        pot_energies_error = []
        for i in range(len(ydata_errors)):
            """error = sqrt((h*g*(m_error))² + (m*h*(g_error))² + (m*g*(h_error))²)"""
            error = round(np.sqrt((ydata[i] * g * m_error)**2 +
                            (ydata[i] * m * g_error)**2 +
                            (m * g * ydata_errors[i])**2), 5)
            pot_energies_error.append(error)
            print(error)
        return pot_energies_error


#loss of potential energy by taking mg(h_n-1 - h_n)
def pot_energy_loss(ydata):
    g = 9.8214675
    loss = []                               #will store loss in potential energy for each oscillation
    for i in range(1, len(ydata)):
        dh = ydata[i-1] - ydata[i]          #dh = difference between top of previous oscillation and current oscillation
        loss.append(round(m*g*dh, 5))
    return loss


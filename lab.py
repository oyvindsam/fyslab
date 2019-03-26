import matplotlib.pyplot as plt


import numpy as np

from forces import force_friction, force_normal
from fys import potential, half_life
from util import get_data, extract_maxvalues, curvefit, save_data, plotData
from util import get_data, extract_maxvalues, curvefit, save_data
from speed import calculate_speed, position_speed_numeric, plot_speed

if __name__ == "__main__":
    print("whoop \n\n")

    CURVEFIT = False
    EULER = False
    POTENTIAL_DELTA = False
    POTENTIAL_MAX = True
    FORCE = False
    FORCE_N = False
    SPEED = False
    PLOT_FORCES = False
    HEIGHT_MEASUREMENTS = False
    NICE_DATA = False

    data = get_data()
    filenames = data.keys()

    half_rate = []

    heights = [[] for x in range(21)]

    for filename in filenames:
        print(filename)
        tracker_data = data[filename][0]
        polynomial = data[filename][1]
        maxvalues = extract_maxvalues(tracker_data) # obs. maxvalues has t-max, x-max, y-max
        tracker_data = tracker_data[:2000]
        t_start = maxvalues[0][0]
        x_start = maxvalues[0][1]
        y_start = maxvalues[0][2]
        #gjennsomsnitt halveringstid

        # add height measurements
        for i in range(len(maxvalues)):
            heights[i].append(maxvalues[i][2])

        if SPEED:
            if filename != '45.txt':  # 45.txt gives weird results
                pos_num, speeds_num, ts_num = position_speed_numeric(x_start, y_start, polynomial)
                pos_tr, speeds_tr, ts_length = calculate_speed(tracker_data)

                pos_num = pos_num[::round(len(pos_num)/len(pos_tr))]  # extract same numer of x values from numeric
                speeds_num = speeds_num[::round(len(speeds_num)/len(speeds_tr))]

                # values in dictionary are arguments for plotData: [x-axis, y-axis, splot-label]
                ds = {
                    1: [ts_length, speeds_num, "fart numerisk"],
                    2: [ts_length, speeds_tr, "fart reell"]
                }

                dp = {
                    1: [ts_length, pos_num, "posisjon numerisk"],
                    2: [ts_length, pos_tr, "posisjon reell"]
                }

                plotData(ds, title="Hastighet", ylabel="hastighet v [m/s]")
                plotData(dp, title="Posisjon", ylabel="posisjon [m]")

                exit()


        if PLOT_FORCES:
            if filename != '45.txt':  # 45.txt gives weird results

                n = 20000
                ffs, xsf = force_friction(x_start, polynomial, n=n)
                fns, xsn = force_normal(x_start, polynomial, n=n)
                t = np.linspace(0, 20, n)

                # values in dictionary are arguments for plotData: [x-axis, y-axis, splot-label]
                # meters from origo as x-axis
                dt = {
                    1: [xsf, ffs, "friksjonskraft f"],
                    2: [xsf, fns, "normalkraft N"]
                }

                # time as x-axis
                dx = {
                    1: [t, ffs, "friksjonskraft f"],
                    2: [t, fns, "normalkraft N"]
                }

                plotData(dt, "Kraft-x", "kraft [N]", "tid t [s]")
                plotData(dx, "Kraft-x", "kraft [N]", "posisjon x-akse [m]")
                exit()

        if FORCE:
            force_friction(x_start, polynomial)
            exit()

        if FORCE_N:
            force_normal(x_start, polynomial)
            exit()

        if CURVEFIT:
            fit, covar = curvefit(maxvalues)
            #std = np.sqrt(np.diag(covar))
            a, b = fit[0], fit[1]

            c = 2*m*b

            s = """%s\na: %s\nb: %s\nc: %s\ncovar: %s 
            
            """ % (filename, a, b, c, covar)

            print("\n\nA: %s\nb: %s\nc: %s " % (fit[0], fit[1], c))
            print("covar: ", covar.__str__())

            save_data(filename + "_curvefit", s)

        if POTENTIAL_DELTA:
            potetial_energies = potential(maxvalues, True)
            print("potentials: ", potetial_energies)

        if POTENTIAL_MAX:
            #if filename != '45.txt':
                potetial_energies = potential(maxvalues, pot_delta=False)
                fit, covar = half_life(potetial_energies)
                #print("Curve fit for %s is %s" % (filename, fit[0]))
                pots_max = potetial_energies[:, [1]].flatten()
                pots_time = potetial_energies[:, [0]].flatten()
                pot_init = pots_max[0]

                def half_func(time: np.array, t_init, t_half):
                    return t_init * (1 / 2) ** (time / t_half)


                half_times = half_func(pots_time, pot_init, t_half=fit[0])
                #print(half_times)
                # time as x-axis
                d_pot = {
                    1: [pots_time, pots_max, "potensiell energi réell"],
                    'kurve': [pots_time, half_times, "potensiell energi analystisk"],
                }

                #plotData(d_pot, "Potensiell energi", "potensiell energi J [J]", "tid t [s]", plot_type='scatter')

                half_rate.append(fit[0])

                #exit()

    if POTENTIAL_MAX:
        half_rate = np.array(half_rate)
        print("Half life ", half_rate)
        print("std error: ", np.std(half_rate) / len(half_rate))
        print("average :", np.average(half_rate))

    if HEIGHT_MEASUREMENTS:
        heights = np.array([np.array(height) for height in heights])
        std_heights = np.array([np.std(height) for height in heights])

        print("std_errors: ", std_heights)



    if NICE_DATA:
        """
        vi trenger:
        
        """
        print("Heights:\n")
        for height in heights:
            print("Std height")
import numpy as np

from forces import force_friction, force_normal
from fys import potential
from util import get_data, extract_maxvalues, curvefit, save_data, plotData
from util import get_data, extract_maxvalues, curvefit, save_data
from speed import calculate_speed, position_speed_numeric, plot_speed

if __name__ == "__main__":
    print("whoop \n\n")

    CURVEFIT = False
    EULER = False
    POTENTIAL = False
    FORCE = False
    FORCE_N = False
    SPEED = True
    PLOT_FORCES = False

    data = get_data()
    filenames = data.keys()

    for filename in filenames:
        print(filename)
        tracker_data = data[filename][0]
        polynomial = data[filename][1]
        maxvalues = extract_maxvalues(tracker_data)
        x_start = maxvalues[0][0]
        y_start = maxvalues[0][1]

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
            n = 20000
            ffs, xsf = force_friction(x_start, polynomial, n=n)
            fns, xsn = force_normal(x_start, polynomial, n=n)
            t = np.linspace(0, 20, n)

            d = {
                1: [t, ffs, "friksjonskraft f"],
                2: [t, fns, "normalkraft N"]
            }
            plotData(d, "Kraft", "kraft [N]", "tid t [s]")
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

        if POTENTIAL:
            pots = potential(maxvalues)
            print("potentials: ", pots)


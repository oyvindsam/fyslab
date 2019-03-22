import numpy as np

from forces import force_friction, force_normal
from fys import potential
from util import get_data, extract_maxvalues, curvefit, save_data, plotData

if __name__ == "__main__":
    print("whoop \n\n")

    CURVEFIT = False
    EULER = False
    POTENTIAL = False
    FORCE = False
    FORCE_N = False
    PLOT_FORCES = True

    data = get_data()
    filenames = data.keys()

    for filename in filenames:
        print(filename)
        tracker_data = data[filename][0]
        polynomial = data[filename][1]
        maxvalues = extract_maxvalues(tracker_data)
        x_start = maxvalues[0][0]


        if PLOT_FORCES:
            n = 20000
            ffs, xsf = force_friction(x_start, polynomial, n=n)
            fns, xsn = force_normal(x_start, polynomial, n=n)
            t = np.linspace(0, 20, n)

            d = {
                1: [t, ffs, "friksjonskraft f [Nm]"],
                2: [t, fns, "Normalkraft N [Nm]"]
            }
            plotData(d, "Krefter", "N/m", "tid t [s]")
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


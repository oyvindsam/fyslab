from forces import force_friction, force_normal
from fys import potential
from util import get_data, extract_maxvalues, curvefit, save_data
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    print("whoop \n\n")

    CURVEFIT = False
    EULER = False
    POTENTIAL = False
    FORCE = False
    FORCE_N = False
    SPEED = True

    data = get_data()
    filenames = data.keys()

    for filename in filenames:
        print(filename)
        tracker_data = data[filename][0]
        polynomial = data[filename][1]
        maxvalues = extract_maxvalues(tracker_data)
        x_start = maxvalues[0][0]

        if SPEED:
            time_list = []
            position_list = []
            speed_list = []

            for i in range(len(tracker_data)):
                if(i==0):
                    speed_list.append(tracker_data[i][0])
                    time_list.append(tracker_data[i][0])
                    position_list.append(np.sqrt(
                        (tracker_data[i][1])**2  # x-value squared
                        + (tracker_data[i][2]**2  # y-value squared
                           )))

                else:
                    delta_time = tracker_data[i][0]-tracker_data[i-1][0]
                    delta_x = tracker_data[i][1]-tracker_data[i-1][1]
                    delta_y = tracker_data[i][2]-tracker_data[i-1][2]
                    calculated_speed = np.sqrt(
                        (delta_x/delta_time)**2 +
                        (delta_y/delta_time)**2
                    )

                    speed_list.append(calculated_speed)
                    position_list.append(np.sqrt(
                        (tracker_data[i][1])**2  # x-value squared
                        + (tracker_data[i][2]**2  # y-value squared
                           )))
                    time_list.append(tracker_data[i][0])

            speed = {
                "time":time_list,
                "position":position_list,
                "speed":speed_list
            }

            print(speed["time"],"\n",speed["position"],"\n",speed["speed"])

            plt.plot(speed["time"], speed["position"], label="p(t)")
            plt.plot(speed["time"], speed["speed"], label="v(t)")
            plt.legend()
            plt.savefig("speed_time_position.png")
            plt.show()
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

import numpy as np
import matplotlib.pyplot as plt

from fys import euler


def calculate_speed(tracker_data):
    time_list = []
    position_list = []
    speed_list = []

    for i in range(len(tracker_data)):
        if i == 0:
            speed_list.append(0)
            time_list.append(tracker_data[i][0])
            position_list.append(np.sqrt(
                (tracker_data[i][1]) ** 2  # x-value squared
                + (tracker_data[i][2] ** 2  # y-value squared
                   )))

        else:
            delta_time = tracker_data[i][0] - tracker_data[i - 1][0]
            delta_x = tracker_data[i][1] - tracker_data[i - 1][1]
            delta_y = tracker_data[i][2] - tracker_data[i - 1][2]
            calculated_speed = np.sqrt(
                (delta_x / delta_time) ** 2 +
                (delta_y / delta_time) ** 2
            )

            speed_list.append(calculated_speed)
            position_list.append(np.sqrt(
                (tracker_data[i][1]) ** 2  # x-value squared
                + (tracker_data[i][2] ** 2  # y-value squared
                   )))
            time_list.append(tracker_data[i][0])

    speed_dict = {
        "time": time_list,
        "position": position_list,
        "speed": speed_list
    }

    print(speed_dict["time"], "\n", speed_dict["position"], "\n", speed_dict["speed"])

    return speed_dict

def plot_speed(speed_dict):
    plt.plot(speed_dict["time"], speed_dict["position"], label="p(t)")
    plt.legend()
    plt.xlabel("tid t [s]")
    plt.ylabel("distanse fra origo [m]")
    plt.savefig("time_position.png")
    plt.show()

    plt.plot(speed_dict["time"], speed_dict["speed"], label="v(t)")
    plt.legend()
    plt.xlabel("tid t [s]")
    plt.ylabel("fart v m/s")
    plt.savefig("time_speed.png")
    plt.show()

    #return speed


def position_speed_numeric(x_start, y_start, poly: np.array, v_start=0, n=20000):
    xn, vn = x_start, v_start
    x_prev, y_prev = x_start, y_start
    print(x_prev, y_prev)
    dt = 20 / n
    speeds = []
    positions = []
    ts = np.linspace(0, 20, n)

    for i in range(n):
        xn, vn, acc, alpha, r, y = euler(xn, vn, poly, dt=dt)
        positions.append(np.sqrt(xn ** 2 + y ** 2))
        speeds.append(vn)
        #x_prev, y_prev = xn, y

    return positions, speeds, ts

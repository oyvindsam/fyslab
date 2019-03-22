import numpy as np
import matplotlib.pyplot as plt


def calculate_speed(tracker_data):
    time_list = []
    position_list = []
    speed_list = []

    for i in range(len(tracker_data)):
        if i == 0:
            speed_list.append(tracker_data[i][0])
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

    speed = {
        "time": time_list,
        "position": position_list,
        "speed": speed_list
    }

    print(speed["time"], "\n", speed["position"], "\n", speed["speed"])

    plt.plot(speed["time"], speed["position"], label="p(t)")
    plt.plot(speed["time"], speed["speed"], label="v(t)")
    plt.legend()
    plt.savefig("speed_time_position.png")
    plt.show()

    return speed

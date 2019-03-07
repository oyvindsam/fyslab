import os
import iptrack as ip


data_folder = "data/"
out_folder = "out/"


# Returns list<np.array>
def get_iptrack():
    data = {}  # 'filename': string -> (tracker_data, iptrack_data): tuple
    for filename in os.listdir(os.getcwd() + "/" + data_folder):
        data[filename] = ip.iptrack(data_folder + filename)

    return data

if __name__ == "__main__":
    for filename, data in get_iptrack().items():
        print(filename)
        x_start = data[0][0][1]


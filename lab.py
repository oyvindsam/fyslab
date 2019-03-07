import os
import iptrack as ip


data_folder = "data/"
out_folder = "out/"

if __name__ == "__main__":
    for filename in os.listdir(os.getcwd() + "/" + data_folder):
        print(filename)
        poly = ip.iptrack(data_folder + filename)

        f = open(out_folder + filename + "_iptrack", "w+")
        f.write(poly.__str__())
        f.close()

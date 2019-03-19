import os
import numpy as np
import iptrack
import truevalues
import scipy.optimize as optimize
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter

data_folder = "data/"
out = "out/"



def get_time_y(filename):
    f = open("out/"+filename, "r")
    time_ycooor = f.readlines()
    f.close()
    time_list = []
    y_list = []
    for element in time_ycooor:

        time_list.append(float(element[2:7]))
        y_list.append(float(element[25:37]))
    return time_list, y_list


calculate_average_time = False
if (calculate_average_time):
    avg_time = []
    std_deviations = []
    for i in range(21):
        time_passed = 0
        for filename in os.listdir(os.getcwd()+"/out"):
            if "time_xcoor_ycoor" in filename:
                time, y = get_time_y(filename)
                time_passed += time[i]
        avg_time.append(round(time_passed / 10, 5))
    print(avg_time)
    for i in range(21):
        variance = 0
        for filename in os.listdir(os.getcwd()+"/out"):
            if "time_xcoor_ycoor" in filename:
                time, y = get_time_y(filename)
                variance += (time[i] - avg_time[i])**2
        std_deviations.append(round(np.sqrt((1/9) * variance), 5))
    print(std_deviations)






calculate_b = False
if(calculate_b):
    for filename in os.listdir(os.getcwd() + "/out"):
        if "time_xcoor_ycoor" in filename:
            print(filename)
            filenumber = filename[16:18]
            print(filenumber)
            time, y = get_time_y(filename)
            y_array = np.array(y)
            time_array = np.array(time)

            def func(tdata, b):
                return y[0] * np.exp(-b * tdata)

            b_value, cov = optimize.curve_fit(func,time_array,y_array)

            curvefit_string = "b: " + str(b_value).strip("[").strip("]")+ "\ncovariance: " +  str(cov).strip("[").strip("]")
            f = open("out/plots/curve_fit_output_"+filenumber+".txt","w+")
            f.write(curvefit_string)
            f.close()


            plt.figure()
            plt.title("optimized curve trail " + filenumber)
            plt.plot(time_array, func(time_array, b_value), label = "curvefit of\ny(t)=a*e^(-bt)\na="
                     +str(y[0])+"\nb="+str(b_value).strip("[").strip("]"))
            plt.plot(time_array, y_array, 'ro')
            plt.legend()
            plt.xlabel("time / sec")
            plt.ylabel("y(t) / meter")
            plt.grid()
            plt.savefig("out/plots/optimized_curve_"+filenumber+".png")
            plt.show()



"""Calculate optimized b value for a function A*e^(-bt) that tangents each y coordinate of top
point measured in the experiemnt.
calulated based on average measured heights, and average time each height was
 reached, for all 10 experiments"""

avg_heights = [0.50461, 0.46702, 0.41634, 0.38814, 0.34718, 0.3252, 0.29349, 0.27857, 0.25147, 0.23902, 0.21711, 0.20624, 0.18635, 0.17779, 0.16049, 0.15415, 0.13914, 0.13461, 0.12121, 0.1166, 0.10451]
avg_time_for_tops = [0.009, 1.098, 2.157, 3.204, 4.238, 5.257, 6.269, 7.271, 8.271, 9.262, 10.249, 11.23, 12.207, 13.182, 14.148, 15.117, 16.078, 17.042, 18.001, 18.957, 19.909]

calculate_b_from_avarages = False
if(calculate_b_from_avarages):
    y_array = np.array(avg_heights)
    time_array = np.array(avg_time_for_tops)

    def func(tdata, b):
        return avg_heights[0] * np.exp(-b * tdata)

    b_value, cov = optimize.curve_fit(func,time_array,y_array)

    curvefit_string = "b: " + str(b_value).strip("[").strip("]")+ "\ncovariance: " +  str(cov).strip("[").strip("]")
    f = open("out/plots/curve_fit_output_average_heights_+_times.txt","w+")
    f.write(curvefit_string)
    f.close()


    plt.figure()
    plt.title("optimized curve for average heights and times")
    plt.plot(time_array, func(time_array, b_value), label = "curvefit of\ny(t)=a*e^(-bt)\na="
             +str(avg_heights[0])+"\nb="+str(b_value).strip("[").strip("]"))
    plt.plot(time_array, y_array, 'ro')
    plt.legend()
    plt.xlabel("time")
    plt.ylabel("y(t)")
    plt.grid()
    plt.savefig("out/plots/optimized_curve_avergae_times_+_heights.png")
    plt.show()



"""plot potential energy as func of time"""
plot_pot_en = False
if plot_pot_en:
    avg_potential_energies = [
        0.14967,
        0.13852,
        0.12349,
        0.11513,
        0.10298,
        0.09646,
        0.08705,
        0.08263,
        0.07459,
        0.0709,
        0.0644,
        0.06117,
        0.05527,
        0.05273,
        0.0476,
        0.04572,
        0.04127,
        0.03993,
        0.03595,
        0.03458,
        0.031]

    plt.figure()
    plt.title("average potential energy at each oscillation as function of time")
    plt.plot(avg_time_for_tops, avg_potential_energies)
    plt.plot(avg_time_for_tops, avg_potential_energies, 'ro')
    plt.xlabel("time / sec")
    plt.ylabel("Ep / mgh")
    plt.grid()
    plt.savefig("out/plots/average_potential_energys.png")
    plt.show()





def v_prime(v,c,alpha):
    m = 0.0302
    g = 9.8214675
    return (5/7)*(g*np.sin(alpha) - ((c * v)/m))

def euler(x_n,y_n, v_abs, c, poly):
    dt = 0.01
    alpha = truevalues.trvalues(poly,x_n)[3]
    v_abs_next = v_abs + dt*((5/7) * v_prime(v_abs,c,alpha))
    vx_next = v_abs_next * np.cos(alpha)
    vy_next = (v_abs_next * np.sin(alpha)) + ((v_abs**2)/truevalues.trvalues(poly,x_n)[4])
    x_next = x_n + (dt * (vx_next))
    y_next = y_n + (dt * vy_next)
    return x_next, y_next, v_abs_next


true_x = []
true_y = []

f = open("data/45.txt")
q = 0
for line in f.readlines():
    if(len(true_x) > 1999): #or len(true_y) > 1999:
        continue
    if q < 2:
        q += 1
    else:
        line = line.strip("\n").split("\t")
        tempList = []
        for element in line:
            tempList.append(float(element))
        true_x.append(float(tempList[1]))
        true_y.append(float(tempList[2]))
f.close()

true_x_array = np.array(true_x)
true_y_array = np.array(true_y)

c = 0.006
v_abs_next = 0
x_next = 0.6445934164187707
y_next = 0.5016737029272254
x_array = []
y_array = []

tracker_polynomial = iptrack.iptrack("data/45.txt")

for i in range(2000):
    x_next, y_next, v_abs_next = euler(x_next, y_next, v_abs_next, c, tracker_polynomial)
    x_array.append(x_next)
    y_array.append(y_next)
x = np.array(x_array)
y = np.array(y_array)


"""
f = open("out/eulerXYResult.txt", "w+")
f.write("x(t):\n\n[")
x_string = ""
vx_string = ""
y_string = ""
vy_string = ""

for i in range(len(x_array)):
    for j in range(10):
        x_string += (str(x_array[i]) + ", ")
        if(j == 9):
            x_string += "\n"
            f.write(x_string)
        j += 1 % 10
f.write("\n\n\n\nvx(t):\n\n[")
for i in range(len(vx_array)):
    for j in range(10):
        vx_string += (str(vx_array[i]) + ", ")
        if(j == 9):
            vx_string += "\n"
            f.write(vx_string)
        j += 1 % 10
f.write("]\n\n\n\ny(t):\n\n[")

for i in range(len(y_array)):
    for j in range(10):
        y_string += (str(y_array[i]) + ", ")
        if(j == 9):
            y_string += "\n"
            f.write(y_string)
        j += 1 % 10


f.write("\n\n\n\nvy(t):\n\n[")
for i in range(len(vy_array)):
    for j in range(10):
        vy_string += (str(vy_array[i]) + ", ")
        if(j == 9):
            vy_string += "\n"
            f.write(vy_string)
        j += 1 % 10

f.write("]")
f.close()
"""
t = np.linspace(0,20, 2000)
plt.plot(t,true_x_array, label = "truex(t)")
#plt.plot(t, true_y_array, label = "truey(t)")
plt.plot(t, x, label = "estx(t)")
#plt.plot(t,y, label = "esty(t)")
plt.legend()
plt.savefig("estimated_vs_true_x(t).png")
plt.show()
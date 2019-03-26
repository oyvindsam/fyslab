import os
import scipy

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

def get_time_x(filename):
    f = open("out/" + filename, "r")
    time_ycooor = f.readlines()
    f.close()
    time_list = []
    x_list = []
    for element in time_ycooor:
        time_list.append(float(element[2:7]))
        x_list.append(float(element[14:25]))
    return time_list, x_list



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


def calculate_avrage(value_list):
    sum = 0
    for value in value_list:
        sum += value
    return (sum/len(value_list))

def calculate_standard_dev(avg_value, measured_values):
    sum_of_mean_deviations_squared = 0
    for value in measured_values:
        sum_of_mean_deviations_squared += (value - avg_value)**2
    return np.sqrt(sum_of_mean_deviations_squared/(len(measured_values) - 1))


def calculate_b(plot=False):
    bs = []
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
            bs.append(b_value[0])
            curvefit_string = "b: " + str(b_value).strip("[").strip("]")+ "\ncovariance: " +  str(cov).strip("[").strip("]")
            #f = open("out/plots/curve_fit_output_"+filenumber+".txt","w+")
            #f.write(curvefit_string)
            #f.close()
    if plot:
        plt.figure()
        plt.title("optimized curve trail " + filenumber)
        plt.plot(time_array, func(time_array, b_value), label = "curvefit of\ny(t)=a*e^(-bt)\na="
                 +str(y[0])+"\nb="+str(b_value).strip("[").strip("]"))
        plt.plot(time_array, y_array, 'ro')
        plt.legend()
        plt.xlabel("time / sec")
        plt.ylabel("y(t) / meter")
        plt.grid()
        #plt.savefig("out/plots/optimized_curve_"+filenumber+".png")
        plt.show()
    return bs

bs = calculate_b()
def calculate_c(bs):
    m = 0.0302
    m_error = 0.001
    b_standard_dev = calculate_standard_dev(calculate_avrage(bs), bs)
    cs = []
    for b_value in bs:
        c = 2*b_value*m
        ec = np.sqrt((2*b_value*m_error)**2 + (2*m*b_standard_dev))
        cs.append(c)
    return cs

print(calculate_c(bs))

def calculate_average_c(cs):
    sum = 0
    for c in cs:
        sum+= c
    return sum/len(cs)

def calculate_c_std_dev(cs):
    sum_of_mean_dev_squared = 0
    avg_c = calculate_average_c(cs)
    for c in cs:
        sum_of_mean_dev_squared += (c-avg_c)**2
    return np.sqrt(sum_of_mean_dev_squared / (len(cs) -1))

def calculate_c_standard_error(std_dev, n):
    return std_dev/np.sqrt(n)

cs = calculate_c(calculate_b())
avg_c = calculate_average_c(cs)
c_std_dev = calculate_c_std_dev(cs)
c_std_err = calculate_c_standard_error(c_std_dev, 10)
print ("gjennomsnittlig c: " + str(avg_c))
print("standardfeil i c: " + str(c_std_err))



"""Calculate optimized b value for a function A*e^(-bt) that tangents each y coordinate of top
point measured in the experiemnt.
calulated based on average measured heights, and average time each height was
 reached, for all 10 experiments"""

avg_heights = [0.50461, 0.46702, 0.41634, 0.38814, 0.34718, 0.3252, 0.29349, 0.27857, 0.25147, 0.23902, 0.21711, 0.20624, 0.18635, 0.17779, 0.16049, 0.15415, 0.13914, 0.13461, 0.12121, 0.1166, 0.10451]
avg_time_for_tops = [0.009, 1.098, 2.157, 3.204, 4.238, 5.257, 6.269, 7.271, 8.271, 9.262, 10.249, 11.23, 12.207, 13.182, 14.148, 15.117, 16.078, 17.042, 18.001, 18.957, 19.909]

calculate_b_from_avarages = False
def calculate_b_from_avarages():
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
calculate_loss_pot_energy = False
avg_potential_energies = np.array([
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
    0.031])
times = np.array([
    0.009,
    1.098,
    2.157,
    3.204,
    4.238,
    5.257,
    6.269,
    7.271,
    8.271,
    9.262,
    10.249,
    11.23,
    12.207,
    13.182,
    14.148,
    15.117,
    16.078,
    17.042,
    18.001,
    18.957,
    19.909])
if plot_pot_en:
    def func1(times,a):
        return (a*times + 0.14967)

    optimals = scipy.optimize.curve_fit(func1, times, avg_potential_energies)
    print(optimals[0][0])
    #plot and scatter potential energy as function of time. curve fit of pot energy as func of time
    plt.figure()
    plt.title("average potential energy at each oscillation as function of time")
    plt.plot(avg_time_for_tops, avg_potential_energies)
    plt.plot(avg_time_for_tops, avg_potential_energies, 'ro')
    #plt.plot(times, func1(times,optimals[0][0]))
    plt.plot()
    plt.xlabel("time / sec")
    plt.ylabel("Ep / mgh")
    plt.grid()
    plt.savefig("out/plots/average_potential_energys.png")
    plt.show()
if calculate_loss_pot_energy:
    sum_of_potential_energies = 0
    for i in range(1, len(avg_potential_energies)):
        sum_of_potential_energies += (avg_potential_energies[i] - avg_potential_energies[i-1])
    average_loss_of_potential_energy = (sum_of_potential_energies/len(avg_potential_energies))
    print(average_loss_of_potential_energy)






def v_prime(v,c,alpha):
    m = 0.0302
    g = 9.8214675
    return (5/7)*(g*np.sin(alpha) - ((c * v)/m))

def euler(x_n, v_abs, c, poly, n):
    dt = 20 / n
    alpha = truevalues.trvalues(poly,x_n)[3]
    v_abs_next = v_abs + dt*(v_prime(v_abs,c,alpha))
    vx_next = v_abs_next * np.cos(alpha)
    x_next = x_n + (dt * (vx_next))
    return x_next, v_abs_next

def Euler_and_plot(filename,n):
    true_x = []
    true_y = []

    f = open(filename)
    q = 0
    #read data from file
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

    c = 0.0041
    v_abs_next = 0
    x_next = 0.6445934164187707
    x_array = []

    tracker_polynomial = iptrack.iptrack("data/45.txt")

    #execute euler with 2000 steps of size 0.01s
    for i in range(n):
        x_next, v_abs_next = euler(x_next, v_abs_next, c, tracker_polynomial,n)
        x_array.append(x_next)
    num_x = np.array(x_array)
    num_y = truevalues.trvalues(tracker_polynomial,num_x)[0]
    print(num_y)

    t = np.linspace(0,20, n)
    true_t = np.linspace(0,20,2000)

    #plot results:
    #plt.plot(t, y, label= "truevalues result y(t)")
    #plt.plot(true_t, true_y_array, label = "measured y(t) with tracker")
    plt.plot(true_t,true_x_array, label = "true x(t)")
    #plt.plot(true_x_array, true_y_array, label = "true y(t)")
    plt.plot(t, num_x, label = "Euler x(t)")
    #plt.plot(x,y, label = "curvefit y(t)")
    #plt.ylabel("y(x) / meter")
    plt.ylabel("x(t) / meter")
    plt.xlabel("t / sec")
    plt.legend()
    #plt.title("y(t) results given by Truevalues.trvalues\nvs. y(t) results as measured with tracker")
    #plt.title("x(t)-verdier funnet ved Eulers metode (blå), vs. \nverdier observert med Tracker(oransje)\nc=0.0041")
    #plt.savefig("truevalues_result_y(x)_VS_true_y(x).png")
    #plt.savefig("euler_vs_true_x(t).png")
    plt.show()

#Euler_and_plot("data/55.txt", 10000)
"""finn ett standardavvik for b"""
perr = np.sqrt(np.diag([8.8070832e-07]))
print(perr)


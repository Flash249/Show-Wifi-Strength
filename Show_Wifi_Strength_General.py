#program to see and plot wifi network strength
import subprocess                                           #library for executing and getting result of cmd commands
#@Windows
import numpy as np                                          #library for using random number
from itertools import count                                 #Library for just counting next integer(used for seconds in program)
import matplotlib.pyplot as plt                             #library for plotting of graph
from matplotlib.animation import FuncAnimation as animate   #library for plotting live graph
import platform                                             #library for identifying operating system
#@Linux
import time                                                 #library for creating delay                         
import argparse                                             #for parsing from bytes to text

#lists that contains variables to plot on x axis and y axis
x_vals=[]                       #empty list for time
signal_vals=[]                  #empty list for signal values

#index element would be used to go to next second(integer, ex- 1,2,3,...)
index = count()

#get which operating system the program is being executed
def get_os():
    operating_system=platform.system()
    return operating_system

#function that will get network strength using subprocess library
def get_windows_signal_value():
    #main command that will return details such as network name, strength, receive rate and transmit rate
    results = subprocess.check_output(["netsh","wlan","show","interface"]).decode()
    #splitting the result to separate out necessary details
    lines = results.split('\r\n')
    #contains the results in line by line format and converting results in dictionary format
    d = {}
    for line in lines:
        if ':' in line:
            vals = line.split(':')
            if vals[0].strip() != '' and vals[1].strip() != '':
                d[vals[0].strip()] = vals[1].strip()

    #Global variables
    global network_name, channel

    #finding signal strength, channel number, network name, receive speed and transmit speed
    for key in d.keys():
        if key == "Signal":                     #finding signal
            quality = d[key][:-1]               #removing %    
            quality = int(quality)              #converting in integer
        
        if key == "SSID":                       #finding network name
            network_name = d[key]
        
        if key == "Channel":                    #finding channel number
            channel = d[key]
        
        if key == "Receive rate (Mbps)":        #finding receiving rate
            re_speed = d[key]
        if key == "Transmit rate (Mbps)":       #finding transmit rate
            tr_speed = d[key]

    #converting percentage to rssi value(dBm)
    if(quality == 0):
        dBm = -100
    elif(quality >= 100):
        dBm = np.random.randint(-50, -25)       #for 100% signal value it lies between (-20 to -50 dBm)
    else:
        dBm = (quality / 2) - 100

    return dBm, quality, re_speed, tr_speed     #function returns signal %, dBm, receive rate and transmit rate

def plot_graph(i):

    #main function that plots the graph

    x_vals.append(next(index))                              #values to plot on X
    dBm, quality, receive, transmit = get_windows_signal_value()     #executing and retreiving speed
    signal_vals.append(dBm)                                 #values to be plotted on y

    plt.cla()                                               #fixing the colour of graph line
    plt.plot(x_vals,signal_vals)                            #plotting the points(x,y)
    
    plt.title("Graph of Signal Strength (dBm vs Time)\n"    #title of the graph with details    
    "\nNetwork name:- "+network_name+"    Channel:- "+channel+
              "\n\nReceive Rate:- "+receive+" Mbps    Transmit rate:- "+transmit+" Mbps"+
              "\n\nSignal Strength:- "+str(quality)+"%    equivalent dBm:- "+str(dBm).format()+" dBm")
    plt.xlabel("Time interval(1 seconds)")                  #label on X-axis
    plt.ylabel("Signal Strength in dBm")                    #label on Y-axis

def plot_windows_graph():
    #use of style for the plotting of the graph
    plt.style.use("fivethirtyeight")
    ani = animate(plt.gcf(), plot_graph, interval=1000)         #interval shows after what duration we have to get the strength

    plt.get_current_fig_manager().window.state('zoomed')        #maximizing the output screen
    plt.tight_layout()
    plt.show() 

def values_in_linux():
    parser = argparse.ArgumentParser(description='Display WLAN signal strength.')
    parser.add_argument(dest='interface', nargs='?', default='wlan0',help='wlan interface (default: wlan0)')
    args = parser.parse_args()

    print('\n---Press CTRL+Z or CTRL+C to stop.---\n')

    while True:
        cmd = subprocess.Popen('iwconfig %s' % args.interface, shell=True, stdout=subprocess.PIPE)
        for line in cmd.stdout:
            if 'Link Quality' in line:
                print (line.lstrip(' '))
            elif 'Not-Associated' in line:
                print ('No signal')
        time.sleep(1)

def values_in_osx():
    print('\n---Press CTRL+Z or CTRL+C to stop.---\n')

    while True:
        scan_cmd = subprocess.Popen(['airport', '-s'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        scan_out, scan_err = scan_cmd.communicate()
        scan_out_lines = str(scan_out).split("\\n")[1:-1]
        for each_line in scan_out_lines:
            split_line = [e for e in each_line.split(" ") if e != ""]
            print(split_line)
            print("The signal strength is(dBm) :", -1*int(split_line[2]))

def get_windows_wifi_signal():
    plot_windows_graph()

def get_linux_wifi_signal():
    values_in_linux()

def get_macOS_wifi_signal():
    values_in_osx()

#finding out of the appropriate OS and executing that 
def show_signal_strength():
    operating_system = get_os()

    if operating_system=='Windows':
        get_windows_wifi_signal()
    elif operating_system=='Darwin':
        get_macOS_wifi_signal()
    elif operating_system=='Linux':
        get_linux_wifi_signal()
    else:
        print("Progam can be executed only on Windows, Mac and Linux Operating System")

#main driver program
show_signal_strength()
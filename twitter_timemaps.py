from datetime import datetime
from os import times
from matplotlib.pyplot import title
import numpy as np
import matplotlib.pylab as plt
import pandas as pd
import time
import datetime

def timemap_plot(userID):
    df = pd.read_csv(r"C:\Users\johan\OneDrive - Aarhus universitet\UNI\3 år\bachelor\Ny mappe\Documents\Tweets\tweet" + str(userID) + ".csv")['created_at'].values.tolist()
    # a sample array containing the timings of events in order: [1, 2.1, 2.9, 3.1...]
    times = []
    for timestamp in reversed(df):
        t = time.mktime(datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").timetuple())
        times.append(t)

    # calculate time differences:
    diffs = np.array([times[i]-times[i-1] for i in range(1,len(times))])
    new_d = []
    
    for d in diffs:
        c = 0
        if d > 1:
            d = d/60
            c += 1
        if d > 1:
            d = d/60
            c += 1
        if d > 1:
            d = d/24
            c += 1
        if d > 1:
            d = d/7
            c += 1
        new_d.append(d+c)
    
    n = len(df)
    a = np.arange(n-2)

    xcoords = new_d[:-1] # all differences except the last
    ycoords = new_d[1:] # all differences except the first
    time_x = [0, 1, 2, 3, 4, 5]

    fig = plt.figure(figsize=(10,20))
    ax = fig.add_subplot(111)

    plt.title("Time Map: User " + str(userID) + " with " + str(n) + " tweets.")
    plt.rc('font', size=16)
    plt.xlabel("Time after last tweet")
    plt.ylabel("Time before next tweet")
    ax.xaxis.set_ticks(time_x) #set the ticks to be a
    ax.xaxis.set_ticklabels(["0", "1 Sec", "1 Min", "1 Hour", "1 Day", "1 Week"]) # change the ticks' names to x

    ax.yaxis.set_ticks(time_x) #set the ticks to be a
    ax.yaxis.set_ticklabels(["0", "1 Sec", "1 Min", "1 Hour", "1 Day", "1 Week"]) # change the ticks' names to x

    ax.plot(xcoords, ycoords, 'b.') # make scatter plot with blue dots

    plt.xlim([1, 5])
    plt.ylim([1, 5])
    plt.show()

timemap_plot(973774553036898304)
from os import listdir
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas
from IPython.display import display

base_dir = "./pcap_stats/"

dir_names = [f for f in listdir(base_dir)]

for dir in dir_names:
    print(dir)
    file_names = [f for f in listdir(base_dir + dir)]
    timeseries = []
    timestamps = []

    def get_ipv4_bytes(line):
        if "IPv4 bytes:" == line[0:11]:
            key, value_raw = line.split(":")
            value = int(value_raw.strip())
            return key, value
        
        return None

    def get_timestamp(line, type):
        if type + " timestamp:" == line[0:len(type) + 11]:
            key, value_raw = line.split(":")
            value = float(value_raw.strip())
            return key, value
        
        return None

    #################
    # Data cleaning #
    #################

    for i, fn in enumerate(file_names):
        pcap_stats_file = open(base_dir + '{}/'.format(dir) + fn, "r")

        for line in pcap_stats_file.readlines():
            if get_ipv4_bytes(line): ipv4_bytes_key, ipv4_bytes_value = get_ipv4_bytes(line)
            if get_timestamp(line, "First"): first_timestamp_key, first_timestamp_value = get_timestamp(line, "First")
            if get_timestamp(line, "Last"): last_timestamp_key, last_timestamp_value = get_timestamp(line, "Last")

        if ipv4_bytes_key and ipv4_bytes_value: timeseries.append(ipv4_bytes_value)
        if (first_timestamp_key and first_timestamp_value) and (last_timestamp_key and last_timestamp_value): timestamps.append([first_timestamp_value, last_timestamp_value])

        pcap_stats_file.close()

    ########################
    # Dataframe generation #
    ########################

    init_datetimes = [datetime.utcfromtimestamp(t[0]) for t in timestamps]
    end_datetimes = [datetime.utcfromtimestamp(t[1]) for t in timestamps]

    dataframe_values = list(zip(init_datetimes, end_datetimes, timeseries))
    dataframe = pandas.DataFrame(dataframe_values, columns=['init_date', 'end_date', 'bytes'])

    display(dataframe)

    # Save dataframe to a CSV file.
    dataframe.to_csv('./time_series_df_{}.csv'.format(dir), index = False) 

    ###################
    # Timeseries plot #
    ###################

    x_values = np.array([(i + 5) for i in range(len(timestamps))])
    y_values = np.array([t/(1024 * 1024) for t in timeseries]) # Convert Bytes to MB.

    fig, ax = plt.subplots()
    plt.plot(x_values, y_values)
    ax.ticklabel_format(useOffset=False)
    ax.ticklabel_format(style='plain')
    plt.xlabel("Step")
    plt.ylabel("MB")
    plt.ylim(0, np.max(y_values) + np.max(y_values)/2)
    plt.title("Step vs Total Bytes")
    plt.show()
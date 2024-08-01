#!/home/rtem/miniconda3/envs/ipensive/bin/python
# -*- coding: utf-8 -*-
"""
Created on 30-Mar-2022
@author: awech
"""

import os
import pandas as pd
from obspy import UTCDateTime

# import config
import barry_config as config

# print(f"TEST HOSTNAME IS {config.HOSTNAME}")


from ipensive_array_processing import process_array

### Done! Now collecting ascii files and determining missing time steps:


T1 = "2022-09-05 00:00"  # May 1
T2 = "2022-11-01 00:00"

#
# COMPLETED TIMES:
#
# Missing lots of data from ~09-08 to 07-17 or so. Retry after finishing all?
#
# T1 = "2023-05-14 18:00"  # May 1 TO
# T2 = "2023-10-01 00:00"  # October 1

OVERWRITE = False

# ARRAYS=['Akutan']
# specify ARRAYS if you want to just process specific arrays
# ARRAYS=['Wake Island North', 'Wake Island South']
# ARRAYS = ['Kenai','Sand Point','Okmok','Cleveland','Adak','Amchitka','Dillingham']
# ARRAYS = ['Saipan']

ARRAYS = ["Barry Arm East"]


def run_backpopulate(T1, T2):

    t1 = UTCDateTime(T1) + config.DURATION
    for t in pd.date_range(T2, t1.strftime("%Y%m%d%H%M"), freq="-10min"):
        print(t)
        for network in config.NETWORKS:
            for array in network["ARRAYS"]:

                # set up filename
                year = "{:.0f}".format(t.year)
                day = "{:03.0f}".format(t.dayofyear)
                time = t.strftime("%Y%m%d-%H%M")
                file = "{}/{}/{}/{}/{}/{}_{}.png".format(
                    config.OUT_WEB_DIR,
                    network["Name"],
                    array["Name"],
                    year,
                    day,
                    array["Name"],
                    time,
                )
                # filename example:

                # check if you should process this time window
                # check for png at 'file', or overwrite it
                if not os.path.exists(file) or (os.path.exists(file) and OVERWRITE):

                    # check if you should process this array
                    if "ARRAYS" in dir():
                        if array["Name"] in ARRAYS:
                            process_array(array, network, UTCDateTime(t))
                        else:
                            print("Array name not on do list. Skip " + array["Name"])
                    else:
                        process_array(array, network, UTCDateTime(t))
                else:
                    print("File exists. No overwrite. Skip " + array["Name"])

    return


if __name__ == "__main__":

    # TESTING PURPOSES:
    print(f"WINDOW = {config.WINDOW_LENGTH}   OVERLAP = {config.OVERLAP}")

    run_backpopulate(T1, T2)

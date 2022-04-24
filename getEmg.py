# Copyright (C) 2015  Niklas Rosenstein, MIT License
# Last modified by Yi Jui Lee (August 15 2015)

from __future__ import division

import time
from os.path import exists
import pandas as pd
import myo
from myo.lowlevel import stream_emg
from myo.six import print_

open('Emg', 'w').close()

last_t = 0
delta_t = []
timestamp_list = []
data_list = []

flag = True

df_myo = pd.DataFrame()

temp = []
with open('PythonVars.txt') as f:
    for val in f:
        temp.append(int(val))

samplerate = temp[0]
t_s = 1 / samplerate
print("\n\nSample rate is adjusted to " + str(samplerate) + " Hz")
print("Collecting emg data every " + str(t_s) + " seconds")

file_number = 0
r = "EMG_READINGS\Emg_" + str(file_number) + ".csv"
while (exists(r)):
    file_number = file_number + 1
    r = "EMG_READINGS\Emg_" + str(file_number) + ".csv"

T = temp[1]
print("\n\nThis program will terminate in " + str(T) + " seconds\n")

myo.init()
r"""
There can be a lot of output from certain data like acceleration and orientation.
This parameter controls the percent of times that data is shown.
"""


class Listener(myo.DeviceListener):
    # return False from any method to stop the Hub

    def on_connect(self, myo, timestamp):
        print_("Connected to Myo")
        myo.vibrate('short')
        myo.set_stream_emg(stream_emg.enabled)
        myo.request_rssi()
        global start
        start = time.time()

    def on_rssi(self, myo, timestamp, rssi):
        print_("RSSI:", rssi)

    def on_event(self, event):
        r""" Called before any of the event callbacks. """

    def on_event_finished(self, event):
        r""" Called after the respective event callbacks have been
        invoked. This method is *always* triggered, even if one of
        the callbacks requested the stop of the Hub. """

    def on_pair(self, myo, timestamp):
        print_('Paired')
        print_("If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")


    def on_disconnect(self, myo, timestamp):
        print_('on_disconnect')

    def on_emg(self, myo, timestamp, emg):
        global start
        global t2
        global t_s
        global r
        current = time.time()
        tdiff = current - start
        t2 = timestamp
        if 't1' not in globals():
            global t1
            t1 = timestamp

        start = time.time()
        show_output('emg', emg, r)

    def on_unlock(self, myo, timestamp):
        print_('unlocked')

    def on_lock(self, myo, timestamp):
        print_('locked')

    def on_sync(self, myo, timestamp):
        print_('synced')

    def on_unsync(self, myo, timestamp):
        print_('unsynced')


def show_output(message, data, r):
    global t2
    global t1
    global T
    global delta_t
    global df_myo
    global flag

    global timestamp_list
    global data_list

    if t2 - t1 < (T * 1000000):
        df_myo = df_myo.append(pd.Series({'timestamp': t2,
                                          'EMG_s0': data[0],
                                          'EMG_s1': data[1],
                                          'EMG_s2': data[2],
                                          'EMG_s3': data[3],
                                          'EMG_s4': data[4],
                                          'EMG_s5': data[5],
                                          'EMG_s6': data[6],
                                          'EMG_s7': data[7]},
                                         ), ignore_index=True)
        # print('t:{:<9}: '.format(
        #     (t2 - t1) / 1000000) + '[{:>8},  {:>8},  {:>8}, {:>8},  {:>8},  {:>8},  {:>8},  {:>8}]'
        #       .format(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
    else:
        if flag:
            print("End of data acquisition")
            print("Saving " + r + " ...")
            df_myo.to_csv(r, index=False)
            print(r + " saved")
            flag = False
        # quit()


def main():

    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)

    input("Press Enter to continue...\n")

    hub.run(1000, Listener())

    print("Running...\n")

    # Listen to keyboard interrupts and stop the
    # hub in that case.
    try:
        while hub.running:
            myo.time.sleep(0.2)
    except KeyboardInterrupt:
        print_("Quitting ...")
        hub.stop(True)


if __name__ == '__main__':
    main()

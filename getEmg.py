# Copyright (C) 2015  Niklas Rosenstein, MIT License
# Last modified by Yi Jui Lee (August 15 2015)

from __future__ import division
import time
import myo
from myo.lowlevel import stream_emg
from myo.six import print_
from os.path import exists

open('Emg', 'w').close()

last_t = 0
delta_t = []

flag = True

temp = []
with open('PythonVars.txt') as f:
    for val in f:
        temp.append(int(val))

samplerate = temp[0]
t_s = 1 / samplerate
print("\n\nSample rate is adjusted to " + str(samplerate) + " Hz")
print("Collecting emg data every " + str(t_s) + " seconds")

file_number = 0
r = "EMG_READINGS\Emg_" + str(file_number) + ".txt"
while (exists(r)):
    file_number = file_number + 1
    r = "EMG_READINGS\Emg_" + str(file_number) + ".txt"

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
        print_(
            "If you don't see any responses to your movements, try re-running the program or making sure the Myo works with Myo Connect (from Thalmic Labs).")
        print_("Double tap enables EMG.")
        print_("Spreading fingers disables EMG.\n")

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
        if tdiff > t_s:
            start = time.time()
            show_output('emg', emg, r, tdiff)

    def on_unlock(self, myo, timestamp):
        print_('unlocked')

    def on_lock(self, myo, timestamp):
        print_('locked')

    def on_sync(self, myo, timestamp):
        print_('synced')

    def on_unsync(self, myo, timestamp):
        print_('unsynced')


def show_output(message, data, r, tdiff):
    global t2
    global t1
    global T
    global delta_t
    global last_t
    global flag

    if t2 - t1 < (T * 1000000):
        delta_t.append(tdiff)
        with open(r, "a") as text_file:
            text_file.write("{0}\n".format(data))
            print('t:{:<9}: '.format(
                (t2 - t1) / 1000000) + '[{:>8},  {:>8},  {:>8}, {:>8},  {:>8},  {:>8},  {:>8},  {:>8}]'
                  .format(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7]))
        last_t = t2
    else:
        if flag:
            print(delta_t)
            print(len(delta_t))
            print((len(delta_t) - 1) / sum(delta_t[1:]))
            flag = False
        # quit()


def main():
    hub = myo.Hub()
    hub.set_locking_policy(myo.locking_policy.none)
    hub.run(1000, Listener())

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

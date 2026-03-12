"""
Joe Snider  3/12/2026
Parse a set of bin files from a disco mode recording.
Each time point is N_POSITION positions with (in this order!) Ambient, White, and Blue driver.
These are compatible with fiji import.
Only writes full time points.
Also note that X1 mode is hacked into the RawImage reader.
"""

"""
Copyright 2026  Scripps Institution of Oceanography
Distributed under MIT license. See license.txt for more information.
"""

from raw_image import RawImage
import glob
import cv2
import h5py
import numpy as np

N_POSITION = 9

# assumes we call clean_timepoint on each one as they are appended
def is_timepoint_complete(w):
    return len(w) == 3*N_POSITION

# check that last element is possible
# modifies w to just be the last time point if the last is bad
# specialized for disco mode output from the bump
def clean_timepoint(w):
    if len(w) < 2:
        # any single is potentially valid
        return
    
    if len(w) % 3 == 1:
        # make sure every third steps forward
        last_position = w[-1][0]['position']
        second_last_position = w[-2][0]['position']
        last_time = w[-1][0]['camera_micros']
        second_last_time = w[-2][0]['camera_micros']
        if last_time > second_last_time and last_position > second_last_position:
            return
        else:
            del w[:-1]
    else:
        # make sure the 2nd and 3rd frames are at the same position
        last_position = w[-1][0]['position']
        second_last_position = w[-2][0]['position']
        last_time = w[-1][0]['camera_micros']
        second_last_time = w[-2][0]['camera_micros']
        if last_time > second_last_time and last_position == second_last_position:
            return
        else:
            del w[:-1]

def save_timepoint(w, t):
    if len(w) != 3*N_POSITION:
        print("Warning: attempting to write bad data ... skipping, but this is bad")
        return

    # probably a clever way to do this
    red_ambient = np.dstack([x[1] for x in w[0::3]]).transpose(2, 0, 1)
    green_ambient = np.dstack([x[2] for x in w[0::3]]).transpose(2, 0, 1)
    blue_ambient = np.dstack([x[3] for x in w[0::3]]).transpose(2, 0, 1)
    with h5py.File('disco_ambient.hdf5', 'a') as hfout:
        hfout.create_dataset(f"/t{t}/channel0", data=red_ambient)
        hfout.create_dataset(f"/t{t}/channel1", data=green_ambient)
        hfout.create_dataset(f"/t{t}/channel2", data=blue_ambient)

    red_white = np.dstack([x[1] for x in w[1::3]]).transpose(2, 0, 1)
    green_white = np.dstack([x[2] for x in w[1::3]]).transpose(2, 0, 1)
    blue_white = np.dstack([x[3] for x in w[1::3]]).transpose(2, 0, 1)
    with h5py.File('disco_white.hdf5', 'a') as hfout:
        hfout.create_dataset(f"/t{t}/channel0", data=red_white)
        hfout.create_dataset(f"/t{t}/channel1", data=green_white)
        hfout.create_dataset(f"/t{t}/channel2", data=blue_white)

    red_blue = np.dstack([x[1] for x in w[2::3]]).transpose(2, 0, 1)
    green_blue = np.dstack([x[2] for x in w[2::3]]).transpose(2, 0, 1)
    blue_blue = np.dstack([x[3] for x in w[2::3]]).transpose(2, 0, 1)
    with h5py.File('disco_blue.hdf5', 'a') as hfout:
        hfout.create_dataset(f"/t{t}/channel0", data=red_blue)
        hfout.create_dataset(f"/t{t}/channel1", data=green_blue)
        hfout.create_dataset(f"/t{t}/channel2", data=blue_blue)

if __name__ == "__main__":
    fils = glob.glob("C:/Users/oldst/bump/long_capture/1771464988/*bin")
    fils.sort()

    w = []
    timepoint = 0
    fcnt = 0

    for f in fils:
        print(f"File {fcnt}/{len(fils)}", f)
        fcnt += 1
        R1 = RawImage(f)
        
        for i in range(R1.frames_in_file):
            f1, q = R1.read_frame(i)
            qq_red = cv2.cvtColor(q[0::2, 0::2], cv2.COLOR_GRAY2BGR)
            qq_green = cv2.cvtColor((q[0::2, 1::2]+q[1::2, 0::2])//2, cv2.COLOR_GRAY2BGR)
            qq_blue = cv2.cvtColor(q[1::2, 1::2], cv2.COLOR_GRAY2BGR)

            w.append([f1, cv2.split(qq_red)[0], cv2.split(qq_green)[0], cv2.split(qq_blue)[0]])
            
            clean_timepoint(w)
            if is_timepoint_complete(w):
                save_timepoint(w, timepoint)
                timepoint += 1



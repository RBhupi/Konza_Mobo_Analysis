import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import sys
import glob
from datetime import datetime as dt
import argparse


def getStatDF(file_list, crop):
    tmean, tmax, tmin, tstd, dt_object = getStat(file_list, crop)
    celsius_df = pd.DataFrame(index=dt_object, dtype="float")
    celsius_df['mean'] = tmean
    celsius_df['max'] = tmax
    celsius_df['min'] = tmin
    celsius_df['std'] = tstd
    return celsius_df

def getStat(file_list, crop):
    nfiles = len(file_list)
    
    tmean = np.zeros(nfiles)
    tmax = np.zeros(nfiles)
    tmin = np.zeros(nfiles)
    tstd = np.zeros(nfiles)
    dt_object = np.zeros(nfiles, dtype='datetime64[s]')
    

    for fcount, fname in enumerate(file_list):
        celsius = np.loadtxt(fname, delimiter=";", skiprows=8)
        
        celsius_crop = celsius[crop, :]
        
        tmean[fcount] = celsius_crop.mean()
        tmax[fcount] = celsius_crop.max()
        tmin[fcount] = celsius_crop.min()
        tstd[fcount] = celsius_crop.std()
        dt_object[fcount] = fileDatetime(fname)
    
    return tmean, tmax, tmin, tstd, dt_object





def fileDatetime(fname):
    """ Extracts timestamp from the thermal raw data filename and returns 
    date-time string.
    """
    match = re.search(string=fname, pattern="\d{19}")
    if match is None:
        sys.exit("Error: file name does not contain date-time stamp.")
        
    dt_stamp = int(match.group())
    dt_object = dt.fromtimestamp(dt_stamp/10**9)
    #dt_str = dt.strftime(dt_object, format="%Y%m%d_%H%M%S")
    return(dt_object)



def main(args):
    file_list = glob.glob(args.indir+"*celsius.csv")
    file_list.sort()

    celsius_sky = getStatDF(file_list, crop=np.arange(0, 100))
    celsius_land = getStatDF(file_list, crop=np.arange(112, 252))
    
    celsius_land['2021-12-21'].plot()
    plt.savefig("/Users/bhupendra/projects/thermal/plots/diurnal_land.pdf")
    celsius_sky['2021-12-21'].plot()
    plt.savefig("/Users/bhupendra/projects/thermal/plots/diurnal_sky.pdf")


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-dir", 
                    dest="indir", 
                    type=str,
                    default="/Users/bhupendra/projects/thermal/data_thermal-raw/")
    
    args = parser.parse_args()



im1 = np.loadtxt(file_list[0], delimiter=";", skiprows=8)
im2 = np.loadtxt(file_list[1], delimiter=";", skiprows=8)

im_diff = im1[112:, :] - im2[112:, :]

plt.imshow(im_diff)
plt.imshow(im1[112:, :])
plt.imshow(im2[112:, :])









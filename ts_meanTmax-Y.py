#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 16:06:11 2022

@author: Bhupendra Raut
"""

import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import glob





indir = '/Users/bhupendra/data/konza_burn/radiancetemps/'

file_wildcard1 = 'sage_mobotix_radiancetemps_20220415-1[89]*nc'
flist1 = glob.glob(indir+file_wildcard1)
file_wildcard2 = 'sage_mobotix_radiancetemps_20220415-2[01]*nc'
flist2 = glob.glob(indir+file_wildcard2)

flist = flist1 + flist2
flist.sort()

nfiles = len(flist)
max_mean_mat = np.ndarray(shape=(92, nfiles))
time = []
for f in range(0, nfiles):
    with Dataset(flist[f]) as ncfile:
        ir_temp = ncfile['thermalimage'][:].squeeze()
        ir_temp = ir_temp[160:, :]
        
    
    max_index = np.unravel_index(np.argmax(ir_temp), ir_temp.shape)
    
    max_values = ir_temp[:, max_index[1]-5:max_index[1]+5]
    max_mean = max_values.mean(axis=1)
    
    max_mean_mat[:, f] = max_mean

cnt=plt.contourf(max_mean_mat, levels=100, cmap='gist_ncar')
# This is the fix for the white lines between contour levels
for c in cnt.collections:
    c.set_edgecolor("face")
plt.savefig('/Users/bhupendra/projects/thermal/plots/thermal_tY-max-mean3_contourf.pdf')
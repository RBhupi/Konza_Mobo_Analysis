# Script downaloads Konza Burn data and write it back in netCDF format using xarray.

import subprocess
import os
import tempfile
import csv
import urllib
import datetime
import cftime

import numpy as np
import xarray as xr
import pandas as pd
from matplotlib import pyplot as plt

import sage_data_client

def read_mob_from_sage(url, datet):
    tempf = tempfile.NamedTemporaryFile()
    try:
        urllib.request.urlretrieve(url, tempf.name)
        head = []
        with open(tempf.name, 'r') as f:
            reader = csv.reader(f, delimiter=';')
            for i in range(7):
                headers = next(reader)
                head.append(headers)
            _ = next(reader)
            data = np.expand_dims(np.flipud(np.array(list(reader)).astype(float)), axis=0)
        print(data.shape)
        tt = datet.to_pydatetime()
        ctime = cftime.datetime(tt.year, tt.month, tt.day, hour=tt.hour, minute=tt.minute, second=tt.second)

        ds = xr.Dataset({
        'thermalimage': xr.DataArray(
                    data   = data,   # enter data here
                    dims   = ['time', 'y', 'x'],
                    coords = {'time': [ctime],
                             'y' : np.arange(data.shape[1]),
                             'x' : np.arange(data.shape[2])},
                    attrs  = {
                        '_FillValue': -999.9,
                        'units'     : 'celsius'
                        }
                    ),
                },
            attrs = {'Source': 'MOBOTIX M16 camera operated by Sage',
                    'URL' : url}
        )
    except urllib.error.HTTPError:
        ds="ERROR"
    
    return ds


data_dir = '/Users/bhupendra/data/apiary/radiancetemps/'

df = sage_data_client.query(
    start="2022-10-07T05:51:36.246454082Z",
    end="2022-10-07T23:51:36.246454082Z",
    filter={
        "plugin": "*mobotix-sampler:1.22.4.13*",
        "vsn" : "W02D"
    }
)




targets = []
times = []
for i in range(len(df)):
    if 'celsius' in df.iloc[i].value:
        targets.append(df.iloc[i].value)
        times.append(df.iloc[i].timestamp)

        
for i in range(len(times)): 
    print(times[i])
    my_ds = read_mob_from_sage(targets[i], times[i])
    if my_ds != 'ERROR':
        filename = os.path.join(data_dir,my_ds.time.data[0].strftime('sage_mobotix_radiancetemps_%Y%m%d-%H%M%S.nc'))
        file_exists = os.path.exists(filename)
        if not file_exists:
            print(filename)
            my_ds.to_netcdf(filename)
        else:
            print('File exists exists')
    else:
        print('ERROR '+ targets[i])


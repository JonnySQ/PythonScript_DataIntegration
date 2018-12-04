from netCDF4 import Dataset
import os
import numpy as np

#prints resulting averages data
def PrintResults():
    outputPath = "./Output_Data/"
    
    files = os.listdir(outputPath)
    
    for name in files:
        print(name)
        
        dataset = Dataset(outputPath+name)
        
        atmos_pressure = dataset.variables['atmospheric_pressure']
        temp_mean      = dataset.variables['mean_temperature']
        base_time      = dataset.variables['base_time']
        time           = dataset.variables['time']
        
        print(base_time)
        print(time)
        print(atmos_pressure)
        print(temp_mean)
        
        i = 0
        
        while i < len(atmos_pressure):
            print (base_time[i], time[i], atmos_pressure[i], temp_mean[i])
            i += 1
    return 1
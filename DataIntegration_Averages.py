from netCDF4 import Dataset
import os
import numpy as np

#name file to represent average values ("met" ==> "metavg")
def makeNameAverage(filename):
    
    newName = ""
    
    for i in filename:
        
        newName += i
        if i == 't':
            newName += "avg"
        
    return newName

#finds 5 minute averages
def findAverages(inputPath, outputPath):
    
    files = os.listdir(inputPath)
    
    #go through each file in directory
    for name in files:
        print(name)
        
        #load input data
        dataset = Dataset(inputPath+name)
        newName = makeNameAverage(name)
        newDataset = Dataset(outputPath+newName, 'w', format='NETCDF4_CLASSIC')
        
        #create dimensions
        newDataset.createDimension('time', None)
        
        #create variables
        newDataset.createVariable('atmospheric_pressure', np.float32, 'time')
        newDataset.createVariable('mean_temperature', np.float32, 'time')
        newDataset.createVariable('time', np.float64, 'time')
        newDataset.createVariable('base_time', np.int32)
        
        #extract input data
        atmos_pressure = dataset.variables['atmos_pressure']
        temp_mean      = dataset.variables['temp_mean']
        base_time      = dataset.variables['base_time']   #different each day
        time           = dataset.variables['time']        #same as time offset?
        
        #set up attributes
        #atmospheric pressure
        newAtmos = newDataset.variables['atmospheric_pressure']
        newAtmos.long_name = atmos_pressure.long_name
        newAtmos.units = atmos_pressure.units
        newAtmos.valid_min = atmos_pressure.valid_min
        newAtmos.valid_max = atmos_pressure.valid_max
        newAtmos.valid_delta = atmos_pressure.valid_delta
        newAtmos.missing_value = atmos_pressure.missing_value
        
        #mean temperature
        newTemp = newDataset.variables['mean_temperature']
        newTemp.long_name = temp_mean.long_name
        newTemp.units = temp_mean.units
        newTemp.valid_min = temp_mean.valid_min
        newTemp.valid_max = temp_mean.valid_max
        newTemp.valid_delta = temp_mean.valid_delta
        newTemp.missing_value = temp_mean.missing_value
        
        #base time
        newBaseTime = newDataset.variables['base_time']
        newBaseTime.string = base_time.string
        newBaseTime.long_name = base_time.long_name
        newBaseTime.units = base_time.units
        
        #time variable
        newTime = newDataset.variables['time']
        newTime.long_name = time.long_name
        newTime.units = time.units
        newTime.standard_name = time.standard_name
        
        #loop variables
        i = 0
        j = 0
        
        #find averages
        while i < len(atmos_pressure):
            interval = time[i] + 300
            start = time[i]
            current = start
            occ_count = 0       #number of occurances
            find_atmos = 0      #used to find 5 min avg
            find_temp = 0       #used to find 5 min avg
            
            while current < interval and i < len(atmos_pressure):
                find_atmos += atmos_pressure[i]
                find_temp += temp_mean[i]
                
                occ_count += 1
                i += 1
                if i < len(atmos_pressure):
                    current = time[i]
                else:
                    break
                    
            if find_atmos != 0:
                #resulting numbers to be recorded
                avg_atmos = find_atmos / occ_count
                avg_temp = find_temp / occ_count
                
                newAtmos[j] = avg_atmos
                newTemp[j] = avg_temp
                newBaseTime[j] = base_time[i]
                newTime[j] = start
                j += 1
        
    #close files when finished
    dataset.close()
    newDataset.close()
    return 1
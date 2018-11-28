from netCDF4 import Dataset
import os


#name file to represent average values ("metavg")
def makeNameAverage(filename):
    
    newName = ""
    
    for i in filename:
        
        newName += i
        if i == 't':
            newName += "avg"
        
    return newName


#-------- Main begins here --------#

#Define file or directory to be processed
#TODO: either predefine file, or prompt user for it
inputPath = "./Input_Data/"
outputPath = "./Output_Data/"

files = os.listdir(inputPath)

#if its a directory do this
for name in files:
    print(name)
    
#debugging
#if 1 == 1:
    #name = "sgpmetE13.b1.20181001.000000.cdf"
    
    #load input data
    dataset = Dataset(inputPath+name)
    newName = makeNameAverage(name)
    newDataset = Dataset(outputPath+newName, 'w', format='NETCDF4_CLASSIC')
    
    
    #Create dimensions and variables for newDataset
    
    #newTime = newDataset.createDimension('time', 1440)
    #newDataset.createVariable('atmospheric_pressure',_,_)
    #newDataset.createVariable('temp_mean',_,_)
    
    #identify dimensions debugging
    #print(dataset.dimensions.keys())
    #time_dimension = dataset.dimensions['time']
    #print(time_dimension)
    
    #identify variables debugging
    #print(dataset.variables.keys())
    
    #extract input data
    atmos_pressure = dataset.variables['atmos_pressure']
    temp_mean      = dataset.variables['temp_mean']
    base_time      = dataset.variables['base_time']   #different each day
    time           = dataset.variables['time']        #same as time offset?
    
    print (len(time))
    print(atmos_pressure)
    print(temp_mean)
    
    i = 0
    
    #find averages
    while i < len(atmos_pressure):
        interval = time[i] + 300
        start = time[i]
        current = start
        occ_count = 0
        find_atmos = 0
        find_temp = 0
        
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
            print(base_time[i], start, avg_atmos, avg_temp)
    
    #record averages
    
    #write averages and associated variable to new dataset
    
    #write averages and associated variables to file
    
    #do this for all files
    
    
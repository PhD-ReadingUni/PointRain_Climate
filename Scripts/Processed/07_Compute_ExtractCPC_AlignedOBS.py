import sys
import os
from os.path import exists
from datetime import datetime, timedelta
import numpy as np
import netCDF4 as nc
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

#######################################################################################################################################
# CODE DESCRIPTION
# 07_Compute_ExtractCPC_AlignedOBS.py extracts the gridded rainfall values from the "CPC Global Unified Gauge-Based Analysis of Daily Precipitation" 
# dataset for the nearest grid point to each station in the aligned STVL dataset. 

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# Git_repo (string): path of local github repository
# DirIN_STVL (string): relative path for the input directory containing the aligned point STVL rainfall observations
# DirIN_CPC (string): relative path for the input directory containing the gridded CPC rainfall observations
# DirOUT_CPC (string): relative path for the output directory that will contain the gridded CPC rainfall values for the nearest grid point to the aligned STVL rain stations

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN_STVL = "Data/Processed/06_AlignedOBS_rawSTVL"
DirIN_CPC = "Data/Raw/OBS/CPC"
DirOUT_CPC = "Data/Processed/07_AlignedOBS_gridCPC"
#######################################################################################################################################

np.set_printoptions(suppress=True, formatter={'float_kind':'{:0.2f}'.format})

# Setting main input/output directories
MainDirIN_CPC = Git_repo + "/" + DirIN_CPC + "_" + str(Acc) + "h"
MainDirIN_STVL = Git_repo + "/" + DirIN_STVL + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF)
MainDirOUT_CPC = Git_repo + "/" + DirOUT_CPC  + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF)
if not exists(MainDirOUT_CPC):
      os.makedirs(MainDirOUT_CPC)


###########################
# EXPLORING THE CPC DATASET #
###########################

print(" ")
print(" ")
print("###########################")
print("# EXPLORING THE CPC DATASET #")
print("###########################")


# Extracting metadata about the netcdf files
print(" ")
print("Extracting metadata about the netcdf files")
FileIN_CPC_temp = MainDirIN_CPC + "/precip." + str(2000) + ".nc"
cpc_metadata = nc.Dataset(FileIN_CPC_temp)
print(cpc_metadata)

print(" ")
print("Metadata about the 'time' variable")
cpc_times_metadata = nc.Dataset(FileIN_CPC_temp)["time"]
cpc_times = nc.Dataset(FileIN_CPC_temp)["time"][:] # 1-d numpy array with dimensions given by the number of days in the considered year
cpc_StartTime = datetime(1900,1,1,0,0) # provided by the "units" parameter in the variable "time"
print(" ")
print(cpc_times_metadata)
print(" ")
print("Time values (in cumulative hours from reference date/time):", cpc_times)
print(" ")
print("Date/time CPC rainfall values are valid for are indicated as cumulative hours from the reference date/time provided by the parameter 'units' in the variable 'time'.")
print("Therefore, to compute the date/time CPC rainfall values are valid for, the cumulative hours provided in the variable 'time' need to be added to the reference date/time indicated in the parameter 'units'.")
print("Since the time-zone is omitted in the parameter 'units', date/time are to be considered given in UTC.")
print("For more detailed information about the conventions adopted for the 'time' variable, read the following pdf from page 33: chrome-extension://efaidnbmnnnibpcajpcglclefindmkaj/https://cfconventions.org/Data/cf-conventions/cf-conventions-1.10/cf-conventions.pdf ")
print(" ")
print("Note that the convention to indicate the accumulation period the rainfall values are valid for is different in the CPC dataset than in the STVL dataset.")
print("In CPC, the accumulation period the rainfall values are valid for is indicated by the beginning of the period; in STVL is indicated by the end of the period.")
print("For example, the 24-hourly observations valid for the period between 14/07/2021 00 UTC and 14/07/2021 23.59 UTC are stored in CPC in the file corresponding to the date/time 14/07/2021 00 UTC; in STVL they are stored in the file corresponding to the date/time 15/07/2021 00UTC.")

print(" ")
print("Metadata about the 'lat' / 'lon' variables")
cpc_lats_metadata = nc.Dataset(FileIN_CPC_temp)["lat"]
cpc_lons_metadata = nc.Dataset(FileIN_CPC_temp)["lon"]
cpc_lats = nc.Dataset(FileIN_CPC_temp)["lat"][:] # 1-d numpy array with dimensions given by the number of considered latitudes 
cpc_lons = nc.Dataset(FileIN_CPC_temp)["lon"][:] # 1-d numpy array with dimensions given by the number of considered longitudes 
print(" ")
print(cpc_lats_metadata)
print(" ")
print(cpc_lons_metadata)
print(" ")
print("The CPC grid point values refer to the centre of the grid point. Therefore, there is no need to offset the lat/lon coordinates in order to extract the correct rainfall values.")
print(" ")
print("Latitude coordinates:", cpc_lats)
print("The latitudes format in CPC are compatible with the one in STVL.")
print(" ")
print("Longitude coordinates:", cpc_lons)
print(" ")
print("The longitudes format in CPC are not compatible with the one in STVL. There is the need to transpose the data for longitudes from 0 to 180 to the right, and convert the longitudes from 180 to 360 to the format -180 to 0 by substracting 180.")
cpc_lons_new = np.concatenate([cpc_lons[360:720]-360, cpc_lons[0:360]], axis=0) 
print(" ")
print("New longitude coordinates:", cpc_lons_new)

print(" ")
print("Metadata about the 'precip' variable")
cpc_precip_metadata = nc.Dataset(FileIN_CPC_temp)["precip"]
cpc_precip = nc.Dataset(FileIN_CPC_temp)["precip"][:] # 3-d numpy array with dimensions given by (time, lat, lon) 
print(" ")
print(cpc_precip_metadata)
print(" ")
print(cpc_precip)
print(" ")
cpc_precip_missing_value = nc.Dataset(FileIN_CPC_temp)["precip"].missing_value
print(" ")
print("Missing values will be sostituded here with NaN values.")


# Plotting an example to compare with the online plot to make sure the data is read correctly
print(" ")
print("Plotting an example from the the netcdf dataset (for the 4th of September 2000) to compare with the online plot to make sure the data is been read correctly.")
print("The online plot taken as an example was saved in " + MainDirOUT_CPC + " but it can also be recreated online here: https://psl.noaa.gov/mddb2/makePlot.html?variableID=2781 ")

ValidTime = datetime(2000,9,4)
ind_day = 0 
ValidTime_temp = datetime(2000,1,1)
while ValidTime_temp != ValidTime:
      ind_day += 1
      ValidTime_temp = cpc_StartTime + timedelta(hours = cpc_times[ind_day]) 

cpc_precip = nc.Dataset(FileIN_CPC_temp)["precip"][ind_day,:,:] # 2-d numpy array
cpc_precip_new = np.concatenate([cpc_precip[:,360:720], cpc_precip[:,0:360]], axis=1)
cpc_precip_new = np.where(cpc_precip_new != cpc_precip_missing_value, cpc_precip_new, np.nan)

map = Basemap(projection="cyl",llcrnrlat=-20,urcrnrlat=40,llcrnrlon=-20,urcrnrlon=115,resolution="l")
map.drawcoastlines()
map.drawcountries()
lons,lats= np.meshgrid(cpc_lons_new,cpc_lats)
x,y = map(lons,lats)
bin = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52]
precip = map.contourf(x,y,cpc_precip_new[:,:], bin, cmap=plt.cm.magma)
plt.title("SEP 04, 2000")
cbar = map.colorbar(precip,location='bottom',pad="10%")
cbar.set_label('mm')
plt.show()


##################################################################
# EXTRACTING THE CPC RAINFALL VALUES TO THE NEAREST STVL RAIN STATIONS #
##################################################################

print(" ")
print(" ")
print("####################################################################")
print("# EXTRACTING THE CPC RAINFALL VALUES FOR THE NEAREST STVL RAIN STATIONS  #")
print("####################################################################")

# Reading the STVL rainfall observations over the period of interest and the correspondent metadata (i.e., ids/lats/lons/dates)
print(" ")
print("Reading the STVL point rainfall observations over the period of interest and the correspondent metadata (i.e., ids/lats/lons/dates)")
stvl_stnids = np.load(MainDirIN_STVL + "/stn_ids.npy")
stvl_lats = np.load(MainDirIN_STVL + "/stn_lats.npy")
stvl_lons = np.load(MainDirIN_STVL + "/stn_lons.npy")
stvl_dates = np.load(MainDirIN_STVL + "/dates.npy")
stvl_obs = np.load(MainDirIN_STVL + "/obs.npy")
NumStns = stvl_obs.shape[0]
NumDays = stvl_obs.shape[1]

# Defining the coordinates of the CPC's nearest grid-points to the rain stations in STVL
print(" ")
print("Defining the coordinates of the CPC's nearest grid-points to the rain stations in STVL")
cpc_nearest_lat = []
cpc_nearest_lon = []
for i in range(NumStns):
      lat_temp = stvl_lats[i]
      lon_temp = stvl_lons[i]
      cpc_nearest_lat.append(np.argmin(np.abs(cpc_lats-lat_temp)))
      cpc_nearest_lon.append(np.argmin(np.abs(cpc_lons_new-lon_temp)))

# Extracting the gridded rainfall observations from the CPC dataset for the nearest grid point to each station in the STVL dataset
# Note that the CPC data will be stored using the dates convention from STVL to make it directly comparable with it
cpc_obs = np.empty(stvl_obs.shape) * np.nan 
year_temp = "-1"
print(" ")
print("Extracting the gridded rainfall observations from the CPC dataset for the nearest grid point to each station in the STVL dataset")
print("Considering date: ")
for ind_day_stvl in range(len(stvl_dates)):

      stvl_date_temp = datetime.strptime(stvl_dates[ind_day_stvl], "%Y%m%d") # STVL convention for indicating the dates the observation is valid for
      cpc_date_temp = stvl_date_temp - timedelta(days = 1) # CPC convention for indication the date the correspondent observation is valid for
      cpc_year_temp = cpc_date_temp.strftime("%Y")
      print(" ")
      print(" - STVL: ", stvl_date_temp.strftime("%Y%m%d"), " / CPC: ", cpc_date_temp.strftime("%Y%m%d"))

      if year_temp != cpc_year_temp:
            FileIN_CPC_temp = MainDirIN_CPC + "/precip." + cpc_year_temp + ".nc"
            cpc_times_temp = nc.Dataset(FileIN_CPC_temp)["time"][:]
            cpc_precip_temp = nc.Dataset(FileIN_CPC_temp)["precip"][:]
            year_temp = cpc_year_temp
            print("     - Reading the CPC's netcdf file: ", FileIN_CPC_temp)

      ind_day_cpc = np.where(cpc_times_temp == float((cpc_date_temp - cpc_StartTime).days * 24))[0][0]
      print("     - CPC date is found at index:", ind_day_cpc)
      cpc_precip_temp_new = np.concatenate([cpc_precip_temp[ind_day_cpc, :, 360:720], cpc_precip_temp[ind_day_cpc, :, 0:360]], axis=1)
      cpc_obs[:,ind_day_stvl] = cpc_precip_temp_new[cpc_nearest_lat,cpc_nearest_lon]

cpc_obs = np.where(cpc_obs != cpc_precip_missing_value, cpc_obs, np.nan)

# Saving the gridded CPC rainfall 
print(" ")
print("Saving the gridded CPC rainfall values for the nearest grid point to each station in the STVL dataset in...")
print(MainDirOUT_CPC)
np.save(MainDirOUT_CPC + "/stn_ids.npy", stvl_stnids)
np.save(MainDirOUT_CPC + "/stn_lats.npy", stvl_lats)
np.save(MainDirOUT_CPC + "/stn_lons.npy", stvl_lons)
np.save(MainDirOUT_CPC + "/dates.npy", stvl_dates)
np.save(MainDirOUT_CPC + "/obs.npy", cpc_obs)
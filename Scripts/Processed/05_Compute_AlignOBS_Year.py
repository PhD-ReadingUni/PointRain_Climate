import sys
import os
from os.path import exists
from datetime import date, timedelta
import numpy as np
import pandas as pd
import metview as mv

#######################################################################################################################
# CODE DESCRIPTION
# 05_Compute_AlignOBS_Year.py aligns the observations over a considered year so there are the same number of stations per day over such year.

# DESCRIPTION OF INPUT PARAMETERS
# Year (number, in YYYY format): start year to consider.
# Period (string, in the format YearS_YearF with the years in the YYYY format): period of reference over which the time series is computed.
# Acc (number, in hours): rainfall accumulation period.
# Git_repo (string): path of local github repository
# DirIN_UniqueStnids (string): relative path for the input directory containing the ids/lats/lons of the unique station over the period of interest
# DirIN (string): relative path for the input directory containing the rainfall observations of interest
# DirOUT (string): relative path for the output directory that will contain the aligned observations for the given year

# INPUT PARAMETERS
Year = int(sys.argv[1])
Period = "2000_2019"
Acc = 24
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN_UniqueStnids = "Data/Processed/04_UniqueStnids"
DirIN = "Data/Processed/02_Combined_UniqueOBS"
DirOUT = "Data/Processed/05_AlignedOBS_Year"
#######################################################################################################################


# Setting main input/output directory
MainDirIN_UniqueStnids = Git_repo + "/" + DirIN_UniqueStnids  + "_" + str(Acc) + "h_" +  Period
MainDirIN = Git_repo + "/" + DirIN  + "_" + str(Acc) + "h"
MainDirOUT = Git_repo + "/" + DirOUT  + "_" + str(Acc) + "h"
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Reading the ids/lats/lons for the unqiue stations over the period of interest
stnids_unique = np.load(MainDirIN_UniqueStnids+ "/stnids_unique.npy")
lats_unique = np.load(MainDirIN_UniqueStnids+ "/lats_unique.npy")
lons_unique = np.load(MainDirIN_UniqueStnids+ "/lons_unique.npy")
NumStns = len(stnids_unique)

# Define the list of dates over the considered year
DateS = date(Year,1,2)
DateF = date(Year+1,1,1)
Dates_range = np.array((pd.date_range(DateS.strftime("%Y%m%d"), DateF.strftime("%Y%m%d")).strftime('%Y%m%d')).tolist())
NumDays = len(Dates_range) 

# Aligning the observations for the considered year
aligned_obs = np.empty((NumStns,NumDays,)) * np.nan # initialize the variable that will contain the aligned observations with NaNs, so there won't be any need to deal with stations with no observations on a given day

TheDate = DateS
while TheDate <= DateF:
      
      TheDateSTR  = TheDate.strftime("%Y%m%d")
      TheYearSTR = TheDate.strftime("%Y")
      ind_dates = np.where(Dates_range == TheDateSTR)[0][0]
      print(" - " + TheDateSTR)

      # Reading the rainfall observations as geopoints 
      FileIN_temp = MainDirIN + "/" + TheYearSTR + "/tp" + str(Acc) + "_obs_" + TheDateSTR + ".geo"
      geo = mv.read(FileIN_temp)
      geo_stnids = np.array(mv.stnids(geo))
      geo_obs = mv.values(geo)
      m = len(geo_stnids)
      
      # Assigning observations to the correspondent unique stations and dates
      for i in range(m):
            stnids_temp = geo_stnids[i]
            obs_temp = geo_obs[i]
            ind_stnids = np.where(stnids_unique == stnids_temp)[0][0]
            aligned_obs[ind_stnids,ind_dates] = obs_temp

      TheDate += timedelta(days=1)

# Saving the aligned rainfall observations for the given year as a 2-d numpy array
FileOUT = MainDirOUT + "/" + str(Year) + ".npy"
np.save(FileOUT,aligned_obs)
import os
from os.path import exists
from datetime import date
import numpy as np
import pandas as pd

####################################################################################################################
# CODE DESCRIPTION
# 06_Compute_CombineYears_AlignedOBS.py combines the aligned stvl observations per year over a whole period of interest.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# Git_repo (string): path of local github repository
# DirIN_UniqueStnids (string): relative path for the input directory containing the ids/lats/lons of the unique station over the period of interest
# DirIN (string): relative path for the input directory containing the aligned rainfall observations on a given year
# DirOUT (string): relative path for the output directory that will contain the aligned observations for the whole period of interest

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN_UniqueStnids = "Data/Processed/04_UniqueStnids"
DirIN = "Data/Processed/05_AlignedOBS_Year"
DirOUT = "Data/Processed/06_AlignedOBS_rawSTVL"
####################################################################################################################

# Setting main input/output directory
MainDirIN_UniqueStnids = Git_repo + "/" + DirIN_UniqueStnids  + "_" + str(Acc) + "h_" +  str(YearS) + "_" + str(YearF)
MainDirIN = Git_repo + "/" + DirIN  + "_" + str(Acc) + "h"
MainDirOUT = Git_repo + "/" + DirOUT  + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF) 
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Define the list of dates over the considered period
DateS = date(YearS,1,2)
DateF = date(YearF+1,1,1)
Dates_range = np.array((pd.date_range(DateS.strftime("%Y%m%d"), DateF.strftime("%Y%m%d")).strftime('%Y%m%d')).tolist())
NumDays_period = len(Dates_range)

# Reading the ids/lats/lons for the unqiue stations over the period of interest
stnids_unique = np.load(MainDirIN_UniqueStnids+ "/stnids_unique.npy")
lats_unique = np.load(MainDirIN_UniqueStnids+ "/lats_unique.npy")
lons_unique = np.load(MainDirIN_UniqueStnids+ "/lons_unique.npy")
NumStns_period = len(stnids_unique)

# Merging the aligned observations for each year over the period of interest
print(" ")
print("Merging aligned observations over the period of interest for year ...")
print(" - " + str(YearS))
FileIN_temp = MainDirIN + "/" + str(YearS) + ".npy"
align_obs = np.load(FileIN_temp)
for Year in range(YearS+1,YearF+1):
      print(" - " + str(Year))
      FileIN_temp = MainDirIN + "/" + str(Year) + ".npy"
      align_obs = np.concatenate((align_obs, np.load(FileIN_temp)), axis=1)
NumStns = align_obs.shape[0]
NumDays = align_obs.shape[1]

# Checking that the number of unique stations and number of days over the considered period matches the total number of stations and days for the single imported files
print(" ")
if (NumStns == NumStns_period) and (NumDays == NumDays_period):
      print("Considering " + str(NumStns) + " rainfall stations each day over the period of interest.")
      print("There are " + str(NumDays) + " days over the period of interest.")
elif (NumStns != NumStns_period):
      print("ERROR! The number of the unique stations over the considered period does not match the number of the stations in the single imported files.")
      exit()
elif (NumDays != NumDays_period):
      print("ERROR! The number of days over the considered period does not match the number of the days in the single imported files.")
      exit()

# Saving the aligned observations over the whole considered period
print(" ")
print("Saving the aligned observations over the whole considered period")
np.save(MainDirOUT + "/stn_ids.npy", stnids_unique)
np.save(MainDirOUT + "/stn_lats.npy", lats_unique)
np.save(MainDirOUT + "/stn_lons.npy", lons_unique)
np.save(MainDirOUT + "/dates.npy", Dates_range)
np.save(MainDirOUT + "/stvl_obs.npy", align_obs)
import os
from os.path import exists
import numpy as np

##################################################################################################################################
# CODE DESCRIPTION
# 08_Compute_CleanSTVL.py cleans the STVL point rainfall observations from possible dodgy values using the gridded rainfall values from the "CPC Global  
# Unified Gauge-Based Analysis of Daily Precipitation" dataset

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# Coeff_Grid2Point_list (list of integer number): list of coefficients used to make comparable CPC's gridded rainfall values with  STVL's point rainfall observations
# Git_repo (string): path of local github repository
# DirIN_STVL (string): relative path for the input directory containing STVL's point rainfall observations
# DirIN_CPC (string): relative path for the input directory containing CPC's gridded rainfall values
# DirOUT (string): relative path for the output directory containing the clean STVL's point rainfall observations

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Coeff_Grid2Point_list = [2,5,10,20,50,100]
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN_STVL = "Data/Processed/06_AlignedOBS_rawSTVL"
DirIN_CPC = "Data/Processed/07_AlignedOBS_gridCPC"
DirOUT = "Data/Processed/08_AlignedOBS_cleanSTVL"
##################################################################################################################################

np.set_printoptions(suppress=True, formatter={'float_kind':'{:0.2f}'.format})

# Setting main input/output directories
MainDirIN_STVL = Git_repo + "/" + DirIN_STVL+ "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF)
MainDirIN_CPC = Git_repo + "/" + DirIN_CPC+ "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF)
MainDirOUT = Git_repo + "/" + DirOUT+ "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF)
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Cleaning STVL observations
print(" ")
print("Cleaning STVL observations")
for Coeff_Grid2Point in Coeff_Grid2Point_list:

      # Setting temporary output directory
      MainDirOUT_temp = MainDirOUT + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
      if not exists(MainDirOUT_temp):
            os.makedirs(MainDirOUT_temp)

      # Reading STVL's point rainfall observations and the correspondent metadata (i.e., ids/lats/lons/dates) over the period of interest 
      print(" ")
      print("Reading STVL's point rainfall observations and the correspondent metadata (i.e., ids/lats/lons/dates) over the period of interest")
      stvl_stnids = np.load(MainDirIN_STVL + "/stn_ids.npy")
      stvl_lats = np.load(MainDirIN_STVL + "/stn_lats.npy")
      stvl_lons = np.load(MainDirIN_STVL + "/stn_lons.npy")
      stvl_dates = np.load(MainDirIN_STVL + "/dates.npy")
      stvl_obs = np.load(MainDirIN_STVL + "/obs.npy")
      NumStns = stvl_obs.shape[0]
      NumDays = stvl_obs.shape[1]

      # Reading CPC's gridded rainfall observations
      print("Reading CPC's gridded rainfall values")
      cpc_obs = np.load(MainDirIN_CPC + "/obs.npy")

      # Automatic corrections using CPC dataset with different coefficients to compare gridded rainfall values with point rainfall observations
      print(" - Automatic corrections using CPC dataset (coefficient to compare gridded rainfall values with point rainfall observations = " + str(Coeff_Grid2Point) + ")")
      stvl_obs_clean = stvl_obs
      cpc_obs_point = cpc_obs * Coeff_Grid2Point
      ind = np.less(cpc_obs_point,stvl_obs)
      stvl_obs_clean[ind] = np.nan

      # Manual corrections of rainfall values that are known to be wrong
      print(" - Manual corrections of rainfall values that are known to be wrong")
      #    - those less than 0 mm
      #     - those equal to 989.0 mm outside the tropics (their major frequency is accepted in the tropics because there is no other way in synop reports to report rainfall totals higher than 1000 mm/6h and such high rainfall totals can be possible in the tropics)
      #     - those in the category between 999.1 and 999.9 because are likely to indicate very small rainfall amounts if the way of reporting synop rainfall < 1mm for 6 hourly was adopted also for the 24-hourly
      #     - those greater than the world record of 1825 mm/24h in La Reunion on 7-8 January 1966 

      print("     - Eliminating negative rainfall values")
      val = 0
      temp = np.where((stvl_obs_clean < val ))
      stvl_obs_clean[temp[0],temp[1]] = np.nan
      
      print("     - Eliminating rainfall values equal to 989.0 mm outside the tropics because it is not likely to observe rainfall > 1000 mm/6h in the extra tropics")
      val = 989.0
      ind_val_stnid = np.where((stvl_obs_clean == val))[0]
      ind_val_date = np.where((stvl_obs_clean == val))[1]
      lats_temp = stvl_lats[ind_val_stnid]
      ind_lat = np.where( (lats_temp > 30.0) | (lats_temp < -30.0) )[0]
      ind_stnids2remove = ind_val_stnid[ind_lat]
      ind_date2remove = ind_val_date[ind_lat]
      stvl_obs_clean[ind_stnids2remove,ind_date2remove] = np.nan

      print("     - Eliminating rainfall values between 999.1 and 999.9 because they are likely to represent instead rainfall totals <= 1 mm/24h")
      val_min = 999.1
      val_max = 999.9
      temp = np.where( (stvl_obs_clean >= val_min ) & (stvl_obs_clean <= val_max) )
      stvl_obs_clean[temp[0],temp[1]] = np.nan

      print("     - Eliminating rainfall values greater than the world record of 1825 mm/24h")
      val = 1825.0
      temp = np.where((stvl_obs_clean > val ))
      stvl_obs_clean[temp[0],temp[1]] = np.nan

      # Saving the cleaned STVL's point rainfall observations
      print(" - Saving cleaned STVL observations")
      np.save(MainDirOUT_temp + "/stn_ids.npy", stvl_stnids)
      np.save(MainDirOUT_temp + "/stn_lats.npy", stvl_lats)
      np.save(MainDirOUT_temp + "/stn_lons.npy", stvl_lons)
      np.save(MainDirOUT_temp + "/dates.npy", stvl_dates)
      np.save(MainDirOUT_temp + "/obs.npy", stvl_obs_clean)
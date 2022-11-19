import os
from os.path import exists
from datetime import datetime
import numpy as np

##########################################################################################################################################################
# CODE DESCRIPTION
# 09_Compute_Climate_OBS.py computes rainfall climatologies from point observations.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# NameOBS_list (list of strings): list of the names of the observations to quality check
# Coeff_Grid2Point_list (list of integer number): list of coefficients used to make comparable CPC's gridded rainfall values with  STVL's point rainfall observations. 
#                                                                                    Used only when running the quality check on the clean STVL observations.
# MinDays_Perc_list (list of number, from 0 to 1): list of percentages for the minimum number of days over the considered period with valid observations to compute the climatologies.
# Perc_year (array of float numbers): percentiles to compute for the year climatology.
# Perc_season (array of float numbers): percentiles to compute for the seasonal climatologies.
# Git_repo (string): path of local github repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
NameOBS_list = ["06_AlignedOBS_rawSTVL", "07_AlignedOBS_gridCPC", "08_AlignedOBS_cleanSTVL"]
Coeff_Grid2Point_list = [2,5,10,20,50,100]
MinDays_Perc_list = [0.5, 0.75]
Perc_year = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95])], axis=0)
Perc_season = np.concatenate([np.arange(0,100), np.array([99.5, 99.8])], axis=0)
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN = "Data/Processed"
DirOUT = "Data/Processed/09_Climate_OBS"
##########################################################################################################################################################


# Costum functions

def compute_climate_obs(MinDays_Perc, Perc_year, Perc_season, DirIN, DirOUT):

      # Reading the rainfall observations over the period of interest and the correspondent metadata (i.e., ids/lats/lons/dates)
      print(" - Reading the rainfall observations over the period of interest and the correspondent metadata (i.e., ids/lats/lons/dates)")
      stnids_unique = np.load(DirIN + "/stn_ids.npy")
      lats_unique = np.load(DirIN + "/stn_lats.npy")
      lons_unique = np.load(DirIN + "/stn_lons.npy")
      dates = np.load(DirIN + "/dates.npy")
      align_obs = np.load(DirIN + "/obs.npy")
      NumStns = align_obs.shape[0]
      NumDays = align_obs.shape[1]

      # Defining the minimum number of days accepted to compute the climatologies and keeping only stations that satisfy that condition
      MinNumDays = round(NumDays * MinDays_Perc)
      NumDays_NotNaN = np.sum(~np.isnan(align_obs), axis=1)
      ind_stns_MinNumDays = np.where(NumDays_NotNaN >= MinNumDays)[0]
      align_obs_MinNumDays = align_obs[ind_stns_MinNumDays,:]
      NumStns_MinNumDays = ind_stns_MinNumDays.shape[0]
      print("     - " + str(NumStns_MinNumDays) + " over " + str(NumStns) + " stations satisfy the threshold of having observations for at least " + str(int(MinDays_Perc*100)) + "% of the days over the considered period.")
      print("     - Saving metadata about the considered stations (stnids/lats/lons)")
      np.save(DirOUT + "/" + "Stn_ids.npy", stnids_unique[ind_stns_MinNumDays])
      np.save(DirOUT + "/" + "Stn_lats.npy", lats_unique[ind_stns_MinNumDays])
      np.save(DirOUT + "/" + "Stn_lons.npy", lons_unique[ind_stns_MinNumDays])

      # Computing and saving the percentiles for the year climatology
      print(" - Computing and saving the year climatology...")
      climate_year = np.transpose(np.nanpercentile(align_obs_MinNumDays, Perc_year, axis=1, interpolation="lower"))
      np.save(DirOUT + "/Percentiles_Year.npy", Perc_year)
      np.save(DirOUT + "/Climate_Year.npy", climate_year)

      # Computing and saving the percentiles for the seasonal climatology - Winter (December/January/February, DJF)
      print(" - Computing and saving the seasonal climatology - Winter (December/January/February, DJF)")
      M1 = 12
      M2 = 1
      M3 = 2
      ind_dates_season = []
      for ind_dates in range(NumDays):
            month = (datetime.strptime(dates[ind_dates], "%Y%m%d")).month
            if (month == M1) or (month == M2) or (month == M3):
                  ind_dates_season.append(ind_dates)
      align_obs_MinNumDays_season = align_obs_MinNumDays[:,ind_dates_season]
      climate_season = np.transpose(np.nanpercentile(align_obs_MinNumDays_season, Perc_season, axis=1, interpolation="lower"))
      np.save(DirOUT + "/Percentiles_Season.npy", Perc_season)
      np.save(DirOUT + "/Climate_DJF.npy", climate_season)

      # Computing and saving the percentiles for the seasonal climatology - Spring (March/April/May, MAM)
      print(" - Computing and saving the seasonal climatology - Spring (March/April/May, MAM)")
      M1 = 3
      M2 = 4
      M3 = 5
      ind_dates_season = []
      for ind_dates in range(NumDays):
            month = (datetime.strptime(dates[ind_dates], "%Y%m%d")).month
            if (month == M1) or (month == M2) or (month == M3):
                  ind_dates_season.append(ind_dates)
      align_obs_MinNumDays_season = align_obs_MinNumDays[:,ind_dates_season]
      climate_season = np.transpose(np.nanpercentile(align_obs_MinNumDays_season, Perc_season, axis=1, interpolation="lower"))
      np.save(DirOUT + "/Climate_MAM.npy", climate_season)

      # Computing and saving the percentiles for the seasonal climatology - Summer (June/July/August, JJA)
      print(" - Computing and saving the seasonal climatology - Summer (June/July/August, JJA)")
      M1 = 6
      M2 = 7
      M3 = 8
      ind_dates_season = []
      for ind_dates in range(NumDays):
            month = (datetime.strptime(dates[ind_dates], "%Y%m%d")).month
            if (month == M1) or (month == M2) or (month == M3):
                  ind_dates_season.append(ind_dates)
      align_obs_MinNumDays_season = align_obs_MinNumDays[:,ind_dates_season]
      climate_season = np.transpose(np.nanpercentile(align_obs_MinNumDays_season, Perc_season, axis=1, interpolation="lower"))
      np.save(DirOUT + "/Climate_JJA.npy", climate_season)

      # Computing and saving the percentiles for the seasonal climatology - Autumn (September/October/November, SON)
      print(" - Computing and saving the seasonal climatology - Autumn (September/October/November, SON)")
      M1 = 9
      M2 = 10
      M3 = 11
      ind_dates_season = []
      for ind_dates in range(NumDays):
            month = (datetime.strptime(dates[ind_dates], "%Y%m%d")).month
            if (month == M1) or (month == M2) or (month == M3):
                  ind_dates_season.append(ind_dates)
      align_obs_MinNumDays_season = align_obs_MinNumDays[:,ind_dates_season]
      climate_season = np.transpose(np.nanpercentile(align_obs_MinNumDays_season, Perc_season, axis=1, interpolation="lower"))
      np.save(DirOUT + "/Climate_SON.npy", climate_season)
###############################################################################################################

# Computing the observational climatologies

for MinDays_Perc in MinDays_Perc_list:

      for NameOBS in NameOBS_list:

            if (NameOBS == "06_AlignedOBS_rawSTVL") or (NameOBS == "07_AlignedOBS_gridCPC"):
                  
                  print(" ")
                  print("Computing the observational climatologies for "+ NameOBS + " with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                  
                  # Setting main input/output directories
                  MainDirIN = Git_repo + "/" + DirIN + "/" + NameOBS + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF) 
                  MainDirOUT = Git_repo + "/" + DirOUT + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF) 
                  if not exists(MainDirOUT):
                        os.makedirs(MainDirOUT)
                  
                  # Computing the observational climatologies
                  compute_climate_obs(MinDays_Perc, Perc_year, Perc_season, MainDirIN, MainDirOUT)

            elif NameOBS == "08_AlignedOBS_cleanSTVL":

                  for Coeff_Grid2Point in Coeff_Grid2Point_list:
                        
                        print(" ")
                        print("Computing the observational climatologies for "+ NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                        
                        # Setting main input/output directories
                        MainDirIN = Git_repo + "/" + DirIN + "/" + NameOBS + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF) + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                        MainDirOUT = Git_repo + "/" + DirOUT + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF) + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                        if not exists(MainDirOUT):
                              os.makedirs(MainDirOUT)

                        # Computing the observational climatologies
                        compute_climate_obs(MinDays_Perc, Perc_year, Perc_season, MainDirIN, MainDirOUT)
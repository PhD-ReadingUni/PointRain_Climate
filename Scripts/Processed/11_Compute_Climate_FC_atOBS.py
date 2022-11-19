import os
from os.path import exists
import numpy as np

######################################################################################################################################################
# CODE DESCRIPTION
# 11_Compute_Climate_FC_atOBS.py computes rainfall climatologies from different forecasting systems, at the location of available point rainfall climatologies over a given period.
# The climatologies are computed in the form of a distribution of percentiles (using the method of linear interpolation), with the highest percentiles computed on the basis of how many realizations are provided by 
# the modelled analysis/forecasts. Separate climatologies are computed for year and seasonal (i.e. DJF, MAM, JJA, SON) climatologies. 

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# SystemFC_list (list of string): list of forecasting systems to consider.
# Climate_OBS_Period (string, in YearS_YearF format): indicates the start/final year the observational climatologies are valid for
# MinDays_Perc_list (list of number, from 0 to 1): list of percentages for the minimum number of days over the considered period with valid observations to compute the climatologies.
# NameOBS_list (list of strings): list of the names of the observations to quality check
# Coeff_Grid2Point_list (list of integer number): list of cosefficients used to make comparable CPC's gridded rainfall values with  STVL's point rainfall observations. Used only when running the quality check on the clean STVL observations.
# Git_repo (string): path of local github repository.
# DirIN_Climate_OBS (string): relative path for the input directory containing the observational climatologies.
# DirIN_FC (string): relative path for the input directory containing the raw analysis/forecasts.
# DirOUT_Climate_FC (string): relative path for the output directory containing the modelled climatologies.

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
SystemFC_list = ["ERA5_ecPoint/Pt_BC_PERC"]
Climate_OBS_Period = "2000_2019"
MinDays_Perc_list = [0.5,0.75]
NameOBS_list = ["06_AlignedOBS_rawSTVL", "07_AlignedOBS_gridCPC", "08_AlignedOBS_cleanSTVL"]
Coeff_Grid2Point_list = [2,5,10,20,50,100]
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN_Climate_OBS = "Data/Processed/09_Climate_OBS"
DirIN_FC = "Data/Processed/10_Rainfall"
DirOUT_Climate_FC = "Data/Processed/11_Climate_FC"
######################################################################################################################################################

# Costum functions

########################################
# Compute and save distribution of percentiles  # 
########################################
def distribution_percentiles(YearS, YearF, PercYear, PercSeason, DirIN_FC, DirOUT_Climate_FC):
      
      Dataset_list = ["Year", "DJF", "MAM", "JJA", "SON"]
      
      for Dataset in Dataset_list:
            
            print(" - Computing percentiles for " + Dataset)
            
            # Reading the indipendent rainfall realizations for the period under consideration
            print("     - Reading the indipendent rainfall realizations for year: " + str(YearS))
            tp = np.load(DirIN_FC + "/tp_" + Dataset + "_" + str(YearS) + ".npy")
            for Year in range (YearS+1,YearF+1):
                        print("     - Reading the indipendent rainfall realizations for year: " + str(Year))
                        tp = np.hstack((tp, np.load(DirIN_FC + "/tp_" + Dataset + "_" + str(Year) + ".npy")))

            # Computing the percentiles for the year/seasonal climatologies
            print("     - Computing the percentiles for the year/seasonal climatologies")
            if Dataset == "Year":
                  Perc = PercYear
            else:
                  Perc = PercSeason
            climate = np.transpose(np.around(np.float32(np.nanpercentile(tp, Perc, axis=1, interpolation="lower").astype(float)), decimals=1))

            # Saving the year/seasonal climatologies and their correspondent metadata
            print("     - Saving the year/seasonal climatologies and their correspondent metadata")
            np.save(DirOUT_Climate_FC + "/Climate_" + Dataset + ".npy", climate)

      # Saving the percentiles computed for the year/seasonal climatologies
      np.save(DirOUT_Climate_FC + "/Percentiles_Year.npy", PercYear)
      np.save(DirOUT_Climate_FC + "/Percentiles_Season.npy", PercSeason)

#############################################################################################################################################


for MinDays_Perc in MinDays_Perc_list:

      for NameOBS in NameOBS_list:

            if (NameOBS == "06_AlignedOBS_rawSTVL") or (NameOBS == "07_AlignedOBS_gridCPC"):

                  for SystemFC in SystemFC_list:
                        
                        print(" ")
                        print("Computing modelled (" + SystemFC + ") climatologies at stations for "+ NameOBS + " with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations")

                        # Definition of the percentiles to compute for different forecasting system
                        if SystemFC == "HRES_46r1":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8])])
                        elif SystemFC == "Reforecasts_46r1":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                        elif SystemFC == "ERA5_ShortRange":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9])])
                        elif SystemFC == "ERA5_EDA_ShortRange":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                        elif SystemFC == "ERA5_LongRange":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                        elif SystemFC == "ERA5_EDA_LongRange":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                        elif SystemFC == "ERA5_ecPoint/Grid_BC_VALS":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9])])
                        elif SystemFC == "ERA5_ecPoint/Pt_BC_PERC":
                              PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998, 99.999, 99.9995, 99.9998])])
                              PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998, 99.999])])

                        # Computing and saving the modelled rainfall climatologies (i.e. the distribution of percentiles computed from the independent rainfall realizations)
                        MainDirIN_FC = Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period
                        MainDirOUT_Climate_FC = Git_repo + "/" + DirOUT_Climate_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period
                        if not exists(MainDirOUT_Climate_FC):
                              os.makedirs(MainDirOUT_Climate_FC)
                        distribution_percentiles(YearS, YearF, PercYear, PercSeason, MainDirIN_FC, MainDirOUT_Climate_FC)

                       # Reading and saving the metadata (i.e. station id/lat/lon) for the considered point observational climatologies
                        MainDirIN_Climate_OBS = Git_repo + "/" + DirIN_Climate_OBS + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period
                        stn_lats = np.load(MainDirIN_Climate_OBS + "/Stn_lats.npy")
                        stn_lons = np.load(MainDirIN_Climate_OBS + "/Stn_lons.npy")
                        stn_ids = np.load(MainDirIN_Climate_OBS + "/Stn_ids.npy")
                        np.save(MainDirOUT_Climate_FC + "/Stn_ids.npy", stn_ids)
                        np.save(MainDirOUT_Climate_FC + "/Stn_lats.npy", stn_lats)
                        np.save(MainDirOUT_Climate_FC + "/Stn_lons.npy", stn_lons)

            elif NameOBS == "08_AlignedOBS_cleanSTVL":

                  for Coeff_Grid2Point in Coeff_Grid2Point_list:
                        
                        for SystemFC in SystemFC_list:
                              
                              print(" ")
                              print("Computing modelled (" + SystemFC + ") climatologies at stations for "+ NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations")

                              # Definition of the percentiles to compute for different forecasting system
                              if SystemFC == "HRES_46r1":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8])])
                              elif SystemFC == "Reforecasts_46r1":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                              elif SystemFC == "ERA5_ShortRange":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9])])
                              elif SystemFC == "ERA5_EDA_ShortRange":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                              elif SystemFC == "ERA5_LongRange":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                              elif SystemFC == "ERA5_EDA_LongRange":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99])])
                              elif SystemFC == "ERA5_ecPoint/Grid_BC_VALS":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9])])
                              elif SystemFC == "ERA5_ecPoint/Pt_BC_PERC":
                                    PercYear = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998, 99.999, 99.9995, 99.9998])])
                                    PercSeason = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995, 99.998, 99.999])])

                              # Computing and saving the modelled rainfall climatologies (i.e. the distribution of percentiles computed from the independent rainfall realizations)
                              MainDirIN_FC = Git_repo + "/" + DirIN_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              MainDirOUT_Climate_FC = Git_repo + "/" + DirOUT_Climate_FC + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              if not exists(MainDirOUT_Climate_FC):
                                    os.makedirs(MainDirOUT_Climate_FC)
                              distribution_percentiles(YearS, YearF, PercYear, PercSeason, MainDirIN_FC, MainDirOUT_Climate_FC)

                              # Reading and saving the metadata (i.e. station id/lat/lon) for the considered point observational climatologies
                              MainDirIN_Climate_OBS = Git_repo + "/" + DirIN_Climate_OBS + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              stn_lats = np.load(MainDirIN_Climate_OBS + "/Stn_lats.npy")
                              stn_lons = np.load(MainDirIN_Climate_OBS + "/Stn_lons.npy")
                              stn_ids = np.load(MainDirIN_Climate_OBS + "/Stn_ids.npy")
                              np.save(MainDirOUT_Climate_FC + "/Stn_ids.npy", stn_ids)
                              np.save(MainDirOUT_Climate_FC + "/Stn_lats.npy", stn_lats)
                              np.save(MainDirOUT_Climate_FC + "/Stn_lons.npy", stn_lons)
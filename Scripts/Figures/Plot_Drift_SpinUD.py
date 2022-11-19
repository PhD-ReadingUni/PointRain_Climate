import os
from datetime import date, timedelta
import numpy as np
import metview as mv
import matplotlib.pyplot as plt

############################################################################################################################################
# CODE DESCRIPTION
# Plot_Drift_SpinUD.py plots the annual average of total precipitation over different lead times to estimate the drift of the forecasts with lead time and their spind-up/down.

# DESCRIPTION OF INPUT PARAMETERS
# Year_list (list of numbers, years in YYYY format): years to consider
# BaseTime_list (list of number, in hours): base times to consider
# StepMin(number, in hours): minimum step to consider
# StepMax(number, in hours): maximum step to consider
# Disc_Step (number, in hours): time discretization for the steps to consider
# Acc (number, in hours): rainfall accumulation period.
# SystemFC_list(list of strings): forecasting systems to consider
# Git_repo (string): path of local github repository
# DirLSM (string): relative path where to find the land-sea mask for the correspondent forecasting system
# DirIN (string): relative path for the input directory
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
Year_list = [1999,2009,2019]
BaseTime_list= [0,12]
StepMin = 0
StepMax = 120
Disc_Step = 6
Acc = 24
SystemFC_list = ["ERA5_EDA_LongRange", "ERA5_LongRange"]
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirLSM = "Data/Raw/LSM"
DirIN="Data/Raw/FC"
DirOUT="Data/Figures/Drift_SpinUD/SingleRuns"
############################################################################################################################################


# Setting step parameters
StepS = StepMin
StepF = StepMax - Acc

for SystemFC in SystemFC_list:

      # Reading the land-sea mask for the considered forecasting system
      # and extracting the sea/land grid points
      FileLSM = Git_repo + "/" + DirLSM + "/lsm_" + SystemFC + ".grib"
      lsm = mv.values(mv.read(FileLSM))
      sea = (lsm == 0) * 1
      land = (lsm > 0) * 1

      # Selecting the grid points belonging to extra-tropics (et) and tropics (t) latitudes
      lats = mv.latitudes(mv.read(FileLSM))
      et = ((lats > 20.0) | (lats < -20.0)) * 1
      t  = ((lats < 20.0) & (lats > -20.0)) * 1

      # Computing the annual average for rainfall
      for Year in Year_list:

            # Setting dates in the considered year
            BaseDateS = date(Year,1,1)
            BaseDateF = date(Year,12,31)
            NumDaysYear = (BaseDateF - BaseDateS).days + 1

            # Setting the input directory for the raw rainfall forecasts
            DirIN_year = Git_repo + "/" + DirIN + "/" + SystemFC + "/" + str(Year)

            # Considering different base times
            for BaseTime in BaseTime_list:
                        
                  BaseTimeSTR = format(BaseTime, '02d')

                  tp_year_mean_sea_et = np.empty((0))
                  tp_year_mean_sea_t = np.empty((0))
                  tp_year_mean_land_et = np.empty((0))
                  tp_year_mean_land_t = np.empty((0))
                  steps = np.empty((0), int)
                  
                  # Considering different starting steps to assess spin-up/spin-down issues in the forecasts
                  for Step1 in range(StepS, StepF+1, Disc_Step):

                        print("SystemFC:", SystemFC, ", Year:", Year, ", BaseTime:", BaseTime, ", Step1:", Step1)

                        Step2 = Step1 + Acc              
                        StepSTR1 = format(Step1, '03d')
                        StepSTR2 = format(Step2, '03d')
                        steps = np.append(steps, Step2)

                        # Computing the rainfall's annual averages
                        BaseDate = BaseDateS
                        tp_day_mean_sea_et = 0
                        tp_day_mean_sea_t = 0
                        tp_day_mean_land_et = 0
                        tp_day_mean_land_t = 0
                        
                        while BaseDate <= BaseDateF:

                              BaseDateSTR = BaseDate.strftime("%Y%m%d")
                              
                              DirIN_temp = DirIN_year + "/" + BaseDateSTR + BaseTimeSTR
                              FileIN_1 = DirIN_temp + "/tp_" + BaseDateSTR + "_" + BaseTimeSTR + "_" + StepSTR1 + ".grib"
                              FileIN_2 = DirIN_temp + "/tp_" + BaseDateSTR + "_" + BaseTimeSTR + "_" + StepSTR2 + ".grib"
                                    
                              tp1 = mv.read(FileIN_1)
                              tp2 = mv.read(FileIN_2)
                              tp_day = mv.values((tp2 - tp1) * 1000)
                              
                              tp_day_sea_et = tp_day[ (sea == 1) & (et == 1) ] #selecting sea grid-proints in the extra-tropics
                              tp_day_sea_t = tp_day[ (sea == 1) & (t == 1) ] #selecting sea grid-proints in the tropics
                              tp_day_land_et = tp_day[ (land == 1) & (et == 1) ] #selecting land grid-proints in the extra-tropics
                              tp_day_land_t = tp_day[ (land == 1) & (t == 1) ] #selecting land grid-proints in the tropics
                              
                              tp_day_mean_sea_et = tp_day_mean_sea_et + np.mean(tp_day_sea_et)
                              tp_day_mean_sea_t = tp_day_mean_sea_t + np.mean(tp_day_sea_t)
                              tp_day_mean_land_et = tp_day_mean_land_et + np.mean(tp_day_land_et)
                              tp_day_mean_land_t = tp_day_mean_land_t + np.mean(tp_day_land_t)
                              
                              BaseDate += timedelta(days=1)

                        tp_year_mean_sea_et = np.append(tp_year_mean_sea_et, tp_day_mean_sea_et / NumDaysYear)
                        tp_year_mean_sea_t = np.append(tp_year_mean_sea_t, tp_day_mean_sea_t / NumDaysYear)
                        tp_year_mean_land_et = np.append(tp_year_mean_land_et, tp_day_mean_land_et / NumDaysYear)
                        tp_year_mean_land_t = np.append(tp_year_mean_land_t, tp_day_mean_land_t / NumDaysYear)

                  Ytick_lower = round(min([np.amin(tp_year_mean_sea_et), np.amin(tp_year_mean_sea_t), np.amin(tp_year_mean_land_et), np.amin(tp_year_mean_land_t)]),1)
                  Ytick_upper = round(max([np.amax(tp_year_mean_sea_et), np.amax(tp_year_mean_sea_t), np.amax(tp_year_mean_land_et), np.amax(tp_year_mean_land_t)]),1)

                  plt.figure(figsize=(15,10))
                  plt.plot(steps, tp_year_mean_sea_et, color ="blue", linewidth=2)
                  plt.plot(steps, tp_year_mean_sea_t, color ="blue", linestyle='dashed', linewidth=2)
                  plt.plot(steps, tp_year_mean_land_et, color ="red", linewidth=2)
                  plt.plot(steps, tp_year_mean_land_t, color ="red", linestyle='dashed', linewidth=2)
                  plt.title(SystemFC + " (Long-Range), " + str(Year) + ", " + BaseTimeSTR + "Z")
                  plt.xlabel("Steps at the end of the " + str(Acc) + "-hourly accumulation period")
                  plt.ylabel(str(Acc) + "-hourly rainfall, annual average [mm]")
                  plt.legend(["Sea, extra-tropics", "Sea, tropics","Land, extra-tropics","Land, tropics"], loc="upper left")
                  plt.xlim([0, Step2])
                  plt.xticks(steps, steps)
                  plt.yticks(np.arange(Ytick_lower, Ytick_upper+0.1, 0.1))
                  plt.grid(True)
                  
                  # Saving the plot
                  DirOUT_temp = Git_repo + "/" + DirOUT + "_" + str(Acc) + "h/" 
                  if not os.path.exists(DirOUT_temp):
                        os.makedirs(DirOUT_temp)
                  FileNameOUT_temp = SystemFC + "_" + str(Year) + "_" + BaseTimeSTR + "Z.png"
                  plt.savefig(DirOUT_temp + "/" + FileNameOUT_temp)
                  plt.close()
import os
from os.path import exists
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import metview as mv

#########################################################################################################################################
# CODE DESCRIPTION
# Plot_TempDistr_OBS.py plots the temporal distribution of the average number of rainfall observations per day, in a given year, in each considered rainfall dataset in stvl.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (number, in hours): rainfall accumulation period.
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Disc_time (number, in hours): discretization to determine the times to consider.
# Dataset_list (list of strings): name of the considered datasets.
# Git_repo (string): path of local github repository
# DirIN (string): relative path for the input directory
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
Acc = 24
YearS = 2000
YearF = 2020
Disc_time = 1
Dataset_list = ["synop", "hdobs", "bom", "india", "efas", "vnm", "ukceda"]
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN = "Data/Processed/01_UniqueOBS_24h_synop_00UTC"
DirOUT = "Data/Figures/TempDistr_OBS"
#########################################################################################################################################

# Setting general parameters
Year_list = range(YearS,YearF+1)
YearSTR_list = [str(Year) for Year in Year_list]
indYear = range(0,len(Year_list))

# Setting main output directory
MainDirOUT = Git_repo + "/" + DirOUT
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Plot the distribution of number of rainfall observation per day/dataset in a given year
for Dataset in Dataset_list:
      
      print("Considering:", Dataset)

      # Setting main input directory
      MainDirIN = Git_repo + "/" + DirIN + "/" + Dataset
      
      # Considering different years
      av_count_obs = [] 
      for Year in Year_list:

            print(" - ", Year)
            DateTime1 = datetime(Year, 1, 2, 0, 0)
            DateTime2 = datetime( (Year+1) , 1, 1, 0, 0)
            NumDays_Year = (DateTime2 - DateTime1).days

            count_obs = 0
            TheDateTime = DateTime1
            while TheDateTime <= DateTime2:
      
                  TheDateSTR = TheDateTime.strftime("%Y%m%d")
                  TheTimeSTR = TheDateTime.strftime("%H")

                  # Reading the rainfall observations and counting how many observation are in each single day, in a given year
                  FileIN_temp = MainDirIN + "/" + TheDateSTR + "/tp" + str(Acc) + "_obs_" + TheDateSTR + TheTimeSTR + ".geo"
                  if exists(FileIN_temp):
                        geo = mv.read(FileIN_temp)
                        count_obs = count_obs + mv.count(geo)

                  TheDateTime += timedelta(hours=1)

            # Computing average number of rainfall observations per day in a given year
            av_count_obs.append(round(count_obs / NumDays_Year))
      
      # Plotting
      plt.bar(Year_list, av_count_obs, color = "b", width = 0.2, label=Dataset)
      plt.xticks(Year_list, YearSTR_list, rotation = 30)
      plt.ylim([0, 8000])
      plt.ylabel("Year")
      plt.ylabel("N. of observations")
      plt.title("Average number of " + str(Acc) + "-hourly rainfall observations per day, in given years")

      # Saving the plots
      FileOUT = MainDirOUT + "/" + Dataset + ".png"
      plt.savefig(FileOUT)
      plt.close()
import sys
import os
from os.path import exists
from datetime import datetime, timedelta
import numpy as np
import metview as mv

################################################################################################################
# CODE DESCRIPTION
# Compute_Climatology_ERA5.py computes a rainfall climatology in the form of a distribution of percentiles from ERA5. 
# Annual and seasonal (i.e. for Summer, Autumn, Winter, and Spring) climatologies are computed.

# INPUT PARAMETERS
BaseDateTimeS = datetime(2000,1,1,0)
BaseDateTimeF = datetime(2019,12,31,0)
StepS = 0
StepF = 240
Acc = 24
PercYear_array = np.concatenate([np.arange(0,100), np.array([99.5, 99.8, 99.9, 99.95, 99.98, 99.99, 99.995])])
PercSeason_array = np.concatenate([np.arange(0,100), np.array([99.5, 99.8])])
System_FC = "ERA5_EDA_LongRange"
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN = "Data/Raw/FC"
DirOUT = "Data/Processed/Climate"
#################################################################################################################

# Setting main input/output directory
MainDirIN = Git_repo + "/" + DirIN + "/" + System_FC
MainDirOUT = Git_repo + "/" + DirOUT
if not exists(MainDirOUT):
      os.makedirs(MainDirOUT)

# Setting the number of grid boxes in each forecasting system, and the number of sub-areas in which to split the climatology computations 
if System_FC == "ERA5_EDA_LongRange":
      NumGB_G = 138346
      NumSA = 34
elif System_FC == "ERA5_LongRange":
      NumGB_G = 542080
      NumSA = 160
NumGB_SA = int(NumGB_G/NumSA)

# Setting the number of realizations for the considered period
NumR = int( ( ( BaseDateTimeF - BaseDateTimeS ).days + 1 ) * ( (StepF - StepS) / Acc) )


###############################################
# Computing the annual rainfall climatologies for each sub-area #
###############################################

for ind_SA in range(1,NumSA+1):
      
      print(" ")
      print("Considering sub-area n. " + str(ind_SA) + " over a total of " + str(NumSA))

      # Initializing the variable that will store all the rainfall realizations over the considered period
      tp = np.empty((NumR, NumGB_SA-1,)) 

      # Indexing the considered sub_area
      SA_end = (NumGB_SA * ind_SA) - 1
      SA_start = SA_end - (NumGB_SA - 1)

      # Computing the rainfall realizations over the considered period
      indR = 0
      BaseDateTime = BaseDateTimeS
      while BaseDateTime <= BaseDateTimeF:
            
            BaseDateTimeSTR  = BaseDateTime.strftime("%Y%m%d%H")
            BaseDateSTR  = BaseDateTime.strftime("%Y%m%d")
            BaseTimeSTR  = BaseDateTime.strftime("%H")
            YearSTR = BaseDateTime.strftime("%Y")
            
            print(" ")
            print(" - " + BaseDateSTR)

            for Step1 in range (StepS, StepF - Acc + 1, Acc):

                  Step2 = Step1 + Acc
                  Step1STR = f"{Step1:03d}"
                  Step2STR = f"{Step2:03d}"

                  FileIN1 = MainDirIN + "/" + YearSTR + "/" + BaseDateTimeSTR + "/tp_" + BaseDateSTR + "_" + BaseTimeSTR + "_" + Step1STR + ".grib"
                  FileIN2 = MainDirIN + "/" + YearSTR + "/" + BaseDateTimeSTR + "/tp_" + BaseDateSTR + "_" + BaseTimeSTR + "_" + Step2STR + ".grib"
                  tp[indR,:] = np.around(mv.values((mv.read(FileIN2) - mv.read(FileIN1)) * 1000), decimals=2)[SA_start:SA_end]
                  
                  indR += 1

            BaseDateTime += timedelta(days=1)

import sys
import os
from os.path import exists
from datetime import datetime, timedelta
import numpy as np
import metview as mv

##########################################################################
# CODE DESCRIPTION
# Compute_Chunk_FC.py chunks globals field forecasts in a given number of sub-areas.  
# Each sub-area is then stored in separate numpy array in order to be processed separately.

# INPUT PARAMETERS
Year = int(sys.argv[1])
StepS = 0
StepF = 240
Acc = 24
System_FC = "ERA5_LongRange"
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN = "Data/Raw/FC"
DirOUT = "Data/Processed/FC_SA"
##########################################################################

# Setting the number of grid boxes in each forecasting system, and the number of sub-areas in which to split the climatology computations 
if System_FC == "ERA5_EDA_LongRange":
      NumGB_G = 138346
      NumSA = 34
elif System_FC == "ERA5_LongRange":
      NumGB_G = 542080
      NumSA = 160
NumGB_SA = int(NumGB_G/NumSA)

# Computing the rainfall realizations for global fields, and chunking and saving the global fields in sub-areas
BaseDateTimeS = datetime(Year,1,1,0)
BaseDateTimeF = datetime(Year,12,31,0)
BaseDateTime = BaseDateTimeS
while BaseDateTime <= BaseDateTimeF:
      
      BaseDateTimeSTR  = BaseDateTime.strftime("%Y%m%d%H")
      BaseDateSTR  = BaseDateTime.strftime("%Y%m%d")
      BaseTimeSTR  = BaseDateTime.strftime("%H")
      YearSTR = BaseDateTime.strftime("%Y")
      
      print(" ")
      print("Processing date: " + BaseDateSTR)

      for Step1 in range (StepS, StepF - Acc + 1, Acc):

            Step2 = Step1 + Acc
            Step1STR = f"{Step1:03d}"
            Step2STR = f"{Step2:03d}"

            # Computing the rainfall realizations for global fields
            print(" - Computing the rainfall realizations for the global field for (t+" + str(Step1) + ",t+" + str(Step2) + ") ...")
            MainDirIN = Git_repo + "/" + DirIN + "/" + System_FC  + "/" + YearSTR + "/" + BaseDateTimeSTR
            FileIN1 = MainDirIN + "/tp_" + BaseDateSTR + "_" + BaseTimeSTR + "_" + Step1STR + ".grib"
            FileIN2 = MainDirIN + "/tp_" + BaseDateSTR + "_" + BaseTimeSTR + "_" + Step2STR + ".grib"
            tp_G = np.around(mv.values((mv.read(FileIN2) - mv.read(FileIN1)) * 1000), decimals=2)

            # Chunking the global fields in sub-areas
            for ind_SA in range(1,NumSA+1):
      
                  print("   - Chunking and saving sub-area n. " + str(ind_SA) + " over a total of " + str(NumSA))
                  indSA_STR = f"{ind_SA:03d}"
                  SA_end = (NumGB_SA * ind_SA) - 1
                  SA_start = SA_end - (NumGB_SA - 1)
                  tp_SA = tp_G[SA_start:SA_end]
                  
                  # Saving the sub-areas
                  MainDirOUT = Git_repo + "/" + DirOUT + "/" + System_FC + "/" + YearSTR + "/" + BaseDateTimeSTR + "/SA" + indSA_STR
                  if not exists(MainDirOUT):
                        os.makedirs(MainDirOUT)
                  FileOUT = MainDirOUT + "/tp" + str(Acc) + "h_SA" + indSA_STR + "_" + BaseDateSTR + "_" + BaseTimeSTR + "_" + Step2STR  + ".npy"
                  np.save(FileOUT, tp_SA)

      BaseDateTime += timedelta(days=1)
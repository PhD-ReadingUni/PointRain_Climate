import numpy as np

#####################################################################################################
# CODE DESCRIPTION
# 04_Compute_CombineYears_UniqueStnids.py combines the unique stnids for each year over a considered period of time.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# Git_repo (string): path of local github repository
# Dir (string): relative path for the input/output directory

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN = "Data/Processed/03_UniqueStnids_Year"
DirOUT = "Data/Processed/04_UniqueStnids"
#####################################################################################################

# Setting main input/output directory
MainDirIN = Git_repo + "/" + DirIN
MainDirOUT = Git_repo + "/" + DirOUT  + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF)

# Defining the unique stnids for the considered period of time
stnids_all = np.array([])
lats_all = np.array([])
lons_all = np.array([])
for Year in range(YearS,YearF+1):
      stnids_all = np.append(stnids_all, np.load(MainDirIN +  "/stnids_unique_" + str(Year) + ".npy"))
      lats_all = np.append(lats_all, np.load(MainDirIN +  "/lats_unique_" + str(Year) + ".npy"))
      lons_all = np.append(lons_all, np.load(MainDirIN +  "/lons_unique_" + str(Year) + ".npy"))
stnids_unique, ind_stnids_unique = np.unique(stnids_all, return_index=True)
lats_unique = lats_all[ind_stnids_unique]
lons_unique = lons_all[ind_stnids_unique]
print(str(len(stnids_unique)) + " unique stnids found for the period between " + str(YearS) + " and " + str(YearF))

# Saving the unique stnids for the period considered
np.save(MainDirOUT +  "/stnids_unique.npy", stnids_unique)
np.save(MainDirOUT +  "/lats_unique.npy", lats_unique)
np.save(MainDirOUT +  "/lons_unique.npy", lons_unique)
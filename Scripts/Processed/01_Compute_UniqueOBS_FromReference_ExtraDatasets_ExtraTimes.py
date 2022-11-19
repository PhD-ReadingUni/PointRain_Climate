import os
from os.path import exists
from datetime import datetime, timedelta
import numpy as np
import metview as mv

######################################################################################################################
# CODE DESCRIPTION
# 01_Compute_UniqueOBS_FromReference_ExtraDatasets_ExtraTimes.py determines, over different times and datasets, which stations are not 
# present in the reference station (typically synop at 00 UTC, but it could be assigned differently). This is done to maximize the geographical 
# coverage of considered rainfall observations, without double counting overlapping rainfall observations at different reporting times and in 
# different datasets.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (number, in hours): rainfall accumulation period.
# DateTimeS (date, in YYYYMMDDHHMM format): start date/time to retrieve. The time values correspond to the considered reference time.
# DateTimeF (date, in YYYYMMDDHHMM format): final date/time to retrieve. The time values correspond to the considered reference time.
# Disc_time (number, in hours): discretization to determine the extra times to consider compared to the reference time.
# Dataset_ref (string): name of the reference dataset.
# Dataset_extra_list (list of strings): names of the considered extra datasets compared to the reference dataset.
# Git_repo (string): path of local github repository
# DirIN (string): relative path for the input directory
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
Acc = 24
DateTimeS = datetime(2000,1,1,0,0)
DateTimeF = datetime(2020,1,1,0,0)
Disc_time = 1
Dataset_ref = "synop"
Dataset_extra_list = ["hdobs", "bom", "india", "efas", "vnm", "ukceda"]
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN = "Data/Raw/OBS"
DirOUT = "Data/Processed/01_UniqueOBS"
######################################################################################################################

# Adding the reference dataset to the list of the considered extra datasets
Dataset_extra_list.insert(0, Dataset_ref)

# Setting main input/output directory
MainDirIN = Git_repo + "/" + DirIN
MainDirOUT = Git_repo + "/" + DirOUT + "_" + str(Acc) + "h_" + Dataset_ref + "_" + DateTimeS.strftime("%H") + "UTC"

# Adding unique stations over extra times and datasets respect to the reference date/time and dataset
TheDateTime_ref = DateTimeS
while TheDateTime_ref <= DateTimeF:
      
      # Reading the observations for the reference date/time and dataset
      TheDateSTR_ref = TheDateTime_ref.strftime("%Y%m%d")
      TheTimeSTR_ref = TheDateTime_ref.strftime("%H")
      FileIN_ref_temp = MainDirIN + "/" + Dataset_ref + "/" + TheDateSTR_ref + "/tp" + str(Acc) + "_obs_" + TheDateSTR_ref + TheTimeSTR_ref + ".geo"
      if exists(FileIN_ref_temp):
            print("Considering reference date/time:", TheDateTime_ref)
            geo_ref = mv.read(FileIN_ref_temp)
            geo_ref = mv.remove_missing_values(geo_ref)
            stnids_ref = mv.stnids(geo_ref) # list
            lats_ref = mv.latitudes(geo_ref) # array
            lons_ref = mv.longitudes(geo_ref) # array
            elevation_ref = mv.levels(geo_ref) # array
            date_ref = mv.dates(geo_ref) # list
            time_ref = mv.times(geo_ref) # array
            vals_ref = mv.values(geo_ref) # array
            
            # Saving the observations for the reference date/time and dataset
            MainDirOUT_ref_temp = MainDirOUT + "/" + Dataset_ref + "/" + TheDateSTR_ref
            if not exists(MainDirOUT_ref_temp):
                  os.makedirs(MainDirOUT_ref_temp)
            FileOUT_ref_temp = MainDirOUT_ref_temp + "/tp" + str(Acc) + "_obs_" + TheDateSTR_ref + TheTimeSTR_ref + ".geo"
            geo_ref = mv.create_geo( # To match the format in which the extra geopoints are going to be saved
                                    type = 'ncols',
                                    latitudes = lats_ref,
                                    longitudes = lons_ref,
                                    stnids = stnids_ref,
                                    levels = elevation_ref,
                                    dates = date_ref,
                                    times = time_ref, 
                                    values = vals_ref,
                                    )
            mv.write(FileOUT_ref_temp, geo_ref)
            
            # Creating geopoint files containing unique stations over extra datasets respect to the reference dataset
            for Dataset in Dataset_extra_list:
                  
                  # Defining the starting extra times to consider
                  if Dataset == Dataset_ref:
                        ExtraTimeS = TheDateTime_ref.hour + Disc_time
                  else:
                        ExtraTimeS = TheDateTime_ref.hour

                  # Creating geopoint files containing unique stations over extra times respect to the reference date/time
                  for hours_extra in range(ExtraTimeS, 24, Disc_time):
                        
                        # Reading the observations for the extra stations
                        TheDateTime_extra = TheDateTime_ref + timedelta(hours=hours_extra)
                        TheDateSTR_extra = TheDateTime_extra.strftime("%Y%m%d")
                        TheTimeSTR_extra = TheDateTime_extra.strftime("%H")
                        FileIN_extra_temp = MainDirIN + "/" + Dataset + "/" + TheDateSTR_extra + "/tp" + str(Acc) + "_obs_" + TheDateSTR_extra + TheTimeSTR_extra + ".geo"
                        if exists(FileIN_extra_temp):
                              geo_extra = mv.read(FileIN_extra_temp)
                              geo_extra = mv.remove_missing_values(geo_extra)
                              stnids_extra = mv.stnids(geo_extra)
                              lats_extra = mv.latitudes(geo_extra)
                              lons_extra = mv.longitudes(geo_extra)
                              elevation_extra = mv.levels(geo_extra)
                              date_extra = mv.dates(geo_extra)
                              time_extra = mv.times(geo_extra)
                              vals_extra = mv.values(geo_extra)

                              # Defining the ids in stnids_extra that are not included in stnids_ref
                              stnids_unique = list(np.setdiff1d(stnids_extra,stnids_ref))
                              if len(stnids_unique) != 0:
                                    
                                    # Extracting different values for the unique stations
                                    lats_unique = np.array([])
                                    lons_unique = np.array([])
                                    elevation_unique = np.array([])
                                    date_unique = []
                                    time_unique = np.array([])
                                    vals_unique = np.array([])
                                    for item in stnids_unique:
                                          ind = stnids_extra.index(item)
                                          lats_unique = np.append(lats_unique, lats_extra[ind])
                                          lons_unique = np.append(lons_unique, lons_extra[ind])
                                          elevation_unique = np.append(elevation_unique, elevation_extra[ind])
                                          date_unique.append(date_extra[ind])
                                          time_unique = np.append(time_unique, time_extra[ind])
                                          vals_unique = np.append(vals_unique, vals_extra[ind])
                                    
                                    # Creating the geopoint file containing only the unique stations 
                                    geo_unique = mv.create_geo(
                                          type = 'ncols',
                                          latitudes = lats_unique,
                                          longitudes = lons_unique,
                                          stnids = stnids_unique,
                                          levels = elevation_unique,
                                          dates = date_unique,
                                          times = time_unique, 
                                          values = vals_unique,
                                          )
                                    
                                    # Saving the geopoint file containing only the unique stations 
                                    MainDirOUT_extra_temp = MainDirOUT + "/" + Dataset + "/" + TheDateSTR_extra
                                    if not exists(MainDirOUT_extra_temp):
                                          os.makedirs(MainDirOUT_extra_temp)
                                    FileOUT_extra_temp = MainDirOUT_extra_temp + "/tp" + str(Acc) + "_obs_" + TheDateSTR_extra + TheTimeSTR_extra + ".geo"
                                    mv.write(FileOUT_extra_temp, geo_unique)

                                    # Adding the ids of the unique stations to the ids of the reference stations
                                    stnids_ref.extend(stnids_unique)

      TheDateTime_ref += timedelta(days=1)
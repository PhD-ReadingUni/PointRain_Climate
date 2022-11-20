import os
from os.path import exists
from datetime import datetime
import numpy as np
import metview as mv

############################################################################################################################################################
# CODE DESCRIPTION
# Plot_MaxRainOBS.py plots the maximum rainfall value observed at each station.
# The script generates the map plots as static svg figures or in a Metview interactive window.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number, in YYYY format): start year to consider.
# YearF (number, in YYYY format): final year to consider.
# Acc (number, in hours): rainfall accumulation period.
# RunType (string): type of run. Valid values are:
#                                   - "Interactive": to open the plot on an interacive Metview window.
#                                   - "Static": to save the plot on a static svg map.
# MinDays_Perc_list (list of number, from 0 to 1): list of percentages for the minimum number of days over the considered period with valid observations to compute the climatologies.
# NameOBS_list (list of strings): list of the names of the observations to quality check
# Coeff_Grid2Point_list (list of integer number): list of coefficients used to make CPC's gridded rainfall values comparable with  STVL's point rainfall observations. Used only when running the quality check on the clean STVL observations.
# ClimateType_list (list of strings): types of climatology to plot. Valid values are:
#                                                               - "Year": for the year climatology
#                                                               - "DJF": for the seasonal climatology, winter months (December, January, February)
#                                                               - "MAM": for the seasonal climatology, spring months (March, April, May)
#                                                               - "JJA": for the seasonal climatology, summer months (June, July, August)
#                                                               - "SON": for the seasonal climatology, autumn months (September, October, November)
# Git_repo (string): path of local github repository.
# DirIN (string): relative path for the input directory.
# DirOUT (string): relative path for the output directory .

# INPUT PARAMETERS
YearS = 2000
YearF = 2019
Acc = 24
RunType = "Static"
NameOBS_list = ["06_AlignedOBS_rawSTVL", "07_AlignedOBS_gridCPC", "08_AlignedOBS_cleanSTVL"]
Coeff_Grid2Point_list = [2,5,10,20,50,100]
MinDays_Perc_list = [0.5,0.75]
ClimateType_list = ["Year", "DJF", "MAM", "JJA", "SON"]
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN = "Data/Processed"
DirOUT = "Data/Figures/MaxRainOBS"

# RunType = "Static"
# NameOBS_list = ["06_AlignedOBS_rawSTVL", "07_AlignedOBS_gridCPC", "08_AlignedOBS_cleanSTVL"]
# Coeff_Grid2Point_list = [2,5,10,20,50,100]
# MinDays_Perc_list = [0.5,0.75]
# ClimateType_list = ["Year", "DJF", "MAM", "JJA", "SON"]

# RunType = "Interactive"
# NameOBS_list = ["08_AlignedOBS_cleanSTVL"]
# Coeff_Grid2Point_list = [20]
# MinDays_Perc_list = [0.5]
# ClimateType_list = ["SON"]
############################################################################################################################################################

# Costum functions

def plot_MaxRainOBS(obs, lats, lons, dates, ClimateType, MinDays_Perc, Title_text_line_1, Title_text_line_2, DirOUT):

      # Selecting the year or the seasonal subset with the observational dataset
      if ClimateType == "Year":
            obs_temp = obs
      else:
            if ClimateType == "DJF":
                  M1 = 12; M2 = 1; M3 = 2
            if ClimateType == "MAM":
                  M1 = 3; M2 = 4; M3 = 5
            if ClimateType == "JJA":
                  M1 = 6; M2 = 7; M3 = 8
            if ClimateType == "SON":
                  M1 = 9; M2 = 10; M3 = 11
            ind_dates_season = []
            for ind_dates in range(obs.shape[1]):
                  month = (datetime.strptime(dates[ind_dates], "%Y%m%d")).month
                  if (month == M1) or (month == M2) or (month == M3):
                        ind_dates_season.append(ind_dates)
            obs_temp = obs[:,ind_dates_season]

      # Selecting the stations with the considered minimum number of days with valid observations
      MinNumDays = round(obs_temp.shape[1] * MinDays_Perc)
      NumDays_NotNaN = np.sum(~np.isnan(obs_temp), axis=1)
      ind_stns_MinNumDays = np.where(NumDays_NotNaN >= MinNumDays)[0]
      obs_temp_MinNumDays = obs_temp[ind_stns_MinNumDays,:]
      lats_MinNumDays = lats[ind_stns_MinNumDays]
      lons_MinNumDays = lons[ind_stns_MinNumDays]
      
      # Selecting the maximum rainfall values observed at each station
      max_obs = np.nanmax(obs_temp_MinNumDays, axis=1)
      
      # Converting the maximum rainfall values to geopoint
      max_obs_geo = mv.create_geo(
            type = 'xyv',
            latitudes =  lats_MinNumDays,
            longitudes = lons_MinNumDays,
            values = max_obs
            )

      # Plotting the maximum rainfall values
      coastlines = mv.mcoast(
            map_coastline_thickness = 2,
            map_coastline_resolution = "medium",
            map_boundaries = "on",
            map_boundaries_colour = "black",
            map_boundaries_thickness = 1,
            map_grid = "off",
            map_label = "off"
            )

      markers = mv.psymb(
            symbol_type = "MARKER",
            symbol_table_mode = "ON",
            legend = "ON",
            symbol_quality = "HIGH",
            symbol_min_table = [0,0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500],
            symbol_max_table = [0.5,2,5,10,20,30,40,50,60,80,100,125,150,200,300,500,10000],
            symbol_marker_table = [15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15],
            symbol_colour_table = ["black","RGB(0.75,0.95,0.93)","RGB(0.45,0.93,0.78)","RGB(0.07,0.85,0.61)","RGB(0.53,0.8,0.13)","RGB(0.6,0.91,0.057)","RGB(0.9,1,0.4)","RGB(0.89,0.89,0.066)","RGB(1,0.73,0.0039)","RGB(1,0.49,0.0039)","red","RGB(0.85,0.0039,1)","RGB(0.63,0.0073,0.92)","RGB(0.37,0.29,0.91)","RGB(0.04,0.04,0.84)","RGB(0.042,0.042,0.43)","RGB(0.45,0.45,0.45)"],
            symbol_height_table = [0.2,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.3]
            )

      legend = mv.mlegend(
            legend_text_font = "arial",
            legend_text_font_size = 0.30
            )
    
      title = mv.mtext(
            text_line_count = 3,
            text_line_1 = Title_text_line_1,
            text_line_2 =  Title_text_line_2,
            text_line_3 = " ",
            text_colou ="purplish_blue",
            text_font ="courier",
            text_font_size = 0.4
            )

      # Create plots
      if RunType == "Interactive":
            mv.plot(max_obs_geo, coastlines, markers, legend, title)
      else:
            svg = mv.png_output(output_name = DirOUT + "/" + ClimateType + "_MinDaysPerc" + str(int(MinDays_Perc*100)) )
            mv.setoutput(svg)
            mv.plot(max_obs_geo, coastlines, markers, legend, title)
#######################################################################################################################

for NameOBS in NameOBS_list:

      if (NameOBS == "06_AlignedOBS_rawSTVL") or (NameOBS == "07_AlignedOBS_gridCPC"):

            print(" ")
            print("Plotting the maximum rainfall value observed for "+ NameOBS + " at each station")
                        
            # Setting main input/output directories
            MainDirIN = Git_repo + "/" + DirIN + "/" + NameOBS + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF)
            MainDirOUT = Git_repo + "/" + DirOUT + "/ " + NameOBS + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF) 
            if not exists(MainDirOUT):
                  os.makedirs(MainDirOUT)

            # Reading rainfall observations and their metadata (i.e. lats/lons/dates)
            lats = np.load(MainDirIN + "/stn_lats.npy")
            lons = np.load(MainDirIN + "/stn_lons.npy")
            dates = np.load(MainDirIN + "/dates.npy")
            align_obs = np.load(MainDirIN + "/obs.npy")
            NumStns = align_obs.shape[0]
            NumDays = align_obs.shape[1]

            # Plotting maximum observed rainfall values
            for ClimateType in ClimateType_list:
                  
                  for MinDays_Perc in MinDays_Perc_list:
                        
                        print(" - " + ClimateType + " with a minum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" )

                        # Select the year/seasonal subset with the minimum number of 
                        Title_text_line_1 = "Maximum " + str(Acc) + "-hourly rainfall (mm) observed at each station between " + str(YearS) + " and " + str(YearF)
                        Title_text_line_2 = ClimateType + " observations in " + NameOBS.split("_")[-1] + " - Minimum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" 
                        plot_MaxRainOBS(align_obs, lats, lons, dates, ClimateType, MinDays_Perc, Title_text_line_1, Title_text_line_2, MainDirOUT)

      elif NameOBS == "08_AlignedOBS_cleanSTVL":

            for Coeff_Grid2Point in Coeff_Grid2Point_list:
                              
                  print(" ")
                  print("Plotting the maximum rainfall value observed for "+ NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") at each station")
                              
                  # Setting main input/output directories
                  MainDirIN = Git_repo + "/" + DirIN + "/" + NameOBS + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF) + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                  MainDirOUT = Git_repo + "/" + DirOUT + "/ " + NameOBS + "_" + str(Acc) + "h_" + str(YearS) + "_" + str(YearF) + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                  if not exists(MainDirOUT):
                        os.makedirs(MainDirOUT)

                  # Reading rainfall observations and their metadata (i.e. lats/lons/dates)
                  lats = np.load(MainDirIN + "/stn_lats.npy")
                  lons = np.load(MainDirIN + "/stn_lons.npy")
                  dates = np.load(MainDirIN + "/dates.npy")
                  align_obs = np.load(MainDirIN + "/obs.npy")
                  NumStns = align_obs.shape[0]
                  NumDays = align_obs.shape[1]

                  # Plotting maximum observed rainfall values
                  for ClimateType in ClimateType_list:
                        
                        for MinDays_Perc in MinDays_Perc_list:
                              
                              print(" - " + ClimateType + " with a minum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" )

                              # Select the year/seasonal subset with the minimum number of 
                              Title_text_line_1 = "Maximum " + str(Acc) + "-hourly rainfall (mm) observed at each station between " + str(YearS) + " and " + str(YearF)
                              Title_text_line_2 = ClimateType + " observations in " + NameOBS.split("_")[-1] + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") - Minimum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" 
                              plot_MaxRainOBS(align_obs, lats, lons, dates, ClimateType, MinDays_Perc, Title_text_line_1, Title_text_line_2, MainDirOUT)
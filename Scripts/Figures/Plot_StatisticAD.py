import os
from os.path import exists
import numpy as np
import metview as mv

########################################################################################################################################################################
# CODE DESCRIPTION
# Plot_StatisticAD.py plots the Anderson-Darling statistic at the points where rainfall climatologies were computed. The script generates the map plots as static svg figures or in a Metview interactive window.

# DESCRIPTION OF INPUT PARAMETERS
# Acc (number, in hours): rainfall accumulation period.
# Climate_OBS_Period (string, in YearS_YearF format): indicates the start/final year the observational climatologies are valid for.
# RunType (string): type of run. Valid values are:
#                                   - "Interactive": to open the plot on an interacive Metview window.
#                                   - "Static": to save the plot on a static svg map.
# SystemFC_list (list of string): list of forecasting systems to consider.
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
Acc = 24
Climate_OBS_Period = "2000_2019"
RunType = "Static"
SystemFC_list = ["HRES_46r1", "Reforecasts_46r1", "ERA5_ShortRange", "ERA5_EDA_ShortRange", "ERA5_LongRange", "ERA5_EDA_LongRange", "ERA5_ecPoint/Grid_BC_VALS", "ERA5_ecPoint/Pt_BC_PERC"]
MinDays_Perc_list = [0.5,0.75]
NameOBS_list = ["06_AlignedOBS_rawSTVL", "07_AlignedOBS_gridCPC", "08_AlignedOBS_cleanSTVL"]
Coeff_Grid2Point_list = [2,5,10,20,50,100]
ClimateType_list = ["Year", "DJF", "MAM", "JJA", "SON"]
Git_repo = "/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN = "Data/Processed/12_StatisticAD"
DirOUT= "Data/Figures/StatisticAD"

# SystemFC_list = ["HRES_46r1", "Reforecasts_46r1", "ERA5_ShortRange", "ERA5_EDA_ShortRange", "ERA5_LongRange", "ERA5_EDA_LongRange", "ERA5_ecPoint/Grid_BC_VALS", "ERA5_ecPoint/Pt_BC_PERC"]
# MinDays_Perc_list = [0.5,0.75]
# NameOBS_list = ["06_AlignedOBS_rawSTVL", "07_AlignedOBS_gridCPC", "08_AlignedOBS_cleanSTVL"]
# Coeff_Grid2Point_list = [2,5,10,20,50,100]
# ClimateType_list = ["Year", "DJF", "MAM", "JJA", "SON"]

# SystemFC_list = ["Reforecasts_46r1"]
# MinDays_Perc_list = [0.5]
# NameOBS_list = ["08_AlignedOBS_cleanSTVL"]
# Coeff_Grid2Point_list = [20]
# ClimateType_list = ["SON"]
############################################################################################################################################################

# Costum functions
def plot_statisticAD(RunType, ClimateType, Title_text_line_1, Title_text_line_2, DirIN, DirOUT):

      # Reading the considered climatology and the correspondent percentiles, and the rainfall stations coordinates
      StatisticAD_array = np.load(DirIN + "/StatisticAD_" + ClimateType + ".npy")
      CriticalVal_array = np.load(DirIN + "/CriticalVal_" + ClimateType + ".npy")
      lats = np.load(DirIN + "/" + "Stn_lats.npy")
      lons = np.load(DirIN + "/" + "Stn_lons.npy")
    
      # Define when to reject or not-reject the null hypothesis of the Anderson-Darling test
      not_reject_array = np.empty(StatisticAD_array.shape[0]) + np.nan
      not_reject_array = np.where(StatisticAD_array[:,0] < CriticalVal_array[0][0], not_reject_array, 1)
      not_reject_array = np.where(StatisticAD_array[:,0] > CriticalVal_array[0][0], not_reject_array, 0)
      
      # Converting the climatology to geopoint
      not_reject_geo = mv.create_geo(
            type = 'xyv',
            latitudes =  lats,
            longitudes = lons,
            values = not_reject_array
            )

      # Plotting the A-D statistic
      coastlines = mv.mcoast(
            map_coastline_thickness = 2,
            map_coastline_resolution = "medium",
            map_boundaries = "on",
            map_boundaries_colour = "black",
            map_boundaries_thickness = 1,
            map_grid = "off",
            map_label = "off"
            )
      
      Europe = mv.geoview(
        map_projection      = "lambert",
        map_area_definition = "corners",
        area                = [23.12,-9.55,56.31,87.75]
        )

      if RunType == "Static":
            symbol_height = 0.1
      else:
            symbol_height = 0.2

      markers = mv.psymb(
            symbol_type = "MARKER",
            symbol_table_mode = "ON",
            legend = "ON",
            symbol_quality = "HIGH",
            symbol_min_table = [ -0.5, 0.5],
            symbol_max_table = [0.5,1.5],
            symbol_marker_table = [ 15,15],
            symbol_colour_table = ["magenta","green"],
            symbol_height_table = [ symbol_height,symbol_height]
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
            
            mv.plot(not_reject_geo, coastlines, markers, legend, title)
      
      else:
            
            # Global map
            svg = mv.png_output(output_name = DirOUT + "/" + ClimateType)
            mv.setoutput(svg)
            mv.plot(not_reject_geo, coastlines, markers, legend, title)
            
            # Zoom for Europe
            svg = mv.png_output(output_name = DirOUT + "/" + ClimateType + "_Europe")
            mv.setoutput(svg)
            mv.plot(not_reject_geo, Europe, coastlines, markers, legend, title)

#######################################################################################################################

for SystemFC in SystemFC_list:

      for MinDays_Perc in MinDays_Perc_list:

            for NameOBS in NameOBS_list:

                  if (NameOBS == "06_AlignedOBS_rawSTVL") or (NameOBS == "07_AlignedOBS_gridCPC"):

                        print(" ")
                        print("Plotting the Anderson-Darling statistic for " + SystemFC + " for " + NameOBS + " with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                        Dataset_temp = NameOBS.split("_")[-1]     
                        Title_text_line_2 = Dataset_temp + " - Minum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" 
                        
                        # Setting main input/output directories
                        MainDirIN = Git_repo + "/" + DirIN + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period
                        MainDirOUT = Git_repo + "/" + DirOUT + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period
                        if not exists(MainDirOUT):
                              os.makedirs(MainDirOUT)

                        # Plotting climatologies
                        for ClimateType in ClimateType_list:               
                              print(" - " + ClimateType)
                              Title_text_line_1 = "Anderson-Darling Statistic for " + SystemFC + " for " + ClimateType + " climatology"
                              plot_statisticAD(RunType, ClimateType, Title_text_line_1, Title_text_line_2, MainDirIN, MainDirOUT)

                  elif NameOBS == "08_AlignedOBS_cleanSTVL":

                        for Coeff_Grid2Point in Coeff_Grid2Point_list:
                                    
                              print(" ")
                              print("Plotting the Anderson-Darling statistic for " + SystemFC + " for " + NameOBS + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ") with a minimum of " + str(int(MinDays_Perc*100)) + "% of days over the considered period with valid observations to compute the climatologies")
                              Dataset_temp = NameOBS.split("_")[-1] + " (Coeff_Grid2Point=" + str(Coeff_Grid2Point) + ")"
                              Title_text_line_2 = Dataset_temp + " - Minum of " + str(int(MinDays_Perc*100)) + "% of days with valid observations" 

                              # Setting main input/output directories
                              MainDirIN = Git_repo + "/" + DirIN + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              MainDirOUT = Git_repo + "/" + DirOUT + "/" + SystemFC + "/MinDays_Perc" + str(int(MinDays_Perc*100)) + "/" + NameOBS + "_" + str(Acc) + "h_" + Climate_OBS_Period + "/Coeff_Grid2Point_" + str(Coeff_Grid2Point)
                              if not exists(MainDirOUT):
                                    os.makedirs(MainDirOUT)

                              # Plotting climatologies
                              for ClimateType in ClimateType_list:               
                                    print(" - " + ClimateType)
                                    Title_text_line_1 = "Anderson-Darling Statistic for " + SystemFC + " for " + ClimateType + " climatology"
                                    plot_statisticAD(RunType, ClimateType, Title_text_line_1, Title_text_line_2, MainDirIN, MainDirOUT)
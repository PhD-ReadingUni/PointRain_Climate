#!/bin/bash

###############################################################################################################################
# CODE DESCRIPTION
# Retrieve_ERA5_ecPoint.sh retrieves (short-range) ERA5_ecPoint rainfall forecasts (point-scale rainfall totals over the ERA5 grid, at 31 km spatial resolution).
# The total precipitation is already accumulated over the period of interest.

# DESCRIPTION OF INPUT PARAMETERS
# Years_array (array of numbers): years to retrieve
# Git_repo (string): path of local github repository
# DirIN_full (string): full path of the database containing the ecPoint-ERA5 rainfall forecasts.
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
Years_array=(2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2018 2019)
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirIN_full="/ec/vol/highlander/ERA5_ecPoint_70yr/Rainfall_24h"
DirOUT="Data/Raw/FC/ERA5_ecPoint"
###############################################################################################################################

# Setting input directories
DirIN_full_Grid=${DirIN_full}/Grid_BC_VALS
DirIN_full_Pt=${DirIN_full}/Pt_BC_PERC
DirIN_full_WT=${DirIN_full}/WT

# Setting output directories
DirOUT_Grid=${Git_repo}/${DirOUT}/Grid_BC_VALS
DirOUT_Pt=${Git_repo}/${DirOUT}/Pt_BC_PERC
DirOUT_WT=${Git_repo}/${DirOUT}/WT
mkdir -p ${DirOUT_Grid}
mkdir -p ${DirOUT_Pt}
mkdir -p ${DirOUT_WT}

# Retrieving ecPoint_ERA5 rainfall forecasts
for Year in ${Years_array[@]}; do
      
      echo "Retrieving year " ${Year}

      cp -r ${DirIN_full_Grid}/${Year}* ${DirOUT_Grid}
      cp -r ${DirIN_full_Pt}/${Year}* ${DirOUT_Pt}
      cp -r ${DirIN_full_WT}/${Year}* ${DirOUT_WT}

done
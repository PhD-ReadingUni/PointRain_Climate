#!/bin/bash

#########################################################################################################################
# CODE DESCRIPTION
# Retrieve_OBS_CPC.sh retrieves rainfall observations from the "CPC Global Unified Gauge-Based Analysis of Daily Precipitation" dataset from NOAA.
# The data is downloaded and saved manually in the relevant directory.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (date, in YYYYMMDD format): start year to retrieve
# YearF (date, in YYYYMMDD format): final year to retrieve
# Acc (number, in hours): accumulation period for rainfall
# Git_repo (string): path of local github repository
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
YearS=2000
YearF=2019
Acc = 24
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirOUT="Data/Raw/OBS/CPC"
#########################################################################################################################

# GENERAL

# The official website of the "CPC Global Unified Gauge-Based Analysis of Daily Precipitation" dataset can be found here:
# https://psl.noaa.gov/data/gridded/data.cpc.globalprecip.html

# A general guide for the "NetCDF Climate and Forecast (CF) Metadata Conventions"can be found here:
# https://cfconventions.org/Data/cf-conventions/cf-conventions-1.10/cf-conventions.html#_data_types

##############################################################
# The raw data was downloaded manually here:
# https://downloads.psl.noaa.gov/Datasets/cpc_global_precip/

# The data is stored in the following directory:
MainDirOUT = Git_repo + "/" + DirOUT + "_" + str(Acc)
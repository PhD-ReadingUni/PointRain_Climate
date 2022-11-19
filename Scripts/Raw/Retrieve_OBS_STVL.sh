#!/bin/bash

#########################################################################
# CODE DESCRIPTION
# Retrieve_OBS_STVL.sh retrieves rainfall observations from the STVL database @ECMWF. 
# For a description of the available rainfall datasets in the database, go to: 
# https://confluence.ecmwf.int/display/VER/STVL+datasets

# DESCRIPTION OF INPUT PARAMETERS
# Acc (number, in hours): accumulation period for rainfall
# DateS (date, in YYYYMMDD format): start date to retrieve
# DateF (date, in YYYYMMDD format): final date to retrieve
# Dataset_array (array of strings): list of datasets downloaded from stvl
# Git_repo (string): path of local github repository
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
Acc=24
DateS=20000101
DateF=20200101
Dataset_array=("synop" "hdobs" "bom" "india" "efas" "vnm" "ukceda")
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirOUT="Data/Raw/OBS/STVL"
#########################################################################

# Setting general parameters
DateS=$(date -d $DateS +%Y%m%d)
DateF=$(date -d $DateF +%Y%m%d)

# Retrieving observations for a considered dataset
for Dataset in ${Dataset_array[@]}; do 

    # Setting main directory
    MainDir=${Git_repo}/${DirOUT}_${Acc}h/${Dataset}
    mkdir -p ${MainDir}
    
    TheDate=${DateS}
    while [[ ${TheDate} -le ${DateF} ]]; do
        
        echo "Retrieving ${Acc}-hourly rainfall observations from ${Dataset} for ${TheDate}..."
    
        # Creating the sub-directories for each considered date
        Dir_temp=${MainDir}/${TheDate}
        mkdir -p ${Dir_temp}
 
        # Retrieve the rainfall observations for the considered date
        ~moz/bin/stvl_getgeo --parameter tp --sources ${Dataset} --period ${Acc} --dates ${TheDate} --times 0/to/23/by/1 --columns value_0 elevation --outdir ${Dir_temp} --flattree

        # Delete empty temporary directories
        if [ -z "$(ls -A ${Dir_temp})" ]; then
            rm -rf ${Dir_temp}
	    fi

    TheDate=$(date -d "${TheDate} + 1 day" +"%Y%m%d")

    done 

done
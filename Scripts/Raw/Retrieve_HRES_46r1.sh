#!/bin/bash

#################################################################################################
# CODE DESCRIPTION
# Retrieve_HRES_46r1.sh retrieves rainfall forecasts from the ECMWF HRES, for the 46r1 cycle (9 km spatial resolution).
# The period between 01/07/2019 and 30/06/2020 is retrieved to match the period considered for the reforecasts. 

# DESCRIPTION OF INPUT PARAMETERS
# BaseDateS (date, in format YYYYMMDD): start base date to retrieve
# BaseDateF (date, in format YYYYMMDD): final base date to retrieve
# Git_repo (string): path of local github repository
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
BaseDateS=20190701
BaseDateF=20200630
Git_repo="/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirOUT="Data/Raw/Forecasts/HRES_46r1"
#################################################################################################

# Setting the main output directory
MainDirOUT=${Git_repo}/${DirOUT}

# Retrieving forecasts from MARS
BaseDateS=$(date -d $BaseDateS +%Y%m%d)
BaseDateF=$(date -d $BaseDateF +%Y%m%d)
BaseDate=$BaseDateS

BaseTime=0
BaseTimeSTR="00"

while [[ $BaseDate -le $BaseDateF ]]; do

        Dir_temp=${MainDirOUT}/${BaseDate}${BaseTimeSTR}
        mkdir -p ${Dir_temp}
    
mars <<EOF

    retrieve,
        class=od,
        date=${BaseDate},
        expver=1,
        levtype=sfc,
        param=228.128,
        step=0/24/48/72/96/120/144/168/192/216/240,
        stream=oper,
        time=${BaseTime},
        type=fc,
        target="${Dir_temp}/tp_${BaseDate}_${BaseTimeSTR}_[step].grib"

EOF

        # Reorganizing the name of the retrieved files
        for Step in 0 24 48 72 96; do
            
            if [[ ${Step} -lt 10 ]]; then
                StepSTR=00${Step}
            else
                StepSTR=0${Step}
            fi        
            
            mv "${Dir_temp}/tp_${BaseDate}_${BaseTimeSTR}_${Step}.grib" "${Dir_temp}/tp_${BaseDate}_${BaseTimeSTR}_${StepSTR}.grib"
        
        done
                
    done
                    
    BaseDate=$(date -d"$BaseDate + 1 day" +"%Y%m%d")
    
done
#!/bin/bash

###################################################################################
# CODE DESCRIPTION
# Retrieve_ERA5_ShortRange.sh retrieves short-range ERA5 rainfall analysis (31 km spatial resolution).

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number): start year to retrieve
# YearF (number): final year to retrieve
# Git_repo (string): path of local github repository
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
YearS=2000
YearF=2019
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirOUT="Data/Raw/FC/ERA5_ShortRange"
###################################################################################

# Setting main output directory
MainDirOUT=${Git_repo}/${DirOUT}

# Creating the database
for Year in $(seq ${YearS} ${YearF}); do
    
    DirOUT_Year=${MainDirOUT}/${Year}
    mkdir -p ${DirOUT_Year}
    
    # Retrieving the forecasts from MARS
    # The advice is to retrieve monthly chunks at a time to be more efficient with the Mars retrievals
    for Month in 01 02 03 04 05 06 07 08 09 10 11 12; do
        
        # Selecting the end day of the month to retrieve
        if [ ${Month} -eq 01 ] || [ ${Month} -eq 03 ] || [ ${Month} -eq 05 ] || [ ${Month} -eq 07 ] || [ ${Month} -eq 08 ] || [ ${Month} -eq 10 ] || [ ${Month} -eq 12 ]; then
            LastDayMonth=31
        elif [ ${Month} -eq 04 ] || [ ${Month} -eq 06 ] || [ ${Month} -eq 09 ] || [ ${Month} -eq 11 ]; then 
            LastDayMonth=30
        elif [ ${Month} -eq 02 ]; then
            ans=`expr ${Year} % 4`
            if [ $ans -eq 0 ]; then     
                LastDayMonth=29
            else
                LastDayMonth=28
            fi
        fi
    
        # Mars retrieval
mars <<EOF
        retrieve,
            class=ea,
            date=${Year}-${Month}-01/to/${Year}-${Month}-${LastDayMonth},
            expver=1,
            levtype=sfc,
            param=228.128,
            step=0/1/2/3/4/5/6/7/8/9/10/11/12/13/14/15/16/17/18,
            stream=oper,
            time=6/18,
            type=fc,
            target="${DirOUT_Year}/tp_[date]_[time]_[step].grib"   
EOF

        # Organizing the retrieved monthly files into single files per day, time, and step
        echo "Organizing the retrieved monthly files into single files per day, time, and step"
        BaseDateS=${Year}-${Month}-01
        BaseDateF=${Year}-${Month}-${LastDayMonth}
        BaseDateS=$(date -d $BaseDateS +%Y%m%d)
        BaseDateF=$(date -d $BaseDateF +%Y%m%d)

        BaseDate=${BaseDateS}
        while [[ ${BaseDate} -le ${BaseDateF} ]]; do
        
            for BaseTime in 6 18; do

                if [[ ${BaseTime} -eq 6 ]]; then    
                    BaseTimeSTR_old="600"
                    BaseTimeSTR_new="06"
                else
                    BaseTimeSTR_old="1800"
                    BaseTimeSTR_new="18"
                fi
                
                DirOUT_temp="${DirOUT_Year}/${BaseDate}${BaseTimeSTR_new}"
                mkdir -p ${DirOUT_temp}
                
                for Step in 0 1 2 3 4 5 6  7 8 9 10 11 12 13 14 15 16 17 18; do

                    if [[ ${Step} -lt 10 ]]; then    
                        StepSTR="00"${Step}
                    else
                        StepSTR="0"${Step}
                    fi

                    mv ${DirOUT_Year}/tp_${BaseDate}_${BaseTimeSTR_old}_${Step}.grib ${DirOUT_temp}/tp_${BaseDate}_${BaseTimeSTR_new}_${StepSTR}.grib

                done
            
            done
            
            BaseDate=$(date -d"${BaseDate} + 1 day" +"%Y%m%d")
        
        done
    
    done 

done
#!/bin/bash

####################################################################################
# CODE DESCRIPTION
# Retrieve_ERA5_LongRange.sh retrieves long-range ERA5 rainfall forecasts (31 km spatial resolution).
# Total precipitation is not stored for the long range forecasts; therefore, it is obtained by adding up the   
# convective and the large-scale components. The right parameter name ("tp") is set to the output files.

# DESCRIPTION OF INPUT PARAMETERS
# YearS (number): start year to retrieve
# YearF (number): final year to retrieve
# Git_repo (string): path of local github repository
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
YearS=2000
YearF=2019
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirOUT="Data/Raw/FC/ERA5_LongRange"
####################################################################################

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
            expver=11,
            levtype=sfc,
            param=142.128/143.128,
            step=0/3/6/9/12/18/24/30/36/42/48/54/60/66/72/78/84/90/96/102/108/114/120/132/144/156/168/180/192/204/216/228/240,
            stream=oper,
            time=0,
            type=fc,
            target="${DirOUT_Year}/[date]_[time].grib"   
EOF

        # Computing the total precipitation
        echo "Computing the total precipitation, and spliting the files for each step"
        
        BaseDateS=${Year}-${Month}-01
        BaseDateF=${Year}-${Month}-${LastDayMonth}
        BaseDateS=$(date -d $BaseDateS +%Y%m%d)
        BaseDateF=$(date -d $BaseDateF +%Y%m%d)
        BaseDate=${BaseDateS}
        
        BaseTime=0
        BaseTimeSTR=0${BaseTime}

        while [[ ${BaseDate} -le ${BaseDateF} ]]; do
            
            DirOUT_temp="${DirOUT_Year}/${BaseDate}${BaseTimeSTR}"
            mkdir -p ${DirOUT_temp}
            mv ${DirOUT_Year}/${BaseDate}_${BaseTime}.grib ${DirOUT_temp}/${BaseDate}_${BaseTimeSTR}.grib
      
mars <<EOF                
                
                read, 
                    source="${DirOUT_temp}/${BaseDate}_${BaseTimeSTR}.grib", 
                    param=142.128, 
                    fieldset=cp
            
                read, 
                    source="${DirOUT_temp}/${BaseDate}_${BaseTimeSTR}.grib", 
                    param=143.128, 
                    fieldset=lsp
        
                compute,
                    formula="cp+lsp",
                    target="${DirOUT_temp}/tp_${BaseDate}_${BaseTimeSTR}.grib"
EOF

                # Setting the correct "shortName" for the computed total precipation, and splitting the original file into single files per step
                echo "Setting the correct "shortName" for the computed total precipation, and splitting the original file into single files per step"
                grib_set -s shortName=tp ${DirOUT_temp}/tp_${BaseDate}_${BaseTimeSTR}.grib ${DirOUT_temp}/new_tp_${BaseDate}_${BaseTimeSTR}.grib
                grib_copy ${DirOUT_temp}/new_tp_${BaseDate}_${BaseTimeSTR}.grib ${DirOUT_temp}/tp_${BaseDate}_${BaseTimeSTR}_[step].grib
                
                # Setting each single file with the final naming convention
                echo "Setting each single file with the final naming convention"
                for Step in 0 3 6 9 12 18 24 30 36 42 48 54 60 66 72 78 84 90 96; do
                    if [[ ${Step} -lt 10 ]]; then
                        StepSTR=00${Step}
                    else
                        StepSTR=0${Step}
                    fi        
                    mv "${DirOUT_temp}/tp_${BaseDate}_${BaseTimeSTR}_${Step}.grib" "${DirOUT_temp}/tp_${BaseDate}_${BaseTimeSTR}_${StepSTR}.grib"
                done

                # Removing the temporary files
                echo "Removing the temporary files"
                rm -rf ${DirOUT_temp}/${BaseDate}_${BaseTimeSTR}.grib ${DirOUT_temp}/tp_${BaseDate}_${BaseTimeSTR}.grib ${DirOUT_temp}/new_tp_${BaseDate}_${BaseTimeSTR}.grib
            
            BaseDate=$(date -d"${BaseDate} + 1 day" +"%Y%m%d")
        
        done
    
    done
    
done  
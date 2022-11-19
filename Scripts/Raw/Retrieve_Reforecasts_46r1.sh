#!/bin/bash

############################################################################################################
# CODE DESCRIPTION
# Retrieve_Reforecasts_46r1.sh retrieves rainfall forecasts from the ECMWF reforecasts, for the 46r1 cycle (18 km spatial resolution).
# Only control forecasts are considered to use the member with the best physics representation of the rainfall generation 
# mechanisms. The period between 01/07/2019 and 30/06/2020 is considered. 

# DESCRIPTION OF INPUT PARAMETERS
# BaseDateS (date, in format YYYYMMDD): start base date to retrieve
# BaseDateF (date, in format YYYYMMDD): final base date to retrieve
# Git_repo (string): path of local github repository
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
BaseDateS=20190701
BaseDateF=20200630
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirOUT="Data/Raw/FC/Reforecasts_46r1"
############################################################################################################

# Setting main output directory
MainDirOUT=${Git_repo}/${DirOUT}

# Retrieving the reforecasts
echo "Retrieving the 00 UTC run reforecasts from MARS for the period between ${BaseDateS} and ${BaseDateF}"
BaseDateS=$(date -d $BaseDateS +%Y%m%d)
BaseDateF=$(date -d $BaseDateF +%Y%m%d)
BaseDate=$BaseDateS
while [[ $BaseDate -le $BaseDateF ]]; do

    # Selecting the days to retrieve that are available in the reforecasts
    TheWeekDay=$(date -d $BaseDate "+%A")
    if [[ ${TheWeekDay} = "Monday" ]] || [[ ${TheWeekDay} = "Thursday" ]]; then    
        
        echo " "
        echo "Retrieving reforecasts for ${BaseDate}"
        
        # Extracting the year, month and day from the basedate
        Year=$(date -d $BaseDate +%Y)
        Month=$(date -d $BaseDate +%m)
        Day=$(date -d $BaseDate +%d)
        
        #Setting the reforecasts years to retrieve
        Year01=$(expr ${Year} - 1)
        Year02=$(expr ${Year} - 2)
        Year03=$(expr ${Year} - 3)
        Year04=$(expr ${Year} - 4)
        Year05=$(expr ${Year} - 5)
        Year06=$(expr ${Year} - 6)
        Year07=$(expr ${Year} - 7)
        Year08=$(expr ${Year} - 8)
        Year09=$(expr ${Year} - 9)
        Year10=$(expr ${Year} - 10)
        Year11=$(expr ${Year} - 11)
        Year12=$(expr ${Year} - 12)
        Year13=$(expr ${Year} - 13)
        Year14=$(expr ${Year} - 14)
        Year15=$(expr ${Year} - 15)
        Year16=$(expr ${Year} - 16)
        Year17=$(expr ${Year} - 17)
        Year18=$(expr ${Year} - 18)
        Year19=$(expr ${Year} - 19)
        Year20=$(expr ${Year} - 20)
        
        # Setting the reforecasts BaseDates to retrieve
        BaseDate01=${Year01}${Month}${Day}
        BaseDate02=${Year02}${Month}${Day}
        BaseDate03=${Year03}${Month}${Day}
        BaseDate04=${Year04}${Month}${Day}
        BaseDate05=${Year05}${Month}${Day}
        BaseDate06=${Year06}${Month}${Day}
        BaseDate07=${Year07}${Month}${Day}
        BaseDate08=${Year08}${Month}${Day}
        BaseDate09=${Year09}${Month}${Day}
        BaseDate10=${Year10}${Month}${Day}
        BaseDate11=${Year11}${Month}${Day}
        BaseDate12=${Year12}${Month}${Day}
        BaseDate13=${Year13}${Month}${Day}
        BaseDate14=${Year14}${Month}${Day}
        BaseDate15=${Year15}${Month}${Day}
        BaseDate16=${Year16}${Month}${Day}
        BaseDate17=${Year17}${Month}${Day}
        BaseDate18=${Year18}${Month}${Day}
        BaseDate19=${Year19}${Month}${Day}
        BaseDate20=${Year20}${Month}${Day}
        TheBaseDates_ref=(${BaseDate01} ${BaseDate02} ${BaseDate03} ${BaseDate04} ${BaseDate05} ${BaseDate06} ${BaseDate07} ${BaseDate08} ${BaseDate09} ${BaseDate10} ${BaseDate11} ${BaseDate12} ${BaseDate13} ${BaseDate14} ${BaseDate15} ${BaseDate16} ${BaseDate17} ${BaseDate18} ${BaseDate19} ${BaseDate20})
                  
        # Creating permanent directories where to store the reforecasts
        Dir01="${MainDirOUT}/${Year01}/${BaseDate01}00"
        Dir02="${MainDirOUT}/${Year02}/${BaseDate02}00"
        Dir03="${MainDirOUT}/${Year03}/${BaseDate03}00"
        Dir04="${MainDirOUT}/${Year04}/${BaseDate04}00"
        Dir05="${MainDirOUT}/${Year05}/${BaseDate05}00"
        Dir06="${MainDirOUT}/${Year06}/${BaseDate06}00"
        Dir07="${MainDirOUT}/${Year07}/${BaseDate07}00"
        Dir08="${MainDirOUT}/${Year08}/${BaseDate08}00"
        Dir09="${MainDirOUT}/${Year09}/${BaseDate09}00"
        Dir10="${MainDirOUT}/${Year10}/${BaseDate10}00"
        Dir11="${MainDirOUT}/${Year11}/${BaseDate11}00"
        Dir12="${MainDirOUT}/${Year12}/${BaseDate12}00"
        Dir13="${MainDirOUT}/${Year13}/${BaseDate13}00"
        Dir14="${MainDirOUT}/${Year14}/${BaseDate14}00"
        Dir15="${MainDirOUT}/${Year15}/${BaseDate15}00"
        Dir16="${MainDirOUT}/${Year16}/${BaseDate16}00"
        Dir17="${MainDirOUT}/${Year17}/${BaseDate17}00"
        Dir18="${MainDirOUT}/${Year18}/${BaseDate18}00"
        Dir19="${MainDirOUT}/${Year19}/${BaseDate19}00"
        Dir20="${MainDirOUT}/${Year20}/${BaseDate20}00"
        TheDirs_ref=(${Dir01} ${Dir02} ${Dir03} ${Dir04} ${Dir05} ${Dir06} ${Dir07} ${Dir08} ${Dir09} ${Dir10} ${Dir11} ${Dir12} ${Dir13} ${Dir14} ${Dir15} ${Dir16} ${Dir17} ${Dir18} ${Dir19} ${Dir20})
        mkdir -p ${Dir01} ${Dir02} ${Dir03} ${Dir04} ${Dir05} ${Dir06} ${Dir07} ${Dir08} ${Dir09} ${Dir10} ${Dir11} ${Dir12} ${Dir13} ${Dir14} ${Dir15} ${Dir16} ${Dir17} ${Dir18} ${Dir19} ${Dir20}
        
        # Retrieving the reforecasts from MARS  
        echo " - Retrieving the reforecasts from MARS..." 
mars <<EOF
    retrieve,
        class=od,
        date=${BaseDate},
        expver=1,
        hdate=${BaseDate01}/${BaseDate02}/${BaseDate03}/${BaseDate04}/${BaseDate05}/${BaseDate06}/${BaseDate07}/${BaseDate08}/${BaseDate09}/${BaseDate10}/${BaseDate11}/${BaseDate12}/${BaseDate13}/${BaseDate14}/${BaseDate15}/${BaseDate16}/${BaseDate17}/${BaseDate18}/${BaseDate19}/${BaseDate20},
        levtype=sfc,
        param=228.128,
        step=0/24/48/72/96/120/144/168/192/216/240,
        stream=enfh,
        time=0,
        type=cf,
        target="${MainDirOUT}/tp_${BaseDate}_00.grib"
EOF

        # Splitting the retrieved files and saving the single files in the relevant directories
        echo " - Splitting the retrieved file and saving them in the relevant directories..."
        grib_copy "${MainDirOUT}/tp_${BaseDate}_00.grib" "${MainDirOUT}/tp_[dataDate]_00.grib"
        
        let length_ref=${#TheBaseDates_ref[@]}-1
        for ind in $(seq 0 ${length_ref}); do
            
            TheBaseDate_ref=${TheBaseDates_ref[${ind}]}
            TheDir=${TheDirs_ref[${ind}]}
            
            grib_copy "${MainDirOUT}/tp_${TheBaseDate_ref}_00.grib" "${TheDir}/tp_${TheBaseDate_ref}_00_[step].grib"
            
            for TheStep in 0 24 48 72 96; do
                
                if [[ ${TheStep} -lt 10 ]]; then
                    TheStepSTR=00${TheStep}
                else
                    TheStepSTR=0${TheStep}
                fi    
                
                mv "${TheDir}/tp_${TheBaseDate_ref}_00_${TheStep}.grib" "${TheDir}/tp_${TheBaseDate_ref}_00_${TheStepSTR}.grib"
            
            done

        done 

        # Deleting all temporary files
        echo " - Deleting all temporary files..."
        rm -rf ${MainDirOUT}/tp_${BaseDate}_00.grib ${MainDirOUT}/tp_${BaseDate01}_00.grib ${MainDirOUT}/tp_${BaseDate02}_00.grib ${MainDirOUT}/tp_${BaseDate03}_00.grib ${MainDirOUT}/tp_${BaseDate04}_00.grib ${MainDirOUT}/tp_${BaseDate05}_00.grib ${MainDirOUT}/tp_${BaseDate06}_00.grib ${MainDirOUT}/tp_${BaseDate07}_00.grib ${MainDirOUT}/tp_${BaseDate08}_00.grib ${MainDirOUT}/tp_${BaseDate09}_00.grib ${MainDirOUT}/tp_${BaseDate10}_00.grib ${MainDirOUT}/tp_${BaseDate11}_00.grib ${MainDirOUT}/tp_${BaseDate12}_00.grib ${MainDirOUT}/tp_${BaseDate13}_00.grib ${MainDirOUT}/tp_${BaseDate14}_00.grib ${MainDirOUT}/tp_${BaseDate15}_00.grib ${MainDirOUT}/tp_${BaseDate16}_00.grib ${MainDirOUT}/tp_${BaseDate17}_00.grib ${MainDirOUT}/tp_${BaseDate18}_00.grib ${MainDirOUT}/tp_${BaseDate19}_00.grib ${MainDirOUT}/tp_${BaseDate20}_00.grib

    else
    
        echo "Date not available in the ECMWF reforecasts."
    
    fi
    
    BaseDate=$(date -d"$BaseDate + 1 day" +"%Y%m%d")
    
done
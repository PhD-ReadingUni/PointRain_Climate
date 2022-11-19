#!/bin/bash

##########################################################################
# CODE DESCRIPTION
# Retrieve_LSM.sh retrieves the land-sea mask for ERA5_EDA, ERA5, Reforecasts and HRES

# DESCRIPTION OF INPUT PARAMETERS
# Git_repo (string): path of local github repository
# DirOUT (string): relative path for the output directory

# INPUT PARAMETERS
Git_repo="/ec/vol/ecpoint/mofp/PhD/Papers2Write/PointRain_Climate"
DirOUT="Data/Raw/LSM"
##########################################################################

# Setting some general parameters
DirOUT=${Git_repo}/${DirOUT}

# Retrieving the land-sea mask for ERA5_EDA
mars <<EOF
        retrieve,
            class=od,
            date=0,
            expver=1,
            levtype=sfc,
            param=172.128,
            step=0,
            stream=enfo,
            time=0,
            type=cf,
            grid=n160,
            target="${DirOUT}/lsm_ERA5_EDA.grib"   
EOF

# Retrieving the land-sea mask for ERA5
mars <<EOF
        retrieve,
            class=od,
            date=0,
            expver=1,
            levtype=sfc,
            param=172.128,
            step=0,
            stream=enfo,
            time=0,
            type=cf,
            grid=n320,
            target="${DirOUT}/lsm_ERA5.grib"   
EOF

# Retrieving the land-sea mask for Reforecasts
mars <<EOF
        retrieve,
            class=od,
            date=0,
            expver=1,
            levtype=sfc,
            param=172.128,
            step=0,
            stream=enfo,
            time=0,
            type=cf,
            target="${DirOUT}/lsm_Reforecasts.grib"   
EOF

# Retrieving the land-sea mask for HRES
mars <<EOF
        retrieve,
            class=od,
            date=0,
            expver=1,
            levtype=sfc,
            param=172.128,
            step=0,
            stream=oper,
            time=0,
            type=fc,
            target="${DirOUT}/lsm_HRES.grib"   
EOF
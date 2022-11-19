#!/bin/bash

#SBATCH --job-name=Extract_Rainfall_atOBS
#SBATCH --output=LogATOS/Extract_Rainfall_atOBS-%J.out
#SBATCH --error=LogATOS/Extract_Rainfall_atOBS-%J.out
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

# INPUTS
Year=${1}

# CODE
time python3 10_Extract_Rainfall_atOBS.py ${Year}
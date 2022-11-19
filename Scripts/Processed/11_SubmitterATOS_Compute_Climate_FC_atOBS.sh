#!/bin/bash

#SBATCH --job-name=Compute_Climate_FC_atOBS
#SBATCH --output=LogATOS/Compute_Climate_FC_atOBS-%J.out
#SBATCH --error=LogATOS/Compute_Climate_FC_atOBS-%J.out
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
#SBATCH --qos=nf
#SBATCH --mail-type=FAIL
#SBATCH --mail-user=fatima.pillosu@ecmwf.int

time python3 11_Compute_Climate_FC_atOBS.py
#!/bin/bash

# # To extract the independent realizations from HRES
# for Year in 2019 2020; do
#       sbatch 10_SubmitterATOS_Extract_Rainfall_atOBS.sh ${Year}
# done

# # To extract the independent realizations from Reforecasts
# for Year in {1999..2019}; do
#       sbatch 10_SubmitterATOS_Extract_Rainfall_atOBS.sh ${Year}
# done

# To extract the independent realizations from all the other forecasting systems
for Year in {2000..2019}; do
      sbatch 10_SubmitterATOS_Extract_Rainfall_atOBS.sh ${Year}
done
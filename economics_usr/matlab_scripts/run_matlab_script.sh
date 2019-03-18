#!/usr/bin/env bash

####  change current working directory and start matlab script 

if [ $1 = "thessaloniki" ]; then
#run both scripts in the same command - shared variables
#Run via MATLAB R2018a
#(cd matlab_scripts/thessaloniki && /usr/local/MATLAB/R2018a/bin/matlab -nodesktop -nosplash -r "regional_baseline; regional_scenario; exit;") > /tmp/matlab.log

#Run via MATLAB R2018a Runtime - 1st parameter is the MATLAB Runtime, 2nd parameter is the unique userID
(cd matlab_scripts/thessaloniki && ./run_main.sh /usr/local/MATLAB/MATLAB_Runtime/v94/ $2) > /tmp/matlab.log
echo "Thessaloniki" > /tmp/matlab_log.txt

elif [ $1 = "cork" ]; then
#Run via MATLAB R2018a
#(cd matlab_scripts/cork && /usr/local/MATLAB/R2018a/bin/matlab -nodesktop -nosplash -r "regional_baseline; regional_scenario; exit;") > /tmp/matlab.log

#Run via MATLAB R2018a Runtime
(cd matlab_scripts/cork && ./run_main.sh /usr/local/MATLAB/MATLAB_Runtime/v94/ $2) > /tmp/matlab.log
echo "Cork" > /tmp/matlab_log.txt

elif [ $1 = "antwerp" ]; then
#Run via MATLAB R2018a
#(cd matlab_scripts/antwerp && /usr/local/MATLAB/R2018a/bin/matlab -nodesktop -nosplash -r "regional_baseline; regional_scenario; exit;") > /tmp/matlab.log

#Run via MATLAB R2018a Runtime
(cd matlab_scripts/antwerp && ./run_main.sh /usr/local/MATLAB/MATLAB_Runtime/v94/ $2) > /tmp/matlab.log
echo "Antwerp" > /tmp/matlab_log.txt

elif [ $1 = "antalya" ]; then
#Run via MATLAB R2018a
#(cd matlab_scripts/antalya && /usr/local/MATLAB/R2018a/bin/matlab -nodesktop -nosplash -r "regional_baseline; regional_scenario; exit;") > /tmp/matlab.log

#Run via MATLAB R2018a Runtime
(cd matlab_scripts/antalya && ./run_main.sh /usr/local/MATLAB/MATLAB_Runtime/v94/ $2) > /tmp/matlab.log
echo "Antalya" > /tmp/matlab_log.txt

else
echo "Matlab script not found" > /tmp/matlab_log.txt
fi


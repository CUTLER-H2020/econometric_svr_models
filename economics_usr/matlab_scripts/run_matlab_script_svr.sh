#!/usr/bin/env bash

####  change current working directory and start matlab script 

if [ $1 = "thessaloniki" ]; then

#Run via MATLAB R2018a Runtime - 1st parameter is the MATLAB Runtime, 2nd parameter is the unique userID
(cd matlab_scripts/thessaloniki_svr && ./run_thes_svr.sh /usr/local/MATLAB/MATLAB_Runtime/v94/ $2) > /tmp/matlab.log
echo "Thessaloniki" > /tmp/matlab_log.txt

elif [ $1 = "cork" ]; then

#Run via MATLAB R2018a Runtime
(cd matlab_scripts/cork_svr && ./run_cork_svr.sh /usr/local/MATLAB/MATLAB_Runtime/v94/ $2) > /tmp/matlab.log
echo "Cork" > /tmp/matlab_log.txt

else
echo "Matlab script not found" > /tmp/matlab_log.txt
fi


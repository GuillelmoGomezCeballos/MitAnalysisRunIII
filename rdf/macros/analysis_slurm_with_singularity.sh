#!/bin/bash

echo "hostname"
hostname
whoami

cd ~/releases/CMSSW_14_1_4/src/;eval `scramv1 runtime -sh`;cd -;

echo "Parameters: " $1 $2 $3 $4 $5

time python3 $5.py --process=$1 --year=$2 --whichJob=$3
status=$?

if [ -f "fillhisto_$5_sample$1_year$2_job$3.root" ]; then
  ###########################################################
  export YEAR=$2
  export SAMPLES=$1
  if [[ "$YEAR" == "20260" && "$SAMPLES" -ge 1000 ]]; then
    export YEAR=20250
    export SAMPLES=$((SAMPLES + 1000))
  fi  
  ########################################################### 
  mv fillhisto_$5_sample$1_year$2_job$3.root fillhisto_$5$4_sample${SAMPLES}_year${YEAR}_job$3.root
  echo "DONE"

elif [ $status -eq 0 ]; then
  echo "DONE NO FILES"

else
  echo "FAILED"

fi

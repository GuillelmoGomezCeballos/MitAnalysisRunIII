#!/bin/bash

echo "hostname"
hostname
whoami

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

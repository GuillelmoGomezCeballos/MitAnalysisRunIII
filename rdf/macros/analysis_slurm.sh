#!/bin/sh

echo "hostname"
hostname
whoami

time python3 $5.py --process=$1 --year=$2 --whichJob=$3
status=$?

if [ -f "fillhisto$5_sample$1_year$2_job$3.root" ]; then
  mv fillhisto$5_sample$1_year$2_job$3.root fillhisto$5$4_sample$1_year$2_job$3.root
  echo "DONE"

elif [ $status -eq 0 ]; then
  echo "DONE NO FILES"

else
  echo "FAILED"

fi

#!/bin/sh

python3 zAnalysis.py --process=$1 --year=$2 --whichJob=$3
status=$?

if [ -f "fillhistoZAna_sample$1_year$2_job$3.root" ]; then
  mv fillhistoZAna_sample$1_year$2_job$3.root fillhistoZAna$4_sample$1_year$2_job$3.root
  echo "DONE"

elif [ $status -eq 0 ]; then
  echo "DONE NO FILES"

else
  echo "FAILED"

fi

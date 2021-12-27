#!/bin/sh

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
scramv1 project CMSSW CMSSW_11_2_0 # cmsrel is an alias not on the workers
cd CMSSW_11_2_0/src/
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
cd ../..

voms-proxy-info

echo "hostname"
hostname
whoami

ls -l
echo $PWD

python sswwAnalysis.py --process=$1 --year=$2 --whichJob=$3
status=$?

rm -f functions_cc* *.pyc

if [ -f "fillhistoSSWWAna_sample$1_year$2_job$3.root" ]; then
  mv fillhistoSSWWAna_sample$1_year$2_job$3.root fillhistoSSWWAna$4_sample$1_year$2_job$3.root
  echo "DONE"

elif [ $status -eq 0 ]; then
  echo "DONE NO FILES"

else
  echo "FAILED"

fi

ls -l

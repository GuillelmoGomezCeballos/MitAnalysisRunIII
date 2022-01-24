#!/bin/sh

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc900
scramv1 project CMSSW CMSSW_12_2_0 # cmsrel is an alias not on the workers
cd CMSSW_12_2_0/src/
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
cd ../..

voms-proxy-info

echo "hostname"
hostname
whoami

ls -l
echo $PWD

python3 zzAnalysis.py --process=$1 --year=$2 --whichJob=$3
status=$?

rm -f functions_cc* *.pyc

if [ -f "fillhistoZZAna_sample$1_year$2_job$3.root" ]; then
  mv fillhistoZZAna_sample$1_year$2_job$3.root fillhistoZZAna$4_sample$1_year$2_job$3.root
  echo "DONE"

elif [ $status -eq 0 ]; then
  echo "DONE NO FILES"

else
  echo "FAILED"

fi

ls -l

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

python3 skim.py --whichSample=$1 --whichJob=$2 --group=$3 --inputSamplesCfg=$4 --inputFilesCfg=$5
status=$?

rm -f functions_cc*

if [ $status -eq 0 ]; then
  echo "SUCCESS"

else
  echo "FAILURE"

fi

ls -l

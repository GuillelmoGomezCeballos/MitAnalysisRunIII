#!/bin/sh

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc11
scramv1 project CMSSW CMSSW_13_2_6 # cmsrel is an alias not on the workers
cd CMSSW_13_2_6/src/
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
cd ../..

voms-proxy-info

echo "hostname"
hostname
whoami

tar xvzf skim.tgz

ls -l
echo $PWD

python3 skim.py --whichSample=$1 --whichJob=$2 --group=$3 --inputSamplesCfg=$4 --inputFilesCfg=$5
status=$?

rm -rf functions_skim_cc* skim.tgz skim.py skim_*.cfg functions_skim.cc haddnanoaod.py jsns config

if [ $status -eq 0 ]; then
  echo "SUCCESS"

else
  echo "FAILURE"

fi

ls -l

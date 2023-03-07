#!/bin/sh

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc10
scramv1 project CMSSW CMSSW_12_6_3 # cmsrel is an alias not on the workers
cd CMSSW_12_6_3/src/
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
cd ../..

voms-proxy-info

tar xvzf $5.tgz

echo $PWD

g++ $(correction config --cflags --ldflags) mysf.cpp -shared -fPIC -o mysf.so

./analysis_slurm.sh $1 $2 $3 $4 $5

rm -rf functions* *.pyc $5.tgz \
*Analysis.py analysis_slurm.sh functions.cc utils*.py \
data \
mysf.* \
jsns config

ls -l

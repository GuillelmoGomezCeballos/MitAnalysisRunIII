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

if [ ! -d "jsonpog/POG" ]; then
  mkdir -p jsonpog/POG/$2;
  mv btagging.json jsonpog/POG/$2/;
  mv electron.json jsonpog/POG/$2/;
  mv muon_Z.json   jsonpog/POG/$2/;
  mv photon.json   jsonpog/POG/$2/;
  mv jmar.json     jsonpog/POG/$2/;
fi

ls -l
echo $PWD

python3 wzAnalysis.py --process=$1 --year=$2 --whichJob=$3
status=$?

rm -f functions_cc* *.pyc

if [ -f "fillhistoWZAna_sample$1_year$2_job$3.root" ]; then
  mv fillhistoWZAna_sample$1_year$2_job$3.root fillhistoWZAna$4_sample$1_year$2_job$3.root
  echo "DONE"

elif [ $status -eq 0 ]; then
  echo "DONE NO FILES"

else
  echo "FAILED"

fi

ls -l

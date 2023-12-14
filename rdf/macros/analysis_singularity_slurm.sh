#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh;export APPTAINER_BIND="/scratch";cmssw-cc7 --command-to-run ls;cd ~/releases/CMSSW_13_2_6/src/;eval `scramv1 runtime -sh`;cd -;./analysis_slurm.sh $1 $2 $3 $4 $5

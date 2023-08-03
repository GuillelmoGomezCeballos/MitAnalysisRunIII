#!/bin/sh

cp -r /home/submit/ceballos/cms/MitAnalysisRunIII/rdf/skimming /data/submit/cms/store/user/ceballos/test0
cd /data/submit/cms/store/user/ceballos/test0
rm config jsns
cp -r /home/submit/ceballos/cms/MitAnalysisRunIII/rdf/macros/jsns .
cp -r /home/submit/ceballos/cms/MitAnalysisRunIII/rdf/macros/config .
rm -rf logs

grep -Ev "tar|rm" skim.sh > skim_new.sh
diff skim_new.sh skim.sh
mv skim_new.sh skim.sh
chmod a+x skim.sh

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc7_amd64_gcc11
scramv1 project CMSSW CMSSW_13_0_0 # cmsrel is an alias not on the workers
cd CMSSW_13_0_0/src/
eval `scramv1 runtime -sh` # cmsenv is an alias not on the workers
cd ../..

cat skim_input_condor_jobs_fromDAS.cfg|awk '{print"./skim.sh "$1" "$2" "$3" skim_input_samples_2023_fromDAS.cfg skim_input_files_fromDAS.cfg"}' > lll
chmod a+x lll

echo "DONE"

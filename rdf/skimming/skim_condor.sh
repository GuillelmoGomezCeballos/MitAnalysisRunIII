#!/bin/sh

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

YEAR=$1

USERPROXY=`id -u`
echo ${USERPROXY}

#condor_q 1769874.0 -analyze
#transfer_input_files = ""
#transfer_output_remaps = "output_1l_${whichSample}_${whichJob}.root =  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/1l/${sampleName}/output_1l_${whichSample}_${whichJob}.root; output_2l_${whichSample}_${whichJob}.root =  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/2l/${sampleName}/output_2l_${whichSample}_${whichJob}.root; output_3l_${whichSample}_${whichJob}.root =  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/3l/${sampleName}/output_3l_${whichSample}_${whichJob}.root"

voms-proxy-init --voms cms --valid 168:00 -pwstdin < $HOME/.grid-cert-passphrase

tar cvzf skim.tgz \
skim.py skim_*.cfg \
functions_skim.cc haddnanoaod.py \
jsns/* config/*

while IFS= read -r line; do

set -- $line
whichSample=$1
whichJob=$2
group=$3
sampleName=$4

if [ ! -d " /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/pho/${sampleName}" ]; then
  echo "creating output folders"  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/nl/${sampleName}
  mkdir -p  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/1l/${sampleName}
  mkdir -p  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/2l/${sampleName}
  mkdir -p  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/3l/${sampleName}
  mkdir -p  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/met/${sampleName}
  mkdir -p  /data/submit/cms/store/user/ceballos/nanoaod/skims_submit/pho/${sampleName}
fi

cat << EOF > submit
Universe   = vanilla
Executable = skim.sh
Arguments  = ${whichSample} ${whichJob} ${group} skim_input_samples_${YEAR}_fromDAS.cfg skim_input_files_fromDAS.cfg
RequestMemory = 6000
RequestCpus = 1
RequestDisk = DiskUsage
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_output_files = ""
Log    = logs/simple_skim_${whichSample}_${whichJob}.log
Output = logs/simple_skim_${whichSample}_${whichJob}.out
Error  = logs/simple_skim_${whichSample}_${whichJob}.error
transfer_input_files = skim.tgz
use_x509userproxy = True
x509userproxy = /tmp/x509up_u${USERPROXY}
Requirements = ( BOSCOCluster =!= "t3serv008.mit.edu" && BOSCOCluster =!= "ce03.cmsaf.mit.edu" && BOSCOCluster =!= "eofe8.mit.edu") && (Machine != "submit81.mit.edu")
+REQUIRED_OS = "rhel7"
+DESIRED_Sites = "mit_tier2,mit_tier3"
Queue
EOF

condor_submit submit

done < skim_input_condor_jobs_fromDAS.cfg

rm -f submit

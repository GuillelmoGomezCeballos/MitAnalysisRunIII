#!/bin/sh

USERPROXY=`id -u`
echo ${USERPROXY}

#condor_q 1769874.0 -analyze

voms-proxy-init --voms cms --valid 168:00

while IFS= read -r line; do

set -- $line
whichSample=$1
whichJob=$2
group=$3
sampleName=$4

if [ ! -d "/work/submit/ceballos/skims/1l/${sampleName}" ]; then
  echo "creating output folders" /work/submit/ceballos/skims/nl/${sampleName}
  mkdir -p /work/submit/ceballos/skims/1l/${sampleName}
  mkdir -p /work/submit/ceballos/skims/2l/${sampleName}
  mkdir -p /work/submit/ceballos/skims/3l/${sampleName}
fi

cat << EOF > submit
Universe   = vanilla
Executable = skim.sh
Arguments  = ${whichSample} ${whichJob} ${group}
RequestMemory = 6000
RequestCpus = 1
RequestDisk = DiskUsage
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_output_remaps = "output_1l_${whichJob}.root = /work/submit/ceballos/skims/1l/${sampleName}/output_1l_${whichJob}.root; output_2l_${whichJob}.root = /work/submit/ceballos/skims/2l/${sampleName}/output_2l_${whichJob}.root; output_3l_${whichJob}.root = /work/submit/ceballos/skims/3l/${sampleName}/output_3l_${whichJob}.root"
Log    = logs/simple_skim_${whichSample}_${whichJob}.log
Output = logs/simple_skim_${whichSample}_${whichJob}.out
Error  = logs/simple_skim_${whichSample}_${whichJob}.error
transfer_input_files = skim.py, skim_input_samples.cfg, skim_input_files.cfg, functions.cc, haddnanoaod.py, jsns/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt
use_x509userproxy = True
x509userproxy = /tmp/x509up_u${USERPROXY}
Requirements = ((BOSCOGroup == "bosco_cms" && BOSCOCluster == "ce03.cmsaf.mit.edu") || (BOSCOCluster == "t3serv008.mit.edu")) && (Machine != "t3btch070.mit.edu") && (Machine != "t3desk014.mit.edu")
+REQUIRED_OS = "rhel7"
Queue
EOF

condor_submit submit

done < skim_input_condor_jobs.cfg

rm -f submit

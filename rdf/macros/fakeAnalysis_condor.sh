#!/bin/sh

USERPROXY=`id -u`
echo ${USERPROXY}

condorJob=1001

voms-proxy-init --voms cms --valid 168:00

while IFS= read -r line; do

set -- $line
whichSample=$1
whichYear=$2

for whichJob in 0 1 2 3 4 5 6 7 8 9
do

cat << EOF > submit
Universe   = vanilla
Executable = fakeAnalysis.sh
Arguments  = ${whichSample} ${whichYear} ${whichJob} ${condorJob}
RequestMemory = 6000
RequestCpus = 1
RequestDisk = DiskUsage
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
Log    = logs/simple_fakeAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}.log
Output = logs/simple_fakeAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}.out
Error  = logs/simple_fakeAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}.error
transfer_input_files = fakeAnalysis.py, functions.cc, utilsAna.py, ../skimming/jsns/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt
use_x509userproxy = True
x509userproxy = /tmp/x509up_u${USERPROXY}
Requirements = ((BOSCOGroup == "bosco_cms" && BOSCOCluster == "ce03.cmsaf.mit.edu") || (BOSCOCluster == "t3serv008.mit.edu")) && (Machine != "t3btch070.mit.edu") && (Machine != "t3desk014.mit.edu")
+REQUIRED_OS = "rhel7"
Queue
EOF

condor_submit submit

done

done < fakeAnalysis_input_condor_jobs.cfg

rm -f submit
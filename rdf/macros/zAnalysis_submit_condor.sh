#!/bin/sh

USERPROXY=`id -u`
echo ${USERPROXY}

condorJob=1001

voms-proxy-init --voms cms --valid 168:00 -pwstdin < $HOME/.grid-cert-passphrase

tar cvzf zAnalysis.tgz \
zAnalysis.py zAnalysis_slurm.sh functions.cc utilsAna.py \
data/* \
mysf.* \
jsns/* config/*

while IFS= read -r line; do

set -- $line
whichSample=$1
whichYear=$2

for whichJob in 0 1 2 3 4 5 6 7 8 9
do

cat << EOF > submit
Universe   = vanilla
Executable = zAnalysis_condor.sh
Arguments  = ${whichSample} ${whichYear} ${whichJob} ${condorJob}
RequestMemory = 6000
RequestCpus = 4
RequestDisk = DiskUsage
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
Log    = logs/simple_zAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}.log
Output = logs/simple_zAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}.out
Error  = logs/simple_zAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}.error
transfer_input_files = zAnalysis.tgz
use_x509userproxy = True
x509userproxy = /tmp/x509up_u${USERPROXY}
Requirements = ( BOSCOCluster =!= "t3serv008.mit.edu" && BOSCOCluster =!= "ce03.cmsaf.mit.edu" && BOSCOCluster =!= "eofe8.mit.edu") && (Machine != "t3btch086.mit.edu")
+REQUIRED_OS = "rhel7"
+DESIRED_Sites = "mit_tier2,mit_tier3"
Queue
EOF

condor_submit submit

done

done < zAnalysis_input_2022_condor_jobs.cfg

rm -f submit

#!/bin/sh

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

theAna=$1
whichAna="DUMMY"
group=9

condorJob=1001
if [ $# -eq 2 ]; then
  condorJob=$2
fi

if [ $theAna -eq 0 ]; then
 whichAna="zAnalysis"
 group=19

elif [ $theAna -eq 1 ]; then
 whichAna="wzAnalysis"

elif [ $theAna -eq 2 ]; then
 whichAna="zzAnalysis"

elif [ $theAna -eq 3 ]; then
 whichAna="sswwAnalysis"

elif [ $theAna -eq 4 ]; then
 whichAna="zmetAnalysis"

elif [ $theAna -eq 5 ]; then
 whichAna="fakeAnalysis"
 nohup ./analysis_slurm.sh 130 2022 -1 1002 fakeAnalysis >& logs/log_130 &
 nohup ./analysis_slurm.sh 131 2022 -1 1003 fakeAnalysis >& logs/log_131 &

elif [ $theAna -eq 6 ]; then
 whichAna="triggerAnalysis"
 group=19

elif [ $theAna -eq 7 ]; then
 whichAna="metAnalysis"

elif [ $theAna -eq 8 ]; then
 whichAna="wwAnalysis"

fi

if [ ${whichAna} = "DUMMY" ]; then
   echo "BAD PARAMETER";
   exit;
fi

USERPROXY=`id -u`
echo ${USERPROXY}

voms-proxy-init --voms cms --valid 168:00 -pwstdin < $HOME/.grid-cert-passphrase

tar cvzf ${whichAna}.tgz \
*Analysis.py analysis_slurm.sh functions.cc utils*.py \
data/* weights_mva/* \
mysf.cpp mysf.h \
jsns/* config/*

while IFS= read -r line; do

set -- $line
whichSample=$1
whichYear=$2
whichSample=$1
whichYear=$2
passSel=$3

if [ "${passSel}" != "no" ]; then

for whichJob in $(seq 0 $group)
do

cat << EOF > submit
Universe   = vanilla
Executable = analysis_condor.sh
Arguments  = ${whichSample} ${whichYear} ${whichJob} ${condorJob} ${whichAna}
RequestMemory = 6000
RequestCpus = 1
RequestDisk = DiskUsage
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
Log    = logs/simple_${whichAna}_${condorJob}_${whichSample}_${whichYear}_${whichJob}.log
Output = logs/simple_${whichAna}_${condorJob}_${whichSample}_${whichYear}_${whichJob}.out
Error  = logs/simple_${whichAna}_${condorJob}_${whichSample}_${whichYear}_${whichJob}.error
transfer_input_files = ${whichAna}.tgz
use_x509userproxy = True
x509userproxy = /tmp/x509up_u${USERPROXY}
Requirements = ( BOSCOCluster =!= "t3serv008.mit.edu" && BOSCOCluster =!= "ce03.cmsaf.mit.edu" && BOSCOCluster =!= "eofe8.mit.edu") && (Machine != "t3btch086.mit.edu")
+REQUIRED_OS = "rhel7"
+DESIRED_Sites = "mit_tier3"
Queue
EOF

condor_submit submit

done

fi

done < ${whichAna}_input_condor_jobs.cfg

rm -f submit

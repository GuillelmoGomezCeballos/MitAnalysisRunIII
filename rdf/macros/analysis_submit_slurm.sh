#!/bin/bash

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
 nohup ./analysis_slurm.sh 110 2022 -1 1002 fakeAnalysis >& logs/log_110 &
 nohup ./analysis_slurm.sh 111 2022 -1 1003 fakeAnalysis >& logs/log_111 &

elif [ $theAna -eq 6 ]; then
 whichAna="triggerAnalysis"
 group=19

elif [ $theAna -eq 7 ]; then
 whichAna="metAnalysis"

fi

if [ ${whichAna} = "DUMMY" ]; then
   echo "BAD PARAMETER";
   exit;
fi

while IFS= read -r line; do

set -- $line
whichSample=$1
whichYear=$2
passSel=$3

if [ "${passSel}" != "no" ]; then

for whichJob in $(seq 0 $group)
do

cat << EOF > submit
#!/bin/bash
#SBATCH --job-name=simple_${whichAna}_${condorJob}_${whichSample}_${whichYear}_${whichJob}
#SBATCH --output=logs/simple_${whichAna}_${condorJob}_${whichSample}_${whichYear}_${whichJob}_%j.out
#SBATCH --error=logs/simple_${whichAna}_${condorJob}_${whichSample}_${whichYear}_${whichJob}_%j.error
#SBATCH --mem-per-cpu=2000
srun ./analysis_slurm.sh ${whichSample} ${whichYear} ${whichJob} ${condorJob} ${whichAna}
EOF

sbatch submit

done

fi

done < ${whichAna}_input_condor_jobs.cfg

rm -f submit

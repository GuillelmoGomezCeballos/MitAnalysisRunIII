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
 nohup ./analysis_slurm.sh 110 20220 -1 1002 fakeAnalysis >& logs/log_110 &
 nohup ./analysis_slurm.sh 136 20220 -1 1003 fakeAnalysis >& logs/log_136 &
 nohup ./analysis_slurm.sh 210 20221 -1 1002 fakeAnalysis >& logs/log_210 &
 nohup ./analysis_slurm.sh 236 20221 -1 1003 fakeAnalysis >& logs/log_236 &

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
#SBATCH --mem-per-cpu=4000
srun ./analysis_slurm.sh ${whichSample} ${whichYear} ${whichJob} ${condorJob} ${whichAna}
EOF

sbatch submit

sleep 0.1

done

fi

done < ${whichAna}_input_condor_jobs.cfg

rm -f submit
#srun ./analysis_slurm.sh ${whichSample} ${whichYear} ${whichJob} ${condorJob} ${whichAna}
##SBATCH --partition=submit-alma9
##SBATCH --exclude=submit[30,81]
#srun ./analysis_singularity_slurm.sh ${whichSample} ${whichYear} ${whichJob} ${condorJob} ${whichAna}
#SBATCH --exclude=submit[52-59]
#scontrol show jobid -dd 644285

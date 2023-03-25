#!/bin/bash

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

theAna=$1
whichAna="DUMMY"

if [ $theAna -eq 0 ]; then
 whichAna="zAnalysis"

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

fi

if [ ${whichAna} = "DUMMY" ]; then
   echo "BAD PARAMETER";
   exit;
fi

condorJob=1001

while IFS= read -r line; do

set -- $line
whichSample=$1
whichYear=$2
passSel=$3

if [ "${passSel}" != "no" ]; then

for whichJob in 0 1 2 3 4 5 6 7 8 9
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

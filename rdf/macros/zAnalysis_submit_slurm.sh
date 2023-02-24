#!/bin/bash

condorJob=1001

while IFS= read -r line; do

set -- $line
whichSample=$1
whichYear=$2

for whichJob in 0 1 2 3 4 5 6 7 8 9
do

cat << EOF > submit
#!/bin/bash
#SBATCH --job-name=simple_zAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}
#SBATCH --output=logs/simple_zAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}_%j.out
#SBATCH --error=logs/simple_zAnalysis_${condorJob}_${whichSample}_${whichYear}_${whichJob}_%j.error
srun ./zAnalysis_slurm.sh ${whichSample} ${whichYear} ${whichJob} ${condorJob}
EOF

sbatch submit

done

done < zAnalysis_input_2022_condor_jobs.cfg

rm -f submit

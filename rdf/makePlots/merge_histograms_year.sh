#!/bin/sh

if [ $# -lt 3 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

theAna=$1;
theCondor=$2;
theYear=$3;
group=9


for i in `seq 0 300`;
do
    if [[ -f anaZ/${theAna}${theCondor}_${theYear}0_${i}.root ]]; then

    hadd -f anaZ/${theAna}${theCondor}_${theYear}_${i}.root anaZ/${theAna}${theCondor}_${theYear}0_${i}.root anaZ/${theAna}${theCondor}_${theYear}1_${i}.root

    fi

done

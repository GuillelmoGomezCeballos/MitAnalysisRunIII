#!/bin/sh

if [ $# -lt 3 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

export theAna=$1
export condorJob=$2
export year=$3

export group=10

if [ $theAna = 'z' ]; then
 export group=20

elif [ $theAna = 'trigger' ]; then
 export group=20

fi

ls logs/simple_${theAna}Analysis_${condorJob}_*_${year}_3_*.out|wc -l|awk '{printf("%d\n",$1*ENVIRON["group"])}'|awk -f ~/bin/sum2.awk;
grep "Total files" logs/simple_${theAna}Analysis_${condorJob}_*_${year}_3_*.out|awk '{a=$3;if(a>ENVIRON["group"])a=ENVIRON["group"];printf("%d\n",a)}'|awk -f ~/bin/sum2.awk;
grep "Total files" logs/simple_${theAna}Analysis_${condorJob}_*_${year}_5_*.out|awk '{a=$3;if(a>ENVIRON["group"])a=ENVIRON["group"];printf("%d\n",a)}'|awk -f ~/bin/sum2.awk;
grep "Total files" logs/simple_${theAna}Analysis_${condorJob}_*_${year}_7_*.out|awk '{a=$3;if(a>ENVIRON["group"])a=ENVIRON["group"];printf("%d\n",a)}'|awk -f ~/bin/sum2.awk;
grep FAILED logs/simple_${theAna}Analysis_${condorJob}_*_${year}_*;
grep DONE   logs/simple_${theAna}Analysis_${condorJob}_*_${year}_*|wc;
grep DONE   logs/simple_${theAna}Analysis_${condorJob}_*_${year}_*|grep -v FILES|wc;
ls fillhisto_${theAna}Analysis${condorJob}*year${year}*|wc

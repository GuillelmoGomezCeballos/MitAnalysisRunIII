#!/bin/sh

export path="fillhisto_zAnalysis1002"
export year=2022
export output="anaZ"

if [ $# -eq 1 ]; then
  export path=$1
fi

hadd -f ${output}/${path}_${year}_muB.root ${output}/${path}_${year}_130.root ${output}/${path}_${year}_131.root
hadd -f ${output}/${path}_${year}_muE.root ${output}/${path}_${year}_132.root ${output}/${path}_${year}_133.root
hadd -f ${output}/${path}_${year}_elB.root ${output}/${path}_${year}_134.root ${output}/${path}_${year}_135.root
hadd -f ${output}/${path}_${year}_elE.root ${output}/${path}_${year}_136.root ${output}/${path}_${year}_137.root

python3 computeLeptonEff.py --path=${path} --year=${year} --output=${output}

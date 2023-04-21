#!/bin/sh

export path="fillhisto_zAnalysis1002"
export year=2022
export output="anaZ"

if [ $# -eq 1 ]; then
  export path=$1
fi

hadd -f ${output}/${path}_${year}_muB.root ${output}/${path}_${year}_130.root ${output}/${path}_${year}_136.root
hadd -f ${output}/${path}_${year}_muE.root ${output}/${path}_${year}_133.root ${output}/${path}_${year}_139.root
hadd -f ${output}/${path}_${year}_elB.root ${output}/${path}_${year}_144.root ${output}/${path}_${year}_150.root
hadd -f ${output}/${path}_${year}_elE.root ${output}/${path}_${year}_147.root ${output}/${path}_${year}_153.root

python3 computeLeptonEff.py --path=${path} --year=${year} --output=${output}

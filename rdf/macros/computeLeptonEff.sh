#!/bin/sh

export path="fillhistoZAna1001"
export year=2018
export output="anaZ"

hadd -f ${output}/${path}_${year}_muB.root ${output}/${path}_${year}_100.root ${output}/${path}_${year}_106.root
hadd -f ${output}/${path}_${year}_muE.root ${output}/${path}_${year}_103.root ${output}/${path}_${year}_109.root
hadd -f ${output}/${path}_${year}_elB.root ${output}/${path}_${year}_114.root ${output}/${path}_${year}_120.root
hadd -f ${output}/${path}_${year}_elE.root ${output}/${path}_${year}_117.root ${output}/${path}_${year}_123.root

python computeLeptonEff.py --path=${path} --year=${year} --output=${output}

#!/bin/sh

theAna=zAnalysis;
theCondor=1002;
theYear=$2;

for theYear in 20220 20221 20230 20231 20240 20250 2027;
do

hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1001.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_178.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_179.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1002.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_180.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_181.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1003.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_182.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_183.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1004.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_184.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_185.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1005.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_186.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_187.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1006.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_190.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_191.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1007.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_192.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_193.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1008.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_194.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_195.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1009.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_196.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_197.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1010.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_198.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_199.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws0_1011.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_188.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_189.root

hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3001.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_378.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_379.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3002.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_380.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_381.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3003.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_382.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_383.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3004.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_384.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_385.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3005.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_386.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_387.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3006.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_390.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_391.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3007.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_392.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_393.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3008.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_394.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_395.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3009.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_396.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_397.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3010.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_398.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_399.root
hadd -f anaZ/fillhisto_${theAna}${theCondor}_${theYear}_ws1_3011.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_388.root anaZ/fillhisto_${theAna}${theCondor}_${theYear}_389.root

done

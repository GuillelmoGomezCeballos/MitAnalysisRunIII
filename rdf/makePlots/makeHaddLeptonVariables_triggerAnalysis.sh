#!/bin/bash

if [ $# -lt 2 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

whichJob=$1
year=$2

hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_200.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_100.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_101.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_202.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_102.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_103.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_204.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_104.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_105.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_206.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_106.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_107.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_208.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_108.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_109.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_210.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_110.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_111.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_212.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_112.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_113.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_214.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_114.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_115.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_216.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_116.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_117.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_218.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_118.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_119.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_220.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_120.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_121.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_222.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_122.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_123.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_224.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_124.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_125.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_226.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_126.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_127.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_228.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_128.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_129.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_230.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_130.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_131.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_232.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_132.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_133.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_234.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_134.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_135.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_236.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_136.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_137.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_238.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_138.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_139.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_240.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_140.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_141.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_242.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_142.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_143.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_244.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_144.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_145.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_246.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_146.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_147.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_248.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_148.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_149.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_250.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_150.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_151.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_252.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_152.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_153.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_254.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_154.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_155.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_256.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_156.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_157.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_258.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_158.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_159.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_260.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_160.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_161.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_262.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_162.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_163.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_264.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_164.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_165.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_266.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_166.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_167.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_268.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_168.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_169.root
hadd -f anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_270.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_170.root anaZ/fillhisto_triggerAnalysis${whichJob}_${year}_171.root

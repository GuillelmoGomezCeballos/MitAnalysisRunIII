#!/bin/sh

if [ $# -lt 2 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

export theOption=$2

if [ $theOption -eq 0 ]; then

  export theAna=sswwAnalysis$1

  root -l -q -b makeSSWWDataCards.C'(0,0,"anaZ","'${theAna}'",20220)'
  root -l -q -b makeSSWWDataCards.C'(0,1,"anaZ","'${theAna}'",20220)'

  root -l -q -b makeSSWWDataCards.C'(0,0,"anaZ","'${theAna}'",20221)'
  root -l -q -b makeSSWWDataCards.C'(0,1,"anaZ","'${theAna}'",20221)'

  root -l -q -b makeSSWWDataCards.C'(0,0,"anaZ","'${theAna}'",20230)'
  root -l -q -b makeSSWWDataCards.C'(0,1,"anaZ","'${theAna}'",20230)'

  root -l -q -b makeSSWWDataCards.C'(0,0,"anaZ","'${theAna}'",20231)'
  root -l -q -b makeSSWWDataCards.C'(0,1,"anaZ","'${theAna}'",20231)'

elif [ $theOption -eq 1 ]; then
  export theAna=wzAnalysis$1

  root -l -q -b makeSSWWDataCards.C'(0,0,"anaZ","'${theAna}'",20220)'
  root -l -q -b makeSSWWDataCards.C'(0,1,"anaZ","'${theAna}'",20220)'

  root -l -q -b makeSSWWDataCards.C'(0,0,"anaZ","'${theAna}'",20221)'
  root -l -q -b makeSSWWDataCards.C'(0,1,"anaZ","'${theAna}'",20221)'

  root -l -q -b makeSSWWDataCards.C'(0,0,"anaZ","'${theAna}'",20230)'
  root -l -q -b makeSSWWDataCards.C'(0,1,"anaZ","'${theAna}'",20230)'

  root -l -q -b makeSSWWDataCards.C'(0,0,"anaZ","'${theAna}'",20231)'
  root -l -q -b makeSSWWDataCards.C'(0,1,"anaZ","'${theAna}'",20231)'

fi

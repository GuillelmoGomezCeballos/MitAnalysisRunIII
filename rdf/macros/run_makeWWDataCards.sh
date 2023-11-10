#!/bin/sh

if [ $# -lt 2 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

export theAna=wwAnalysis$1
export theOption=$2

if [ $theOption -eq 0 ]; then

  root -l -q -b makeWWDataCards.C'(0,1,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(0,2,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(0,3,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(0,4,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(0,1,"anaZ","'${theAna}'",20221,0)'
  root -l -q -b makeWWDataCards.C'(0,2,"anaZ","'${theAna}'",20221,0)'
  root -l -q -b makeWWDataCards.C'(0,3,"anaZ","'${theAna}'",20221,0)'
  root -l -q -b makeWWDataCards.C'(0,4,"anaZ","'${theAna}'",20221,0)'

  root -l -q -b makeWWDataCards.C'(0,1,"anaZ","'${theAna}'",20220,1)'
  root -l -q -b makeWWDataCards.C'(0,2,"anaZ","'${theAna}'",20220,1)'
  root -l -q -b makeWWDataCards.C'(0,3,"anaZ","'${theAna}'",20220,1)'
  root -l -q -b makeWWDataCards.C'(0,4,"anaZ","'${theAna}'",20220,1)'
  root -l -q -b makeWWDataCards.C'(0,1,"anaZ","'${theAna}'",20221,1)'
  root -l -q -b makeWWDataCards.C'(0,2,"anaZ","'${theAna}'",20221,1)'
  root -l -q -b makeWWDataCards.C'(0,3,"anaZ","'${theAna}'",20221,1)'
  root -l -q -b makeWWDataCards.C'(0,4,"anaZ","'${theAna}'",20221,1)'

elif [ $theOption -eq 1 ]; then

  root -l -q -b makeWWDataCards.C'(1,1,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(1,2,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(1,3,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(1,1,"anaZ","'${theAna}'",20221,0)'
  root -l -q -b makeWWDataCards.C'(1,2,"anaZ","'${theAna}'",20221,0)'
  root -l -q -b makeWWDataCards.C'(1,3,"anaZ","'${theAna}'",20221,0)'

fi

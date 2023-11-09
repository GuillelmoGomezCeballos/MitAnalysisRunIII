#!/bin/sh

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

export theAna=wwAnalysis$1

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

#!/bin/sh

if [ $# -lt 2 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

export theOption=$2

export mergingHist=1
if [ $# -eq 3 ]; then
   export mergingHist=$3
fi

if [ $theOption -eq 0 ]; then

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

  export theAna=wzAnalysis$1
  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",20221,0)'

  export theAna=zzAnalysis$1
  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",20221,0)'

elif [ $theOption -eq 1 ]; then

  export theAna=wwAnalysis$1

  root -l -q -b makeWWDataCards.C'(1,1,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(1,2,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(1,3,"anaZ","'${theAna}'",20220,0)'
  root -l -q -b makeWWDataCards.C'(1,1,"anaZ","'${theAna}'",20221,0)'
  root -l -q -b makeWWDataCards.C'(1,2,"anaZ","'${theAna}'",20221,0)'
  root -l -q -b makeWWDataCards.C'(1,3,"anaZ","'${theAna}'",20221,0)'

elif [ $theOption -eq 2 ]; then

  export theAna=wzAnalysis$1
  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",20220,1)'
  root -l -q -b makeVVDataCards.C'(0,1,"anaZ","'${theAna}'",20220,1)'
  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",20221,1)'
  root -l -q -b makeVVDataCards.C'(0,1,"anaZ","'${theAna}'",20221,1)'

  export theAna=zzAnalysis$1
  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",20220,1)'
  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",20221,1)'

elif [ $theOption -eq 10 ]; then

  theYear=2022;

  # WW
  export theAna=wwAnalysis$1
  if [ $mergingHist -eq 1 ]; then
    hadd -f anaZ/fillhisto_${theAna}_${theYear}_nonprompt.root anaZ/fillhisto_${theAna}_${theYear}0_nonprompt.root anaZ/fillhisto_${theAna}_${theYear}1_nonprompt.root
    for i in `seq 0 1000`;
    do
      if [[ -f anaZ/fillhisto_${theAna}_${theYear}0_${i}_mva.root ]]; then

      hadd -f anaZ/fillhisto_${theAna}_${theYear}_${i}_mva.root anaZ/fillhisto_${theAna}_${theYear}0_${i}_mva.root anaZ/fillhisto_${theAna}_${theYear}1_${i}_mva.root

      fi
    done
  fi

  root -l -q -b makeWWDataCards.C'(0,1,"anaZ","'${theAna}'",2022,0)'
  root -l -q -b makeWWDataCards.C'(0,2,"anaZ","'${theAna}'",2022,0)'
  root -l -q -b makeWWDataCards.C'(0,3,"anaZ","'${theAna}'",2022,0)'
  root -l -q -b makeWWDataCards.C'(0,4,"anaZ","'${theAna}'",2022,0)'

  root -l -q -b makeWWDataCards.C'(0,1,"anaZ","'${theAna}'",2022,1)'
  root -l -q -b makeWWDataCards.C'(0,2,"anaZ","'${theAna}'",2022,1)'
  root -l -q -b makeWWDataCards.C'(0,3,"anaZ","'${theAna}'",2022,1)'
  root -l -q -b makeWWDataCards.C'(0,4,"anaZ","'${theAna}'",2022,1)'

  # WZ
  export theAna=wzAnalysis$1
  if [ $mergingHist -eq 1 ]; then
    hadd -f anaZ/fillhisto_${theAna}_${theYear}_nonprompt.root anaZ/fillhisto_${theAna}_${theYear}0_nonprompt.root anaZ/fillhisto_${theAna}_${theYear}1_nonprompt.root
    for i in `seq 300 700`;
    do
      if [[ -f anaZ/fillhisto_${theAna}_${theYear}0_${i}.root ]]; then

      hadd -f anaZ/fillhisto_${theAna}_${theYear}_${i}.root anaZ/fillhisto_${theAna}_${theYear}0_${i}.root anaZ/fillhisto_${theAna}_${theYear}1_${i}.root

      fi
    done
  fi

  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",2022,0)'

  # ZZ
  export theAna=zzAnalysis$1
  if [ $mergingHist -eq 1 ]; then
    for i in `seq 300 700`;
    do
      if [[ -f anaZ/fillhisto_${theAna}_${theYear}0_${i}.root ]]; then

      hadd -f anaZ/fillhisto_${theAna}_${theYear}_${i}.root anaZ/fillhisto_${theAna}_${theYear}0_${i}.root anaZ/fillhisto_${theAna}_${theYear}1_${i}.root

      fi
    done
  fi

  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",2022,0)'

elif [ $theOption -eq 11 ]; then

  theYear=2022;

  # WW
  export theAna=wwAnalysis$1
  if [ $mergingHist -eq 1 ]; then
    hadd -f anaZ/fillhisto_${theAna}_${theYear}_nonprompt.root anaZ/fillhisto_${theAna}_${theYear}0_nonprompt.root anaZ/fillhisto_${theAna}_${theYear}1_nonprompt.root
    for i in `seq 1000 1600`;
    do
      if [[ -f anaZ/fillhisto_${theAna}_${theYear}0_${i}_mva.root ]]; then

      hadd -f anaZ/fillhisto_${theAna}_${theYear}_${i}_mva.root anaZ/fillhisto_${theAna}_${theYear}0_${i}_mva.root anaZ/fillhisto_${theAna}_${theYear}1_${i}_mva.root

      fi
    done
  fi

  root -l -q -b makeWWDataCards.C'(1,1,"anaZ","'${theAna}'",2022,0)'
  root -l -q -b makeWWDataCards.C'(1,2,"anaZ","'${theAna}'",2022,0)'
  root -l -q -b makeWWDataCards.C'(1,3,"anaZ","'${theAna}'",2022,0)'

elif [ $theOption -eq 12 ]; then

  theYear=2022;

  # WZ
  export theAna=wzAnalysis$1
  if [ $mergingHist -eq 1 ]; then
    hadd -f anaZ/fillhisto_${theAna}_${theYear}_nonprompt.root anaZ/fillhisto_${theAna}_${theYear}0_nonprompt.root anaZ/fillhisto_${theAna}_${theYear}1_nonprompt.root
    for i in `seq 300 700`;
    do
      if [[ -f anaZ/fillhisto_${theAna}_${theYear}0_${i}.root ]]; then

      hadd -f anaZ/fillhisto_${theAna}_${theYear}_${i}.root anaZ/fillhisto_${theAna}_${theYear}0_${i}.root anaZ/fillhisto_${theAna}_${theYear}1_${i}.root

      fi
    done
  fi

  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",2022,1)'
  root -l -q -b makeVVDataCards.C'(0,1,"anaZ","'${theAna}'",2022,1)'

  # ZZ
  export theAna=zzAnalysis$1
  if [ $mergingHist -eq 1 ]; then
    for i in `seq 300 700`;
    do
      if [[ -f anaZ/fillhisto_${theAna}_${theYear}0_${i}.root ]]; then

      hadd -f anaZ/fillhisto_${theAna}_${theYear}_${i}.root anaZ/fillhisto_${theAna}_${theYear}0_${i}.root anaZ/fillhisto_${theAna}_${theYear}1_${i}.root

      fi
    done
  fi

  root -l -q -b makeVVDataCards.C'(0,0,"anaZ","'${theAna}'",2022,1)'

fi

#!/bin/sh

if [ $# -lt 2 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

export theOption=$2

if [ $theOption -eq 0 ]; then

  export theAna=sswwAnalysis$1

  for year in 20220 20221 20230 20231 20240;
  #for year in 2022 2023 20240;
  do

  #for bin in 0 1 2 3 4 5;
  for bin in 0 1;
  do

  root -l -q -b makeSSWWDataCards.C'(0,'${bin}',"anaZ","'${theAna}'",'${year}')';

  done
  done

elif [ $theOption -eq 1 ]; then
  export theAna=wzAnalysis$1

  for year in 20220 20221 20230 20231 20240;
  #for year in 2022 2023 20240;
  do

  for bin in 0 1;
  do

  root -l -q -b makeSSWWDataCards.C'(0,'${bin}',"anaZ","'${theAna}'",'${year}')';

  done
  done

elif [ $theOption -eq 2 ]; then
  export theAna=zzAnalysis$1

  for year in 20220 20221 20230 20231 20240;
  #for year in 2022 2023 20240;
  do

  for bin in 0;
  do

  root -l -q -b makeSSWWDataCards.C'(0,'${bin}',"anaZ","'${theAna}'",'${year}')';

  done
  done


elif [ $theOption -eq 10 ]; then

  for ana in sswwAnalysis$1 wzAnalysis$1 zzAnalysis$1;
  do

  for year in 2022 2023;
  do

  for bin in 0 1;
  do

    if [[ -f output_${ana}_${year}_bin${bin}.root ]]; then

    mv output_${ana}_${year}_bin${bin}.root  output_${ana}_${year}0_bin${bin}.root
    mv datacard_${ana}_${year}_bin${bin}.txt datacard_${ana}_${year}0_bin${bin}.txt
    sed -i 's/output_${ana}_${year}_bin${bin}.root/output_${ana}_${year}0_bin${bin}.root/' datacard_${ana}_${year}0_bin${bin}.txt

    fi

  done
  done
  done

fi

#!/bin/sh

export YEAR=2022
export removePDFFiles=1

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

if [ $# -eq 2 ]; then
   removePDFFiles=$2
fi

export YEAR=$1

rm -f histoFakeEtaPt_fakeAnalysis100?_${YEAR}_anaType?.root;

python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1001 --year=${YEAR} --anaType=1 --isPseudoData=0
python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1001 --year=${YEAR} --anaType=2 --isPseudoData=0
python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1001 --year=${YEAR} --anaType=3 --isPseudoData=0

python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1002 --year=${YEAR} --anaType=1 --isPseudoData=1
python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1002 --year=${YEAR} --anaType=2 --isPseudoData=1
python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1002 --year=${YEAR} --anaType=3 --isPseudoData=1

python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1003 --year=${YEAR} --anaType=1 --isPseudoData=1
python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1003 --year=${YEAR} --anaType=2 --isPseudoData=1
python3 computeFakeRates.py --path=fillhisto_fakeAnalysis1003 --year=${YEAR} --anaType=3 --isPseudoData=1

hadd -f histoFakeEtaPt_${YEAR}.root histoFakeEtaPt_fakeAnalysis100?_${YEAR}_anaType?.root;

if [ ${removePDFFiles} -eq 1 ]; then
  rm -f histoFake*.pdf;
fi

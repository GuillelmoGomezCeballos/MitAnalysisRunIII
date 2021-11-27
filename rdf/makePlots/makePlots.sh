#!/bin/sh

export NSEL=$1;
export APPLYSCALING=$2;
export YEAR=$3;

if [ $NSEL == 'z' ]; then
  export legendBSM="";
  export isNeverBlinded=0;
  export isBlinded=0;
  export fidAnaName="";
  export mlfitResult="";
  export channelName="XXX"; 

  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{ll}","GeV","anaZ/fillhistoZAna_'${YEAR}'_0.root","dy_zsel_massmm",0,'${YEAR}',"'${legendBSM}'",1.0, '${isBlinded}',"",1,"'${APPLYSCALING}'","'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{ll}","GeV","anaZ/fillhistoZAna_'${YEAR}'_1.root","dy_zsel_massem",0,'${YEAR}',"'${legendBSM}'",1.0, '${isBlinded}',"",1,"'${APPLYSCALING}'","'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{ll}","GeV","anaZ/fillhistoZAna_'${YEAR}'_2.root","dy_zsel_massee",0,'${YEAR}',"'${legendBSM}'",1.0, '${isBlinded}',"",1,"'${APPLYSCALING}'","'${mlfitResult}'","'${channelName}'")';

fi

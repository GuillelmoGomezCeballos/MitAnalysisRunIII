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

  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{ll}","GeV","anaZ/fillhistoZAna1001_'${YEAR}'_100.root","dy_zsel_massmm",0,'${YEAR}',"'${legendBSM}'",1.0, '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{ll}","GeV","anaZ/fillhistoZAna1001_'${YEAR}'_103.root","dy_zsel_massem",0,'${YEAR}',"'${legendBSM}'",1.0, '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{ll}","GeV","anaZ/fillhistoZAna1001_'${YEAR}'_114.root","dy_zsel_massee",0,'${YEAR}',"'${legendBSM}'",1.0, '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';

elif [ $NSEL == 'fake' ]; then
  export legendBSM="";
  export isNeverBlinded=0;
  export isBlinded=0;
  export fidAnaName="";
  export mlfitResult="";
  export channelName="XXX"; 

  export SF_DY=0.9;
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_0.root","fakemsel_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_2.root","fakemsel_dphilmet", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_4.root","fakemsel_met", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_6.root","fakemsel_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_8.root","fakemsel_ptloose", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_10.root","fakemsel_etaloose", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_12.root","fakemsel_pttight", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_14.root","fakemsel_etatight", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_16.root","fakemsel_sel0_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_18.root","fakemsel_sel1_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_20.root","fakemsel_sel2_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_22.root","fakemsel_sel3_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_24.root","fakemsel_sel4_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_26.root","fakemsel_sel5_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_28.root","fakemsel_sel0_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_30.root","fakemsel_sel1_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_32.root","fakemsel_sel2_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_34.root","fakemsel_sel3_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_36.root","fakemsel_sel4_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_38.root","fakemsel_sel5_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_40.root","fakemsel_ptl", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';

  export SF_DY=0.8;
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_1.root","fakeesel_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_3.root","fakeesel_dphilmet", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_5.root","fakeesel_met", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_7.root","fakeesel_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_9.root","fakeesel_ptloose", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_11.root","fakeesel_etaloose", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_13.root","fakeesel_pttight", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_15.root","fakeesel_etatight", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_17.root","fakeesel_sel0_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_19.root","fakeesel_sel1_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_21.root","fakeesel_sel2_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_23.root","fakeesel_sel3_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_25.root","fakeesel_sel4_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_27.root","fakeesel_sel5_mt_fix", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_29.root","fakeesel_sel0_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_31.root","fakeesel_sel1_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_33.root","fakeesel_sel2_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_35.root","fakeesel_sel3_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_37.root","fakeesel_sel4_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_39.root","fakeesel_sel5_mt", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","GeV","anaZ/fillhistoFakeAna1001_'${YEAR}'_41.root","fakeesel_ptl", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';

fi

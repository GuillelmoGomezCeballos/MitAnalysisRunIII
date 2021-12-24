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

  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"MVA","","anaZ/fillhistoZAna1001_'${YEAR}'_130.root","dy_zsel_tthmvam",0,'${YEAR}',"'${legendBSM}'",1.0, '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"MVA","","anaZ/fillhistoZAna1001_'${YEAR}'_131.root","dy_zsel_tthmvae",0,'${YEAR}',"'${legendBSM}'",1.0, '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';

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

elif [ $NSEL == 'wz' ]; then
  export legendBSM="";
  export isNeverBlinded=0;
  export isBlinded=0;
  export fidAnaName="";
  export mlfitResult="";
  export channelName="XXX"; 
  export SF_DY=1;
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Min(m_{ll})","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_0.root","wzsel_mllmin", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"|m_{ll}-m_{Z}|","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_1.root","wzsel_mllz", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{3l}","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_2.root","wzsel_m3l", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"p_{T}^{l-W}","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_3.root","wzsel_ptlw", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Max Btag jet","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_4.root","wzsel_nbtagjet", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Leading p_{T}^{l-Z}","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_5.root","wzsel_ptlz1", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Trailing p_{T}^{l-Z}","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_6.root","wzsel_ptlz2", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{T}^{W}","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_7.root","wzsel_mtw", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Lepton type","","anaZ/fillhistoWZAna1001_'${YEAR}'_8.root","wzsel_ltype", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"N_{jets}","","anaZ/fillhistoWZAna1001_'${YEAR}'_9.root","wzsel_njets", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
 root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"p_{T}^{miss}","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_10.root","wzsel_ptmiss", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{T}^{W}","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_11.root","wzbsel_mtw", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Lepton type","","anaZ/fillhistoWZAna1001_'${YEAR}'_12.root","wzbsel_ltype", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"N_{jets}","","anaZ/fillhistoWZAna1001_'${YEAR}'_13.root","wzbsel_njets", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
 root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"p_{T}^{miss}","GeV","anaZ/fillhistoWZAna1001_'${YEAR}'_14.root","wzbsel_ptmiss", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';

elif [ $NSEL == 'zz' ]; then
  export legendBSM="";
  export isNeverBlinded=0;
  export isBlinded=0;
  export fidAnaName="";
  export mlfitResult="";
  export channelName="XXX"; 
  export SF_DY=1;
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Min(m_{ll})","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_0.root","zzsel_mllmin", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"|m_{ll}-m_{Z1}|","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_1.root","zzsel_mllz1", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"|m_{ll}-m_{Z2}|","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_2.root","zzsel_mllz2", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Leading p_{T}^{l-Z1}","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_3.root","zzsel_ptlz11", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Trailing p_{T}^{l-Z1}","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_4.root","zzsel_ptlz12", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Leading p_{T}^{l-Z1}","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_5.root","zzsel_ptlz21", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Trailing p_{T}^{l-Z1}","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_6.root","zzsel_ptlz22", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{T}^{W}","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_7.root","zzsel_m4l", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Lepton type","","anaZ/fillhistoZZAna1001_'${YEAR}'_8.root","zzsel_ltype", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"N_{jets}","","anaZ/fillhistoZZAna1001_'${YEAR}'_9.root","zzsel_njets", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
 root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"p_{T}^{miss}","GeV","anaZ/fillhistoZZAna1001_'${YEAR}'_10.root","zzsel_ptmiss", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';

elif [ $NSEL == 'met' ]; then
  export legendBSM="";
  export isNeverBlinded=0;
  export isBlinded=0;
  export fidAnaName="";
  export mlfitResult="";
  export channelName="XXX"; 
  export SF_DY=1;

  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Min(m_{ll})","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_0.root","metsel0_mtot", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Min(m_{ll})","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_1.root","metsel1_mtot", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Min(m_{ll})","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_2.root","metsel2_mtot", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Min(m_{ll})","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_3.root","metsel3_mtot", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Min(m_{ll})","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_4.root","metsel4_mtot", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"Min(m_{ll})","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_5.root","metsel5_mtot", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';

  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{tot}","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_6.root","metsel0_mllmin", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{tot}","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_7.root","metsel1_mllmin", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{tot}","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_8.root","metsel2_mllmin", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{tot}","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_9.root","metsel3_mllmin", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{tot}","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_10.root","metsel4_mllmin", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';
  root -q -b -l MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"m_{tot}","GeV","anaZ/fillhistoMETAna1001_'${YEAR}'_11.root","metsel5_mllmin", 0,'${YEAR}',"'${legendBSM}'",'${SF_DY}', '${isBlinded}',"",1,'${APPLYSCALING}',"'${mlfitResult}'","'${channelName}'")';

fi

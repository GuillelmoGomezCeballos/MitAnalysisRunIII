#include <TROOT.h>
#include <TFile.h>
#include <TSystem.h>
#include <TString.h>
#include "TLorentzVector.h"

#include "finalPlot.C"

void makeAllPlots(TString nsel, int applyScaling, int year, int whichCondorJob = 1001){
  TString legendBSM="";
  int isNeverBlinded=0;
  int isBlinded=0;
  TString fidAnaName="";
  TString mlfitResult="";
  TString channelName="XXX"; 
  double SF_DY=1.0;
  if(nsel.Contains(".root") == true){
    finalPlot(0,1,"NPV","",Form("%s",nsel.Data()),"variable",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "z"){
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_0.root",whichCondorJob,year),"dy_zsel_massmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_1.root",whichCondorJob,year),"dy_zsel_massem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_2.root",whichCondorJob,year),"dy_zsel_massee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}^{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_3.root",whichCondorJob,year),"dy_zsel_ptllmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_4.root",whichCondorJob,year),"dy_zsel_ptllem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_5.root",whichCondorJob,year),"dy_zsel_ptllee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#Delta R_{ll}","",Form("anaZ/fillhisto_zAnalysis%d_%d_6.root",whichCondorJob,year),"dy_zsel_drllmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta R_{ll}","",Form("anaZ/fillhisto_zAnalysis%d_%d_7.root",whichCondorJob,year),"dy_zsel_drllem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta R_{ll}","",Form("anaZ/fillhisto_zAnalysis%d_%d_8.root",whichCondorJob,year),"dy_zsel_drllee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#Delta #phi_{ll}","",Form("anaZ/fillhisto_zAnalysis%d_%d_9.root",whichCondorJob,year),"dy_zsel_dphillmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta #phi_{ll}","",Form("anaZ/fillhisto_zAnalysis%d_%d_10.root",whichCondorJob,year),"dy_zsel_dphillem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta #phi_{ll}","",Form("anaZ/fillhisto_zAnalysis%d_%d_11.root",whichCondorJob,year),"dy_zsel_dphillee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}^{l1}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_12.root",whichCondorJob,year),"dy_zsel_ptl1mm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l1}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_13.root",whichCondorJob,year),"dy_zsel_ptl1em",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l1}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_14.root",whichCondorJob,year),"dy_zsel_ptl1ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}^{l2}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_15.root",whichCondorJob,year),"dy_zsel_ptl2mm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l2}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_16.root",whichCondorJob,year),"dy_zsel_ptl2em",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l2}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_17.root",whichCondorJob,year),"dy_zsel_ptl2ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#eta_{T}^{l1}","",Form("anaZ/fillhisto_zAnalysis%d_%d_18.root",whichCondorJob,year),"dy_zsel_etal1mm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{l1}","",Form("anaZ/fillhisto_zAnalysis%d_%d_19.root",whichCondorJob,year),"dy_zsel_etal1em",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{l1}","",Form("anaZ/fillhisto_zAnalysis%d_%d_20.root",whichCondorJob,year),"dy_zsel_etal1ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#eta_{T}^{l2}","",Form("anaZ/fillhisto_zAnalysis%d_%d_21.root",whichCondorJob,year),"dy_zsel_etal2mm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{l2}","",Form("anaZ/fillhisto_zAnalysis%d_%d_22.root",whichCondorJob,year),"dy_zsel_etal2em",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{l2}","",Form("anaZ/fillhisto_zAnalysis%d_%d_23.root",whichCondorJob,year),"dy_zsel_etal2ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"N_{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_24.root",whichCondorJob,year),"dy_zsel_njetsmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_25.root",whichCondorJob,year),"dy_zsel_njetsem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_26.root",whichCondorJob,year),"dy_zsel_njetsee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"N_{bj}","",Form("anaZ/fillhisto_zAnalysis%d_%d_27.root",whichCondorJob,year),"dy_zsel_nbjetsmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{bj}","",Form("anaZ/fillhisto_zAnalysis%d_%d_28.root",whichCondorJob,year),"dy_zsel_nbjetsem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{bj}","",Form("anaZ/fillhisto_zAnalysis%d_%d_29.root",whichCondorJob,year),"dy_zsel_nbjetsee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"NPV","",Form("anaZ/fillhisto_zAnalysis%d_%d_30.root",whichCondorJob,year),"dy_zsel_npvmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"NPV","",Form("anaZ/fillhisto_zAnalysis%d_%d_31.root",whichCondorJob,year),"dy_zsel_npvem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"NPV","",Form("anaZ/fillhisto_zAnalysis%d_%d_32.root",whichCondorJob,year),"dy_zsel_npvee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Calo p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_33.root",whichCondorJob,year),"dy_zsel_calometmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Calo p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_34.root",whichCondorJob,year),"dy_zsel_calometem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Calo p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_35.root",whichCondorJob,year),"dy_zsel_calometee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"CHS p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_36.root",whichCondorJob,year),"dy_zsel_chsmetmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"CHS p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_37.root",whichCondorJob,year),"dy_zsel_chsmetem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"CHS p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_38.root",whichCondorJob,year),"dy_zsel_chsmetee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_39.root",whichCondorJob,year),"dy_zsel_metmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_40.root",whichCondorJob,year),"dy_zsel_metem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_41.root",whichCondorJob,year),"dy_zsel_metee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"PUPPI p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_42.root",whichCondorJob,year),"dy_zsel_puppimetmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"PUPPI p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_43.root",whichCondorJob,year),"dy_zsel_puppimetem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"PUPPI p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_44.root",whichCondorJob,year),"dy_zsel_puppimetee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"TRK p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_45.root",whichCondorJob,year),"dy_zsel_trkmetmm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"TRK p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_46.root",whichCondorJob,year),"dy_zsel_trkmetem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"TRK p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_47.root",whichCondorJob,year),"dy_zsel_trkmetee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#rho","",Form("anaZ/fillhisto_zAnalysis%d_%d_48.root",whichCondorJob,year),"dy_zsel_rhomm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#rho","",Form("anaZ/fillhisto_zAnalysis%d_%d_49.root",whichCondorJob,year),"dy_zsel_rhoem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#rho","",Form("anaZ/fillhisto_zAnalysis%d_%d_50.root",whichCondorJob,year),"dy_zsel_rhoee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ee}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_58.root",whichCondorJob,year),"dy_tighteesel_os_mass",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ee}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_59.root",whichCondorJob,year),"dy_tighteesel_ss_mass",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Btag","",Form("anaZ/fillhisto_zAnalysis%d_%d_110.root",whichCondorJob,year),"dy_1jsel_btagDeepBll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Btag","",Form("anaZ/fillhisto_zAnalysis%d_%d_111.root",whichCondorJob,year),"dy_1jsel_btagDeepBem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"N_{bj}","",Form("anaZ/fillhisto_zAnalysis%d_%d_112.root",whichCondorJob,year),"dy_1jsel_nbjetsll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{bj}","",Form("anaZ/fillhisto_zAnalysis%d_%d_113.root",whichCondorJob,year),"dy_1jsel_nbjetsem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}^{j}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_114.root",whichCondorJob,year),"dy_1jsel_ptjll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{j}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_115.root",whichCondorJob,year),"dy_1jsel_ptjem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#eta_{T}^{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_116.root",whichCondorJob,year),"dy_1jsel_etajll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_117.root",whichCondorJob,year),"dy_1jsel_etajem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#Delta #phi_{ll}","",Form("anaZ/fillhisto_zAnalysis%d_%d_118.root",whichCondorJob,year),"dy_1jsel_dphill",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta #phi_{ll}","",Form("anaZ/fillhisto_zAnalysis%d_%d_119.root",whichCondorJob,year),"dy_1jsel_dphiem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"PUPPI p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_120.root",whichCondorJob,year),"dy_1jsel_puppimetll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"PUPPI p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_121.root",whichCondorJob,year),"dy_1jsel_puppimetem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}^{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_122.root",whichCondorJob,year),"dy_1jsel_ptllll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_123.root",whichCondorJob,year),"dy_1jsel_ptllem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#eta_{T}^{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_124.root",whichCondorJob,year),"dy_sel_ptj30_etajallll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_125.root",whichCondorJob,year),"dy_sel_ptj30_etajallem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_126.root",whichCondorJob,year),"dy_sel_ptj50_etajallll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{j}","",Form("anaZ/fillhisto_zAnalysis%d_%d_127.root",whichCondorJob,year),"dy_sel_ptj50_etajallem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{llg}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_154.root",whichCondorJob,year),"dy_mmmg",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{llg}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_155.root",whichCondorJob,year),"dy_memg",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{llg}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_156.root",whichCondorJob,year),"dy_meeg",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{#gamma}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_157.root",whichCondorJob,year),"dy_mmg_ptg",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{#gamma}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_158.root",whichCondorJob,year),"dy_emg_ptg",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{#gamma}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_159.root",whichCondorJob,year),"dy_eeg_ptg",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Neutral electromagnetic energy fraction","",Form("anaZ/fillhisto_zAnalysis%d_%d_128.root",whichCondorJob,year),"dy_1jsel_prob_neEmEFll",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Neutral electromagnetic energy fraction","",Form("anaZ/fillhisto_zAnalysis%d_%d_129.root",whichCondorJob,year),"dy_1jsel_prob_neEmEFem",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Neutral hadronic energy fraction","",Form("anaZ/fillhisto_zAnalysis%d_%d_160.root",whichCondorJob,year),"dy_1jsel_prob_neHEFll",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Neutral hadronic energy fraction","",Form("anaZ/fillhisto_zAnalysis%d_%d_161.root",whichCondorJob,year),"dy_1jsel_prob_neHEFem",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Charged energy fraction","",Form("anaZ/fillhisto_zAnalysis%d_%d_162.root",whichCondorJob,year),"dy_1jsel_prob_chEFll",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Charged energy fraction","",Form("anaZ/fillhisto_zAnalysis%d_%d_163.root",whichCondorJob,year),"dy_1jsel_prob_chEFem",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_164.root",whichCondorJob,year),"dy_2jsel_mjjll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_165.root",whichCondorJob,year),"dy_2jsel_mjjem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}^{jj}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_166.root",whichCondorJob,year),"dy_2jsel_ptjjll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{jj}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_167.root",whichCondorJob,year),"dy_2jsel_ptjjem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"#Delta #phi_{jj}","",Form("anaZ/fillhisto_zAnalysis%d_%d_168.root",whichCondorJob,year),"dy_2jsel_dphijjll",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta #phi_{jj}","",Form("anaZ/fillhisto_zAnalysis%d_%d_169.root",whichCondorJob,year),"dy_2jsel_dphijjem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_179.root",whichCondorJob,year),"dy_zsel_massmm_trig0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_180.root",whichCondorJob,year),"dy_zsel_massem_trig0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_181.root",whichCondorJob,year),"dy_zsel_massee_trig0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_182.root",whichCondorJob,year),"dy_zsel_massmm_trig1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_183.root",whichCondorJob,year),"dy_zsel_massem_trig1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_184.root",whichCondorJob,year),"dy_zsel_massee_trig1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_185.root",whichCondorJob,year),"dy_zsel_massmm_trig2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_186.root",whichCondorJob,year),"dy_zsel_massem_trig2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_187.root",whichCondorJob,year),"dy_zsel_massee_trig2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_188.root",whichCondorJob,year),"dy_zsel_massmm_trig3",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_189.root",whichCondorJob,year),"dy_zsel_massem_trig3",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_190.root",whichCondorJob,year),"dy_zsel_massee_trig3",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_191.root",whichCondorJob,year),"dy_zsel_massmm_trig4",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_192.root",whichCondorJob,year),"dy_zsel_massem_trig4",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_193.root",whichCondorJob,year),"dy_zsel_massee_trig4",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_194.root",whichCondorJob,year),"dy_zsel_massmm_trig5",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_195.root",whichCondorJob,year),"dy_zsel_massem_trig5",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_196.root",whichCondorJob,year),"dy_zsel_massee_trig5",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_197.root",whichCondorJob,year),"dy_zsel_massmm_trig6",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_198.root",whichCondorJob,year),"dy_zsel_massem_trig6",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_199.root",whichCondorJob,year),"dy_zsel_massee_trig6",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_200.root",whichCondorJob,year),"dy_zsel_massmm_trig7",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_201.root",whichCondorJob,year),"dy_zsel_massem_trig7",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_202.root",whichCondorJob,year),"dy_zsel_massee_trig7",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_203.root",whichCondorJob,year),"dy_zsel_massmm_trig8",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_204.root",whichCondorJob,year),"dy_zsel_massem_trig8",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_205.root",whichCondorJob,year),"dy_zsel_massee_trig8",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_206.root",whichCondorJob,year),"dy_zme_pttag",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_207.root",whichCondorJob,year),"dy_zem_pttag",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_208.root",whichCondorJob,year),"dy_zme_pttag_trig",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_209.root",whichCondorJob,year),"dy_zem_pttag_trig",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_210.root",whichCondorJob,year),"dy_zme_ptprobe",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_211.root",whichCondorJob,year),"dy_zem_ptprobe",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_212.root",whichCondorJob,year),"dy_zme_ptprobe_trigem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_213.root",whichCondorJob,year),"dy_zem_ptprobe_trigem",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_214.root",whichCondorJob,year),"dy_zme_ptprobe_trigse",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_215.root",whichCondorJob,year),"dy_zem_ptprobe_trigsm",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_240.root",whichCondorJob,year),"dy_zsel_massmm_bb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_241.root",whichCondorJob,year),"dy_zsel_massmm_eb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_242.root",whichCondorJob,year),"dy_zsel_massmm_ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_243.root",whichCondorJob,year),"dy_zsel_massmmdef_bb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_244.root",whichCondorJob,year),"dy_zsel_massmmdef_eb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_245.root",whichCondorJob,year),"dy_zsel_massmmdef_ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_246.root",whichCondorJob,year),"dy_zsel_massmmup_bb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_247.root",whichCondorJob,year),"dy_zsel_massmmup_eb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_248.root",whichCondorJob,year),"dy_zsel_massmmup_ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_249.root",whichCondorJob,year),"dy_zsel_massmmdown_bb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_250.root",whichCondorJob,year),"dy_zsel_massmmdown_eb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_251.root",whichCondorJob,year),"dy_zsel_massmmdown_ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_252.root",whichCondorJob,year),"dy_zsel_massee_bb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_253.root",whichCondorJob,year),"dy_zsel_massee_eb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_254.root",whichCondorJob,year),"dy_zsel_massee_ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_255.root",whichCondorJob,year),"dy_zsel_masseedef_bb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_256.root",whichCondorJob,year),"dy_zsel_masseedef_eb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_257.root",whichCondorJob,year),"dy_zsel_masseedef_ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_258.root",whichCondorJob,year),"dy_zsel_masseeup_bb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_259.root",whichCondorJob,year),"dy_zsel_masseeup_eb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_260.root",whichCondorJob,year),"dy_zsel_masseeup_ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_261.root",whichCondorJob,year),"dy_zsel_masseedown_bb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_262.root",whichCondorJob,year),"dy_zsel_masseedown_eb",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_263.root",whichCondorJob,year),"dy_zsel_masseedown_ee",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "ztrigger"){
    TString legendLL="";
    for(int ltype=0; ltype<3; ltype++){
      if     (ltype == 0) legendLL="mm";
      else if(ltype == 1) legendLL="em";
      else if(ltype == 2) legendLL="ee";
      finalPlot(0,1,"p_{T}^{lmin}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_%d.root",whichCondorJob,year,ltype+297),Form("dy_z%strg_ptmin%d",legendLL.Data(),ltype),0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
      for(int nTrg=0; nTrg<18; nTrg++){
         finalPlot(0,1,"p_{T}^{lmin}","GeV",Form("anaZ/fillhisto_zAnalysis%d_%d_%d.root",whichCondorJob,year,3*nTrg+ltype+300),Form("dy_z%strg_ptmin%d",legendLL.Data(),3*nTrg+ltype+300),0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
      }
    }
  }
  else if(nsel == "trigger"){
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_0.root",whichCondorJob,year),"dy_triggersel_os_mll_mm0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_1.root",whichCondorJob,year),"dy_triggersel_os_mll_mm1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_2.root",whichCondorJob,year),"dy_triggersel_os_mll_ee0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_3.root",whichCondorJob,year),"dy_triggersel_os_mll_ee1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_4.root",whichCondorJob,year),"dy_triggersel_ss_mll_mm0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_5.root",whichCondorJob,year),"dy_triggersel_ss_mll_mm1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_6.root",whichCondorJob,year),"dy_triggersel_ss_mll_ee0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_7.root",whichCondorJob,year),"dy_triggersel_ss_mll_ee1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_8.root",whichCondorJob,year), "dy_triggersel_os_ptprobe_mm0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_9.root",whichCondorJob,year), "dy_triggersel_os_ptprobe_mm1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_10.root",whichCondorJob,year),"dy_triggersel_os_ptprobe_ee0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_11.root",whichCondorJob,year),"dy_triggersel_os_ptprobe_ee1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"p_{T}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_12.root",whichCondorJob,year),"dy_triggersel_tight_os_ptprobe_mm0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_13.root",whichCondorJob,year),"dy_triggersel_tight_os_ptprobe_mm1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_14.root",whichCondorJob,year),"dy_triggersel_tight_os_ptprobe_ee0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_15.root",whichCondorJob,year),"dy_triggersel_tight_os_ptprobe_ee1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_16.root",whichCondorJob,year),"dy_triggersel_os_mll_mm0_pt0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_17.root",whichCondorJob,year),"dy_triggersel_os_mll_mm1_pt0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_18.root",whichCondorJob,year),"dy_triggersel_os_mll_ee0_pt0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_19.root",whichCondorJob,year),"dy_triggersel_os_mll_ee1_pt0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_20.root",whichCondorJob,year),"dy_triggersel_os_mll_mm0_pt1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_21.root",whichCondorJob,year),"dy_triggersel_os_mll_mm1_pt1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_22.root",whichCondorJob,year),"dy_triggersel_os_mll_ee0_pt1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_23.root",whichCondorJob,year),"dy_triggersel_os_mll_ee1_pt1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_24.root",whichCondorJob,year),"dy_triggersel_os_mll_mm0_pt2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_25.root",whichCondorJob,year),"dy_triggersel_os_mll_mm1_pt2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_26.root",whichCondorJob,year),"dy_triggersel_os_mll_ee0_pt2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_27.root",whichCondorJob,year),"dy_triggersel_os_mll_ee1_pt2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_28.root",whichCondorJob,year),"dy_triggersel_os_mll_mm0_pt3",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_29.root",whichCondorJob,year),"dy_triggersel_os_mll_mm1_pt3",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_30.root",whichCondorJob,year),"dy_triggersel_os_mll_ee0_pt3",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_31.root",whichCondorJob,year),"dy_triggersel_os_mll_ee1_pt3",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_32.root",whichCondorJob,year),"dy_triggersel_os_mll_mm0_ptup",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_33.root",whichCondorJob,year),"dy_triggersel_os_mll_mm1_ptup",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_34.root",whichCondorJob,year),"dy_triggersel_os_mll_ee0_ptup",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_35.root",whichCondorJob,year),"dy_triggersel_os_mll_ee1_ptup",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_36.root",whichCondorJob,year),"dy_triggersel_os_mll_mm0_ptdown",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_37.root",whichCondorJob,year),"dy_triggersel_os_mll_mm1_ptdown",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_38.root",whichCondorJob,year),"dy_triggersel_os_mll_ee0_ptdown",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_39.root",whichCondorJob,year),"dy_triggersel_os_mll_ee1_ptdown",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_50.root",whichCondorJob,year),"dy_fakesel_mll_mm0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_52.root",whichCondorJob,year),"dy_fakesel_mll_mm1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_54.root",whichCondorJob,year),"dy_fakesel_mll_mm2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_56.root",whichCondorJob,year),"dy_fakesel_triggerslep_mll_mm0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_58.root",whichCondorJob,year),"dy_fakesel_triggerslep_mll_mm1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_60.root",whichCondorJob,year),"dy_fakesel_triggerslep_mll_mm2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_51.root",whichCondorJob,year),"dy_fakesel_mll_ee0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_53.root",whichCondorJob,year),"dy_fakesel_mll_ee1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_55.root",whichCondorJob,year),"dy_fakesel_mll_ee2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_57.root",whichCondorJob,year),"dy_fakesel_triggerslep_mll_ee0",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_59.root",whichCondorJob,year),"dy_fakesel_triggerslep_mll_ee1",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeVBinWidth",Form("anaZ/fillhisto_triggerAnalysis%d_%d_61.root",whichCondorJob,year),"dy_fakesel_triggerslep_mll_ee2",0,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"ttHMVA","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_200.root",whichCondorJob,year),"trigger_zsel_highpt_tthmvam",0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"ttHMVA","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_202.root",whichCondorJob,year),"trigger_zsel_highpt_tthmvae",0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"ttHMVA","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_204.root",whichCondorJob,year),"trigger_zsel_lowpt_tthmvam" ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"ttHMVA","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_206.root",whichCondorJob,year),"trigger_zsel_lowpt_tthmvae" ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"sip3d","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_208.root",whichCondorJob,year),"trigger_zsel_highpt_sip3dm",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"sip3d","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_210.root",whichCondorJob,year),"trigger_zsel_highpt_sip3de",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"sip3d","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_212.root",whichCondorJob,year),"trigger_zsel_lowpt_sip3dm" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"sip3d","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_214.root",whichCondorJob,year),"trigger_zsel_lowpt_sip3de" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"jetRelIso","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_216.root",whichCondorJob,year),"trigger_zsel_highpt_jetRelIsom",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetRelIso","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_218.root",whichCondorJob,year),"trigger_zsel_highpt_jetRelIsoe",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetRelIso","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_220.root",whichCondorJob,year),"trigger_zsel_lowpt_jetRelIsom" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetRelIso","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_222.root",whichCondorJob,year),"trigger_zsel_lowpt_jetRelIsoe" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"dxy","cm",Form("anaZ/fillhisto_triggerAnalysis%d_%d_224.root",whichCondorJob,year),"trigger_zsel_highpt_dxym",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"dxy","cm",Form("anaZ/fillhisto_triggerAnalysis%d_%d_226.root",whichCondorJob,year),"trigger_zsel_highpt_dxye",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"dxy","cm",Form("anaZ/fillhisto_triggerAnalysis%d_%d_228.root",whichCondorJob,year),"trigger_zsel_lowpt_dxym" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"dxy","cm",Form("anaZ/fillhisto_triggerAnalysis%d_%d_230.root",whichCondorJob,year),"trigger_zsel_lowpt_dxye" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"dz","cm",Form("anaZ/fillhisto_triggerAnalysis%d_%d_232.root",whichCondorJob,year),"trigger_zsel_highpt_dzm",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"dz","cm",Form("anaZ/fillhisto_triggerAnalysis%d_%d_234.root",whichCondorJob,year),"trigger_zsel_highpt_dze",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"dz","cm",Form("anaZ/fillhisto_triggerAnalysis%d_%d_236.root",whichCondorJob,year),"trigger_zsel_lowpt_dzm" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"dz","cm",Form("anaZ/fillhisto_triggerAnalysis%d_%d_238.root",whichCondorJob,year),"trigger_zsel_lowpt_dze" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_240.root",whichCondorJob,year),"trigger_zsel_highpt_pfrelisom",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_242.root",whichCondorJob,year),"trigger_zsel_highpt_pfrelisoe",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_244.root",whichCondorJob,year),"trigger_zsel_lowpt_pfrelisom" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_246.root",whichCondorJob,year),"trigger_zsel_lowpt_pfrelisoe" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Mini PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_248.root",whichCondorJob,year),"trigger_zsel_highpt_minipfrelisom",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Mini PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_250.root",whichCondorJob,year),"trigger_zsel_highpt_minipfrelisoe",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Mini PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_252.root",whichCondorJob,year),"trigger_zsel_lowpt_minipfrelisom" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Mini PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_254.root",whichCondorJob,year),"trigger_zsel_lowpt_minipfrelisoe" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Number muon stations","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_256.root",whichCondorJob,year),"trigger_zsel_highpt_muonstationsm",0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"H/E","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_258.root",whichCondorJob,year),"trigger_zsel_highpt_hoee"                          ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Number muon stations","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_260.root",whichCondorJob,year),"trigger_zsel_lowpt_muonstationsm" ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"H/E","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_262.root",whichCondorJob,year),"trigger_zsel_lowpt_hoee"                           ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Number of tracker layers","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_264.root",whichCondorJob,year),"trigger_zsel_highpt_trackinglayersm",0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"R9","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_266.root",whichCondorJob,year),"trigger_highpt_zsel_r9e"                                  ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Number of tracker layers","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_268.root",whichCondorJob,year),"trigger_zsel_lowpt_trackinglayersm" ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"R9","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_270.root",whichCondorJob,year),"trigger_zsel_lowpt_r9e"                                   ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Tracker PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_272.root",whichCondorJob,year),"trigger_zsel_highpt_trkpfrelisom",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Tracker PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_274.root",whichCondorJob,year),"trigger_zsel_highpt_trkpfrelisoe",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Tracker PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_276.root",whichCondorJob,year),"trigger_zsel_lowpt_trkpfrelisom" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Tracker PF isolation/p_{T}","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_278.root",whichCondorJob,year),"trigger_zsel_lowpt_trkpfrelisoe" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Muon MVA ID","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_280.root",whichCondorJob,year),"trigger_zsel_highpt_muonmvaidm",0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"MVA Iso","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_282.root",whichCondorJob,year),"trigger_zsel_highpt_mvaisoe",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Muon MVA ID","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_284.root",whichCondorJob,year),"trigger_zsel_lowpt_muonmvaidm" ,0,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"MVA Iso","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_286.root",whichCondorJob,year),"trigger_zsel_lowpt_mvaisoe" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Muon MVA LowPt ID","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_288.root",whichCondorJob,year),"trigger_zsel_highpt_muonmvalowptm",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} > 30 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"MVA No Iso","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_290.root",whichCondorJob,year),"trigger_zsel_highpt_mvanoisoe",1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} > 30 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Muon MVA LowPt ID","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_292.root",whichCondorJob,year),"trigger_zsel_lowpt_muonmvalowptm" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{#mu} < 25 GeV",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"MVA No Iso","",Form("anaZ/fillhisto_triggerAnalysis%d_%d_294.root",whichCondorJob,year),"trigger_zsel_lowpt_mvanoisoe" ,1,year,legendBSM.Data(),1.0,isBlinded,"p_{T}^{e} < 25 GeV"  ,1,applyScaling,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "fake"){
    legendBSM="";
    isNeverBlinded=0;
    isBlinded=0;
    fidAnaName="";
    mlfitResult="";
    channelName="XXX"; 

    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_24.root",whichCondorJob,year),"faketrgmsel0_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_25.root",whichCondorJob,year),"faketrgmsel1_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_26.root",whichCondorJob,year),"faketrgmsel2_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_27.root",whichCondorJob,year),"faketrgesel0_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_28.root",whichCondorJob,year),"faketrgesel1_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_29.root",whichCondorJob,year),"faketrgesel2_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_30.root",whichCondorJob,year),"faketrgmsel0_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_31.root",whichCondorJob,year),"faketrgmsel1_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_32.root",whichCondorJob,year),"faketrgmsel2_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_33.root",whichCondorJob,year),"faketrgesel0_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_34.root",whichCondorJob,year),"faketrgesel1_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_35.root",whichCondorJob,year),"faketrgesel2_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_36.root",whichCondorJob,year),"faketrgmsel0_mtfix", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_37.root",whichCondorJob,year),"faketrgmsel1_mtfix", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_38.root",whichCondorJob,year),"faketrgmsel2_mtfix", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_39.root",whichCondorJob,year),"faketrgesel0_mtfix", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_40.root",whichCondorJob,year),"faketrgesel1_mtfix", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_41.root",whichCondorJob,year),"faketrgesel2_mtfix", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_42.root",whichCondorJob,year),"faketrgmsel0_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_43.root",whichCondorJob,year),"faketrgmsel1_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_44.root",whichCondorJob,year),"faketrgmsel2_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_45.root",whichCondorJob,year),"faketrgesel0_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_46.root",whichCondorJob,year),"faketrgesel1_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_47.root",whichCondorJob,year),"faketrgesel2_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_48.root",whichCondorJob,year),"faketrgmsel0_etal", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_49.root",whichCondorJob,year),"faketrgmsel1_etal", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_50.root",whichCondorJob,year),"faketrgmsel2_etal", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_51.root",whichCondorJob,year),"faketrgesel0_etal", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_52.root",whichCondorJob,year),"faketrgesel1_etal", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_53.root",whichCondorJob,year),"faketrgesel2_etal", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_54.root",whichCondorJob,year),"faketrgmsel0_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_55.root",whichCondorJob,year),"faketrgmsel1_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_56.root",whichCondorJob,year),"faketrgmsel2_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_57.root",whichCondorJob,year),"faketrgesel0_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_58.root",whichCondorJob,year),"faketrgesel1_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_59.root",whichCondorJob,year),"faketrgesel2_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_60.root",whichCondorJob,year),"faketrgmsel0_mnbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_61.root",whichCondorJob,year),"faketrgmsel1_mnbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_62.root",whichCondorJob,year),"faketrgmsel2_mnbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_63.root",whichCondorJob,year),"faketrgesel0_mnbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_64.root",whichCondorJob,year),"faketrgesel1_mnbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_65.root",whichCondorJob,year),"faketrgesel2_mnbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_66.root",whichCondorJob,year),"faketrgmsel0_ptlcone", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_67.root",whichCondorJob,year),"faketrgmsel1_ptlcone", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_68.root",whichCondorJob,year),"faketrgmsel2_ptlcone", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_69.root",whichCondorJob,year),"faketrgesel0_ptlcone", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_70.root",whichCondorJob,year),"faketrgesel1_ptlcone", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_71.root",whichCondorJob,year),"faketrgesel2_ptlcone", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_0.root",whichCondorJob,year),"fakemsel_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_1.root",whichCondorJob,year),"fakeesel_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_2.root",whichCondorJob,year),"fakemsel_dphilmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_3.root",whichCondorJob,year),"fakeesel_dphilmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_4.root",whichCondorJob,year),"fakemsel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_5.root",whichCondorJob,year),"fakeesel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_6.root",whichCondorJob,year),"fakemsel_mtfix", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_7.root",whichCondorJob,year),"fakeesel_mtfix", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_8.root",whichCondorJob,year),"fakemsel_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_9.root",whichCondorJob,year),"fakeesel_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_10.root",whichCondorJob,year),"fakemsel_etal", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_11.root",whichCondorJob,year),"fakeesel_etal", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_12.root",whichCondorJob,year),"fakemsel_ptlcone", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_13.root",whichCondorJob,year),"fakeesel_ptlcone", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_14.root",whichCondorJob,year),"fakemsel_maxmetmt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_15.root",whichCondorJob,year),"fakeesel_maxmetmt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_16.root",whichCondorJob,year),"fakemsel_triggermatch0_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_17.root",whichCondorJob,year),"fakeesel_triggermatch0_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_18.root",whichCondorJob,year),"fakemsel_triggermatch1_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_19.root",whichCondorJob,year),"fakeesel_triggermatch1_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_20.root",whichCondorJob,year),"fakemsel_triggermatch2_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_21.root",whichCondorJob,year),"fakeesel_triggermatch2_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_22.root",whichCondorJob,year),"fakemsel_triggermatch3_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_23.root",whichCondorJob,year),"fakeesel_triggermatch3_ptl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_72.root",whichCondorJob,year),"fakemsel_jet_drljet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_73.root",whichCondorJob,year),"fakeesel_jet_drljet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_74.root",whichCondorJob,year),"fakemsel_bjet_drljet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_75.root",whichCondorJob,year),"fakeesel_bjet_drljet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_76.root",whichCondorJob,year),"fakemsel_jet_metlt30_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_77.root",whichCondorJob,year),"fakeesel_jet_metlt30_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_78.root",whichCondorJob,year),"fakemsel_bjet_metlt30_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_79.root",whichCondorJob,year),"fakeesel_bjet_metlt30_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"NPV","",Form("anaZ/fillhisto_fakeAnalysis%d_%d_80.root",whichCondorJob,year),"fakemsel_npv", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,1,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"NPV","",Form("anaZ/fillhisto_fakeAnalysis%d_%d_81.root",whichCondorJob,year),"fakeesel_npv", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,1,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "fake_fit"){
    legendBSM="";
    isNeverBlinded=0;
    isBlinded=0;
    fidAnaName="";
    mlfitResult="";
    channelName="XXX"; 
    TString legendL = "DUMMY";
    for(int type=0; type<32; type++){
      if     (type%2 == 0) legendL="m";
      else if(type%2 == 1) legendL="e";
        finalPlot(0,1,"X","GeV",Form("anaZ/fillhisto_fakeAnalysis%d_%d_%d.root",whichCondorJob,year,100+type),Form("fake%ssel_ptltight%d_mtfix",legendL.Data(),type), 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    }
  }
  else if(nsel == "wz"){
    legendBSM="";
    isNeverBlinded=0;
    isBlinded=0;
    fidAnaName="";
    mlfitResult="";
    channelName="XXX"; 
    SF_DY=1;
    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_0.root",whichCondorJob,year),"wzsel_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|m_{ll}-m_{Z}|","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_1.root",whichCondorJob,year),"wzsel_mllz", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{3l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_2.root",whichCondorJob,year),"wzsel_m3l", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l-W}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_3.root",whichCondorJob,year),"wzsel_ptlw", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{b jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_4.root",whichCondorJob,year),"wzsel_nbtagjet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Leading p_{T}^{l-Z}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_5.root",whichCondorJob,year),"wzsel_ptlz1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Leading p_{T}^{l-Z}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_6.root",whichCondorJob,year),"wzbsel_ptlz1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Trailing p_{T}^{l-Z}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_7.root",whichCondorJob,year),"wzsel_ptlz2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Trailing p_{T}^{l-Z}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_8.root",whichCondorJob,year),"wzbsel_ptlz2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}^{W}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_9.root",whichCondorJob,year),"wzsel_mtw", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}^{W}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_10.root",whichCondorJob,year),"wzbsel_mtw", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_wzAnalysis%d_%d_11.root",whichCondorJob,year),"wzsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_wzAnalysis%d_%d_12.root",whichCondorJob,year),"wzbsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_13.root",whichCondorJob,year),"wzsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_14.root",whichCondorJob,year),"wzbsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_15.root",whichCondorJob,year),"wzsel_ptmiss", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_16.root",whichCondorJob,year),"wzbsel_ptmiss", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_17.root",whichCondorJob,year),"wzjjsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_18.root",whichCondorJob,year),"wzbjjsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_19.root",whichCondorJob,year),"wzjjsel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_20.root",whichCondorJob,year),"wzbjjsel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_21.root",whichCondorJob,year),"wzjjsel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_22.root",whichCondorJob,year),"wzbjjsel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_23.root",whichCondorJob,year),"wzjjsel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_24.root",whichCondorJob,year),"wzbjjsel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_wzAnalysis%d_%d_25.root",whichCondorJob,year),"wzjjsel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_wzAnalysis%d_%d_26.root",whichCondorJob,year),"wzbjjsel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_27.root",whichCondorJob,year),"wzvbssel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_28.root",whichCondorJob,year),"wzbvbssel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_29.root",whichCondorJob,year),"wzvbssel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_30.root",whichCondorJob,year),"wzbvbssel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_31.root",whichCondorJob,year),"wzvbssel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_32.root",whichCondorJob,year),"wzbvbssel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_33.root",whichCondorJob,year),"wzvbssel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_34.root",whichCondorJob,year),"wzbvbssel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_wzAnalysis%d_%d_35.root",whichCondorJob,year),"wzvbssel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_wzAnalysis%d_%d_36.root",whichCondorJob,year),"wzbvbssel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{3l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_37.root",whichCondorJob,year),"llgsel_m3l", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_wzAnalysis%d_%d_38.root",whichCondorJob,year),"llgsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{#gamma}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_39.root",whichCondorJob,year),"llgsel_ptle", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{#gamma}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_40.root",whichCondorJob,year),"llgsel_ptlm", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{b jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_51.root",whichCondorJob,year),"whsel_nbtagjet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_52.root",whichCondorJob,year),"whsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_wzAnalysis%d_%d_53.root",whichCondorJob,year),"whsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_54.root",whichCondorJob,year),"whsel_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta R_{ll}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_55.root",whichCondorJob,year),"whsel_drllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l3}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_56.root",whichCondorJob,year),"whsel_ptl3", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_57.root",whichCondorJob,year),"wzsel_mmm_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_58.root",whichCondorJob,year),"wzsel_emm_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_59.root",whichCondorJob,year),"wzsel_mee_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_wzAnalysis%d_%d_60.root",whichCondorJob,year),"wzsel_eee_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_61.root",whichCondorJob,year),"wzsel_pttag_trigger0", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_62.root",whichCondorJob,year),"wzsel_pttag_trigger1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_63.root",whichCondorJob,year),"wzsel_pttag_trigger2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_64.root",whichCondorJob,year),"wzsel_pttag_trigger3", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_65.root",whichCondorJob,year),"wzsel_ptl_trigger0", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_66.root",whichCondorJob,year),"wzsel_ptl_trigger1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_67.root",whichCondorJob,year),"wzsel_ptl_trigger2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_68.root",whichCondorJob,year),"wzsel_ptl_trigger3", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_69.root",whichCondorJob,year),"wzsel_ptl_trigger4", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_70.root",whichCondorJob,year),"wzsel_ptl_trigger5", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_71.root",whichCondorJob,year),"wzsel_ptl_trigger6", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_72.root",whichCondorJob,year),"wzsel_ptl_trigger7", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,2,"p_{T}^{#mu-W}","GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_73.root",whichCondorJob,year),"wzsel_ptmw", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,2,"p_{T}^{e-W}"  ,"GeV",Form("anaZ/fillhisto_wzAnalysis%d_%d_74.root",whichCondorJob,year),"wzsel_ptew", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|#eta^{#mu-W}|","",Form("anaZ/fillhisto_wzAnalysis%d_%d_75.root",whichCondorJob,year),"wzsel_etamw", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|#eta^{e-W}|" ,"",Form("anaZ/fillhisto_wzAnalysis%d_%d_76.root",whichCondorJob,year),"wzsel_etaew", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "zz"){
    legendBSM="";
    isNeverBlinded=0;
    isBlinded=0;
    fidAnaName="";
    mlfitResult="";
    channelName="XXX"; 
    SF_DY=1;
    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_0.root",whichCondorJob,year),"zzsel_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|m_{ll}-m_{Z1}|","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_1.root",whichCondorJob,year),"zzsel_mllz1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|m_{ll}-m_{Z2}|","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_2.root",whichCondorJob,year),"zzsel_mllz2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Leading p_{T}^{l-Z1}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_3.root",whichCondorJob,year),"zzsel_ptlz11", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Trailing p_{T}^{l-Z1}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_4.root",whichCondorJob,year),"zzsel_ptlz12", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Leading p_{T}^{l-Z1}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_5.root",whichCondorJob,year),"zzsel_ptlz21", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Trailing p_{T}^{l-Z1}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_6.root",whichCondorJob,year),"zzsel_ptlz22", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{4l}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_7.root",whichCondorJob,year),"zzsel_m4l", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_zzAnalysis%d_%d_8.root",whichCondorJob,year),"zzsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_9.root",whichCondorJob,year),"zzsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_10.root",whichCondorJob,year),"zzsel_ptmiss", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_11.root",whichCondorJob,year),"zzjjsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_12.root",whichCondorJob,year),"zzjjsel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_13.root",whichCondorJob,year),"zzjjsel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_14.root",whichCondorJob,year),"zzjjsel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_zzAnalysis%d_%d_15.root",whichCondorJob,year),"zzjjsel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_16.root",whichCondorJob,year),"zzvbssel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_17.root",whichCondorJob,year),"zzvbssel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_18.root",whichCondorJob,year),"zzvbssel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_19.root",whichCondorJob,year),"zzvbssel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_zzAnalysis%d_%d_20.root",whichCondorJob,year),"zzvbssel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_zzAnalysis%d_%d_21.root",whichCondorJob,year),"zzsel_no4l_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{4l}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_22.root",whichCondorJob,year),"zzsel_no4l_m4l", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{bjets}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_23.root",whichCondorJob,year),"zzsel_no4l_nbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{bjets}","",Form("anaZ/fillhisto_zzAnalysis%d_%d_24.root",whichCondorJob,year),"zzsel_xy_nbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{4l}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_25.root",whichCondorJob,year),"zzsel_xy_btagged_m4l", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_zzAnalysis%d_%d_26.root",whichCondorJob,year),"zzsel_xy_nonbtagged_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{e#mu}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_27.root",whichCondorJob,year),"zzsel_xy_nonbtagged_mll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_28.root",whichCondorJob,year),"zzsel_xy_nonbtagged_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{4l}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_29.root",whichCondorJob,year),"zzsel_xy_nonbtagged_m4l", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{Z2}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_30.root",whichCondorJob,year),"zzsel_xy_nonbtagged_ptz2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}^{Z2,met}","GeV",Form("anaZ/fillhisto_zzAnalysis%d_%d_31.root",whichCondorJob,year),"zzsel_xy_nonbtagged_mtxy", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "met"){
    legendBSM="";
    isNeverBlinded=0;
    isBlinded=0;
    fidAnaName="";
    mlfitResult="";
    channelName="XXX"; 
    SF_DY=1;
    finalPlot(0,1,"m_{tot}","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_0.root",whichCondorJob,year),"metsel0_mtot", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{tot}","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_1.root",whichCondorJob,year),"metsel1_mtot", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{tot}","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_2.root",whichCondorJob,year),"metsel2_mtot", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{tot}","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_3.root",whichCondorJob,year),"metsel3_mtot", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{tot}","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_4.root",whichCondorJob,year),"metsel4_mtot", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{tot}","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_5.root",whichCondorJob,year),"metsel5_mtot", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());

    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_6.root",whichCondorJob,year),"metsel0_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_7.root",whichCondorJob,year),"metsel1_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_8.root",whichCondorJob,year),"metsel2_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_9.root",whichCondorJob,year),"metsel3_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_10.root",whichCondorJob,year),"metsel4_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Min(m_{ll})","GeV",Form("anaZ/fillhisto_metAnalysis%d_%d_11.root",whichCondorJob,year),"metsel5_mllmin", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "ssww"){
    legendBSM="";
    isNeverBlinded=0;
    isBlinded=0;
    fidAnaName="";
    mlfitResult="";
    channelName="XXX"; 
    SF_DY=1;
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_0.root",whichCondorJob,year),"sswwpresel_mll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{bjets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_1.root",whichCondorJob,year),"sswwpresel_nbjets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_2.root",whichCondorJob,year),"sswwpresel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_3.root",whichCondorJob,year),"sswwbpresel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_4.root",whichCondorJob,year),"sswwpresel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_5.root",whichCondorJob,year),"sswwbpresel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_6.root",whichCondorJob,year),"sswwpresel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_7.root",whichCondorJob,year),"sswwbpresel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_8.root",whichCondorJob,year),"sswwsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_9.root",whichCondorJob,year),"sswwbsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_10.root",whichCondorJob,year),"sswwsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_11.root",whichCondorJob,year),"sswwbsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_12.root",whichCondorJob,year),"sswwsel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_13.root",whichCondorJob,year),"sswwbsel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_14.root",whichCondorJob,year),"sswwsel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_15.root",whichCondorJob,year),"sswwbsel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_16.root",whichCondorJob,year),"sswwsel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_17.root",whichCondorJob,year),"sswwbsel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_18.root",whichCondorJob,year),"sswwjjsel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_19.root",whichCondorJob,year),"sswwbjjsel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_20.root",whichCondorJob,year),"sswwvbssel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_21.root",whichCondorJob,year),"sswwbvbssel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_22.root",whichCondorJob,year),"sswwvbssel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_23.root",whichCondorJob,year),"sswwbvbssel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_24.root",whichCondorJob,year),"sswwvbssel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{jj}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_25.root",whichCondorJob,year),"sswwbvbssel_mjj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_26.root",whichCondorJob,year),"sswwvbssel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_27.root",whichCondorJob,year),"sswwbvbssel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_28.root",whichCondorJob,year),"sswwvbssel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_29.root",whichCondorJob,year),"sswwbvbssel_dphijj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Zep(V)","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_30.root",whichCondorJob,year),"sswwvbssel_zepvv", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Zep(V)","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_31.root",whichCondorJob,year),"sswwbvbssel_zepvv", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_32.root",whichCondorJob,year),"sswwvbssel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"BDT","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_33.root",whichCondorJob,year),"sswwbvbssel_bdt_vbfincl", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_34.root",whichCondorJob,year),"sswwjjsel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#eta_{jj}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_35.root",whichCondorJob,year),"sswwbjjsel_detajj", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_36.root",whichCondorJob,year),"sswwjjsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"Lepton type","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_37.root",whichCondorJob,year),"sswwbjjsel_ltype", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_38.root",whichCondorJob,year),"sswwjjsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_39.root",whichCondorJob,year),"sswwbjjsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{j1}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_40.root",whichCondorJob,year),"sswwjjsel_ptj1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{j1}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_41.root",whichCondorJob,year),"sswwbjjsel_ptj1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{j2}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_42.root",whichCondorJob,year),"sswwjjsel_ptj2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{j2}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_43.root",whichCondorJob,year),"sswwbjjsel_ptj2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{j1}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_44.root",whichCondorJob,year),"sswwjjsel_etaj1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{j1}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_45.root",whichCondorJob,year),"sswwbjjsel_etaj1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{j2}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_46.root",whichCondorJob,year),"sswwjjsel_etaj2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{j2}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_47.root",whichCondorJob,year),"sswwbjjsel_etaj2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l1}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_48.root",whichCondorJob,year),"sswwjjsel_ptl1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l1}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_49.root",whichCondorJob,year),"sswwbjjsel_ptl1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l2}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_50.root",whichCondorJob,year),"sswwjjsel_ptl2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l2}","GeV",Form("anaZ/fillhisto_sswwAnalysis%d_%d_51.root",whichCondorJob,year),"sswwbjjsel_ptl2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{l1}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_52.root",whichCondorJob,year),"sswwjjsel_etal1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{l1}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_53.root",whichCondorJob,year),"sswwbjjsel_etal1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{l2}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_54.root",whichCondorJob,year),"sswwjjsel_etal2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta_{T}^{l2}","",Form("anaZ/fillhisto_sswwAnalysis%d_%d_55.root",whichCondorJob,year),"sswwbjjsel_etal2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "zmet"){
    legendBSM="";
    isNeverBlinded=0;
    isBlinded=0;
    fidAnaName="";
    mlfitResult="";
    channelName="XXX"; 
    SF_DY=1;
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_0.root",whichCondorJob,year), "zmetmmsel_mll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_1.root",whichCondorJob,year), "zmetemsel_mll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{ll}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_2.root",whichCondorJob,year), "zmeteesel_mll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p^{ll}_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_3.root",whichCondorJob,year), "zmetmmsel_ptll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p^{ll}_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_4.root",whichCondorJob,year), "zmetemsel_ptll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p^{ll}_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_5.root",whichCondorJob,year), "zmeteesel_ptll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#DeltaR_{ll}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_6.root",whichCondorJob,year), "zmetmmsel_drll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#DeltaR_{ll}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_7.root",whichCondorJob,year), "zmetemsel_drll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#DeltaR_{ll}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_8.root",whichCondorJob,year), "zmeteesel_drll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{ll}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_9.root",whichCondorJob,year),"zmetmmsel_dphill", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{ll}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_10.root",whichCondorJob,year),"zmetemsel_dphill", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{ll}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_11.root",whichCondorJob,year),"zmeteesel_dphill", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l1}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_12.root",whichCondorJob,year),"zmetmmsel_ptl1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l1}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_13.root",whichCondorJob,year),"zmetemsel_ptl1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l1}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_14.root",whichCondorJob,year),"zmeteesel_ptl1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l2}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_15.root",whichCondorJob,year),"zmetmmsel_ptl2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l2}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_16.root",whichCondorJob,year),"zmetemsel_ptl2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{l2}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_17.root",whichCondorJob,year),"zmeteesel_ptl2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta^{l1}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_18.root",whichCondorJob,year),"zmetmmsel_etal1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta^{l1}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_19.root",whichCondorJob,year),"zmetemsel_etal1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta^{l1}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_20.root",whichCondorJob,year),"zmeteesel_etal1", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta^{l2}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_21.root",whichCondorJob,year),"zmetmmsel_etal2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta^{l2}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_22.root",whichCondorJob,year),"zmetemsel_etal2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#eta^{l2}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_23.root",whichCondorJob,year),"zmeteesel_etal2", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"n_{jets}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_24.root",whichCondorJob,year),"zmetmmsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"n_{jets}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_25.root",whichCondorJob,year),"zmetemsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"n_{jets}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_26.root",whichCondorJob,year),"zmeteesel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_27.root",whichCondorJob,year),"zmetmmsel_ptmiss", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_28.root",whichCondorJob,year),"zmetemsel_ptmiss", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_29.root",whichCondorJob,year),"zmeteesel_ptmiss", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{ll}_{T}-p_{T}^{miss}|/p^{ll}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_30.root",whichCondorJob,year),"zmetmmsel_ptbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{ll}_{T}-p_{T}^{miss}|/p^{ll}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_31.root",whichCondorJob,year),"zmetemsel_ptbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{ll}_{T}-p_{T}^{miss}|/p^{ll}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_32.root",whichCondorJob,year),"zmeteesel_ptbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llj}_{T}-p_{T}^{miss}|/p^{llj}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_33.root",whichCondorJob,year),"zmetmmsel_ptjbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llj}_{T}-p_{T}^{miss}|/p^{llj}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_34.root",whichCondorJob,year),"zmetemsel_ptjbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llj}_{T}-p_{T}^{miss}|/p^{llj}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_35.root",whichCondorJob,year),"zmeteesel_ptjbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{ll,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_36.root",whichCondorJob,year),"zmetmmsel_dphillmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{ll,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_37.root",whichCondorJob,year),"zmetemsel_dphillmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{ll,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_38.root",whichCondorJob,year),"zmeteesel_dphillmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llj,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_39.root",whichCondorJob,year),"zmetmmsel_dphilljmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llj,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_40.root",whichCondorJob,year),"zmetemsel_dphilljmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llj,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_41.root",whichCondorJob,year),"zmeteesel_dphilljmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{j,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_42.root",whichCondorJob,year),"zmetmmsel_dphijmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{j,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_43.root",whichCondorJob,year),"zmetemsel_dphijmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{j,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_44.root",whichCondorJob,year),"zmeteesel_dphijmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_45.root",whichCondorJob,year),"zmetmmsel_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_46.root",whichCondorJob,year),"zmetemsel_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_47.root",whichCondorJob,year),"zmeteesel_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p^{ll}_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_48.root",whichCondorJob,year), "zmetbmmsel_ptll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p^{ll}_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_49.root",whichCondorJob,year), "zmetbemsel_ptll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p^{ll}_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_50.root",whichCondorJob,year), "zmetbeesel_ptll", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_51.root",whichCondorJob,year),"zmetbmmsel_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_52.root",whichCondorJob,year),"zmetbemsel_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_53.root",whichCondorJob,year),"zmetbeesel_mt", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_54.root",whichCondorJob,year),"zmetbmmsel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_55.root",whichCondorJob,year),"zmetbemsel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_56.root",whichCondorJob,year),"zmetbeesel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llg}_{T}-p_{T}^{miss}|/p^{llg}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_57.root",whichCondorJob,year),"zmetgmmsel_ptgbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llg}_{T}-p_{T}^{miss}|/p^{llg}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_58.root",whichCondorJob,year),"zmetgemsel_ptgbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llg}_{T}-p_{T}^{miss}|/p^{llg}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_59.root",whichCondorJob,year),"zmetgeesel_ptgbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llgj}_{T}-p_{T}^{miss}|/p^{llgj}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_60.root",whichCondorJob,year),"zmetgmmsel_ptgjbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llgj}_{T}-p_{T}^{miss}|/p^{llgj}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_61.root",whichCondorJob,year),"zmetgemsel_ptgjbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"|p^{llgj}_{T}-p_{T}^{miss}|/p^{llgj}_{T}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_62.root",whichCondorJob,year),"zmetgeesel_ptgjbalance", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llg,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_63.root",whichCondorJob,year),"zmetgmmsel_dphillgmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llg,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_64.root",whichCondorJob,year),"zmetgemsel_dphillgmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llg,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_65.root",whichCondorJob,year),"zmetgeesel_dphillgmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llgj,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_66.root",whichCondorJob,year),"zmetgmmsel_dphillgjmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llgj,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_67.root",whichCondorJob,year),"zmetgemsel_dphillgjmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"#Delta#phi_{llgj,p_{T}^{miss}}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_68.root",whichCondorJob,year),"zmetgeesel_dphillgjmet", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_69.root",whichCondorJob,year),"zmetgmmsel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_70.root",whichCondorJob,year),"zmetgemsel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_71.root",whichCondorJob,year),"zmetgeesel_met", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_72.root",whichCondorJob,year),"zmetgmmsel_mtg", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_73.root",whichCondorJob,year),"zmetgemsel_mtg", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"m_{T}","GeV",Form("anaZ/fillhisto_zmetAnalysis%d_%d_74.root",whichCondorJob,year),"zmetgeesel_mtg", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_75.root",whichCondorJob,year),"zmetgmmsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_76.root",whichCondorJob,year),"zmetgemsel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"N_{jets}","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_77.root",whichCondorJob,year),"zmetgeesel_njets", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss} significance","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_78.root",whichCondorJob,year),"zmetgmmsel_metsig", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss} significance","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_79.root",whichCondorJob,year),"zmetgemsel_metsig", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss} significance","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_80.root",whichCondorJob,year),"zmetgeesel_metsig", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetPtgFrac","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_81.root",whichCondorJob,year),"zmetgmmsel_jetptfrac", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetPtgFrac","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_82.root",whichCondorJob,year),"zmetgemsel_jetptfrac", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetPtgFrac","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_83.root",whichCondorJob,year),"zmetgeesel_jetptfrac", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss} significance","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_84.root",whichCondorJob,year),"zmetmmsel_metsig", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss} significance","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_85.root",whichCondorJob,year),"zmetemsel_metsig", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"p_{T}^{miss} significance","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_86.root",whichCondorJob,year),"zmeteesel_metsig", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetPtFrac","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_87.root",whichCondorJob,year),"zmetmmsel_jetptfrac", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetPtFrac","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_88.root",whichCondorJob,year),"zmetemsel_jetptfrac", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
    finalPlot(0,1,"jetPtFrac","",Form("anaZ/fillhisto_zmetAnalysis%d_%d_89.root",whichCondorJob,year),"zmeteesel_jetptfrac", 0,year,legendBSM.Data(),SF_DY,isBlinded,"",1,applyScaling,mlfitResult.Data(),channelName.Data());
  }
  else if(nsel == "gj"){
    legendBSM="";
    isNeverBlinded=0;
    isBlinded=0;
    fidAnaName="";
    channelName="XXX"; 
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_3.root",whichCondorJob,year),"sietaieta_pt0_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt0_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_13.root",whichCondorJob,year),"sietaieta_pt1_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt1_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_23.root",whichCondorJob,year),"sietaieta_pt2_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt2_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_33.root",whichCondorJob,year),"sietaieta_pt3_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt3_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_43.root",whichCondorJob,year),"sietaieta_pt4_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt4_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_53.root",whichCondorJob,year),"sietaieta_pt5_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt5_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_63.root",whichCondorJob,year),"sietaieta_pt6_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt6_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_73.root",whichCondorJob,year),"sietaieta_pt7_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt7_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_83.root",whichCondorJob,year),"sietaieta_pt8_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt8_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_93.root",whichCondorJob,year),"sietaieta_pt9_eta0_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt9_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_103.root",whichCondorJob,year),"sietaieta_pt10_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt10_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_113.root",whichCondorJob,year),"sietaieta_pt11_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt11_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_123.root",whichCondorJob,year),"sietaieta_pt12_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt12_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_133.root",whichCondorJob,year),"sietaieta_pt13_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt13_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_143.root",whichCondorJob,year),"sietaieta_pt14_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt14_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_153.root",whichCondorJob,year),"sietaieta_pt15_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt15_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_163.root",whichCondorJob,year),"sietaieta_pt16_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt16_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_173.root",whichCondorJob,year),"sietaieta_pt17_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt17_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_183.root",whichCondorJob,year),"sietaieta_pt18_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt18_eta0_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_193.root",whichCondorJob,year),"sietaieta_pt19_eta0_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt19_eta0_obs.root",channelName.Data(),1);

    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_7.root",whichCondorJob,year),"sietaieta_pt0_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt0_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_17.root",whichCondorJob,year),"sietaieta_pt1_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt1_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_27.root",whichCondorJob,year),"sietaieta_pt2_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt2_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_37.root",whichCondorJob,year),"sietaieta_pt3_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt3_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_47.root",whichCondorJob,year),"sietaieta_pt4_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt4_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_57.root",whichCondorJob,year),"sietaieta_pt5_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt5_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_67.root",whichCondorJob,year),"sietaieta_pt6_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt6_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_77.root",whichCondorJob,year),"sietaieta_pt7_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt7_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_87.root",whichCondorJob,year),"sietaieta_pt8_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt8_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_97.root",whichCondorJob,year),"sietaieta_pt9_eta1_obs", 1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt9_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_107.root",whichCondorJob,year),"sietaieta_pt10_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt10_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_117.root",whichCondorJob,year),"sietaieta_pt11_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt11_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_127.root",whichCondorJob,year),"sietaieta_pt12_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt12_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_137.root",whichCondorJob,year),"sietaieta_pt13_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt13_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_147.root",whichCondorJob,year),"sietaieta_pt14_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt14_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_157.root",whichCondorJob,year),"sietaieta_pt15_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt15_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_167.root",whichCondorJob,year),"sietaieta_pt16_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt16_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_177.root",whichCondorJob,year),"sietaieta_pt17_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt17_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_187.root",whichCondorJob,year),"sietaieta_pt18_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt18_eta1_obs.root",channelName.Data(),1);
    finalPlot(0,1,"#sigma_{i#eta i#eta}","",Form("anaZ/fillhisto_gammaAnalysis%d_%d_197.root",whichCondorJob,year),"sietaieta_pt19_eta1_obs",1,year,legendBSM.Data(),1.0,isBlinded,"",1,applyScaling,"gammajet/result0_20bins/fitDiagnosticsgj_pt19_eta1_obs.root",channelName.Data(),1);
  }
}

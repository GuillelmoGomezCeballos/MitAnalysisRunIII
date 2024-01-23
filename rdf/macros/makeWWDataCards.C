#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TSystem.h>
#include <TString.h>
#include <TRandom.h>
#include <TH1D.h>
#include <TH2D.h>
#include <TMath.h>
#include <iostream>
#include <fstream>
#include "TLorentzVector.h"
#include "TColor.h"

#include "../makePlots/common.h"

void makeWWDataCards(int whichAna = 0, int fidAna = 1, TString InputDir = "anaZ", TString anaSel = "wwAnalysis1001", int year = 20221, bool isFiducial = false){
  double WWNNLO_resumSyst[4] = {1.015,0.980,0.959,0.959};
  double WWNNLO_scaleSyst[4] = {1.002,0.999,0.988,0.988};

  if(fidAna <= 0 || fidAna >= 5) printf("Wrong fidAna(%d)\n",fidAna);

  double triggerEffUnc = 1.000;
  if     (year == 20220) triggerEffUnc = 1.002;
  else if(year == 20221) triggerEffUnc = 1.004;

  int jumpValue = 200;

  TString addFiducialName = "";
  if(isFiducial == true) addFiducialName = "_isFiducial";

  double systValue;
  TFile *inputFile;
  TFile *outputFile;
  const int nSelTotal = 5;
  const int nSystTotal = 179;

  TH1D *histo_Auxiliar[nSelTotal][nPlotCategories];
  TH1D *histo_Baseline[nPlotCategories];
  TH1D *histo_QCDScaleUp[nPlotCategories];
  TH1D *histo_QCDScaleDown[nPlotCategories];
  TH1D *histo_PSUp[nPlotCategories];
  TH1D *histo_PSDown[nPlotCategories];
  TH1D *histo_WWNNLO_resumUp[nPlotCategories];
  TH1D *histo_WWNNLO_resumDown[nPlotCategories];
  TH1D *histo_WWNNLO_scaleUp[nPlotCategories];
  TH1D *histo_WWNNLO_scaleDown[nPlotCategories];

  TH1D *histo_Syst[nSystTotal][nPlotCategories];
  TH1D *histo_PDFUp  [101][nPlotCategories];
  TH1D *histo_PDFDown[101][nPlotCategories];

  TString BtagSFBCNames[13] = {"BtagSFBC_00", "BtagSFBC_01", "BtagSFBC_02", "BtagSFBC_03", "BtagSFBC_04", "BtagSFBC_05", "BtagSFBC_06", "BtagSFBC_07", "BtagSFBC_08", "BtagSFBC_09", "BtagSFBC_10", "BtagSFBC_11", "BtagSFBC_12"};

  TString nameSyst[nSystTotal];
  nameSyst[ 0] = Form("%sUp"  ,BtagSFBCNames[ 0].Data());
  nameSyst[ 1] = Form("%sDown",BtagSFBCNames[ 0].Data());
  nameSyst[ 2] = Form("%sUp"  ,BtagSFBCNames[ 1].Data());
  nameSyst[ 3] = Form("%sDown",BtagSFBCNames[ 1].Data());
  nameSyst[ 4] = Form("%sUp"  ,BtagSFBCNames[ 2].Data());
  nameSyst[ 5] = Form("%sDown",BtagSFBCNames[ 2].Data());
  nameSyst[ 6] = Form("%sUp"  ,BtagSFBCNames[ 3].Data());
  nameSyst[ 7] = Form("%sDown",BtagSFBCNames[ 3].Data());
  nameSyst[ 8] = "MuoSFTRKUp";
  nameSyst[ 9] = "MuoSFTRKDown";
  nameSyst[10] = "MuoSFIDUp";
  nameSyst[11] = "MuoSFIDDown";
  nameSyst[12] = "MuoSFISOUp";
  nameSyst[13] = "MuoSFISODown";
  nameSyst[14] = "EleSFTRKUp";
  nameSyst[15] = "EleSFTRKDown";
  nameSyst[16] = "EleSFIDUp";
  nameSyst[17] = "EleSFIDDown";
  nameSyst[18] = "PUSFUp";
  nameSyst[19] = "PUSFDown";
  nameSyst[20] = "PS0";
  nameSyst[21] = "PS1";
  nameSyst[22] = "PS2";
  nameSyst[23] = "PS3";
  nameSyst[24] = "QCDScale0";
  nameSyst[25] = "QCDScale1";
  nameSyst[26] = "QCDScale2";
  nameSyst[27] = "QCDScale3";
  nameSyst[28] = "QCDScale4";
  nameSyst[29] = "QCDScale5";
  for(int i=0; i<=102; i++) nameSyst[30+i] = Form("PDF%d",i);
  nameSyst[133] = Form("%sUp"  ,BtagSFBCNames[ 4].Data());
  nameSyst[134] = Form("%sDown",BtagSFBCNames[ 4].Data());
  nameSyst[135] = Form("%sUp"  ,BtagSFBCNames[ 5].Data());
  nameSyst[136] = Form("%sDown",BtagSFBCNames[ 5].Data());
  nameSyst[137] = Form("%sUp"  ,BtagSFBCNames[ 6].Data());
  nameSyst[138] = Form("%sDown",BtagSFBCNames[ 6].Data());
  nameSyst[139] = Form("%sUp"  ,BtagSFBCNames[ 7].Data());
  nameSyst[140] = Form("%sDown",BtagSFBCNames[ 7].Data());
  nameSyst[141] = Form("%sUp"  ,BtagSFBCNames[ 8].Data());
  nameSyst[142] = Form("%sDown",BtagSFBCNames[ 8].Data());
  nameSyst[143] = Form("%sUp"  ,BtagSFBCNames[ 9].Data());
  nameSyst[144] = Form("%sDown",BtagSFBCNames[ 9].Data());
  nameSyst[145] = Form("%sUp"  ,BtagSFBCNames[10].Data());
  nameSyst[146] = Form("%sDown",BtagSFBCNames[10].Data());
  nameSyst[147] = Form("%sUp"  ,BtagSFBCNames[11].Data());
  nameSyst[148] = Form("%sDown",BtagSFBCNames[11].Data());
  nameSyst[149] = Form("%sUp"  ,BtagSFBCNames[12].Data());
  nameSyst[150] = Form("%sDown",BtagSFBCNames[12].Data());
  nameSyst[151] = "BtagSFLF_00Up";
  nameSyst[152] = "BtagSFLF_00Down";
  nameSyst[153] = "JesUp";
  nameSyst[154] = "JesDown";
  nameSyst[155] = "JerUp";
  nameSyst[156] = "JerDown";
  nameSyst[157] = "MuonMomUp";
  nameSyst[158] = "MuonMomDown";
  nameSyst[159] = "ElectronMomUp";
  nameSyst[160] = "ElectronMomDown";
  nameSyst[161] = "metJERUp";
  nameSyst[162] = "metJERDown";
  nameSyst[163] = "metJESUp";
  nameSyst[164] = "metJESDown";
  nameSyst[165] = "metUnclusteredUp";
  nameSyst[166] = "metUnclusteredDown";
  nameSyst[167] = "JesSubTotalPileUpUp";
  nameSyst[168] = "JesSubTotalPileUpDown";
  nameSyst[169] = "JesSubTotalRelativeUp";
  nameSyst[170] = "JesSubTotalRelativeDown";
  nameSyst[171] = "JesSubTotalPtUp";
  nameSyst[172] = "JesSubTotalPtDown";
  nameSyst[173] = "JesSubTotalScaleUp";
  nameSyst[174] = "JesSubTotalScaleDown";
  nameSyst[175] = "JesFlavorQCDUp";
  nameSyst[176] = "JesFlavorQCDDown";
  nameSyst[177] = "JesTimePtEtaUp";
  nameSyst[178] = "JesTimePtEtaDown";

  double scaleFactorFiducial[nSelTotal][nPlotCategories];
 for(unsigned nSel=0; nSel<nSelTotal; nSel++) for(int ic=0; ic<nPlotCategories; ic++) scaleFactorFiducial[nSel][ic] = 0.0;

  int BinXF = nSelTotal; double minXF = -0.5; double maxXF = nSelTotal-0.5;    
  if(whichAna != 0){
    BinXF = 25; minXF = 85; maxXF = 385;    
  }

  for(int ic=0; ic<nPlotCategories; ic++) {
    histo_Baseline[ic] = new TH1D(Form("histo_%s",plotBaseNames[ic].Data()),Form("histo_%s",plotBaseNames[ic].Data()), BinXF, minXF, maxXF);
    TString plotBaseNamesTemp =  plotBaseNames[ic];
    if(ic == kPlotSignal0 || ic == kPlotSignal1 ||
       ic == kPlotSignal2 || ic == kPlotSignal3 ||
       ic == kPlotqqWW) plotBaseNamesTemp = "WW";
    histo_QCDScaleUp  [ic] = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_QCDScale_%s_ACCEPTUp"  , plotBaseNames[ic].Data(), plotBaseNamesTemp.Data()));
    histo_QCDScaleDown[ic] = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_QCDScale_%s_ACCEPTDown", plotBaseNames[ic].Data(), plotBaseNamesTemp.Data()));
    histo_PSUp  [ic]       = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_PS_%s_ACCEPTUp"  , plotBaseNames[ic].Data(), plotBaseNamesTemp.Data()));
    histo_PSDown[ic]       = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_PS_%s_ACCEPTDown", plotBaseNames[ic].Data(), plotBaseNamesTemp.Data()));
    histo_WWNNLO_resumUp  [ic] = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_WWNNLO_resumUp"  , plotBaseNames[ic].Data()));
    histo_WWNNLO_resumDown[ic] = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_WWNNLO_resumDown", plotBaseNames[ic].Data()));
    histo_WWNNLO_scaleUp  [ic] = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_WWNNLO_scaleUp"  , plotBaseNames[ic].Data()));
    histo_WWNNLO_scaleDown[ic] = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_WWNNLO_scaleDown", plotBaseNames[ic].Data()));
  }

  for(int j=0; j<nSystTotal; j++){
    for(int ic=0; ic<nPlotCategories; ic++) histo_Syst[j][ic] = new TH1D(Form("histo_%s_%s",plotBaseNames[ic].Data(),nameSyst[j].Data()),Form("histo_%s_%s",plotBaseNames[ic].Data(),nameSyst[j].Data()), BinXF, minXF, maxXF);
  }
  for(int j=0; j<101; j++){
    for(int ic=0; ic<nPlotCategories; ic++) histo_PDFUp  [j][ic] = new TH1D(Form("histo_%s_PDF%dUp"  ,plotBaseNames[ic].Data(),j),Form("histo_%s_PDF%dUp"  ,plotBaseNames[ic].Data(),j), BinXF, minXF, maxXF);
    for(int ic=0; ic<nPlotCategories; ic++) histo_PDFDown[j][ic] = new TH1D(Form("histo_%s_PDF%dDown",plotBaseNames[ic].Data(),j),Form("histo_%s_PDF%dDown",plotBaseNames[ic].Data(),j), BinXF, minXF, maxXF);
  }

  if(whichAna == 0){
    // same-sign / WW / DY / Top1 / Top2
    for(unsigned nSel=0; nSel<nSelTotal; nSel++) {
      inputFile = new TFile(Form("%s/fillhisto_%s_%d_%d_mva.root",InputDir.Data(),anaSel.Data(),year,nSel*jumpValue), "read");
      for(unsigned ic=kPlotData; ic!=nPlotCategories; ic++) {
	histo_Auxiliar[nSel][ic] = (TH1D*)inputFile->Get(Form("histoMVA%d", ic)); assert(histo_Auxiliar[nSel][ic]);
      if((ic == kPlotSignal0 || ic == kPlotSignal1 ||
          ic == kPlotSignal2 || ic == kPlotSignal3 ||
          ic == kPlotqqWW) && histo_Auxiliar[nSel][ic]->GetSumOfWeights() > 0) scaleFactorFiducial[nSel][ic] = histo_Auxiliar[nSel][ic]->GetSumOfWeights();
	histo_Baseline[ic]->SetBinContent(nSel+1,histo_Auxiliar[nSel][ic]->GetBinContent(fidAna));
	histo_Baseline[ic]->SetBinError  (nSel+1,histo_Auxiliar[nSel][ic]->GetBinError  (fidAna));
      }
      delete inputFile;
    }

    for(int j=0; j<nSystTotal; j++){
      for(unsigned nSel=0; nSel<nSelTotal; nSel++) {
	inputFile = new TFile(Form("%s/fillhisto_%s_%d_%d_mva.root",InputDir.Data(),anaSel.Data(),year,nSel*jumpValue+1+j), "read");
	for(unsigned ic=kPlotData; ic!=nPlotCategories; ic++) {
          histo_Auxiliar[nSel][ic] = (TH1D*)inputFile->Get(Form("histoMVA%d", ic)); assert(histo_Auxiliar[nSel][ic]);

          if(isFiducial == true && 
           (ic == kPlotqqWW ||
            ic == kPlotggWW ||
            ic == kPlotSignal0 ||
            ic == kPlotSignal1 ||
            ic == kPlotSignal2 ||
            ic == kPlotSignal3
            ) && histo_Auxiliar[nSel][ic]->GetSumOfWeights() > 0 &&
            (j == 20 || j == 21 || j == 22 || j == 23 ||
             j == 24 || j == 25 || j == 26 || j == 27 || j == 28 || j == 29)
            ) histo_Auxiliar[nSel][ic]->Scale(scaleFactorFiducial[nSel][ic]/histo_Auxiliar[nSel][ic]->GetSumOfWeights());

          histo_Syst[j][ic]->SetBinContent(nSel+1,histo_Auxiliar[nSel][ic]->GetBinContent(fidAna));
          histo_Syst[j][ic]->SetBinError  (nSel+1,histo_Auxiliar[nSel][ic]->GetBinError  (fidAna));
        }
        delete inputFile;
      }
    }

  } // Default analysis
  else if(whichAna != 0){
    inputFile = new TFile(Form("%s/fillhisto_%s_%d_%d_mva.root",InputDir.Data(),anaSel.Data(),year,600+fidAna*jumpValue), "read");
    for(unsigned ic=kPlotData; ic!=nPlotCategories; ic++) {
      histo_Baseline[ic] = (TH1D*)inputFile->Get(Form("histoMVA%d", ic)); assert(histo_Baseline[ic]); histo_Baseline[ic]->SetDirectory(0);
      histo_Baseline[ic]->SetNameTitle(Form("histo_%s",plotBaseNames[ic].Data()),Form("histo_%s",plotBaseNames[ic].Data()));
    }
    delete inputFile;

    for(int j=0; j<nSystTotal; j++){
      inputFile = new TFile(Form("%s/fillhisto_%s_%d_%d_mva.root",InputDir.Data(),anaSel.Data(),year,600+fidAna*jumpValue+1+j), "read");
      for(unsigned ic=kPlotData; ic!=nPlotCategories; ic++) {
        histo_Syst[j][ic] = (TH1D*)inputFile->Get(Form("histoMVA%d", ic)); assert(histo_Syst[j][ic]); histo_Syst[j][ic]->SetDirectory(0);
        histo_Syst[j][ic]->SetNameTitle(Form("histo_%s_%s",plotBaseNames[ic].Data(),nameSyst[j].Data()),Form("histo_%s_%s",plotBaseNames[ic].Data(),nameSyst[j].Data()));
      }
      delete inputFile;
    }

  } // Alternative distributions

  for(unsigned ic=0; ic<nPlotCategories; ic++) {
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    histo_WWNNLO_resumUp  [ic]->Add(histo_Baseline[ic]); histo_WWNNLO_resumUp  [ic]->Scale(WWNNLO_resumSyst[fidAna-1]);
    histo_WWNNLO_resumDown[ic]->Add(histo_Baseline[ic]); histo_WWNNLO_resumDown[ic]->Scale(1./WWNNLO_resumSyst[fidAna-1]);
    histo_WWNNLO_scaleUp  [ic]->Add(histo_Baseline[ic]); histo_WWNNLO_scaleUp  [ic]->Scale(WWNNLO_scaleSyst[fidAna-1]);
    histo_WWNNLO_scaleDown[ic]->Add(histo_Baseline[ic]); histo_WWNNLO_scaleDown[ic]->Scale(1./WWNNLO_scaleSyst[fidAna-1]);
    for(int nb=1; nb<=histo_Baseline[ic]->GetNbinsX(); nb++){
      histo_Baseline[ic]->SetBinContent(nb, TMath::Max((float)histo_Baseline[ic]->GetBinContent(nb),0.0f));

      // compute QCD scale uncertainties bin-by-bin
      double diffQCDScale[6] = {
       TMath::Abs(histo_Syst[24][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb)),
       TMath::Abs(histo_Syst[25][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb)),
       TMath::Abs(histo_Syst[26][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb)),
       TMath::Abs(histo_Syst[27][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb)),
       TMath::Abs(histo_Syst[28][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb)),
       TMath::Abs(histo_Syst[29][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb))};

      double systQCDScale = diffQCDScale[0];
      for(int nqcd=1; nqcd<6; nqcd++) {
        if(diffQCDScale[nqcd] > systQCDScale) systQCDScale = diffQCDScale[nqcd];
      }

      if(histo_Baseline[ic]->GetBinContent(nb) > 0) 
        systQCDScale = 1.0+systQCDScale/histo_Baseline[ic]->GetBinContent(nb);
      else systQCDScale = 1;

      histo_QCDScaleUp  [ic]->SetBinContent(nb, histo_Baseline[ic]->GetBinContent(nb)*systQCDScale);
      histo_QCDScaleDown[ic]->SetBinContent(nb, histo_Baseline[ic]->GetBinContent(nb)/systQCDScale);

      // compute PS uncertainties bin-by-bin
      double diffPS[4] = {
       TMath::Abs(histo_Syst[20][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb)),
       TMath::Abs(histo_Syst[21][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb)),
       TMath::Abs(histo_Syst[22][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb)),
       TMath::Abs(histo_Syst[23][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb))};

      double systPS = diffPS[0];
      for(int nps=1; nps<4; nps++) {
        if(diffPS[nps] > systPS) systPS = diffPS[nps];
      }

      if(histo_Baseline[ic]->GetBinContent(nb) > 0) 
        systPS = 1.0+systPS/histo_Baseline[ic]->GetBinContent(nb);
      else systPS = 1;

      histo_PSUp  [ic]->SetBinContent(nb, histo_Baseline[ic]->GetBinContent(nb)*systPS);
      histo_PSDown[ic]->SetBinContent(nb, histo_Baseline[ic]->GetBinContent(nb)/systPS);

      histo_Baseline    [ic]->SetBinContent(nb, TMath::Max((float)histo_Baseline    [ic]->GetBinContent(nb),0.0f));
      histo_QCDScaleUp  [ic]->SetBinContent(nb, TMath::Max((float)histo_QCDScaleUp  [ic]->GetBinContent(nb),0.0f));
      histo_QCDScaleDown[ic]->SetBinContent(nb, TMath::Max((float)histo_QCDScaleDown[ic]->GetBinContent(nb),0.0f));
      histo_PSUp        [ic]->SetBinContent(nb, TMath::Max((float)histo_PSUp        [ic]->GetBinContent(nb),0.0f));
      histo_PSDown      [ic]->SetBinContent(nb, TMath::Max((float)histo_PSDown      [ic]->GetBinContent(nb),0.0f));
      for(int j=0; j<nSystTotal; j++) histo_Syst[j][ic]->SetBinContent(nb, TMath::Max((float)histo_Syst[j][ic]->GetBinContent(nb),0.0f));

      // compute PDF uncertainties
      if(histo_Baseline[ic]->GetBinContent(nb) > 0 && TMath::Abs(histo_Baseline[ic]->GetBinContent(nb)-histo_Syst[30][ic]->GetBinContent(nb))/histo_Baseline[ic]->GetBinContent(nb) > 0.001) printf("PDF problem %f %f %f\n",histo_Baseline[ic]->GetBinContent(nb),histo_Syst[30][ic]->GetBinContent(nb),TMath::Abs(histo_Baseline[ic]->GetBinContent(nb)-histo_Syst[30][ic]->GetBinContent(nb)));
      for(int npdf=0; npdf<100; npdf++){
        double diff = 0;
        if(histo_Baseline[ic]->GetBinContent(nb) > 0) diff = TMath::Abs(histo_Syst[npdf+31][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb))/histo_Baseline[ic]->GetBinContent(nb);
        if(diff > 0.05) printf("Large PDFUnc(%d) %d %d %f\n",npdf,ic,nb,diff);
        histo_PDFUp  [npdf][ic]->SetBinContent(nb, histo_Baseline[ic]->GetBinContent(nb)*(1.0+diff));
        histo_PDFDown[npdf][ic]->SetBinContent(nb, histo_Baseline[ic]->GetBinContent(nb)/(1.0+diff));
      }
      histo_PDFUp  [100][ic]->SetBinContent(nb, histo_Syst[131][ic]->GetBinContent(nb));
      histo_PDFDown[100][ic]->SetBinContent(nb, histo_Syst[132][ic]->GetBinContent(nb));

      // making symmetric uncertainties
      if(histo_Baseline[ic]->GetBinContent(nb) > 0) {
        // First 20
        for(int nuis=0; nuis<10; nuis++) {
          systValue = histo_Syst[2*nuis+1][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
          if(systValue > 0) histo_Syst[2*nuis][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        }
        // Last ones
        for(int nuis=67; nuis<90; nuis++) {
          systValue = histo_Syst[2*nuis][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
          if(systValue > 0) histo_Syst[2*nuis-1][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        }
        // Jer
        systValue = (histo_Syst[156][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb))/5.0;
        histo_Syst[156][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)+systValue);
        systValue = histo_Syst[156][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[155][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
      }
    } // loop over bins
  } // loop over categories

  // Begin Nonprompt study
  const int nNonPromptSyst = 12;
  TString namenonPromptSyst[nSystTotal];
  namenonPromptSyst[ 0] = "nonPromptMuonAlt0Up";
  namenonPromptSyst[ 1] = "nonPromptMuonAlt1Down";
  namenonPromptSyst[ 2] = "nonPromptMuonAlt2Up";
  namenonPromptSyst[ 3] = "nonPromptElectronAlt0Up";
  namenonPromptSyst[ 4] = "nonPromptElectronAlt1Up";
  namenonPromptSyst[ 5] = "nonPromptElectronAlt2Up";
  namenonPromptSyst[ 6] = "nonPromptMuonAlt0Down";
  namenonPromptSyst[ 7] = "nonPromptMuonAlt1Up";
  namenonPromptSyst[ 8] = "nonPromptMuonAlt2Down";
  namenonPromptSyst[ 9] = "nonPromptElectronAlt0Down";
  namenonPromptSyst[10] = "nonPromptElectronAlt1Down";
  namenonPromptSyst[11] = "nonPromptElectronAlt2Down";
  TH1D *histo_NonPromtUnc[nNonPromptSyst];
  for(int j=0; j<nNonPromptSyst; j++){
    histo_NonPromtUnc[j] = new TH1D(Form("histo_%s_%s", plotBaseNames[kPlotNonPrompt].Data(), namenonPromptSyst[j].Data()), Form("histo_%s_%s", plotBaseNames[kPlotNonPrompt].Data(), namenonPromptSyst[j].Data()), BinXF, minXF, maxXF);
  }

  const int totalNumberFakeSyst = 6;
  if(whichAna == 0){ 
    TH1D *histo_InputNonPromtUnc[30];
    inputFile = new TFile(Form("%s/fillhisto_%s_%d_nonprompt.root",InputDir.Data(),anaSel.Data(),year), "read");
    for(int j=0; j<30; j++){
      histo_InputNonPromtUnc[j] = (TH1D*)inputFile->Get(Form("histoNonPrompt_%d", j));
    }
    for(int j=0; j<totalNumberFakeSyst; j++){
      for(unsigned nSel=0; nSel<nSelTotal; nSel++) {
        histo_NonPromtUnc[j]->SetBinContent(nSel+1,histo_InputNonPromtUnc[j+nSel*totalNumberFakeSyst]->GetBinContent(fidAna));
        histo_NonPromtUnc[j]->SetBinError  (nSel+1,histo_InputNonPromtUnc[j+nSel*totalNumberFakeSyst]->GetBinError  (fidAna));
      }
    }
    delete inputFile;
  } else {
    TH1D *histo_InputNonPromtUnc[18];
    inputFile = new TFile(Form("%s/fillhisto_%s_%d_nonprompt.root",InputDir.Data(),anaSel.Data(),year), "read");
    for(int j=0; j<18; j++){
      histo_InputNonPromtUnc[j] = (TH1D*)inputFile->Get(Form("histoNonPrompt_%d", 30+j));
    }
    for(int j=0; j<totalNumberFakeSyst; j++){
      for(int nb=1; nb<=histo_InputNonPromtUnc[j]->GetNbinsX(); nb++){
        histo_NonPromtUnc[j]->SetBinContent(nb,histo_InputNonPromtUnc[j+(fidAna-1)*totalNumberFakeSyst]->GetBinContent(nb));
        histo_NonPromtUnc[j]->SetBinError  (nb,histo_InputNonPromtUnc[j+(fidAna-1)*totalNumberFakeSyst]->GetBinError  (nb));
      }
    }
  }

  for(int j=0; j<totalNumberFakeSyst; j++){
    for(int nb=1; nb<=histo_Baseline[kPlotNonPrompt]->GetNbinsX(); nb++){
      if(histo_Baseline[kPlotNonPrompt]->GetBinContent(nb) > 0) {
        systValue = histo_NonPromtUnc[j+0]->GetBinContent(nb) / histo_Baseline[kPlotNonPrompt]->GetBinContent(nb);
        if     (systValue > 1.15) systValue = 1.15;
        else if(systValue < 0.85) systValue = 0.85;
        histo_NonPromtUnc[j+0]->SetBinContent(nb,histo_Baseline[kPlotNonPrompt]->GetBinContent(nb)*systValue);
        printf("fake(%d,%d) = %.3f\n",j,nb,systValue);
        if(systValue > 0) histo_NonPromtUnc[j+totalNumberFakeSyst]->SetBinContent(nb,histo_Baseline[kPlotNonPrompt]->GetBinContent(nb)/systValue);
      }
    }
  }
  // End Nonprompt study

  TString additionalSuffix = "";
  if(whichAna != 0){ 
    additionalSuffix = "_alt";
  }

  TString outputLimits = Form("output_%s_%d_bin%d%s%s.root",anaSel.Data(),year,fidAna-1,additionalSuffix.Data(),addFiducialName.Data());
  outputFile = new TFile(outputLimits, "RECREATE");
  outputFile->cd();
  for(unsigned ic=kPlotData; ic!=nPlotCategories; ic++) {
    if(histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    histo_Baseline[ic]->Write();
    for(int j=0; j<nSystTotal; j++) histo_Syst[j][ic]->Write();

    histo_WWNNLO_resumUp  [ic]->Write();
    histo_WWNNLO_resumDown[ic]->Write();
    histo_WWNNLO_scaleUp  [ic]->Write();
    histo_WWNNLO_scaleDown[ic]->Write();
    histo_QCDScaleUp  [ic]->Write();
    histo_QCDScaleDown[ic]->Write();
    histo_PSUp        [ic]->Write();
    histo_PSDown      [ic]->Write();
    for(int npdf=0; npdf<101; npdf++){
      histo_PDFUp  [npdf][ic]->Write();
      histo_PDFDown[npdf][ic]->Write();
    }
  }
  for(int j=0; j<nNonPromptSyst; j++) histo_NonPromtUnc[j]->Write();
  outputFile->Close();

  // Filling datacards txt file
  char outputLimitsCard[200];
  sprintf(outputLimitsCard,"datacard_%s_%d_bin%d%s%s.txt",anaSel.Data(),year,fidAna-1,additionalSuffix.Data(),addFiducialName.Data());
  ofstream newcardShape;
  newcardShape.open(outputLimitsCard);
  newcardShape << Form("imax * number of channels\n");
  newcardShape << Form("jmax * number of background minus 1\n");
  newcardShape << Form("kmax * number of nuisance parameters\n");

  newcardShape << Form("shapes    *   *   %s  histo_$PROCESS histo_$PROCESS_$SYSTEMATIC\n",outputLimits.Data());
  newcardShape << Form("shapes data_obs * %s  histo_Data\n",outputLimits.Data());

  newcardShape << Form("Observation %f\n",histo_Baseline[kPlotData]->GetSumOfWeights());

  newcardShape << Form("bin   ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    newcardShape << Form("ch%d ",fidAna-1);

  }
  newcardShape << Form("\n");

  newcardShape << Form("process  ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    newcardShape << Form("%s  ", plotBaseNames[ic].Data());
  }
  newcardShape << Form("\n");

  newcardShape << Form("process  ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic != kPlotSignal0 &&
            ic != kPlotSignal1 &&
            ic != kPlotSignal2 &&
            ic != kPlotSignal3 &&
            ic != kPlotqqWW
            ) newcardShape << Form("%d  ", ic);
    else if(ic == kPlotSignal0) newcardShape << Form("%d  ", -1);
    else if(ic == kPlotSignal1) newcardShape << Form("%d  ", -2);
    else if(ic == kPlotSignal2) newcardShape << Form("%d  ", -3);
    else if(ic == kPlotSignal3) newcardShape << Form("%d  ", -4);
    else if(ic == kPlotqqWW)    newcardShape << Form("%d  ", -5);
  }
  newcardShape << Form("\n");

  newcardShape << Form("rate  ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    newcardShape << Form("%f  ", histo_Baseline[ic]->GetSumOfWeights());
  }
  newcardShape << Form("\n");

  //newcardShape << Form("CMS_fakee_norm lnN ");
  //for (int ic=0; ic<nPlotCategories; ic++){
  //  if(!histo_Baseline[ic]) continue;
  //  if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
  //  if(ic == kPlotNonPrompt) newcardShape << Form("%6.3f ",1.15);
  //  else                     newcardShape << Form("- "); 
  //}
  //newcardShape << Form("\n");

  //newcardShape << Form("CMS_fakem_norm   lnN     ");
  //for (int ic=0; ic<nPlotCategories; ic++){
  //  if(!histo_Baseline[ic]) continue;
  //  if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
  //  if(ic == kPlotNonPrompt) newcardShape << Form("%6.3f ",1.15);
  //  else                     newcardShape << Form("- ");
  //}
  //newcardShape << Form("\n");

  newcardShape << Form("nonPromptMuonAlt0 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
    else                     newcardShape << Form("- "); 
  }
  newcardShape << Form("\n");

  newcardShape << Form("nonPromptMuonAlt1 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
    else                     newcardShape << Form("- "); 
  }
  newcardShape << Form("\n");

  newcardShape << Form("nonPromptMuonAlt2 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
    else                     newcardShape << Form("- "); 
  }
  newcardShape << Form("\n");

  newcardShape << Form("nonPromptElectronAlt0 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
    else                     newcardShape << Form("- "); 
  }
  newcardShape << Form("\n");

  newcardShape << Form("nonPromptElectronAlt1 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
    else                     newcardShape << Form("- "); 
  }
  newcardShape << Form("\n");

  newcardShape << Form("nonPromptElectronAlt2 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
    else                     newcardShape << Form("- "); 
  }
  newcardShape << Form("\n");

  int yearLumi = year;
  if(year == 20220 || year == 20221) yearLumi = 2022;
  newcardShape << Form("CMS_lumi_%d   lnN     ",yearLumi);
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("%6.3f ",1.02);
  }
  newcardShape << Form("\n");

  newcardShape << Form("CMS_triggerEff_%d   lnN     ",yearLumi);
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("%6.3f ",triggerEffUnc);
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 0].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 1].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 2].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 3].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 4].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 5].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 6].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 7].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 8].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[ 9].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[10].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[11].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("%s shape ",BtagSFBCNames[12].Data());
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFLF_00 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("MuoSFTRK shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("MuoSFID shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else		     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("MuoSFISO shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else		     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("EleSFTRK shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("EleSFID shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("PUSF shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("JesSubTotalPileUp shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic == kPlotNonPrompt) newcardShape << Form("- ");
    else if(ic == kPlotTop)       newcardShape << Form("- ");
    else if(ic == kPlotDY)        newcardShape << Form("- ");
    else                          newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("JesSubTotalRelative shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic == kPlotNonPrompt) newcardShape << Form("- ");
    else if(ic == kPlotTop)       newcardShape << Form("- ");
    else if(ic == kPlotDY)        newcardShape << Form("- ");
    else                          newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("JesSubTotalPt shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic == kPlotNonPrompt) newcardShape << Form("- ");
    else if(ic == kPlotTop)       newcardShape << Form("- ");
    else if(ic == kPlotDY)        newcardShape << Form("- ");
    else                          newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("JesSubTotalScale shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic == kPlotNonPrompt) newcardShape << Form("- ");
    else if(ic == kPlotTop)       newcardShape << Form("- ");
    else if(ic == kPlotDY)        newcardShape << Form("- ");
    else                          newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("JesFlavorQCD shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic == kPlotNonPrompt) newcardShape << Form("- ");
    else if(ic == kPlotTop)       newcardShape << Form("- ");
    else if(ic == kPlotDY)        newcardShape << Form("- ");
    else                          newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("JesTimePtEta shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic == kPlotNonPrompt) newcardShape << Form("- ");
    else if(ic == kPlotTop)       newcardShape << Form("- ");
    else if(ic == kPlotDY)        newcardShape << Form("- ");
    else                          newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("Jer shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("MuonMom shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");
 
  newcardShape << Form("ElectronMom shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  for(unsigned ic=0; ic<nPlotCategories; ic++) {
    if(ic== kPlotData || ic == kPlotNonPrompt || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic== kPlotSignal0 || ic == kPlotSignal1 || ic== kPlotSignal2 || ic == kPlotSignal3 || ic == kPlotqqWW || ic == kPlotqqWW) continue;
    newcardShape << Form("QCDScale_%s_ACCEPT	shape	",plotBaseNames[ic].Data());
    for(unsigned ic2=0; ic2<nPlotCategories; ic2++) {
      if(ic2 == kPlotData || histo_Baseline[ic2]->GetSumOfWeights() <= 0) continue;
      if(ic==ic2) newcardShape << Form("1.0  ");
      else        newcardShape << Form("-  ");
    }
    newcardShape << Form("\n");
  }

  newcardShape << Form("QCDScale_WW_ACCEPT shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic != kPlotSignal0 &&
            ic != kPlotSignal1 &&
            ic != kPlotSignal2 &&
            ic != kPlotSignal3 &&
            ic != kPlotqqWW
            ) newcardShape << Form("- ");
    else      newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  for(unsigned ic=0; ic<nPlotCategories; ic++) {
    if(ic== kPlotData || ic == kPlotNonPrompt || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic== kPlotSignal0 || ic == kPlotSignal1 || ic== kPlotSignal2 || ic == kPlotSignal3 || ic == kPlotqqWW) continue;
    newcardShape << Form("PS_%s_ACCEPT	shape	",plotBaseNames[ic].Data());
    for(unsigned ic2=0; ic2<nPlotCategories; ic2++) {
      if(ic2 == kPlotData || histo_Baseline[ic2]->GetSumOfWeights() <= 0) continue;
      if(ic==ic2) newcardShape << Form("1.0  ");
      else        newcardShape << Form("-  ");
    }
    newcardShape << Form("\n");
  } 

  newcardShape << Form("PS_WW_ACCEPT shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if     (ic != kPlotSignal0 &&
            ic != kPlotSignal1 &&
            ic != kPlotSignal2 &&
            ic != kPlotSignal3 &&
            ic != kPlotqqWW
            ) newcardShape << Form("- ");
    else      newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  if(whichAna == 0){
    newcardShape << Form("WWNNLO_resum shape ");
    for (int ic=0; ic<nPlotCategories; ic++){
      if(!histo_Baseline[ic]) continue;
      if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
      if     (ic != kPlotqqWW &&
              ic != kPlotggWW &&
              ic != kPlotSignal0 &&
              ic != kPlotSignal1 &&
              ic != kPlotSignal2 &&
              ic != kPlotSignal3
              ) newcardShape << Form("- ");
      else      newcardShape << Form("1.0 ");
    }
    newcardShape << Form("\n");

    newcardShape << Form("WWNNLO_scale shape ");
    for (int ic=0; ic<nPlotCategories; ic++){
      if(!histo_Baseline[ic]) continue;
      if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
      if     (ic != kPlotqqWW &&
              ic != kPlotggWW &&
              ic != kPlotSignal0 &&
              ic != kPlotSignal1 &&
              ic != kPlotSignal2 &&
              ic != kPlotSignal3
              ) newcardShape << Form("- ");
      else      newcardShape << Form("1.0 ");
    }
    newcardShape << Form("\n");
  }

  for(int npdf=0; npdf<=100; npdf++){
    newcardShape << Form("PDF%d shape ",npdf);
    for (int ic=0; ic<nPlotCategories; ic++){
      if(!histo_Baseline[ic]) continue;
      if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
      if(ic == kPlotNonPrompt) newcardShape << Form("- ");
      else if(isFiducial == true && 
           (ic == kPlotqqWW ||
            ic == kPlotggWW ||
            ic == kPlotSignal0 ||
            ic == kPlotSignal1 ||
            ic == kPlotSignal2 ||
            ic == kPlotSignal3
            ))                 newcardShape << Form("- ");
      else                     newcardShape << Form("1.0 ");
    }
    newcardShape << Form("\n");
  }

  newcardShape << Form("CMS_ww_fakenorm_bin%d_%d  rateParam * %s 1 [0.1,4.9]\n",fidAna-1,year,plotBaseNames[kPlotNonPrompt].Data());
  newcardShape << Form("CMS_ww_dytautaunorm_bin%d_%d  rateParam * %s 1 [0.1,4.9]\n",fidAna-1,year,plotBaseNames[kPlotDY].Data());
  newcardShape << Form("CMS_ww_topnorm_bin%d_%d  rateParam * %s 1 [0.1,4.9]\n",fidAna-1,year,plotBaseNames[kPlotTop].Data());

  newcardShape << Form("ch%d autoMCStats 0\n",fidAna-1);

  newcardShape.close();

}

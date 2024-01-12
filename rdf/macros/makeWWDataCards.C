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
  const int nSystTotal = 177;

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

  TString nameSyst[nSystTotal];
  nameSyst[ 0] = "BtagSFBC_00Up";
  nameSyst[ 1] = "BtagSFBC_00Down";
  nameSyst[ 2] = "BtagSFBC_01Up";
  nameSyst[ 3] = "BtagSFBC_01Down";
  nameSyst[ 4] = "BtagSFBC_02Up";
  nameSyst[ 5] = "BtagSFBC_02Down";
  nameSyst[ 6] = "BtagSFBC_03Up";
  nameSyst[ 7] = "BtagSFBC_03Down";
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
  nameSyst[133] = "BtagSFBC_04Up";
  nameSyst[134] = "BtagSFBC_04Down";
  nameSyst[135] = "BtagSFBC_05Up";
  nameSyst[136] = "BtagSFBC_05Down";
  nameSyst[137] = "BtagSFBC_06Up";
  nameSyst[138] = "BtagSFBC_06Down";
  nameSyst[139] = "BtagSFBC_07Up";
  nameSyst[140] = "BtagSFBC_07Down";
  nameSyst[141] = "BtagSFBC_08Up";
  nameSyst[142] = "BtagSFBC_08Down";
  nameSyst[143] = "BtagSFBC_09Up";
  nameSyst[144] = "BtagSFBC_09Down";
  nameSyst[145] = "BtagSFBC_10Up";
  nameSyst[146] = "BtagSFBC_10Down";
  nameSyst[147] = "BtagSFBC_11Up";
  nameSyst[148] = "BtagSFBC_11Down";
  nameSyst[149] = "BtagSFLF_00Up";
  nameSyst[150] = "BtagSFLF_00Down";
  nameSyst[151] = "JesUp";
  nameSyst[152] = "JesDown";
  nameSyst[153] = "JerUp";
  nameSyst[154] = "JerDown";
  nameSyst[155] = "MuonMomUp";
  nameSyst[156] = "MuonMomDown";
  nameSyst[157] = "ElectronMomUp";
  nameSyst[158] = "ElectronMomDown";
  nameSyst[159] = "metJERUp";
  nameSyst[160] = "metJERDown";
  nameSyst[161] = "metJESUp";
  nameSyst[162] = "metJESDown";
  nameSyst[163] = "metUnclusteredUp";
  nameSyst[164] = "metUnclusteredDown";
  nameSyst[165] = "JesSubTotalPileUpUp";
  nameSyst[166] = "JesSubTotalPileUpDown";
  nameSyst[167] = "JesSubTotalRelativeUp";
  nameSyst[168] = "JesSubTotalRelativeDown";
  nameSyst[169] = "JesSubTotalPtUp";
  nameSyst[170] = "JesSubTotalPtDown";
  nameSyst[171] = "JesSubTotalScaleUp";
  nameSyst[172] = "JesSubTotalScaleDown";
  nameSyst[173] = "JesFlavorQCDUp";
  nameSyst[174] = "JesFlavorQCDDown";
  nameSyst[175] = "JesTimePtEtaUp";
  nameSyst[176] = "JesTimePtEtaDown";

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
        // PU
        systValue = histo_Syst[19][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[18][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // Jes
        systValue = histo_Syst[152][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[151][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // Jer
        systValue = (histo_Syst[154][ic]->GetBinContent(nb)-histo_Baseline[ic]->GetBinContent(nb))/5.0;
        histo_Syst[154][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)+systValue);
        systValue = histo_Syst[154][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[153][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // MuonMom
        systValue = histo_Syst[156][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[155][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // ElectronMom
        systValue = histo_Syst[158][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[157][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // metJER
        systValue = histo_Syst[160][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[159][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // metJES
        systValue = histo_Syst[162][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[161][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // metUnclustered
        systValue = histo_Syst[164][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[163][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // JesSubTotalPileUp
        systValue = histo_Syst[166][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[165][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // JesSubTotalRelative
        systValue = histo_Syst[168][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[167][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // JesSubTotalPt
        systValue = histo_Syst[170][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[169][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // JesSubTotalScale
        systValue = histo_Syst[172][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[171][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // JesFlavorQCD
        systValue = histo_Syst[174][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[173][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
        // JesTimePtEta
        systValue = histo_Syst[176][ic]->GetBinContent(nb) / histo_Baseline[ic]->GetBinContent(nb);
        if(systValue > 0) histo_Syst[175][ic]->SetBinContent(nb,histo_Baseline[ic]->GetBinContent(nb)/systValue);
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

  //newcardShape << Form("BtagSFBC_00 shape ");
  //for (int ic=0; ic<nPlotCategories; ic++){
  //  if(!histo_Baseline[ic]) continue;
  //  if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
  //  if(ic == kPlotNonPrompt) newcardShape << Form("- ");
  //  else                     newcardShape << Form("1.0 ");
  //}
  //newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_01 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_02 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_03 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_04 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_05 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_06 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_07 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_08 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_09 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_10 shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("BtagSFBC_11 shape ");
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

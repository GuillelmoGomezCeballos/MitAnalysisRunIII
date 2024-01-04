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

// whichAna = 0 (WZ), fidAna = 0 (SR), 1 (CR)
// whichAna = 0 (ZZ), fidAna = 0 (SR)

void makeVVDataCards(int whichAna = 0, int fidAna = 0, TString InputDir = "anaZ", TString anaSel = "wwAnalysis1001", int year = 20221, int srAna = 1){

  if(fidAna < 0 || fidAna > 2) printf("Wrong fidAna(%d)\n",fidAna);

  plotBaseNames[kPlotNonPrompt] = "NonPromptWZ";

  int jumpValue = 200;

  double systValue;
  TFile *inputFile;
  TFile *outputFile;
  const int nSystTotal = 177;

  TH1D *histo_Baseline[nPlotCategories];
  TH1D *histo_QCDScaleUp[nPlotCategories];
  TH1D *histo_QCDScaleDown[nPlotCategories];
  TH1D *histo_PSUp[nPlotCategories];
  TH1D *histo_PSDown[nPlotCategories];

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

  int BinXF = 4; double minXF = -0.5; double maxXF = 3.5;

  if(anaSel.Contains("zzAnalysis")) {
    printf("Modifying default binning\n");
    BinXF = 3; minXF = -0.5; maxXF = 2.5;
  }

  for(int ic=0; ic<nPlotCategories; ic++) {
    histo_Baseline[ic] = new TH1D(Form("histo_%s",plotBaseNames[ic].Data()),Form("histo_%s",plotBaseNames[ic].Data()), BinXF, minXF, maxXF);
    TString plotBaseNamesTemp =  plotBaseNames[ic];
    histo_QCDScaleUp  [ic] = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_QCDScale_%s_ACCEPTUp"  , plotBaseNames[ic].Data(), plotBaseNamesTemp.Data()));
    histo_QCDScaleDown[ic] = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_QCDScale_%s_ACCEPTDown", plotBaseNames[ic].Data(), plotBaseNamesTemp.Data()));
    histo_PSUp  [ic]       = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_PS_%s_ACCEPTUp"  , plotBaseNames[ic].Data(), plotBaseNamesTemp.Data()));
    histo_PSDown[ic]       = (TH1D*)histo_Baseline[ic]->Clone(Form("histo_%s_PS_%s_ACCEPTDown", plotBaseNames[ic].Data(), plotBaseNamesTemp.Data()));
  }

  for(int j=0; j<nSystTotal; j++){
    for(int ic=0; ic<nPlotCategories; ic++) histo_Syst[j][ic] = new TH1D(Form("histo_%s_%s",plotBaseNames[ic].Data(),nameSyst[j].Data()),Form("histo_%s_%s",plotBaseNames[ic].Data(),nameSyst[j].Data()), BinXF, minXF, maxXF);
  }
  for(int j=0; j<101; j++){
    for(int ic=0; ic<nPlotCategories; ic++) histo_PDFUp  [j][ic] = new TH1D(Form("histo_%s_PDF%dUp"  ,plotBaseNames[ic].Data(),j),Form("histo_%s_PDF%dUp"  ,plotBaseNames[ic].Data(),j), BinXF, minXF, maxXF);
    for(int ic=0; ic<nPlotCategories; ic++) histo_PDFDown[j][ic] = new TH1D(Form("histo_%s_PDF%dDown",plotBaseNames[ic].Data(),j),Form("histo_%s_PDF%dDown",plotBaseNames[ic].Data(),j), BinXF, minXF, maxXF);
  }

  inputFile = new TFile(Form("%s/fillhisto_%s_%d_%d.root",InputDir.Data(),anaSel.Data(),year,300+fidAna*jumpValue), "read");
  for(unsigned ic=kPlotData; ic!=nPlotCategories; ic++) {
    histo_Baseline[ic] = (TH1D*)inputFile->Get(Form("histo%d", ic)); assert(histo_Baseline[ic]); histo_Baseline[ic]->SetDirectory(0);
    histo_Baseline[ic]->SetNameTitle(Form("histo_%s",plotBaseNames[ic].Data()),Form("histo_%s",plotBaseNames[ic].Data()));
  }
  delete inputFile;

  for(int j=0; j<nSystTotal; j++){
    inputFile = new TFile(Form("%s/fillhisto_%s_%d_%d.root",InputDir.Data(),anaSel.Data(),year,300+fidAna*jumpValue+1+j), "read");
    for(unsigned ic=kPlotData; ic!=nPlotCategories; ic++) {
      histo_Syst[j][ic] = (TH1D*)inputFile->Get(Form("histo%d", ic)); assert(histo_Syst[j][ic]); histo_Syst[j][ic]->SetDirectory(0);
      histo_Syst[j][ic]->SetNameTitle(Form("histo_%s_%s",plotBaseNames[ic].Data(),nameSyst[j].Data()),Form("histo_%s_%s",plotBaseNames[ic].Data(),nameSyst[j].Data()));
    }
    delete inputFile;
  }

  for(unsigned ic=0; ic<nPlotCategories; ic++) {
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
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
  namenonPromptSyst[ 0] = "nonPromptWZMuonAlt0Up";
  namenonPromptSyst[ 1] = "nonPromptWZMuonAlt1Down";
  namenonPromptSyst[ 2] = "nonPromptWZMuonAlt2Up";
  namenonPromptSyst[ 3] = "nonPromptWZElectronAlt0Up";
  namenonPromptSyst[ 4] = "nonPromptWZElectronAlt1Up";
  namenonPromptSyst[ 5] = "nonPromptWZElectronAlt2Up";
  namenonPromptSyst[ 6] = "nonPromptWZMuonAlt0Down";
  namenonPromptSyst[ 7] = "nonPromptWZMuonAlt1Up";
  namenonPromptSyst[ 8] = "nonPromptWZMuonAlt2Down";
  namenonPromptSyst[ 9] = "nonPromptWZElectronAlt0Down";
  namenonPromptSyst[10] = "nonPromptWZElectronAlt1Down";
  namenonPromptSyst[11] = "nonPromptWZElectronAlt2Down";
  const int totalNumberFakeSyst = 6;
  TH1D *histo_InputNonPromtUnc[totalNumberFakeSyst];
  TH1D *histo_NonPromtUnc[nNonPromptSyst];
  if(anaSel.Contains("wzAnalysis")){
    inputFile = new TFile(Form("%s/fillhisto_%s_%d_nonprompt.root",InputDir.Data(),anaSel.Data(),year), "read");
    int startH = 0; if(fidAna == 1) startH = totalNumberFakeSyst;
    for(int j=0; j<totalNumberFakeSyst; j++){
      histo_InputNonPromtUnc[j] = (TH1D*)inputFile->Get(Form("histoNonPrompt_%d", j+startH));
      histo_NonPromtUnc[j+                  0] = (TH1D*)histo_InputNonPromtUnc[j]->Clone(Form("histo_%s_%s", plotBaseNames[kPlotNonPrompt].Data(), namenonPromptSyst[j+                  0].Data())); histo_NonPromtUnc[j+		    0]->SetDirectory(0);
      histo_NonPromtUnc[j+totalNumberFakeSyst] = (TH1D*)histo_InputNonPromtUnc[j]->Clone(Form("histo_%s_%s", plotBaseNames[kPlotNonPrompt].Data(), namenonPromptSyst[j+totalNumberFakeSyst].Data())); histo_NonPromtUnc[j+totalNumberFakeSyst]->SetDirectory(0);
    }
    delete inputFile;

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
  }
  // End Nonprompt study

  TString additionalSuffix = "";
  if(whichAna != 0){ 
    additionalSuffix = "_alt";
  }

  TString outputLimits = Form("output_%s_%d_bin%d%s.root",anaSel.Data(),year,fidAna,additionalSuffix.Data());
  outputFile = new TFile(outputLimits, "RECREATE");
  outputFile->cd();
  for(unsigned ic=kPlotData; ic!=nPlotCategories; ic++) {
    if(histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    histo_Baseline[ic]->Write();
    for(int j=0; j<nSystTotal; j++) histo_Syst[j][ic]->Write();

    histo_QCDScaleUp  [ic]->Write();
    histo_QCDScaleDown[ic]->Write();
    histo_PSUp        [ic]->Write();
    histo_PSDown      [ic]->Write();
    for(int npdf=0; npdf<101; npdf++){
      histo_PDFUp  [npdf][ic]->Write();
      histo_PDFDown[npdf][ic]->Write();
    }
  }
  if(anaSel.Contains("wzAnalysis")) for(int j=0; j<nNonPromptSyst; j++) histo_NonPromtUnc[j]->Write();
  outputFile->Close();

  // Filling datacards txt file
  char outputLimitsCard[200];
  sprintf(outputLimitsCard,"datacard_%s_%d_bin%d%s.txt",anaSel.Data(),year,fidAna,additionalSuffix.Data());
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
    newcardShape << Form("ch%d ",fidAna);

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
    if     ((ic != kPlotWZ &&
             ic != kPlotZZ) || srAna == 0
            ) newcardShape << Form("%d  ", ic);
    else if(ic == kPlotWZ) newcardShape << Form("%d  ", -1);
    else if(ic == kPlotZZ) newcardShape << Form("%d  ", -2);
  }
  newcardShape << Form("\n");

  newcardShape << Form("rate  ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    newcardShape << Form("%f  ", histo_Baseline[ic]->GetSumOfWeights());
  }
  newcardShape << Form("\n");

  if(anaSel.Contains("wzAnalysis")){
    bool isTraditionalSyst = false;
    if(isTraditionalSyst == true){
      newcardShape << Form("nonPromptWZMuon      lnN     ");
      for (int ic=0; ic<nPlotCategories; ic++){
        if(!histo_Baseline[ic]) continue;
        if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
        if(ic == kPlotNonPrompt) newcardShape << Form("%6.3f ",1.15);
        else                     newcardShape << Form("- "); 
      }
      newcardShape << Form("\n");

      newcardShape << Form("nonPromptWZElectron	lnN	");
      for (int ic=0; ic<nPlotCategories; ic++){
        if(!histo_Baseline[ic]) continue;
        if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
        if(ic == kPlotNonPrompt) newcardShape << Form("%6.3f ",1.15);
        else                     newcardShape << Form("- ");
      }
      newcardShape << Form("\n");
    } // isTraditionalSyst == true
    else {
      newcardShape << Form("nonPromptWZMuonAlt0 shape ");
      for (int ic=0; ic<nPlotCategories; ic++){
        if(!histo_Baseline[ic]) continue;
        if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
        if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
        else                     newcardShape << Form("- "); 
      }
      newcardShape << Form("\n");

      newcardShape << Form("nonPromptWZMuonAlt1 shape ");
      for (int ic=0; ic<nPlotCategories; ic++){
        if(!histo_Baseline[ic]) continue;
        if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
        if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
        else                     newcardShape << Form("- "); 
      }
      newcardShape << Form("\n");

      newcardShape << Form("nonPromptWZMuonAlt2 shape ");
      for (int ic=0; ic<nPlotCategories; ic++){
        if(!histo_Baseline[ic]) continue;
        if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
        if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
        else                     newcardShape << Form("- "); 
      }
      newcardShape << Form("\n");

      newcardShape << Form("nonPromptWZElectronAlt0 shape ");
      for (int ic=0; ic<nPlotCategories; ic++){
        if(!histo_Baseline[ic]) continue;
        if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
        if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
        else                     newcardShape << Form("- "); 
      }
      newcardShape << Form("\n");

      newcardShape << Form("nonPromptWZElectronAlt1 shape ");
      for (int ic=0; ic<nPlotCategories; ic++){
        if(!histo_Baseline[ic]) continue;
        if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
        if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
        else                     newcardShape << Form("- "); 
      }
      newcardShape << Form("\n");

      newcardShape << Form("nonPromptWZElectronAlt2 shape ");
      for (int ic=0; ic<nPlotCategories; ic++){
        if(!histo_Baseline[ic]) continue;
        if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
        if(ic == kPlotNonPrompt) newcardShape << Form("1.0 ");
        else                     newcardShape << Form("- "); 
      }
      newcardShape << Form("\n");
    } // isTraditionalSyst == false
  }

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
    else                     newcardShape << Form("1.0 ");
  }
  newcardShape << Form("\n");

  newcardShape << Form("MuoSFISO shape ");
  for (int ic=0; ic<nPlotCategories; ic++){
    if(!histo_Baseline[ic]) continue;
    if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    if(ic == kPlotNonPrompt) newcardShape << Form("- ");
    else                     newcardShape << Form("1.0 ");
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

  if(anaSel.Contains("wzAnalysis")){
    newcardShape << Form("metJER shape ");
    for (int ic=0; ic<nPlotCategories; ic++){
      if(!histo_Baseline[ic]) continue;
      if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
      if(ic == kPlotNonPrompt) newcardShape << Form("- ");
      else                     newcardShape << Form("1.0 ");
    }
    newcardShape << Form("\n");

    newcardShape << Form("metJES shape ");
    for (int ic=0; ic<nPlotCategories; ic++){
      if(!histo_Baseline[ic]) continue;
      if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
      if(ic == kPlotNonPrompt) newcardShape << Form("- ");
      else                     newcardShape << Form("1.0 ");
    }
    newcardShape << Form("\n");

    newcardShape << Form("metUnclustered shape ");
    for (int ic=0; ic<nPlotCategories; ic++){
      if(!histo_Baseline[ic]) continue;
      if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
      if(ic == kPlotNonPrompt) newcardShape << Form("- ");
      else                     newcardShape << Form("1.0 ");
    }
    newcardShape << Form("\n");
  }

  for(unsigned ic=0; ic<nPlotCategories; ic++) {
    if(ic== kPlotData || ic == kPlotNonPrompt || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    newcardShape << Form("QCDScale_%s_ACCEPT shape ",plotBaseNames[ic].Data());
    for(unsigned ic2=0; ic2<nPlotCategories; ic2++) {
      if(ic2 == kPlotData || histo_Baseline[ic2]->GetSumOfWeights() <= 0) continue;
      if(ic==ic2) newcardShape << Form("1.0  ");
      else        newcardShape << Form("-  ");
      }
      newcardShape << Form("\n");
  } 

  for(unsigned ic=0; ic<nPlotCategories; ic++) {
    if(ic== kPlotData || ic == kPlotNonPrompt || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
    newcardShape << Form("PS_%s_ACCEPT shape ",plotBaseNames[ic].Data());
    for(unsigned ic2=0; ic2<nPlotCategories; ic2++) {
      if(ic2 == kPlotData || histo_Baseline[ic2]->GetSumOfWeights() <= 0) continue;
      if(ic==ic2) newcardShape << Form("1.0  ");
      else        newcardShape << Form("-  ");
      }
      newcardShape << Form("\n");
  } 

  for(int npdf=0; npdf<=100; npdf++){
    newcardShape << Form("PDF%d shape ",npdf);
    for (int ic=0; ic<nPlotCategories; ic++){
      if(!histo_Baseline[ic]) continue;
      if(ic == kPlotData || histo_Baseline[ic]->GetSumOfWeights() <= 0) continue;
      if(ic == kPlotNonPrompt) newcardShape << Form("- ");
      else                     newcardShape << Form("1.0 ");
    }
    newcardShape << Form("\n");
  }

  //newcardShape << Form("CMS_ww_wznorm  rateParam * %s 1 [0.1,4.9]\n",plotBaseNames[kPlotWZ].Data());
  //newcardShape << Form("CMS_ww_zznorm  rateParam * %s 1 [0.1,4.9]\n",plotBaseNames[kPlotZZ].Data());
  //newcardShape << Form("CMS_ww_wzbnorm rateParam * %s 1 [0.1,4.9]\n",plotBaseNames[kPlotTVX].Data());

  newcardShape << Form("ch%d autoMCStats 0\n",fidAna);

  newcardShape.close();

}

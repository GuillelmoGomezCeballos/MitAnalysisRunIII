#include "TROOT.h"
#include "TInterpreter.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TStyle.h"
#include "TPad.h"
#include "Math/QuantFuncMathCore.h"
#include "TMath.h"
#include "TGraphAsymmErrors.h"
#include "TSystem.h"
#include "TLegend.h"
#include <iostream>

void computeGenWWXS(TString input = "", int selectType = 0, bool doPDFRMS = false, bool debug = false){

  TH1D *histo_RMSPDF = new TH1D("histo_RMSPDF", "histo_RMSPDF", 200, 0.90, 1.10);

  const int number_unc_PS       = 4;
  const int number_unc_QCDScale = 6;
  const int number_unc_PDF      = 101;

  int startFX=0; int startFY=10; // WW fiducial
  if     (selectType ==  1) {startFY=1;} // No requirements
  else if(selectType ==  2) {startFY=2;} // mZ requirement
  else if(selectType ==  3) {startFY=3;} // mZ + 3l requirements
  else if(selectType >= 10) {startFY=selectType;} // WW fiducial measurements

  TString nameH = "WWNJETS";
  if     (selectType ==  0) {nameH = "WWNJETS";}
  else if(selectType ==  1) {nameH = "WWINC";}
  else if(selectType ==  2) {nameH = "ZINC";}
  else if(selectType ==  3) {nameH = "WZINC";}
  else if(selectType == 10) {nameH = "WWNJETS";}
  else if(selectType == 11) {nameH = "WWPTL1";}
  else if(selectType == 12) {nameH = "WWPTL2";}
  else if(selectType == 13) {nameH = "WWMLL";}
  else if(selectType == 14) {nameH = "WWPTLL";}
  else if(selectType == 15) {nameH = "WWPTWW";}
  else if(selectType == 16) {nameH = "WWNJET";}
  else if(selectType == 17) {nameH = "WWPTJ1";}
  else if(selectType == 18) {nameH = "WWPTJ2";}
  else if(selectType == 19) {nameH = "WWMJJ";}
  else if(selectType == 20) {nameH = "WWDPHIJJ";}
  else {printf("WRONG OPTION!\n"); return;}

  TString output = Form("xswwgen_%s.root",nameH.Data());

  TH1D *histo_Baseline;
  TH1D *histo_PS[number_unc_PS];
  TH1D *histo_QCDScale[number_unc_QCDScale];
  TH1D *histo_PDF[number_unc_PDF];
  TH1D *histo_PS_unc;
  TH1D *histo_QCDScale_unc;
  TH1D *histo_PDF_unc;

  TFile *_fileGenWW = TFile::Open(Form("%s",input.Data()));
  histo_Baseline = (TH1D*)_fileGenWW->Get(Form("histo_%d_%d",startFX+0,startFY));
  for(int i=0; i<number_unc_PS; i++)       histo_PS[i]       = (TH1D*)_fileGenWW->Get(Form("histo_%d_%d",startFX+1+i,startFY));
  for(int i=0; i<number_unc_QCDScale; i++) histo_QCDScale[i] = (TH1D*)_fileGenWW->Get(Form("histo_%d_%d",startFX+1+number_unc_PS+i,startFY));
  for(int i=0; i<number_unc_PDF; i++)      histo_PDF[i]      = (TH1D*)_fileGenWW->Get(Form("histo_%d_%d",startFX+1+number_unc_PS+number_unc_QCDScale+i,startFY));

  histo_PS_unc       = (TH1D*)histo_Baseline->Clone();
  histo_QCDScale_unc = (TH1D*)histo_Baseline->Clone();
  histo_PDF_unc      = (TH1D*)histo_Baseline->Clone();
  histo_Baseline    ->SetNameTitle(Form("hD%s",nameH.Data())    ,Form("hD%s",nameH.Data())    );
  histo_PS_unc      ->SetNameTitle(Form("hD%s_PS",nameH.Data()) ,Form("hD%s_PS",nameH.Data()) );
  histo_QCDScale_unc->SetNameTitle(Form("hD%s_QCD",nameH.Data()),Form("hD%s_QCD",nameH.Data()));
  histo_PDF_unc     ->SetNameTitle(Form("hD%s_PDF",nameH.Data()),Form("hD%s_PDF",nameH.Data()));


  for(int nb=1; nb<=histo_Baseline->GetNbinsX(); nb++){

    // compute PS uncertainties bin-by-bin
    double diffPS[number_unc_PS] = {
     TMath::Abs(histo_PS[0]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb)),
     TMath::Abs(histo_PS[1]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb)),
     TMath::Abs(histo_PS[2]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb)),
     TMath::Abs(histo_PS[3]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb))};

    double systPS = diffPS[0];
    if(debug) printf("diffPS(%d): %.3f %.3f\n",0,diffPS[0]/histo_Baseline->GetBinContent(nb),systPS/histo_Baseline->GetBinContent(nb));
    for(int nps=1; nps<number_unc_PS; nps++) {
      if(diffPS[nps] > systPS) systPS = diffPS[nps];
      if(debug) printf("diffPS(%d): %.3f %.3f\n",nps,diffPS[nps]/histo_Baseline->GetBinContent(nb),systPS/histo_Baseline->GetBinContent(nb));
    }

    if(histo_Baseline->GetBinContent(nb) > 0) 
      systPS = 1.0+systPS/histo_Baseline->GetBinContent(nb);
    else systPS = 1;

    // compute QCD scale uncertainties bin-by-bin
    double diffQCDScale[number_unc_QCDScale] = {
     TMath::Abs(histo_QCDScale[0]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb)),
     TMath::Abs(histo_QCDScale[1]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb)),
     TMath::Abs(histo_QCDScale[2]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb)),
     TMath::Abs(histo_QCDScale[3]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb)),
     TMath::Abs(histo_QCDScale[4]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb)),
     TMath::Abs(histo_QCDScale[5]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb))};

    double systQCDScale = diffQCDScale[0];
    if(debug) printf("diffQCDScale(%d): %.3f %.3f\n",0,diffQCDScale[0]/histo_Baseline->GetBinContent(nb),systQCDScale/histo_Baseline->GetBinContent(nb));
    for(int nqcd=1; nqcd<number_unc_QCDScale; nqcd++) {
      if(diffQCDScale[nqcd] > systQCDScale) systQCDScale = diffQCDScale[nqcd];
      if(debug) printf("diffQCDScale(%d): %.3f %.3f\n",nqcd,diffQCDScale[nqcd]/histo_Baseline->GetBinContent(nb),systQCDScale/histo_Baseline->GetBinContent(nb));
    }

    if(histo_Baseline->GetBinContent(nb) > 0) 
      systQCDScale = 1.0+systQCDScale/histo_Baseline->GetBinContent(nb);
    else systQCDScale = 1;

    double systPDF = 0.0;
    // compute PDF uncertainties bin-by-bin
    if(histo_Baseline->GetBinContent(nb) <= 0){
      systPDF = 1;
    }
    else if(doPDFRMS == false){
      for(int i=0; i<number_unc_PDF; i++) {
        double diff = TMath::Abs(histo_PDF[i]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb));
        systPDF = systPDF + TMath::Power(diff,2);
        //printf("%d %d %f %f\n",nb,i,diff,sqrt(systPDF));
      }
      systPDF = sqrt(systPDF);

      systPDF = 1.0+systPDF/histo_Baseline->GetBinContent(nb);
    }
    else {
      histo_RMSPDF->Reset();
      for(int i=0; i<number_unc_PDF; i++) {
        //double diff = TMath::Abs(histo_PDF[i]->GetBinContent(nb)-histo_Baseline->GetBinContent(nb))/histo_Baseline->GetBinContent(nb);
        double diff = histo_PDF[i]->GetBinContent(nb)/histo_Baseline->GetBinContent(nb);
        histo_RMSPDF->Fill(diff);
      }
      systPDF = 1.0 + histo_RMSPDF->GetRMS();
      //printf("%d %f %f\n",nb,histo_RMSPDF->GetMean(),histo_RMSPDF->GetRMS());
    }

    histo_PS_unc      ->SetBinContent(nb, histo_Baseline->GetBinContent(nb)*systPS);
    histo_QCDScale_unc->SetBinContent(nb, histo_Baseline->GetBinContent(nb)*systQCDScale);
    histo_PDF_unc     ->SetBinContent(nb, histo_Baseline->GetBinContent(nb)*systPDF);

    double tot = sqrt((systPS-1)*(systPS-1)+(systQCDScale-1)*(systQCDScale-1)+(systPDF-1)*(systPDF-1));
    printf("bin(%2d): %6.1f / %.3f %.3f %.3f / %.3f %6.1f\n",nb,histo_Baseline->GetBinContent(nb),systPS-1,systQCDScale-1,systPDF-1,tot,histo_Baseline->GetBinContent(nb)*tot);
  }
  double tot = sqrt((histo_PS_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1)*(histo_PS_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1)+(histo_QCDScale_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1)*(histo_QCDScale_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1)+(histo_PDF_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1)*(histo_PDF_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1));
  printf("bin(%2d): %6.1f / %.3f %.3f %.3f / %.3f %6.1f\n",0,histo_Baseline->GetSumOfWeights(),histo_PS_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1,histo_QCDScale_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1,histo_PDF_unc->GetSumOfWeights()/histo_Baseline->GetSumOfWeights()-1,tot,histo_Baseline->GetSumOfWeights()*tot);
  TFile *outputFile = TFile::Open(Form("%s",output.Data()),"recreate");
  outputFile->cd();
  histo_Baseline    ->Write();
  histo_PS_unc      ->Write();
  histo_QCDScale_unc->Write();
  histo_PDF_unc     ->Write();
  outputFile->Close();
}

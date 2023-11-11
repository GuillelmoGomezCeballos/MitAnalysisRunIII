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

void computeGenPtWWUnc(TString input = ""){

  const int number_unc = 5;
  int startF=20;
  TH1D *histo_Baseline;
  TH1D *histo_PTWWUnc[number_unc];

  TFile *_fileGenWW = TFile::Open(Form("%s",input.Data()));
  histo_Baseline = (TH1D*)_fileGenWW->Get(Form("histo_%d_0",startF+0));
  for(int i=0; i<number_unc; i++) {
    histo_PTWWUnc[i] = (TH1D*)_fileGenWW->Get(Form("histo_%d_0",134+i));
  }
  double scaleFactor = histo_Baseline->GetSumOfWeights()/histo_PTWWUnc[0]->GetSumOfWeights();

  printf("===> Overall yields\n");
  printf("%5.1f ",histo_Baseline->GetSumOfWeights());
  for(int i=0; i<number_unc; i++) {
    printf("| %6.1f ",histo_PTWWUnc[i]->GetSumOfWeights());
    histo_PTWWUnc[i]->Scale(scaleFactor);
    printf(" %6.1f ",histo_PTWWUnc[i]->GetSumOfWeights());
  }
  printf("\n");

  printf("===> Overall uncertainties\n");
  for(int nb=1; nb<=histo_Baseline->GetNbinsX(); nb++){
    printf("bin(%d) ",nb);
    for(int i=0; i<number_unc; i++) {
      printf("%.3f ",histo_PTWWUnc[i]->GetBinContent(nb)/histo_Baseline->GetBinContent(nb));
    }
    printf("\n");
  }

  histo_Baseline->Scale(1./histo_Baseline->GetSumOfWeights());
  for(int i=0; i<number_unc; i++) {
    histo_PTWWUnc[i]->Scale(1./histo_PTWWUnc[i]->GetSumOfWeights());
  }

  printf("===> Relative uncertainties\n");
  for(int nb=1; nb<=histo_Baseline->GetNbinsX(); nb++){
    printf("bin(%d) ",nb);
    for(int i=0; i<number_unc; i++) {
      printf("%.3f ",histo_PTWWUnc[i]->GetBinContent(nb)/histo_Baseline->GetBinContent(nb));
    }
    printf("\n");
  }
  printf("===> Relative symmetric uncertainties\n");
  for(int nb=1; nb<=histo_Baseline->GetNbinsX(); nb++){
    printf("bin(%d) ",nb);
    printf("%.3f %.3f | %.3f %.3f",
    1.0+(histo_PTWWUnc[1]->GetBinContent(nb)-histo_PTWWUnc[2]->GetBinContent(nb))/histo_PTWWUnc[0]->GetBinContent(nb)/2.,
    1.0+(histo_PTWWUnc[3]->GetBinContent(nb)-histo_PTWWUnc[4]->GetBinContent(nb))/histo_PTWWUnc[0]->GetBinContent(nb)/2.,
    1.0+(histo_PTWWUnc[1]->GetBinContent(nb)-histo_PTWWUnc[2]->GetBinContent(nb))/histo_Baseline->GetBinContent(nb)/2.,
    1.0+(histo_PTWWUnc[3]->GetBinContent(nb)-histo_PTWWUnc[4]->GetBinContent(nb))/histo_Baseline->GetBinContent(nb)/2.);
    printf("\n");
  }
}

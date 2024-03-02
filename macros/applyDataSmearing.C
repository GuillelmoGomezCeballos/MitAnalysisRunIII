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

void theApplyDataSmearing(TString inputName, double factor = 2.0){
  TFile* file = new TFile(inputName, "read");
  const int nPlotCategories = 24;
  TH1F* _hist[nPlotCategories];
  
  for(int ic=0; ic<nPlotCategories; ic++){
    _hist[ic] = (TH1F*)file->Get(Form("histo%d",ic));
  }
  TH1F* hBck = (TH1F*)_hist[0]->Clone(Form("hBck"));
  hBck->Scale(0);
  for(int ic=1; ic<nPlotCategories; ic++){
    hBck->Add(_hist[ic]);
  }

  for(int nb=1; nb<=_hist[0]->GetNbinsX(); nb++){
    double systValue = 1.0+(_hist[0]->GetBinContent(nb)/hBck->GetBinContent(nb)-1.0)/factor;
    //hBck->SetBinContent(nb,hBck->GetBinContent(nb)+systValue);
    //printf("DA/MC = %d %f\n",nb, systValue);
    for(int ic=1; ic<nPlotCategories; ic++){
      _hist[ic]->SetBinContent(nb,_hist[ic]->GetBinContent(nb)*systValue);
    }
  }

  //while(_hist[0]->GetSumOfWeights() < hBck->GetSumOfWeights()){
  //  _hist[0]->Fill(hBck->GetRandom());
  //}

  double sumBck = 0;
  TString outputName = inputName.ReplaceAll(".root","_alt.root");
  TFile output(outputName,"RECREATE");
  for(int ic=0; ic<nPlotCategories; ic++){
    _hist[ic]->Write();
    if(ic!=0) sumBck = sumBck + _hist[ic]->GetSumOfWeights();
  }
  output.Close();
  //printf("DA/MC = %f/%f\n", _hist[0]->GetSumOfWeights(),sumBck);
}

void applyDataSmearing(int nsel = 0){
  if(nsel == 0){
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20220_243.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20220_244.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20220_245.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20221_243.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20221_244.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20221_245.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20220_255.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20220_256.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20220_257.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20221_255.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20221_256.root");
    theApplyDataSmearing("anaZ/fillhisto_zAnalysis1001_20221_257.root");

    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20220_243_alt.root anaZ/fillhisto_zAnalysis1001_20220_243.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20220_244_alt.root anaZ/fillhisto_zAnalysis1001_20220_244.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20220_245_alt.root anaZ/fillhisto_zAnalysis1001_20220_245.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20221_243_alt.root anaZ/fillhisto_zAnalysis1001_20221_243.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20221_244_alt.root anaZ/fillhisto_zAnalysis1001_20221_244.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20221_245_alt.root anaZ/fillhisto_zAnalysis1001_20221_245.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20220_255_alt.root anaZ/fillhisto_zAnalysis1001_20220_255.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20220_256_alt.root anaZ/fillhisto_zAnalysis1001_20220_256.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20220_257_alt.root anaZ/fillhisto_zAnalysis1001_20220_257.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20221_255_alt.root anaZ/fillhisto_zAnalysis1001_20221_255.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20221_256_alt.root anaZ/fillhisto_zAnalysis1001_20221_256.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_zAnalysis1001_20221_257_alt.root anaZ/fillhisto_zAnalysis1001_20221_257.root"));
  }
  else if(nsel == 1){
    theApplyDataSmearing("anaZ/fillhisto_wwAnalysis1001_20220_62.root",3.0);
    theApplyDataSmearing("anaZ/fillhisto_wwAnalysis1001_20220_63.root",3.0);
    theApplyDataSmearing("anaZ/fillhisto_wwAnalysis1001_20221_62.root",3.0);
    theApplyDataSmearing("anaZ/fillhisto_wwAnalysis1001_20221_63.root",3.0);

    gSystem->Exec(Form("mv anaZ/fillhisto_wwAnalysis1001_20220_62_alt.root anaZ/fillhisto_wwAnalysis1001_20220_62.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_wwAnalysis1001_20220_63_alt.root anaZ/fillhisto_wwAnalysis1001_20220_63.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_wwAnalysis1001_20221_62_alt.root anaZ/fillhisto_wwAnalysis1001_20221_62.root"));
    gSystem->Exec(Form("mv anaZ/fillhisto_wwAnalysis1001_20221_63_alt.root anaZ/fillhisto_wwAnalysis1001_20221_63.root"));
 }
}

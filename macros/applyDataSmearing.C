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

//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20220_243.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20220_244.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20220_245.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20221_243.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20221_244.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20221_245.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20220_255.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20220_256.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20220_257.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20221_255.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20221_256.root")'
//root -q -l -b ~/cms/MitAnalysisRunIII/macros/applyDataSmearing.C'("fillhisto_zAnalysis1001_20221_257.root")'
void applyDataSmearing(TString inputName){
  TFile* file = new TFile(inputName, "read");
  const int nPlotCategories = 24;
  TH1F* _hist[nPlotCategories];
  TH1F* hBck = 0;
  
  for(int ic=0; ic<nPlotCategories; ic++){
    _hist[ic] = (TH1F*)file->Get(Form("histo%d",ic));
  }
  TH1F* _histData = (TH1F*)_hist[0]->Clone(Form("_histData"));
  _hist[0]->Scale(0);
  hBck  = (TH1F*)_hist[0]->Clone("hBck");
  for(int ic=1; ic<nPlotCategories; ic++){
    hBck->Add(_hist[ic]);
  }

  for(int nb=1; nb<=_histData->GetNbinsX(); nb++){
    double systValue = (_histData->GetBinContent(nb)-hBck->GetBinContent(nb))/2.0;
    hBck->SetBinContent(nb,hBck->GetBinContent(nb)+systValue);
  }

  while(_hist[0]->GetSumOfWeights() < hBck->GetSumOfWeights()){
    _hist[0]->Fill(hBck->GetRandom());
  }

  TString outputName = inputName.ReplaceAll(".root","_alt.root");
  TFile output(outputName,"RECREATE");
  for(int ic=0; ic<nPlotCategories; ic++){
    _hist[ic]->Write();
  }
  output.Close();

}

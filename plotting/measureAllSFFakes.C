#include "Math/ProbFuncMathCore.h"
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
#include "TRandom.h"
#include "common.h"

void measureSFFakes(TString inputName){
  TFile* file = new TFile(inputName, "read");
  TH1F* _hist[nPlotCategories];
  
  for(int ic=0; ic<nPlotCategories; ic++){
    _hist[ic] = (TH1F*)file->Get(Form("histo%d",ic));
  }
  TH1F* hAll = (TH1F*)_hist[kPlotData]->Clone(Form("hAll"));
  hAll->Scale(0);
  TH1F* hBck = (TH1F*)_hist[kPlotData]->Clone(Form("hBck"));
  hBck->Scale(0);
  for(int ic=0; ic<nPlotCategories; ic++){
    if(ic == kPlotData) continue;
    hAll->Add(_hist[ic]);
    if(ic == kPlotNonPrompt) continue;
    hBck->Add(_hist[ic]);
  }

  for(int nb=1; nb<=_hist[0]->GetNbinsX(); nb++){
    printf("%3d %6.0f %8.1f %8.1f %8.1f ==> %5.2f %5.2f\n",nb,_hist[kPlotData]->GetBinContent(nb),hAll->GetBinContent(nb),hBck->GetBinContent(nb),_hist[kPlotNonPrompt]->GetBinContent(nb),_hist[kPlotData]->GetBinContent(nb)/hAll->GetBinContent(nb),(_hist[kPlotData]->GetBinContent(nb)-hBck->GetBinContent(nb))/_hist[kPlotNonPrompt]->GetBinContent(nb));
  }

  printf("All %6.0f %8.1f %8.1f %8.1f ==> %5.2f %5.2f\n",_hist[kPlotData]->GetSumOfWeights(),hAll->GetSumOfWeights(),hBck->GetSumOfWeights(),_hist[kPlotNonPrompt]->GetSumOfWeights(),_hist[kPlotData]->GetSumOfWeights()/hAll->GetSumOfWeights(),(_hist[kPlotData]->GetSumOfWeights()-hBck->GetSumOfWeights())/_hist[kPlotNonPrompt]->GetSumOfWeights());
}

void measureAllSFFakes(int nsel = -1, int condorJob = 1001, int year = 2027){
  TString inputFolder = "anaZ/";
  vector<TString> infileName_;
  if      (nsel == 30){
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_18", inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_116",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_117",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_118",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_119",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_120",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_121",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_122",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_123",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_124",inputFolder.Data(),condorJob,year));
  }
  else if(nsel == 31){
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_19", inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_125",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_126",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_127",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_128",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_129",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_130",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_131",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_132",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_sswwAnalysis%d_%d_133",inputFolder.Data(),condorJob,year));
  }
  else if(nsel == 80){
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_42", inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_150",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_151",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_152",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_153",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_154",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_155",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_156",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_157",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_158",inputFolder.Data(),condorJob,year));
  }
  else if(nsel == 81){
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_71", inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_160",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_161",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_162",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_163",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_164",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_165",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_166",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_167",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_168",inputFolder.Data(),condorJob,year));
  }
  else if(nsel == 82){
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_72", inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_170",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_171",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_172",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_173",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_174",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_175",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_176",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_177",inputFolder.Data(),condorJob,year));
    infileName_.push_back(Form("%sfillhisto_wwAnalysis%d_%d_178",inputFolder.Data(),condorJob,year));
  }
  else {
    return;
  }

  for(UInt_t ifile=0; ifile<infileName_.size(); ifile++) {
    printf("%s\n",infileName_[ifile].Data());
    measureSFFakes(Form("%s.root",infileName_[ifile].Data()));
  }
}

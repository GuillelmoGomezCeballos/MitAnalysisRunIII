#include "TROOT.h"
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
#include "CMS_lumi.C"
#include "TRandom.h"
#include "common.h"

void producingYields_fromHistograms(TString plotName = "/home/submit/ceballos/cards/combine_plots_madgraph_smp24001/ww_output_bin-1.root") {

  TFile* file = new TFile(plotName, "read");  if(!file) {printf("File %s does not exist\n",plotName.Data()); return;}
  TH1F* _hist[nPlotCategories];
  TH1F* _histo_total;
  for(int ic=0; ic<nPlotCategories; ic++){
    _hist[ic] = (TH1F*)file->Get(Form("histo%d",ic));
    _histo_total = (TH1F*)file->Get(Form("histo_total"));
  }
  for(int ic=0; ic<nPlotCategories; ic++){
    if(_hist[ic]) {
      if(ic == kPlotggWW ||
         ic == kPlotSignal0 || ic == kPlotSignal1 || ic == kPlotSignal2 ||
         ic == kPlotSignal3 || ic == kPlotSignal4 || ic == kPlotSignal5) {_hist[kPlotqqWW]->Add(_hist[ic]); _hist[ic]->Scale(0.0);}
      if(ic == kPlotTW) {_hist[kPlotTT]->Add(_hist[ic]); _hist[ic]->Scale(0.0);}
    }
  }
  for(int ic=0; ic<nPlotCategories; ic++){
    if(_hist[ic] && _hist[ic]->GetSumOfWeights() > 0.0) {
      printf("%20s & ",plotBaseNames[ic].Data());
      for(int i=1; i<=_hist[ic]->GetNbinsX(); i++){
        if(ic == kPlotData)             printf("      %6d         ",(int)_hist[ic]->GetBinContent(i));
        else                            printf(" %7.1f $\\pm$ %5.1f ",_hist[ic]->GetBinContent(i),_hist[ic]->GetBinError(i));
        if(i == _hist[ic]->GetNbinsX()) printf("\\\\"); else printf("&");
      }
      printf("\n");
    }
  }
  printf("%20s & ","Total");
  if(_histo_total && _histo_total->GetSumOfWeights() > 0.0) {
    for(int i=1; i<=_histo_total->GetNbinsX(); i++){
      printf(" %7.1f $\\pm$ %5.1f ",_histo_total->GetBinContent(i),_histo_total->GetBinError(i));
      if(i == _histo_total->GetNbinsX()) printf("\\\\"); else printf("&");
    }
  }
  printf("\n");

}

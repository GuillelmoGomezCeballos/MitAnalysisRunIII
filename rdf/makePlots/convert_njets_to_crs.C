#include "TROOT.h"
#include "TFile.h"
#include "TH1F.h"
#include "TColor.h"
#include <map>
#include "common.h"

void convert_njets_to_crs(){
  const int njets = 4;

  TFile *fileInput[njets];
  for(int nj=0; nj<njets; nj++) {
    fileInput[nj] = new TFile(Form("ww_output_bin%d.root",nj), "read");
  }

  TH1F* histo[njets][nPlotCategories];
  for(int nj=0; nj<njets; nj++) for(int nc=0; nc<nPlotCategories; nc++) histo[nj][nc] = NULL;

  for(int nj=0; nj<njets; nj++) {
    for(int nc=0; nc<nPlotCategories; nc++) {
      histo[nj][nc] = (TH1F*)fileInput[nj]->Get(Form("histo%d",nc));
    }
  }

  TH1F* _hist[nPlotCategories];
  for(int nc=0; nc<nPlotCategories; nc++) {
    _hist[nc] = new TH1F(Form("histo%d",nc), Form("histo%d",nc), 4, -0.5, 3.5);
  }

  for(int ncr=0; ncr<5; ncr++){
    TFile* outFileLimits = new TFile(Form("ww_output_cr%d.root",ncr),"recreate");
    outFileLimits->cd();
    for(int nc=0; nc<nPlotCategories; nc++) {
      if(!histo[0][nc]) continue;
      for(int nj=0; nj<njets; nj++) {
        _hist[nc]->SetBinContent(nj+1, histo[nj][nc]->GetBinContent(ncr+1));
        _hist[nc]->SetBinError  (nj+1, histo[nj][nc]->GetBinError  (ncr+1));
      }
      _hist[nc]->Write();
    }
    outFileLimits->Close();
  }
}
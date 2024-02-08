#include "TROOT.h"
#include "TFile.h"
#include "TH1F.h"
#include "TColor.h"
#include <map>
#include "common.h"

void convert_njets_to_crs(TString postfix = ""){
  const int njets = 4;

  TFile *fileInput[njets];
  for(int nj=0; nj<njets; nj++) {
    fileInput[nj] = new TFile(Form("ww_output_bin%d%s.root",nj,postfix.Data()), "read");
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

  if(strcmp(postfix.Data(),"_prefit")==0){
    _hist[kPlotTT]->SetBinContent(2+1, 4*histo[2][kPlotTT]->GetBinContent(1+1));
    _hist[kPlotTT]->SetBinContent(3+1, 4*histo[3][kPlotTT]->GetBinContent(1+1));
  }

  for(int ncr=0; ncr<5; ncr++){
    TFile* outFileLimits = new TFile(Form("ww_output_cr%d%s.root",ncr,postfix.Data()),"recreate");
    outFileLimits->cd();
    for(int nc=0; nc<nPlotCategories; nc++) {
      bool isNonZero = false;
      for(int nj=0; nj<njets; nj++) {
        if(!histo[nj][nc]) continue;
        isNonZero = true;
        _hist[nc]->SetBinContent(nj+1, histo[nj][nc]->GetBinContent(ncr+1));
        _hist[nc]->SetBinError  (nj+1, histo[nj][nc]->GetBinError  (ncr+1));

        if(strcmp(postfix.Data(),"_prefit")==0 && ncr == 1 && (nj == 2 || nj == 3) && nc == kPlotTT){
          _hist[nc]->SetBinContent(nj+1, 1.15*_hist[nc]->GetBinContent(nj+1));
        }

      }
      if(isNonZero == true) _hist[nc]->Write();
    }
    outFileLimits->Close();
  }
}

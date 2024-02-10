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

void producingYields(int jetBin = -1, TString mlfitResult = "/home/submit/ceballos/cards/ww_smp24001/logs_ana1001/fitDiagnosticsww_fid_normalized0_obs.root") {

  TFile *mlfit = TFile::Open(mlfitResult); assert(mlfit);

  const int chan = 8;  
  TString channelName[chan] = {"ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8"}; 
  const int regions = 5;

  double yields[regions][nPlotCategories], yieldsE[regions][nPlotCategories];
  bool nonZeroYields[nPlotCategories];
  double total[regions], totalE[regions];
  for(int ic=0; ic<nPlotCategories; ic++) nonZeroYields[ic] = false;
  for(int nr=0; nr<regions; nr++){
    for(int ic=0; ic<nPlotCategories; ic++){
      yields[nr][ic] = 0;
      yieldsE[nr][ic] = 0;
    }
    total[nr] = 0;
    totalE[nr] = 0;
  }

  TH1F* _hist[chan][nPlotCategories+1];
  for(int nc=0; nc<chan; nc++){
    bool passJetBin = false;
    if(jetBin == -1 || nc%4 == jetBin) passJetBin = true;
    if(!passJetBin) continue;
    for(int ic=0; ic<nPlotCategories; ic++){
      if(ic != kPlotData){
        _hist[nc][ic] = ((TH1F*)mlfit->Get(Form("shapes_fit_s/%s/%s",channelName[nc].Data(),plotBaseNames[ic].Data())));
        if(_hist[nc][ic]){
          for(int nr=0; nr<regions; nr++){
            int theIC = ic;
            if(ic == kPlotqqWW || ic == kPlotggWW ||
               ic == kPlotSignal0 || ic == kPlotSignal1 || ic == kPlotSignal2 ||
               ic == kPlotSignal3 || ic == kPlotSignal4 || ic == kPlotSignal5) theIC = kPlotqqWW;
            if(ic == kPlotTT || ic == kPlotTW) theIC = kPlotTT;
            yields[nr][theIC]  += _hist[nc][ic]->GetBinContent(nr+1);
            yieldsE[nr][theIC] += _hist[nc][ic]->GetBinError(nr+1);
            nonZeroYields[theIC] = true;
          } // loop over regions        
        }
      }
      else {
        nonZeroYields[kPlotData] = true;
        double x,y;
        TGraphAsymmErrors *gr = ((TGraphAsymmErrors*)mlfit->Get(Form("shapes_fit_s/%s/%s",channelName[nc].Data(),"data")));
        for(int nr=0; nr<regions; nr++){
          int a = gr->GetPoint(nr, x, y);
          yields[nr][ic]  += y;
          yieldsE[nr][ic] += y;
        }
      }
    } // loop over categories

    _hist[nc][nPlotCategories] = ((TH1F*)mlfit->Get(Form("shapes_fit_s/%s/%s",channelName[nc].Data(),"total")));
    for(int nr=0; nr<regions; nr++){
      total[nr]  += _hist[nc][nPlotCategories]->GetBinContent(nr+1);
      totalE[nr] += _hist[nc][nPlotCategories]->GetBinError(nr+1);
    } // loop over regions	  

  } // loop over jet bins

  for(int ic=0; ic<nPlotCategories; ic++){
    if(nonZeroYields[ic] == true) {
      printf("%20s & ",plotBaseNames[ic].Data());
      for(int nr=0; nr<regions; nr++){
        yieldsE[nr][kPlotData] = sqrt(yieldsE[nr][kPlotData]);
        if(ic == kPlotData) printf("      %6d         ",(int)yields[nr][ic]);
        else                printf(" %7.1f $\\pm$ %5.1f ",yields[nr][ic],yieldsE[nr][ic]);
        if(nr == regions-1) printf("\\\\"); else printf("&");
      }
      printf("\n");
    }
  }
  printf("%20s & ","Total");
  for(int nr=0; nr<regions; nr++){
    printf(" %7.1f $\\pm$ %5.1f ",total[nr],totalE[nr]);
    if(nr == regions-1) printf("\\\\"); else printf("&");
  }
  printf("\n");
}

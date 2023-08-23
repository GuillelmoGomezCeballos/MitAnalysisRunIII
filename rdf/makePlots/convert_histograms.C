#include "TROOT.h"
#include "TFile.h"
#include "TH1F.h"
#include "TColor.h"
#include <map>
#include "common.h"

void convert_histograms(TString inputSampleName = "/home/submit/ceballos/cards/combine_plots/mytest.root", 
  TString subFoldersName = "combinedMy/mll", TString outputSampleName = "output.root"){

  TFile *fileInput = new TFile(inputSampleName.Data(), "read");

  TH1F* histo[nPlotCategories];
  for(int nc=0; nc<nPlotCategories; nc++) histo[nc] = NULL;

  for(int nc=0; nc<nPlotCategories; nc++) {
    if((TH1F*)fileInput->Get(Form("%s/histo_%s",subFoldersName.Data(), plotBaseNames[nc].Data()))){
      histo[nc] = (TH1F*)fileInput->Get(Form("%s/histo_%s",subFoldersName.Data(), plotBaseNames[nc].Data()));
      histo[nc]->SetNameTitle(Form("histo%d",nc),Form("histo%d",nc));
      histo[nc]->SetDirectory(0);
    }
  }
  // Special for Data
  if((TH1F*)fileInput->Get(Form("%s/histo_%s",subFoldersName.Data(), "DATA"))){
    histo[kPlotData] = (TH1F*)fileInput->Get(Form("%s/histo_%s",subFoldersName.Data(), "DATA"));
    histo[kPlotData]->SetNameTitle(Form("histo%d",kPlotData),Form("histo%d",kPlotData));
    histo[kPlotData]->SetDirectory(0);
  }

  TFile fileOutput(outputSampleName.Data(),"RECREATE");
  fileOutput.cd();
  for(int nc=0; nc<nPlotCategories; nc++) {
    if(!histo[nc]) continue;
    histo[nc]->Write();
  }
  fileOutput.Close();
}
//root -q -b -l ~/cms/MitAnalysisRunIII/rdf/makePlots/finalPlot.C+'(0,1,"X","Y","output.root","mva",0,2019,"",1.0,0,"",1,"","","")';

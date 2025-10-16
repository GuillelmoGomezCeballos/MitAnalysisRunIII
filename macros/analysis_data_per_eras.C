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
#include "TColor.h"

void SetMyMultiGraph(TMultiGraph *gr, TAxis *xaxis, TAxis *yaxis, TString title)
{
  xaxis = gr->GetXaxis();
  yaxis = gr->GetYaxis();

  xaxis->SetLabelFont(72);
  yaxis->SetLabelFont(72);
  xaxis->SetLabelOffset(0.01);
  yaxis->SetLabelOffset(0.01);
  xaxis->SetLabelSize(0.04);
  yaxis->SetLabelSize(0.04);
  xaxis->SetNdivisions(507);
  yaxis->SetNdivisions(0);
  xaxis->SetTitle(title.Data());
  xaxis->SetTitleOffset(0.9);
  yaxis->SetTitleOffset(0.9);
  xaxis->SetTitleSize(0.05);
  yaxis->SetTitleSize(0.05);
  yaxis->CenterTitle(kTRUE);     
}

TLegend *SetMyLegend()
{
  TLegend *myLegend = new TLegend(0.625,0.8,0.925,0.9); 

  myLegend->SetBorderSize(0);
  myLegend->SetFillColor(0);
  myLegend->SetTextSize(0.035);

  return myLegend;
}

void analysis_data_per_eras(){
  const int numberEras = 16;
  const int nHist = 23;
  const int refEra = 7;
  double lumi[numberEras] = {8.1,26.7, 18.1,9.7, 7.2,7.9,11.3,27.7,37.7,5.4,11.3, 19.0, 24.2, 14.0, 24.0, 0.0};
  TString nameEra[numberEras] = {"2022A", "2022B", "2023A", "2023B", "2024C", "2024D", "2024E", "2024F", "2024G", "2024H", "2024I",
                              "2025C", "2025D", "2025E", "2025F", "2025G"};
  TString nameAna[nHist] = {"Zmm   ", "Zee   ", "Zmm1j ", "Zee1j ", "Zmm1b ", "Zee1b ", "ssmm  ", "ssee  ", "ssem  ",
                            "wwem  ", "Zem   ", "em12b ", "em1b  ", "em2b  ", "ZZ4l  ", "ZZ4m  ", "ZZ2e2m", "ZZ4e  ",
                            "WZ3l  ", "WZ3m  ", "WZ2m1e", "WZ1m2e", "WZ3e  "};
 TString zSamples[numberEras] = {"anaZ/fillhisto_zAnalysis_20220.root",
                                  "anaZ/fillhisto_zAnalysis_20221.root",

                                  "anaZ/fillhisto_zAnalysis_20230.root",
                                  "anaZ/fillhisto_zAnalysis_20231.root",

                                  "anaZ/fillhisto_zAnalysis_20240.root",
                                  "anaZ/fillhisto_zAnalysis_20241.root",
                                  "anaZ/fillhisto_zAnalysis_20242.root",
                                  "anaZ/fillhisto_zAnalysis_20243.root",
                                  "anaZ/fillhisto_zAnalysis_20244.root",
                                  "anaZ/fillhisto_zAnalysis_20245.root",
                                  "anaZ/fillhisto_zAnalysis_20246.root",

                                  "anaZ/fillhisto_zAnalysis_20250.root",
                                  "anaZ/fillhisto_zAnalysis_20251.root",
                                  "anaZ/fillhisto_zAnalysis_20252.root",
                                  "anaZ/fillhisto_zAnalysis_20253.root"};

  TString wwSamples[numberEras] ={"anaZ/fillhisto_wwAnalysis_20220.root",
                                  "anaZ/fillhisto_wwAnalysis_20221.root",

                                  "anaZ/fillhisto_wwAnalysis_20230.root",
                                  "anaZ/fillhisto_wwAnalysis_20231.root",

                                  "anaZ/fillhisto_wwAnalysis_20240.root",
                                  "anaZ/fillhisto_wwAnalysis_20241.root",
                                  "anaZ/fillhisto_wwAnalysis_20242.root",
                                  "anaZ/fillhisto_wwAnalysis_20243.root",
                                  "anaZ/fillhisto_wwAnalysis_20244.root",
                                  "anaZ/fillhisto_wwAnalysis_20245.root",
                                  "anaZ/fillhisto_wwAnalysis_20246.root",

                                  "anaZ/fillhisto_wwAnalysis_20250.root",
                                  "anaZ/fillhisto_wwAnalysis_20251.root",
                                  "anaZ/fillhisto_wwAnalysis_20252.root",
                                  "anaZ/fillhisto_wwAnalysis_20253.root"};

  TString zzSamples[numberEras] ={"anaZ/fillhisto_zzAnalysis_20220.root",
                                  "anaZ/fillhisto_zzAnalysis_20221.root",

                                  "anaZ/fillhisto_zzAnalysis_20230.root",
                                  "anaZ/fillhisto_zzAnalysis_20231.root",

                                  "anaZ/fillhisto_zzAnalysis_20240.root",
                                  "anaZ/fillhisto_zzAnalysis_20241.root",
                                  "anaZ/fillhisto_zzAnalysis_20242.root",
                                  "anaZ/fillhisto_zzAnalysis_20243.root",
                                  "anaZ/fillhisto_zzAnalysis_20244.root",
                                  "anaZ/fillhisto_zzAnalysis_20245.root",
                                  "anaZ/fillhisto_zzAnalysis_20246.root",

                                  "anaZ/fillhisto_zzAnalysis_20250.root",
                                  "anaZ/fillhisto_zzAnalysis_20251.root",
                                  "anaZ/fillhisto_zzAnalysis_20252.root",
                                  "anaZ/fillhisto_zzAnalysis_20253.root"};

  TString wzSamples[numberEras] ={"anaZ/fillhisto_wzAnalysis_20220.root",
                                  "anaZ/fillhisto_wzAnalysis_20221.root",

                                  "anaZ/fillhisto_wzAnalysis_20230.root",
                                  "anaZ/fillhisto_wzAnalysis_20231.root",

                                  "anaZ/fillhisto_wzAnalysis_20240.root",
                                  "anaZ/fillhisto_wzAnalysis_20241.root",
                                  "anaZ/fillhisto_wzAnalysis_20242.root",
                                  "anaZ/fillhisto_wzAnalysis_20243.root",
                                  "anaZ/fillhisto_wzAnalysis_20244.root",
                                  "anaZ/fillhisto_wzAnalysis_20245.root",
                                  "anaZ/fillhisto_wzAnalysis_20246.root",

                                  "anaZ/fillhisto_wzAnalysis_20250.root",
                                  "anaZ/fillhisto_wzAnalysis_20251.root",
                                  "anaZ/fillhisto_wzAnalysis_20252.root",
                                  "anaZ/fillhisto_wzAnalysis_20253.root"};

  double sel[numberEras][nHist],sele[numberEras][nHist];
  printf("             ");
  for(int nh=0; nh<nHist; nh++) printf(" %s",nameAna[nh].Data());
  printf("\n");

  for(int i=0; i<numberEras-1; i++){
     //if(lumi[i] <= 0) continue;
     TH1D* _hist[nHist];
     TFile *inputzFile = new TFile(Form("%s",zSamples[i].Data()));
     _hist[ 0] = (TH1D*)inputzFile->Get(Form("histo_0_0"))->Clone();
     _hist[ 1] = (TH1D*)inputzFile->Get(Form("histo_2_0"))->Clone();
     _hist[ 2] = (TH1D*)inputzFile->Get(Form("histo_113_0"))->Clone();
     _hist[ 3] = (TH1D*)inputzFile->Get(Form("histo_115_0"))->Clone();
     _hist[ 4] = (TH1D*)inputzFile->Get(Form("histo_119_0"))->Clone();
     _hist[ 5] = (TH1D*)inputzFile->Get(Form("histo_121_0"))->Clone();
     TFile *inputwwFile = new TFile(Form("%s",wwSamples[i].Data()));
     _hist[ 6] = (TH1D*)inputwwFile->Get(Form("histo_71_0"))->Clone();
     _hist[ 7] = (TH1D*)inputwwFile->Get(Form("histo_72_0"))->Clone();
     _hist[ 8] = (TH1D*)inputwwFile->Get(Form("histo_22_0"))->Clone();
     _hist[ 9] = (TH1D*)inputwwFile->Get(Form("histo_23_0"))->Clone();
     _hist[10] = (TH1D*)inputwwFile->Get(Form("histo_24_0"))->Clone();
     _hist[11] = (TH1D*)inputwwFile->Get(Form("histo_25_0"))->Clone();
     _hist[12] = (TH1D*)inputwwFile->Get(Form("histoMVA_600_0"))->Clone();
     _hist[13] = (TH1D*)inputwwFile->Get(Form("histoMVA_800_0"))->Clone();
     TFile *inputzzFile = new TFile(Form("%s",zzSamples[i].Data()));
     _hist[14] = (TH1D*)inputzzFile->Get(Form("histo_8_0"))->Clone();
     _hist[15] = (TH1D*)inputzzFile->Get(Form("histo_8_0"))->Clone(); _hist[15]->SetBinContent(2,0); _hist[15]->SetBinContent(3,0);
     _hist[16] = (TH1D*)inputzzFile->Get(Form("histo_8_0"))->Clone(); _hist[16]->SetBinContent(1,0); _hist[16]->SetBinContent(3,0);
     _hist[17] = (TH1D*)inputzzFile->Get(Form("histo_8_0"))->Clone(); _hist[17]->SetBinContent(1,0); _hist[17]->SetBinContent(2,0);
     TFile *inputwzFile = new TFile(Form("%s",wzSamples[i].Data()));
     _hist[18] = (TH1D*)inputwzFile->Get(Form("histo_11_0"))->Clone();
     _hist[19] = (TH1D*)inputwzFile->Get(Form("histo_11_0"))->Clone(); _hist[19]->SetBinContent(2,0); _hist[19]->SetBinContent(3,0); _hist[19]->SetBinContent(4,0);
     _hist[20] = (TH1D*)inputwzFile->Get(Form("histo_11_0"))->Clone(); _hist[20]->SetBinContent(1,0); _hist[20]->SetBinContent(3,0); _hist[20]->SetBinContent(4,0);
     _hist[21] = (TH1D*)inputwzFile->Get(Form("histo_11_0"))->Clone(); _hist[21]->SetBinContent(1,0); _hist[21]->SetBinContent(2,0); _hist[21]->SetBinContent(4,0);
     _hist[22] = (TH1D*)inputwzFile->Get(Form("histo_11_0"))->Clone(); _hist[22]->SetBinContent(1,0); _hist[22]->SetBinContent(2,0); _hist[22]->SetBinContent(3,0);
     printf("%s (%4.1f):",nameEra[i].Data(),lumi[i]);
     for(int nh=0; nh<nHist; nh++) {
       sele[i][nh] = sqrt(_hist[nh]->GetSumOfWeights());
       _hist[nh]->Scale(1./lumi[i]);
       printf(" %6.0f",_hist[nh]->GetSumOfWeights());
       sel[i][nh]  = _hist[nh]->GetSumOfWeights();
       sele[i][nh] = sele[i][nh]/lumi[i];
     }
     printf("\n");
  }

  const int numberUsedEras = numberEras-1;
  for(int nh=0; nh<nHist; nh++) {
    // Reset first of all
    gROOT->Reset();

    // Axis for cosmetics
    TAxis *xaxis, *yaxis;

    double dilVal[numberUsedEras]; for(int i=0; i<numberUsedEras; i++) dilVal[i] =  sel[i][nh]/sel[refEra][nh];
    double dilErr[numberUsedEras]; for(int i=0; i<numberUsedEras; i++) dilErr[i] = sele[i][nh]/sel[refEra][nh];

    double yVal[numberUsedEras]; for(int i=0; i<numberUsedEras; i++) yVal[i] = i;
    double yErr[numberUsedEras]; for(int i=0; i<numberUsedEras; i++) yErr[i] = 0.0;

    double ranges[2] = {2.0, 0.0};
    for(int i=0; i<numberUsedEras; i++) if(ranges[0] > dilVal[i]) ranges[0] = dilVal[i];
    for(int i=0; i<numberUsedEras; i++) if(ranges[1] < dilVal[i]) ranges[1] = dilVal[i];

    //----------------------------------------------------------------------------
    // Prepare the graph, canvas, legend
    //----------------------------------------------------------------------------
    TGraphErrors* myGraph  = new TGraphErrors(numberUsedEras,dilVal,yVal,dilErr,yErr);
    myGraph->SetMinimum(yVal[0          ]-0.2);
    myGraph->SetMaximum(yVal[numberUsedEras-1]+0.2);
    TMultiGraph*  myMGraph = new TMultiGraph();
    myMGraph->SetMinimum(yVal[0	        ]-0.2);
    myMGraph->SetMaximum(yVal[numberUsedEras-1]+0.2);
    TCanvas* myCanvas = new TCanvas("mu","mu");
    TLegend* myLegend = SetMyLegend();

    //----------------------------------------------------------------------------
    // Draw the graph
    //----------------------------------------------------------------------------
    myGraph->SetMarkerColor(50);
    myGraph->SetMarkerStyle(8);
    myGraph->SetFillColor(0);
    myMGraph->Add(myGraph);

    myMGraph->SetTitle(Form("%s analysis",nameAna[nh].Data()));
    myMGraph->Draw("apz"); 
    SetMyMultiGraph(myMGraph,xaxis,yaxis,Form("Ratio w.r.t. %s",nameEra[refEra].Data())); 

    //----------------------------------------------------------------------------
    // Draw the error of the combined result with a TFrame
    //----------------------------------------------------------------------------
    double lowerEdge = 0.0;
    double upperEdge = 2.0;

    yaxis = myMGraph->GetYaxis();
    double leftY  = yaxis->GetXmin();
    double rightY = yaxis->GetXmax();

    TFrame* oneSigma = new TFrame(lowerEdge,leftY,upperEdge,rightY);
    oneSigma->SetBorderMode(00000);
    oneSigma->SetBorderSize(0);
    oneSigma->SetFillColor(211);
    oneSigma->SetLineColor( 10);
    oneSigma->Draw("same");
    myMGraph->Draw("apzs"); 

    //----------------------------------------------------------------------------
    // Draw the combined dilution with a TF1
    //----------------------------------------------------------------------------
    //TF1* combined = new TF1("combined","[0]+[1]*x",leftY,rightY);
    //combined->SetParameter(0,dilutionValue);
    //combined->SetLineColor(1);
    //combined->SetLineStyle(4);
    //combined->SetLineWidth(3);
    //combined->Draw("same");

    //myLegend->AddEntry(myGraph," Experiments","p");
    //myLegend->AddEntry(combined," Combined","l");
    //myLegend->Draw("same");

    TLine *line0 = new TLine(1, yVal[0]-0.2, 1, yVal[numberUsedEras-1]+0.2);
    line0->SetLineColor(1);
    line0->SetLineStyle(4);
    line0->SetLineWidth(3);
    line0->Draw("same");

    //----------------------------------------------------------------------------
    // Use names instead of numbers in the x axis
    //----------------------------------------------------------------------------
    TText *myText = new TText();
    myText->SetTextAlign(21);
    myText->SetTextFont(72);
    myText->SetTextSize(0.025);

    for (int i=0; i<numberUsedEras; i++) myText->DrawText(ranges[0]*0.97,yVal[i],nameEra[i].Data());

    //----------------------------------------------------------------------------
    // Print to eps
    //----------------------------------------------------------------------------
    TString fia("");
    fia.Append(Form("ratio_%d",nh));
    //myCanvas->Print(Form("%s.pdf",fia.Data()));
    myCanvas->Print(Form("%s.png",fia.Data()));

  }
}

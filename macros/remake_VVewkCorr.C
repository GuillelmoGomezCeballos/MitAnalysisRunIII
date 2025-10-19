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

double GetEdgeValues(TH1D* h, TH1D* hAux, int nsel)
{
    Float_t max = 0;
    Float_t min = 100000000;

    for (Int_t i=1; i<=h->GetNbinsX(); i++) {
        if(hAux->GetBinContent(i) <= 0) continue;
        if (h->GetBinContent(i) > max) max = h->GetBinContent(i);
        if (h->GetBinContent(i) < min) min = h->GetBinContent(i);
    }
    
    if(nsel == 1) return min;

    return max;
}

void atributes(TH1D *histo, TString xtitle = "", TString ytitle = "Fraction", TString units = "", Int_t color = 1, Int_t style = 1){

  histo->SetTitle("");
  //histo->SetMarkerStyle(20);
  //histo->SetMarkerSize(0.8);
  //histo->SetLineWidth(4);
  if(strcmp(units.Data(),"")==0){
    histo->GetXaxis()->SetTitle(xtitle.Data());
  } else {
    units = units.ReplaceAll("BIN","");
    histo->GetXaxis()->SetTitle(Form("%s [%s]",xtitle.Data(),units.Data()));
  }
  histo->GetXaxis()->SetLabelFont  (   42);
  histo->GetXaxis()->SetLabelOffset(0.015);
  histo->GetXaxis()->SetLabelSize  (0.140);
  histo->GetXaxis()->SetNdivisions (  505);
  histo->GetXaxis()->SetTitleFont  (   42);
  histo->GetXaxis()->SetTitleOffset( 0.95);
  histo->GetXaxis()->SetTitleSize  (0.140);
  histo->GetXaxis()->SetTickLength (0.07 );

  histo->GetYaxis()->SetTitle(ytitle.Data());
  histo->GetYaxis()->SetLabelFont  (   42);
  histo->GetYaxis()->SetLabelOffset(0.015);
  histo->GetYaxis()->SetLabelSize  (0.120);
  histo->GetYaxis()->SetNdivisions (  505);
  histo->GetYaxis()->SetTitleFont  (   42);
  histo->GetYaxis()->SetTitleOffset(  0.4);
  histo->GetYaxis()->SetTitleSize  (0.120);
  histo->GetYaxis()->SetTickLength (0.03 );

  histo->SetLineWidth(3);
  histo->SetLineColor(color);
  histo->SetMarkerStyle(kFullCircle);
  histo->SetLineStyle(style);
}

const int nPlotCategories=27;
enum plotCategory {
  kPlotData	     , // 0
  kPlotqqWW	     , // 1
  kPlotggWW	     , // 2
  kPlotTT	     , // 3
  kPlotTW	     , // 4
  kPlotDY	     , // 5
  kPlotEWKSSWW       , // 6
  kPlotQCDSSWW       , // 7
  kPlotEWKWZ	     , // 8
  kPlotWZ	     , // 9
  kPlotZZ	     , //10
  kPlotNonPrompt     , //11
  kPlotVVV	     , //12
  kPlotTVX	     , //13
  kPlotVG	     , //14
  kPlotHiggs	     , //15
  kPlotWS	     , //16
  kPlotOther	     , //17
  kPlotEM	     , //18
  kPlotBSM	     , //19
  kPlotSignal0       , //20
  kPlotSignal1       , //21
  kPlotSignal2       , //22
  kPlotSignal3       , //23
  kPlotSignal4       , //24
  kPlotSignal5       , //25
  NonPromptWZ	       //26
};

std::map<int, TString> plotBaseNames={
  { kPlotData	       , "Data" },
  { kPlotqqWW	       , "qqWW" },
  { kPlotggWW	       , "ggWW" },
  { kPlotTT	       , "TT" },
  { kPlotTW	       , "TW" },
  { kPlotDY	       , "DY" },
  { kPlotEWKSSWW       , "EWKSSWW" },
  { kPlotQCDSSWW       , "QCDSSWW" },
  { kPlotEWKWZ         , "EWKWZ" },
  { kPlotWZ	       , "WZ" },
  { kPlotZZ	       , "ZZ" },
  { kPlotNonPrompt     , "NonPrompt" },
  { kPlotVVV	       , "VVV" },
  { kPlotTVX	       , "TVX" },
  { kPlotVG	       , "VG" },
  { kPlotHiggs         , "Higgs" },
  { kPlotWS	       , "WS" },
  { kPlotOther         , "Other" },
  { kPlotEM	       , "EM" },
  { kPlotBSM	       , "BSM" },
  { kPlotSignal0       , "Signal0" },
  { kPlotSignal1       , "Signal1" },
  { kPlotSignal2       , "Signal2" },
  { kPlotSignal3       , "Signal3" },
  { kPlotSignal4       , "Signal4" },
  { kPlotSignal5       , "Signal5" },
  { NonPromptWZ        , "NonPromptWZ" }
}; 

const int nSystNames=72;
std::map<int, TString> systNames={
  { 0 ,"CMS_SMPXXXXXX_fake_ssww_e0"},
  { 1 ,"CMS_SMPXXXXXX_fake_ssww_e1"},
  { 2 ,"CMS_SMPXXXXXX_fake_ssww_e2"},
  { 3 ,"CMS_SMPXXXXXX_fake_ssww_m0"},
  { 4 ,"CMS_SMPXXXXXX_fake_ssww_m1"},
  { 5 ,"CMS_SMPXXXXXX_fake_ssww_m2"},
  { 6 ,"CMS_SMPXXXXXX_fake_wz_e0"},
  { 7 ,"CMS_SMPXXXXXX_fake_wz_e1"},
  { 8 ,"CMS_SMPXXXXXX_fake_wz_e2"},
  { 9 ,"CMS_SMPXXXXXX_fake_wz_m0"},
  { 10,"CMS_SMPXXXXXX_fake_wz_m1"},
  { 11,"CMS_SMPXXXXXX_fake_wz_m2"},
  { 12,"CMS_SMPXXXXXX_wrongsign_method"},
  { 13,"CMS_SMPXXXXXX_wrongsign_stat"},
  { 14,"CMS_SMPXXXXX_WWtrigger"},
  { 15,"CMS_bc_btag_bfragmentation"},
  { 16,"CMS_bc_btag_colorreconnection"},
  { 17,"CMS_bc_btag_hdamp"},
  { 18,"CMS_bc_btag_jer"},
  { 19,"CMS_bc_btag_jes"},
  { 20,"CMS_bc_btag_pdf"},
  { 21,"CMS_bc_btag_pileup"},
  { 22,"CMS_bc_btag_statistic"},
  { 23,"CMS_bc_btag_topmass"},
  { 24,"CMS_bc_btag_type3"},
  { 25,"CMS_eff_e_id"},
  { 26,"CMS_eff_e_reco"},
  { 27,"CMS_eff_m_id"},
  { 28,"CMS_eff_m_iso"},
  { 29,"CMS_eff_m_reco"},
  { 30,"CMS_lf_btag"},
  { 31,"CMS_met_jer"},
  { 32,"CMS_met_jes"},
  { 33,"CMS_met_unclustered"},
  { 34,"CMS_res_j"},
  { 35,"CMS_scale_e"},
  { 36,"CMS_scale_j_AbsoluteMPFBias"},
  { 37,"CMS_scale_j_AbsoluteScale"},
  { 38,"CMS_scale_j_AbsoluteStat"},
  { 39,"CMS_scale_j_FlavorQCD"},
  { 40,"CMS_scale_j_Fragmentation"},
  { 41,"CMS_scale_j_PileUpDataMC"},
  { 42,"CMS_scale_j_PileUpPtBB"},
  { 43,"CMS_scale_j_PileUpPtEC1"},
  { 44,"CMS_scale_j_PileUpPtEC2"},
  { 45,"CMS_scale_j_PileUpPtHF"},
  { 46,"CMS_scale_j_PileUpPtRef"},
  { 47,"CMS_scale_j_RelativeBal"},
  { 48,"CMS_scale_j_RelativeFSR"},
  { 49,"CMS_scale_j_RelativeJEREC1"},
  { 50,"CMS_scale_j_RelativeJEREC2"},
  { 51,"CMS_scale_j_RelativeJERHF"},
  { 52,"CMS_scale_j_RelativePtBB"},
  { 53,"CMS_scale_j_RelativePtEC1"},
  { 54,"CMS_scale_j_RelativePtEC2"},
  { 55,"CMS_scale_j_RelativePtHF"},
  { 56,"CMS_scale_j_RelativeSample"},
  { 57,"CMS_scale_j_RelativeStatEC"},
  { 58,"CMS_scale_j_RelativeStatFSR"},
  { 59,"CMS_scale_j_RelativeStatHF"},
  { 60,"CMS_scale_j_SinglePionECAL"},
  { 61,"CMS_scale_j_SinglePionHCAL"},
  { 62,"CMS_scale_j_TimePtEta"},
  { 63,"CMS_scale_m"},
  { 64,"PS"},
  { 65,"QCD_scale"},
  { 66,"WWewkCorr"},
  { 67,"WZewkCorr"},
  { 68,"luminosity"},
  { 69,"pdf100"},
  { 70,"pdfqq"},
  { 71,"pileup"}
}; 

void remake_VVewkCorr(
TString inputName="data/VV_NLO_LO_CMS_mjj_run2.root"
) {

  TFile *infile = TFile::Open(Form("%s",inputName.Data()));

  TH1D* hWZ_KF_CMS     = (TH1D*)infile->Get(Form("hWZ_KF_CMS"));
  TH1D* hWZ_KF_CMSUp   = (TH1D*)infile->Get(Form("hWZ_KF_CMSUp"));
  TH1D* hWZ_KF_CMSDown = (TH1D*)infile->Get(Form("hWZ_KF_CMSDown"));
  TH1D* hWW_KF_CMS     = (TH1D*)infile->Get(Form("hWW_KF_CMS"));
  TH1D* hWW_KF_CMSUp   = (TH1D*)infile->Get(Form("hWW_KF_CMSUp"));
  TH1D* hWW_KF_CMSDown = (TH1D*)infile->Get(Form("hWW_KF_CMSDown"));

  hWZ_KF_CMS    ->SetDirectory(0);
  hWZ_KF_CMSUp  ->SetDirectory(0);
  hWZ_KF_CMSDown->SetDirectory(0);
  hWW_KF_CMS    ->SetDirectory(0);
  hWW_KF_CMSUp  ->SetDirectory(0);
  hWW_KF_CMSDown->SetDirectory(0);

  for(int j=1; j<=hWZ_KF_CMS->GetNbinsX(); j++) {
    if(hWZ_KF_CMS->GetBinCenter(j) > 3000) {
      hWZ_KF_CMS    ->SetBinContent(j,hWZ_KF_CMS    ->GetBinContent(j-1));
      hWZ_KF_CMSUp  ->SetBinContent(j,hWZ_KF_CMSUp  ->GetBinContent(j-1));
      hWZ_KF_CMSDown->SetBinContent(j,hWZ_KF_CMSDown->GetBinContent(j-1));
    }
  }
  hWZ_KF_CMSUp  ->Scale(hWZ_KF_CMS->GetSumOfWeights()/hWZ_KF_CMSUp  ->GetSumOfWeights());
  hWZ_KF_CMSDown->Scale(hWZ_KF_CMS->GetSumOfWeights()/hWZ_KF_CMSDown->GetSumOfWeights());


  for(int j=1; j<=hWW_KF_CMS->GetNbinsX(); j++) {
    float unc = 1.000 + 0.012 + (hWW_KF_CMS->GetBinCenter(j)-500)*0.00001;
    hWW_KF_CMSUp  ->SetBinContent(j,hWW_KF_CMS->GetBinContent(j)*unc);
    hWW_KF_CMSDown->SetBinContent(j,hWW_KF_CMS->GetBinContent(j)/unc);
  }
  hWW_KF_CMSUp  ->Scale(hWW_KF_CMS->GetSumOfWeights()/hWW_KF_CMSUp  ->GetSumOfWeights());
  hWW_KF_CMSDown->Scale(hWW_KF_CMS->GetSumOfWeights()/hWW_KF_CMSDown->GetSumOfWeights());

  TFile oufile(Form("%s_new.root",inputName.ReplaceAll(".root","").Data()),"RECREATE");
  oufile.cd();
  
  hWZ_KF_CMS    ->Write();
  hWZ_KF_CMSUp  ->Write();
  hWZ_KF_CMSDown->Write();

  hWW_KF_CMS    ->Write();
  hWW_KF_CMSUp  ->Write();
  hWW_KF_CMSDown->Write();

  oufile.Close();
}

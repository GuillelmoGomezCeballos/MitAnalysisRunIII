#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include "TROOT.h"
#include "TFile.h"
#include "TH1.h"
#include "TF2.h"
#include "TString.h"
#include "TRandom.h"
#include "TRandom3.h"
#include "TSpline.h"
#include "TCanvas.h"
#include "TGraphAsymmErrors.h"
#include "TLorentzVector.h"
#include "TEfficiency.h"
#include "TVector2.h"
#include "Math/GenVector/LorentzVector.h"
#include "Math/GenVector/PtEtaPhiM4D.h"

#include "mysf.h"

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <array>
#include <string>
#include <vector>
#include <unordered_map>
#include <utility>
#include <algorithm>
#include <limits>
#include <map>

#include <ROOT/RVec.hxx>
#include <ROOT/RDataFrame.hxx>

using Vec_b = ROOT::VecOps::RVec<bool>;
using Vec_d = ROOT::VecOps::RVec<double>;
using Vec_f = ROOT::VecOps::RVec<float>;
using Vec_i = ROOT::VecOps::RVec<int>;
using Vec_ui = ROOT::VecOps::RVec<unsigned int>;

typedef ROOT::Math::LorentzVector<ROOT::Math::PtEtaPhiM4D<double> > PtEtaPhiMVector;
std::unordered_map< UInt_t, std::vector< std::pair<UInt_t,UInt_t> > > jsonMap;

TH2D histoFakeEtaPt_mu;
TH2D histoFakeEtaPt_el;
TH2D histoLepSFEtaPt_mu;
TH2D histoLepSFEtaPt_el;
TH2D histoTriggerSFEtaPt_0_0;
TH2D histoTriggerSFEtaPt_0_1;
TH2D histoTriggerSFEtaPt_0_2;
TH2D histoTriggerSFEtaPt_0_3;
TH2D histoTriggerSFEtaPt_1_0;
TH2D histoTriggerSFEtaPt_1_1;
TH2D histoTriggerSFEtaPt_1_2;
TH2D histoTriggerSFEtaPt_1_3;
TH2D histoTriggerSFEtaPt_2_0;
TH2D histoTriggerSFEtaPt_2_1;
TH2D histoTriggerSFEtaPt_2_2;
TH2D histoTriggerSFEtaPt_2_3;
TH2D histoTriggerSFEtaPt_3_0;
TH2D histoTriggerSFEtaPt_3_1;
TH2D histoTriggerSFEtaPt_3_2;
TH2D histoTriggerSFEtaPt_3_3;
TH2D histoBTVEffEtaPtLF;
TH2D histoBTVEffEtaPtCJ;
TH2D histoBTVEffEtaPtBJ;
TH2F histoElRecoSF;
TH2F histoElSelSF;
TH2F histoMuIDSF;
TH2F histoMuISOSF;
TH1D puWeights;
auto corrSFs = MyCorrections(2018);

void initHisto2F(TH2F h, int nsel){
  if     (nsel == 0) histoElRecoSF = h;
  else if(nsel == 1) histoElSelSF = h;
  else if(nsel == 2) histoMuIDSF = h;
  else if(nsel == 3) histoMuISOSF = h;
}

void initHisto2D(TH2D h, int nsel){
  if     (nsel ==  0) histoFakeEtaPt_mu = h;
  else if(nsel ==  1) histoFakeEtaPt_el = h;
  else if(nsel ==  2) histoLepSFEtaPt_mu = h;
  else if(nsel ==  3) histoLepSFEtaPt_el = h;
  else if(nsel ==  4) histoTriggerSFEtaPt_0_0 = h;
  else if(nsel ==  5) histoTriggerSFEtaPt_0_1 = h;
  else if(nsel ==  6) histoTriggerSFEtaPt_0_2 = h;
  else if(nsel ==  7) histoTriggerSFEtaPt_0_3 = h;
  else if(nsel ==  8) histoTriggerSFEtaPt_1_0 = h;
  else if(nsel ==  9) histoTriggerSFEtaPt_1_1 = h;
  else if(nsel == 10) histoTriggerSFEtaPt_1_2 = h;
  else if(nsel == 11) histoTriggerSFEtaPt_1_3 = h;
  else if(nsel == 12) histoTriggerSFEtaPt_2_0 = h;
  else if(nsel == 13) histoTriggerSFEtaPt_2_1 = h;
  else if(nsel == 14) histoTriggerSFEtaPt_2_2 = h;
  else if(nsel == 15) histoTriggerSFEtaPt_2_3 = h;
  else if(nsel == 16) histoTriggerSFEtaPt_3_0 = h;
  else if(nsel == 17) histoTriggerSFEtaPt_3_1 = h;
  else if(nsel == 18) histoTriggerSFEtaPt_3_2 = h;
  else if(nsel == 19) histoTriggerSFEtaPt_3_3 = h;
  else if(nsel == 20) histoBTVEffEtaPtLF = h;
  else if(nsel == 21) histoBTVEffEtaPtCJ = h;
  else if(nsel == 22) histoBTVEffEtaPtBJ = h;
}

void initHisto1D(TH1D h, int nsel){
  if(nsel == 0) puWeights = h;
}

float getValFromTH1(const TH1& h, const float& x, const float& sumError=0.0) {
  int xbin = std::max(1, std::min(h.GetNbinsX(), h.GetXaxis()->FindFixBin(x)));
  if (sumError)
    return h.GetBinContent(xbin) + sumError * h.GetBinError(xbin);
  else
    return h.GetBinContent(xbin);
}

float getValFromTH2(const TH2& h, const float& x, const float& y, const float& sumError=0.0) {
  //std::cout << "x,y --> " << x << "," << y << std::endl;
  int xbin = std::max(1, std::min(h.GetNbinsX(), h.GetXaxis()->FindFixBin(x)));
  int ybin = std::max(1, std::min(h.GetNbinsY(), h.GetYaxis()->FindFixBin(y)));
  //std::cout << "xbin,ybin --> " << xbin << "," << ybin << std::endl;
  if (sumError)
    return h.GetBinContent(xbin, ybin) + sumError * h.GetBinError(xbin, ybin);
  else
    return h.GetBinContent(xbin, ybin);
}

void initJSONSFs(int year){
  corrSFs = MyCorrections(year);
}

Vec_f compute_JES(Vec_f jet_pt, Vec_f jet_eta) {

  Vec_f jet_pt_new(jet_pt.size(), 0);
  for(unsigned int i=0;i<jet_pt.size();i++) {
    jet_pt_new[i] = jet_pt[i]*0.03;
  }
  return jet_pt_new;
}

// PUJetID SFs
float compute_JSONS_PUJetID_SF(Vec_f jet_pt, Vec_f jet_eta, unsigned int sel)
{
  //printf("pujetidsf: %lu %lu %d\n",jet_pt.size(),jet_eta.size(),sel);
  double sfTot = 1.0;
  char *valType = (char*)"T"; double bcut = 0.711;
  if     (sel == 0) {valType = (char*)"T";}
  else if(sel == 1) {valType = (char*)"M";}
  else if(sel == 2) {valType = (char*)"L";}
  for(unsigned int i=0;i<jet_pt.size();i++) {
    if(jet_pt[i] <= 30 || fabs(jet_eta[i]) >= 5.0) continue;
    double sf = corrSFs.eval_puJetIDSF((char*)"nom",valType,jet_eta[i],min(jet_pt[i],999.999f));
    sfTot *= sf;
    //printf("pujetidsf(%d) %.3f %.3f %.3f %.3f\n",i,jet_pt[i],jet_eta[i],sfTot,sf);
  }
  return sfTot;
}

// BTag SFs
float compute_JSONS_BTV_SF(Vec_f jet_pt, Vec_f jet_eta, Vec_f jet_btag, Vec_i jet_flavor, unsigned int sel)
{
  //printf("btagsf: %lu %lu %lu %lu %d\n",jet_pt.size(),jet_eta.size(),jet_btag.size(),jet_flavor.size(),sel);
  double sfTot[2] = {1.0, 1.0};
  char *valType = (char*)"T"; double bcut = 0.711;
  if     (sel == 0) {valType = (char*)"T"; bcut = 0.7100;}
  else if(sel == 1) {valType = (char*)"M"; bcut = 0.2783;}
  else if(sel == 2) {valType = (char*)"L"; bcut = 0.0490;}
  for(unsigned int i=0;i<jet_pt.size();i++) {
    if(jet_flavor[i] != 0 && jet_flavor[i] != 4 && jet_flavor[i] != 5) continue;
    if(jet_pt[i] <= 20 || fabs(jet_eta[i]) >= 2.5) continue;
    double sf = corrSFs.eval_btvSF((char*)"central",valType,abs(jet_eta[i]),min(jet_pt[i],999.999f),jet_flavor[i]);
    double eff = 1;
    if     (jet_flavor[i] == 0) {const TH2D& hcorr0 = histoBTVEffEtaPtLF; eff = getValFromTH2(hcorr0, fabs(jet_eta[i]),min(jet_pt[i],999.999f));}
    else if(jet_flavor[i] == 4) {const TH2D& hcorr1 = histoBTVEffEtaPtCJ; eff = getValFromTH2(hcorr1, fabs(jet_eta[i]),min(jet_pt[i],999.999f));}
    else if(jet_flavor[i] == 5) {const TH2D& hcorr2 = histoBTVEffEtaPtBJ; eff = getValFromTH2(hcorr2, fabs(jet_eta[i]),min(jet_pt[i],999.999f));}
    if(jet_btag[i] > bcut) {
      sfTot[0] *= sf * eff; sfTot[1] *= eff;
    }
    else {
      sfTot[0] *= (1.0 - sf * eff); sfTot[1] *= (1.0 - eff);
    }
    //printf("btagsf(%d) %.3f %.3f %d %d %.3f %.3f %.3f %.3f\n",i,jet_pt[i],jet_eta[i],jet_flavor[i],jet_btag[i] > bcut,sfTot[0],sfTot[1],sf,eff);
  }
  
  if(sfTot[1] > 0) return sfTot[0]/sfTot[1];
  return 1.0;
}

float compute_JSON_SFs(const Vec_f& mu_pt, const Vec_f& mu_eta,
                       const Vec_f& el_pt, const Vec_f& el_eta){

  //printf("lepeff: %lu %lu\n",mu_pt.size(),el_pt.size());
  double sfTot = 1.0;

  char *year = (char*)"2018_UL";
  char *valType = (char*)"sf";
  char *workingPoint = (char*)"Medium";
  for(unsigned int i=0;i<mu_pt.size();i++) {
    double sf = corrSFs.eval_muonIDSF (year,valType,workingPoint,mu_eta[i],max(mu_pt[i],15.0f))*
    		corrSFs.eval_muonISOSF(year,valType,workingPoint,mu_eta[i],max(mu_pt[i],15.0f));
    sfTot = sfTot*sf;
    //printf("lepmu(%d) %.3f %.3f %.3f %.3f\n",i,mu_pt[i],mu_eta[i],sf,sfTot);
  }

  year = (char*)"2018";
  valType = (char*)"sf";
  workingPoint = (char*)"Medium";
  for(unsigned int i=0;i<el_pt.size();i++) {
    double sf = corrSFs.eval_electronSF(year,valType,workingPoint,el_eta[i],el_pt[i]);
    sfTot = sfTot*sf;
    //printf("lepel(%d) %.3f %.3f %.3f %.3f\n",i,el_pt[i],el_eta[i],sf,sfTot);
  }
      
  return sfTot;
}

float compute_bdt_test(const Vec_f& bdt){
  if(bdt.size() != 1) {
    printf("bdt size != 1 %lu\n",bdt.size());
    return -10.0;
  }
  return bdt[0];
}

Vec_b cleaningBitmap(const Vec_i& Photon_vidNestedWPBitmap, int var, int cutBased) {

  Vec_b mask(Photon_vidNestedWPBitmap.size(), true);
  for(unsigned int i=0;i<Photon_vidNestedWPBitmap.size();i++) {
    if((Photon_vidNestedWPBitmap[i]>>var&3) >= cutBased) continue;
    mask[i] = false;
  }
  return mask;
}

float compute_photon_test(const Vec_f& Photon_pt, const Vec_f& Photon_eta, const Vec_f& Photon_phi, 
const Vec_i& Photon_cutBased, const Vec_f& Photon_pfRelIso03_all, const Vec_f& Photon_pfRelIso03_chg, 
const Vec_f& Photon_hoe, const Vec_f& Photon_sieie, const Vec_i& Photon_vidNestedWPBitmap)
{
  for(unsigned int i=0;i<Photon_pt.size();i++) {
  int pass0 = (Photon_vidNestedWPBitmap[i]>>4&3);  // H/E
  int pass1 = (Photon_vidNestedWPBitmap[i]>>6&3);  // sigmaiEtaiEta
  int pass2 = (Photon_vidNestedWPBitmap[i]>>8&3);  // ChIso
  int pass3 = (Photon_vidNestedWPBitmap[i]>>10&3); // NeuIso
  int pass4 = (Photon_vidNestedWPBitmap[i]>>12&3); // PhoIso
  printf("test %5.1f %d %d %.5f %.4f %.4f %.4f %.4f | %d %d %d %d %d\n",Photon_pt[i],(int)(Photon_eta[i]<1.5),Photon_cutBased[i],Photon_hoe[i],Photon_sieie[i],
  Photon_pfRelIso03_all[i]*Photon_pt[i],Photon_pfRelIso03_chg[i]*Photon_pt[i],(Photon_pfRelIso03_all[i]-Photon_pfRelIso03_chg[i])*Photon_pt[i],
  pass0,pass1,pass2,pass3,pass4);

  //printf("test %5.1f %d %d %.5f %.4f %.4f %.4f %.4f | %d %d | %d %d | %d %d | %d %d | %d %d | %d %d | %d %d\n",Photon_pt[i],(int)(Photon_eta[i]<1.5),Photon_cutBased[i],Photon_hoe[i],Photon_sieie[i],
  //Photon_pfRelIso03_all[i]*Photon_pt[i],Photon_pfRelIso03_chg[i]*Photon_pt[i],(Photon_pfRelIso03_all[i]-Photon_pfRelIso03_chg[i])*Photon_pt[i],
  //(Photon_vidNestedWPBitmap[i]&(1<<0))==(1<<0),(Photon_vidNestedWPBitmap[i]&(1<<1))==(1<<1),(Photon_vidNestedWPBitmap[i]&(1<<2))==(1<<2),(Photon_vidNestedWPBitmap[i]&(1<<3))==(1<<3),
  //(Photon_vidNestedWPBitmap[i]&(1<<4))==(1<<4),(Photon_vidNestedWPBitmap[i]&(1<<5))==(1<<5),(Photon_vidNestedWPBitmap[i]&(1<<6))==(1<<6),(Photon_vidNestedWPBitmap[i]&(1<<7))==(1<<7),
  //(Photon_vidNestedWPBitmap[i]&(1<<8))==(1<<8),(Photon_vidNestedWPBitmap[i]&(1<<9))==(1<<9),(Photon_vidNestedWPBitmap[i]&(1<<10))==(1<<10),(Photon_vidNestedWPBitmap[i]&(1<<11))==(1<<11),
  //(Photon_vidNestedWPBitmap[i]&(1<<12))==(1<<12),(Photon_vidNestedWPBitmap[i]&(1<<13))==(1<<13));
  }
  return 1.0;
}

float compute_test(const Vec_f& mu_pt, const Vec_f& mu_eta, TH2D histo_mu){
  printf("test %f\n",histo_mu.GetBinContent(2,2));
  return 1.0;
}

struct WeightsComputer {
   TH2D *fHist2D;
   WeightsComputer(TH2D *h) : fHist2D(h) {}

   float operator()(const Vec_f &mu_pt, const Vec_f &mu_eta) {
      return compute_test(mu_pt, mu_eta, *fHist2D);
  }
};

float compute_fakeRate(const bool isData,
                       const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_i& tight_mu,
                       const Vec_f& el_pt, const Vec_f& el_eta, const Vec_i& tight_el){

  if(mu_pt.size() != tight_mu.size() || el_pt.size() != tight_el.size()) {
    printf("PROBLEM in compute_fakeRate!\n");
    return 0;
  }

  double sfTot = 1.0;
  for(unsigned int i=0;i<mu_pt.size();i++) {
    if(tight_mu[i] == 1) continue;
    const TH2D& hcorr = histoFakeEtaPt_mu;
    double sf = getValFromTH2(hcorr, fabs(mu_eta[i]),mu_pt[i]);
    sfTot = -sfTot*sf/(1-sf)*0.5;
    //printf("fakemu(%d) %.3f %.3f %.3f %.3f %.3f\n",i,mu_pt[i],mu_eta[i],sf,sf/(1-sf),sfTot);
  }

  for(unsigned int i=0;i<el_pt.size();i++) {
    if(tight_el[i] == 1) continue;
    const TH2D& hcorr = histoFakeEtaPt_el;
    double sf = getValFromTH2(hcorr, fabs(el_eta[i]), el_pt[i]);
    sfTot = -sfTot*sf/(1-sf);
    //printf("fakeel(%d) %.3f %.3f %.3f %.3f %.3f\n",i,el_pt[i],el_eta[i],sf,sf/(1-sf),sfTot);
  }
      
  if(sfTot != 1 && isData) sfTot = -sfTot;
  return sfTot;
}

float compute_LepSF(const Vec_f& mu_pt, const Vec_f& mu_eta,
                    const Vec_f& el_pt, const Vec_f& el_eta){

  //printf("lepeff: %lu %lu\n",mu_pt.size(),el_pt.size());
  double sfTot = 1.0;
  for(unsigned int i=0;i<mu_pt.size();i++) {
    const TH2D& hcorr = histoLepSFEtaPt_mu;
    double sf = getValFromTH2(hcorr, fabs(mu_eta[i]),mu_pt[i]);
    sfTot = sfTot*sf;
    //printf("lepmu(%d) %.3f %.3f %.3f %.3f\n",i,mu_pt[i],mu_eta[i],sf,sfTot);
  }

  for(unsigned int i=0;i<el_pt.size();i++) {
    const TH2D& hcorr = histoLepSFEtaPt_el;
    double sf = getValFromTH2(hcorr, fabs(el_eta[i]), el_pt[i]);
    sfTot = sfTot*sf;
    //printf("lepel(%d) %.3f %.3f %.3f %.3f\n",i,el_pt[i],el_eta[i],sf,sfTot);
  }
      
  return sfTot;
}

float compute_PURecoSF(const Vec_f& mu_pt, const Vec_f& mu_eta,
                       const Vec_f& el_pt, const Vec_f& el_eta,
		       const float nPU){

  //printf("lepeff: %lu %lu\n",mu_pt.size(),el_pt.size());
  double sfTot = 1.0;
  for(unsigned int i=0;i<mu_pt.size();i++) {
    const TH2F& hcorr0 = histoMuIDSF;
    double sf0 = getValFromTH2(hcorr0, fabs(mu_eta[i]),mu_pt[i]);
    const TH2F& hcorr1 = histoMuISOSF;
    double sf1 = getValFromTH2(hcorr1, fabs(mu_eta[i]),mu_pt[i]);
    sfTot = sfTot*sf0*sf1;
    //printf("leprecomu(%d) %.3f %.3f %.3f %.3f %.3f\n",i,mu_pt[i],mu_eta[i],sf0,sf1,sfTot);
  }

  for(unsigned int i=0;i<el_pt.size();i++) {
    const TH2F& hcorr0 = histoElRecoSF;
    double sf0 = getValFromTH2(hcorr0, el_eta[i], el_pt[i]);
    const TH2F& hcorr1 = histoElSelSF;
    double sf1 = getValFromTH2(hcorr1, el_eta[i], el_pt[i]);
    sfTot = sfTot*sf0*sf1;
    //printf("leprecoel(%d) %.3f %.3f %.3f %.3f %.3f\n",i,el_pt[i],el_eta[i],sf0,sf1,sfTot);
  }

  const TH1D& hcorr = puWeights;
  double sf = getValFromTH1(hcorr, nPU);
  sfTot = sfTot*sf;
  //printf("pu %.3f %.3f %.3f\n",nPU,sf,sfTot);

  return sfTot;
}

float compute_TriggerSF(float ptl1, float ptl2, float etal1, float etal2, int ltype){

  TH2D hcorr;
  if	 (etal1 <= 1.5 && etal2 <= 1.5 && ltype == 0) hcorr = histoTriggerSFEtaPt_0_0;
  else if(etal1 >  1.5 && etal2 <= 1.5 && ltype == 0) hcorr = histoTriggerSFEtaPt_0_1;
  else if(etal1 <= 1.5 && etal2 >  1.5 && ltype == 0) hcorr = histoTriggerSFEtaPt_0_2;
  else if(etal1 >  1.5 && etal2 >  1.5 && ltype == 0) hcorr = histoTriggerSFEtaPt_0_3;
  else if(etal1 <= 1.5 && etal2 <= 1.5 && ltype == 1) hcorr = histoTriggerSFEtaPt_1_0;
  else if(etal1 >  1.5 && etal2 <= 1.5 && ltype == 1) hcorr = histoTriggerSFEtaPt_1_1;
  else if(etal1 <= 1.5 && etal2 >  1.5 && ltype == 1) hcorr = histoTriggerSFEtaPt_1_2;
  else if(etal1 >  1.5 && etal2 >  1.5 && ltype == 1) hcorr = histoTriggerSFEtaPt_1_3;
  else if(etal1 <= 1.5 && etal2 <= 1.5 && ltype == 2) hcorr = histoTriggerSFEtaPt_2_0;
  else if(etal1 >  1.5 && etal2 <= 1.5 && ltype == 2) hcorr = histoTriggerSFEtaPt_2_1;
  else if(etal1 <= 1.5 && etal2 >  1.5 && ltype == 2) hcorr = histoTriggerSFEtaPt_2_2;
  else if(etal1 >  1.5 && etal2 >  1.5 && ltype == 2) hcorr = histoTriggerSFEtaPt_2_3;
  else if(etal1 <= 1.5 && etal2 <= 1.5 && ltype == 3) hcorr = histoTriggerSFEtaPt_3_0;
  else if(etal1 >  1.5 && etal2 <= 1.5 && ltype == 3) hcorr = histoTriggerSFEtaPt_3_1;
  else if(etal1 <= 1.5 && etal2 >  1.5 && ltype == 3) hcorr = histoTriggerSFEtaPt_3_2;
  else if(etal1 >  1.5 && etal2 >  1.5 && ltype == 3) hcorr = histoTriggerSFEtaPt_3_3;
  else printf("Problem trigger type (%d) %f %f\n",ltype,etal1,etal2);
  return getValFromTH2(hcorr, ptl1, ptl2);
}

bool isGoodRunLS(const bool isData, const UInt_t run, const UInt_t lumi) {

  if(not isData) return true;

  if(jsonMap.find(run) == jsonMap.end()) return false; // run not found

  auto& validlumis = jsonMap.at(run);
  auto match = std::lower_bound(std::begin(validlumis), std::end(validlumis), lumi,
				[](std::pair<unsigned int, unsigned int>& range, unsigned int val) { return range.second < val; });
  return match->first <= lumi && match->second >= lumi;
}

float deltaPhi(float phi1, float phi2) {
  float result = phi1 - phi2;
  while (result > float(M_PI)) result -= float(2*M_PI);
  while (result <= -float(M_PI)) result += float(2*M_PI);
  return fabs(result);
}

float deltaR2(float eta1, float phi1, float eta2, float phi2) {
  float deta = eta1-eta2;
  float dphi = deltaPhi(phi1,phi2);
  return deta*deta + dphi*dphi;
}

float deltaR(float eta1, float phi1, float eta2, float phi2) {
  return std::sqrt(deltaR2(eta1,phi1,eta2,phi2));
}

Vec_f compute_deltaR_var(Vec_f eta, Vec_f phi, float eta1, float phi1){
  Vec_f dR(eta.size(), 0.0);
  for (unsigned int idx = 0; idx < eta.size(); idx++) {
    dR[idx] = std::sqrt(deltaR2(eta[idx],phi[idx],eta1,phi1));
  }
  return dR;
}

Vec_b cleaningMask(Vec_i indices, int size) {

  Vec_b mask(size, true);
  for (int idx : indices) {
    if(idx < 0) continue;
    mask[idx] = false;
  }
  return mask;
}

bool hasTriggerMatch(const float& eta, const float& phi, const Vec_f& TrigObj_eta, const Vec_f& TrigObj_phi) {

  for (unsigned int jtrig = 0; jtrig < TrigObj_eta.size(); ++jtrig) {
    if (deltaR(eta, phi, TrigObj_eta[jtrig], TrigObj_phi[jtrig]) < 0.3) return true;
  }
  return false;
}

float get_variable_index(Vec_f var, Vec_f pt, const unsigned int index){

  if(var.size() < index) return 0.0;

  for(unsigned int i=0;i<pt.size();i++) {
    for(unsigned int j=i+1;j<pt.size();j++) {
      if(pt[i]<pt[j]) {
        float temp0 = pt[i]; float temp1 = var[i];
        pt[i] = pt[j];	     var[i] = var[j];
        pt[j] = temp0;	     var[j] = temp1;
      }
    }
  }
  
  return var[index];

}

// Muon Id variables
int compute_muid_var(const Vec_b& mu_mediumId, const Vec_b& mu_tightId, const Vec_i& mu_pfIsoId,
		     const Vec_i& mu_mvaId,  const Vec_i& mu_miniIsoId, const Vec_f& mu_mvaTTH, 
		     unsigned int nsel)
{
  if(mu_mediumId.size() < nsel+1) return -1;

  int var = 0;
  if(mu_mediumId[nsel] == true && mu_pfIsoId[nsel] >= 4) var = var + 1;
  if(mu_tightId[nsel] == true && mu_pfIsoId[nsel] >= 4) var = var + 2;
  if(mu_mvaId[nsel] >= 2 && mu_miniIsoId[nsel] >= 2) var = var + 4;
  if(mu_mvaId[nsel] >= 3 && mu_miniIsoId[nsel] >= 3) var = var + 8;
  if(mu_mvaId[nsel] >= 2 && mu_miniIsoId[nsel] >= 3) var = var + 16;
  if(mu_mvaId[nsel] >= 3 && mu_pfIsoId[nsel] >= 4) var = var + 32;
  if(mu_tightId[nsel] == true && mu_mvaTTH[nsel] > 0.7) var = var + 64;
  if(mu_mvaId[nsel] >= 4 && mu_miniIsoId[nsel] >= 4) var = var + 128;

  return var;
}

// Electron Id variables
int compute_elid_var(const Vec_i& el_cutBased, const Vec_b& el_mvaFall17V2Iso_WP90, const Vec_b& el_mvaFall17V2Iso_WP80,
                     const Vec_i& el_tightCharge, const Vec_f& el_mvaTTH, unsigned int nsel)
{
  if(el_cutBased.size() < nsel+1) return -1;

  int var = 0;
  if(el_cutBased[nsel] >= 3) var = var + 1;
  if(el_cutBased[nsel] >= 4) var = var + 2;
  if(el_mvaFall17V2Iso_WP90[nsel] == true) var = var + 4;
  if(el_mvaFall17V2Iso_WP80[nsel] == true) var = var + 8;
  if(el_mvaTTH[nsel] > 0.5) var = var + 16;
  if(el_cutBased[nsel] >= 4 && el_tightCharge[nsel] == 2) var = var + 32;
  if(el_mvaFall17V2Iso_WP80[nsel] == true && el_tightCharge[nsel] == 2) var = var + 64;
  if(el_mvaTTH[nsel] > 0.5 && el_tightCharge[nsel] == 2) var = var + 128;

  return var;
}

// Met-lepton-gamma variables
float compute_met_lepton_gamma_var(Vec_f pt, Vec_f eta, Vec_f phi, Vec_f mass, 
                                   const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass,
                                   const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass,
			           const float met_pt, const float met_phi,
				   const Vec_f& ph_pt, const Vec_f& ph_eta, const Vec_f& ph_phi,
		                   unsigned int var)
{
  if(mu_pt.size() + el_pt.size() < 2) return -1;
  if(ph_pt.size() < 1) return -1;

  float HT[2]= {0,0};
  PtEtaPhiMVector p4llgmom = PtEtaPhiMVector(0.0,0.0,0.0,0.0);

  for(unsigned int i=0;i<mu_pt.size();i++) {
    HT[0] += mu_pt[i];
    p4llgmom += PtEtaPhiMVector(mu_pt[i],mu_eta[i],mu_phi[i],mu_mass[i]);
  }

  for(unsigned int i=0;i<el_pt.size();i++) {
    HT[0] += el_pt[i];
    p4llgmom += PtEtaPhiMVector(el_pt[i],el_eta[i],el_phi[i],el_mass[i]);
  }

  HT[0] += ph_pt[0];
  p4llgmom += PtEtaPhiMVector(ph_pt[0],ph_eta[0],ph_phi[0],0.0);

  PtEtaPhiMVector p4jetmom = PtEtaPhiMVector(met_pt,0.0,met_phi,0.0);
  float dPhiJMET = 999.;
  for(unsigned int i=0;i<pt.size();i++) {
    HT[1] += pt[i];
    p4jetmom += PtEtaPhiMVector(pt[i],eta[i],phi[i],mass[i]);
    if(dPhiJMET > deltaPhi(phi[i],met_phi)) dPhiJMET = deltaPhi(phi[i],met_phi);
  }

  double theVar = 0;
  if     (var == 0) theVar = fabs(p4llgmom.Pt()-met_pt)/p4llgmom.Pt();
  else if(var == 1) theVar = fabs(p4llgmom.Pt()-p4jetmom.Pt())/p4llgmom.Pt();
  else if(var == 2) theVar = deltaPhi(p4llgmom.Phi(),met_phi);
  else if(var == 3) theVar = deltaPhi(p4llgmom.Phi(),p4jetmom.Phi());
  else if(var == 4) theVar = sqrt(2*ph_pt[0]*met_pt*(1-cos(deltaPhi(ph_phi[0],met_phi))));
  else if(var == 5) theVar = HT[1]/(HT[0]+HT[1]);
  else if(var == 6) theVar = ph_pt[0];
  else if(var == 7) theVar = p4llgmom.M();
  return theVar;
}

// Met-lepton variables
float compute_met_lepton_var(Vec_f pt, Vec_f eta, Vec_f phi, Vec_f mass, 
                             const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass,
                             const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass,
			     const float met_pt, const float met_phi,
		             unsigned int var)
{
  if(mu_pt.size() + el_pt.size() < 2) return -1;

  float HT[2]= {0,0};
  PtEtaPhiMVector p4llmom = PtEtaPhiMVector(0.0,0.0,0.0,0.0);

  for(unsigned int i=0;i<mu_pt.size();i++) {
    HT[0] += mu_pt[i];
    p4llmom += PtEtaPhiMVector(mu_pt[i],mu_eta[i],mu_phi[i],mu_mass[i]);
  }

  for(unsigned int i=0;i<el_pt.size();i++) {
    HT[0] += el_pt[i];
    p4llmom += PtEtaPhiMVector(el_pt[i],el_eta[i],el_phi[i],el_mass[i]);
  }

  PtEtaPhiMVector p4jetmom = PtEtaPhiMVector(met_pt,0.0,met_phi,0.0);
  float dPhiJMET = 999.;
  for(unsigned int i=0;i<pt.size();i++) {
    HT[1] += pt[i];
    p4jetmom += PtEtaPhiMVector(pt[i],eta[i],phi[i],mass[i]);
    if(dPhiJMET > deltaPhi(phi[i],met_phi)) dPhiJMET = deltaPhi(phi[i],met_phi);
  }

  double theVar = 0;
  if     (var == 0) theVar = fabs(p4llmom.Pt()-met_pt)/p4llmom.Pt();
  else if(var == 1) theVar = fabs(p4llmom.Pt()-p4jetmom.Pt())/p4llmom.Pt();
  else if(var == 2) theVar = deltaPhi(p4llmom.Phi(),met_phi);
  else if(var == 3) theVar = deltaPhi(p4llmom.Phi(),p4jetmom.Phi());
  else if(var == 4) theVar = sqrt(2*p4llmom.Pt()*met_pt*(1-cos(deltaPhi(p4llmom.Phi(),met_phi))));
  else if(var == 5) theVar = HT[1]/(HT[0]+HT[1]);
  else if(var == 6) theVar = dPhiJMET;
  return theVar;
}

// Jet-X-gamma variables
float compute_jet_x_gamma_var(Vec_f pt, Vec_f eta, Vec_f phi, Vec_f mass, 
                             const float  x_pt, const float  x_eta, const float  x_phi, const float x_mass,
                             const float ph_pt, const float ph_eta, const float pt_phi,
		             unsigned int var)
{
  if(pt.size() < 2) return -1;

  PtEtaPhiMVector p1(pt[0], eta[0], phi[0], mass[0]);
  PtEtaPhiMVector p2(pt[1], eta[1], phi[1], mass[1]);
  if(p1.Pt() < p2.Pt()) printf("Pt jet reversed!\n");
  for(unsigned int i=0;i<pt.size();i++) {
    for(unsigned int j=i+1;j<pt.size();j++) {
      if(pt[i]<pt[j]) {
        float temp0 = pt[i]; float temp1 = eta[i]; float temp2 = phi[i]; float temp3 = mass[i];
        pt[i] = pt[j];	     eta[i] = eta[j];	   phi[i] = phi[j];      mass[i] = mass[j];
        pt[j] = temp0;	     eta[j] = temp1;	   phi[j] = temp2;	 mass[j] = temp3;
      }
    }
  }

  float deltaEtaJJ = fabs(p1.Eta()-p2.Eta());
  float sumHT = p1.Pt() + p2.Pt() + x_pt + ph_pt;

  PtEtaPhiMVector p4momX  = PtEtaPhiMVector( x_pt, x_eta, x_phi, x_mass);
  PtEtaPhiMVector p4momPh = PtEtaPhiMVector(ph_pt,ph_eta,pt_phi, 0);

  PtEtaPhiMVector p4momVV = p4momX + p4momPh;
  PtEtaPhiMVector p4momTot = p4momX + p4momPh + p1 + p2;

  float maxZ = fabs(x_eta-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ;
  if(fabs(ph_eta-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ > maxZ) maxZ = fabs(ph_eta-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ;

  double theVar = 0;
  if     (var == 0) theVar = fabs(p4momVV.Eta()-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ;
  else if(var == 1) theVar = maxZ;
  else if(var == 2) theVar = sumHT;
  else if(var == 3) theVar = p4momVV.Pt();
  else if(var == 4) theVar = p4momTot.Pt();
  else if(var == 5) theVar = fabs(p4momVV.Eta()-p1.Eta());
  else if(var == 6) theVar = fabs(p4momVV.Eta()-p2.Eta());
  else if(var == 7) theVar = (p4momVV.Pt()-(p1+p2).Pt())/(p1+p2).Pt();
  return theVar;
}

// Jet-lepton variables
float compute_jet_lepton_var(Vec_f pt, Vec_f eta, Vec_f phi, Vec_f mass, 
                             const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass,
                             const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass,
		             const float met_pt, const float met_phi, unsigned int var)
{
  if(mu_pt.size() + el_pt.size() == 0) return -1;
  if(pt.size() < 2) return -1;

  PtEtaPhiMVector p1(pt[0], eta[0], phi[0], mass[0]);
  PtEtaPhiMVector p2(pt[1], eta[1], phi[1], mass[1]);
  if(p1.Pt() < p2.Pt()) printf("Pt jet reversed!\n");
  for(unsigned int i=0;i<pt.size();i++) {
    for(unsigned int j=i+1;j<pt.size();j++) {
      if(pt[i]<pt[j]) {
        float temp0 = pt[i]; float temp1 = eta[i]; float temp2 = phi[i]; float temp3 = mass[i];
        pt[i] = pt[j];	     eta[i] = eta[j];	   phi[i] = phi[j];      mass[i] = mass[j];
        pt[j] = temp0;	     eta[j] = temp1;	   phi[j] = temp2;	 mass[j] = temp3;
      }
    }
  }

  float deltaEtaJJ = fabs(p1.Eta()-p2.Eta());
  float maxZ = 0.0;
  float sumHT = p1.Pt() + p2.Pt() + met_pt;

  vector<PtEtaPhiMVector> p4mom;

  for(unsigned int i=0;i<mu_pt.size();i++) {
    p4mom.push_back(PtEtaPhiMVector(mu_pt[i],mu_eta[i],mu_phi[i],mu_mass[i]));
    if(fabs(mu_eta[i]-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ > maxZ) maxZ = fabs(mu_eta[i]-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ;
    sumHT += mu_pt[i];
  }

  for(unsigned int i=0;i<el_pt.size();i++) {
    p4mom.push_back(PtEtaPhiMVector(el_pt[i],el_eta[i],el_phi[i],el_mass[i]));   
    if(fabs(el_eta[i]-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ > maxZ) maxZ = fabs(el_eta[i]-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ;
    sumHT += el_pt[i];
  }

  PtEtaPhiMVector p4momVV = PtEtaPhiMVector(met_pt,0,met_phi,0);
  PtEtaPhiMVector p4momTot = PtEtaPhiMVector(met_pt,0,met_phi,0) + p1 + p2;
  for(unsigned int i=0; i<p4mom.size(); i++){
    p4momVV = p4momVV + p4mom[i];
    p4momTot = p4momTot + p4mom[i];
  }

  double theVar = 0;
  if     (var == 0) theVar = fabs(p4momVV.Eta()-(p1.Eta()+p2.Eta())/2.)/deltaEtaJJ;
  else if(var == 1) theVar = maxZ;
  else if(var == 2) theVar = sumHT;
  else if(var == 3) theVar = p4momVV.Pt();
  else if(var == 4) theVar = p4momTot.Pt();
  else if(var == 5) theVar = fabs(p4momVV.Eta()-p1.Eta());
  else if(var == 6) theVar = fabs(p4momVV.Eta()-p2.Eta());
  else if(var == 7) theVar = (p4momVV.Pt()-(p1+p2).Pt())/(p1+p2).Pt();
  return theVar;
}

// Jet variables
float compute_jet_var(Vec_f pt, Vec_f eta, Vec_f phi, Vec_f mass, unsigned int var)
{
  if(pt.size() < 2) return -1;
  PtEtaPhiMVector p1(pt[0], eta[0], phi[0], mass[0]);
  PtEtaPhiMVector p2(pt[1], eta[1], phi[1], mass[1]);
  if(p1.Pt() < p2.Pt()) printf("Pt jet reversed!\n");
  for(unsigned int i=0;i<pt.size();i++) {
    for(unsigned int j=i+1;j<pt.size();j++) {
      if(pt[i]<pt[j]) {
        float temp0 = pt[i]; float temp1 = eta[i]; float temp2 = phi[i]; float temp3 = mass[i];
        pt[i] = pt[j];	     eta[i] = eta[j];	   phi[i] = phi[j];      mass[i] = mass[j];
        pt[j] = temp0;	     eta[j] = temp1;	   phi[j] = temp2;	 mass[j] = temp3;
      }
    }
  }

  double theVar = 0;
  if	 (var == 0) theVar = (p1 + p2).M();
  else if(var == 1) theVar = (p1 + p2).Pt();
  else if(var == 2) theVar = fabs(p1.Eta()-p2.Eta());
  else if(var == 3) theVar = deltaPhi(p1.Phi(), p2.Phi());
  else if(var == 4) theVar = p1.Pt();
  else if(var == 5) theVar = p2.Pt();
  else if(var == 6) theVar = abs(p1.Eta());
  else if(var == 7) theVar = abs(p2.Eta());
  return theVar;
}

// lepton+met variables
float compute_lmet_var(const Vec_f& mu_pt, const Vec_f& mu_phi,
                       const Vec_f& el_pt, const Vec_f& el_phi,
		       const float met_pt, const float met_phi,
		       unsigned int var)
{
   float ptl, phil;
   if(mu_pt.size() == 1){
       ptl = mu_pt[0]; phil = mu_phi[0];
   }
   else if(el_pt.size() == 1){
       ptl = el_pt[0]; phil = el_phi[0];
   }
   else {
      return 0;
   }

   double theVar = 0;
   if     (var == 0) theVar = std::sqrt(2*ptl*met_pt*(1-std::cos(deltaPhi(phil,met_phi))));
   else if(var == 1) theVar = deltaPhi(phil,met_phi);
   else if(var == 2) theVar = std::sqrt(2*30.0*met_pt*(1-std::cos(deltaPhi(phil,met_phi))));
   else if(var == 3) theVar = std::max(std::sqrt(2*ptl*met_pt*(1-std::cos(deltaPhi(phil,met_phi)))),met_pt);
   else if(var == 4) theVar = std::min(std::sqrt(2*ptl*met_pt*(1-std::cos(deltaPhi(phil,met_phi)))),met_pt);

   theVar = std::min(theVar, 199.999);
   
   return theVar;
}

// Dilepton variables
float compute_ll_var(const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass,
                     const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass,
		     unsigned int var)
{
   if(mu_pt.size() + el_pt.size() != 2) return 0;

   float pt[2], eta[2], phi[2], mass[2];
   if(mu_pt.size() == 2){
       pt[0] = mu_pt[0]; eta[0] = mu_eta[0]; phi[0] = mu_phi[0]; mass[0] = mu_mass[0];
       pt[1] = mu_pt[1]; eta[1] = mu_eta[1]; phi[1] = mu_phi[1]; mass[1] = mu_mass[1];
   }
   else if(el_pt.size() == 2){
       pt[0] = el_pt[0]; eta[0] = el_eta[0]; phi[0] = el_phi[0]; mass[0] = el_mass[0];
       pt[1] = el_pt[1]; eta[1] = el_eta[1]; phi[1] = el_phi[1]; mass[1] = el_mass[1];
   }
   else if(mu_pt.size() == 1 && el_pt.size() == 1){
       pt[0] = mu_pt[0]; eta[0] = mu_eta[0]; phi[0] = mu_phi[0]; mass[0] = mu_mass[0];
       pt[1] = el_pt[0]; eta[1] = el_eta[0]; phi[1] = el_phi[0]; mass[1] = el_mass[0];
   }
   else {
      return 0;
   }

   PtEtaPhiMVector p1(pt[0],eta[0],phi[0],mass[0]);
   PtEtaPhiMVector p2(pt[1],eta[1],phi[1],mass[1]);
   if(pt[0] < pt[1]){
     PtEtaPhiMVector paux = p2;
     p2 = p1;
     p1 = paux;
   }
   if(p1.Pt() < p2.Pt()) printf("Pt lepton reversed!\n");

   double theVar = 0;
   if     (var == 0) theVar = (p1 + p2).M();
   else if(var == 1) theVar = (p1 + p2).Pt();
   else if(var == 2) theVar = deltaR(p1.Eta(), p1.Phi(), p2.Eta(), p2.Phi());
   else if(var == 3) theVar = deltaPhi(p1.Phi(), p2.Phi());
   else if(var == 4) theVar = p1.Pt();
   else if(var == 5) theVar = p2.Pt();
   else if(var == 6) theVar = p1.Eta();
   else if(var == 7) theVar = p2.Eta();
   return theVar;
}

// Trilepton variables
float compute_3l_var(const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass, const Vec_f& mu_charge,
                     const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass, const Vec_f& el_charge,
		     const float met_pt, const float met_phi, unsigned int var)
{
   if(mu_pt.size() + el_pt.size() != 3) return 0;

   vector<PtEtaPhiMVector> p4mom;
   vector<int> charge, ltype;
   if     (mu_pt.size() == 3){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[2],mu_eta[2],mu_phi[2],mu_mass[2])); charge.push_back(mu_charge[2]); ltype.push_back(0);
   }
   else if(mu_pt.size() == 2){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 1){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 0){
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[2],el_eta[2],el_phi[2],el_mass[2])); charge.push_back(el_charge[2]); ltype.push_back(1);
   }
   else {
      printf("3l impossible combination\n");
      return 0;
   }

   for(unsigned int i=0; i<p4mom.size(); i++){
     for(unsigned int j=i+1; j<p4mom.size(); j++){
       if(p4mom[i].Pt() < p4mom[j].Pt()){
         PtEtaPhiMVector paux = p4mom[j]; int chargeaux = charge[j]; int ltypeaux = ltype[j];
         p4mom[j] = p4mom[i];                 charge[j] = charge[i];     ltype[j] = ltype[i];
         p4mom[i] = paux;                     charge[i] = chargeaux;     ltype[i] = ltypeaux;
       }
     }
   }

   float mllmin = 10000; float drllmin = 10000;
   PtEtaPhiMVector p4momTot = p4mom[0];
   for(unsigned int i=0; i<p4mom.size(); i++){
     if(i != 0) p4momTot = p4momTot + p4mom[i];
     for(unsigned int j=i+1; j<p4mom.size(); j++){
       if(charge[i] == charge[j]) continue;
       if((p4mom[i]+p4mom[j]).M() < mllmin) mllmin = (p4mom[i]+p4mom[j]).M();
       if(deltaR(p4mom[i].Eta(),p4mom[i].Phi(),p4mom[j].Eta(),p4mom[j].Phi()) < drllmin){
         drllmin = deltaR(p4mom[i].Eta(), p4mom[i].Phi(), p4mom[j].Eta(), p4mom[j].Phi());
       }
     }
   }

   double mllZ = 10000;
   int tagZ[2] = {-1, -1}; int tagW = -1;
   double theVar = 0;
   if     (var == 0) theVar = p4momTot.M();
   else if(var == 1) theVar = mllmin;
   else if(var == 2) theVar = drllmin;
   else if(var == 3) theVar = p4mom[0].Pt();
   else if(var == 4) theVar = p4mom[1].Pt();
   else if(var == 5) theVar = p4mom[2].Pt();
   else {
     for(int i=0; i<3; i++){
       for(int j=i+1; j<3; j++){  
         if(charge[i] != charge[j] && ltype[i] == ltype[j]){
           if(fabs((p4mom[i]+p4mom[j]).M()-91.1876) < fabs(mllZ-91.1876)) {
	     mllZ = (p4mom[i]+p4mom[j]).M();
	     tagZ[0] = i;
	     tagZ[1] = j;
	   }
         }
       }
     }
     if(tagZ[0] == -1) return -1;
     for(int i=0; i<3; i++){
       if(i != tagZ[0] && i != tagZ[1]) tagW = i;
     }
     
     if     (var ==  6) theVar = mllZ;
     else if(var ==  7) theVar = p4mom[tagZ[0]].Pt();
     else if(var ==  8) theVar = p4mom[tagZ[1]].Pt();
     else if(var ==  9) theVar = p4mom[tagW].Pt();
     else if(var == 10) theVar = std::sqrt(2*p4mom[tagW].Pt()*met_pt*(1-std::cos(deltaPhi(p4mom[tagW].Phi(),met_phi))));
   }
   return theVar;
}

// Fourlepton variables
float compute_4l_var(const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass, const Vec_f& mu_charge,
                     const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass, const Vec_f& el_charge,
		     const float met_pt, const float met_phi, unsigned int var)
{
   if(mu_pt.size() + el_pt.size() != 4) return 0;

   vector<PtEtaPhiMVector> p4mom;
   vector<int> charge, ltype;
   if     (mu_pt.size() == 4){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[2],mu_eta[2],mu_phi[2],mu_mass[2])); charge.push_back(mu_charge[2]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[3],mu_eta[3],mu_phi[3],mu_mass[3])); charge.push_back(mu_charge[3]); ltype.push_back(0);
   }
   else if(mu_pt.size() == 3){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[2],mu_eta[2],mu_phi[2],mu_mass[2])); charge.push_back(mu_charge[2]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 2){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 1){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[2],el_eta[2],el_phi[2],el_mass[2])); charge.push_back(el_charge[2]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 0){
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[2],el_eta[2],el_phi[2],el_mass[2])); charge.push_back(el_charge[2]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[3],el_eta[3],el_phi[3],el_mass[3])); charge.push_back(el_charge[3]); ltype.push_back(1);
   }
   else {
      printf("4l impossible combination\n");
      return 0;
   }

   for(unsigned int i=0; i<p4mom.size(); i++){
     for(unsigned int j=i+1; j<p4mom.size(); j++){
       if(p4mom[i].Pt() < p4mom[j].Pt()){
         PtEtaPhiMVector paux = p4mom[j]; int chargeaux = charge[j]; int ltypeaux = ltype[j];
         p4mom[j] = p4mom[i];                 charge[j] = charge[i];     ltype[j] = ltype[i];
         p4mom[i] = paux;                     charge[i] = chargeaux;     ltype[i] = ltypeaux;
       }
     }
   }

   float mllmin = 10000; float ptmax = 0;
   PtEtaPhiMVector p4momTot = p4mom[0];
   for(unsigned int i=0; i<p4mom.size(); i++){
     if(p4mom[i].Pt() > ptmax) ptmax = p4mom[i].Pt();
     if(i != 0) p4momTot = p4momTot + p4mom[i];
     for(unsigned int j=i+1; j<p4mom.size(); j++){
       if((p4mom[i]+p4mom[j]).M() < mllmin) mllmin = (p4mom[i]+p4mom[j]).M();
     }
   }
   
   float mllZ1 = 100000; float mllZ2 = 100000; float mllxy = 0;
   int tagZ1[2] = {-1, -1}; int tagZ2[2] = {-1, -1};
   float theVar = 0;
   if     (var == 0) theVar = p4momTot.M();
   else if(var == 1) theVar = ptmax;
   else if(var == 2) theVar = mllmin;
   else {
     for(int i=0; i<4; i++){
       for(int j=i+1; j<4; j++){  
         if(charge[i] != charge[j] && ltype[i] == ltype[j]){
           if(fabs((p4mom[i]+p4mom[j]).M()-91.1876) < fabs(mllZ1-91.1876)) {
	     mllZ1 = (p4mom[i]+p4mom[j]).M();
	     tagZ1[0] = i;
	     tagZ1[1] = j;
	   }
         }
       }
     }
     if(tagZ1[0] == -1) return -1;
     for(int i=0; i<4; i++){
       if(i != tagZ1[0] && i != tagZ1[1] && tagZ2[0] == -1) tagZ2[0] = i;
     }
     for(int i=0; i<4; i++){
       if(i != tagZ1[0] && i != tagZ1[1] && i != tagZ2[0]) tagZ2[1] = i;
     }

     if(charge[tagZ2[0]] != charge[tagZ2[1]] && ltype[tagZ2[0]] == ltype[tagZ2[1]]){     
       mllZ2 = (p4mom[tagZ2[0]]+p4mom[tagZ2[1]]).M();
     }
     else if(tagZ2[0] >= 0 && tagZ2[1] >= 0 && charge[tagZ2[0]] != charge[tagZ2[1]]){     
       mllxy = (p4mom[tagZ2[0]]+p4mom[tagZ2[1]]).M();
     }
     else if(tagZ2[0] >= 0 && tagZ2[1] >= 0){     
       mllxy = 0.0;
       printf("mllxy same-sign leptons %d %d\n",tagZ2[0],tagZ2[1]);
     }
     else {     
       printf("mllxy problem %d %d\n",tagZ2[0],tagZ2[1]);
     }
     
     if     (var ==  3) theVar = fabs(mllZ1-91.1876);
     else if(var ==  4) theVar = fabs(mllZ2-91.1876);
     else if(var ==  5) theVar = p4mom[tagZ1[0]].Pt();
     else if(var ==  6) theVar = p4mom[tagZ1[1]].Pt();
     else if(var ==  7) theVar = p4mom[tagZ2[0]].Pt();
     else if(var ==  8) theVar = p4mom[tagZ2[1]].Pt();
     else if(var ==  9) theVar = mllxy;
     else if(var == 10) theVar = (p4mom[tagZ1[0]]+p4mom[tagZ1[1]]).Pt();
     else if(var == 11) theVar = (p4mom[tagZ2[0]]+p4mom[tagZ2[1]]).Pt();
     else if(var == 12) theVar = std::sqrt(2*(p4mom[tagZ2[0]]+p4mom[tagZ2[1]]).Pt()*met_pt*(1-std::cos(deltaPhi((p4mom[tagZ2[0]]+p4mom[tagZ2[1]]).Phi(),met_phi))));
   }
   return theVar;
}


// Multilepton variables
float compute_nl_var(const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass, const Vec_f& mu_charge,
                     const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass, const Vec_f& el_charge,
		     const float met_pt, const float met_phi, unsigned int var)
{
   if(mu_pt.size() + el_pt.size() < 2 || mu_pt.size() + el_pt.size() > 4) return 0;

   vector<PtEtaPhiMVector> p4mom;
   vector<int> charge, ltype;
   if     (mu_pt.size() == 4 && el_pt.size() == 0){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[2],mu_eta[2],mu_phi[2],mu_mass[2])); charge.push_back(mu_charge[2]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[3],mu_eta[3],mu_phi[3],mu_mass[3])); charge.push_back(mu_charge[3]); ltype.push_back(0);
   }
   else if(mu_pt.size() == 3 && el_pt.size() == 1){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[2],mu_eta[2],mu_phi[2],mu_mass[2])); charge.push_back(mu_charge[2]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 2 && el_pt.size() == 2){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 1 && el_pt.size() == 3){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[2],el_eta[2],el_phi[2],el_mass[2])); charge.push_back(el_charge[2]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 0 && el_pt.size() == 4){
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[2],el_eta[2],el_phi[2],el_mass[2])); charge.push_back(el_charge[2]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[3],el_eta[3],el_phi[3],el_mass[3])); charge.push_back(el_charge[3]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 3 && el_pt.size() == 0){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[2],mu_eta[2],mu_phi[2],mu_mass[2])); charge.push_back(mu_charge[2]); ltype.push_back(0);
   }
   else if(mu_pt.size() == 2 && el_pt.size() == 1){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 1 && el_pt.size() == 2){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 0 && el_pt.size() == 3){
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[2],el_eta[2],el_phi[2],el_mass[2])); charge.push_back(el_charge[2]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 2 && el_pt.size() == 0){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(mu_pt[1],mu_eta[1],mu_phi[1],mu_mass[1])); charge.push_back(mu_charge[1]); ltype.push_back(0);
   }
   else if(mu_pt.size() == 1 && el_pt.size() == 1){
       p4mom.push_back(PtEtaPhiMVector(mu_pt[0],mu_eta[0],mu_phi[0],mu_mass[0])); charge.push_back(mu_charge[0]); ltype.push_back(0);
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
   }
   else if(mu_pt.size() == 0 && el_pt.size() == 2){
       p4mom.push_back(PtEtaPhiMVector(el_pt[0],el_eta[0],el_phi[0],el_mass[0])); charge.push_back(el_charge[0]); ltype.push_back(1);
       p4mom.push_back(PtEtaPhiMVector(el_pt[1],el_eta[1],el_phi[1],el_mass[1])); charge.push_back(el_charge[1]); ltype.push_back(1);
   }
   else {
      printf("Impossible combination %lu %lu\n",mu_pt.size(),el_pt.size());
      return 0;
   }

   for(unsigned int i=0; i<p4mom.size(); i++){
     for(unsigned int j=i+1; j<p4mom.size(); j++){
       if(p4mom[i].Pt() < p4mom[j].Pt()){
         PtEtaPhiMVector paux = p4mom[j]; int chargeaux = charge[j]; int ltypeaux = ltype[j];
         p4mom[j] = p4mom[i];                 charge[j] = charge[i];     ltype[j] = ltype[i];
         p4mom[i] = paux;                     charge[i] = chargeaux;     ltype[i] = ltypeaux;
       }
     }
   }

   float mllmin = 10000;
   PtEtaPhiMVector p4momTot = p4mom[0];
   for(unsigned int i=0; i<p4mom.size(); i++){
     if(i != 0) p4momTot = p4momTot + p4mom[i];
     for(unsigned int j=i+1; j<p4mom.size(); j++){
       if((p4mom[i]+p4mom[j]).M() < mllmin) mllmin = (p4mom[i]+p4mom[j]).M();
     }
   }

   float theVar = -1;
   if     (var == 0) theVar = p4momTot.M();
   else if(var == 1) theVar = mllmin;
   else if(var == 2) {
     if     (p4mom.size() == 2 && ltype[0] == 0 && ltype[1] == 0) theVar = 0.;
     else if(p4mom.size() == 2 && ltype[0] == 1 && ltype[1] == 1) theVar = 1.;
     else if(p4mom.size() == 2 && ltype[0] == 0 && ltype[1] == 1) theVar = 2.;
     else if(p4mom.size() == 2 && ltype[0] == 1 && ltype[1] == 0) theVar = 3.;
     else if(p4mom.size() == 3) theVar = 4.;
     else if(p4mom.size() == 4) theVar = 5.;
     else printf("Impossible ltype %lu %lu\n",mu_pt.size(),el_pt.size());
   }
   else {
     if     (var ==  3) theVar = p4mom[0].Pt();
     else if(var ==  4) theVar = p4mom[p4mom.size()-1].Pt();
     else if(var ==  5) theVar = abs(p4mom[0].Eta());
     else if(var ==  6) theVar = abs(p4mom[p4mom.size()-1].Eta());
   }
   return theVar;
}

int applySkim(const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass,
              const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass,
	      const int lep_charge, const float met_pt)
{
   if     (mu_pt.size() + el_pt.size() < 2) return 0;
   else if(mu_pt.size() + el_pt.size() > 2) return 1;

   float pt[2], eta[2], phi[2], mass[2];
   if(mu_pt.size() == 2){
       pt[0] = mu_pt[0]; eta[0] = mu_eta[0]; phi[0] = mu_phi[0]; mass[0] = mu_mass[0];
       pt[1] = mu_pt[1]; eta[1] = mu_eta[1]; phi[1] = mu_phi[1]; mass[1] = mu_mass[1];
   }
   else if(el_pt.size() == 2){
       pt[0] = el_pt[0]; eta[0] = el_eta[0]; phi[0] = el_phi[0]; mass[0] = el_mass[0];
       pt[1] = el_pt[1]; eta[1] = el_eta[1]; phi[1] = el_phi[1]; mass[1] = el_mass[1];
   }
   else if(mu_pt.size() == 1 && el_pt.size() == 1){
       pt[0] = mu_pt[0]; eta[0] = mu_eta[0]; phi[0] = mu_phi[0]; mass[0] = mu_mass[0];
       pt[1] = el_pt[0]; eta[1] = el_eta[0]; phi[1] = el_phi[0]; mass[1] = el_mass[0];
   }
   else {
      printf("This lep comb can not happen\n");
      return 0;
   }

   PtEtaPhiMVector p1(pt[0],eta[0],phi[0],mass[0]);
   PtEtaPhiMVector p2(pt[1],eta[1],phi[1],mass[1]);
   if(pt[0] < pt[1]){
     PtEtaPhiMVector paux = p2;
     p2 = p1;
     p1 = paux;
   }
   if(p1.Pt() < p2.Pt()) printf("Pt lepton reversed!\n");

   double mll = (p1 + p2).M();
   if(mll <= 10) return 0;

   if     (lep_charge != 0) return 2;
   else if(met_pt > 50 && (p1 + p2).Pt() > 50) return 3;
   else return 4;

   printf("This can not happen\n");
   return 0;
}

// Select meson-photon pair
Vec_i HiggsCandFromRECO(const Vec_f& meson_pt, const Vec_f& meson_eta, const Vec_f& meson_phi, const Vec_f& meson_mass,
                        const Vec_f& ph_pt, const Vec_f& ph_eta, const Vec_f& ph_phi) {

  Vec_i idx(2, -1); // initialize with -1 a vector of size 2
  if(ph_pt.size() == 0 || meson_pt.size() == 0) return idx;

  //float Minv = -1;
  //float ptHiggs = -1;
  float ptCandMax=0;

  PtEtaPhiMVector p_ph(ph_pt[0], ph_eta[0], ph_phi[0], 0);
  int indexPhoton = 0;
  for(unsigned int i=1; i<ph_pt.size(); i++){
    if(ph_pt[i] > p_ph.Pt()) {
      p_ph.SetPt(ph_pt[i]);
      p_ph.SetEta(ph_eta[i]);
      p_ph.SetPhi(ph_phi[i]);
      indexPhoton = i;
    }
  }

  // loop over all the phiCand
  for (unsigned int i=0; i<meson_pt.size(); i++) {

    PtEtaPhiMVector p_meson(meson_pt[i], meson_eta[i], meson_phi[i], meson_mass[i]);
    // save the leading Pt
    float ptCand = p_meson.pt();
    if( ptCand < ptCandMax ) continue;
    ptCandMax=ptCand;
    //Minv = (p_meson + p_ph).mass();
    //ptHiggs = (p_meson + p_ph).pt();
    idx[0] = i;
    idx[1] = indexPhoton;
  }

  return idx;

}

// cleaning jets close-by to the meson
Vec_b cleaningJetFromMeson(Vec_f & Jeta, Vec_f & Jphi, float & eta, float & phi) {

  Vec_b mask(Jeta.size(), true);
  for (unsigned int idx = 0; idx < Jeta.size(); ++idx) {
    if(deltaR(Jeta[idx], Jphi[idx], eta, phi)<0.3) mask[idx] = false;
  }
  return mask;
}

// Minv2
std::pair<float, float>  Minv2(const float& pt, const float& eta, const float& phi, const float& m,
                               const float& ph_pt, const float& ph_eta, const float& ph_phi) {

  PtEtaPhiMVector p_M(pt, eta, phi, m);
  PtEtaPhiMVector p_ph(ph_pt, ph_eta, ph_phi, 0);

  float Minv = (p_M + p_ph).mass();
  float ptPair = (p_M + p_ph).pt();

  std::pair<float, float> pairRECO = std::make_pair(Minv , ptPair);
  return pairRECO;

}

// compute category
int compute_category(const int mc, const int typeFake, const int nFake, const int nTight){
  if     (nFake > nTight) return typeFake;
  else if(nFake < nTight) {printf("IMPOSSIBLE compute_category\n"); return -1;}
  return mc;
}

// compute category
float compute_weights(const float weight, const float genWeight, const TString theCat,
                      const Vec_f& mu_genPartFlav, const Vec_f& el_genPartFlav, unsigned int var){
  if(theCat.Contains("WJetsToLNu") && genWeight > 10000) {
    printf("Huge genWeight: %f\n",genWeight);
    return 0.0;
  }
  if(var == 1) {
    bool isRealGenLep = true;
    for(unsigned int i=0;i<mu_genPartFlav.size();i++) {
       if(mu_genPartFlav[i] != 1 && mu_genPartFlav[i] != 15) {isRealGenLep = false; break;}
    }
    if(isRealGenLep == false) return 0.0;

    for(unsigned int i=0;i<el_genPartFlav.size();i++) {
       if(el_genPartFlav[i] != 1 && el_genPartFlav[i] != 15 && el_genPartFlav[i] != 22) {isRealGenLep = false; break;}
    }
    if(isRealGenLep == false) return 0.0;
  }
  return weight*genWeight;
}

#endif

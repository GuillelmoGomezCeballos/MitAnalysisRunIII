#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include "TROOT.h"
#include "TFile.h"
#include "TH2.h"
#include "TH3.h"
#include "TF1.h"
#include "TH2Poly.h"
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

#include <iostream>
#include <stdlib.h>
#include <stdio.h>
#include <cstdlib> //as stdlib.h      
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
  return result;
}

float deltaR2(float eta1, float phi1, float eta2, float phi2) {
  float deta = eta1-eta2;
  float dphi = deltaPhi(phi1,phi2);
  return deta*deta + dphi*dphi;
}

float deltaR(float eta1, float phi1, float eta2, float phi2) {
  return std::sqrt(deltaR2(eta1,phi1,eta2,phi2));
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
  if(el_mvaTTH[nsel] > 0.7) var = var + 16;
  if(el_cutBased[nsel] >= 4 && el_tightCharge[nsel] == 2) var = var + 32;
  if(el_mvaFall17V2Iso_WP80[nsel] == true && el_tightCharge[nsel] == 2) var = var + 64;
  if(el_mvaTTH[nsel] > 0.7 && el_tightCharge[nsel] == 2) var = var + 128;

  return var;
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
      if(pt[i]>pt[j]) {
        float temp0 = pt[i]; float temp1 = eta[i]; float temp2 = phi[i]; float temp3 = mass[i];
        pt[i] = pt[j];	     eta[i] = eta[j];	   phi[i] = phi[j];      mass[i] = mass[j];
        pt[j] = temp0;	     eta[j] = temp1;	   phi[j] = temp2;	 mass[j] = temp3;
      }
    }
  }

  double theVar = 0;
  if	 (var == 0) theVar = (p1 + p2).M();
  else if(var == 1) theVar = (p1 + p2).Pt();
  else if(var == 2) theVar = deltaR(p1.Eta(), p1.Phi(), p2.Eta(), p2.Phi());
  else if(var == 3) theVar = deltaPhi(p1.Phi(), p2.Phi());
  else if(var == 4) theVar = p1.Pt();
  else if(var == 5) theVar = p2.Pt();
  else if(var == 6) theVar = p1.Eta();
  else if(var == 7) theVar = p2.Eta();
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
   if     (var == 0) theVar = std::sqrt(2*ptl*met_pt*(1-std::cos(phil-met_phi)));
   else if(var == 1) theVar = std::abs(deltaPhi(phil,met_phi));
   else if(var == 2) theVar = std::sqrt(2*35.0*met_pt*(1-std::cos(phil-met_phi)));
   return theVar;
}

// Dilepton variables
float compute_ll_var(const Vec_f& mu_pt, const Vec_f& mu_eta, const Vec_f& mu_phi, const Vec_f& mu_mass,
                     const Vec_f& el_pt, const Vec_f& el_eta, const Vec_f& el_phi, const Vec_f& el_mass,
		     unsigned int var)
{
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

// compute category
int compute_category(const int mc){
  return mc;
}

// compute category
float compute_weights(const float weight, const float genWeight){
  return weight*genWeight;
}

#endif

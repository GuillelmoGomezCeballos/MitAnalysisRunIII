#ifndef FUNCTIONS_H
#define FUNCTIONS_H

#include "TROOT.h"
#include "TFile.h"
#include "TH2.h"
#include "TH3.h"
#include "TF1.h"
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
   if     (var == 0) theVar = std::sqrt(2*ptl*met_pt*(1-std::cos(phil-met_phi)));
   else if(var == 1) theVar = std::abs(deltaPhi(phil,met_phi));
   else if(var == 2) theVar = std::sqrt(2*30.0*met_pt*(1-std::cos(phil-met_phi)));
   else if(var == 3) theVar = std::max(std::sqrt(2*ptl*met_pt*(1-std::cos(phil-met_phi))),met_pt);
   else if(var == 4) theVar = std::min(std::sqrt(2*ptl*met_pt*(1-std::cos(phil-met_phi))),met_pt);

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

   float mllmin = 10000;
   PtEtaPhiMVector p4momTot = p4mom[0];
   for(unsigned int i=0; i<p4mom.size(); i++){
     if(i != 0) p4momTot = p4momTot + p4mom[i];
     for(unsigned int j=i+1; j<p4mom.size(); j++){
       if((p4mom[i]+p4mom[j]).M() < mllmin) mllmin = (p4mom[i]+p4mom[j]).M();
     }
   }
   
   double mllZ = 10000;
   int tagZ[2] = {-1, -1}; int tagW = -1;
   double theVar = 0;
   if     (var == 0) theVar = p4momTot.M();
   else if(var == 1) theVar = mllmin;
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
     
     if     (var == 2) theVar = fabs(mllZ-91.1876);
     else if(var == 3) theVar = p4mom[tagZ[0]].Pt();
     else if(var == 4) theVar = p4mom[tagZ[1]].Pt();
     else if(var == 5) theVar = p4mom[tagW].Pt();
     else if(var == 6) theVar = std::sqrt(2*p4mom[tagW].Pt()*met_pt*(1-std::cos(p4mom[tagW].Phi()-met_phi)));
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

   float mllmin = 10000;
   PtEtaPhiMVector p4momTot = p4mom[0];
   for(unsigned int i=0; i<p4mom.size(); i++){
     if(i != 0) p4momTot = p4momTot + p4mom[i];
     for(unsigned int j=i+1; j<p4mom.size(); j++){
       if((p4mom[i]+p4mom[j]).M() < mllmin) mllmin = (p4mom[i]+p4mom[j]).M();
     }
   }
   
   double mllZ1 = 10000; double mllZ2 = 10000;
   int tagZ1[2] = {-1, -1}; int tagZ2[2] = {-1, -1};
   double theVar = 0;
   if     (var == 0) theVar = p4momTot.M();
   else if(var == 1) theVar = mllmin;
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
     
     if     (var == 2) theVar = fabs(mllZ1-91.1876);
     else if(var == 3) theVar = fabs(mllZ2-91.1876);
     else if(var == 4) theVar = p4mom[tagZ1[0]].Pt();
     else if(var == 5) theVar = p4mom[tagZ1[1]].Pt();
     else if(var == 6) theVar = p4mom[tagZ2[0]].Pt();
     else if(var == 7) theVar = p4mom[tagZ2[1]].Pt();
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

// compute category
int compute_category(const int mc){
  return mc;
}

// compute category
float compute_weights(const float weight, const float genWeight, const TString theCat){
  if(theCat.Contains("WJetsToLNu") && genWeight > 10000) {
    printf("Huge genWeight: %f\n",genWeight);
    return 0.0;
  }
  return weight*genWeight;
}

#endif

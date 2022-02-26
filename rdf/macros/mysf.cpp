#include "mysf.h"

MyCorrections::MyCorrections(int year) {
  char* fileNameMu = (char*)"";
  if(year == 2018){
    fileNameMu = (char*)"jsonpog/POG/2018/muon_Z.json";
  }
  auto csetMu = correction::CorrectionSet::from_file(fileNameMu);
  muonIDSF_ = csetMu->at("NUM_MediumID_DEN_genTracks");
  muonISOSF_ = csetMu->at("NUM_TightRelIso_DEN_MediumID");

  char* fileNameEl = (char*)"";
  if(year == 2018){
    fileNameEl = (char*)"jsonpog/POG/2018/electron.json";
  }
  auto csetEl = correction::CorrectionSet::from_file(fileNameEl);
  electronSF_ = csetEl->at("UL-Electron-ID-SF");

  char* fileNamePh = (char*)"";
  if(year == 2018){
    fileNamePh = (char*)"jsonpog/POG/2018/photon.json";
  }
  auto csetPh = correction::CorrectionSet::from_file(fileNamePh);
  photonSF_ = csetPh->at("UL-Photon-ID-SF");

  char* fileNameBTV = (char*)"";
  if(year == 2018){
    fileNameBTV = (char*)"jsonpog/POG/2018/btagging.json";
  }
  auto csetBTV = correction::CorrectionSet::from_file(fileNameBTV);
  btvHFSF_ = csetBTV->at("deepJet_comb");
  btvLFSF_ = csetBTV->at("deepJet_incl");

  char* fileNamePUJetID = (char*)"";
  if(year == 2018){
    fileNamePUJetID = (char*)"jsonpog/POG/2018/jmar.json";
  }
  auto csetPUJetID = correction::CorrectionSet::from_file(fileNamePUJetID);
  puJetIDSF_ = csetPUJetID->at("PUJetID_eff");
}

double MyCorrections::eval_muonIDSF(char *year, char *valType, char *workingPoint, double eta, double pt) {
  eta = abs(eta);
  return muonIDSF_->evaluate({year, eta, pt, valType});
};

double MyCorrections::eval_muonISOSF(char *year, char *valType, char *workingPoint, double eta, double pt) {
  eta = abs(eta);
  return muonISOSF_->evaluate({year, eta, pt, valType});
};

double MyCorrections::eval_electronSF(char *year, char *valType, char *workingPoint, double eta, double pt) {
  return electronSF_->evaluate({year, valType, workingPoint, eta, pt});
};

double MyCorrections::eval_photonSF(char *year, char *valType, char *workingPoint, double eta, double pt) {
  return photonSF_->evaluate({year, valType, workingPoint, eta, pt});
};

double MyCorrections::eval_btvSF(char *valType, char *workingPoint, double eta, double pt, int flavor) {
  if(flavor != 0)
    return btvHFSF_->evaluate({valType, workingPoint, flavor, eta, pt});
  else
    return btvLFSF_->evaluate({valType, workingPoint, flavor, eta, pt});
};

double MyCorrections::eval_puJetIDSF(char *valType, char *workingPoint, double eta, double pt) {
  return puJetIDSF_->evaluate({eta, pt, valType, workingPoint});
};

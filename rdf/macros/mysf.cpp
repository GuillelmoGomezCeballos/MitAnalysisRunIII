#include "mysf.h"

MyCorrections::MyCorrections(int year) {

  if(year == 2022) year = 2018;

  std::string dirName = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/";

  std::string subDirName = "";
  if     (year == 12016) subDirName += "2016preVFP_UL/";  
  else if(year == 22016) subDirName += "2016postVFP_UL/";
  else if(year == 2017)  subDirName += "2017_UL/";
  else if(year == 2018)  subDirName += "2018_UL/";
  
  std::string fileNameLUM = dirName+"LUM/"+subDirName+"puWeights.json.gz";

  std::string corrNameLUM = "";  
  if(year == 22016 or year == 12016) corrNameLUM = "Collisions16_UltraLegacy_goldenJSON";
  else if(year == 2017) corrNameLUM = "Collisions17_UltraLegacy_goldenJSON";
  else if(year == 2018) corrNameLUM = "Collisions18_UltraLegacy_goldenJSON";
  
  auto csetPU = correction::CorrectionSet::from_file(fileNameLUM);
  puSF_ = csetPU->at(corrNameLUM);
  
  std::string fileNameBTV = dirName+"BTV/"+subDirName+"btagging.json.gz";
  auto csetBTV = correction::CorrectionSet::from_file(fileNameBTV);
  btvHFSF_ = csetBTV->at("deepJet_comb");
  btvLFSF_ = csetBTV->at("deepJet_incl");

  std::string fileNameMu = dirName+"MUO/"+subDirName+"muon_Z.json.gz";
  auto csetMu = correction::CorrectionSet::from_file(fileNameMu);
  muonTRKSF_ = csetMu->at("NUM_TrackerMuons_DEN_genTracks");
  muonIDSF_ = csetMu->at("NUM_MediumID_DEN_genTracks");
  muonISOSF_ = csetMu->at("NUM_TightRelIso_DEN_MediumID");
  
  std::string fileNamePH = dirName+"EGM/"+subDirName+"photon.json.gz";
  auto csetPH = correction::CorrectionSet::from_file(fileNamePH);
  photonSF_ = csetPH->at("UL-Photon-ID-SF");

  std::string fileNameELE = dirName+"EGM/"+subDirName+"electron.json.gz";
  auto csetELE = correction::CorrectionSet::from_file(fileNameELE);
  electronSF_ = csetELE->at("UL-Electron-ID-SF");

  std::string fileNameTAU = dirName+"TAU/"+subDirName+"tau.json.gz";
  auto csetTAU = correction::CorrectionSet::from_file(fileNameTAU);
  tauJETSF_ = csetTAU->at("DeepTau2017v2p1VSjet");
  tauELESF_ = csetTAU->at("DeepTau2017v2p1VSe");
  tauMUOSF_ = csetTAU->at("DeepTau2017v2p1VSmu");

  std::string fileNameJEC = dirName+"JME/"+subDirName+"jet_jerc.json.gz";
  auto csetJEC = correction::CorrectionSet::from_file(fileNameJEC);

  std::string jecName = ""; std::string jerName = "";
  if(year == 2018)  {jecName = "Summer19UL18_V5_MC";    jerName = "Summer19UL18_JRV2_MC";}
  if(year == 2017)  {jecName = "Summer19UL17_V5_MC";    jerName = "Summer19UL17_JRV2_MC";}
  if(year == 22016) {jecName = "Summer19UL16_V5_MC";    jerName = "Summer20UL16_JRV3";}
  if(year == 12016) {jecName = "Summer19UL16APV_V5_MC"; jerName = "Summer20UL16APV_JRV3";}

  std::string algoName = "AK4PFchs";

  std::string tagName = jecName + "_" + "L1L2L3Res" + "_" + algoName;
  JEC_ = csetJEC->compound().at(tagName);

  tagName = jecName + "_" + "Total" + "_" + algoName;
  jesUnc_ = csetJEC->at(tagName);

  tagName = jerName + "_" + "ScaleFactor" + "_" + algoName;
  jerMethod1Unc_ = csetJEC->at(tagName);

  tagName = jerName + "_" + "PtResolution" + "_" + algoName;
  jerMethod2Unc_ = csetJEC->at(tagName);

  std::string fileNamePUJetID = dirName+"JME/"+subDirName+"jmar.json.gz";
  auto csetPUJetID = correction::CorrectionSet::from_file(fileNamePUJetID);
  puJetIDSF_ = csetPUJetID->at("PUJetID_eff");

};

double MyCorrections::eval_puSF(double int1, std::string str1) {
  return puSF_->evaluate({int1, str1});
};

double MyCorrections::eval_muonTRKSF(const char *year, const char *valType, const char *workingPoint, double eta, double pt) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  return muonTRKSF_->evaluate({year, eta, pt, valType});
};

double MyCorrections::eval_muonIDSF(const char *year, const char *valType, const char *workingPoint, double eta, double pt) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  return muonIDSF_->evaluate({year, eta, pt, valType});
};

double MyCorrections::eval_muonISOSF(const char *year, const char *valType, const char *workingPoint, double eta, double pt) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  return muonISOSF_->evaluate({year, eta, pt, valType});
};

double MyCorrections::eval_electronSF(const char *year, const char *valType, const char *workingPoint, double eta, double pt) {
  pt = std::max(pt,10.001);
  return electronSF_->evaluate({year, valType, workingPoint, eta, pt});
};

double MyCorrections::eval_photonSF(const char *year, const char *valType, const char *workingPoint, double eta, double pt) {
  pt = std::max(pt,20.001);
  return photonSF_->evaluate({year, valType, workingPoint, eta, pt});
};

double MyCorrections::eval_tauJETSF(double pt, int dm, int genmatch, const char *workingPoint, const char *valType) {
  pt = std::min(std::max(pt,20.001),1999.999);
  return tauJETSF_->evaluate({pt, dm, genmatch, workingPoint, valType, "pt"});
};

double MyCorrections::eval_tauELESF(double eta, int genmatch, const char *workingPoint, const char *valType) {
  eta = std::min(std::abs(eta),2.299);
  return tauELESF_->evaluate({eta, genmatch, workingPoint, valType});
};

double MyCorrections::eval_tauMUOSF(double eta, int genmatch, const char *workingPoint, const char *valType) {
  eta = std::min(std::abs(eta),2.299);
  return tauMUOSF_->evaluate({eta, genmatch, workingPoint, valType});
};

double MyCorrections::eval_btvSF(char *valType, char *workingPoint, double eta, double pt, int flavor) {
  if(flavor != 0)
    return btvHFSF_->evaluate({valType, workingPoint, flavor, eta, pt});
  else
    return btvLFSF_->evaluate({valType, workingPoint, flavor, eta, pt});
};

double MyCorrections::eval_jetCORR(double area, double eta, double pt, double rho) {
  return JEC_->evaluate({area, eta, pt, rho});
};

double MyCorrections::eval_jesUnc(double eta, double pt, int type) {
  if(type == 0) return jesUnc_->evaluate({eta, pt});
  return 0.0;
};

double MyCorrections::eval_jerMethod1(double eta, int type) {
  if     (type ==  0) return jerMethod1Unc_->evaluate({eta,"nom"});
  else if(type == +1) return jerMethod1Unc_->evaluate({eta,"up"});
  else if(type == -1) return jerMethod1Unc_->evaluate({eta,"down"});
  return 0.0;
};

double MyCorrections::eval_jerMethod2(double eta, double pt, double rho) {
  return jerMethod2Unc_->evaluate({eta,pt,rho});
};

double MyCorrections::eval_puJetIDSF(char *valType, char *workingPoint, double eta, double pt) {
  return puJetIDSF_->evaluate({eta, pt, valType, workingPoint});
};

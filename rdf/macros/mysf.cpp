#include "mysf.h"

MyCorrections::MyCorrections(int the_input_year) {

  if(the_input_year == 20221) the_input_year = 2022;

  year = the_input_year;
  yearPrime = the_input_year;

  if(year == 2022) year = 2018;

  if(year == 2023) yearPrime = 2022;
  if(year == 2023) year = 2018;

  std::string dirName = "/cvmfs/cms.cern.ch/rsync/cms-nanoAOD/jsonpog-integration/POG/";

  std::string subDirName = "";
  if     (year == 12016) subDirName += "2016preVFP_UL/";  
  else if(year == 22016) subDirName += "2016postVFP_UL/";
  else if(year == 2017)  subDirName += "2017_UL/";
  else if(year == 2018)  subDirName += "2018_UL/";
  else if(year == 2022)  subDirName += "2022_Summer22EE/";

  std::string subDirNamePrime0 = ""; std::string subDirNamePrime1 = "";
  if     (yearPrime == 12016) {subDirNamePrime0 += "2016preVFP_UL/";   subDirNamePrime1 += "2016preVFP_UL/";}  
  else if(yearPrime == 22016) {subDirNamePrime0 += "2016postVFP_UL/";  subDirNamePrime1 += "2016postVFP_UL/";}
  else if(yearPrime == 2017)  {subDirNamePrime0 += "2017_UL/";	       subDirNamePrime1 += "2017_UL/";}
  else if(yearPrime == 2018)  {subDirNamePrime0 += "2018_UL/";	       subDirNamePrime1 += "2018_UL/";}
  else if(yearPrime == 2022)  {subDirNamePrime0 += "2022_Summer22EE/"; subDirNamePrime1 += "2022_Prompt/";}

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

  std::string fileNameJEC = dirName+"JME/"+subDirNamePrime0+"jet_jerc.json.gz";
  //std::cout << fileNameJEC << std::endl;
  auto csetJEC = correction::CorrectionSet::from_file(fileNameJEC);

  std::string algoName = "AK4PFchs";

  std::string jecMCName = ""; std::string jerName = "";
  std::string jecDATAName[10]    = {"NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL"};
  std::string jetVetoMapName[10] = {"NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL"};
  if(yearPrime == 2022)  {
    jecMCName = "Summer22EEPrompt22_V1_MC"; jerName = "Summer22EEPrompt22_JRV1_MC";
    jecDATAName[0] = "Summer22EEPrompt22_RunF_V1_DATA"; jetVetoMapName[0] = "Winter22Run3_RunCD_V1"; // A
    jecDATAName[1] = "Summer22EEPrompt22_RunF_V1_DATA"; jetVetoMapName[1] = "Winter22Run3_RunCD_V1"; // B
    jecDATAName[2] = "Summer22EEPrompt22_RunF_V1_DATA"; jetVetoMapName[2] = "Winter22Run3_RunCD_V1"; // C
    jecDATAName[3] = "Summer22EEPrompt22_RunF_V1_DATA"; jetVetoMapName[3] = "Winter22Run3_RunCD_V1"; // D
    jecDATAName[4] = "Summer22EEPrompt22_RunF_V1_DATA"; jetVetoMapName[4] = "Winter22Run3_RunE_V1"; // E
    jecDATAName[5] = "Summer22EEPrompt22_RunF_V1_DATA"; jetVetoMapName[5] = "Winter22Run3_RunE_V1"; // F
    jecDATAName[6] = "Summer22EEPrompt22_RunG_V1_DATA"; jetVetoMapName[6] = "Winter22Run3_RunE_V1"; // G
    algoName = "AK4PFPuppi";
  }
  else if(yearPrime == 2018)  {
    jecMCName = "Summer19UL18_V5_MC"; jerName = "Summer19UL18_JRV2_MC";
    jecDATAName[0] = "Summer19UL18_RunA_V5_DATA"; jetVetoMapName[0] = "Summer19UL18_V1"; // A
    jecDATAName[1] = "Summer19UL18_RunB_V5_DATA"; jetVetoMapName[1] = "Summer19UL18_V1"; // B
    jecDATAName[2] = "Summer19UL18_RunC_V5_DATA"; jetVetoMapName[2] = "Summer19UL18_V1"; // C
    jecDATAName[3] = "Summer19UL18_RunD_V5_DATA"; jetVetoMapName[3] = "Summer19UL18_V1"; // D
  }
  else if(yearPrime == 2017)  {jecMCName = "Summer19UL17_V5_MC";    jerName = "Summer19UL17_JRV2_MC";}
  else if(yearPrime == 22016) {jecMCName = "Summer19UL16_V5_MC";    jerName = "Summer20UL16_JRV3";}
  else if(yearPrime == 12016) {jecMCName = "Summer19UL16APV_V5_MC"; jerName = "Summer20UL16APV_JRV3";}

  std::string tagName = jecMCName + "_" + "L1L2L3Res" + "_" + algoName;
  JECMC_ = csetJEC->compound().at(tagName);

  tagName = jecMCName + "_" + "Total" + "_" + algoName;
  jesUnc_ = csetJEC->at(tagName);

  for(int i=0; i<10; i++){
    if(jecDATAName[i].compare("NULL") == 0) continue;
    tagName = jecDATAName[i] + "_" + "L1L2L3Res" + "_" + algoName;
    JECDATA_[i] = csetJEC->compound().at(tagName);
    tagName = jecDATAName[i] + "_" + "L2Relative" + "_" + algoName;
    JECL2ResDATA_[i] = csetJEC->at(tagName);
  }

  tagName = jerName + "_" + "ScaleFactor" + "_" + algoName;
  //std::cout << tagName << std::endl;
  jerMethod1Unc_ = csetJEC->at(tagName);

  tagName = jerName + "_" + "PtResolution" + "_" + algoName;
  jerMethod2Unc_ = csetJEC->at(tagName);

  std::string fileNamePUJetID = dirName+"JME/"+subDirName+"jmar.json.gz";
  auto csetPUJetID = correction::CorrectionSet::from_file(fileNamePUJetID);
  puJetIDSF_ = csetPUJetID->at("PUJetID_eff");

  std::string fileNamejetVetoMap = dirName+"JME/"+subDirNamePrime1+"jetvetomaps.json.gz";
  auto csetJetVetoMap = correction::CorrectionSet::from_file(fileNamejetVetoMap);

  for(int i=0; i<10; i++){
    if(jetVetoMapName[i].compare("NULL") == 0) continue;
    jetVetoMap_[i] = csetJetVetoMap->at(jetVetoMapName[i]);
  }

};

double MyCorrections::eval_puSF(double int1, std::string str1) {
  return puSF_->evaluate({int1, str1});
};

double MyCorrections::eval_muonTRKSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  return muonTRKSF_->evaluate({the_input_year, eta, pt, valType});
};

double MyCorrections::eval_muonIDSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  return muonIDSF_->evaluate({the_input_year, eta, pt, valType});
};

double MyCorrections::eval_muonISOSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  return muonISOSF_->evaluate({the_input_year, eta, pt, valType});
};

double MyCorrections::eval_electronSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt) {
  pt = std::max(pt,10.001);
  return electronSF_->evaluate({the_input_year, valType, workingPoint, eta, pt});
};

double MyCorrections::eval_photonSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt) {
  pt = std::max(pt,20.001);
  return photonSF_->evaluate({the_input_year, valType, workingPoint, eta, pt});
};

double MyCorrections::eval_tauJETSF(double pt, int dm, int genmatch, const char *workingPoint, const char *valType) {
  pt = std::min(std::max(pt,20.001),1999.999);
  return tauJETSF_->evaluate({pt, dm, genmatch, workingPoint, "VVLoose", valType, "pt"});
};

double MyCorrections::eval_tauELESF(double eta, int genmatch, const char *workingPoint, const char *valType) {
  eta = std::min(std::abs(eta),2.299);
  return tauELESF_->evaluate({eta, genmatch, workingPoint, valType});
};

double MyCorrections::eval_tauMUOSF(double eta, int genmatch, const char *workingPoint, const char *valType) {
  eta = std::min(std::abs(eta),2.299);
  return tauMUOSF_->evaluate({eta, genmatch, workingPoint, valType});
};

double MyCorrections::eval_btvSF(const char *valType, char *workingPoint, double eta, double pt, int flavor) {
  if(flavor != 0)
    return btvHFSF_->evaluate({valType, workingPoint, flavor, eta, pt});
  else
    return btvLFSF_->evaluate({valType, workingPoint, flavor, eta, pt});
};

double MyCorrections::eval_jetCORR(double area, double eta, double pt, double rho, int type) {
  if(type >= 4 && yearPrime == 2022) return JECL2ResDATA_[type]->evaluate({eta, pt});
  if(type >= 0) return JECDATA_[type]->evaluate({area, eta, pt, rho});
  return JECMC_->evaluate({area, eta, pt, rho});
};

double MyCorrections::eval_jesUnc(double eta, double pt, int type) {
  if(type == 0) return jesUnc_->evaluate({eta, pt});
  return 0.0;
};

double MyCorrections::eval_jerMethod1(double eta, double pt, int type) {
  if(yearPrime < 2020){
    if     (type ==  0) return jerMethod1Unc_->evaluate({eta,"nom"});
    else if(type == +1) return jerMethod1Unc_->evaluate({eta,"up"});
    else if(type == -1) return jerMethod1Unc_->evaluate({eta,"down"});
  } else {
    if     (type ==  0) return jerMethod1Unc_->evaluate({eta,"nom"});
    else if(type == +1) return jerMethod1Unc_->evaluate({eta,"up"});
    else if(type == -1) return jerMethod1Unc_->evaluate({eta,"down"});
  }
  return 0.0;
};

double MyCorrections::eval_jerMethod2(double eta, double pt, double rho) {
  return jerMethod2Unc_->evaluate({eta,pt,rho});
};

double MyCorrections::eval_puJetIDSF(char *valType, char *workingPoint, double eta, double pt) {
  return puJetIDSF_->evaluate({eta, pt, valType, workingPoint});
};

double MyCorrections::eval_jetVetoMap(double eta, double phi, int type) {
  eta = std::min(std::max(eta,-5.18),5.18);
  phi = std::min(std::max(phi,-3.1415),3.1415);
  if(type >= 0) return jetVetoMap_[type]->evaluate({"jetvetomap", eta, phi});
  return 0;
};

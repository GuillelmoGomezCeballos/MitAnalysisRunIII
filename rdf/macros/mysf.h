#include "correction.h"
#include <stdio.h>
#include <string.h>
#include <iostream>

//g++ $(correction config --cflags --ldflags) mysf.cpp -shared -fPIC -o mysf.so

class MyCorrections {
  public:
    MyCorrections(int the_input_year);

    double eval_puSF      (double NumTrueInteractions, std::string weights);

    double eval_muonTRKSF (double eta, double pt, double p, const char *valType);
    double eval_muonIDSF  (double eta, double pt, const char *valType);
    double eval_muonISOSF (double eta, double pt, const char *valType);

    double eval_electronSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_electronScale(const char *valType, const int gain, const double run, const double eta, const double r9, const double et);
    double eval_electronSmearing(const char *valType, const double eta, const double r9);
    double eval_photonSF  (const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt);

    double eval_tauJETSF  (double pt, int dm, int genmatch, const char *workingPoint, const char *workingPoint_VSe, const char *valType);

    double eval_btvSF     (const char *valType, char *workingPoint, double eta, double pt, int flavor);

    double eval_jetCORR   (double area, double eta, double phi, double pt, double rho, int type);
    double eval_jesUnc    (double eta, double pt, int type);
    double eval_jerMethod1(double eta, double pt, int type);
    double eval_jerMethod2(double eta, double pt, double rho);
    double eval_puJetIDSF (char *valType, char *workingPoint, double eta, double pt);
    double eval_jetVetoMap(double eta, double phi, int type);

  private:
    correction::Correction::Ref puSF_;
    correction::Correction::Ref muonTRKSF_;
    correction::Correction::Ref muonIDSF_;
    correction::Correction::Ref muonISOSF_;
    correction::Correction::Ref muonHighPtTRKSF_;
    correction::Correction::Ref muonHighPtIDSF_;
    correction::Correction::Ref muonHighPtISOSF_;
    correction::Correction::Ref electronSF_;
    correction::Correction::Ref electronScale_;
    correction::Correction::Ref electronSmearing_;
    correction::Correction::Ref photonSF_;
    correction::Correction::Ref tauJETSF_;
    correction::Correction::Ref btvHFSF_;
    correction::Correction::Ref btvLFSF_;
    correction::CompoundCorrection::Ref JECMC_;
    correction::CompoundCorrection::Ref JECDATA_[10];
    correction::Correction::Ref JECL2ResDATA_[10];
    correction::Correction::Ref jetVetoMap_[10];
    correction::Correction::Ref jesSourcesUnc_[28];
    correction::Correction::Ref jerMethod1Unc_;
    correction::Correction::Ref jerMethod2Unc_;
    correction::Correction::Ref puJetIDSF_;
    int year;
    bool isJan24JME = false;
};

MyCorrections::MyCorrections(int the_input_year) {

  year = the_input_year;

  std::string dirName    = "jsonpog-integration/POG/";

  std::string subDirName = "";
  if     (year == 20220) subDirName = "2022_Summer22/";  
  else if(year == 20221) subDirName = "2022_Summer22EE/";
  else if(year == 20230) subDirName = "2023_Summer23/";
  else if(year == 20231) subDirName = "2023_Summer23BPix/";
  else return;

  std::cout << "subDirName/year: " << subDirName << " " << year << std::endl;

  //std::string subDirNamePrime0 = ""; std::string subDirNamePrime1 = "";
  //if     (yearPrime == 12016) {subDirNamePrime0 = "2016preVFP_UL/";   subDirNamePrime1 = "2016preVFP_UL/";}  
  //else if(yearPrime == 22016) {subDirNamePrime0 = "2016postVFP_UL/";  subDirNamePrime1 = "2016postVFP_UL/";}
  //else if(yearPrime == 2017)  {subDirNamePrime0 = "2017_UL/";         subDirNamePrime1 = "2017_UL/";}
  //else if(yearPrime == 2018)  {subDirNamePrime0 = "2018_UL/";         subDirNamePrime1 = "2018_UL/";}
  //else if(yearPrime == 2022)  {subDirNamePrime0 = "2022_Summer22EE/"; subDirNamePrime1 = "2022_Prompt/";}

  std::string fileNameLUM = dirName+"LUM/"+subDirName+"puWeights.json.gz";

  std::string corrNameLUM = "";  
  if     (year == 20220) corrNameLUM = "Collisions2022_355100_357900_eraBCD_GoldenJson";
  else if(year == 20221) corrNameLUM = "Collisions2022_359022_362760_eraEFG_GoldenJson";
  else if(year == 20230) corrNameLUM = "Collisions2023_366403_369802_eraBC_GoldenJson";
  else if(year == 20231) corrNameLUM = "Collisions2023_369803_370790_eraD_GoldenJson";
  
  auto csetPU = correction::CorrectionSet::from_file(fileNameLUM);
  puSF_ = csetPU->at(corrNameLUM);
  
  std::string fileNameHFBTV = dirName+"BTV/"+subDirName+"btagging_v1_mar24.json.gz";
  auto csetHFBTV = correction::CorrectionSet::from_file(fileNameHFBTV);
  btvHFSF_ = csetHFBTV->at("robustParticleTransformer_comb");

  std::string fileNameLFBTV = dirName+"BTV/"+subDirName+"btagging_v1_mar24.json.gz";
  auto csetLFBTV = correction::CorrectionSet::from_file(fileNameLFBTV);
  btvLFSF_ = csetLFBTV->at("robustParticleTransformer_light");

  std::string fileNameMu = dirName+"MUO/"+subDirName+"muon_Z.json.gz";
  auto csetMu = correction::CorrectionSet::from_file(fileNameMu);
  //muonTRKSF_ = csetMu->at("NUM_TrackerMuons_DEN_genTracks");
  muonIDSF_ = csetMu->at("NUM_MediumID_DEN_TrackerMuons");
  muonISOSF_ = csetMu->at("NUM_TightPFIso_DEN_MediumID");

  std::string fileNameHighPtRECOMu = dirName+"MUO/"+subDirName+"ScaleFactors_Muon_highPt_RECO_schemaV2.json.gz";
  auto csetHighPtRECOMu = correction::CorrectionSet::from_file(fileNameHighPtRECOMu);
  muonHighPtTRKSF_ = csetHighPtRECOMu->at("NUM_GlobalMuons_DEN_TrackerMuonProbes");

  std::string fileNameHighPtIDISOMu = dirName+"MUO/"+subDirName+"ScaleFactors_Muon_highPt_IDISO_schemaV2.json.gz";
  auto csetHighPtIDISOMu = correction::CorrectionSet::from_file(fileNameHighPtIDISOMu);
  muonHighPtIDSF_ = csetHighPtIDISOMu->at("NUM_MediumID_DEN_GlobalMuonProbes");
  muonHighPtISOSF_ = csetHighPtIDISOMu->at("NUM_probe_TightRelTkIso_DEN_MediumIDProbes");
  
  std::string fileNamePH = dirName+"EGM/"+subDirName+"photon.json.gz";
  auto csetPH = correction::CorrectionSet::from_file(fileNamePH);
  if     (year == 20220) photonSF_ = csetPH->at("Photon-ID-SF");
  else if(year == 20221) photonSF_ = csetPH->at("Photon-ID-SF");
  else if(year == 20230) photonSF_ = csetPH->at("Photon-ID-SF");
  else if(year == 20231) photonSF_ = csetPH->at("Photon-ID-SF");

  std::string fileNameELE = dirName+"EGM/"+subDirName+"electron.json.gz";
  auto csetELE = correction::CorrectionSet::from_file(fileNameELE);
  if     (year == 20220) electronSF_ = csetELE->at("Electron-ID-SF");
  else if(year == 20221) electronSF_ = csetELE->at("Electron-ID-SF");
  else if(year == 20230) electronSF_ = csetELE->at("Electron-ID-SF");
  else if(year == 20231) electronSF_ = csetELE->at("Electron-ID-SF");

  std::string fileNameEnergyELE = dirName+"EGM/"+subDirName+"electronSS.json.gz";
  auto csetEnergyELE = correction::CorrectionSet::from_file(fileNameEnergyELE);
  if     (year == 20220) {electronScale_ = csetEnergyELE->at("2022Re-recoBCD_ScaleJSON");        electronSmearing_ = csetEnergyELE->at("2022Re-recoBCD_SmearingJSON");}
  else if(year == 20221) {electronScale_ = csetEnergyELE->at("2022Re-recoE+PromptFG_ScaleJSON"); electronSmearing_ = csetEnergyELE->at("2022Re-recoE+PromptFG_SmearingJSON");}
  else if(year == 20230) {electronScale_ = csetEnergyELE->at("2022Re-recoBCD_ScaleJSON");        electronSmearing_ = csetEnergyELE->at("2022Re-recoBCD_SmearingJSON");}
  else if(year == 20231) {electronScale_ = csetEnergyELE->at("2022Re-recoBCD_ScaleJSON");        electronSmearing_ = csetEnergyELE->at("2022Re-recoBCD_SmearingJSON");}

  std::string fileNameTAU = dirName+"TAU/"+subDirName+"tau_DeepTau2018v2p5.json.gz";
  auto csetTAU = correction::CorrectionSet::from_file(fileNameTAU);
  tauJETSF_ = csetTAU->at("DeepTau2018v2p5VSjet");

  std::string fileNameJER = dirName+"JME/"+subDirName+"jet_jerc.json.gz";
  if(isJan24JME == true) fileNameJER = dirName+"JME/"+subDirName+"jerc_only_jan24.json.gz";
  //std::cout << fileNameJER << std::endl;
  auto csetJER = correction::CorrectionSet::from_file(fileNameJER);

  std::string fileNameJEC = dirName+"JME/"+subDirName+"jet_jerc.json.gz";
  if(isJan24JME == true) fileNameJEC = dirName+"JME/"+subDirName+"jet_jerc_jan24.json.gz";
  //std::cout << fileNameJEC << std::endl;
  auto csetJEC = correction::CorrectionSet::from_file(fileNameJEC);

  std::string algoName = "AK4PFPuppi";

  std::string jecMCName = ""; std::string jerName = "";
  std::string jecDATAName[10]    = {"NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL"};
  std::string jetVetoMapName[10] = {"NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL","NULL"};

  if      (year == 20220)  {
    jecMCName = "Summer22_22Sep2023_V2_MC"; jerName = "Summer22_22Sep2023_JRV1_MC";
    if(isJan24JME == true) jerName = "JR_Winter22Run3_V1_MC";
    jecDATAName[0] = "Summer22_22Sep2023_RunCD_V2_DATA";   jetVetoMapName[0] = "Summer22_23Sep2023_RunCD_V1"; // A
    jecDATAName[1] = "Summer22_22Sep2023_RunCD_V2_DATA";   jetVetoMapName[1] = "Summer22_23Sep2023_RunCD_V1"; // B
    jecDATAName[2] = "Summer22_22Sep2023_RunCD_V2_DATA";   jetVetoMapName[2] = "Summer22_23Sep2023_RunCD_V1"; // C
    jecDATAName[3] = "Summer22_22Sep2023_RunCD_V2_DATA";   jetVetoMapName[3] = "Summer22_23Sep2023_RunCD_V1"; // D
    jecDATAName[4] = "NULL"; jetVetoMapName[4] = "NULL";  // E
    jecDATAName[5] = "NULL"; jetVetoMapName[5] = "NULL";  // F
    jecDATAName[6] = "NULL"; jetVetoMapName[6] = "NULL";  // G
  }
  else if(year == 20221)  {
    jecMCName = "Summer22EE_22Sep2023_V2_MC"; jerName = "Summer22EE_22Sep2023_JRV1_MC";
    if(isJan24JME == true) jerName = "Summer22EEPrompt22_JRV1_MC";
    jecDATAName[0] = "NULL";   jetVetoMapName[0] = "NULL"; // A
    jecDATAName[1] = "NULL";   jetVetoMapName[1] = "NULL"; // B
    jecDATAName[2] = "NULL";   jetVetoMapName[2] = "NULL"; // C
    jecDATAName[3] = "NULL";   jetVetoMapName[3] = "NULL"; // D
    jecDATAName[4] = "Summer22EE_22Sep2023_RunE_V2_DATA"; jetVetoMapName[4] = "Summer22EE_23Sep2023_RunEFG_V1";  // E
    jecDATAName[5] = "Summer22EE_22Sep2023_RunF_V2_DATA"; jetVetoMapName[5] = "Summer22EE_23Sep2023_RunEFG_V1";  // F
    jecDATAName[6] = "Summer22EE_22Sep2023_RunG_V2_DATA"; jetVetoMapName[6] = "Summer22EE_23Sep2023_RunEFG_V1";  // G
  }
  else if(year == 20230)  {
    jecMCName = "Summer23Prompt23_V1_MC"; jerName = "Summer23Prompt23_RunCv4_JRV1_MC";
    jecDATAName[0] = "NULL";   jetVetoMapName[0] = "NULL"; // A
    jecDATAName[1] = "NULL";   jetVetoMapName[1] = "NULL"; // B
    jecDATAName[2] = "Summer23Prompt23_RunCv123_V1_DATA";   jetVetoMapName[2] = "Summer23Prompt23_RunC_V1"; // C
    jecDATAName[3] = "NULL";   jetVetoMapName[3] = "NULL"; // D
    jecDATAName[4] = "NULL";   jetVetoMapName[4] = "NULL"; // E
    jecDATAName[5] = "NULL";   jetVetoMapName[5] = "NULL"; // F
    jecDATAName[6] = "NULL";   jetVetoMapName[6] = "NULL"; // G
  }
  else if(year == 20231)  {
    jecMCName = "Summer23BPixPrompt23_V1_MC"; jerName = "Summer23BPixPrompt23_RunD_JRV1_MC";
    jecDATAName[0] = "NULL";   jetVetoMapName[0] = "NULL"; // A
    jecDATAName[1] = "NULL";   jetVetoMapName[1] = "NULL"; // B
    jecDATAName[2] = "NULL";   jetVetoMapName[2] = "NULL"; // C
    jecDATAName[3] = "Summer23BPixPrompt23_RunD_V1_DATA";   jetVetoMapName[3] = "Summer23BPixPrompt23_RunD_V1"; // D
    jecDATAName[4] = "NULL";   jetVetoMapName[4] = "NULL"; // E
    jecDATAName[5] = "NULL";   jetVetoMapName[5] = "NULL"; // F
    jecDATAName[6] = "NULL";   jetVetoMapName[6] = "NULL"; // G
  }

  std::string tagName = jecMCName + "_" + "L1L2L3Res" + "_" + algoName;
  JECMC_ = csetJEC->compound().at(tagName);

  tagName = jecMCName + "_" + "Total" + "_" + algoName;
  jesSourcesUnc_[0] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "AbsoluteMPFBias" + "_" + algoName;
  jesSourcesUnc_[ 1] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "AbsoluteScale" + "_" + algoName;
  jesSourcesUnc_[ 2] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "AbsoluteStat" + "_" + algoName;
  jesSourcesUnc_[ 3] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "FlavorQCD" + "_" + algoName;
  jesSourcesUnc_[ 4] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "Fragmentation" + "_" + algoName;
  jesSourcesUnc_[ 5] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "PileUpDataMC" + "_" + algoName;
  jesSourcesUnc_[ 6] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "PileUpPtBB" + "_" + algoName;
  jesSourcesUnc_[ 7] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "PileUpPtEC1" + "_" + algoName;
  jesSourcesUnc_[ 8] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "PileUpPtEC2" + "_" + algoName;
  jesSourcesUnc_[ 9] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "PileUpPtHF" + "_" + algoName;
  jesSourcesUnc_[10] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "PileUpPtRef" + "_" + algoName;
  jesSourcesUnc_[11] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeFSR" + "_" + algoName;
  jesSourcesUnc_[12] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeJEREC1" + "_" + algoName;
  jesSourcesUnc_[13] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeJEREC2" + "_" + algoName;
  jesSourcesUnc_[14] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeJERHF" + "_" + algoName;
  jesSourcesUnc_[15] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativePtBB" + "_" + algoName;
  jesSourcesUnc_[16] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativePtEC1" + "_" + algoName;
  jesSourcesUnc_[17] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativePtEC2" + "_" + algoName;
  jesSourcesUnc_[18] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativePtHF" + "_" + algoName;
  jesSourcesUnc_[19] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeBal" + "_" + algoName;
  jesSourcesUnc_[20] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeSample" + "_" + algoName;
  jesSourcesUnc_[21] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeStatEC" + "_" + algoName;
  jesSourcesUnc_[22] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeStatFSR" + "_" + algoName;
  jesSourcesUnc_[23] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "RelativeStatHF" + "_" + algoName;
  jesSourcesUnc_[24] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "SinglePionECAL" + "_" + algoName;
  jesSourcesUnc_[25] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "SinglePionHCAL" + "_" + algoName;
  jesSourcesUnc_[26] = csetJEC->at(tagName);

  tagName = jecMCName + "_" + "TimePtEta" + "_" + algoName;
  jesSourcesUnc_[27] = csetJEC->at(tagName);

  for(int i=0; i<10; i++){
    if(jecDATAName[i].compare("NULL") == 0) continue;
    tagName = jecDATAName[i] + "_" + "L1L2L3Res" + "_" + algoName;
    JECDATA_[i] = csetJEC->compound().at(tagName);
    tagName = jecDATAName[i] + "_" + "L2Relative" + "_" + algoName;
    JECL2ResDATA_[i] = csetJEC->at(tagName);
  }

  tagName = jerName + "_" + "ScaleFactor" + "_" + algoName;
  //std::cout << tagName << std::endl;
  jerMethod1Unc_ = csetJER->at(tagName);

  tagName = jerName + "_" + "PtResolution" + "_" + algoName;
  jerMethod2Unc_ = csetJER->at(tagName);

  //std::string fileNamePUJetID = dirName+"JME/"+subDirName+"jmar.json.gz";
  //auto csetPUJetID = correction::CorrectionSet::from_file(fileNamePUJetID);
  //puJetIDSF_ = csetPUJetID->at("PUJetID_eff");

  //std::cout << fileNameJEC << std::endl;
  std::string fileNamejetVetoMap = dirName+"JME/"+subDirName+"jetvetomaps.json.gz";
  auto csetJetVetoMap = correction::CorrectionSet::from_file(fileNamejetVetoMap);

  for(int i=0; i<10; i++){
    if(jetVetoMapName[i].compare("NULL") == 0) continue;
    jetVetoMap_[i] = csetJetVetoMap->at(jetVetoMapName[i]);
  }

};

double MyCorrections::eval_puSF(double int1, std::string str1) {
  return puSF_->evaluate({int1, str1});
};

double MyCorrections::eval_muonTRKSF(double eta, double pt, double p, const char *valType) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  if(pt > 200)                            return muonHighPtTRKSF_->evaluate({eta, p, valType});
  else if(strcmp(valType,"nominal") == 0) return 1.0;
  else                                    return 0.0;
  return 1.0;
};

double MyCorrections::eval_muonIDSF(double eta, double pt, const char *valType) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  if(pt > 200) return muonHighPtIDSF_->evaluate({eta, pt, valType});
  else         return muonIDSF_->evaluate({eta, pt, valType});
  return 1.0;
};

double MyCorrections::eval_muonISOSF(double eta, double pt, const char *valType) {
  eta = std::min(std::abs(eta),2.399);
  pt = std::max(pt,15.001);
  if(pt > 200) return muonHighPtISOSF_->evaluate({eta, pt, valType});
  else         return muonISOSF_->evaluate({eta, pt, valType});
  return 1.0;
};

double MyCorrections::eval_electronSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt) {
  pt = std::max(pt,10.001);
  return electronSF_->evaluate({the_input_year, valType, workingPoint, eta, pt});
};

double MyCorrections::eval_electronScale(const char *valType, const int gain, const double run, const double eta, const double r9, const double et) {
  return electronScale_->evaluate({valType, gain, run, eta, r9, et});
};

double MyCorrections::eval_electronSmearing(const char *valType, const double eta, const double r9) {
  return electronSmearing_->evaluate({valType, eta, r9});
};

double MyCorrections::eval_photonSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt) {
  pt = std::max(pt,20.001);
  return photonSF_->evaluate({the_input_year, valType, workingPoint, eta, pt});
};

double MyCorrections::eval_tauJETSF(double pt, int dm, int genmatch, const char *workingPoint, const char *workingPoint_VSe, const char *valType) {
  pt = std::min(std::max(pt,20.001),1999.999);
  return tauJETSF_->evaluate({pt, dm, genmatch, workingPoint, workingPoint_VSe, valType, "dm"});
};

double MyCorrections::eval_btvSF(const char *valType, char *workingPoint, double eta, double pt, int flavor) {
  if(eta <= -2.5 || eta >= 2.5) return 0.0;
  eta = std::min(std::abs(eta),2.399);
  pt = std::min(pt,999.999);
  if(flavor != 0)
    return btvHFSF_->evaluate({valType, workingPoint, flavor, eta, pt});
  else
    return btvLFSF_->evaluate({valType, workingPoint, flavor, eta, pt});
};

double MyCorrections::eval_jetCORR(double area, double eta, double phi, double pt, double rho, int type) {
  // data
  if     (type >= 0 && year == 20231) return JECDATA_[type]->evaluate({area, eta, phi, pt, rho});
  else if(type >= 0 && year != 20231) return JECDATA_[type]->evaluate({area, eta,      pt, rho});
  // MC
  if     (year == 20231) return JECMC_->evaluate({area, eta, phi, pt, rho});
  else if(year != 20231) return JECMC_->evaluate({area, eta,      pt, rho});
  printf("ERROR in eval_jetCORR!\n");
  return 1.0;
};

double MyCorrections::eval_jesUnc(double eta, double pt, int type) {
  return std::abs(jesSourcesUnc_[type]->evaluate({eta, pt}));
};

double MyCorrections::eval_jerMethod1(double eta, double pt, int type) {
  if(isJan24JME == true) {
    if     (year == 20220){
      if     (type ==  0) return jerMethod1Unc_->evaluate({eta,pt,"nom"});
      else if(type == +1) return jerMethod1Unc_->evaluate({eta,pt,"up"});
      else if(type == -1) return jerMethod1Unc_->evaluate({eta,pt,"down"});
    }
    else if(year == 20221){
      if     (type ==  0) return jerMethod1Unc_->evaluate({eta,"nom"});
      else if(type == +1) return jerMethod1Unc_->evaluate({eta,"up"});
      else if(type == -1) return jerMethod1Unc_->evaluate({eta,"down"});
    }
  }
  if     (type ==  0) return jerMethod1Unc_->evaluate({eta,pt,"nom"});
  else if(type == +1) return jerMethod1Unc_->evaluate({eta,pt,"up"});
  else if(type == -1) return jerMethod1Unc_->evaluate({eta,pt,"down"});
  std::cout << "0 JER correction!" << std::endl;
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

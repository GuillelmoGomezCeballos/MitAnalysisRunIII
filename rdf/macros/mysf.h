#include "correction.h"
#include <stdio.h>
#include <string.h>
#include <iostream>

//g++ $(correction config --cflags --ldflags) mysf.cpp -shared -fPIC -o mysf.so

class MyCorrections {
  public:
    MyCorrections(int year);
    double eval_puSF      (double NumTrueInteractions, std::string weights);
    double eval_muonTRKSF (const char *year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_muonIDSF  (const char *year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_muonISOSF (const char *year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_electronSF(const char *year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_photonSF  (const char *year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_tauJETSF  (double pt, int dm, int genmatch, const char *workingPoint, const char *valType);
    double eval_tauELESF  (double eta, int genmatch, const char *workingPoint, const char *valType);
    double eval_tauMUOSF  (double eta, int genmatch, const char *workingPoint, const char *valType);
    double eval_btvSF     (char *valType, char *workingPoint, double eta, double pt, int flavor);
    double eval_jetCORR   (double area, double eta, double pt, double rho);
    double eval_jesUnc    (double eta, double pt, int type);
    double eval_puJetIDSF (char *valType, char *workingPoint, double eta, double pt);
  private:
    correction::Correction::Ref puSF_;
    correction::Correction::Ref muonTRKSF_;
    correction::Correction::Ref muonIDSF_;
    correction::Correction::Ref muonISOSF_;
    correction::Correction::Ref electronSF_;
    correction::Correction::Ref photonSF_;
    correction::Correction::Ref tauJETSF_;
    correction::Correction::Ref tauELESF_;
    correction::Correction::Ref tauMUOSF_;
    correction::Correction::Ref btvHFSF_;
    correction::Correction::Ref btvLFSF_;
    correction::CompoundCorrection::Ref JEC_;
    correction::Correction::Ref jesUnc_;
    correction::Correction::Ref puJetIDSF_;
};

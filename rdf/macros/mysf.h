#include "correction.h"
#include <stdio.h>
#include <string.h>
#include <iostream>

//g++ $(correction config --cflags --ldflags) mysf.cpp -shared -fPIC -o mysf.so

class MyCorrections {
  public:
    MyCorrections(int the_input_year);
    double eval_puSF      (double NumTrueInteractions, std::string weights);
    double eval_muonTRKSF (const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_muonIDSF  (const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_muonISOSF (const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_electronSF(const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_photonSF  (const char *the_input_year, const char *valType, const char *workingPoint, double eta, double pt);
    double eval_tauJETSF  (double pt, int dm, int genmatch, const char *workingPoint, const char *valType);
    double eval_tauELESF  (double eta, int genmatch, const char *workingPoint, const char *valType);
    double eval_tauMUOSF  (double eta, int genmatch, const char *workingPoint, const char *valType);
    double eval_btvSF     (const char *valType, char *workingPoint, double eta, double pt, int flavor);
    double eval_jetCORR   (double area, double eta, double pt, double rho, int type);
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
    correction::Correction::Ref electronSF_;
    correction::Correction::Ref photonSF_;
    correction::Correction::Ref tauJETSF_;
    correction::Correction::Ref tauELESF_;
    correction::Correction::Ref tauMUOSF_;
    correction::Correction::Ref btvHFSF_;
    correction::Correction::Ref btvLFSF_;
    correction::CompoundCorrection::Ref JECMC_;
    correction::CompoundCorrection::Ref JECDATA_[10];
    correction::Correction::Ref JECL2ResDATA_[10];
    correction::Correction::Ref jetVetoMap_[10];
    correction::Correction::Ref jesUnc_;
    correction::Correction::Ref jerMethod1Unc_;
    correction::Correction::Ref jerMethod2Unc_;
    correction::Correction::Ref puJetIDSF_;
    int year;
    int yearPrime;
};

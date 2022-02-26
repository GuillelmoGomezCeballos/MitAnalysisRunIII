#include "correction.h"
#include <stdio.h>
#include <string.h>

//g++ $(correction config --cflags --ldflags) mysf.cpp -shared -fPIC -o mysf.so

class MyCorrections {
  public:
    MyCorrections(int year);
    double eval_muonIDSF  (char *year, char *valType, char *workingPoint, double eta, double pt);
    double eval_muonISOSF (char *year, char *valType, char *workingPoint, double eta, double pt);
    double eval_electronSF(char *year, char *valType, char *workingPoint, double eta, double pt);
    double eval_photonSF  (char *year, char *valType, char *workingPoint, double eta, double pt);
    double eval_btvSF     (            char *valType, char *workingPoint, double eta, double pt, int flavor);
    double eval_puJetIDSF (            char *valType, char *workingPoint, double eta, double pt);
  private:
    correction::Correction::Ref muonIDSF_;
    correction::Correction::Ref muonISOSF_;
    correction::Correction::Ref electronSF_;
    correction::Correction::Ref photonSF_;
    correction::Correction::Ref btvHFSF_;
    correction::Correction::Ref btvLFSF_;
    correction::Correction::Ref puJetIDSF_;
};

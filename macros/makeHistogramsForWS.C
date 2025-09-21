void makeHistogramsForWS(const int year){

  const int nBinEta0 = 5; Float_t xbinsEta0[nBinEta0+1] = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5};

  const int nBinEta1 = 2; Float_t xbinsEta1[nBinEta1+1] = {0.0, 1.5, 2.5};
  const int nBinPt1  = 3; Float_t xbinsPt1 [nBinPt1+1]  = {10, 25, 40, 80};

  double WSSF20220[5]  = {1.456953,1.707981,1.348056,1.335759,1.384332};
  double WSSFE_mcanddata20220[5] = {0.342959,0.173783,0.087966,0.048742,0.046326};

  double WSSF20221[5]  = {1.347428,1.515720,1.414271,1.403208,1.405011};
  double WSSFE_mcanddata20221[5] = {0.191316,0.119399,0.054362,0.029153,0.025964};

  double WSSF20230[5]  = {1.636975,1.587178,1.598208,1.331865,1.476417};
  double WSSFE_mcanddata20230[5] = {0.190365,0.127726,0.064845,0.034086,0.032246};

  double WSSF20231[5]  = {1.470449,1.315584,1.265207,1.433499,1.373112};
  double WSSFE_mcanddata20231[5] = {0.280629,0.161489,0.090423,0.046717,0.044425};

  double WSSF20240[5]  = {1.383295,1.287207,1.227201,1.310760,1.507986};
  double WSSFE_mcanddata20240[5] = {0.092341,0.048968,0.028301,0.016327,0.016441};

  double WSSF20250[5]  = {1.790886,1.502887,1.405082,1.300130,1.448496};
  double WSSFE_mcanddata20250[5] = {0.110087,0.065237,0.037531,0.023219,0.024229};

  double WSSF2027[5]  = {1.433251,1.391224,1.318956,1.338758,1.476039};
  double WSSFE_mcanddata2027[5] = {0.072217,0.041461,0.021813,0.012287,0.011782};

  double WSEtaPtSF20220[6]  = {1.773063,1.349036,1.420971,1.304070,1.391079,1.324912};
  double WSEtaPtSFE_mcanddata20220[6] = {0.377516,0.122097,0.118468,0.150649,0.053242,0.044583};

  double WSEtaPtSF20221[6]  = {3.811876,1.384878,1.309926,1.662885,1.345719,1.383791};
  double WSEtaPtSFE_mcanddata20221[6] = {0.311142,0.080930,0.072872,0.087330,0.030241,0.026138};

  double WSEtaPtSF20230[6]  = {2.541849,1.670873,1.423588,1.500680,1.328621,1.436064};
  double WSEtaPtSFE_mcanddata20230[6] = {0.223695,0.088917,0.086094,0.105448,0.036428,0.032114};

  double WSEtaPtSF20231[6]  = {1.565437,1.349280,1.163277,1.552925,1.400193,1.355689};
  double WSEtaPtSFE_mcanddata20231[6] = {0.247055,0.117430,0.119513,0.150565,0.050377,0.043653};

  double WSEtaPtSF20240[6]  = {1.780785,1.188894,1.225741,1.860825,1.458175,1.345240};
  double WSEtaPtSFE_mcanddata20240[6] = {0.118660,0.041487,0.033463,0.074328,0.019113,0.014440};

  double WSEtaPtSF20250[6]  = {2.185967,1.450225,1.409894,1.544765,1.369447,1.326094};
  double WSEtaPtSFE_mcanddata20250[6] = {0.144865,0.054632,0.043609,0.110786,0.027671,0.020913};

  double WSEtaPtSF2027[6]  = {1.970985,1.280193,1.260362,1.659024,1.415632,1.369881};
  double WSEtaPtSFE_mcanddata2027[6] = {0.082669,0.030930,0.026565,0.044918,0.013707,0.010941};

  double WSSF[nBinEta0];
  double WSSFE_mcanddataF[nBinEta0];

  TH1D* histoWSEtaSF     = new TH1D("histoWSEtaSF",     "histoWSEtaSF",     nBinEta0, xbinsEta0);
  TH1D* histoWSEtaSF_unc = new TH1D("histoWSEtaSF_unc", "histoWSEtaSF_unc", nBinEta0, xbinsEta0);
  TH2D* histoWSEtaPtSF   = new TH2D("histoWSEtaPtSF",   "histoWSEtaPtSF",   nBinEta1, xbinsEta1, nBinPt1, xbinsPt1);

  if     (year == 20220){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20220[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20220[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20220[i]+WSSFE_mcanddata20220[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20220[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20220[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20220[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20220[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20220[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20220[5]);
  }
  else if(year == 20221){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20221[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20221[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20221[i]+WSSFE_mcanddata20221[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20221[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20221[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20221[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20221[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20221[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20221[5]);
  }
  else if(year == 20230){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20230[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20230[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20230[i]+WSSFE_mcanddata20230[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20230[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20230[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20230[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20230[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20230[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20230[5]);
  }
  else if(year == 20231){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20231[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20231[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20231[i]+WSSFE_mcanddata20231[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20231[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20231[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20231[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20231[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20231[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20231[5]);
  }
  else if(year == 20240){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20240[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20240[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20240[i]+WSSFE_mcanddata20240[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20240[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20240[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20240[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20240[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20240[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20240[5]);
  }
  else if(year == 20250){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20250[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20250[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20250[i]+WSSFE_mcanddata20250[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20250[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20250[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20250[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20250[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20250[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20250[5]);
  }
  else if(year == 2027){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF2027[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata2027[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF2027[i]+WSSFE_mcanddata2027[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF2027[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF2027[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF2027[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF2027[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF2027[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF2027[5]);
  }
  else {
    printf("WRONG year (%d)\n",year);
    return;
  }

  char outputLimits[200];
  sprintf(outputLimits,"histoWSSF_%d.root",year);
  TFile* outFileLimits = new TFile(outputLimits,"recreate");
  outFileLimits->cd();
    histoWSEtaSF    ->Write();
    histoWSEtaSF_unc->Write();
    histoWSEtaPtSF  ->Write();
  outFileLimits->Close();
}

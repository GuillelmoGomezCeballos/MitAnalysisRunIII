void makeHistogramsForWS(const int year){

  const int nBinEta0 = 5; Float_t xbinsEta0[nBinEta0+1] = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5};

  const int nBinEta1 = 2; Float_t xbinsEta1[nBinEta1+1] = {0.0, 1.5, 2.5};
  const int nBinPt1  = 3; Float_t xbinsPt1 [nBinPt1+1]  = {10, 25, 40, 80};
 
  double WSSF20220[5]  = {1.678770,1.781094,1.301419,1.346593,1.397297};
  double WSSFE_mcanddata20220[5] = {0.322528,0.169063,0.085333,0.047117,0.045555};

  double WSSF20221[5]  = {1.422787,1.508731,1.321264,1.382549,1.417033};
  double WSSFE_mcanddata20221[5] = {0.179678,0.116045,0.051591,0.028172,0.025762};

  double WSSF20230[5]  = {1.596583,1.691725,1.554082,1.333472,1.548538};
  double WSSFE_mcanddata20230[5] = {0.180954,0.120721,0.061388,0.032853,0.032278};

  double WSSF20231[5]  = {1.379372,1.449481,1.437460,1.467949,1.382699};
  double WSSFE_mcanddata20231[5] = {0.263212,0.154385,0.086542,0.045220,0.044198};

  double WSSF20240[5]  = {1.472165,1.267221,1.244714,1.335560,1.546570};
  double WSSFE_mcanddata20240[5] = {0.087221,0.047547,0.028233,0.016345,0.017125};

  double WSSF20250[5]  = {1.472165,1.267221,1.244714,1.335560,1.546570};
  double WSSFE_mcanddata20250[5] = {0.087221,0.047547,0.028233,0.016345,0.017125};

  double WSSF2027[5]  = {1.418776,1.372515,1.314003,1.348186,1.502452};
  double WSSFE_mcanddata2027[5] = {0.068900,0.038747,0.020904,0.012133,0.011968};

  double WSEtaPtSF20220[6]  = {1.781311,1.368976,1.422955,1.510154,1.365332,1.340711};
  double WSEtaPtSFE_mcanddata20220[6] = {0.350821,0.113929,0.116816,0.143390,0.051490,0.043913};

  double WSEtaPtSF20221[6]  = {1.800264,1.280407,1.315156,1.759977,1.324909,1.395706};
  double WSEtaPtSFE_mcanddata20221[6] = {0.244618,0.074735,0.068863,0.083874,0.029426,0.025898};

  double WSEtaPtSF20230[6]  = {1.421723,1.705011,1.357148,1.759478,1.370710,1.436809};
  double WSEtaPtSFE_mcanddata20230[6] = {0.190663,0.084592,0.084113,0.102315,0.035460,0.031906};

  double WSEtaPtSF20231[6]  = {2.087435,1.394561,1.302442,1.601241,1.420967,1.369273};
  double WSEtaPtSFE_mcanddata20231[6] = {0.245243,0.110113,0.116070,0.137816,0.049025,0.043653};

  double WSEtaPtSF20240[6]  = {1.853957,1.233264,1.266865,2.012984,1.495563,1.375291};
  double WSEtaPtSFE_mcanddata20240[6] = {0.119915,0.039173,0.030416,0.075984,0.019440,0.014838};

  double WSEtaPtSF20250[6]  = {1.853957,1.233264,1.266865,2.012984,1.495563,1.375291};
  double WSEtaPtSFE_mcanddata20250[6] = {0.119915,0.039173,0.030416,0.075984,0.019440,0.014838};

  double WSEtaPtSF2027[6]  = {2.010664,1.331542,1.276627,1.772149,1.427713,1.387398};
  double WSEtaPtSFE_mcanddata2027[6] = {0.079418,0.029429,0.026461,0.043693,0.013567,0.011118};

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

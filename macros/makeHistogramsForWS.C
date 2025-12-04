void makeHistogramsForWS(const int year){

  const int nBinEta0 = 5; Float_t xbinsEta0[nBinEta0+1] = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5};

  const int nBinEta1 = 2; Float_t xbinsEta1[nBinEta1+1] = {0.0, 1.5, 2.5};
  const int nBinPt1  = 3; Float_t xbinsPt1 [nBinPt1+1]  = {10, 25, 40, 80};

  double WSSF20220[5]  = {1.444886,1.719085,1.411088,1.338871,1.385369};
  double WSSFE_mcanddata20220[5] = {0.339688,0.174927,0.089330,0.048611,0.046340};

  double WSSF20221[5]  = {1.349703,1.504901,1.409908,1.423997,1.405394};
  double WSSFE_mcanddata20221[5] = {0.190748,0.122907,0.054938,0.029280,0.025986};

  double WSSF20230[5]  = {1.617011,1.603229,1.602291,1.357769,1.474984};
  double WSSFE_mcanddata20230[5] = {0.189980,0.127298,0.065037,0.034160,0.032297};

  double WSSF20231[5]  = {1.475188,1.301941,1.285810,1.445522,1.396421};
  double WSSFE_mcanddata20231[5] = {0.281791,0.160468,0.090855,0.046773,0.044599};

  double WSSF20240[5]  = {1.419137,1.283531,1.232335,1.311556,1.513457};
  double WSSFE_mcanddata20240[5] = {0.093707,0.048896,0.028363,0.016332,0.016473};

  double WSSF20250[5]  = {1.790886,1.502887,1.405082,1.300130,1.448496};
  double WSSFE_mcanddata20250[5] = {0.110087,0.065237,0.037531,0.023219,0.024229};

  double WSSF2027[5]  = {1.461637,1.381894,1.325222,1.347565,1.494572};
  double WSSFE_mcanddata2027[5] = {0.073003,0.041329,0.021871,0.012301,0.011758};

  double WSEtaPtSF20220[6]  = {1.969173,1.445763,1.399182,1.302349,1.395060,1.329518};
  double WSEtaPtSFE_mcanddata20220[6] = {0.401528,0.124965,0.116602,0.148136,0.053017,0.044559};

  double WSEtaPtSF20221[6]  = {1.496270,1.368049,1.324932,1.708737,1.359140,1.385124};
  double WSEtaPtSFE_mcanddata20221[6] = {0.295550,0.080350,0.073577,0.087470,0.030383,0.026114};

  double WSEtaPtSF20230[6]  = {1.271994,1.698211,1.421946,1.538757,1.338578,1.448112};
  double WSEtaPtSFE_mcanddata20230[6] = {0.208751,0.089961,0.085907,0.106287,0.036398,0.032236};

  double WSEtaPtSF20231[6]  = {1.564861,1.360465,1.181154,1.623327,1.416386,1.366002};
  double WSEtaPtSFE_mcanddata20231[6] = {0.247496,0.117887,0.117185,0.150385,0.050416,0.043806};

  double WSEtaPtSF20240[6]  = {1.813130,1.190802,1.255048,1.915648,1.471237,1.343251};
  double WSEtaPtSFE_mcanddata20240[6] = {0.118967,0.041284,0.030562,0.075007,0.019191,0.014435};

  double WSEtaPtSF20250[6]  = {2.185967,1.450225,1.409894,1.544765,1.369447,1.326094};
  double WSEtaPtSFE_mcanddata20250[6] = {0.144865,0.054632,0.043609,0.110786,0.027671,0.020913};

  double WSEtaPtSF2027[6]  = {1.767110,1.290283,1.268377,1.703524,1.430770,1.372616};
  double WSEtaPtSFE_mcanddata2027[6] = {0.081997,0.031104,0.026758,0.044767,0.013738,0.010951};

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

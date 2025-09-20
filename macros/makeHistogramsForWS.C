void makeHistogramsForWS(const int year){

  const int nBinEta0 = 5; Float_t xbinsEta0[nBinEta0+1] = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5};

  const int nBinEta1 = 2; Float_t xbinsEta1[nBinEta1+1] = {0.0, 1.5, 2.5};
  const int nBinPt1  = 3; Float_t xbinsPt1 [nBinPt1+1]  = {10, 25, 40, 80};

  double WSSF20220[5]  = {1.455410,1.762831,1.355610,1.326729,1.381207};
  double WSSFE_mcanddata20220[5] = {0.342627,0.177163,0.087833,0.048716,0.046294};

  double WSSF20221[5]  = {1.284425,1.524303,1.397195,1.400960,1.398607};
  double WSSFE_mcanddata20221[5] = {0.186939,0.122590,0.054689,0.029139,0.025935};

  double WSSF20230[5]  = {1.622424,1.581323,1.609463,1.344382,1.481584};
  double WSSFE_mcanddata20230[5] = {0.189300,0.127426,0.064882,0.034103,0.032289};

  double WSSF20231[5]  = {1.336398,1.338252,1.312078,1.415754,1.369194};
  double WSSFE_mcanddata20231[5] = {0.265627,0.162847,0.091225,0.046521,0.044367};

  double WSSF20240[5]  = {1.431734,1.266253,1.226895,1.311623,1.509026};
  double WSSFE_mcanddata20240[5] = {0.094192,0.048561,0.028298,0.016343,0.016473};

  double WSSF20250[5]  = {1.790886,1.502887,1.405082,1.300130,1.448496};
  double WSSFE_mcanddata20250[5] = {0.110087,0.065237,0.037531,0.023219,0.024229};

  double WSSF2027[5]  = {1.449368,1.380176,1.320396,1.337724,1.476468};
  double WSSFE_mcanddata2027[5] = {0.072691,0.041266,0.021832,0.012282,0.011827};

  double WSEtaPtSF20220[6]  = {1.806414,1.367786,1.423876,1.251550,1.382545,1.332036};
  double WSEtaPtSFE_mcanddata20220[6] = {0.379967,0.123072,0.118596,0.148667,0.053101,0.044639};

  double WSEtaPtSF20221[6]  = {3.635651,1.346878,1.318716,1.648752,1.340380,1.382475};
  double WSEtaPtSFE_mcanddata20221[6] = {0.306365,0.079725,0.073144,0.087172,0.030330,0.026108};

  double WSEtaPtSF20230[6]  = {2.510822,1.688150,1.407907,1.489264,1.343260,1.436649};
  double WSEtaPtSFE_mcanddata20230[6] = {0.221850,0.089410,0.085504,0.105245,0.036564,0.032140};

  double WSEtaPtSF20231[6]  = {1.545110,1.396520,1.156642,1.526238,1.371190,1.365001};
  double WSEtaPtSFE_mcanddata20231[6] = {0.245855,0.119772,0.119158,0.149320,0.049990,0.043760};

  double WSEtaPtSF20240[6]  = {1.786838,1.192662,1.224136,1.838636,1.455345,1.348724};
  double WSEtaPtSFE_mcanddata20240[6] = {0.118922,0.041551,0.033438,0.073750,0.019106,0.014471};

  double WSEtaPtSF20250[6]  = {2.185967,1.450225,1.409894,1.544765,1.369447,1.326094};
  double WSEtaPtSFE_mcanddata20250[6] = {0.144865,0.054632,0.043609,0.110786,0.027671,0.020913};

  double WSEtaPtSF2027[6]  = {1.982180,1.281539,1.264779,1.636197,1.410804,1.371175};
  double WSEtaPtSFE_mcanddata2027[6] = {0.082988,0.030947,0.026621,0.044532,0.013680,0.010946};

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

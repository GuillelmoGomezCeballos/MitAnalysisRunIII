void makeHistogramsForWS(const int year){

  const int nBinEta0 = 5; Float_t xbinsEta0[nBinEta0+1] = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5};

  const int nBinEta1 = 2; Float_t xbinsEta1[nBinEta1+1] = {0.0, 1.5, 2.5};
  const int nBinPt1  = 3; Float_t xbinsPt1 [nBinPt1+1]  = {10, 25, 40, 80};
 
  double WSSF20220[5]  = {1.724361,1.720582,1.316642,1.350376,1.388903};
  double WSSFE_mcanddata20220[5] = {0.320037,0.164859,0.085857,0.047020,0.045386};

  double WSSF20221[5]  = {1.394527,1.511810,1.335918,1.398463,1.431596};
  double WSSFE_mcanddata20221[5] = {0.177414,0.116180,0.051740,0.028185,0.025806};

  double WSSF20230[5]  = {1.583335,1.772180,1.525053,1.335223,1.541087};
  double WSSFE_mcanddata20230[5] = {0.179835,0.121039,0.060906,0.032809,0.032170};

  double WSSF20231[5]  = {1.441103,1.361295,1.435914,1.498158,1.393888};
  double WSSFE_mcanddata20231[5] = {0.270068,0.150757,0.086248,0.045631,0.044320};

  double WSSF20240[5]  = {1.452932,1.259267,1.240283,1.339206,1.542629};
  double WSSFE_mcanddata20240[5] = {0.086463,0.047385,0.028178,0.016370,0.017099};

  double WSSF20250[5]  = {1.452932,1.259267,1.240283,1.339206,1.542629};
  double WSSFE_mcanddata20250[5] = {0.086463,0.047385,0.028178,0.016370,0.017099};

  double WSSF2027[5]  = {1.391573,1.365013,1.312266,1.355391,1.502695};
  double WSSFE_mcanddata2027[5] = {0.068158,0.038628,0.020889,0.012169,0.011969};

  double WSEtaPtSF20220[6]  = {1.641880,1.415508,1.407502,1.551702,1.363360,1.329818};
  double WSEtaPtSFE_mcanddata20220[6] = {0.342677,0.115449,0.116033,0.144459,0.051450,0.043702};

  double WSEtaPtSF20221[6]  = {1.698654,1.306237,1.307805,1.805553,1.336699,1.406315};
  double WSEtaPtSFE_mcanddata20221[6] = {0.237657,0.075599,0.068632,0.084258,0.029581,0.025908};

  double WSEtaPtSF20230[6]  = {2.153996,1.703362,1.374837,1.805506,1.359599,1.442101};
  double WSEtaPtSFE_mcanddata20230[6] = {0.177533,0.084613,0.084767,0.103218,0.035413,0.031973};

  double WSEtaPtSF20231[6]  = {1.923395,1.457263,1.242220,1.659616,1.443289,1.377317};
  double WSEtaPtSFE_mcanddata20231[6] = {0.235842,0.112940,0.113170,0.139874,0.049287,0.043718};

  double WSEtaPtSF20240[6]  = {1.747771,1.220658,1.266658,1.998466,1.489643,1.381203};
  double WSEtaPtSFE_mcanddata20240[6] = {0.115403,0.038951,0.030409,0.076524,0.019426,0.014737};

  double WSEtaPtSF20250[6]  = {1.747771,1.220658,1.266658,1.998466,1.489643,1.381203};
  double WSEtaPtSFE_mcanddata20250[6] = {0.115403,0.038951,0.030409,0.076524,0.019426,0.014737};

  double WSEtaPtSF2027[6]  = {1.913582,1.332075,1.277888,1.803556,1.422959,1.394027};
  double WSEtaPtSFE_mcanddata2027[6] = {0.077174,0.029504,0.026577,0.043762,0.013655,0.011139};

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

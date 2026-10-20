void makeHistogramsForWS(const int year){

  const int nBinEta0 = 5; Float_t xbinsEta0[nBinEta0+1] = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5};

  const int nBinEta1 = 2; Float_t xbinsEta1[nBinEta1+1] = {0.0, 1.5, 2.5};
  const int nBinPt1  = 3; Float_t xbinsPt1 [nBinPt1+1]  = {10, 25, 40, 80};
 
  double WSSF20160[5]  = {1.0, 1.0, 1.0, 1.0, 1.0};
  double WSSFE_mcanddata20160[5] = {0.30, 0.30, 0.30, 0.30, 0.30};

  double WSSF20161[5]  = {1.0, 1.0, 1.0, 1.0, 1.0};
  double WSSFE_mcanddata20161[5] = {0.30, 0.30, 0.30, 0.30, 0.30};

  double WSSF20170[5]  = {1.4, 1.4, 1.4, 1.4, 1.4};
  double WSSFE_mcanddata20170[5] = {0.30, 0.30, 0.30, 0.30, 0.30};

  double WSSF20180[5]  = {1.4, 1.4, 1.4, 1.4, 1.4};
  double WSSFE_mcanddata20180[5] = {0.30, 0.30, 0.30, 0.30, 0.30};

  double WSSF20220[5]  = {1.752590,1.730878,1.330919,1.339548,1.395591};
  double WSSFE_mcanddata20220[5] = {0.323340,0.165419,0.085794,0.046940,0.045495};

  double WSSF20221[5]  = {1.423832,1.477721,1.336006,1.392386,1.424612};
  double WSSFE_mcanddata20221[5] = {0.179716,0.114530,0.051754,0.028125,0.025764};

  double WSSF20230[5]  = {1.625766,1.712589,1.549456,1.335808,1.542244};
  double WSSFE_mcanddata20230[5] = {0.182706,0.121568,0.060623,0.032815,0.032184};

  double WSSF20231[5]  = {1.344670,1.391745,1.434847,1.458056,1.388671};
  double WSSFE_mcanddata20231[5] = {0.265674,0.152929,0.086487,0.045114,0.044234};

  double WSSF20240[5]  = {1.462372,1.261704,1.244791,1.333009,1.544757};
  double WSSFE_mcanddata20240[5] = {0.086827,0.047426,0.028229,0.016369,0.017114};

  double WSSF20250[5]  = {1.713083,1.544651,1.469566,1.484190,1.600614};
  double WSSFE_mcanddata20250[5] = {0.071178,0.044506,0.026336,0.016608,0.019289};

  double WSSF2028[5]  = {1.552498,1.459772,1.376709,1.395523,1.524755};
  double WSSFE_mcanddata2028[5] = {0.052130,0.028602,0.016484,0.009783,0.010131};

  double WSEtaPtSF20160[6]  = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
  double WSEtaPtSFE_mcanddata20160[6] = {0.30, 0.30, 0.30, 0.30, 0.30, 0.30};

  double WSEtaPtSF20161[6]  = {1.0, 1.0, 1.0, 1.0, 1.0, 1.0};
  double WSEtaPtSFE_mcanddata20161[6] = {0.30, 0.30, 0.30, 0.30, 0.30, 0.30};

  double WSEtaPtSF20170[6]  = {1.4, 1.4, 1.4, 1.4, 1.4, 1.4};
  double WSEtaPtSFE_mcanddata20170[6] = {0.30, 0.30, 0.30, 0.30, 0.30, 0.30};

  double WSEtaPtSF20180[6]  = {1.4, 1.4, 1.4, 1.4, 1.4, 1.4};
  double WSEtaPtSFE_mcanddata20180[6] = {0.30, 0.30, 0.30, 0.30, 0.30, 0.30};

  double WSEtaPtSF20220[6]  = {1.682938,1.411229,1.412242,1.537781,1.360882,1.327544};
  double WSEtaPtSFE_mcanddata20220[6] = {0.364936,0.115214,0.116238,0.144118,0.051482,0.043764};

  double WSEtaPtSF20221[6]  = {1.613833,1.292309,1.309209,1.779102,1.332733,1.403640};
  double WSEtaPtSFE_mcanddata20221[6] = {0.240820,0.075117,0.068669,0.083467,0.029518,0.025797};

  double WSEtaPtSF20230[6]  = {1.422412,1.700224,1.365583,1.746786,1.370773,1.433966};
  double WSEtaPtSFE_mcanddata20230[6] = {0.188254,0.084435,0.084406,0.102183,0.035451,0.031863};

  double WSEtaPtSF20231[6]  = {1.877272,1.398069,1.283142,1.556335,1.418757,1.377423};
  double WSEtaPtSFE_mcanddata20231[6] = {0.234020,0.110260,0.115136,0.136958,0.048929,0.043664};

  double WSEtaPtSF20240[6]  = {1.826410,1.221404,1.267416,1.985713,1.497290,1.376173};
  double WSEtaPtSFE_mcanddata20240[6] = {0.118578,0.038963,0.030421,0.076339,0.019449,0.014826};

  double WSEtaPtSF20250[6]  = {1.261859,1.464816,1.462728,2.312027,1.572312,1.473188};
  double WSEtaPtSFE_mcanddata20250[6] = {0.105273,0.035671,0.028983,0.088107,0.020631,0.015955};

  double WSEtaPtSF2028[6]  = {1.763172,1.391336,1.353152,1.852830,1.468410,1.418515};
  double WSEtaPtSFE_mcanddata2028[6] = {0.060719,0.022213,0.019843,0.039366,0.011133,0.009097};

  double WSSF[nBinEta0];
  double WSSFE_mcanddataF[nBinEta0];

  TH1D* histoWSEtaSF     = new TH1D("histoWSEtaSF",     "histoWSEtaSF",     nBinEta0, xbinsEta0);
  TH1D* histoWSEtaSF_unc = new TH1D("histoWSEtaSF_unc", "histoWSEtaSF_unc", nBinEta0, xbinsEta0);
  TH2D* histoWSEtaPtSF   = new TH2D("histoWSEtaPtSF",   "histoWSEtaPtSF",   nBinEta1, xbinsEta1, nBinPt1, xbinsPt1);

  if     (year == 20160){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20160[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20160[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20160[i]+WSSFE_mcanddata20160[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20160[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20160[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20160[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20160[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20160[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20160[5]);
  }
  else if(year == 20161){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20161[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20161[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20161[i]+WSSFE_mcanddata20161[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20161[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20161[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20161[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20161[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20161[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20161[5]);
  }
  else if(year == 20170){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20170[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20170[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20170[i]+WSSFE_mcanddata20170[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20170[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20170[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20170[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20170[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20170[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20170[5]);
  }
  else if(year == 20180){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20180[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata20180[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20180[i]+WSSFE_mcanddata20180[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20180[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20180[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20180[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20180[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20180[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20180[5]);
  }
  else if(year == 20220){
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
  else if(year == 2028){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF2028[i]);
      histoWSEtaSF    ->SetBinError  (i+1,WSSFE_mcanddata2028[i]);
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF2028[i]+WSSFE_mcanddata2028[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF2028[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF2028[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF2028[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF2028[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF2028[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF2028[5]);
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

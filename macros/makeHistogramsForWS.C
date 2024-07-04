void makeHistogramsForWS(const int year){

  const int nBinEta0 = 5; Float_t xbinsEta0[nBinEta0+1] = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5};

  const int nBinEta1 = 2; Float_t xbinsEta1[nBinEta1+1] = {0.0, 1.5, 2.5};
  const int nBinPt1  = 3; Float_t xbinsPt1 [nBinPt1+1]  = {10, 25, 40, 80};

  double WSSF20220[nBinEta0]  = {1.268119,1.138050,1.622429,1.287785,1.368622};
  double WSSFE_mcanddata20220[nBinEta0] = {0.529878,0.130784,0.149766,0.094497,0.054267};

  double WSSF20221[nBinEta0]  = {1.274343,1.568827,2.208971,1.327840,1.324173};
  double WSSFE_mcanddata20221[nBinEta0] = {0.590153,0.087071,0.118618,0.055036,0.030685};

  double WSSF20230[nBinEta0]  = {1.256221,1.573012,1.623754,1.726238,1.316275};
  double WSSFE_mcanddata20230[nBinEta0] = {0.439486,0.103894,0.132410,0.070581,0.040678};

  double WSSF20231[nBinEta0]  = {1.057984,1.149316,0.858194,1.582266,1.377443};
  double WSSFE_mcanddata20231[nBinEta0] = {0.510979,0.145717,0.164173,0.100790,0.056244};

  double WSEtaPtSF20220[nBinEta1*nBinPt1]  = {1.595965,0.988321,1.579822,1.749350,1.377976,1.267989};
  double WSEtaPtSF20220_mcanddata[nBinEta1*nBinPt1] = {0.533625,0.166669,0.155761,0.208432,0.065267,0.056556};

  double WSEtaPtSF20221[nBinEta1*nBinPt1]  = {1.850293,1.567888,1.305748,1.564472,1.285516,1.392796};
  double WSEtaPtSF20221_mcanddata[nBinEta1*nBinPt1] = {0.309125,0.115638,0.096890,0.123297,0.038300,0.033021};

  double WSEtaPtSF20230[nBinEta1*nBinPt1]  = {1.388195,1.575605,1.351364,21.809448,1.628451,1.386071};
  double WSEtaPtSF20230_mcanddata[nBinEta1*nBinPt1] = {0.586104,0.114903,0.124833,1.301535,0.052702,0.042382};

  double WSEtaPtSF20231[nBinEta1*nBinPt1]  = {1.337865,1.145688,1.421703,1.523568,1.315334,1.360165};
  double WSEtaPtSF20231_mcanddata[nBinEta1*nBinPt1] = {0.378983,0.179897,0.167731,0.215343,0.066434,0.059861};

  double WSSF[nBinEta0];
  double WSSFE_mcanddataF[nBinEta0];

  TH1D* histoWSEtaSF     = new TH1D("histoWSEtaSF",     "histoWSEtaSF",     nBinEta0, xbinsEta0);
  TH1D* histoWSEtaSF_unc = new TH1D("histoWSEtaSF_unc", "histoWSEtaSF_unc", nBinEta0, xbinsEta0);
  TH2D* histoWSEtaPtSF   = new TH2D("histoWSEtaPtSF",   "histoWSEtaPtSF",   nBinEta1, xbinsEta1, nBinPt1, xbinsPt1);

  if     (year == 20220){
    for(int i=0; i<nBinEta0; i++){
      histoWSEtaSF    ->SetBinContent(i+1,WSSF20220[i]);
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
      histoWSEtaSF_unc->SetBinContent(i+1,WSSF20231[i]+WSSFE_mcanddata20231[i]);
    }
    histoWSEtaPtSF->SetBinContent(1,1,WSEtaPtSF20231[0]);
    histoWSEtaPtSF->SetBinContent(1,2,WSEtaPtSF20231[1]);
    histoWSEtaPtSF->SetBinContent(1,3,WSEtaPtSF20231[2]);
    histoWSEtaPtSF->SetBinContent(2,1,WSEtaPtSF20231[3]);
    histoWSEtaPtSF->SetBinContent(2,2,WSEtaPtSF20231[4]);
    histoWSEtaPtSF->SetBinContent(2,3,WSEtaPtSF20231[5]);
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

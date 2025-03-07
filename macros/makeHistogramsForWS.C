void makeHistogramsForWS(const int year){

  const int nBinEta0 = 5; Float_t xbinsEta0[nBinEta0+1] = {0.0, 0.5, 1.0, 1.5, 2.0, 2.5};

  const int nBinEta1 = 2; Float_t xbinsEta1[nBinEta1+1] = {0.0, 1.5, 2.5};
  const int nBinPt1  = 3; Float_t xbinsPt1 [nBinPt1+1]  = {10, 25, 40, 80};

  double WSSF20220[nBinEta0]  = {1.315811,1.153349,1.631069,1.284297,1.380738};
  double WSSFE_mcanddata20220[nBinEta0] = {0.540189,0.131664,0.150244,0.094354,0.054452};

  double WSSF20221[nBinEta0]  = {1.194855,1.579243,2.185388,1.313134,1.330893};
  double WSSFE_mcanddata20221[nBinEta0] = {0.571791,0.087366,0.117793,0.054770,0.030737};

  double WSSF20230[nBinEta0]  = {1.211092,1.586622,1.715340,1.760252,1.329134};
  double WSSFE_mcanddata20230[nBinEta0] = {0.408411,0.103444,0.130921,0.070409,0.040865};

  double WSSF20231[nBinEta0]  = {0.826141,1.215861,0.912377,1.575210,1.415072};
  double WSSFE_mcanddata20231[nBinEta0] = {0.556369,0.142265,0.164868,0.099155,0.056500};

  double WSSF20240[nBinEta0]  = {1.321356,1.294005,1.471534,1.464870,1.370746};
  double WSSFE_mcanddata20240[nBinEta0] = {0.155831,0.039666,0.047071,0.027348,0.017527};

  double WSEtaPtSF20220[nBinEta1*nBinPt1]  = {1.729370,0.793228,1.570735,1.631007,1.395025,1.268174};
  double WSEtaPtSF20220_mcanddata[nBinEta1*nBinPt1] = {0.555493,0.167070,0.155184,0.201537,0.065378,0.056575};

  double WSEtaPtSF20221[nBinEta1*nBinPt1]  = {1.882378,1.574969,1.280408,1.700515,1.275865,1.399145};
  double WSEtaPtSF20221_mcanddata[nBinEta1*nBinPt1] = {0.312745,0.116033,0.095811,0.127144,0.038127,0.033025};

  double WSEtaPtSF20230[nBinEta1*nBinPt1]  = {1.643671,1.550877,1.339880,59.853772,1.643334,1.387880};
  double WSEtaPtSF20230_mcanddata[nBinEta1*nBinPt1] = {0.501791,0.112420,0.124612,3.354394,0.052577,0.042393};

  double WSEtaPtSF20231[nBinEta1*nBinPt1]  = {1.679764,1.238634,1.339455,1.435482,1.233011,1.363176};
  double WSEtaPtSF20231_mcanddata[nBinEta1*nBinPt1] = {0.342833,0.163913,0.168713,0.240652,0.074078,0.059627};

  double WSEtaPtSF20240[nBinEta1*nBinPt1]  = {1.687095,1.176340,1.338764,1.533076,1.327149,1.357125};
  double WSEtaPtSF20240_mcanddata[nBinEta1*nBinPt1] = {0.101269,0.048274,0.043808,0.050532,0.019880,0.019145};

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

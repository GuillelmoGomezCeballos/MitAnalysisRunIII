import ROOT
import os, json

def selectionTauVeto(df,year):

    dftag =(df.Define("good_tau", "abs(Tau_eta) < 2.3 && Tau_pt > 20 && Tau_idDeepTau2018v2p5VSjet >= 6 && Tau_idDeepTau2018v2p5VSe >= 6 && Tau_idDeepTau2018v2p5VSmu >= 4")
              .Filter("Sum(good_tau) == 0","No selected hadronic taus")
              .Define("good_Tau_pt", "Tau_pt[good_tau]")
              .Define("good_Tau_eta", "Tau_eta[good_tau]")
              .Define("good_Tau_decayMode", "Tau_decayMode[good_tau]")
              .Define("good_Tau_genPartFlav", "Tau_genPartFlav[good_tau]")
              )

    return dftag

def selectionPhoton(df,year,BARRELphotons,ENDCAPphotons):

    dftag =(df.Define("photon_mask", "cleaningMask(Electron_photonIdx[fake_el],nPhoton)")
              .Define("good_Photons", "{}".format(BARRELphotons)+" or {}".format(ENDCAPphotons) )
              .Define("good_Photons_pt", "Photon_pt[good_Photons]")
              .Define("good_Photons_eta", "Photon_eta[good_Photons]")
              .Define("good_Photons_phi", "Photon_phi[good_Photons]")
              )

    return dftag

def selectionJetMet(df,year):

    dftag =(df.Define("jet_mask1", "cleaningMask(Muon_jetIdx[fake_mu],nJet)")
              .Define("jet_mask2", "cleaningMask(Electron_jetIdx[fake_el],nJet)")
              .Define("clean_jet", "Jet_pt > 10 && jet_mask1 && jet_mask2 && Jet_jetId > 0")
              .Define("clean_Jet_pt", "Jet_pt[clean_jet]")
              .Define("clean_Jet_eta", "Jet_eta[clean_jet]")
              .Define("clean_Jet_phi", "Jet_phi[clean_jet]")
              .Define("clean_Jet_mass", "Jet_mass[clean_jet]")
              .Define("clean_Jet_area", "Jet_area[clean_jet]")
              .Define("clean_Jet_rawFactor", "Jet_rawFactor[clean_jet]")
              .Define("clean_Jet_genJetIdx", "Jet_genJetIdx[clean_jet]")
              .Define("clean_Jet_btagCSVV2", "Jet_btagCSVV2[clean_jet]")
              .Define("clean_Jet_btagDeepB", "Jet_btagDeepB[clean_jet]")
              .Define("clean_Jet_btagDeepFlavB", "Jet_btagDeepFlavB[clean_jet]")
              .Define("clean_Jet_muonSubtrFactor", "Jet_muonSubtrFactor[clean_jet]")
              .Define("clean_Jet_chEmEF", "Jet_chEmEF[clean_jet]")
              .Define("clean_Jet_neEmEF", "Jet_neEmEF[clean_jet]")

              #.Define("clean_JetDef_pt",  "compute_JSON_JES_Unc(clean_Jet_pt,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,0)")
              #.Define("clean_JetDef_pt",  "clean_Jet_pt")
              .Define("clean_JetDef_pt"    , "compute_JSON_JER_Unc(clean_Jet_pt,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,0)")
              .Define("clean_Jet_ptJesUp"  , "compute_JSON_JES_Unc(clean_JetDef_pt,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,+1)")
              .Define("clean_Jet_ptJesDown", "compute_JSON_JES_Unc(clean_JetDef_pt,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,-1)")
              .Define("clean_Jet_ptJerUp"  , "compute_JSON_JER_Unc(clean_JetDef_pt,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,+1)")
              .Define("clean_Jet_ptJerDown", "compute_JSON_JER_Unc(clean_JetDef_pt,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,-1)")

              .Define("newMET", "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_Jet_pt,clean_JetDef_pt,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,-1)")
              .Filter("newMET > 0","Good newMET")
       
              .Define("MET_pt_def",     "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_Jet_pt   ,clean_JetDef_pt    ,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,1)")
              .Define("MET_pt_JesUp",   "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_JetDef_pt,clean_Jet_ptJesUp  ,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,1)")
              .Define("MET_pt_JesDown", "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_JetDef_pt,clean_Jet_ptJesDown,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,1)")
              .Define("MET_pt_JerUp",   "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_JetDef_pt,clean_Jet_ptJerUp  ,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,1)")
              .Define("MET_pt_JerDown", "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_JetDef_pt,clean_Jet_ptJerDown,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,1)")
       
              .Define("MET_phi_def",    "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_Jet_pt   ,clean_JetDef_pt    ,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,2)")
              .Define("MET_phi_JesUp",  "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_JetDef_pt,clean_Jet_ptJesUp  ,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,2)")
              .Define("MET_phi_JesDown","compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_JetDef_pt,clean_Jet_ptJesDown,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,2)")
              .Define("MET_phi_JerUp",  "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_JetDef_pt,clean_Jet_ptJerUp  ,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,2)")
              .Define("MET_phi_JerDown","compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_JetDef_pt,clean_Jet_ptJerDown,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,2)")

              .Define("goodbtag_jet", "abs(clean_Jet_eta) < 2.5 && clean_JetDef_pt > 20")
              .Define("goodbtag_Jet_pt", "clean_JetDef_pt[goodbtag_jet]")
              .Define("goodbtag_Jet_eta", "abs(clean_Jet_eta[goodbtag_jet])")
              .Define("goodbtag_Jet_btagDeepB", "clean_Jet_btagDeepB[goodbtag_jet]")

              .Define("good_jet", "abs(clean_Jet_eta) < 5.0 && clean_JetDef_pt > 30")
              .Define("ngood_jets", "Sum(good_jet)")
              .Define("good_Jet_pt", "clean_JetDef_pt[good_jet]")
              .Define("good_Jet_eta", "clean_Jet_eta[good_jet]")
              .Define("good_Jet_phi", "clean_Jet_phi[good_jet]")
              .Define("good_Jet_mass", "clean_Jet_mass[good_jet]")
              .Define("good_Jet_area", "clean_Jet_area[good_jet]")
              .Define("good_Jet_rawFactor", "clean_Jet_rawFactor[good_jet]")
              .Define("good_Jet_btagCSVV2", "clean_Jet_btagCSVV2[good_jet]")
              .Define("good_Jet_btagDeepB", "clean_Jet_btagDeepB[good_jet]")
              .Define("good_Jet_btagDeepFlavB", "clean_Jet_btagDeepFlavB[good_jet]")
              .Define("mjj",	"compute_jet_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, 0)")
              .Define("ptjj",	"compute_jet_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, 1)")
              .Define("detajj", "compute_jet_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, 2)")
              .Define("dphijj", "compute_jet_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, 3)")

              .Define("good_jetJesUp", "abs(clean_Jet_eta) < 5.0 && clean_Jet_ptJesUp > 30")
              .Define("ngood_jetsJesUp", "Sum(good_jetJesUp)")
              .Define("good_Jet_ptJesUp", "clean_Jet_ptJesUp[good_jetJesUp]")
              .Define("good_Jet_etaJesUp", "clean_Jet_eta[good_jetJesUp]")
              .Define("good_Jet_phiJesUp", "clean_Jet_phi[good_jetJesUp]")
              .Define("good_Jet_massJesUp", "clean_Jet_mass[good_jetJesUp]")
              .Define("mjjJesUp", "compute_jet_var(good_Jet_ptJesUp,good_Jet_etaJesUp,good_Jet_phiJesUp,good_Jet_massJesUp,0)")

              .Define("good_jetJesDown", "abs(clean_Jet_eta) < 5.0 && clean_Jet_ptJesDown > 30")
              .Define("ngood_jetsJesDown", "Sum(good_jetJesDown)")
              .Define("good_Jet_ptJesDown", "clean_Jet_ptJesDown[good_jetJesDown]")
              .Define("good_Jet_etaJesDown", "clean_Jet_eta[good_jetJesDown]")
              .Define("good_Jet_phiJesDown", "clean_Jet_phi[good_jetJesDown]")
              .Define("good_Jet_massJesDown", "clean_Jet_mass[good_jetJesDown]")
              .Define("mjjJesDown", "compute_jet_var(good_Jet_ptJesDown,good_Jet_etaJesDown,good_Jet_phiJesDown,good_Jet_massJesDown,0)")

              .Define("good_jetJerUp", "abs(clean_Jet_eta) < 5.0 && clean_Jet_ptJerUp > 30")
              .Define("ngood_jetsJerUp", "Sum(good_jetJerUp)")
              .Define("good_Jet_ptJerUp", "clean_Jet_ptJerUp[good_jetJerUp]")
              .Define("good_Jet_etaJerUp", "clean_Jet_eta[good_jetJerUp]")
              .Define("good_Jet_phiJerUp", "clean_Jet_phi[good_jetJerUp]")
              .Define("good_Jet_massJerUp", "clean_Jet_mass[good_jetJerUp]")
              .Define("mjjJerUp", "compute_jet_var(good_Jet_ptJerUp,good_Jet_etaJerUp,good_Jet_phiJerUp,good_Jet_massJerUp,0)")

              .Define("good_jetJerDown", "abs(clean_Jet_eta) < 5.0 && clean_Jet_ptJerDown > 30")
              .Define("ngood_jetsJerDown", "Sum(good_jetJerDown)")
              .Define("good_Jet_ptJerDown", "clean_Jet_ptJerDown[good_jetJerDown]")
              .Define("good_Jet_etaJerDown", "clean_Jet_eta[good_jetJerDown]")
              .Define("good_Jet_phiJerDown", "clean_Jet_phi[good_jetJerDown]")
              .Define("good_Jet_massJerDown", "clean_Jet_mass[good_jetJerDown]")
              .Define("mjjJerDown", "compute_jet_var(good_Jet_ptJerDown,good_Jet_etaJerDown,good_Jet_phiJerDown,good_Jet_massJerDown,0)")
              )

    return dftag

def selection3LVar(df,year):

    dftag =(df.Define("TriLepton_flavor", "(Sum(fake_mu)+3*Sum(fake_el)-3)/2")
              .Define("m3l",    "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 0)")
              .Define("mllmin", "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 1)")
              .Define("drllmin","compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 2)")
              .Define("ptl1",   "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 3)")
              .Define("ptl2",   "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 4)")
              .Define("ptl3",   "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 5)")
              .Define("mll",    "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 6)")
              .Define("ptl1Z",  "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 7)")
              .Define("ptl2Z",  "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 8)")
              .Define("ptlW",   "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 9)")
              .Define("mtW",    "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,10)")
              .Filter("ptl1 > 25 && ptl2 > 20","ptl1 > 25 && ptl2 > 20")
              .Define("mllZ",  "abs(mll-91.1876)")
              )

    return dftag

def selection2LVar(df,year):

    dftag =(df.Define("mll",    "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,0)")
              .Define("ptll",   "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,1)")
              .Define("drll",   "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,2)")
              .Define("dphill", "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,3)")
              .Define("ptl1",   "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,4)")
              .Define("ptl2",   "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,5)")
              .Define("etal1",  "abs(compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,6))")
              .Define("etal2",  "abs(compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,7))")
              .Define("DiLepton_flavor", "Sum(fake_mu)+2*Sum(fake_el)-2")

              .Define("muid1",  "compute_muid_var(fake_Muon_mediumId, fake_Muon_tightId, fake_Muon_pfIsoId, fake_Muon_mvaId, fake_Muon_miniIsoId, fake_Muon_mvaTTH, 0)")
              .Define("muid2",  "compute_muid_var(fake_Muon_mediumId, fake_Muon_tightId, fake_Muon_pfIsoId, fake_Muon_mvaId, fake_Muon_miniIsoId, fake_Muon_mvaTTH, 1)")
              .Define("elid1",  "compute_elid_var(fake_Electron_cutBased, fake_Electron_mvaIso_Fall17V2_WP90, fake_Electron_mvaIso_Fall17V2_WP80, fake_Electron_tightCharge, fake_Electron_mvaTTH, 0)")
              .Define("elid2",  "compute_elid_var(fake_Electron_cutBased, fake_Electron_mvaIso_Fall17V2_WP90, fake_Electron_mvaIso_Fall17V2_WP80, fake_Electron_tightCharge, fake_Electron_mvaTTH, 1)")

              .Define("ltype",  "compute_nl_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,2)")
              )

    return dftag

def selectionTrigger2L(df,year,PDType,JSON,isData,triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG):

    triggerLEP = "{0} or {1} or {2} or {3} or {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)

    if(year == 2018 and PDType == "MuonEG"):
        triggerLEP = "{0}".format(triggerMUEG)
    elif(year == 2018 and PDType == "DoubleMuon"):
        triggerLEP = "{0} and not {1}".format(triggerDMU,triggerMUEG)
    elif(year == 2018 and PDType == "SingleMuon"):
        triggerLEP = "{0} and not {1} and not {2}".format(triggerSMU,triggerDMU,triggerMUEG)
    elif(year == 2018 and PDType == "EGamma"):
        triggerLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)
    elif(year == 2018):
        triggerLEP = "{0} or {1} or {2} or {3} or {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)
    elif(year == 2022 and PDType == "MuonEG"):
        triggerLEP = "{0}".format(triggerMUEG)
    elif(year == 2022 and PDType == "Muon"):
        triggerLEP = "({0} or {1}) and not {1}".format(triggerDMU,triggerSMU,triggerMUEG)
    elif(year == 2022 and PDType == "EGamma"):
        triggerLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)
    elif(year == 2022):
        triggerLEP = "{0} or {1} or {2} or {3} or {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)
    else:
        print("PROBLEM with triggers!!!")

    print("triggerLEP: {0}".format(triggerLEP))

    dftag =(df.Define("isData","{}".format(isData))
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")
              .Define("trigger","{0}".format(triggerLEP))
              .Filter("trigger > 0","Passed trigger")
              )

    return dftag

def selectionElMu(df,year,fake_mu,tight_mu,fake_el,tight_el):
    dftag =(df.Define("loose_mu"           ,"abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")
              .Define("fake_mu"            ,"{0}".format(fake_mu))
              .Define("fake_Muon_pt"       ,"Muon_pt[fake_mu]")
              .Define("fake_Muon_eta"      ,"Muon_eta[fake_mu]")
              .Define("fake_Muon_phi"      ,"Muon_phi[fake_mu]")
              .Define("fake_Muon_dxy"      ,"Muon_dxy[fake_mu]")
              .Define("fake_Muon_dz"       ,"Muon_dz[fake_mu]")
              .Define("fake_Muon_mass"     ,"Muon_mass[fake_mu]")
              .Define("fake_Muon_charge"   ,"Muon_charge[fake_mu]")
              .Define("fake_Muon_looseId"  ,"Muon_looseId[fake_mu]")
              .Define("fake_Muon_mediumId" ,"Muon_mediumId[fake_mu]")
              .Define("fake_Muon_tightId"  ,"Muon_tightId[fake_mu]")
              .Define("fake_Muon_pfIsoId"  ,"Muon_pfIsoId[fake_mu]")
              .Define("fake_Muon_mvaId"    ,"Muon_mvaId[fake_mu]")
              .Define("fake_Muon_miniIsoId","Muon_miniIsoId[fake_mu]")
              .Define("fake_Muon_mvaTTH"   ,"Muon_mvaTTH[fake_mu]")
              .Define("tight_mu"           ,"{0}".format(tight_mu))

              .Define("loose_el"                          ,"abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")
              .Define("fake_el"                           ,"{0}".format(fake_el))
              .Define("fake_Electron_pt"                  ,"Electron_pt[fake_el]")
              .Define("fake_Electron_eta"                 ,"Electron_eta[fake_el]")
              .Define("fake_Electron_phi"                 ,"Electron_phi[fake_el]")
              .Define("fake_Electron_mass"                ,"Electron_mass[fake_el]")
              .Define("fake_Electron_charge"              ,"Electron_charge[fake_el]")
              .Define("fake_Electron_dxy"                 ,"Electron_dxy[fake_el]")
              .Define("fake_Electron_dz"                  ,"Electron_dz[fake_el]")
              .Define("fake_Electron_cutBased"            ,"Electron_cutBased[fake_el]")
              .Define("fake_Electron_mvaIso_Fall17V2_WP90","Electron_mvaIso_Fall17V2_WP90[fake_el]")
              .Define("fake_Electron_mvaIso_Fall17V2_WP80","Electron_mvaIso_Fall17V2_WP80[fake_el]")
              .Define("fake_Electron_tightCharge"         ,"Electron_tightCharge[fake_el]")
              .Define("fake_Electron_mvaTTH"              ,"Electron_mvaTTH[fake_el]")
              .Define("tight_el"                          ,"{0}".format(tight_el))

              .Define("nLoose","Sum(loose_mu)+Sum(loose_el)")
              .Define("nFake","Sum(fake_mu)+Sum(fake_el)")
              .Define("nTight","Sum(tight_mu)+Sum(tight_el)")
              )

    return dftag

def selectionMCWeigths(df,year,PDType,weight):

    MUOYEAR = "2018_UL"
    #if(year == 2022): MUOYEAR = "2022"
    ELEYEAR = "2018"
    #if(year == 2022): ELEYEAR = "2022"
    PHOYEAR = "2018"
    #if(year == 2022): PHOYEAR = "2022"

    dftag =(df.Define("PDType","\"{0}\"".format(PDType))
              .Define("clean_Jet_hadronFlavour", "Jet_btagDeepFlavB[clean_jet]")
              .Define("goodbtag_Jet_hadronFlavour","clean_Jet_hadronFlavour[goodbtag_jet]")
              .Define("fake_Muon_genPartFlav","Muon_genPartFlav[fake_mu]")
              .Define("fake_Electron_genPartFlav","Electron_genPartFlav[fake_el]")
              .Define("weightPURecoSF","compute_PURecoSF(fake_Muon_pt,fake_Muon_eta,fake_Muon_pt,fake_Muon_eta,Pileup_nTrueInt)")
              .Filter("weightPURecoSF > 0","good PURecoSF weight")
              .Define("weightTriggerSF","compute_TriggerSF(ptl1,ptl2,etal1,etal2,ltype)")
              .Filter("weightTriggerSF > 0","good TriggerSF weight")

              .Define("MUOYEAR","\"{0}\"".format(MUOYEAR))
              .Define("ELEYEAR","\"{0}\"".format(ELEYEAR))
              .Define("PHOYEAR","\"{0}\"".format(PHOYEAR))
              .Define("MUOWP","\"Medium\"")
              .Define("ELEWP","\"Medium\"")
              .Define("PHOWP","\"Medium\"")
              .Define("weightBtagSFJSON","compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepB,goodbtag_Jet_hadronFlavour,0)")
              .Filter("weightBtagSFJSON > 0","weightBtagSFJSON > 0")
              .Define("weightMuoSFJSON","compute_JSON_MUO_SFs(MUOYEAR,\"sf\",MUOWP,fake_Muon_pt,fake_Muon_eta)")
              .Filter("weightMuoSFJSON > 0","weightMuoSFJSON > 0")
              .Define("weightEleSFJSON","compute_JSON_ELE_SFs(ELEYEAR,\"sf\",ELEWP,fake_Electron_pt,fake_Electron_eta)")
              .Filter("weightEleSFJSON > 0","weightEleSFJSON > 0")
              .Define("weightPhoSFJSON","compute_JSON_PHO_SFs(PHOYEAR,\"sf\",PHOWP,good_Photons_pt,good_Photons_eta)")
              .Filter("weightPhoSFJSON > 0","weightPhoSFJSON > 0")
              .Define("weightTauSFJSON","compute_JSON_TAU_SFs(good_Tau_pt,good_Tau_eta,good_Tau_decayMode,good_Tau_genPartFlav,\"nom\")")
              .Filter("weightTauSFJSON > 0","weightTauSFJSON > 0")
              .Define("weightPUSF_Nom","compute_JSON_PU_SF(Pileup_nTrueInt,\"nominal\")")
              .Filter("weightPUSF_Nom > 0","weightPUSF_Nom > 0")

              .Define("weightMC","compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,0)".format(weight))
              .Filter("weightMC != 0","MC weight")
              .Define("weight","weightMC")
              )

    return dftag

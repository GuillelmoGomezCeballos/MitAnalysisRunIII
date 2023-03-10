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

def makeJES(df,year,postFix):
    postFitDef = postFix
    postFitMet = "Def"
    if(postFix == ""):
        postFitDef = "Def"
        postFitMet = ""

    dftag =(df.Define("good_jet{0}".format(postFix), "abs(clean_Jet_eta) < 5.0 && clean_Jet_pt{0} > 30".format(postFitDef))
              .Define("ngood_jets{0}".format(postFix), "Sum(good_jet{0})*1.0f".format(postFix))
              .Define("good_Jet_pt{0}".format(postFix), "clean_Jet_pt{0}[good_jet{1}]".format(postFitDef,postFix))
              .Define("good_Jet_eta{0}".format(postFix), "clean_Jet_eta[good_jet{0}]".format(postFix))
              .Define("good_Jet_phi{0}".format(postFix), "clean_Jet_phi[good_jet{0}]".format(postFix))
              .Define("good_Jet_mass{0}".format(postFix), "clean_Jet_mass[good_jet{0}]".format(postFix))
              .Define("good_Jet_area{0}".format(postFix), "clean_Jet_area[good_jet{0}]".format(postFix))
              .Define("good_Jet_rawFactor{0}".format(postFix), "clean_Jet_rawFactor[good_jet{0}]".format(postFix))
              .Define("good_Jet_btagCSVV2{0}".format(postFix), "clean_Jet_btagCSVV2[good_jet{0}]".format(postFix))
              .Define("good_Jet_btagDeepB{0}".format(postFix), "clean_Jet_btagDeepB[good_jet{0}]".format(postFix))
              .Define("good_Jet_btagDeepFlavB{0}".format(postFix), "clean_Jet_btagDeepFlavB[good_jet{0}]".format(postFix))

              .Define("mjj{0}".format(postFix),	  "compute_jet_var(good_Jet_pt{0}, good_Jet_eta, good_Jet_phi, good_Jet_mass, 0)".format(postFix))
              .Define("ptjj{0}".format(postFix),  "compute_jet_var(good_Jet_pt{0}, good_Jet_eta, good_Jet_phi, good_Jet_mass, 1)".format(postFix))
              .Define("detajj{0}".format(postFix),"compute_jet_var(good_Jet_pt{0}, good_Jet_eta, good_Jet_phi, good_Jet_mass, 2)".format(postFix))
              .Define("dphijj{0}".format(postFix),"compute_jet_var(good_Jet_pt{0}, good_Jet_eta, good_Jet_phi, good_Jet_mass, 3)".format(postFix))
              .Define("ptj1{0}".format(postFix),  "compute_jet_var(good_Jet_pt{0}, good_Jet_eta, good_Jet_phi, good_Jet_mass, 4)".format(postFix))
              .Define("ptj2{0}".format(postFix),  "compute_jet_var(good_Jet_pt{0}, good_Jet_eta, good_Jet_phi, good_Jet_mass, 5)".format(postFix))
              .Define("etaj1{0}".format(postFix), "compute_jet_var(good_Jet_pt{0}, good_Jet_eta, good_Jet_phi, good_Jet_mass, 6)".format(postFix))
              .Define("etaj2{0}".format(postFix), "compute_jet_var(good_Jet_pt{0}, good_Jet_eta, good_Jet_phi, good_Jet_mass, 7)".format(postFix))

              .Define("goodbtag_jet{0}".format(postFix), "abs(clean_Jet_eta) < 2.5 && clean_Jet_pt{0} > 20".format(postFitDef))
              .Define("goodbtag_Jet_pt{0}".format(postFix), "clean_Jet_pt{0}[goodbtag_jet{1}]".format(postFitDef,postFix))
              .Define("goodbtag_Jet_eta{0}".format(postFix), "abs(clean_Jet_eta[goodbtag_jet{0}])".format(postFix))
              .Define("goodbtag_Jet_btagDeepB{0}".format(postFix), "clean_Jet_btagDeepB[goodbtag_jet{0}]".format(postFix))
              .Define("goodbtag_Jet_bjet{0}".format(postFix), "goodbtag_Jet_btagDeepB{0} > 0.7100".format(postFix))
              .Define("nbtag_goodbtag_Jet_bjet{0}".format(postFix), "Sum(goodbtag_Jet_bjet{0})*1.0f".format(postFix))

              .Define("vbs_jet{0}".format(postFix), "abs(clean_Jet_eta) < 5.0 && clean_Jet_pt{0} > 50".format(postFitDef))
              .Define("nvbs_jets{0}".format(postFix), "Sum(vbs_jet{0})*1.0f".format(postFix))
              .Define("vbs_Jet_pt{0}".format(postFix), "clean_Jet_pt{0}[vbs_jet{1}]".format(postFitDef,postFix))
              .Define("vbs_Jet_eta{0}".format(postFix), "clean_Jet_eta[vbs_jet{0}]".format(postFix))
              .Define("vbs_Jet_phi{0}".format(postFix), "clean_Jet_phi[vbs_jet{0}]".format(postFix))
              .Define("vbs_Jet_mass{0}".format(postFix), "clean_Jet_mass[vbs_jet{0}]".format(postFix))

              .Define("vbs_mjj{0}".format(postFix),   "compute_jet_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, 0)".format(postFix))
              .Define("vbs_ptjj{0}".format(postFix),  "compute_jet_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, 1)".format(postFix))
              .Define("vbs_detajj{0}".format(postFix),"compute_jet_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, 2)".format(postFix))
              .Define("vbs_dphijj{0}".format(postFix),"compute_jet_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, 3)".format(postFix))
              .Define("vbs_ptj1{0}".format(postFix),  "compute_jet_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, 4)".format(postFix))
              .Define("vbs_ptj2{0}".format(postFix),  "compute_jet_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, 5)".format(postFix))
              .Define("vbs_etaj1{0}".format(postFix), "compute_jet_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, 6)".format(postFix))
              .Define("vbs_etaj2{0}".format(postFix), "compute_jet_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, 7)".format(postFix))

              .Define("MET_pt{0}".format(postFitDef), "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_Jet_pt{0},clean_Jet_pt{1},clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,1)".format(postFitMet,postFitDef))
              .Define("MET_phi{0}".format(postFitDef),"compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_Jet_pt{0},clean_Jet_pt{1},clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,2)".format(postFitMet,postFitDef))

              .Define("vbs_zepvv{0}".format(postFix),    "compute_jet_lepton_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, MET_pt{1}, MET_phi{2}, 0)".format(postFix,postFix,postFix))
              .Define("vbs_zepmax{0}".format(postFix),   "compute_jet_lepton_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, MET_pt{1}, MET_phi{2}, 1)".format(postFix,postFix,postFix))
              .Define("vbs_sumHT{0}".format(postFix),    "compute_jet_lepton_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, MET_pt{1}, MET_phi{2}, 2)".format(postFix,postFix,postFix))
              .Define("vbs_ptvv{0}".format(postFix),     "compute_jet_lepton_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, MET_pt{1}, MET_phi{2}, 3)".format(postFix,postFix,postFix))
              .Define("vbs_pttot{0}".format(postFix),    "compute_jet_lepton_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, MET_pt{1}, MET_phi{2}, 4)".format(postFix,postFix,postFix))
              .Define("vbs_detavvj1{0}".format(postFix), "compute_jet_lepton_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, MET_pt{1}, MET_phi{2}, 5)".format(postFix,postFix,postFix))
              .Define("vbs_detavvj2{0}".format(postFix), "compute_jet_lepton_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, MET_pt{1}, MET_phi{2}, 6)".format(postFix,postFix,postFix))
              .Define("vbs_ptbalance{0}".format(postFix),"compute_jet_lepton_var(vbs_Jet_pt{0}, vbs_Jet_eta, vbs_Jet_phi, vbs_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, MET_pt{1}, MET_phi{2}, 7)".format(postFix,postFix,postFix))
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

              #.Define("clean_Jet_ptDef",  "compute_JSON_JES_Unc(clean_Jet_pt,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,0)")
              #.Define("clean_Jet_ptDef",  "clean_Jet_pt")
              .Define("clean_Jet_ptDef"    , "compute_JSON_JER_Unc(clean_Jet_pt,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,0)")
              .Define("clean_Jet_ptJesUp"  , "compute_JSON_JES_Unc(clean_Jet_ptDef,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,+1)")
              .Define("clean_Jet_ptJesDown", "compute_JSON_JES_Unc(clean_Jet_ptDef,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,-1)")
              .Define("clean_Jet_ptJerUp"  , "compute_JSON_JER_Unc(clean_Jet_ptDef,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,+1)")
              .Define("clean_Jet_ptJerDown", "compute_JSON_JER_Unc(clean_Jet_ptDef,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,-1)")

              .Define("newMET", "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_Jet_pt,clean_Jet_ptDef,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,-1)")
              .Filter("newMET > 0","Good newMET")
              )

    dftag = makeJES(dftag,year,"")
    dftag = makeJES(dftag,year,"JesUp"  )
    dftag = makeJES(dftag,year,"JesDown")
    dftag = makeJES(dftag,year,"JerUp"  )
    dftag = makeJES(dftag,year,"JerDown")

    return dftag

def selection4LVar(df,year):

    dftag =(df.Define("FourLepton_flavor", "(Sum(fake_mu)+4*Sum(fake_el)-4)/6")
              .Define("m4l",   "compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 0)")
              .Define("ptlmax","compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 1)")
              .Filter("ptlmax > 25","ptl > 25 for one of the leptons")
              .Define("mllmin","compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 2)")
              .Define("mllZ1", "compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 3)")
              .Define("mllZ2", "compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 4)")
              .Define("ptl1Z1","compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 5)")
              .Define("ptl2Z1","compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 6)")
              .Define("ptl1Z2","compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 7)")
              .Define("ptl2Z2","compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 8)")
              .Define("mllxy", "compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 9)")
              .Define("ptZ1",  "compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,10)")
              .Define("ptZ2",  "compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,11)")
              .Define("mtxy",  "compute_4l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,12)")
              .Define("ltype", "compute_nl_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,2)")
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
              .Define("etal1",  "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 6)")
              .Define("etal2",  "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 7)")
              .Define("etal3",  "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 8)")
              .Define("mll",    "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi, 9)")
              .Define("ptl1Z",  "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,10)")
              .Define("ptl2Z",  "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,11)")
              .Define("ptlW",   "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,12)")
              .Define("mtW",    "compute_3l_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,13)")
              .Filter("ptl1 > 25 && ptl2 > 20","ptl1 > 25 && ptl2 > 20")
              .Define("mllZ",  "abs(mll-91.1876)")
              .Define("ltype",  "compute_nl_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, MET_pt, MET_phi,2)")
              )

    return dftag

def selection2LVar(df,year):

    dftag =(df.Define("mll",    "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,0)")
              .Define("ptll",   "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,1)")
              .Define("drll",   "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,2)")
              .Define("dphill", "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,3)")
              .Define("ptl1",   "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,4)")
              .Define("ptl2",   "compute_ll_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,5)")
              .Define("ptl3",   "0.0f")
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

def selectionMCWeigths(df,year,PDType,weight,type):

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

              .Define("weightMC","compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})".format(weight,type))
              .Filter("weightMC != 0","MC weight")
              .Define("weight","weightMC")
              )

    return dftag

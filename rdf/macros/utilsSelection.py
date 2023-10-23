import ROOT
import os, json
from utilsCategory import plotCategory

def getBTagCut(type,year):

    if(type < 0 or type > 2): return 100
    value = [0.7100, 0.2783, 0.0490]
    if(year == 20220):
       value[0] = 0.7183
       value[1] = 0.3086
       value[2] = 0.0583
    elif(year == 20221):
       value[0] = 0.7300
       value[1] = 0.3196
       value[2] = 0.0614

    return value[type]

def selectionGenLepJet(df,ptlcut,ptjcut):

    dftag =(df.Define("good_GenDressedLepton", "abs(GenDressedLepton_eta) < 2.5 && GenDressedLepton_pt > {0}".format(ptlcut))
              .Define("good_GenDressedLepton_pt", "GenDressedLepton_pt[good_GenDressedLepton]")
              .Define("good_GenDressedLepton_eta", "GenDressedLepton_eta[good_GenDressedLepton]")
              .Define("good_GenDressedLepton_phi", "GenDressedLepton_phi[good_GenDressedLepton]")
              .Define("GenJet_mask", "cleaningJetFromLepton(GenJet_eta,GenJet_phi,good_GenDressedLepton_eta,good_GenDressedLepton_phi)")
              .Define("good_GenJet", "GenJet_pt > {0} && abs(GenJet_eta) < 5.0 && GenJet_mask > 0".format(ptjcut))
              .Define("ngood_GenJets","Sum(good_GenJet)*1.0f")
              .Define("good_GenJet_pt",            "GenJet_pt[good_GenJet]")
              .Define("good_GenJet_eta",           "GenJet_eta[good_GenJet]")
              .Define("good_GenJet_phi",           "GenJet_phi[good_GenJet]")
              .Define("good_GenJet_hadronFlavour", "GenJet_hadronFlavour[good_GenJet]")
              .Define("good_GenJet_partonFlavour", "GenJet_partonFlavour[good_GenJet]")
              )

    return dftag

def selectionTauVeto(df,year,isData):

    dftag =(df.Define("good_tau", "abs(Tau_eta) < 2.3 && Tau_pt > 20 && Tau_idDeepTau2018v2p5VSjet >= 6 && Tau_idDeepTau2018v2p5VSe >= 6 && Tau_idDeepTau2018v2p5VSmu >= 4")
              .Filter("Sum(good_tau) == 0","No selected hadronic taus")
              .Define("good_Tau_pt", "Tau_pt[good_tau]")
              .Define("good_Tau_eta", "Tau_eta[good_tau]")
              .Define("good_Tau_decayMode", "Tau_decayMode[good_tau]")
              )

    if(isData == "false"):
        dftag = dftag.Define("good_Tau_genPartFlav", "Tau_genPartFlav[good_tau]")

    return dftag

def selectionPhoton(df,year,BARRELphotons,ENDCAPphotons):

    dftag =(df.Define("photon_mask", "cleaningMask(Electron_photonIdx[fake_el],nPhoton)")
              .Define("good_Photons", "{}".format(BARRELphotons)+" or {}".format(ENDCAPphotons) )
              .Define("good_Photons_pt", "Photon_pt[good_Photons]")
              .Define("good_Photons_eta", "Photon_eta[good_Photons]")
              .Define("good_Photons_phi", "Photon_phi[good_Photons]")
              )

    return dftag

def makeJES(df,year,postFix,bTagSel):
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
             #.Define("good_Jet_btagDeepB{0}".format(postFix), "clean_Jet_btagDeepB[good_jet{0}]".format(postFix))
              .Define("good_Jet_btagDeepFlavB{0}".format(postFix), "clean_Jet_btagDeepFlavB[good_jet{0}]".format(postFix))
              .Define("good_Jet_chEmEF{0}".format(postFix), "clean_Jet_chEmEF[good_jet{0}]".format(postFix))
              .Define("good_Jet_neEmEF{0}".format(postFix), "clean_Jet_neEmEF[good_jet{0}]".format(postFix))
              .Define("good_Jet_chHEF{0}".format(postFix), "clean_Jet_chHEF[good_jet{0}]".format(postFix))
              .Define("good_Jet_neHEF{0}".format(postFix), "clean_Jet_neHEF[good_jet{0}]".format(postFix))

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
              .Define("goodbtag_Jet_phi{0}".format(postFix), "abs(clean_Jet_phi[goodbtag_jet{0}])".format(postFix))
              .Define("goodbtag_Jet_btagDeepFlavB{0}".format(postFix), "clean_Jet_btagDeepFlavB[goodbtag_jet{0}]".format(postFix))
              .Define("goodbtag_Jet_bjet{0}".format(postFix), "goodbtag_Jet_btagDeepFlavB{0} > {1}".format(postFix,getBTagCut(bTagSel,year)))
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

def selectionJetMet(df,year,bTagSel,isData,count):

    jetTypeCorr = -1
    if(count > 1000): jetTypeCorr = count%10
    print("jetTypeCorr: {0}".format(jetTypeCorr))

    dftag =(df.Define("jet_mask1", "cleaningMask(Muon_jetIdx[fake_mu],nJet)")
              .Define("jet_mask2", "cleaningMask(Electron_jetIdx[fake_el],nJet)")
              .Define("jet_VetoMapMask", "cleaningJetVetoMapMask(Jet_eta,Jet_phi,{0})".format(jetTypeCorr))
              .Define("clean_jet", "Jet_pt > 10 && jet_mask1 && jet_mask2 && jet_VetoMapMask > 0 && Jet_jetId > 0")
              .Define("clean_Jet_pt", "Jet_pt[clean_jet]")
              .Define("clean_Jet_eta", "Jet_eta[clean_jet]")
              .Define("clean_Jet_phi", "Jet_phi[clean_jet]")
              .Define("clean_Jet_mass", "Jet_mass[clean_jet]")
              .Define("clean_Jet_area", "Jet_area[clean_jet]")
              .Define("clean_Jet_rawFactor", "Jet_rawFactor[clean_jet]")
             #.Define("clean_Jet_btagDeepB", "Jet_btagDeepB[clean_jet]")
              .Define("clean_Jet_btagDeepFlavB", "Jet_btagDeepFlavB[clean_jet]")
              .Define("clean_Jet_muonSubtrFactor", "Jet_muonSubtrFactor[clean_jet]")
              .Define("clean_Jet_chEmEF", "Jet_chEmEF[clean_jet]")
              .Define("clean_Jet_neEmEF", "Jet_neEmEF[clean_jet]")
              .Define("clean_Jet_chHEF",  "Jet_chHEF[clean_jet]")
              .Define("clean_Jet_neHEF",  "Jet_neHEF[clean_jet]")
              )

    if(isData == "false"):
        dftag =(dftag.Define("clean_Jet_genJetIdx", "Jet_genJetIdx[clean_jet]")
                     .Define("clean_Jet_ptDef",  "compute_JSON_JES_Unc(clean_Jet_pt,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,0,-1)")
                     #.Define("clean_Jet_ptDef",  "clean_Jet_pt")
                     #.Define("clean_Jet_ptDef"    , "compute_JSON_JER_Unc(clean_Jet_pt,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,0,{0})".format(jetTypeCorr))
                     .Define("clean_Jet_ptJesUp"  , "compute_JSON_JES_Unc(clean_Jet_ptDef,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,+1,{0})".format(jetTypeCorr))
                     .Define("clean_Jet_ptJesDown", "compute_JSON_JES_Unc(clean_Jet_ptDef,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,-1,{0})".format(jetTypeCorr))
                     .Define("clean_Jet_ptJerUp"  , "compute_JSON_JER_Unc(clean_Jet_ptDef,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,+1)")
                     .Define("clean_Jet_ptJerDown", "compute_JSON_JER_Unc(clean_Jet_ptDef,clean_Jet_eta,clean_Jet_genJetIdx,GenJet_pt,Rho_fixedGridRhoFastjetAll,-1)")
                     .Define("newMET", "compute_JSON_MET_Unc(MET_pt,MET_phi,RawMET_pt,RawMET_phi,clean_Jet_chEmEF,clean_Jet_neEmEF,clean_Jet_muonSubtrFactor,clean_Jet_rawFactor,clean_Jet_pt,clean_Jet_ptDef,clean_Jet_eta,clean_Jet_phi,clean_Jet_mass,-1)")
                     .Filter("newMET > 0","Good newMET")
                     )

    else:
        #dftag =(dftag.Define("clean_Jet_ptDef","clean_Jet_pt")
        dftag =(dftag.Define("clean_Jet_ptDef",  "compute_JSON_JES_Unc(clean_Jet_pt,clean_Jet_eta,clean_Jet_rawFactor,clean_Jet_area,Rho_fixedGridRhoFastjetAll,0,{0})".format(jetTypeCorr))
                     .Define("clean_Jet_ptJesUp"  , "clean_Jet_ptDef")
                     .Define("clean_Jet_ptJesDown", "clean_Jet_ptDef")
                     .Define("clean_Jet_ptJerUp"  , "clean_Jet_ptDef")
                     .Define("clean_Jet_ptJerDown", "clean_Jet_ptDef")
                     )

    dftag = makeJES(dftag,year,""       ,bTagSel)
    dftag = makeJES(dftag,year,"JesUp"  ,bTagSel)
    dftag = makeJES(dftag,year,"JesDown",bTagSel)
    dftag = makeJES(dftag,year,"JerUp"  ,bTagSel)
    dftag = makeJES(dftag,year,"JerDown",bTagSel)

    return dftag

def makeLGVar(df,postFixMu,postFixEl,postFixPh):

    postFix = ""
    if(postFixMu != ""):
        postFix = postFixMu
    elif(postFixEl != ""):
        postFix = postFixEl
    elif(postFixPh != ""):
        postFix = postFixPh

    dftag =(df.Define("ptbalance{0}".format(postFix), "compute_met_lepton_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, 0)".format(postFixMu,postFixEl))
              .Define("ptjbalance{0}".format(postFix),"compute_met_lepton_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, 1)".format(postFixMu,postFixEl))
              .Define("dphillmet{0}".format(postFix), "compute_met_lepton_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, 2)".format(postFixMu,postFixEl))
              .Define("dphilljmet{0}".format(postFix),"compute_met_lepton_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, 3)".format(postFixMu,postFixEl))
              .Define("mt{0}".format(postFix),        "compute_met_lepton_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, 4)".format(postFixMu,postFixEl))
              .Define("jetPtFrac{0}".format(postFix), "compute_met_lepton_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, 5)".format(postFixMu,postFixEl))
              .Define("dphijmet{0}".format(postFix),  "compute_met_lepton_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, 6)".format(postFixMu,postFixEl))
              .Define("ptgbalance{0}".format(postFix), "compute_met_lepton_gamma_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, good_Photons_pt{2}, good_Photons_eta, good_Photons_phi, 0)".format(postFixMu,postFixEl,postFixPh))
              .Define("ptgjbalance{0}".format(postFix),"compute_met_lepton_gamma_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, good_Photons_pt{2}, good_Photons_eta, good_Photons_phi, 1)".format(postFixMu,postFixEl,postFixPh))
              .Define("dphillgmet{0}".format(postFix), "compute_met_lepton_gamma_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, good_Photons_pt{2}, good_Photons_eta, good_Photons_phi, 2)".format(postFixMu,postFixEl,postFixPh))
              .Define("dphillgjmet{0}".format(postFix),"compute_met_lepton_gamma_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, good_Photons_pt{2}, good_Photons_eta, good_Photons_phi, 3)".format(postFixMu,postFixEl,postFixPh))
              .Define("mtg{0}".format(postFix),        "compute_met_lepton_gamma_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, good_Photons_pt{2}, good_Photons_eta, good_Photons_phi, 4)".format(postFixMu,postFixEl,postFixPh))
              .Define("jetPtgFrac{0}".format(postFix), "compute_met_lepton_gamma_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, PuppiMET_pt, PuppiMET_phi, good_Photons_pt{2}, good_Photons_eta, good_Photons_phi, 5)".format(postFixMu,postFixEl,postFixPh))
	      )

    return dftag

def selectionLGVar(df,year,isData):

    if(isData == "false"):
        dftag =(df.Define("good_Photons_ptPhotonMomUp"  , "compute_PHOPT_Unc(good_Photons_pt,+1)")
                  .Define("good_Photons_ptPhotonMomDown", "compute_PHOPT_Unc(good_Photons_pt,-1)")
                  )
    else:
        dftag =(df.Define("good_Photons_ptPhotonMomUp"  , "good_Photons_pt")
                  .Define("good_Photons_ptPhotonMomDown", "good_Photons_pt")
                  )

    dftag = makeLGVar(dftag,""            ,""              ,"")
    dftag = makeLGVar(dftag,"MuonMomUp"  ,""               ,"")
    dftag = makeLGVar(dftag,"MuonMomDown",""               ,"")
    dftag = makeLGVar(dftag,""           ,"ElectronMomUp"  ,"")
    dftag = makeLGVar(dftag,""           ,"ElectronMomDown","")
    dftag = makeLGVar(dftag,""            ,""              ,"PhotonMomUp")
    dftag = makeLGVar(dftag,""            ,""              ,"PhotonMomDown")

    return dftag


def make4LVar(df,postFixMu,postFixEl):

    postFix = ""
    if(postFixMu != ""):
        postFix = postFixMu
    elif(postFixEl != ""):
        postFix = postFixEl

    dftag =(df.Define("m4l{0}".format(postFix),   "compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 0)".format(postFixMu,postFixEl))
              .Define("ptlmax{0}".format(postFix),"compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 1)".format(postFixMu,postFixEl))
              .Define("mllmin{0}".format(postFix),"compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 2)".format(postFixMu,postFixEl))
              .Define("mllZ1{0}".format(postFix), "compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 3)".format(postFixMu,postFixEl))
              .Define("mllZ2{0}".format(postFix), "compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 4)".format(postFixMu,postFixEl))
              .Define("ptl1Z1{0}".format(postFix),"compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 5)".format(postFixMu,postFixEl))
              .Define("ptl2Z1{0}".format(postFix),"compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 6)".format(postFixMu,postFixEl))
              .Define("ptl1Z2{0}".format(postFix),"compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 7)".format(postFixMu,postFixEl))
              .Define("ptl2Z2{0}".format(postFix),"compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 8)".format(postFixMu,postFixEl))
              .Define("mllxy{0}".format(postFix), "compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 9)".format(postFixMu,postFixEl))
              .Define("ptZ1{0}".format(postFix),  "compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,10)".format(postFixMu,postFixEl))
              .Define("ptZ2{0}".format(postFix),  "compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,11)".format(postFixMu,postFixEl))
              .Define("mtxy{0}".format(postFix),  "compute_4l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,12)".format(postFixMu,postFixEl))
              .Define("ltype{0}".format(postFix), "compute_nl_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,2)".format(postFixMu,postFixEl))
	      )

    return dftag

def selection4LVar(df,year,isData):

    if(isData == "false"):
        dftag =(df.Define("FourLepton_flavor"              , "(Sum(fake_mu)+4*Sum(fake_el)-4)/6")
                  .Define("fake_Muon_ptMuonMomUp"          , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,+1)")
                  .Define("fake_Muon_ptDef"                , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,0)")
                  .Define("fake_Muon_ptMuonMomDown"        , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,-1)")
                  .Define("fake_Electron_ptElectronMomUp"  , "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,+1)")
                  .Define("fake_Electron_ptDef"            , "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,0)")
                  .Define("fake_Electron_ptElectronMomDown", "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,-1)")
                  )
    else:
        dftag =(df.Define("FourLepton_flavor"              , "(Sum(fake_mu)+4*Sum(fake_el)-4)/6")
                  .Define("fake_Muon_ptMuonMomUp"          , "fake_Muon_pt")
                  .Define("fake_Muon_ptDef"                , "fake_Muon_pt")
                  .Define("fake_Muon_ptMuonMomDown"        , "fake_Muon_pt")
                  .Define("fake_Electron_ptElectronMomUp"  , "fake_Electron_pt")
                  .Define("fake_Electron_ptDef"            , "fake_Electron_pt")
                  .Define("fake_Electron_ptElectronMomDown", "fake_Electron_pt")
                  )

    dftag = make4LVar(dftag,"","")
    dftag = make4LVar(dftag,"MuonMomUp","")
    dftag = make4LVar(dftag,"MuonMomDown","")
    dftag = make4LVar(dftag,"","ElectronMomUp")
    dftag = make4LVar(dftag,"","ElectronMomDown")
    dftag = make4LVar(dftag,"Def","Def")

    return dftag


def make3LVar(df,postFixMu,postFixEl):

    postFix = ""
    if(postFixMu != ""):
        postFix = postFixMu
    elif(postFixEl != ""):
        postFix = postFixEl

    dftag =(df.Define("m3l{0}".format(postFix),    "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 0)".format(postFixMu,postFixEl))
              .Define("mllmin{0}".format(postFix), "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 1)".format(postFixMu,postFixEl))
              .Define("drllmin{0}".format(postFix),"compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 2)".format(postFixMu,postFixEl))
              .Define("ptl1{0}".format(postFix),   "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 3)".format(postFixMu,postFixEl))
              .Define("ptl2{0}".format(postFix),   "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 4)".format(postFixMu,postFixEl))
              .Define("ptl3{0}".format(postFix),   "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 5)".format(postFixMu,postFixEl))
              .Define("etal1{0}".format(postFix),  "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 6)".format(postFixMu,postFixEl))
              .Define("etal2{0}".format(postFix),  "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 7)".format(postFixMu,postFixEl))
              .Define("etal3{0}".format(postFix),  "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 8)".format(postFixMu,postFixEl))
              .Define("mll{0}".format(postFix),    "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi, 9)".format(postFixMu,postFixEl))
              .Define("ptl1Z{0}".format(postFix),  "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,10)".format(postFixMu,postFixEl))
              .Define("ptl2Z{0}".format(postFix),  "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,11)".format(postFixMu,postFixEl))
              .Define("ptlW{0}".format(postFix),   "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,12)".format(postFixMu,postFixEl))
              .Define("etalW{0}".format(postFix),  "abs(compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,13))".format(postFixMu,postFixEl))
              .Define("mtW{0}".format(postFix),    "compute_3l_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,14)".format(postFixMu,postFixEl))
              .Define("mllZ{0}".format(postFix),   "abs(mll{0}-91.1876)".format(postFix))
              .Define("ltype{0}".format(postFix),  "compute_nl_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,2)".format(postFixMu,postFixEl))
              )

    return dftag

def selection3LVar(df,year,isData):

    if(isData == "false"):
        dftag =(df.Define("TriLepton_flavor"               , "(Sum(fake_mu)+3*Sum(fake_el)-3)/2")
                  .Define("fake_Muon_ptMuonMomUp"          , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,+1)")
                  .Define("fake_Muon_ptDef"                , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,0)")
                  .Define("fake_Muon_ptMuonMomDown"        , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,-1)")
                  .Define("fake_Electron_ptElectronMomUp"  , "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,+1)")
                  .Define("fake_Electron_ptDef"            , "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,0)")
                  .Define("fake_Electron_ptElectronMomDown", "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,-1)")
                  )
    else:
        dftag =(df.Define("TriLepton_flavor"               , "(Sum(fake_mu)+3*Sum(fake_el)-3)/2")
                  .Define("fake_Muon_ptMuonMomUp"          , "fake_Muon_pt")
                  .Define("fake_Muon_ptDef"                , "fake_Muon_pt")
                  .Define("fake_Muon_ptMuonMomDown"        , "fake_Muon_pt")
                  .Define("fake_Electron_ptElectronMomUp"  , "fake_Electron_pt")
                  .Define("fake_Electron_ptDef"            , "fake_Electron_pt")
                  .Define("fake_Electron_ptElectronMomDown", "fake_Electron_pt")
                  )

    dftag = make3LVar(dftag,"","")
    dftag = make3LVar(dftag,"MuonMomUp","")
    dftag = make3LVar(dftag,"MuonMomDown","")
    dftag = make3LVar(dftag,"","ElectronMomUp")
    dftag = make3LVar(dftag,"","ElectronMomDown")
    dftag = make3LVar(dftag,"Def","Def")

    return dftag

def make2LVar(df,postFixMu,postFixEl):

    postFix = ""
    if(postFixMu != ""):
        postFix = postFixMu
    elif(postFixEl != ""):
        postFix = postFixEl

    dftag =(df.Define("mll{0}".format(postFix),   "compute_ll_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,0)".format(postFixMu,postFixEl))
              .Define("ptll{0}".format(postFix),  "compute_ll_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,1)".format(postFixMu,postFixEl))
              .Define("drll{0}".format(postFix),  "compute_ll_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,2)".format(postFixMu,postFixEl))
              .Define("dphill{0}".format(postFix),"compute_ll_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,3)".format(postFixMu,postFixEl))
              .Define("ptl1{0}".format(postFix),  "compute_ll_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,4)".format(postFixMu,postFixEl))
              .Define("ptl2{0}".format(postFix),  "compute_ll_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,5)".format(postFixMu,postFixEl))
              .Define("etal1{0}".format(postFix), "abs(compute_ll_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,6))".format(postFixMu,postFixEl))
              .Define("etal2{0}".format(postFix), "abs(compute_ll_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass,7))".format(postFixMu,postFixEl))
              .Define("ltype{0}".format(postFix), "compute_nl_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,2)".format(postFixMu,postFixEl))
              .Define("dPhilMETMin{0}".format(postFix), "compute_nl_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,7)".format(postFixMu,postFixEl))
              .Define("minPMET{0}".format(postFix), "compute_nl_var(fake_Muon_pt{0}, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_charge, fake_Electron_pt{1}, fake_Electron_eta, fake_Electron_phi, fake_Electron_mass, fake_Electron_charge, PuppiMET_pt, PuppiMET_phi,8)".format(postFixMu,postFixEl))
              )

    return dftag

def selection2LVar(df,year,isData):

    if(isData == "false"):
        dftag =(df.Define("DiLepton_flavor"                , "Sum(fake_mu)+2*Sum(fake_el)-2")
                  .Define("fake_Muon_ptMuonMomUp"          , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,+1)")
                  .Define("fake_Muon_ptDef"                , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,0)")
                  .Define("fake_Muon_ptMuonMomDown"        , "compute_MUOPT_Unc(fake_Muon_pt,fake_Muon_eta,-1)")
                  .Define("fake_Electron_ptElectronMomUp"  , "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,+1)")
                  .Define("fake_Electron_ptDef"            , "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,0)")
                  .Define("fake_Electron_ptElectronMomDown", "compute_ELEPT_Unc(fake_Electron_pt,fake_Electron_eta,-1)")
                  )
    else:
        dftag =(df.Define("DiLepton_flavor"                , "Sum(fake_mu)+2*Sum(fake_el)-2")
                  .Define("fake_Muon_ptMuonMomUp"          , "fake_Muon_pt")
                  .Define("fake_Muon_ptDef"                , "fake_Muon_pt")
                  .Define("fake_Muon_ptMuonMomDown"        , "fake_Muon_pt")
                  .Define("fake_Electron_ptElectronMomUp"  , "fake_Electron_pt")
                  .Define("fake_Electron_ptDef"            , "fake_Electron_pt")
                  .Define("fake_Electron_ptElectronMomDown", "fake_Electron_pt")
                  )

    dftag =(dftag.Define("ptl3", "0.0f")
                 .Define("muid1", "compute_muid_var(fake_Muon_mediumId, fake_Muon_tightId, fake_Muon_pfIsoId, fake_Muon_miniIsoId, fake_Muon_mvaTTH, fake_Muon_mediumPromptId, 0)")
                 .Define("muid2", "compute_muid_var(fake_Muon_mediumId, fake_Muon_tightId, fake_Muon_pfIsoId, fake_Muon_miniIsoId, fake_Muon_mvaTTH, fake_Muon_mediumPromptId, 1)")
                 .Define("elid1", "compute_elid_var(fake_Electron_cutBased, fake_Electron_mvaNoIso_WP80, fake_Electron_mvaIso_WP80, fake_Electron_mvaIso_WP90, fake_Electron_tightCharge, fake_Electron_mvaTTH, fake_Electron_pfRelIso03_chg, fake_Electron_pfRelIso03_all, 0)")
                 .Define("elid2", "compute_elid_var(fake_Electron_cutBased, fake_Electron_mvaNoIso_WP80, fake_Electron_mvaIso_WP80, fake_Electron_mvaIso_WP90, fake_Electron_tightCharge, fake_Electron_mvaTTH, fake_Electron_pfRelIso03_chg, fake_Electron_pfRelIso03_all, 1)")
                 )

    dftag = make2LVar(dftag,"","")
    dftag = make2LVar(dftag,"MuonMomUp","")
    dftag = make2LVar(dftag,"MuonMomDown","")
    dftag = make2LVar(dftag,"","ElectronMomUp")
    dftag = make2LVar(dftag,"","ElectronMomDown")
    dftag = make2LVar(dftag,"Def","Def")

    return dftag

def selectionTrigger2L(df,year,PDType,JSON,isData,triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG):

    if(year > 10000): year = year // 10

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
        triggerLEP = "({0} or {1}) and not {2}".format(triggerDMU,triggerSMU,triggerMUEG)

    elif(year == 2022 and PDType == "DoubleMuon"):
        triggerLEP = "{0} and not {1}".format(triggerDMU,triggerMUEG)

    elif(year == 2022 and PDType == "SingleMuon"):
        triggerLEP = "{0} and not {1} and not {2}".format(triggerSMU,triggerDMU,triggerMUEG)

    elif(year == 2022 and PDType == "EGamma"):
        triggerLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)

    elif(year == 2022):
        triggerLEP = "{0} or {1} or {2} or {3} or {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)

    elif(year == 2023 and PDType == "MuonEG"):
        triggerLEP = "{0}".format(triggerMUEG)

    elif(year == 2023 and PDType == "Muon"):
        triggerLEP = "({0} or {1}) and not {2}".format(triggerDMU,triggerSMU,triggerMUEG)

    elif(year == 2023 and PDType == "EGamma"):
        triggerLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)

    elif(year == 2023):
        triggerLEP = "{0} or {1} or {2} or {3} or {4}".format(triggerSEL,triggerDEL,triggerSMU,triggerDMU,triggerMUEG)

    else:
        print("PROBLEM with triggers!!!")

    print("triggerLEP: {0}".format(triggerLEP))

    dftag =(df.Define("isData","{}".format(isData))
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")
              .Define("trigger","{0}".format(triggerLEP))
              .Filter("trigger > 0","Passed trigger")
              .Define("triggerMUEG","{0}".format(triggerMUEG))
              .Define("triggerDMU", "{0}".format(triggerDMU))
              .Define("triggerSMU", "{0}".format(triggerSMU))
              .Define("triggerDEL", "{0}".format(triggerDEL))
              .Define("triggerSEL", "{0}".format(triggerSEL))
              )

    return dftag

def selectionTrigger1L(df,year,PDType,JSON,isData,triggerFAKEMU,triggerFAKEEL):

    if(year > 10000): year = year // 10

    triggerFAKE = "0"

    if(year == 2018 and PDType == "DoubleMuon"):
        triggerFAKE = triggerFAKEMU
    elif(year == 2018 and PDType == "EGamma"):
        triggerFAKE =  triggerFAKEEL
    elif(year == 2022 and PDType == "DoubleMuon"):
        triggerFAKE = triggerFAKEMU
    elif(year == 2022 and PDType == "Muon"):
        triggerFAKE = triggerFAKEMU
    elif(year == 2022 and PDType == "EGamma"):
        triggerFAKE =  triggerFAKEEL
    elif(year == 2023 and PDType == "Muon"):
        triggerFAKE = triggerFAKEMU
    elif(year == 2023 and PDType == "EGamma"):
        triggerFAKE =  triggerFAKEEL
    elif(PDType == "MuonEG"):
        triggerFAKE =  "0"
    elif(year == 2018):
        triggerFAKE = "{0} or {1}".format(triggerFAKEMU,triggerFAKEEL)
    elif(year == 2022):
        triggerFAKE = "{0} or {1}".format(triggerFAKEMU,triggerFAKEEL)
    elif(year == 2023):
        triggerFAKE = "{0} or {1}".format(triggerFAKEMU,triggerFAKEEL)
    else:
        print("PROBLEM with triggers!!!")

    print("triggerFAKE: {0}".format(triggerFAKE))

    dftag =(df.Define("isData","{}".format(isData))
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")
              .Define("trigger","{0}".format(triggerFAKE))
              .Filter("trigger > 0","Passed trigger1l")
              .Define("triggerFAKEMU","{0}".format(triggerFAKEMU))
              .Define("triggerFAKEEL", "{0}".format(triggerFAKEEL))
	      )

    return dftag

def selectionElMu(df,year,fake_mu,tight_mu,fake_el,tight_el):
    dftag =(df.Define("loose_mu"                  ,"abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")
              .Define("fake_mu"                   ,"{0}".format(fake_mu))
              .Define("fake_Muon_pt"              ,"Muon_pt[fake_mu]")
              .Define("fake_Muon_eta"             ,"Muon_eta[fake_mu]")
              .Define("fake_Muon_phi"             ,"Muon_phi[fake_mu]")
              .Define("fake_Muon_dxy"             ,"Muon_dxy[fake_mu]")
              .Define("fake_Muon_dz"              ,"Muon_dz[fake_mu]")
              .Define("fake_Muon_sip3d"           ,"Muon_sip3d[fake_mu]")
              .Define("fake_Muon_mass"            ,"Muon_mass[fake_mu]")
              .Define("fake_Muon_charge"          ,"Muon_charge[fake_mu]")
              .Define("fake_Muon_jetRelIso"       ,"Muon_jetRelIso[fake_mu]")
              .Define("fake_Muon_looseId"         ,"Muon_looseId[fake_mu]")
              .Define("fake_Muon_mediumId"        ,"Muon_mediumId[fake_mu]")
              .Define("fake_Muon_mediumPromptId"  ,"Muon_mediumPromptId[fake_mu]")
              .Define("fake_Muon_tightId"         ,"Muon_tightId[fake_mu]")
              .Define("fake_Muon_pfIsoId"         ,"Muon_pfIsoId[fake_mu]")
              .Define("fake_Muon_mvaMuID"         ,"Muon_mvaMuID[fake_mu]")
              .Define("fake_Muon_miniIsoId"       ,"Muon_miniIsoId[fake_mu]")
              .Define("fake_Muon_mvaTTH"          ,"Muon_mvaTTH[fake_mu]")
              .Define("fake_Muon_mvaLowPt"        ,"Muon_mvaLowPt[fake_mu]")
              .Define("fake_Muon_pfRelIso03_all"  ,"Muon_pfRelIso03_all[fake_mu]")
              .Define("fake_Muon_pfRelIso04_all"  ,"Muon_pfRelIso04_all[fake_mu]")
              .Define("fake_Muon_miniPFRelIso_all","Muon_miniPFRelIso_all[fake_mu]")
              .Define("fake_Muon_nStations"       ,"Muon_nStations[fake_mu]")
              .Define("fake_Muon_nTrackerLayers"  ,"Muon_nTrackerLayers[fake_mu]")
              .Define("fake_Muon_pfRelIso03_chg"  ,"Muon_pfRelIso03_chg[fake_mu]")
              .Define("tight_mu"                  ,"{0}".format(tight_mu))

              .Define("loose_el"                          ,"abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")
              .Define("fake_el"                           ,"{0}".format(fake_el))
              .Define("fake_Electron_pt"                  ,"Electron_pt[fake_el]")
              .Define("fake_Electron_eta"                 ,"Electron_eta[fake_el]")
              .Define("fake_Electron_phi"                 ,"Electron_phi[fake_el]")
              .Define("fake_Electron_mass"                ,"Electron_mass[fake_el]")
              .Define("fake_Electron_charge"              ,"Electron_charge[fake_el]")
              .Define("fake_Electron_jetRelIso"           ,"Electron_jetRelIso[fake_el]")
              .Define("fake_Electron_dxy"                 ,"Electron_dxy[fake_el]")
              .Define("fake_Electron_dz"                  ,"Electron_dz[fake_el]")
              .Define("fake_Electron_sip3d"               ,"Electron_sip3d[fake_el]")
              .Define("fake_Electron_cutBased"            ,"Electron_cutBased[fake_el]")
              .Define("fake_Electron_mvaNoIso_WP80"       ,"Electron_mvaNoIso_WP80[fake_el]")
              .Define("fake_Electron_mvaIso_WP80"         ,"Electron_mvaIso_WP80[fake_el]")
              .Define("fake_Electron_mvaIso_WP90"         ,"Electron_mvaIso_WP90[fake_el]")
              .Define("fake_Electron_tightCharge"         ,"Electron_tightCharge[fake_el]")
              .Define("fake_Electron_mvaTTH"              ,"Electron_mvaTTH[fake_el]")
              .Define("fake_Electron_mvaIso"              ,"Electron_mvaIso[fake_el]")
              .Define("fake_Electron_mvaNoIso"            ,"Electron_mvaNoIso[fake_el]")
              .Define("fake_Electron_pfRelIso03_all"      ,"Electron_pfRelIso03_all[fake_el]")
              .Define("fake_Electron_miniPFRelIso_all"    ,"Electron_miniPFRelIso_all[fake_el]")
              .Define("fake_Electron_hoe"                 ,"Electron_hoe[fake_el]")
              .Define("fake_Electron_r9"                  ,"Electron_r9[fake_el]")
              .Define("fake_Electron_pfRelIso03_chg"      ,"Electron_pfRelIso03_chg[fake_el]")
              .Define("tight_el"                          ,"{0}".format(tight_el))

              .Define("nLoose","Sum(loose_mu)+Sum(loose_el)")
              .Define("nFake","Sum(fake_mu)+Sum(fake_el)")
              .Define("nTight","Sum(tight_mu)+Sum(tight_el)")
              )

    return dftag

def selectionDAWeigths(df,year,PDType):
    dftag =(df.Define("PDType","\"{0}\"".format(PDType))
              .Define("weightFake","compute_fakeRate(isData,fake_Muon_pt,fake_Muon_eta,tight_mu,fake_Electron_pt,fake_Electron_eta,tight_el)")
              .Define("weight","weightFake*1.0")
              .Define("weight0","1.0")
              .Define("weight1","weightFake*1.0")
              .Define("weight2","weightFake*1.0")
              .Define("weight3","weightFake*1.0")
              .Define("weight4","weightFake*1.0")
              .Define("weight5","weightFake*1.0")
              .Define("weightNoLepSF","weightFake*1.0")
              .Define("weightBTag","weight")
              .Define("weightNoBTag","weight")
              )

    return dftag

def selectionMCWeigths(df,year,PDType,weight,type,bTagSel,useBTaggingWeights,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,MUOWP,ELEWP,correctionString):

    hasTheoryColumnName = [True, True, True]
    theoryColumnName = ["PSWeight", "LHEScaleWeight", "LHEPdfWeight"]
    for x in range(len(theoryColumnName)):
        try:
            ColumnType = df.GetColumnType(theoryColumnName[x])
        except Exception as e:
            print("No {0} weights: {1}".format(theoryColumnName[x],e))
            hasTheoryColumnName[x] = False

    MUOYEAR = year
    ELEYEAR = "NULL"
    if  (year == 20220): ELEYEAR = "2022FG"
    elif(year == 20221): ELEYEAR = "2022FG"
    PHOYEAR = "NULL"
    if  (year == 20220): PHOYEAR = "2022FG"
    elif(year == 20221): PHOYEAR = "2022FG"
    if(correctionString == "_correction"):
        MUOWP = "Medium"
        ELEWP = "Medium"
    print("MUOYEAR/ELEYEAR/PHOYEAR/MUOWP/ELEWP: {0}/{1}/{2}/{3}/{4}".format(MUOYEAR,ELEYEAR,PHOYEAR,MUOWP,ELEWP))

    dftag =(df.Define("PDType","\"{0}\"".format(PDType))
              .Define("clean_Jet_hadronFlavour", "Jet_hadronFlavour[clean_jet]")
              .Define("goodbtag_Jet_hadronFlavour","clean_Jet_hadronFlavour[goodbtag_jet]")
              .Define("fake_Muon_genPartFlav","Muon_genPartFlav[fake_mu]")
              .Define("fake_Electron_genPartFlav","Electron_genPartFlav[fake_el]")
              .Define("weightPURecoSF","compute_PURecoSF(fake_Muon_pt,fake_Muon_eta,fake_Electron_pt,fake_Electron_eta,Pileup_nTrueInt,0)")
              .Define("weightMuonSF","compute_MuonSF(fake_Muon_pt,fake_Muon_eta)")
              .Define("weightElectronSF","compute_ElectronSF(fake_Electron_pt,fake_Electron_eta)")
              .Define("weightTriggerSF","compute_TriggerSF(ptl1,ptl2,etal1,etal2,ltype)")

              .Define("weightMC","compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})".format(weight,type))
              .Filter("weightMC != 0","MC weight")

              .Define("MUOYEAR","\"{0}\"".format(MUOYEAR))
              .Define("ELEYEAR","\"{0}\"".format(ELEYEAR))
              .Define("PHOYEAR","\"{0}\"".format(PHOYEAR))
              .Define("MUOWP","\"{0}\"".format(MUOWP))
              .Define("ELEWP","\"{0}\"".format(ELEWP))
              .Define("PHOWP","\"Medium\"")

              .Define("weightFake","compute_fakeRate(isData,fake_Muon_pt,fake_Muon_eta,tight_mu,fake_Electron_pt,fake_Electron_eta,tight_el)")

              .Define("weightBtagSF","compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"central\",0,{0})".format(bTagSel))

              .Define("weightMuoSFJSON","compute_JSON_MUO_SFs(\"nominal\",\"nominal\",\"nominal\",fake_Muon_pt,fake_Muon_eta,0)")

              .Define("weightEleSFJSON","compute_JSON_ELE_SFs(ELEYEAR,\"sf\",\"sf\",ELEWP,fake_Electron_pt,fake_Electron_eta)")

              .Define("weightPUSF_Nom","compute_JSON_PU_SF(Pileup_nTrueInt,\"nominal\")")
              )

    if(correctionString == "_correction"):
        if(useBTaggingWeights == 1):
            print("BtagCorr/AddCorr: 1/1")
            dftag = (dftag
                     .Define("weight","weightMC*weightFake*weightBtagSF*weightPURecoSF*weightTriggerSF*weightMuoSFJSON*weightEleSFJSON*weightMuonSF*weightElectronSF")
                    )
        else:
            print("BtagCorr/AddCorr: 0/1")
            dftag = (dftag
                     .Define("weight","weightMC*weightFake*weightPURecoSF*weightTriggerSF*weightMuoSFJSON*weightEleSFJSON*weightMuonSF*weightElectronSF")
                    )

    else:
        if(useBTaggingWeights == 1):
            print("BtagCorr/AddCorr: 1/0")
            dftag = (dftag
                     .Define("weight","weightMC*weightFake*weightBtagSF*weightPURecoSF*weightTriggerSF*weightMuoSFJSON*weightEleSFJSON")
                    )
        else:
            print("BtagCorr/AddCorr: 0/0")
            dftag = (dftag
                     .Define("weight","weightMC*weightFake*weightPURecoSF*weightTriggerSF*weightMuoSFJSON*weightEleSFJSON")
                    )

    if(useBTaggingWeights == 1):
        dftag = (dftag
                 .Define("weightNoLepSF","weightMC*weightFake*weightBtagSF*weightPURecoSF*weightTriggerSF")
                 .Define("weightBTag","weight")
                 .Define("weightNoBTag","weight/weightBtagSF")
                )
    else:
        dftag = (dftag
                 .Define("weightNoLepSF","weightMC*weightFake*weightPURecoSF*weightTriggerSF")
                 .Define("weightBTag","weight*weightBtagSF")
                 .Define("weightNoBTag","weight")
                )

    dftag =(dftag.Define("weight0","weightMC*weightFake*weightBtagSF")
                 .Define("weight1","weightMC*weightFake*weightMuoSFJSON")
                 .Define("weight2","weightMC*weightFake*weightEleSFJSON")
                 .Define("weight3","weight/weightPURecoSF")
                 .Define("weight4","weight/weightMuonSF/weightElectronSF")
                 .Define("weight5","weight/weightTriggerSF")

                 .Define("weightBtagSFBC_correlatedUp"    ,"weight/weightBtagSF*compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"up_correlated\",1,{0})".format(bTagSel))
                 .Define("weightBtagSFBC_correlatedDown"  ,"weight/weightBtagSF*compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"down_correlated\",1,{0})".format(bTagSel))
                 .Define("weightBtagSFBC_uncorrelatedUp"  ,"weight/weightBtagSF*compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"up_uncorrelated\",1,{0})".format(bTagSel))
                 .Define("weightBtagSFBC_uncorrelatedDown","weight/weightBtagSF*compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"down_uncorrelated\",1,{0})".format(bTagSel))

                 .Define("weightBtagSFLF_correlatedUp"    ,"weight/weightBtagSF*compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"up_correlated\",-1,{0})".format(bTagSel))
                 .Define("weightBtagSFLF_correlatedDown"  ,"weight/weightBtagSF*compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"down_correlated\",-1,{0})".format(bTagSel))
                 .Define("weightBtagSFLF_uncorrelatedUp"  ,"weight/weightBtagSF*compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"up_uncorrelated\",-1,{0})".format(bTagSel))
                 .Define("weightBtagSFLF_uncorrelatedDown","weight/weightBtagSF*compute_JSON_BTV_SF(goodbtag_Jet_pt,goodbtag_Jet_eta,goodbtag_Jet_btagDeepFlavB,goodbtag_Jet_hadronFlavour,\"down_uncorrelated\",-1,{0})".format(bTagSel))

                 .Define("weightMuoSFTRKUp","weight/weightMuoSFJSON*compute_JSON_MUO_SFs(\"syst\",\"nominal\",\"nominal\",fake_Muon_pt,fake_Muon_eta,+1)")
                 .Define("weightMuoSFIDUp" ,"weight/weightMuoSFJSON*compute_JSON_MUO_SFs(\"nominal\",\"syst\",\"nominal\",fake_Muon_pt,fake_Muon_eta,+1)")
                 .Define("weightMuoSFISOUp","weight/weightMuoSFJSON*compute_JSON_MUO_SFs(\"nominal\",\"nominal\",\"syst\",fake_Muon_pt,fake_Muon_eta,+1)")

                 .Define("weightMuoSFTRKDown","weight/weightMuoSFJSON*compute_JSON_MUO_SFs(\"syst\",\"nominal\",\"nominal\",fake_Muon_pt,fake_Muon_eta,-1)")
                 .Define("weightMuoSFIDDown" ,"weight/weightMuoSFJSON*compute_JSON_MUO_SFs(\"nominal\",\"syst\",\"nominal\",fake_Muon_pt,fake_Muon_eta,-1)")
                 .Define("weightMuoSFISODown","weight/weightMuoSFJSON*compute_JSON_MUO_SFs(\"nominal\",\"nominal\",\"syst\",fake_Muon_pt,fake_Muon_eta,-1)")

                 .Define("weightEleSFTRKUp","weight/weightEleSFJSON*compute_JSON_ELE_SFs(ELEYEAR,\"sfup\",\"sf\",ELEWP,fake_Electron_pt,fake_Electron_eta)")
                 .Define("weightEleSFIDUp" ,"weight/weightEleSFJSON*compute_JSON_ELE_SFs(ELEYEAR,\"sf\",\"sfup\",ELEWP,fake_Electron_pt,fake_Electron_eta)")

                 .Define("weightEleSFTRKDown","weight/weightEleSFJSON*compute_JSON_ELE_SFs(ELEYEAR,\"sfdown\",\"sf\",ELEWP,fake_Electron_pt,fake_Electron_eta)")
                 .Define("weightEleSFIDDown" ,"weight/weightEleSFJSON*compute_JSON_ELE_SFs(ELEYEAR,\"sf\",\"sfdown\",ELEWP,fake_Electron_pt,fake_Electron_eta)")

                 #.Define("weightPUSF_Up"  ,"weight/weightPUSF_Nom*compute_JSON_PU_SF(Pileup_nTrueInt,\"up\")")
                 #.Define("weightPUSF_Down","weight/weightPUSF_Nom*compute_JSON_PU_SF(Pileup_nTrueInt,\"down\")")
                 .Define("weightPUSF_Up"  ,"weight/weightPURecoSF*compute_PURecoSF(fake_Muon_pt,fake_Muon_eta,fake_Electron_pt,fake_Electron_eta,Pileup_nTrueInt,1)")
                 .Define("weightPUSF_Down","weight/weightPURecoSF*compute_PURecoSF(fake_Muon_pt,fake_Muon_eta,fake_Electron_pt,fake_Electron_eta,Pileup_nTrueInt,2)")


                 .Define("weightPhoSFJSON","compute_JSON_PHO_SFs(PHOYEAR,\"sf\",PHOWP,good_Photons_pt,good_Photons_eta)")
                 .Filter("weightPhoSFJSON > 0","weightPhoSFJSON > 0")

                 .Define("weightTauSFJSON","compute_JSON_TAU_SFs(good_Tau_pt,good_Tau_eta,good_Tau_decayMode,good_Tau_genPartFlav,\"nom\")")
                 .Filter("weightTauSFJSON > 0","weightTauSFJSON > 0")

                 )

    if(hasTheoryColumnName[0] == True and nTheoryReplicas[2] == 4):
        dftag =(dftag.Define("weightPS0" ,"weight*PSWeight[0]/{0}".format(genEventSumPSRenorm[0]))
                     .Define("weightPS1" ,"weight*PSWeight[1]/{0}".format(genEventSumPSRenorm[1]))
                     .Define("weightPS2" ,"weight*PSWeight[2]/{0}".format(genEventSumPSRenorm[2]))
                     .Define("weightPS3" ,"weight*PSWeight[3]/{0}".format(genEventSumPSRenorm[3]))
                     )
    else:
        dftag =(dftag.Define("weightPS0" ,"weight*1.0")
                     .Define("weightPS1" ,"weight*1.0")
                     .Define("weightPS2" ,"weight*1.0")
                     .Define("weightPS3" ,"weight*1.0")
                     )

    if(hasTheoryColumnName[1] == True and nTheoryReplicas[1] == 9):
        #LHEScaleWeight 2 / 4 / 6 not used
        dftag =(dftag.Define("weightQCDScale0" ,"weight*LHEScaleWeight[0]/{0}".format(genEventSumLHEScaleRenorm[0]))
                     .Define("weightQCDScale1" ,"weight*LHEScaleWeight[1]/{0}".format(genEventSumLHEScaleRenorm[1]))
                     .Define("weightQCDScale2" ,"weight*LHEScaleWeight[3]/{0}".format(genEventSumLHEScaleRenorm[2]))
                     .Define("weightQCDScale3" ,"weight*LHEScaleWeight[5]/{0}".format(genEventSumLHEScaleRenorm[3]))
                     .Define("weightQCDScale4" ,"weight*LHEScaleWeight[7]/{0}".format(genEventSumLHEScaleRenorm[4]))
                     .Define("weightQCDScale5" ,"weight*LHEScaleWeight[8]/{0}".format(genEventSumLHEScaleRenorm[5]))
                     )
    else:
        dftag =(dftag.Define("weightQCDScale0" ,"weight*1.0")
                     .Define("weightQCDScale1" ,"weight*1.0")
                     .Define("weightQCDScale2" ,"weight*1.0")
                     .Define("weightQCDScale3" ,"weight*1.0")
                     .Define("weightQCDScale4" ,"weight*1.0")
                     .Define("weightQCDScale5" ,"weight*1.0")
                     )

    # 0 (default) 1...100 101/102 (Up/Down for alphas)
    if(hasTheoryColumnName[2] == True):
        for xpdf in range(103):
            if(nTheoryReplicas[0] > xpdf):
                dftag = dftag.Define("weightPDF{0}".format(xpdf),"weight*LHEPdfWeight[{0}]".format(xpdf))
            else:
                dftag = dftag.Define("weightPDF{0}".format(xpdf),"weight*1.0")
    else:
        for xpdf in range(103):
            dftag = dftag.Define("weightPDF{0}".format(xpdf),"weight*1.0")

    return dftag

def selectionWeigths(df,isData,year,PDType,weight,type,bTagSel,useBTaggingWeights,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,MUOWP,ELEWP,correctionString):
    if(isData == "true"): return selectionDAWeigths(df,year,PDType)
    else:                 return selectionMCWeigths(df,year,PDType,weight,type,bTagSel,useBTaggingWeights,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,MUOWP,ELEWP,correctionString)

def makeFinalVariable(df,var,theCat,start,x,bin,min,max,type):
    histoNumber = start+type
    if(theCat == plotCategory("kPlotData")):
        return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weight")

    if  (type ==  0): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weight")
    elif(type ==  1): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightBtagSFBC_correlatedUp")
    elif(type ==  2): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightBtagSFBC_correlatedDown")
    elif(type ==  3): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightBtagSFBC_uncorrelatedUp")
    elif(type ==  4): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightBtagSFBC_uncorrelatedDown")
    elif(type ==  5): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightBtagSFLF_correlatedUp")
    elif(type ==  6): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightBtagSFLF_correlatedDown")
    elif(type ==  7): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightBtagSFLF_uncorrelatedUp")
    elif(type ==  8): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightBtagSFLF_uncorrelatedDown")
    elif(type ==  9): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightMuoSFTRKUp")
    elif(type == 10): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightMuoSFTRKDown")
    elif(type == 11): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightMuoSFIDUp")
    elif(type == 12): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightMuoSFIDDown")
    elif(type == 13): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightMuoSFISOUp")
    elif(type == 14): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightMuoSFISODown")
    elif(type == 15): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightEleSFTRKUp")
    elif(type == 16): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightEleSFTRKDown")
    elif(type == 17): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightEleSFIDUp")
    elif(type == 18): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightEleSFIDDown")
    elif(type == 19): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightPUSF_Up")
    elif(type == 20): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightPUSF_Down")
    elif(type == 21): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightPS0")
    elif(type == 22): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightPS1")
    elif(type == 23): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightPS2")
    elif(type == 24): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightPS3")
    elif(type == 25): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightQCDScale0")
    elif(type == 26): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightQCDScale1")
    elif(type == 27): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightQCDScale2")
    elif(type == 28): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightQCDScale3")
    elif(type == 29): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightQCDScale4")
    elif(type == 30): return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightQCDScale5")
    elif(type >= 31 and type <= 133):
                      return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weightPDF{0}".format(type-31))
    else:             return df.Histo1D(("histo_{0}_{1}".format(histoNumber,x), "histo_{0}_{1}".format(histoNumber,x),bin,min,max), "{0}".format(var),"weight")

def makeFinalVariable2D(df,varX,varY,theCat,start,x,binX,minX,maxX,binY,minY,maxY,type):
    histoNumber = start+type
    if(theCat == plotCategory("kPlotData")):
        return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weight")

    if  (type ==  0): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weight")
    elif(type ==  1): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightBtagSFBC_correlatedUp")
    elif(type ==  2): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightBtagSFBC_correlatedDown")
    elif(type ==  3): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightBtagSFBC_uncorrelatedUp")
    elif(type ==  4): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightBtagSFBC_uncorrelatedDown")
    elif(type ==  5): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightBtagSFLF_correlatedUp")
    elif(type ==  6): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightBtagSFLF_correlatedDown")
    elif(type ==  7): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightBtagSFLF_uncorrelatedUp")
    elif(type ==  8): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightBtagSFLF_uncorrelatedDown")
    elif(type ==  9): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightMuoSFTRKUp")
    elif(type == 10): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightMuoSFTRKDown")
    elif(type == 11): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightMuoSFIDUp")
    elif(type == 12): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightMuoSFIDDown")
    elif(type == 13): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightMuoSFISOUp")
    elif(type == 14): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightMuoSFISODown")
    elif(type == 15): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightEleSFTRKUp")
    elif(type == 16): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightEleSFTRKDown")
    elif(type == 17): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightEleSFIDUp")
    elif(type == 18): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightEleSFIDDown")
    elif(type == 19): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightPUSF_Up")
    elif(type == 20): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightPUSF_Down")
    elif(type == 21): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightPS0")
    elif(type == 22): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightPS1")
    elif(type == 23): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightPS2")
    elif(type == 24): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightPS3")
    elif(type == 25): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightQCDScale0")
    elif(type == 26): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightQCDScale1")
    elif(type == 27): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightQCDScale2")
    elif(type == 28): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightQCDScale3")
    elif(type == 29): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightQCDScale4")
    elif(type == 30): return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightQCDScale5")
    elif(type >= 31 and type <= 133):
                      return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weightPDF{0}".format(type-31))
    else:             return df.Histo2D(("histo2d_{0}_{1}".format(histoNumber,x), "histo2d_{0}_{1}".format(histoNumber,x),binX,minX,maxX,binY,minY,maxY), "{0}".format(varX), "{0}".format(varY),"weight")

import ROOT
import os, sys, getopt, json, time

ROOT.ROOT.EnableImplicitMT(3)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getMesonFromJson

lumi = [36.1, 41.5, 60.0]

doNtuples = False

selectionJsonPath = "config/selection.json"
if(not os.path.exists(selectionJsonPath)):
    selectionJsonPath = "selection.json"

with open(selectionJsonPath) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

JSON = jsonObject['JSON']

VBSSEL = jsonObject['VBSLOOSESEL']

BARRELphotons = jsonObject['BARRELphotons']
ENDCAPphotons = jsonObject['ENDCAPphotons']

FAKE_MU   = jsonObject['FAKE_MU']
FAKE_EL   = jsonObject['FAKE_EL']

def selectionLL(df,year,PDType,isData,whichSel):

    overallTriggers = jsonObject['triggers']
    TRIGGERMUEG = getTriggerFromJson(overallTriggers, "TRIGGERMUEG", year)
    TRIGGERDMU  = getTriggerFromJson(overallTriggers, "TRIGGERDMU", year)
    TRIGGERSMU  = getTriggerFromJson(overallTriggers, "TRIGGERSMU", year)
    TRIGGERDEL  = getTriggerFromJson(overallTriggers, "TRIGGERDEL", year)
    TRIGGERSEL  = getTriggerFromJson(overallTriggers, "TRIGGERSEL", year)
    TRIGGERVBF  = getTriggerFromJson(overallTriggers, "TRIGGERVBF", year)
    TRIGGERKKG  = getTriggerFromJson(overallTriggers, "TRIGGERKKG", year)

    mesons = jsonObject['mesons']
    GOODPHI = "{}".format(getMesonFromJson(mesons, "isVBF", "isPhiCat"))
    GOODRHO = "{}".format(getMesonFromJson(mesons, "isVBF", "isRhoCat"))

    TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    if(year == 2018 and PDType == "MuonEG"):
        TRIGGERLEP = "{0}".format(TRIGGERMUEG)
    elif(year == 2018 and PDType == "DoubleMuon"):
        TRIGGERLEP = "{0} and not {1}".format(TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "SingleMuon"):
        TRIGGERLEP = "{0} and not {1} and not {2}".format(TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "EGamma"):
        TRIGGERLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018):
        TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    else:
        print("PROBLEM with triggers!!!")

    print("TRIGGERLEP: {0}".format(TRIGGERLEP))

    dftag =(df.Define("isData","{}".format(isData))
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")
              .Define("triggerVBF","{0}".format(TRIGGERVBF))
              .Define("triggerKKG","{0}".format(TRIGGERKKG))

              .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")
              .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")

              .Define("fake_mu"           ,"{0}".format(FAKE_MU))
              .Define("fakemu_pt"         ,"Muon_pt[fake_mu]")
              .Define("fakemu_eta"        ,"Muon_eta[fake_mu]")
              .Define("fakemu_phi"        ,"Muon_phi[fake_mu]")
              .Define("fakemu_mass"       ,"Muon_mass[fake_mu]")
              .Define("fakemu_charge"     ,"Muon_charge[fake_mu]")
              .Define("fakemu_dxy"        ,"Muon_dxy[fake_mu]")
              .Define("fakemu_dz"         ,"Muon_dz[fake_mu]")
              .Define("fakemu_looseId"    ,"Muon_looseId[fake_mu]")
              .Define("fakemu_mediumId"   ,"Muon_mediumId[fake_mu]")
              .Define("fakemu_tightId"    ,"Muon_tightId[fake_mu]")
              .Define("fakemu_pfIsoId"    ,"Muon_pfIsoId[fake_mu]")
              .Define("fakemu_mvaId"      ,"Muon_mvaId[fake_mu]")
              .Define("fakemu_miniIsoId"  ,"Muon_miniIsoId[fake_mu]")
              .Define("fakemu_mvaTTH"     ,"Muon_mvaTTH[fake_mu]")

              .Define("fake_el"                   ,"{0}".format(FAKE_EL))
              .Define("fakeel_pt"                 ,"Electron_pt[fake_el]")
              .Define("fakeel_eta"                ,"Electron_eta[fake_el]")
              .Define("fakeel_phi"                ,"Electron_phi[fake_el]")
              .Define("fakeel_mass"               ,"Electron_mass[fake_el]")
              .Define("fakeel_charge"             ,"Electron_charge[fake_el]")
              .Define("fakeel_dxy"                ,"Electron_dxy[fake_el]")
              .Define("fakeel_dz"                 ,"Electron_dz[fake_el]")
              .Define("fakeel_cutBased"           ,"Electron_cutBased[fake_el]")
              .Define("fakeel_mvaFall17V2Iso_WP90","Electron_mvaFall17V2Iso_WP90[fake_el]")
              .Define("fakeel_mvaFall17V2Iso_WP80","Electron_mvaFall17V2Iso_WP80[fake_el]")
              .Define("fakeel_tightCharge"        ,"Electron_tightCharge[fake_el]")
              .Define("fakeel_mvaTTH"             ,"Electron_mvaTTH[fake_el]")

              .Filter("Sum(fake_mu) == 0","0 fake muons")
              .Filter("Sum(fake_el) == 0","0 fake electrons")

              .Define("compute_photon_test","compute_photon_test(Photon_pt,Photon_eta,Photon_phi,Photon_cutBased,Photon_pfRelIso03_all,Photon_pfRelIso03_chg,Photon_hoe,Photon_sieie,Photon_vidNestedWPBitmap)")
              .Filter("compute_photon_test > 0","compute_photon_test > 0")

              .Define("photon_mask", "cleaningMask(Electron_photonIdx[fake_el],nPhoton)")
              .Define("goodPhotons", "{}".format(BARRELphotons)+" or {}".format(ENDCAPphotons) )
              .Define("goodPhotons_pt", "Photon_pt[goodPhotons]")
              .Define("goodPhotons_eta", "Photon_eta[goodPhotons]")
              .Define("goodPhotons_phi", "Photon_phi[goodPhotons]")
              .Define("goodPhotons_mass", "Photon_mass[goodPhotons]")
              .Filter("Sum(goodPhotons) > 0",">= 1 photon")
              .Define("testPhotons_dR", "compute_deltaR_var(Photon_eta,Photon_phi,goodPhotons_eta[0],goodPhotons_phi[0])")

              .Define("test0Photons", "Photon_pt > 20 and Photon_electronVeto and photon_mask and Photon_isScEtaEB and testPhotons_dR < 0.3")
              .Define("test0Photons_pt", "Photon_pt[test0Photons]")
              .Define("test0Photons_eta", "Photon_eta[test0Photons]")
              .Define("test0Photons_phi", "Photon_phi[test0Photons]")
              .Define("test0Photons_cutBased", "Photon_cutBased[test0Photons]")
              .Define("test0Photons_mvaID_WP80", "Photon_mvaID_WP80[test0Photons]*1.0")
              .Define("test0Photons_mvaID_WP90", "Photon_mvaID_WP90[test0Photons]*1.0")
              .Define("test0Photons_mvaID", "Photon_mvaID[test0Photons]")
              .Define("test0Photons_pfRelIso03_all", "Photon_pfRelIso03_all[test0Photons]")
              .Define("test0Photons_pfRelIso03_chg", "Photon_pfRelIso03_chg[test0Photons]")
              .Define("test0Photons_hoe", "Photon_hoe[test0Photons]")
              .Define("test0Photons_r9", "Photon_r9[test0Photons]")
              .Define("test0Photons_sieie", "Photon_sieie[test0Photons]")

              .Define("test1Photons", "Photon_pt > 20 and Photon_electronVeto and photon_mask and Photon_isScEtaEE and testPhotons_dR < 0.3")
              .Define("test1Photons_pt", "Photon_pt[test1Photons]")
              .Define("test1Photons_eta", "Photon_eta[test1Photons]")
              .Define("test1Photons_phi", "Photon_phi[test1Photons]")
              .Define("test1Photons_cutBased", "Photon_cutBased[test1Photons]")
              .Define("test1Photons_mvaID_WP80", "Photon_mvaID_WP80[test1Photons]*1.0")
              .Define("test1Photons_mvaID_WP90", "Photon_mvaID_WP90[test1Photons]*1.0")
              .Define("test1Photons_mvaID", "Photon_mvaID[test1Photons]")
              .Define("test1Photons_pfRelIso03_all", "Photon_pfRelIso03_all[test1Photons]")
              .Define("test1Photons_pfRelIso03_chg", "Photon_pfRelIso03_chg[test1Photons]")
              .Define("test1Photons_hoe", "Photon_hoe[test1Photons]")
              .Define("test1Photons_r9", "Photon_r9[test1Photons]")
              .Define("test1Photons_sieie", "Photon_sieie[test1Photons]")

              .Define("test2Photons", "Photon_pt > 20 and Photon_electronVeto and photon_mask and Photon_isScEtaEB and testPhotons_dR > 0.3")
              .Define("test2Photons_pt", "Photon_pt[test2Photons]")
              .Define("test2Photons_eta", "Photon_eta[test2Photons]")
              .Define("test2Photons_phi", "Photon_phi[test2Photons]")
              .Define("test2Photons_cutBased", "Photon_cutBased[test2Photons]")
              .Define("test2Photons_mvaID_WP80", "Photon_mvaID_WP80[test2Photons]*1.0")
              .Define("test2Photons_mvaID_WP90", "Photon_mvaID_WP90[test2Photons]*1.0")
              .Define("test2Photons_mvaID", "Photon_mvaID[test2Photons]")
              .Define("test2Photons_pfRelIso03_all", "Photon_pfRelIso03_all[test2Photons]")
              .Define("test2Photons_pfRelIso03_chg", "Photon_pfRelIso03_chg[test2Photons]")
              .Define("test2Photons_hoe", "Photon_hoe[test2Photons]")
              .Define("test2Photons_r9", "Photon_r9[test2Photons]")
              .Define("test2Photons_sieie", "Photon_sieie[test2Photons]")

              .Define("test3Photons", "Photon_pt > 20 and Photon_electronVeto and photon_mask and Photon_isScEtaEE and testPhotons_dR > 0.3")
              .Define("test3Photons_pt", "Photon_pt[test3Photons]")
              .Define("test3Photons_eta", "Photon_eta[test3Photons]")
              .Define("test3Photons_phi", "Photon_phi[test3Photons]")
              .Define("test3Photons_cutBased", "Photon_cutBased[test3Photons]")
              .Define("test3Photons_mvaID_WP80", "Photon_mvaID_WP80[test3Photons]*1.0")
              .Define("test3Photons_mvaID_WP90", "Photon_mvaID_WP90[test3Photons]*1.0")
              .Define("test3Photons_mvaID", "Photon_mvaID[test3Photons]")
              .Define("test3Photons_pfRelIso03_all", "Photon_pfRelIso03_all[test3Photons]")
              .Define("test3Photons_pfRelIso03_chg", "Photon_pfRelIso03_chg[test3Photons]")
              .Define("test3Photons_hoe", "Photon_hoe[test3Photons]")
              .Define("test3Photons_r9", "Photon_r9[test3Photons]")
              .Define("test3Photons_sieie", "Photon_sieie[test3Photons]")

              )
    if(whichSel == 0):
        print("Select PHI")
        dftag = (dftag
              .Define("goodX","{0}".format(GOODPHI))
              .Define("goodX_pt", "phi_kin_pt[goodX]")
              .Define("goodX_eta", "phi_kin_eta[goodX]")
              .Define("goodX_phi", "phi_kin_phi[goodX]")
              .Define("goodX_mass", "phi_kin_mass[goodX]")
              .Define("goodX_massErr", "phi_kin_massErr[goodX]")
              .Define("goodX_iso", "phi_iso[goodX]")
              .Define("goodX_vtx_chi2dof", "phi_kin_vtx_chi2dof[goodX]")
              .Define("goodX_vtx_prob", "phi_kin_vtx_prob[goodX]")
              .Define("goodX_trk1_pt", "phi_trk1_pt[goodX]")
              .Define("goodX_trk2_pt", "phi_trk2_pt[goodX]")
              .Define("goodX_trk1_eta", "phi_trk1_eta[goodX]")
              .Define("goodX_trk2_eta", "phi_trk2_eta[goodX]")
              .Define("goodXDR","DeltaR(phi_trk1_eta[goodX],phi_trk2_eta[goodX],phi_trk1_phi[goodX],phi_trk2_phi[goodX])")
              )
    elif(whichSel == 1):
        print("Select RHO")
        dftag = (dftag
              .Define("goodX","{0}".format(GOODRHO))
              .Define("goodX_pt", "rho_kin_pt[goodX]")
              .Define("goodX_eta", "rho_kin_eta[goodX]")
              .Define("goodX_phi", "rho_kin_phi[goodX]")
              .Define("goodX_mass", "rho_kin_mass[goodX]")
              .Define("goodX_massErr", "rho_kin_massErr[goodX]")
              .Define("goodX_iso", "rho_iso[goodX]")
              .Define("goodX_vtx_chi2dof", "rho_kin_vtx_chi2dof[goodX]")
              .Define("goodX_vtx_prob", "rho_kin_vtx_prob[goodX]")
              .Define("goodX_trk1_pt", "rho_trk1_pt[goodX]")
              .Define("goodX_trk2_pt", "rho_trk2_pt[goodX]")
              .Define("goodX_trk1_eta", "rho_trk1_eta[goodX]")
              .Define("goodX_trk2_eta", "rho_trk2_eta[goodX]")
              .Define("goodXDR","DeltaR(rho_trk1_eta[goodX],rho_trk2_eta[goodX],rho_trk1_phi[goodX],rho_trk2_phi[goodX])")
              )

    dftag = (dftag
    	  .Filter("Sum(goodX) > 0",">= 1 phi")

    	  .Define("index_pair","HiggsCandFromRECO(goodX_pt,goodX_eta,goodX_phi,goodX_mass,goodPhotons_pt,goodPhotons_eta,goodPhotons_phi)")
    	  .Filter("index_pair[0]!= -1", "at least a good meson candidate")
    	  .Define("jet_mask0", "cleaningJetFromMeson(Jet_eta, Jet_phi, goodX_eta[index_pair[0]], goodX_phi[index_pair[0]])")
    	  .Define("HCandMass", "Minv2(goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]]).first")
    	  .Define("HCandPT",   "Minv2(goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]]).second")
    	  .Define("x_pt", "goodX_pt[index_pair[0]]")
    	  .Define("k1_pt", "goodX_trk1_pt[index_pair[0]]")
    	  .Define("k2_pt", "goodX_trk2_pt[index_pair[0]]")
    	  .Define("photon_pt", "goodPhotons_pt[index_pair[1]]")
 
    	  .Define("jet_mask1", "cleaningMask(Muon_jetIdx[fake_mu],nJet)")
    	  .Define("jet_mask2", "cleaningMask(Electron_jetIdx[fake_el],nJet)")
    	  .Define("jet_mask3", "cleaningMask(Photon_jetIdx[goodPhotons],nJet)")
    	  .Define("goodloose_jet", "abs(Jet_eta) < 2.5 && Jet_pt > 20 && jet_mask0 && jet_mask1 && jet_mask2 && jet_mask3")
    	  .Define("good_jet"	 , "abs(Jet_eta) < 5.0 && Jet_pt > 30 && jet_mask0 && jet_mask1 && jet_mask2 && jet_mask3 && Jet_jetId > 0 && Jet_puId > 0")
    	  .Define("goodvbs_jet"  , "abs(Jet_eta) < 5.0 && Jet_pt > 30 && jet_mask0 && jet_mask1 && jet_mask2 && jet_mask3 && Jet_jetId > 0 && Jet_puId > 0")
    	  .Define("ngood_jets", "Sum(good_jet)*1.0f")
    	  .Define("ngoodvbs_jets", "Sum(goodvbs_jet)*1.0f")
    	  .Define("goodvbsjet_pt",    "Jet_pt[goodvbs_jet]")
    	  .Define("goodvbsjet_eta",   "Jet_eta[goodvbs_jet]")
    	  .Define("goodvbsjet_phi",   "Jet_phi[goodvbs_jet]")
    	  .Define("goodvbsjet_mass",  "Jet_mass[goodvbs_jet]")
    	  .Define("mjj",   "compute_jet_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, 0)")
    	  .Define("ptjj",  "compute_jet_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, 1)")
    	  .Define("detajj","compute_jet_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, 2)")
    	  .Define("dphijj","compute_jet_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, 3)")
    	  .Define("ptj1",  "compute_jet_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, 4)")
    	  .Define("ptj2",  "compute_jet_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, 5)")
    	  .Define("etaj1", "compute_jet_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, 6)")
    	  .Define("etaj2", "compute_jet_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, 7)")
    	  .Define("zepvv",    "compute_jet_x_gamma_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], 0)")
    	  .Define("zepmax",   "compute_jet_x_gamma_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], 1)")
    	  .Define("sumHT",    "compute_jet_x_gamma_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], 2)")
    	  .Define("ptvv",     "compute_jet_x_gamma_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], 3)")
    	  .Define("pttot",    "compute_jet_x_gamma_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], 4)")
    	  .Define("detavvj1", "compute_jet_x_gamma_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], 5)")
    	  .Define("detavvj2", "compute_jet_x_gamma_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], 6)")
    	  .Define("ptbalance","compute_jet_x_gamma_var(goodvbsjet_pt, goodvbsjet_eta, goodvbsjet_phi, goodvbsjet_mass, goodX_pt[index_pair[0]],goodX_eta[index_pair[0]],goodX_phi[index_pair[0]],goodX_mass[index_pair[0]],goodPhotons_pt[index_pair[1]],goodPhotons_eta[index_pair[1]],goodPhotons_phi[index_pair[1]], 7)")
    	  .Define("goodloosejet_pt", "Jet_pt[goodloose_jet]")
    	  .Define("goodloosejet_eta", "abs(Jet_eta[goodloose_jet])")
    	  .Define("goodloosejet_btagDeepB", "Jet_btagDeepB[goodloose_jet]")
    	  .Define("goodloose_bjet", "goodloosejet_btagDeepB > 0.2783")
    	  .Define("nbtagloosejet", "Sum(goodloose_bjet)")
    	  )
    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob,whichSel,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6} / {7}".format(count,category,weight,year,PDType,isData,whichJob,whichSel))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo = [[0 for y in range(nCat)] for x in range(nHisto)]

    ROOT.initHisto2D(histoFakeEtaPt_mu,0)
    ROOT.initHisto2D(histoFakeEtaPt_el,1)
    ROOT.initHisto2D(histoLepSFEtaPt_mu,2)
    ROOT.initHisto2D(histoLepSFEtaPt_el,3)
    ROOT.initHisto2D(histoTriggerSFEtaPt_0_0, 4)
    ROOT.initHisto2D(histoTriggerSFEtaPt_0_1, 5)
    ROOT.initHisto2D(histoTriggerSFEtaPt_0_2, 6)
    ROOT.initHisto2D(histoTriggerSFEtaPt_0_3, 7)
    ROOT.initHisto2D(histoTriggerSFEtaPt_1_0, 8)
    ROOT.initHisto2D(histoTriggerSFEtaPt_1_1, 9)
    ROOT.initHisto2D(histoTriggerSFEtaPt_1_2,10)
    ROOT.initHisto2D(histoTriggerSFEtaPt_1_3,11)
    ROOT.initHisto2D(histoTriggerSFEtaPt_2_0,12)
    ROOT.initHisto2D(histoTriggerSFEtaPt_2_1,13)
    ROOT.initHisto2D(histoTriggerSFEtaPt_2_2,14)
    ROOT.initHisto2D(histoTriggerSFEtaPt_2_3,15)
    ROOT.initHisto2D(histoTriggerSFEtaPt_3_0,16)
    ROOT.initHisto2D(histoTriggerSFEtaPt_3_1,17)
    ROOT.initHisto2D(histoTriggerSFEtaPt_3_2,18)
    ROOT.initHisto2D(histoTriggerSFEtaPt_3_3,19)
    ROOT.initHisto2D(histoBTVEffEtaPtLF,20)
    ROOT.initHisto2D(histoBTVEffEtaPtCJ,21)
    ROOT.initHisto2D(histoBTVEffEtaPtBJ,22)
    ROOT.initHisto2F(histoElRecoSF,0)
    ROOT.initHisto2F(histoElSelSF,1)
    ROOT.initHisto2F(histoMuIDSF,2)
    ROOT.initHisto2F(histoMuISOSF,3)
    ROOT.initHisto1D(puWeights,0)

    ROOT.initJSONSFs(2018)

    ROOT.gInterpreter.ProcessLine('''
    TMVA::Experimental::RReader model("weights_mva/bdt_BDTG_vbfinc_v0.weights.xml");
    computeModel = TMVA::Experimental::Compute<15, float>(model);
    ''')

    variables = ROOT.model.GetVariableNames()
    print(variables)

    dftag = selectionLL(df,year,PDType,isData,whichSel)

    if(theCat == plotCategory("kPlotData")):
        dfbase =(dftag.Define("weight","1.0")
                      )

    else:
        dfbase = (dftag.Define("PDType","\"{0}\"".format(PDType))
                       .Define("fakemu_genPartFlav","Muon_genPartFlav[loose_mu]")
                       .Define("fakeel_genPartFlav","Electron_genPartFlav[loose_el]")
                       .Define("goodloosejet_hadronFlavour","Jet_hadronFlavour[goodloose_jet]")
                       .Define("weightMC","compute_weights({0},genWeight,PDType,fakemu_genPartFlav,fakeel_genPartFlav,0)".format(weight))
                       .Filter("weightMC != 0","MC weight")
                       .Define("weight"           ,"weightMC")
                       )

    dfbase = (dfbase.Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                    .Define("theCat","compute_category({0},kPlotNonPrompt,0,0)".format(theCat))
		    .Define("bdt_vbfinc", ROOT.computeModel, ROOT.model.GetVariableNames())
                    )

    dfcat = []
    dfjjcat = []
    dfvbscat = []
    dfvbs0cat = []
    dfvbs1cat = []
    for x in range(nCat):
        dfcat.append(dfbase.Filter("theCat=={0}".format(x), "correct category ({0})".format(x)))

        dfjjcat.append(dfcat[x].Filter("ngoodvbs_jets >= 2", "At least two VBS jets"))

        dfvbscat.append(dfjjcat[x] .Filter(VBSSEL, "VBS selection"))

        dfvbscat[x] = dfvbscat[x].Filter("triggerVBF>0||triggerKKG>0","triggerVBF>0||triggerKKG>0")

        dfvbs0cat.append(dfvbscat[x].Filter("triggerVBF>0","triggerVBF>0"))
        dfvbs1cat.append(dfvbscat[x].Filter("triggerVBF==0&&triggerKKG>0","triggerVBF==0&&triggerKKG>0"))

        histo[ 0][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x),100, 50, 150), "HCandMass","weight")
        histo[ 1][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x),100, 50, 150), "HCandMass","weight")
        histo[ 2][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x),40,-1,1), "bdt_vbfinc","weight")
        histo[ 3][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x),40,-1,1), "bdt_vbfinc","weight")
        histo[ 4][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x),40,0,200), "x_pt","weight")
        histo[ 5][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x),40,0,200), "x_pt","weight")
        histo[ 6][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x),40,10,210), "photon_pt","weight")
        histo[ 7][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x),40,10,210), "photon_pt","weight")
        histo[ 8][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x),40,300,2300), "mjj","weight")
        histo[ 9][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x),40,300,2300), "mjj","weight")
        histo[10][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x),40,2,8), "detajj","weight")
        histo[11][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x),40,2,8), "detajj","weight")
        histo[12][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x),40,30,430), "ptj1","weight")
        histo[13][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x),40,30,430), "ptj1","weight")
        histo[14][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x),40,30,430), "ptj2","weight")
        histo[15][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x),40,30,430), "ptj2","weight")
        histo[16][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x),40,0,200), "k1_pt","weight")
        histo[17][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format(17,x), "histo_{0}_{1}".format(17,x),40,0,200), "k1_pt","weight")
        histo[18][x] = dfvbs0cat[x].Histo1D(("histo_{0}_{1}".format(18,x), "histo_{0}_{1}".format(18,x),40,0,200), "k2_pt","weight")
        histo[19][x] = dfvbs1cat[x].Histo1D(("histo_{0}_{1}".format(19,x), "histo_{0}_{1}".format(19,x),40,0,200), "k2_pt","weight")

        histo[100][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(100,x), "histo_{0}_{1}".format(100,x),4,-0.5,3.5), "test0Photons_cutBased","weight")
        histo[101][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(101,x), "histo_{0}_{1}".format(101,x),2,-0.5,1.5), "test0Photons_mvaID_WP80","weight")
        histo[102][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(102,x), "histo_{0}_{1}".format(102,x),2,-0.5,1.5), "test0Photons_mvaID_WP90","weight")
        histo[103][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(103,x), "histo_{0}_{1}".format(103,x),100,-1,1), "test0Photons_mvaID","weight")
        histo[104][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(104,x), "histo_{0}_{1}".format(104,x),100,0,1), "test0Photons_pfRelIso03_all","weight")
        histo[105][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(105,x), "histo_{0}_{1}".format(105,x),100,0,1), "test0Photons_pfRelIso03_chg","weight")
        histo[106][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(106,x), "histo_{0}_{1}".format(106,x),100,0,0.1), "test0Photons_hoe","weight")
        histo[107][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(107,x), "histo_{0}_{1}".format(107,x),100,0.5,1), "test0Photons_r9","weight")
        histo[108][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(108,x), "histo_{0}_{1}".format(108,x),60,0.000,0.060), "test0Photons_sieie","weight")

        histo[110][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(110,x), "histo_{0}_{1}".format(110,x),4,-0.5,3.5), "test1Photons_cutBased","weight")
        histo[111][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(111,x), "histo_{0}_{1}".format(111,x),2,-0.5,1.5), "test1Photons_mvaID_WP80","weight")
        histo[112][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(112,x), "histo_{0}_{1}".format(112,x),2,-0.5,1.5), "test1Photons_mvaID_WP90","weight")
        histo[113][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(113,x), "histo_{0}_{1}".format(113,x),100,-1,1), "test1Photons_mvaID","weight")
        histo[114][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(114,x), "histo_{0}_{1}".format(114,x),100,0,1), "test1Photons_pfRelIso03_all","weight")
        histo[115][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(115,x), "histo_{0}_{1}".format(115,x),100,0,1), "test1Photons_pfRelIso03_chg","weight")
        histo[116][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(116,x), "histo_{0}_{1}".format(116,x),100,0,0.1), "test1Photons_hoe","weight")
        histo[117][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(117,x), "histo_{0}_{1}".format(117,x),100,0.5,1), "test1Photons_r9","weight")
        histo[118][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(118,x), "histo_{0}_{1}".format(118,x),60,0.000,0.060), "test1Photons_sieie","weight")

        histo[120][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(120,x), "histo_{0}_{1}".format(120,x),4,-0.5,3.5), "test2Photons_cutBased","weight")
        histo[121][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(121,x), "histo_{0}_{1}".format(121,x),2,-0.5,1.5), "test2Photons_mvaID_WP80","weight")
        histo[122][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(122,x), "histo_{0}_{1}".format(122,x),2,-0.5,1.5), "test2Photons_mvaID_WP90","weight")
        histo[123][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(123,x), "histo_{0}_{1}".format(123,x),100,-1,1), "test2Photons_mvaID","weight")
        histo[124][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(124,x), "histo_{0}_{1}".format(124,x),100,0,1), "test2Photons_pfRelIso03_all","weight")
        histo[125][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(125,x), "histo_{0}_{1}".format(125,x),100,0,1), "test2Photons_pfRelIso03_chg","weight")
        histo[126][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(126,x), "histo_{0}_{1}".format(126,x),100,0,0.1), "test2Photons_hoe","weight")
        histo[127][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(127,x), "histo_{0}_{1}".format(127,x),100,0.5,1), "test2Photons_r9","weight")
        histo[128][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(128,x), "histo_{0}_{1}".format(128,x),60,0.000,0.060), "test2Photons_sieie","weight")

        histo[130][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(130,x), "histo_{0}_{1}".format(130,x),4,-0.5,3.5), "test3Photons_cutBased","weight")
        histo[131][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(131,x), "histo_{0}_{1}".format(131,x),2,-0.5,1.5), "test3Photons_mvaID_WP80","weight")
        histo[132][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(132,x), "histo_{0}_{1}".format(132,x),2,-0.5,1.5), "test3Photons_mvaID_WP90","weight")
        histo[133][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(133,x), "histo_{0}_{1}".format(133,x),100,-1,1), "test3Photons_mvaID","weight")
        histo[134][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(134,x), "histo_{0}_{1}".format(134,x),100,0,1), "test3Photons_pfRelIso03_all","weight")
        histo[135][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(135,x), "histo_{0}_{1}".format(135,x),100,0,1), "test3Photons_pfRelIso03_chg","weight")
        histo[136][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(136,x), "histo_{0}_{1}".format(136,x),100,0,0.1), "test3Photons_hoe","weight")
        histo[137][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(137,x), "histo_{0}_{1}".format(137,x),100,0.5,1), "test3Photons_r9","weight")
        histo[138][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(138,x), "histo_{0}_{1}".format(138,x),60,0.000,0.060), "test3Photons_sieie","weight")


    report = []
    for x in range(nCat):
        report.append(dfvbscat[x].Report())
        if(x != theCat): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    myfile = ROOT.TFile("fillhistoXGAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            if(histo[j][i].GetSumOfWeights() == 0): continue
            histo[j][i].Write()
    myfile.Close()

def readMCSample(sampleNOW,year,skimType,whichJob,whichSel,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    files = getMClist(sampleNOW, skimType)
    print("Total files: {0}".format(len(files)))

    now = time.time()
    rdfRunTree = ROOT.RDataFrame("Runs", files)
    genEventSumWeight = rdfRunTree.Sum("genEventSumw").GetValue()
    genEventSumNoWeight = rdfRunTree.Sum("genEventCount").GetValue()
    print("TIME {0}".format(time.time()-now))

    weight = (SwitchSample(sampleNOW, skimType)[1] / genEventSumWeight)*lumi[year-2016]
    weightApprox = (SwitchSample(sampleNOW, skimType)[1] / genEventSumNoWeight)*lumi[year-2016]

    if(whichJob != -1):
        groupedFile = groupFiles(files, group)
        files = groupedFile[whichJob]
        if(len(files) == 0):
            print("no files in job/group: {0} / {1}".format(whichJob, group))
            return 0
        print("Used files: {0}".format(len(files)))

    df = ROOT.RDataFrame("Events", files)
    nevents = df.Count().GetValue()

    print("genEventSum({0}): {1} / Events(total/ntuple): {2} / {3}".format(rdfRunTree.Count().GetValue(),genEventSumWeight,genEventSumNoWeight,nevents))
    print("WeightExact/Approx %f / %f / Cross section: %f" %(weight, weightApprox, SwitchSample(sampleNOW, skimType)[1]))

    PDType = os.path.basename(SwitchSample(sampleNOW, skimType)[0]).split('+')[0]

    analysis(df,sampleNOW,SwitchSample(sampleNOW,skimType)[2],weight,year,PDType,"false",whichJob,whichSel,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

def readDASample(sampleNOW,year,skimType,whichJob,whichSel,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    PDType = "0"
    if  (sampleNOW >= 1001 and sampleNOW <= 1004): PDType = "SingleMuon"
    elif(sampleNOW >= 1005 and sampleNOW <= 1008): PDType = "DoubleMuon"
    elif(sampleNOW >= 1009 and sampleNOW <= 1012): PDType = "MuonEG"
    elif(sampleNOW >= 1012 and sampleNOW <= 1016): PDType = "EGamma"

    files = getDATAlist(sampleNOW, year, skimType)
    print("Total files: {0}".format(len(files)))

    if(whichJob != -1):
        groupedFile = groupFiles(files, group)
        files = groupedFile[whichJob]
        if(len(files) == 0):
            print("no files in job/group: {0} / {1}".format(whichJob, group))
            return 0
        print("Used files: {0}".format(len(files)))

    df = ROOT.RDataFrame("Events", files)

    weight=1.
    nevents = df.Count().GetValue()
    print("%s entries in the dataset" %nevents)

    analysis(df,sampleNOW,sampleNOW,weight,year,PDType,"true",whichJob,whichSel,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

if __name__ == "__main__":

    group = 10

    skimType = "3l"
    year = 2018
    process = -1
    whichJob = -1
    whichSel = 0

    valid = ['year=', "process=", 'whichJob=', 'whichSel=', 'help']
    usage  =  "Usage: ana.py --year=<{0}>\n".format(year)
    usage +=  "              --process=<{0}>\n".format(process)
    usage +=  "              --whichJob=<{0}>".format(whichJob)
    usage +=  "              --whichSel=<{0}>".format(whichSel)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", valid)
    except getopt.GetoptError as ex:
        print(usage)
        print(str(ex))
        sys.exit(1)

    for opt, arg in opts:
        if opt == "--help":
            print(usage)
            sys.exit(1)
        if opt == "--year":
            year = int(arg)
        if opt == "--process":
            process = int(arg)
        if opt == "--whichJob":
            whichJob = int(arg)
        if opt == "--whichSel":
            whichSel = int(arg)

    puPath = "data/puWeights_UL_{0}.root".format(year)
    if(not os.path.exists(puPath)):
        puPath = "puWeights_UL_{0}.root".format(year)
    fPuFile = ROOT.TFile(puPath)
    puWeights = fPuFile.Get("puWeights")
    puWeights.SetDirectory(0)
    fPuFile.Close()

    recoElPath = "data/electronReco_UL_{0}.root".format(year)
    if(not os.path.exists(recoElPath)):
        recoElPath = "electronReco_UL_{0}.root".format(year)
    fRecoElFile = ROOT.TFile(recoElPath)
    histoElRecoSF = fRecoElFile.Get("EGamma_SF2D")
    histoElRecoSF.SetDirectory(0)
    fRecoElFile.Close()

    selElPath = "data/electronMediumID_UL_{0}.root".format(year)
    if(not os.path.exists(selElPath)):
        selElPath = "electronMediumID_UL_{0}.root".format(year)
    fSelElFile = ROOT.TFile(selElPath)
    histoElSelSF = fSelElFile.Get("EGamma_SF2D")
    histoElSelSF.SetDirectory(0)
    fSelElFile.Close()

    idMuPath = "data/Efficiencies_muon_generalTracks_Z_Run{0}_UL_ID.root".format(year)
    if(not os.path.exists(idMuPath)):
        idMuPath = "Efficiencies_muon_generalTracks_Z_Run{0}_UL_ID.root".format(year)
    fidMuFile = ROOT.TFile(idMuPath)
    histoMuIDSF = fidMuFile.Get("NUM_MediumID_DEN_TrackerMuons_abseta_pt")
    histoMuIDSF.SetDirectory(0)
    fidMuFile.Close()

    isoMuPath = "data/Efficiencies_muon_generalTracks_Z_Run{0}_UL_ISO.root".format(year)
    if(not os.path.exists(isoMuPath)):
        isoMuPath = "Efficiencies_muon_generalTracks_Z_Run{0}_UL_ISO.root".format(year)
    fisoMuFile = ROOT.TFile(isoMuPath)
    histoMuISOSF = fisoMuFile.Get("NUM_TightRelIso_DEN_MediumID_abseta_pt")
    histoMuISOSF.SetDirectory(0)
    fisoMuFile.Close()

    fakePath = "data/histoFakeEtaPt_{0}_anaType3.root".format(year)
    if(not os.path.exists(fakePath)):
        fakePath = "histoFakeEtaPt_{0}_anaType3.root".format(year)
    fFakeFile = ROOT.TFile(fakePath)
    histoFakeEtaPt_mu = fFakeFile.Get("histoFakeEffSelEtaPt_0_0")
    histoFakeEtaPt_el = fFakeFile.Get("histoFakeEffSelEtaPt_1_0")
    histoFakeEtaPt_mu.SetDirectory(0)
    histoFakeEtaPt_el.SetDirectory(0)
    fFakeFile.Close()

    lepSFPath = "data/histoLepSFEtaPt_{0}.root".format(year)
    if(not os.path.exists(lepSFPath)):
        lepSFPath = "histoLepSFEtaPt_{0}.root".format(year)
    fLepSFFile = ROOT.TFile(lepSFPath)
    histoLepSFEtaPt_mu = fLepSFFile.Get("histoLepSFEtaPt_0_0")
    histoLepSFEtaPt_el = fLepSFFile.Get("histoLepSFEtaPt_1_0")
    histoLepSFEtaPt_mu.SetDirectory(0)
    histoLepSFEtaPt_el.SetDirectory(0)
    fLepSFFile.Close()

    triggerSFPath = "data/histoTriggerSFEtaPt_{0}.root".format(year)
    if(not os.path.exists(triggerSFPath)):
        triggerSFPath = "histoTriggerSFEtaPt_{0}.root".format(year)
    fTriggerSFFile = ROOT.TFile(triggerSFPath)
    histoTriggerSFEtaPt_0_0 = fTriggerSFFile.Get("histoTriggerSFEtaPt_0_0")
    histoTriggerSFEtaPt_0_1 = fTriggerSFFile.Get("histoTriggerSFEtaPt_0_1")
    histoTriggerSFEtaPt_0_2 = fTriggerSFFile.Get("histoTriggerSFEtaPt_0_2")
    histoTriggerSFEtaPt_0_3 = fTriggerSFFile.Get("histoTriggerSFEtaPt_0_3")
    histoTriggerSFEtaPt_1_0 = fTriggerSFFile.Get("histoTriggerSFEtaPt_1_0")
    histoTriggerSFEtaPt_1_1 = fTriggerSFFile.Get("histoTriggerSFEtaPt_1_1")
    histoTriggerSFEtaPt_1_2 = fTriggerSFFile.Get("histoTriggerSFEtaPt_1_2")
    histoTriggerSFEtaPt_1_3 = fTriggerSFFile.Get("histoTriggerSFEtaPt_1_3")
    histoTriggerSFEtaPt_2_0 = fTriggerSFFile.Get("histoTriggerSFEtaPt_2_0")
    histoTriggerSFEtaPt_2_1 = fTriggerSFFile.Get("histoTriggerSFEtaPt_2_1")
    histoTriggerSFEtaPt_2_2 = fTriggerSFFile.Get("histoTriggerSFEtaPt_2_2")
    histoTriggerSFEtaPt_2_3 = fTriggerSFFile.Get("histoTriggerSFEtaPt_2_3")
    histoTriggerSFEtaPt_3_0 = fTriggerSFFile.Get("histoTriggerSFEtaPt_3_0")
    histoTriggerSFEtaPt_3_1 = fTriggerSFFile.Get("histoTriggerSFEtaPt_3_1")
    histoTriggerSFEtaPt_3_2 = fTriggerSFFile.Get("histoTriggerSFEtaPt_3_2")
    histoTriggerSFEtaPt_3_3 = fTriggerSFFile.Get("histoTriggerSFEtaPt_3_3")
    histoTriggerSFEtaPt_0_0.SetDirectory(0)
    histoTriggerSFEtaPt_0_1.SetDirectory(0)
    histoTriggerSFEtaPt_0_2.SetDirectory(0)
    histoTriggerSFEtaPt_0_3.SetDirectory(0)
    histoTriggerSFEtaPt_1_0.SetDirectory(0)
    histoTriggerSFEtaPt_1_1.SetDirectory(0)
    histoTriggerSFEtaPt_1_2.SetDirectory(0)
    histoTriggerSFEtaPt_1_3.SetDirectory(0)
    histoTriggerSFEtaPt_2_0.SetDirectory(0)
    histoTriggerSFEtaPt_2_1.SetDirectory(0)
    histoTriggerSFEtaPt_2_2.SetDirectory(0)
    histoTriggerSFEtaPt_2_3.SetDirectory(0)
    histoTriggerSFEtaPt_3_0.SetDirectory(0)
    histoTriggerSFEtaPt_3_1.SetDirectory(0)
    histoTriggerSFEtaPt_3_2.SetDirectory(0)
    histoTriggerSFEtaPt_3_3.SetDirectory(0)
    fTriggerSFFile.Close()

    BTVEffPath = "data/histoBtagEffSelEtaPt_{0}.root".format(year)
    if(not os.path.exists(BTVEffPath)):
        BTVEffPath = "histoBtagEffSelEtaPt_{0}.root".format(year)
    fBTVEffPathFile = ROOT.TFile(BTVEffPath)
    histoBTVEffEtaPtLF = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_3")
    histoBTVEffEtaPtCJ = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_4")
    histoBTVEffEtaPtBJ = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_5")
    histoBTVEffEtaPtLF.SetDirectory(0)
    histoBTVEffEtaPtCJ.SetDirectory(0)
    histoBTVEffEtaPtBJ.SetDirectory(0)
    fBTVEffPathFile.Close()

    try:
        if(process >= 0 and process < 1000):
            readMCSample(process,year,skimType,whichJob,whichSel,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
        elif(process > 1000):
            readDASample(process,year,skimType,whichJob,whichSel,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
    except Exception as e:
        print("Error sample: {0}".format(e))

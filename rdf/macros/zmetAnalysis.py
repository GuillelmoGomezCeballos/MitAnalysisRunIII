import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(3)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson

lumi = [36.1, 41.5, 60.0]

selectionJsonPath = "config/selection.json"
if(not os.path.exists(selectionJsonPath)):
    selectionJsonPath = "selection.json"

with open(selectionJsonPath) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

BARRELphotons = jsonObject['BARRELphotons']
ENDCAPphotons = jsonObject['ENDCAPphotons']

JSON = jsonObject['JSON']

VBSSEL = jsonObject['VBSSEL']

FAKE_MU   = jsonObject['FAKE_MU']
TIGHT_MU0 = jsonObject['TIGHT_MU0']
TIGHT_MU1 = jsonObject['TIGHT_MU1']
TIGHT_MU2 = jsonObject['TIGHT_MU2']
TIGHT_MU3 = jsonObject['TIGHT_MU3']
TIGHT_MU4 = jsonObject['TIGHT_MU4']
TIGHT_MU5 = jsonObject['TIGHT_MU5']
TIGHT_MU6 = jsonObject['TIGHT_MU6']
TIGHT_MU7 = jsonObject['TIGHT_MU7']

FAKE_EL   = jsonObject['FAKE_EL']
TIGHT_EL0 = jsonObject['TIGHT_EL0']
TIGHT_EL1 = jsonObject['TIGHT_EL1']
TIGHT_EL2 = jsonObject['TIGHT_EL2']
TIGHT_EL3 = jsonObject['TIGHT_EL3']
TIGHT_EL4 = jsonObject['TIGHT_EL4']
TIGHT_EL5 = jsonObject['TIGHT_EL5']
TIGHT_EL6 = jsonObject['TIGHT_EL6']
TIGHT_EL7 = jsonObject['TIGHT_EL7']

def selectionLL(df,year,PDType,isData):

    overallTriggers = jsonObject['triggers']
    TRIGGERMUEG = getTriggerFromJson(overallTriggers, "TRIGGERMUEG", year)
    TRIGGERDMU  = getTriggerFromJson(overallTriggers, "TRIGGERDMU", year)
    TRIGGERSMU  = getTriggerFromJson(overallTriggers, "TRIGGERSMU", year)
    TRIGGERDEL  = getTriggerFromJson(overallTriggers, "TRIGGERDEL", year)
    TRIGGERSEL  = getTriggerFromJson(overallTriggers, "TRIGGERSEL", year)

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
              .Define("trigger","{0}".format(TRIGGERLEP))
              .Filter("trigger > 0","Passed trigger")

              .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")
              .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")
              .Filter("Sum(loose_mu)+Sum(loose_el) == 2","Three loose leptons")

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
              .Define("tight_mu"          ,"{0}".format(TIGHT_MU0))

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
              .Define("tight_el"                  ,"{0}".format(TIGHT_EL0))

              .Define("nFake","Sum(fake_mu)+Sum(fake_el)")
              .Define("nTight","Sum(tight_mu)+Sum(tight_el)")
              .Filter("nFake == 2","Two fake leptons")
              .Filter("nTight == 2","Two tight leptons")
              .Filter("Sum(fakemu_charge)+Sum(fakeel_charge) == 0", "Opposite-sign leptons")

              .Define("good_tau", "abs(Tau_eta) < 2.3 && Tau_pt > 20 && ((Tau_idDeepTau2017v2p1VSe & 8) != 0) && ((Tau_idDeepTau2017v2p1VSjet & 16) != 0) && ((Tau_idDeepTau2017v2p1VSmu & 8) != 0)")
              .Filter("Sum(good_tau) == 0","No selected hadronic taus")

              .Define("mll",    "compute_ll_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass,0)")
              .Define("DiLepton_flavor", "Sum(fake_mu)+2*Sum(fake_el)-2")
              .Filter("abs(mll-91.1876) < 15","abs(mll-mZ)<15")
              .Define("ptll",   "compute_ll_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass,1)")
              .Filter("MET_pt > 60 && ptll > 60","met > 60 && ptll > 60")

              .Define("drll",   "compute_ll_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass,2)")
              .Define("dphill", "compute_ll_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass,3)")
              .Define("ptl1",   "compute_ll_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass,4)")
              .Define("ptl2",   "compute_ll_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass,5)")
              .Define("etal1",  "abs(compute_ll_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass,6))")
              .Define("etal2",  "abs(compute_ll_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass,7))")
              .Define("ltype",  "compute_nl_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi,2)")

              .Filter("ptl1 > 25 && ptl2 > 20","ptl1 > 25 && ptl2 > 20")

              .Define("jet_mask1", "cleaningMask(Muon_jetIdx[fake_mu],nJet)")
              .Define("jet_mask2", "cleaningMask(Electron_jetIdx[fake_el],nJet)")

              .Define("goodloose_jet", "abs(Jet_eta) < 2.5 && Jet_pt > 20 && jet_mask1 && jet_mask2")
              .Define("goodloosejet_pt", "Jet_pt[goodloose_jet]")
              .Define("goodloosejet_eta", "abs(Jet_eta[goodloose_jet])")
              .Define("goodloosejet_btagDeepB", "Jet_btagDeepB[goodloose_jet]")
              .Define("goodloose_bjet", "goodloosejet_btagDeepB > 0.7100")
              .Define("nbtagloosejet", "Sum(goodloose_bjet)")
 
              .Define("good_jet"     , "abs(Jet_eta) < 5.0 && Jet_pt > 30 && jet_mask1 && jet_mask2 && Jet_puId > 0 && Jet_puId > 0")
              .Define("ngood_jets", "Sum(good_jet)")
              .Define("goodjet_pt",    "Jet_pt[good_jet]")
              .Define("goodjet_eta",   "Jet_eta[good_jet]")
              .Define("goodjet_phi",   "Jet_phi[good_jet]")
              .Define("goodjet_mass",  "Jet_mass[good_jet]")
              .Define("mjj",    "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 0)")
              .Define("ptjj",   "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 1)")
              .Define("detajj", "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 2)")
              .Define("dphijj", "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 3)")

              .Define("ptbalance", "compute_met_lepton_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, 0)")
              .Define("ptjbalance","compute_met_lepton_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, 1)")
              .Define("dphillmet", "compute_met_lepton_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, 2)")
              .Define("dphilljmet","compute_met_lepton_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, 3)")
              .Define("mt",        "compute_met_lepton_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, 4)")
              .Define("jetPtFrac", "compute_met_lepton_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, 5)")
              .Define("dphijmet",  "compute_met_lepton_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, 6)")

              .Define("photon_mask", "cleaningMask(Electron_photonIdx[fake_el],nPhoton)")
              .Define("goodPhotons", "{}".format(BARRELphotons)+" or {}".format(ENDCAPphotons) )
              .Define("goodPhotons_pt", "Photon_pt[goodPhotons]")
              .Define("goodPhotons_eta", "Photon_eta[goodPhotons]")
              .Define("goodPhotons_phi", "Photon_phi[goodPhotons]")

              .Define("ptgbalance", "compute_met_lepton_gamma_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, goodPhotons_pt, goodPhotons_eta, goodPhotons_phi, 0)")
              .Define("ptgjbalance","compute_met_lepton_gamma_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, goodPhotons_pt, goodPhotons_eta, goodPhotons_phi, 1)")
              .Define("dphillgmet", "compute_met_lepton_gamma_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, goodPhotons_pt, goodPhotons_eta, goodPhotons_phi, 2)")
              .Define("dphillgjmet","compute_met_lepton_gamma_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, goodPhotons_pt, goodPhotons_eta, goodPhotons_phi, 3)")
              .Define("mtg",        "compute_met_lepton_gamma_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, goodPhotons_pt, goodPhotons_eta, goodPhotons_phi, 4)")
              .Define("jetPtgFrac", "compute_met_lepton_gamma_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, MET_pt, MET_phi, goodPhotons_pt, goodPhotons_eta, goodPhotons_phi, 5)")

              )

    return dftag

def analysis(df,count,category,weight,year,PDType,isData,whichJob,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    xPtbins = array('d', [10,15,20,25,30,35,40,50,60,70,85,100,200,1000])
    xEtabins = array('d', [0.0,1.0,1.5,2.0,2.5])

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")
    elif(theCat == plotCategory("kPlotqqWW") or theCat == plotCategory("kPlotggWW") or
         theCat == plotCategory("kPlotTop") or theCat == plotCategory("kPlotHiggs")):
        theCat = plotCategory("kPlotEM")
    elif(theCat == plotCategory("kPlotTVX")):
        theCat = plotCategory("kPlotVVV")

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo   = [[0 for y in range(nCat)] for x in range(nHisto)]
    histo2D = [[0 for y in range(nCat)] for x in range(nHisto)]

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

    dftag = selectionLL(df,year,PDType,isData)

    if(theCat == plotCategory("kPlotData")):
        dfbase =(dftag.Define("weightNoPURecoSF","1.0")
                      .Define("weightNoLepSF","1.0")
                      .Define("weightNoTriggerSF","1.0")
                      .Define("weightNoBTVSF","1.0")
                      .Define("weight","1.0")
                      )

    else:
        dfbase = (dftag.Define("PDType","\"{0}\"".format(PDType))
                       #.Define("weightsTest1", ROOT.WeightsComputer(histoFakeEtaPt_mu), ("fakemu_pt", "fakemu_eta"))
                       #.Filter("weightsTest1 >= 0","good fake weight1")
                       .Define("goodloosejet_hadronFlavour","Jet_hadronFlavour[goodloose_jet]")
                       .Define("fakemu_genPartFlav","Muon_genPartFlav[fake_mu]")
                       .Define("fakeel_genPartFlav"        ,"Electron_genPartFlav[fake_el]")
                       .Define("weightPURecoSF","compute_PURecoSF(fakemu_pt,fakemu_eta,fakeel_pt,fakeel_eta,Pileup_nTrueInt)")
                       .Filter("weightPURecoSF > 0","good PURecoSF weight")
                       .Define("weightLepSF","compute_LepSF(fakemu_pt,fakemu_eta,fakeel_pt,fakeel_eta)")
                       .Filter("weightLepSF > 0","good LepSF weight")
                       .Define("weightTriggerSF","compute_TriggerSF(ptl1,ptl2,etal1,etal2,ltype)")
                       .Filter("weightTriggerSF > 0","good TriggerSF weight")
                       .Define("weightMC","compute_weights({0},genWeight,PDType,fakemu_genPartFlav,fakeel_genPartFlav,0)".format(weight))
                       .Filter("weightMC != 0","MC weight")
                       .Define("weightBtagSFJSON","compute_JSONS_BTV_SF(goodloosejet_pt,goodloosejet_eta,goodloosejet_btagDeepB,goodloosejet_hadronFlavour,0)")
                       .Filter("weightBtagSFJSON > 0","weightBtagSFJSON > 0")
                       .Define("weightLepSFJSON","compute_JSON_SFs(fakemu_pt,fakemu_eta,fakeel_pt,fakeel_eta)")
                       .Filter("weightLepSFJSON > 0","weightLepSFJSON > 0")
                       .Define("weight"           ,"weightPURecoSF*weightLepSF*weightTriggerSF*weightMC*weightBtagSFJSON")
                       .Define("weightNoPURecoSF" ,"weightLepSF*weightTriggerSF*weightMC*weightBtagSFJSON")
                       .Define("weightNoLepSF"    ,"weightPURecoSF*weightTriggerSF*weightMC*weightBtagSFJSON")
                       .Define("weightNoTriggerSF","weightPURecoSF*weightLepSF*weightMC*weightBtagSFJSON")
                       .Define("weightNoBTVSF"    ,"weightPURecoSF*weightLepSF*weightTriggerSF*weightMC")
                       )

    dfzllcat = []
    dfzllbcat = []
    dfzllgcat = []
    for x in range(nCat):
        for ltype in range(3):
            dfzllcat.append(dfbase.Filter("DiLepton_flavor=={0}".format(ltype), "flavor type == {0}".format(ltype))
                                  .Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                                  .Define("theCat{0}".format(x), "compute_category({0},kPlotNonPrompt,nFake,nTight)".format(theCat))
                                  .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x))
                                  )
            dfzllbcat.append(dfzllcat[3*x+ltype].Filter("nbtagloosejet > 0","at least one btagloosejet"))
            dfzllbcat[3*x+ltype] = dfzllbcat[3*x+ltype].Filter("ptbalance < 0.4","ptbalance < 0.4")
            dfzllbcat[3*x+ltype] = dfzllbcat[3*x+ltype].Filter("dphillmet > 2.5","dphillmet > 2.5")

            dfzllcat[3*x+ltype] = dfzllcat[3*x+ltype].Filter("nbtagloosejet == 0","no btagloosejet")

            dfzllgcat.append(dfzllcat[3*x+ltype].Filter("Sum(goodPhotons) > 0","At least one photon"))

            histo[ltype+30][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+30,x), "histo_{0}_{1}".format(ltype+30,x), 50, 0, 2), "ptbalance","weight")
            histo[ltype+33][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+33,x), "histo_{0}_{1}".format(ltype+33,x), 50, 0, 2), "ptjbalance","weight")

            dfzllcat[3*x+ltype] = dfzllcat[3*x+ltype].Filter("ptbalance < 0.4","ptbalance < 0.4")

            histo[ltype+36][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+36,x), "histo_{0}_{1}".format(ltype+36,x), 50, 0, 3.1416), "dphillmet","weight")
            histo[ltype+39][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+39,x), "histo_{0}_{1}".format(ltype+39,x), 50, 0, 3.1416), "dphilljmet","weight")

            dfzllcat[3*x+ltype] = dfzllcat[3*x+ltype].Filter("dphillmet > 2.5","dphillmet > 2.5")

            dfzllcat[3*x+ltype] = dfzllcat[3*x+ltype].Filter("MET_pt >  60 && (MET_significance > 20||jetPtFrac<0.2)","MET_pt > X1")

            histo[ltype+27][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+27,x), "histo_{0}_{1}".format(ltype+27,x), 50, 60, 260), "MET_pt","weight")

            dfzllcat[3*x+ltype] = dfzllcat[3*x+ltype].Filter("MET_pt > 100 && (MET_significance > 20||jetPtFrac<0.2)","MET_pt > X2")

            histo[ltype+ 0][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,x), "histo_{0}_{1}".format(ltype+ 0,x), 60, 91.1876-15, 91.1876+15), "mll","weight")
            histo[ltype+ 3][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 3,x), "histo_{0}_{1}".format(ltype+ 3,x), 50,  60, 260), "ptll","weight")
            histo[ltype+ 6][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,x), "histo_{0}_{1}".format(ltype+ 6,x), 50,  0, 5),   "drll","weight")
            histo[ltype+ 9][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 9,x), "histo_{0}_{1}".format(ltype+ 9,x), 50,  0, 3.1416), "dphill","weight")
            histo[ltype+12][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+12,x), "histo_{0}_{1}".format(ltype+12,x), 40,  0, 200), "ptl1","weight")
            histo[ltype+15][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+15,x), "histo_{0}_{1}".format(ltype+15,x), 40,  0, 200), "ptl2","weight")
            histo[ltype+18][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+18,x), "histo_{0}_{1}".format(ltype+18,x), 25,  0,2.5), "etal1","weight")
            histo[ltype+21][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+21,x), "histo_{0}_{1}".format(ltype+21,x), 25,  0,2.5), "etal2","weight")
            histo[ltype+24][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+24,x), "histo_{0}_{1}".format(ltype+24,x), 10,-0.5, 9.5), "ngood_jets","weight")
            histo[ltype+42][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+42,x), "histo_{0}_{1}".format(ltype+42,x), 50, 0, 3.1416), "dphijmet","weight")
            histo[ltype+45][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+45,x), "histo_{0}_{1}".format(ltype+45,x), 40,100, 500), "mt","weight")
            histo[ltype+84][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+84,x), "histo_{0}_{1}".format(ltype+84,x), 40,0,80), "MET_significance","weight")
            histo[ltype+87][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+87,x), "histo_{0}_{1}".format(ltype+87,x), 20,0,1), "jetPtFrac","weight")

            histo[ltype+48][x] =dfzllbcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+48,x), "histo_{0}_{1}".format(ltype+48,x), 40, 60, 260), "ptll","weight")
            histo[ltype+51][x] =dfzllbcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+51,x), "histo_{0}_{1}".format(ltype+51,x), 40,100, 300), "MET_pt","weight")
            histo[ltype+54][x] =dfzllbcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+54,x), "histo_{0}_{1}".format(ltype+54,x), 40,100, 500), "mt","weight")

            histo[ltype+57][x] = dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+57,x), "histo_{0}_{1}".format(ltype+57,x), 50, 0, 2), "ptgbalance","weight")
            histo[ltype+60][x] = dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+60,x), "histo_{0}_{1}".format(ltype+60,x), 50, 0, 2), "ptgjbalance","weight")

            dfzllgcat[3*x+ltype] = dfzllgcat[3*x+ltype].Filter("ptgbalance < 0.4","ptgbalance < 0.4")

            histo[ltype+63][x] = dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+63,x), "histo_{0}_{1}".format(ltype+63,x), 50, 0, 3.1416), "dphillgmet","weight")
            histo[ltype+66][x] = dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+66,x), "histo_{0}_{1}".format(ltype+66,x), 50, 0, 3.1416), "dphillgjmet","weight")

            dfzllgcat[3*x+ltype] = dfzllgcat[3*x+ltype].Filter("dphillgmet > 2.5","dphillgmet > 2.5")

            dfzllgcat[3*x+ltype] = dfzllgcat[3*x+ltype].Filter("MET_pt >  60 && (MET_significance > 20||jetPtgFrac<0.2)","MET_pt > X1")

            histo[ltype+69][x] =dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+69,x), "histo_{0}_{1}".format(ltype+69,x), 25, 60, 260), "MET_pt","weight")

            dfzllgcat[3*x+ltype] = dfzllgcat[3*x+ltype].Filter("MET_pt > 100 && (MET_significance > 20||jetPtgFrac<0.2)","MET_pt > X2")

            histo[ltype+72][x] =dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+72,x), "histo_{0}_{1}".format(ltype+72,x), 20,0,400), "mtg","weight")
            histo[ltype+75][x] =dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+75,x), "histo_{0}_{1}".format(ltype+75,x), 10,-0.5, 9.5), "ngood_jets","weight")
            histo[ltype+78][x] =dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+78,x), "histo_{0}_{1}".format(ltype+78,x), 40,0,80), "MET_significance","weight")
            histo[ltype+81][x] =dfzllgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+81,x), "histo_{0}_{1}".format(ltype+81,x), 20,0,1), "jetPtgFrac","weight")

            histo[ltype+96][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+96,x), "histo_{0}_{1}".format(ltype+96,x), 10,-0.5, 9.5), "ngood_jets","weightNoPURecoSF")
            histo[ltype+97][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+97,x), "histo_{0}_{1}".format(ltype+97,x), 10,-0.5, 9.5), "ngood_jets","weightNoLepSF")
            histo[ltype+98][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+98,x), "histo_{0}_{1}".format(ltype+98,x), 10,-0.5, 9.5), "ngood_jets","weightNoTriggerSF")
            histo[ltype+99][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+99,x), "histo_{0}_{1}".format(ltype+99,x), 10,-0.5, 9.5), "ngood_jets","weightNoBTVSF")

    reporta = []
    reportb = []
    for x in range(nCat):
        for ltype in range(3):
            reporta.append(dfzllcat[3*x+ltype].Report())
            reportb.append(dfzllgcat[3*x+ltype].Report())
            if(x != theCat): continue
            print("---------------- SUMMARY 3*{0}+{1} = {2} -------------".format(x,ltype,3*x+ltype))
            reporta[3*x+ltype].Print()
            print("-----------------------------")
            reportb[3*x+ltype].Print()

    myfile = ROOT.TFile("fillhistoZMETAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].Write()
    myfile.Close()

def readMCSample(sampleNOW,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    files = getMClist(sampleNOW, skimType)
    print("Total files: {0}".format(len(files)))

    rdfRunTree = ROOT.RDataFrame("Runs", files)
    genEventSumWeight = rdfRunTree.Sum("genEventSumw").GetValue()
    genEventSumNoWeight = rdfRunTree.Sum("genEventCount").GetValue()

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

    analysis(df,sampleNOW,SwitchSample(sampleNOW,skimType)[2],weight,year,PDType,"false",whichJob,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

def readDASample(sampleNOW,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

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

    analysis(df,sampleNOW,sampleNOW,weight,year,PDType,"true",whichJob,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

if __name__ == "__main__":

    group = 10

    skimType = "3l"
    year = 2018
    process = -1
    whichJob = -1

    valid = ['year=', "process=", 'whichJob=', 'help']
    usage  =  "Usage: ana.py --year=<{0}>\n".format(year)
    usage +=  "              --process=<{0}>\n".format(process)
    usage +=  "              --whichJob=<{0}>".format(whichJob)
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
    histoBTVEffEtaPtLF = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_0")
    histoBTVEffEtaPtCJ = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_1")
    histoBTVEffEtaPtBJ = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_2")
    histoBTVEffEtaPtLF.SetDirectory(0)
    histoBTVEffEtaPtCJ.SetDirectory(0)
    histoBTVEffEtaPtBJ.SetDirectory(0)
    fBTVEffPathFile.Close()

    try:
        if(process >= 0 and process < 1000):
            readMCSample(process,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
        elif(process > 1000):
            readDASample(process,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
    except Exception as e:
        print("Error sample: {0}".format(e))

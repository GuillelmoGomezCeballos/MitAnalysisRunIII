import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(3)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi

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

PHOTONSKIM = "Photon_pt > 20 && abs(Photon_eta) < 2.5 && Photon_electronVeto && Photon_pfChargedIsoPFPV*Photon_pt < 10 && cleaningBitmap(Photon_vidNestedWPBitmap,4,2) && cleaningBitmap(Photon_vidNestedWPBitmap,10,2) && cleaningBitmap(Photon_vidNestedWPBitmap,12,2)"

def selectionLL(df,year,PDType,isData):

    overallTriggers = jsonObject['triggers']
    TRIGGERMUEG = getTriggerFromJson(overallTriggers, "TRIGGERMUEG", year)
    TRIGGERDMU  = getTriggerFromJson(overallTriggers, "TRIGGERDMU", year)
    TRIGGERSMU  = getTriggerFromJson(overallTriggers, "TRIGGERSMU", year)
    TRIGGERDEL  = getTriggerFromJson(overallTriggers, "TRIGGERDEL", year)
    TRIGGERSEL  = getTriggerFromJson(overallTriggers, "TRIGGERSEL", year)

    TRIGGERPHOINC  = getTriggerFromJson(overallTriggers, "TRIGGERPHOFAKE", year)

    TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    if(year == 2018 and PDType == "MuonEG"):
        triggerLEP = "{0}".format(TRIGGERMUEG)
    elif(year == 2018 and PDType == "DoubleMuon"):
        triggerLEP = "{0} and not {1}".format(TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "SingleMuon"):
        triggerLEP = "{0} and not {1} and not {2}".format(TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "EGamma"):
        triggerLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018):
        triggerLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2022 and PDType == "MuonEG"):
        triggerLEP = "{0}".format(TRIGGERMUEG)
    elif(year == 2022 and PDType == "Muon"):
        triggerLEP = "({0} or {1}) and not {1}".format(TRIGGERDMU,TRIGGERSMU,TRIGGERMUEG)
    elif(year == 2022 and PDType == "EGamma"):
        triggerLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2022):
        triggerLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    else:
        print("PROBLEM with triggers!!!")

    dftag =(df.Define("isData","{}".format(isData))
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")
              .Define("trigger","{0}".format(TRIGGERPHOINC))
              .Filter("trigger > 0","Passed trigger")

              .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")
              .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")
              .Filter("Sum(loose_mu)+Sum(loose_el) == 0","No loose leptons")

              .Filter("MET_pt < 100","met < 100")

              .Define("goodPhotonsEB0", "{0} && Photon_isScEtaEB && cleaningBitmap(Photon_vidNestedWPBitmap,6,2) && cleaningBitmap(Photon_vidNestedWPBitmap,8,2)".format(PHOTONSKIM))
              .Define("goodPhotonsEB0_pt", "get_variable_index(Photon_pt[goodPhotonsEB0],Photon_pt[goodPhotonsEB0],0)")
              .Define("goodPhotonsEB0_sieie", "get_variable_index(Photon_sieie[goodPhotonsEB0],Photon_pt[goodPhotonsEB0],0)")
              .Define("goodPhotonsEB0_iso03_chg", "get_variable_index(Photon_pfChargedIsoPFPV[goodPhotonsEB0]*Photon_pt[goodPhotonsEB0],Photon_pt[goodPhotonsEB0],0)")
              .Define("nGoodPhotonsEB0","Sum(goodPhotonsEB0)")

              .Define("goodPhotonsEB1", "{0} && Photon_isScEtaEB && cleaningBitmap(Photon_vidNestedWPBitmap,8,2) == false && Photon_pfChargedIsoPFPV*Photon_pt > 3 && Photon_pfChargedIsoPFPV*Photon_pt < 6".format(PHOTONSKIM))
              .Define("goodPhotonsEB1_pt", "get_variable_index(Photon_pt[goodPhotonsEB1],Photon_pt[goodPhotonsEB1],0)")
              .Define("goodPhotonsEB1_sieie", "get_variable_index(Photon_sieie[goodPhotonsEB1],Photon_pt[goodPhotonsEB1],0)")
              .Define("goodPhotonsEB1_iso03_chg", "get_variable_index(Photon_pfChargedIsoPFPV[goodPhotonsEB1]*Photon_pt[goodPhotonsEB1],Photon_pt[goodPhotonsEB1],0)")
              .Define("nGoodPhotonsEB1","Sum(goodPhotonsEB1)")

              .Define("goodPhotonsEB2", "{0} && Photon_isScEtaEB && cleaningBitmap(Photon_vidNestedWPBitmap,8,2) == false && Photon_pfChargedIsoPFPV*Photon_pt > 6 && Photon_pfChargedIsoPFPV*Photon_pt < 9".format(PHOTONSKIM))
              .Define("goodPhotonsEB2_pt", "get_variable_index(Photon_pt[goodPhotonsEB2],Photon_pt[goodPhotonsEB2],0)")
              .Define("goodPhotonsEB2_sieie", "get_variable_index(Photon_sieie[goodPhotonsEB2],Photon_pt[goodPhotonsEB2],0)")
              .Define("goodPhotonsEB2_iso03_chg", "get_variable_index(Photon_pfChargedIsoPFPV[goodPhotonsEB2]*Photon_pt[goodPhotonsEB2],Photon_pt[goodPhotonsEB2],0)")
              .Define("nGoodPhotonsEB2","Sum(goodPhotonsEB2)")

              .Define("goodPhotonsEB3", "{0} && Photon_isScEtaEB && cleaningBitmap(Photon_vidNestedWPBitmap,8,2)".format(PHOTONSKIM))
              .Define("goodPhotonsEB3_pt", "get_variable_index(Photon_pt[goodPhotonsEB3],Photon_pt[goodPhotonsEB3],0)")
              .Define("goodPhotonsEB3_sieie", "get_variable_index(Photon_sieie[goodPhotonsEB3],Photon_pt[goodPhotonsEB3],0)")
              .Define("goodPhotonsEB3_iso03_chg", "get_variable_index(Photon_pfChargedIsoPFPV[goodPhotonsEB3]*Photon_pt[goodPhotonsEB3],Photon_pt[goodPhotonsEB3],0)")
              .Define("nGoodPhotonsEB3","Sum(goodPhotonsEB3)")

              .Define("goodPhotonsEE0", "{0} && Photon_isScEtaEE && cleaningBitmap(Photon_vidNestedWPBitmap,6,2) && cleaningBitmap(Photon_vidNestedWPBitmap,8,2)".format(PHOTONSKIM))
              .Define("goodPhotonsEE0_pt", "get_variable_index(Photon_pt[goodPhotonsEE0],Photon_pt[goodPhotonsEE0],0)")
              .Define("goodPhotonsEE0_sieie", "get_variable_index(Photon_sieie[goodPhotonsEE0],Photon_pt[goodPhotonsEE0],0)")
              .Define("goodPhotonsEE0_iso03_chg", "get_variable_index(Photon_pfChargedIsoPFPV[goodPhotonsEE0]*Photon_pt[goodPhotonsEE0],Photon_pt[goodPhotonsEE0],0)")
              .Define("nGoodPhotonsEE0","Sum(goodPhotonsEE0)")

              .Define("goodPhotonsEE1", "{0} && Photon_isScEtaEE && cleaningBitmap(Photon_vidNestedWPBitmap,8,2) == false && Photon_pfChargedIsoPFPV*Photon_pt > 3 && Photon_pfChargedIsoPFPV*Photon_pt < 6".format(PHOTONSKIM))
              .Define("goodPhotonsEE1_pt", "get_variable_index(Photon_pt[goodPhotonsEE1],Photon_pt[goodPhotonsEE1],0)")
              .Define("goodPhotonsEE1_sieie", "get_variable_index(Photon_sieie[goodPhotonsEE1],Photon_pt[goodPhotonsEE1],0)")
              .Define("goodPhotonsEE1_iso03_chg", "get_variable_index(Photon_pfChargedIsoPFPV[goodPhotonsEE1]*Photon_pt[goodPhotonsEE1],Photon_pt[goodPhotonsEE1],0)")
              .Define("nGoodPhotonsEE1","Sum(goodPhotonsEE1)")

              .Define("goodPhotonsEE2", "{0} && Photon_isScEtaEE && cleaningBitmap(Photon_vidNestedWPBitmap,8,2) == false && Photon_pfChargedIsoPFPV*Photon_pt > 6 && Photon_pfChargedIsoPFPV*Photon_pt < 9".format(PHOTONSKIM))
              .Define("goodPhotonsEE2_pt", "get_variable_index(Photon_pt[goodPhotonsEE2],Photon_pt[goodPhotonsEE2],0)")
              .Define("goodPhotonsEE2_sieie", "get_variable_index(Photon_sieie[goodPhotonsEE2],Photon_pt[goodPhotonsEE2],0)")
              .Define("goodPhotonsEE2_iso03_chg", "get_variable_index(Photon_pfChargedIsoPFPV[goodPhotonsEE2]*Photon_pt[goodPhotonsEE2],Photon_pt[goodPhotonsEE2],0)")
              .Define("nGoodPhotonsEE2","Sum(goodPhotonsEE2)")

              .Define("goodPhotonsEE3", "{0} && Photon_isScEtaEE && cleaningBitmap(Photon_vidNestedWPBitmap,8,2)".format(PHOTONSKIM))
              .Define("goodPhotonsEE3_pt", "get_variable_index(Photon_pt[goodPhotonsEE3],Photon_pt[goodPhotonsEE3],0)")
              .Define("goodPhotonsEE3_sieie", "get_variable_index(Photon_sieie[goodPhotonsEE3],Photon_pt[goodPhotonsEE3],0)")
              .Define("goodPhotonsEE3_iso03_chg", "get_variable_index(Photon_pfChargedIsoPFPV[goodPhotonsEE3]*Photon_pt[goodPhotonsEE3],Photon_pt[goodPhotonsEE3],0)")
              .Define("nGoodPhotonsEE3","Sum(goodPhotonsEE3)")

              .Filter("nGoodPhotonsEB0+nGoodPhotonsEB1+nGoodPhotonsEB2+nGoodPhotonsEB3+nGoodPhotonsEE0+nGoodPhotonsEE1+nGoodPhotonsEE2+nGoodPhotonsEE3 >= 1","At least one loose photon")

              .Define("jet_maskl0", "cleaningMask(Muon_jetIdx[loose_mu],nJet)")
              .Define("jet_maskl1", "cleaningMask(Electron_jetIdx[loose_el],nJet)")
              .Define("jet_maskg0", "cleaningMask(Photon_jetIdx[goodPhotonsEB0],nJet)")
              .Define("jet_maskg1", "cleaningMask(Photon_jetIdx[goodPhotonsEB1],nJet)")
              .Define("jet_maskg2", "cleaningMask(Photon_jetIdx[goodPhotonsEB2],nJet)")
              .Define("jet_maskg3", "cleaningMask(Photon_jetIdx[goodPhotonsEB3],nJet)")
              .Define("jet_maskg4", "cleaningMask(Photon_jetIdx[goodPhotonsEE0],nJet)")
              .Define("jet_maskg5", "cleaningMask(Photon_jetIdx[goodPhotonsEE1],nJet)")
              .Define("jet_maskg6", "cleaningMask(Photon_jetIdx[goodPhotonsEE2],nJet)")
              .Define("jet_maskg7", "cleaningMask(Photon_jetIdx[goodPhotonsEE3],nJet)")

              .Define("goodloose_jet", "abs(Jet_eta) < 2.5 && Jet_pt > 20 && jet_maskl0 && jet_maskl1 && jet_maskg0 && jet_maskg1 && jet_maskg2 && jet_maskg3 && jet_maskg4 && jet_maskg5 && jet_maskg6 && jet_maskg7")
              .Define("goodloosejet_pt", "Jet_pt[goodloose_jet]")
              .Define("goodloosejet_eta", "abs(Jet_eta[goodloose_jet])")
              .Define("goodloosejet_btagDeepB", "Jet_btagDeepB[goodloose_jet]")
              .Define("goodloose_bjet", "goodloosejet_btagDeepB > 0.7100")
              .Define("nbtagloosejet", "Sum(goodloose_bjet)")

              .Define("good_jet"     , "abs(Jet_eta) < 5.0 && Jet_pt > 30 && jet_maskl0 && jet_maskl1 && jet_maskg0 && jet_maskg1 && jet_maskg2 && jet_maskg3 && jet_maskg4 && jet_maskg5 && jet_maskg6 && jet_maskg7 && Jet_jetId > 0")
              .Define("ngood_jets", "Sum(good_jet)")
              .Define("goodjet_pt",    "Jet_pt[good_jet]")
              .Define("goodjet_eta",   "Jet_eta[good_jet]")
              .Define("goodjet_phi",   "Jet_phi[good_jet]")
              .Define("goodjet_mass",  "Jet_mass[good_jet]")

              )

    return dftag

def analysis(df,count,category,weight,year,PDType,isData,whichJob,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")
    elif(theCat == plotCategory("kPlotqqWW") or theCat == plotCategory("kPlotggWW") or
         theCat == plotCategory("kPlotTop") or theCat == plotCategory("kPlotHiggs")):
        theCat = plotCategory("kPlotEM")
    elif(theCat == plotCategory("kPlotTVX")):
        theCat = plotCategory("kPlotVVV")

    nCat, nHisto = plotCategory("kPlotCategories"), 400
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

    ROOT.initJSONSFs(year)

    dftag = selectionLL(df,year,PDType,isData)

    dftag = (dftag.Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                  .Define("theCat","compute_category({0},kPlotNonPrompt,0,0)".format(theCat))
                    )

    if(theCat == plotCategory("kPlotData")):
        dfbase =(dftag.Define("weight","1.0")
                      )

    else:
        dfbase = (dftag.Define("PDType","\"{0}\"".format(PDType))
                       .Define("fakemu_genPartFlav","Muon_genPartFlav[loose_mu]")
                       .Define("fakeel_genPartFlav","Electron_genPartFlav[loose_el]")
                       .Define("weightMC","compute_weights({0},genWeight,PDType,fakemu_genPartFlav,fakeel_genPartFlav,0)".format(weight))
                       .Filter("weightMC != 0","MC weight")
                       .Define("weight","weightMC")
                       )

    xPtbins = array('d', [20,40,60,80,100,120,140,160,180,200,220,240,260,280,300,350,400,450,500,750,1000])

    dfcat = []
    for x in range(nCat):
        dfcat.append(dfbase.Filter("theCat=={0}".format(x), "correct category ({0})".format(x)))

        histo[ 8][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x), 10,-0.5,9.5), "ngood_jets","weight")

        dfcat[x] = dfcat[x].Filter("ngood_jets >= 1", "ngood_jets >= 1")

        histo[18][x] = dfcat[x].Filter("Sum(goodPhotonsEB0) >= 1").Histo1D(("histo_{0}_{1}".format(18,x), "histo_{0}_{1}".format(18,x), len(xPtbins)-1, xPtbins), "goodPhotonsEB0_pt","weight")
        histo[28][x] = dfcat[x].Filter("Sum(goodPhotonsEB1) >= 1").Histo1D(("histo_{0}_{1}".format(28,x), "histo_{0}_{1}".format(28,x), len(xPtbins)-1, xPtbins), "goodPhotonsEB1_pt","weight")
        histo[38][x] = dfcat[x].Filter("Sum(goodPhotonsEB2) >= 1").Histo1D(("histo_{0}_{1}".format(38,x), "histo_{0}_{1}".format(38,x), len(xPtbins)-1, xPtbins), "goodPhotonsEB2_pt","weight")
        histo[48][x] = dfcat[x].Filter("Sum(goodPhotonsEB3) >= 1").Histo1D(("histo_{0}_{1}".format(48,x), "histo_{0}_{1}".format(48,x), len(xPtbins)-1, xPtbins), "goodPhotonsEB3_pt","weight")
        histo[58][x] = dfcat[x].Filter("Sum(goodPhotonsEE0) >= 1").Histo1D(("histo_{0}_{1}".format(58,x), "histo_{0}_{1}".format(58,x), len(xPtbins)-1, xPtbins), "goodPhotonsEE0_pt","weight")
        histo[68][x] = dfcat[x].Filter("Sum(goodPhotonsEE1) >= 1").Histo1D(("histo_{0}_{1}".format(68,x), "histo_{0}_{1}".format(68,x), len(xPtbins)-1, xPtbins), "goodPhotonsEE1_pt","weight")
        histo[78][x] = dfcat[x].Filter("Sum(goodPhotonsEE2) >= 1").Histo1D(("histo_{0}_{1}".format(78,x), "histo_{0}_{1}".format(78,x), len(xPtbins)-1, xPtbins), "goodPhotonsEE2_pt","weight")
        histo[88][x] = dfcat[x].Filter("Sum(goodPhotonsEE3) >= 1").Histo1D(("histo_{0}_{1}".format(88,x), "histo_{0}_{1}".format(88,x), len(xPtbins)-1, xPtbins), "goodPhotonsEE3_pt","weight")

        histo[19][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(19,x), "histo_{0}_{1}".format(19,x), 5, -0.5, 4.5), "nGoodPhotonsEB0","weight")
        histo[29][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(29,x), "histo_{0}_{1}".format(29,x), 5, -0.5, 4.5), "nGoodPhotonsEB1","weight")
        histo[39][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(39,x), "histo_{0}_{1}".format(39,x), 5, -0.5, 4.5), "nGoodPhotonsEB2","weight")
        histo[49][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(49,x), "histo_{0}_{1}".format(49,x), 5, -0.5, 4.5), "nGoodPhotonsEB3","weight")
        histo[59][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(59,x), "histo_{0}_{1}".format(59,x), 5, -0.5, 4.5), "nGoodPhotonsEE0","weight")
        histo[69][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(69,x), "histo_{0}_{1}".format(69,x), 5, -0.5, 4.5), "nGoodPhotonsEE1","weight")
        histo[79][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(79,x), "histo_{0}_{1}".format(79,x), 5, -0.5, 4.5), "nGoodPhotonsEE2","weight")
        histo[89][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(89,x), "histo_{0}_{1}".format(89,x), 5, -0.5, 4.5), "nGoodPhotonsEE3","weight")

        for j in xPtbins:
            if(len(xPtbins)-1 == xPtbins.index(j)): continue
            histo[  0+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEB0) >= 1 && goodPhotonsEB0_pt > {0} && goodPhotonsEB0_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(  0+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(  0+xPtbins.index(j)*10,x), 30,0.000,0.030), "goodPhotonsEB0_sieie","weight")
            histo[  1+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEB1) >= 1 && goodPhotonsEB1_pt > {0} && goodPhotonsEB1_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(  1+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(  1+xPtbins.index(j)*10,x), 30,0.000,0.030), "goodPhotonsEB1_sieie","weight")
            histo[  2+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEB2) >= 1 && goodPhotonsEB2_pt > {0} && goodPhotonsEB2_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(  2+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(  2+xPtbins.index(j)*10,x), 30,0.000,0.030), "goodPhotonsEB2_sieie","weight")
            histo[  3+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEB3) >= 1 && goodPhotonsEB3_pt > {0} && goodPhotonsEB3_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(  3+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(  3+xPtbins.index(j)*10,x), 30,0.000,0.030), "goodPhotonsEB3_sieie","weight")
            histo[  4+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEE0) >= 1 && goodPhotonsEE0_pt > {0} && goodPhotonsEE0_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(  4+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(  4+xPtbins.index(j)*10,x), 60,0.000,0.060), "goodPhotonsEE0_sieie","weight")
            histo[  5+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEE1) >= 1 && goodPhotonsEE1_pt > {0} && goodPhotonsEE1_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(  5+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(  5+xPtbins.index(j)*10,x), 60,0.000,0.060), "goodPhotonsEE1_sieie","weight")
            histo[  6+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEE2) >= 1 && goodPhotonsEE2_pt > {0} && goodPhotonsEE2_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(  6+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(  6+xPtbins.index(j)*10,x), 60,0.000,0.060), "goodPhotonsEE2_sieie","weight")
            histo[  7+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEE3) >= 1 && goodPhotonsEE3_pt > {0} && goodPhotonsEE3_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(  7+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(  7+xPtbins.index(j)*10,x), 60,0.000,0.060), "goodPhotonsEE3_sieie","weight")

            histo[200+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEB0) >= 1 && goodPhotonsEB0_pt > {0} && goodPhotonsEB0_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(200+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(200+xPtbins.index(j)*10,x), 50,0,10), "goodPhotonsEB0_iso03_chg","weight")
            histo[201+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEB1) >= 1 && goodPhotonsEB1_pt > {0} && goodPhotonsEB1_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(201+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(201+xPtbins.index(j)*10,x), 50,0,10), "goodPhotonsEB1_iso03_chg","weight")
            histo[202+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEB2) >= 1 && goodPhotonsEB2_pt > {0} && goodPhotonsEB2_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(202+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(202+xPtbins.index(j)*10,x), 50,0,10), "goodPhotonsEB2_iso03_chg","weight")
            histo[203+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEB3) >= 1 && goodPhotonsEB3_pt > {0} && goodPhotonsEB3_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(203+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(203+xPtbins.index(j)*10,x), 50,0,10), "goodPhotonsEB3_iso03_chg","weight")
            histo[204+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEE0) >= 1 && goodPhotonsEE0_pt > {0} && goodPhotonsEE0_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(204+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(204+xPtbins.index(j)*10,x), 50,0,10), "goodPhotonsEE0_iso03_chg","weight")
            histo[205+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEE1) >= 1 && goodPhotonsEE1_pt > {0} && goodPhotonsEE1_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(205+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(205+xPtbins.index(j)*10,x), 50,0,10), "goodPhotonsEE1_iso03_chg","weight")
            histo[206+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEE2) >= 1 && goodPhotonsEE2_pt > {0} && goodPhotonsEE2_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(206+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(206+xPtbins.index(j)*10,x), 50,0,10), "goodPhotonsEE2_iso03_chg","weight")
            histo[207+xPtbins.index(j)*10][x] = dfcat[x].Filter("Sum(goodPhotonsEE3) >= 1 && goodPhotonsEE3_pt > {0} && goodPhotonsEE3_pt < {1}".format(xPtbins[xPtbins.index(j)],xPtbins[xPtbins.index(j)+1])).Histo1D(("histo_{0}_{1}".format(207+xPtbins.index(j)*10,x), "histo_{0}_{1}".format(207+xPtbins.index(j)*10,x), 50,0,10), "goodPhotonsEE3_iso03_chg","weight")

    report = []
    for x in range(nCat):
        report.append(dfcat[x].Report())
        if(x != theCat): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    myfile = ROOT.TFile("fillhistogammaAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
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

    weight = (SwitchSample(sampleNOW, skimType)[1] / genEventSumWeight)*getLumi(year)
    weightApprox = (SwitchSample(sampleNOW, skimType)[1] / genEventSumNoWeight)*getLumi(year)

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

    group = 20

    skimType = "pho"
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

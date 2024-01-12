import ROOT
import os, sys, getopt, json

ROOT.ROOT.EnableImplicitMT(4)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection2LVar, selectionTrigger2L, selectionElMu, selectionWeigths, selectionGenLepJet, makeFinalVariable2D
#from utilsAna import loadCorrectionSet

print_info = False
makeDataCards = 1
correctionString = ""

# 0 = T, 1 = M, 2 = L
bTagSel = 2
useBTaggingWeights = 1

useFR = 1

altMass = "Def"

jetEtaCut = 2.5

selectionJsonPath = "config/selection.json"

with open(selectionJsonPath) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

JSON = jsonObject['JSON']

BARRELphotons = jsonObject['BARRELphotons']
ENDCAPphotons = jsonObject['ENDCAPphotons']

VBSSEL = jsonObject['VBSSEL']

#2/4/5/8
muSelChoice = 2
FAKE_MU   = jsonObject['FAKE_MU']
TIGHT_MU = jsonObject['TIGHT_MU{0}'.format(muSelChoice)]
MUOWP = "Medium"

#1/3/4/8
elSelChoice = 3
FAKE_EL   = jsonObject['FAKE_EL']
TIGHT_EL = jsonObject['TIGHT_EL{0}'.format(elSelChoice)]
ELEWP = "DUMMY"
if(elSelChoice == 0):
    ELEWP = "Medium"
elif(elSelChoice == 1):
    ELEWP = "Tight"
elif(elSelChoice == 2):
    ELEWP = "wp80noiso"
elif(elSelChoice == 3):
    ELEWP = "wp80iso"
elif(elSelChoice == 4):
    ELEWP = "wp80iso"
elif(elSelChoice == 5):
    ELEWP = "wp90iso"
elif(elSelChoice == 6):
    ELEWP = "wp80iso"
elif(elSelChoice == 7):
    ELEWP = "wp80iso"
elif(elSelChoice == 8):
    ELEWP = "wp80iso"
elif(elSelChoice == 9):
    ELEWP = "Veto"

def selectionLL(df,year,PDType,isData,TRIGGERMUEG,TRIGGERDMU,TRIGGERSMU,TRIGGERDEL,TRIGGERSEL,count):

    dftag = selectionTrigger2L(df,year,PDType,JSON,isData,TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU,FAKE_EL,TIGHT_EL)

    dftag = (dftag.Filter("nLoose >= 2","At least two loose leptons")
                  .Filter("nLoose == 2","Only two loose leptons")
                  .Filter("nFake == 2","Two fake leptons")

                  .Filter("(Sum(fake_mu) == 1 && Sum(fake_el) == 1) or (Sum(fake_Muon_charge)+Sum(fake_Electron_charge) != 0)","e-mu events")

                  )

    global useFR
    if(year == 2023): useFR = 0
    if(useFR == 0):
        dftag = dftag.Filter("nTight == 2","Two tight leptons")

    dftag = selection2LVar  (dftag,year,isData)

    dftag = dftag.Filter("mll{0} > 20".format(altMass),"mll > 20")

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData,count,jetEtaCut)

    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto, nHistoMVA, nhistoNonPrompt = plotCategory("kPlotCategories"), 500, 1600, 50
    histo    = [[0 for y in range(nCat)] for x in range(nHisto)]
    histo2D  = [[0 for y in range(nCat)] for x in range(nHistoMVA)]
    histoMVA = [[0 for y in range(nCat)] for x in range(nHistoMVA)]
    histoNonPrompt = [0 for y in range(nhistoNonPrompt)]

    ROOT.initHisto2D(histoFakeEtaPt_mu[0],0)
    ROOT.initHisto2D(histoFakeEtaPt_el[0],1)
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
    ROOT.initHisto2D(histoFakeEtaPt_mu[1],23)
    ROOT.initHisto2D(histoFakeEtaPt_mu[2],24)
    ROOT.initHisto2D(histoFakeEtaPt_mu[3],25)
    ROOT.initHisto2D(histoFakeEtaPt_mu[4],26)
    ROOT.initHisto2D(histoFakeEtaPt_mu[5],27)
    ROOT.initHisto2D(histoFakeEtaPt_mu[6],28)
    ROOT.initHisto2D(histoFakeEtaPt_mu[7],29)
    ROOT.initHisto2D(histoFakeEtaPt_mu[8],30)
    ROOT.initHisto2D(histoFakeEtaPt_el[1],31)
    ROOT.initHisto2D(histoFakeEtaPt_el[2],32)
    ROOT.initHisto2D(histoFakeEtaPt_el[3],33)
    ROOT.initHisto2D(histoFakeEtaPt_el[4],34)
    ROOT.initHisto2D(histoFakeEtaPt_el[5],35)
    ROOT.initHisto2D(histoFakeEtaPt_el[6],36)
    ROOT.initHisto2D(histoFakeEtaPt_el[7],37)
    ROOT.initHisto2D(histoFakeEtaPt_el[8],38)
    ROOT.initHisto1D(puWeights[0],0)
    ROOT.initHisto1D(puWeights[1],1)
    ROOT.initHisto1D(puWeights[2],2)

    ROOT.initJSONSFs(year)

    overallTriggers = jsonObject['triggers']
    TRIGGERMUEG = getTriggerFromJson(overallTriggers, "TRIGGERMUEG", year)
    TRIGGERDMU  = getTriggerFromJson(overallTriggers, "TRIGGERDMU", year)
    TRIGGERSMU  = getTriggerFromJson(overallTriggers, "TRIGGERSMU", year)
    TRIGGERDEL  = getTriggerFromJson(overallTriggers, "TRIGGERDEL", year)
    TRIGGERSEL  = getTriggerFromJson(overallTriggers, "TRIGGERSEL", year)

    list_TRIGGERMUEG = TRIGGERMUEG.split('(')[1].split(')')[0].split('||')
    list_TRIGGERDMU  = TRIGGERDMU .split('(')[1].split(')')[0].split('||')
    list_TRIGGERSMU  = TRIGGERSMU .split('(')[1].split(')')[0].split('||')
    list_TRIGGERDEL  = TRIGGERDEL .split('(')[1].split(')')[0].split('||')
    list_TRIGGERSEL  = TRIGGERSEL .split('(')[1].split(')')[0].split('||')

    list_TRIGGER = list_TRIGGERMUEG
    list_TRIGGER.extend(list_TRIGGERDMU)
    list_TRIGGER.extend(list_TRIGGERSMU)
    list_TRIGGER.extend(list_TRIGGERDEL)
    list_TRIGGER.extend(list_TRIGGERSEL)
    print("Total number of trigger paths: {0}".format(len(list_TRIGGER)))

    dfbase = selectionLL(df,year,PDType,isData,TRIGGERMUEG,TRIGGERDMU,TRIGGERSMU,TRIGGERDEL,TRIGGERSEL,count)

    global useFR
    if(year == 2023): useFR = 0
    dfbase = selectionWeigths(dfbase,isData,year,PDType,weight,useFR,bTagSel,useBTaggingWeights,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,MUOWP,ELEWP,correctionString,0)

    overallMETFilters = jsonObject['met_filters']
    METFILTERS = getTriggerFromJson(overallMETFilters, "All", year)
    dfbase = dfbase.Define("METFILTERS", "{0}".format(METFILTERS)).Filter("METFILTERS > 0","METFILTERS > 0")

    dfcat = []
    dfssx0cat = []
    dfwwx0cat = []
    dfztt0cat = []
    dftop0cat = []
    dfhwwxcat = []
    dftop1cat = []

    dfssx1cat = []
    dfssx2cat = []

    dfssx0catMuonMomUp       = []
    dfssx0catMuonMomDown     = []
    dfssx0catElectronMomUp   = []
    dfssx0catElectronMomDown = []
    dfwwx0catMuonMomUp       = []
    dfwwx0catMuonMomDown     = []
    dfwwx0catElectronMomUp   = []
    dfwwx0catElectronMomDown = []
    dfztt0catMuonMomUp       = []
    dfztt0catMuonMomDown     = []
    dfztt0catElectronMomUp   = []
    dfztt0catElectronMomDown = []
    dftop0catMuonMomUp       = []
    dftop0catMuonMomDown     = []
    dftop0catElectronMomUp   = []
    dftop0catElectronMomDown = []
    dftop1catMuonMomUp       = []
    dftop1catMuonMomDown     = []
    dftop1catElectronMomUp   = []
    dftop1catElectronMomDown = []

    for x in range(nCat):
        dfcat.append(dfbase.Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                           .Define("kPlotWS", "{0}".format(plotCategory("kPlotWS")))
                           .Define("theCat{0}".format(x), "compute_category({0},kPlotNonPrompt,kPlotWS,nFake,nTight,0)".format(theCat))
                           .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x))
                           )

        if(isData == "false"):
            dfcat[x] = dfcat[x].Define("nPileupJets", "compute_nPileupJets(good_Jet_pt,good_Jet_eta,good_Jet_phi,GenJet_pt,GenJet_eta,GenJet_phi)")
        else:
            dfcat[x] = dfcat[x].Define("nPileupJets", "ngood_jets")

        if(x == plotCategory("kPlotTop")):
            dfcat[x] = dfcat[x].Define("weightWW", "weight")
        else:
            dfcat[x] = dfcat[x].Define("weightWW", "weight")

        if((x == plotCategory("kPlotqqWW") or x == plotCategory("kPlotggWW")) and isData == "false"):
            dfcat[x] = selectionGenLepJet(dfcat[x],20,30,jetEtaCut)
            dfcat[x] = (dfcat[x].Define("kPlotSignal0", "{0}".format(plotCategory("kPlotSignal0")))
                                .Define("kPlotSignal1", "{0}".format(plotCategory("kPlotSignal1")))
                                .Define("kPlotSignal2", "{0}".format(plotCategory("kPlotSignal2")))
                                .Define("kPlotSignal3", "{0}".format(plotCategory("kPlotSignal3")))
                                .Define("theGenCat", "compute_gen_category({0},kPlotSignal0,kPlotSignal1,kPlotSignal2,kPlotSignal3,ngood_GenJets,ngood_GenDressedLeptons)".format(x))
                                )
        else:
            dfcat[x] = dfcat[x].Define("theGenCat", "{0}".format(0))

        dfssx0cat.append(dfcat[x].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) != 0 && Sum(fake_mu) == 1 && Sum(fake_el) == 1", "Same-sign leptons"))
        dfssx1cat.append(dfcat[x].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) != 0 && Sum(fake_mu) == 2 && Sum(fake_el) == 0", "Same-sign muons"))
        dfssx2cat.append(dfcat[x].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) != 0 && Sum(fake_mu) == 0 && Sum(fake_el) == 2", "Same-sign electrons"))

        histo[ 0][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x), 60, 20, 320), "mll{0}".format(altMass),"weightWW")
        histo[ 1][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x), 50,  0, 200), "ptll{0}".format(altMass),"weightWW")
        histo[ 2][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjet","weightWW")

        dfcat[x] = dfcat[x].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) == 0 && Sum(fake_mu) == 1 && Sum(fake_el) == 1", "Opposite-sign leptons")

        histo[ 3][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x), 60, 20, 320), "mll{0}".format(altMass),"weightWW")
        histo[ 4][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x), 50,  0, 200), "ptll{0}".format(altMass),"weightWW")
        histo[ 5][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjet","weightWW")
        histo[77][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(77,x), "histo_{0}_{1}".format(77,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjetPNetB","weightWW")
        histo[78][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(78,x), "histo_{0}_{1}".format(78,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjetRobustParTAK4","weightWW")
        histo[79][x] = dfcat[x].Filter("ngood_jets==0").Histo1D(("histo_{0}_{1}".format(79,x), "histo_{0}_{1}".format(79,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjet","weightWW")
        histo[80][x] = dfcat[x].Filter("ngood_jets==0").Histo1D(("histo_{0}_{1}".format(80,x), "histo_{0}_{1}".format(80,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjetPNetB","weightWW")
        histo[81][x] = dfcat[x].Filter("ngood_jets==0").Histo1D(("histo_{0}_{1}".format(81,x), "histo_{0}_{1}".format(81,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjetRobustParTAK4","weightWW")

        dfssx0cat[x] = dfssx0cat[x].Filter("nbtag_goodbtag_Jet_bjet == 0", "No b-jets")
        dfssx0catMuonMomUp      .append(dfssx0cat[x])
        dfssx0catMuonMomDown    .append(dfssx0cat[x])
        dfssx0catElectronMomUp  .append(dfssx0cat[x])
        dfssx0catElectronMomDown.append(dfssx0cat[x])
        dfssx1cat[x] = dfssx1cat[x].Filter("nbtag_goodbtag_Jet_bjet == 0", "No b-jets")
        dfssx2cat[x] = dfssx2cat[x].Filter("nbtag_goodbtag_Jet_bjet == 0", "No b-jets")

        dfssx0catMuonMomUp      [x] = dfssx0catMuonMomUp      [x].Filter("mllMuonMomUp       > 85 && ptl1MuonMomUp       > 25 && ptl2MuonMomUp      > 20")
        dfssx0catMuonMomDown    [x] = dfssx0catMuonMomDown    [x].Filter("mllMuonMomDown     > 85 && ptl1MuonMomDown     > 25 && ptl2MuonMomDown    > 20")
        dfssx0catElectronMomUp  [x] = dfssx0catElectronMomUp  [x].Filter("mllElectronMomUp   > 85 && ptl1ElectronMomUp   > 25 && ptl2ElectronMomUp  > 20")
        dfssx0catElectronMomDown[x] = dfssx0catElectronMomDown[x].Filter("mllElectronMomDown > 85 && ptl1ElectronMomDown > 25 && ptl2ElectronMomDown> 20")

        dfssx0cat[x] = dfssx0cat[x].Filter("mll{0} > 85 && ptl1{0} > 25 && ptl2{0} > 20".format(altMass), "mll > 85 && ptl1 > 25 && ptl2 > 20")
        dfssx1cat[x] = dfssx1cat[x].Filter("mll{0} > 50 && ptl1{0} > 25 && ptl2{0} > 20".format(altMass), "mll > 50 && ptl1 > 25 && ptl2 > 20")
        dfssx2cat[x] = dfssx2cat[x].Filter("mll{0} > 50 && ptl1{0} > 25 && ptl2{0} > 20".format(altMass), "mll > 50 && ptl1 > 25 && ptl2 > 20")

        dfwwx0cat.append(dfcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0", "No b-jets"))
        dfwwx0catMuonMomUp      .append(dfwwx0cat[x])
        dfwwx0catMuonMomDown    .append(dfwwx0cat[x])
        dfwwx0catElectronMomUp  .append(dfwwx0cat[x])
        dfwwx0catElectronMomDown.append(dfwwx0cat[x])

        dfwwx0catMuonMomUp      [x] = dfwwx0catMuonMomUp      [x].Filter("mllMuonMomUp       > 85 && ptl1MuonMomUp       > 25 && ptl2MuonMomUp      > 20")
        dfwwx0catMuonMomDown    [x] = dfwwx0catMuonMomDown    [x].Filter("mllMuonMomDown     > 85 && ptl1MuonMomDown     > 25 && ptl2MuonMomDown    > 20")
        dfwwx0catElectronMomUp  [x] = dfwwx0catElectronMomUp  [x].Filter("mllElectronMomUp   > 85 && ptl1ElectronMomUp   > 25 && ptl2ElectronMomUp  > 20")
        dfwwx0catElectronMomDown[x] = dfwwx0catElectronMomDown[x].Filter("mllElectronMomDown > 85 && ptl1ElectronMomDown > 25 && ptl2ElectronMomDown> 20")

        dfwwx0cat[x] = dfwwx0cat[x].Filter("mll{0} > 85 && ptl1{0} > 25 && ptl2{0} > 20".format(altMass), "mll > 85 && ptl1 > 25 && ptl2 > 20")

        dfztt0cat.append(dfcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0", "No b-jets"))
        dfztt0catMuonMomUp      .append(dfztt0cat[x])
        dfztt0catMuonMomDown    .append(dfztt0cat[x])
        dfztt0catElectronMomUp  .append(dfztt0cat[x])
        dfztt0catElectronMomDown.append(dfztt0cat[x])

        dfztt0catMuonMomUp      [x] = dfztt0catMuonMomUp      [x].Filter("ptllMuonMomUp       < 30 && mllMuonMomUp       < 85 && ptl1MuonMomUp       > 25 && ptl2MuonMomUp      > 20")
        dfztt0catMuonMomDown    [x] = dfztt0catMuonMomDown    [x].Filter("ptllMuonMomDown     < 30 && mllMuonMomDown     < 85 && ptl1MuonMomDown     > 25 && ptl2MuonMomDown    > 20")
        dfztt0catElectronMomUp  [x] = dfztt0catElectronMomUp  [x].Filter("ptllElectronMomUp   < 30 && mllElectronMomUp   < 85 && ptl1ElectronMomUp   > 25 && ptl2ElectronMomUp  > 20")
        dfztt0catElectronMomDown[x] = dfztt0catElectronMomDown[x].Filter("ptllElectronMomDown < 30 && mllElectronMomDown < 85 && ptl1ElectronMomDown > 25 && ptl2ElectronMomDown> 20")

        dfztt0cat[x] = dfztt0cat[x].Filter("ptll{0} < 30 && mll{0} < 85 && ptl1{0} > 25 && ptl2{0} > 20".format(altMass), "ptll < 30 && mll < 85 && ptl1 > 25 && ptl2 > 20")

        dftop0cat.append(dfcat[x].Filter("nbtag_goodbtag_Jet_bjet >= 1 && nbtag_goodbtag_Jet_bjet <= 2", "b-jets"))
        dftop0catMuonMomUp      .append(dftop0cat[x])
        dftop0catMuonMomDown    .append(dftop0cat[x])
        dftop0catElectronMomUp  .append(dftop0cat[x])
        dftop0catElectronMomDown.append(dftop0cat[x])

        dftop0catMuonMomUp      [x] = dftop0catMuonMomUp      [x].Filter("mllMuonMomUp       > 85 && ptl1MuonMomUp       > 25 && ptl2MuonMomUp      > 20")
        dftop0catMuonMomDown    [x] = dftop0catMuonMomDown    [x].Filter("mllMuonMomDown     > 85 && ptl1MuonMomDown     > 25 && ptl2MuonMomDown    > 20")
        dftop0catElectronMomUp  [x] = dftop0catElectronMomUp  [x].Filter("mllElectronMomUp   > 85 && ptl1ElectronMomUp   > 25 && ptl2ElectronMomUp  > 20")
        dftop0catElectronMomDown[x] = dftop0catElectronMomDown[x].Filter("mllElectronMomDown > 85 && ptl1ElectronMomDown > 25 && ptl2ElectronMomDown> 20")

        dftop0cat[x] = dftop0cat[x].Filter("mll{0} > 85 && ptl1{0} > 25 && ptl2{0} > 20".format(altMass), "mll > 85 && ptl1 > 25 && ptl2 > 20")

        dftop1cat.append(dfcat[x].Filter("nbtag_goodbtag_Jet_bjet == 2", "b-jets"))
        dftop1catMuonMomUp      .append(dftop1cat[x])
        dftop1catMuonMomDown    .append(dftop1cat[x])
        dftop1catElectronMomUp  .append(dftop1cat[x])
        dftop1catElectronMomDown.append(dftop1cat[x])

        dftop1catMuonMomUp      [x] = dftop1catMuonMomUp      [x].Filter("mllMuonMomUp       > 85 && ptl1MuonMomUp       > 25 && ptl2MuonMomUp      > 20")
        dftop1catMuonMomDown    [x] = dftop1catMuonMomDown    [x].Filter("mllMuonMomDown     > 85 && ptl1MuonMomDown     > 25 && ptl2MuonMomDown    > 20")
        dftop1catElectronMomUp  [x] = dftop1catElectronMomUp  [x].Filter("mllElectronMomUp   > 85 && ptl1ElectronMomUp   > 25 && ptl2ElectronMomUp  > 20")
        dftop1catElectronMomDown[x] = dftop1catElectronMomDown[x].Filter("mllElectronMomDown > 85 && ptl1ElectronMomDown > 25 && ptl2ElectronMomDown> 20")

        dftop1cat[x] = dftop1cat[x].Filter("mll{0} > 85 && ptl1{0} > 25 && ptl2{0} > 20".format(altMass), "mll > 85 && ptl1 > 25 && ptl2 > 20")

        dfhwwxcat.append(dfcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0", "No b-jets")
                                 .Filter("ptll{0} > 30 && mll{0} < 85 && minPMET{0} > 20".format(altMass), "ptll > 30 && mll < 85 && minPMET > 20")
                                 )

        histo[ 6][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x), 50,  0, 3.1416), "dPhilMETMin","weightWW")
        histo[ 7][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x), 50,  0, 3.1416), "dPhilMETMin","weightWW")
        histo[ 8][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x), 50,  0, 3.1416), "dPhilMETMin","weightWW")
        histo[ 9][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x), 50,  0, 3.1416), "dPhilMETMin","weightWW")

        histo[10][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 100, 0, 200), "minPMET{0}".format(altMass),"weightWW")
        histo[11][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 100, 0, 200), "minPMET{0}".format(altMass),"weightWW")
        histo[12][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 100, 0, 200), "minPMET{0}".format(altMass),"weightWW")
        histo[13][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 100, 0, 200), "minPMET{0}".format(altMass),"weightWW")

        histo[14][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 100, 0, 200), "thePuppiMET_pt","weightWW")
        histo[15][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 100, 0, 200), "thePuppiMET_pt","weightWW")
        histo[16][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x), 100, 0, 200), "thePuppiMET_pt","weightWW")
        histo[17][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(17,x), "histo_{0}_{1}".format(17,x), 100, 0, 200), "thePuppiMET_pt","weightWW")

        histo[18][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(18,x), "histo_{0}_{1}".format(18,x), 50,  0, 5), "drll","weightWW")
        histo[19][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(19,x), "histo_{0}_{1}".format(19,x), 50,  0, 5), "drll","weightWW")
        histo[20][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(20,x), "histo_{0}_{1}".format(20,x), 50,  0, 5), "drll","weightWW")
        histo[21][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(21,x), "histo_{0}_{1}".format(21,x), 50,  0, 5), "drll","weightWW")

        histo[22][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(22,x), "histo_{0}_{1}".format(22,x), 50,  0, 3.1416), "dphill","weightWW")
        histo[23][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(23,x), "histo_{0}_{1}".format(23,x), 50,  0, 3.1416), "dphill","weightWW")
        histo[24][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(24,x), "histo_{0}_{1}".format(24,x), 50,  0, 3.1416), "dphill","weightWW")
        histo[25][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(25,x), "histo_{0}_{1}".format(25,x), 50,  0, 3.1416), "dphill","weightWW")

        histo[26][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(26,x), "histo_{0}_{1}".format(26,x), 40, 25, 225), "ptl1{0}".format(altMass),"weightWW")
        histo[27][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(27,x), "histo_{0}_{1}".format(27,x), 40, 25, 225), "ptl1{0}".format(altMass),"weightWW")
        histo[28][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(28,x), "histo_{0}_{1}".format(28,x), 40, 25, 225), "ptl1{0}".format(altMass),"weightWW")
        histo[29][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(29,x), "histo_{0}_{1}".format(29,x), 40, 25, 225), "ptl1{0}".format(altMass),"weightWW")

        histo[30][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(30,x), "histo_{0}_{1}".format(30,x), 40, 20, 220), "ptl2{0}".format(altMass),"weightWW")
        histo[31][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(31,x), "histo_{0}_{1}".format(31,x), 40, 20, 220), "ptl2{0}".format(altMass),"weightWW")
        histo[32][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(32,x), "histo_{0}_{1}".format(32,x), 40, 20, 220), "ptl2{0}".format(altMass),"weightWW")
        histo[33][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(33,x), "histo_{0}_{1}".format(33,x), 40, 20, 220), "ptl2{0}".format(altMass),"weightWW")

        histo[34][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(34,x), "histo_{0}_{1}".format(34,x), 25,  0,2.5), "etal1","weightWW")
        histo[35][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(35,x), "histo_{0}_{1}".format(35,x), 25,  0,2.5), "etal1","weightWW")
        histo[36][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(36,x), "histo_{0}_{1}".format(36,x), 25,  0,2.5), "etal1","weightWW")
        histo[37][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(37,x), "histo_{0}_{1}".format(37,x), 25,  0,2.5), "etal1","weightWW")

        histo[38][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(38,x), "histo_{0}_{1}".format(38,x), 25,  0,2.5), "etal2","weightWW")
        histo[39][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(39,x), "histo_{0}_{1}".format(39,x), 25,  0,2.5), "etal2","weightWW")
        histo[40][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(40,x), "histo_{0}_{1}".format(40,x), 25,  0,2.5), "etal2","weightWW")
        histo[41][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(41,x), "histo_{0}_{1}".format(41,x), 25,  0,2.5), "etal2","weightWW")

        histo[42][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(42,x), "histo_{0}_{1}".format(42,x), 4,-0.5,3.5), "ngood_jets","weightWW")
        histo[43][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(43,x), "histo_{0}_{1}".format(43,x), 4,-0.5,3.5), "ngood_jets","weightWW")
        histo[44][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(44,x), "histo_{0}_{1}".format(44,x), 4,-0.5,3.5), "ngood_jets","weightWW")
        histo[45][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(45,x), "histo_{0}_{1}".format(45,x), 4,-0.5,3.5), "ngood_jets","weightWW")

        histo[46][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(46,x), "histo_{0}_{1}".format(46,x), 50, 85, 385), "mll{0}".format(altMass),"weightWW")
        histo[47][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(47,x), "histo_{0}_{1}".format(47,x), 50, 85, 385), "mll{0}".format(altMass),"weightWW")
        histo[48][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(48,x), "histo_{0}_{1}".format(48,x), 50, 35,  85), "mll{0}".format(altMass),"weightWW")
        histo[49][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(49,x), "histo_{0}_{1}".format(49,x), 50, 85, 385), "mll{0}".format(altMass),"weightWW")

        histo[50][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(50,x), "histo_{0}_{1}".format(50,x), 50,  0, 200), "ptll{0}".format(altMass),"weightWW")
        histo[51][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(51,x), "histo_{0}_{1}".format(51,x), 50,  0, 200), "ptll{0}".format(altMass),"weightWW")
        histo[52][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(52,x), "histo_{0}_{1}".format(52,x), 30,  0,  30), "ptll{0}".format(altMass),"weightWW")
        histo[53][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(53,x), "histo_{0}_{1}".format(53,x), 50,  0, 200), "ptll{0}".format(altMass),"weightWW")

        histo[54][x] = dfhwwxcat[x].Histo1D(("histo_{0}_{1}".format(54,x), "histo_{0}_{1}".format(54,x), 40, 30, 190), "ptll{0}".format(altMass),"weightWW")
        histo[55][x] = dfhwwxcat[x].Histo1D(("histo_{0}_{1}".format(55,x), "histo_{0}_{1}".format(55,x), 100,20, 220), "minPMET{0}".format(altMass),"weightWW")
        histo[56][x] = dfhwwxcat[x].Histo1D(("histo_{0}_{1}".format(56,x), "histo_{0}_{1}".format(56,x), 50,  0, 3.1416), "dphill","weightWW")
        histo[57][x] = dfhwwxcat[x].Histo1D(("histo_{0}_{1}".format(57,x), "histo_{0}_{1}".format(57,x), 4,-0.5,3.5), "ngood_jets","weightWW")
        histo[58][x] = dftop0cat[x].Filter("nbtag_goodbtag_Jet_bjet == 1").Histo1D(("histo_{0}_{1}".format(58,x), "histo_{0}_{1}".format(58,x), 4,-0.5,3.5), "ngood_jets","weightWW")
        histo[59][x] = dftop0cat[x].Filter("nbtag_goodbtag_Jet_bjet == 2").Histo1D(("histo_{0}_{1}".format(59,x), "histo_{0}_{1}".format(59,x), 4,-0.5,3.5), "ngood_jets","weightWW")

        histo[60][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(60,x), "histo_{0}_{1}".format(60,x), 50,-5.0,5.0), "good_Jet_eta","weightWW")
        histo[61][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(61,x), "histo_{0}_{1}".format(61,x), 50,-5.0,5.0), "good_Jet_etaJes0Up","weightWW")
        histo[62][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(62,x), "histo_{0}_{1}".format(62,x), 50,-5.0,5.0), "good_Jet_etaJes0Down","weightWW")
        histo[63][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(63,x), "histo_{0}_{1}".format(63,x), 50,-5.0,5.0), "good_Jet_eta","weightWW")
        histo[64][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(64,x), "histo_{0}_{1}".format(64,x), 50,-5.0,5.0), "good_Jet_etaJes0Up","weightWW")
        histo[65][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(65,x), "histo_{0}_{1}".format(65,x), 50,-5.0,5.0), "good_Jet_etaJes0Down","weightWW")
        histo[66][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(66,x), "histo_{0}_{1}".format(66,x), 50,-5.0,5.0), "good_Jet_eta","weightWW")
        histo[67][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(67,x), "histo_{0}_{1}".format(67,x), 50,-5.0,5.0), "good_Jet_etaJes0Up","weightWW")
        histo[68][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(68,x), "histo_{0}_{1}".format(68,x), 50,-5.0,5.0), "good_Jet_etaJes0Down","weightWW")

        dftop0cat[x] = dftop0cat[x].Filter("nbtag_goodbtag_Jet_bjet == 1")
        dftop0catMuonMomUp      [x] = dftop0catMuonMomUp      [x].Filter("nbtag_goodbtag_Jet_bjet == 1")
        dftop0catMuonMomDown    [x] = dftop0catMuonMomDown    [x].Filter("nbtag_goodbtag_Jet_bjet == 1")
        dftop0catElectronMomUp  [x] = dftop0catElectronMomUp  [x].Filter("nbtag_goodbtag_Jet_bjet == 1")
        dftop0catElectronMomDown[x] = dftop0catElectronMomDown[x].Filter("nbtag_goodbtag_Jet_bjet == 1")

        histo[69][x] = dfssx1cat[x].Histo1D(("histo_{0}_{1}".format(69,x), "histo_{0}_{1}".format(69,x), 60, 50, 410), "mll{0}".format(altMass),"weightWW")
        histo[70][x] = dfssx2cat[x].Histo1D(("histo_{0}_{1}".format(70,x), "histo_{0}_{1}".format(70,x), 60, 50, 410), "mll{0}".format(altMass),"weightWW")
        dfssx2cat[x] = dfssx2cat[x].Filter("mll{0} > 130".format(altMass), "mll > 130")
        histo[71][x] = dfssx1cat[x].Histo1D(("histo_{0}_{1}".format(71,x), "histo_{0}_{1}".format(71,x), 4,-0.5,3.5), "ngood_jets","weightWW")
        histo[72][x] = dfssx2cat[x].Histo1D(("histo_{0}_{1}".format(72,x), "histo_{0}_{1}".format(72,x), 4,-0.5,3.5), "ngood_jets","weightWW")

        histo[73][x] = dfssx0cat[x].Histo1D(("histo_{0}_{1}".format(73,x), "histo_{0}_{1}".format(73,x), 50,  0, 200), "ptww","weightWW")
        histo[74][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(74,x), "histo_{0}_{1}".format(74,x), 50,  0, 200), "ptww","weightWW")
        histo[75][x] = dfztt0cat[x].Histo1D(("histo_{0}_{1}".format(75,x), "histo_{0}_{1}".format(75,x), 30,  0, 200), "ptww","weightWW")
        histo[76][x] = dftop0cat[x].Histo1D(("histo_{0}_{1}".format(76,x), "histo_{0}_{1}".format(76,x), 50,  0, 200), "ptww","weightWW")

        histo[77][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(77,x), "histo_{0}_{1}".format(77,x), 10,-0.5, 9.5), "nPileupJets","weightWW")

        #histo[100][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(100,x), "histo_{0}_{1}".format(100,x), 100, 0, 200), "thePuppiMET_pt"		  ,"weightWW")
        #histo[101][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(101,x), "histo_{0}_{1}".format(101,x), 100, 0, 200), "thePuppiMET_ptJERUp" 	  ,"weightWW")
        #histo[102][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(102,x), "histo_{0}_{1}".format(102,x), 100, 0, 200), "thePuppiMET_ptJERDown"	  ,"weightWW")
        #histo[103][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(103,x), "histo_{0}_{1}".format(103,x), 100, 0, 200), "thePuppiMET_ptJESUp" 	  ,"weightWW")
        #histo[104][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(104,x), "histo_{0}_{1}".format(104,x), 100, 0, 200), "thePuppiMET_ptJESDown"	  ,"weightWW")
        #histo[105][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(105,x), "histo_{0}_{1}".format(105,x), 100, 0, 200), "thePuppiMET_ptUnclusteredUp"   ,"weightWW")
        #histo[106][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(106,x), "histo_{0}_{1}".format(106,x), 100, 0, 200), "thePuppiMET_ptUnclusteredDown" ,"weightWW")
        #histo[107][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(107,x), "histo_{0}_{1}".format(107,x), 100, 0, 200), "MET_ptDef"			  ,"weightWW")
        #histo[108][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(108,x), "histo_{0}_{1}".format(108,x), 100, 0, 200), "MET_ptJes0Up"		  ,"weightWW")
        #histo[109][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(109,x), "histo_{0}_{1}".format(109,x), 100, 0, 200), "MET_ptJes0Down"		  ,"weightWW")

        if(x == plotCategory("kPlotData") and print_info == True):
             histo_test = (dfwwx0cat[x].Define("print_info","print_info(run,event)")
                          .Filter("print_info > 0")
                          .Histo1D(("test", "test", 4,-0.5,3.5), "ngood_jets","weightWW"))

        if(makeDataCards == -1):
            histo[100][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(100,x), "histo_{0}_{1}".format(100,x), 4,-0.5,3.5), "ngood_jets","weight")
            histo[101][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(101,x), "histo_{0}_{1}".format(101,x), 4,-0.5,3.5), "ngood_jets","weight0")
            histo[102][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(102,x), "histo_{0}_{1}".format(102,x), 4,-0.5,3.5), "ngood_jets","weight1")
            histo[103][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(103,x), "histo_{0}_{1}".format(103,x), 4,-0.5,3.5), "ngood_jets","weight2")
            histo[104][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(104,x), "histo_{0}_{1}".format(104,x), 4,-0.5,3.5), "ngood_jets","weight3")
            histo[105][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(105,x), "histo_{0}_{1}".format(105,x), 4,-0.5,3.5), "ngood_jets","weight4")
            histo[106][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(106,x), "histo_{0}_{1}".format(106,x), 4,-0.5,3.5), "ngood_jets","weight5")
            histo[107][x] = dfwwx0cat[x].Histo1D(("histo_{0}_{1}".format(107,x), "histo_{0}_{1}".format(107,x), 4,-0.5,3.5), "ngood_jets","weight6")

        if(makeDataCards >= 1):
            BinXF = 4
            minXF = -0.5
            maxXF = 3.5
            BinYF = 4
            minYF = -0.5
            maxYF = 3.5

            startF = 0
            for nv in range(0,152):
                histo2D[startF+nv][x] = makeFinalVariable2D(dfssx0cat[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,nv)
            histo2D[startF+152][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes0Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,152)
            histo2D[startF+153][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes0Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,153)
            histo2D[startF+154][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJerUp"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,154)
            histo2D[startF+155][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJerDown"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,155)
            histo2D[startF+156][x]    = makeFinalVariable2D(dfssx0catMuonMomUp      [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,156)
            histo2D[startF+157][x]    = makeFinalVariable2D(dfssx0catMuonMomDown    [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,157)
            histo2D[startF+158][x]    = makeFinalVariable2D(dfssx0catElectronMomUp  [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,158)
            histo2D[startF+159][x]    = makeFinalVariable2D(dfssx0catElectronMomDown[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,159)
            histo2D[startF+160][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,160)
            histo2D[startF+161][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,161)
            histo2D[startF+162][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,162)
            histo2D[startF+163][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,163)
            histo2D[startF+164][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,164)
            histo2D[startF+165][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,165)
            histo2D[startF+166][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes1Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,166)
            histo2D[startF+167][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes1Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,167)
            histo2D[startF+168][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes2Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,168)
            histo2D[startF+169][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes2Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,169)
            histo2D[startF+170][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes3Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,170)
            histo2D[startF+171][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes3Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,171)
            histo2D[startF+172][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes4Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,172)
            histo2D[startF+173][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes4Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,173)
            histo2D[startF+174][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes5Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,174)
            histo2D[startF+175][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes5Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,175)
            histo2D[startF+176][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes6Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,176)
            histo2D[startF+177][x]    = makeFinalVariable2D(dfssx0cat[x],"ngood_jetsJes6Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,177)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 0
                histoNonPrompt[0+startNonPrompt] = dfssx0cat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfssx0cat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfssx0cat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfssx0cat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfssx0cat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfssx0cat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte2")

            startF = 200
            for nv in range(0,152):
                histo2D[startF+nv][x] = makeFinalVariable2D(dfwwx0cat[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,nv)
            histo2D[startF+152][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes0Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,152)
            histo2D[startF+153][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes0Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,153)
            histo2D[startF+154][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJerUp"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,154)
            histo2D[startF+155][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJerDown"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,155)
            histo2D[startF+156][x]    = makeFinalVariable2D(dfwwx0catMuonMomUp      [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,156)
            histo2D[startF+157][x]    = makeFinalVariable2D(dfwwx0catMuonMomDown    [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,157)
            histo2D[startF+158][x]    = makeFinalVariable2D(dfwwx0catElectronMomUp  [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,158)
            histo2D[startF+159][x]    = makeFinalVariable2D(dfwwx0catElectronMomDown[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,159)
            histo2D[startF+160][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,160)
            histo2D[startF+161][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,161)
            histo2D[startF+162][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,162)
            histo2D[startF+163][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,163)
            histo2D[startF+164][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,164)
            histo2D[startF+165][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,165)
            histo2D[startF+166][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes1Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,166)
            histo2D[startF+167][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes1Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,167)
            histo2D[startF+168][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes2Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,168)
            histo2D[startF+169][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes2Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,169)
            histo2D[startF+170][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes3Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,170)
            histo2D[startF+171][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes3Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,171)
            histo2D[startF+172][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes4Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,172)
            histo2D[startF+173][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes4Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,173)
            histo2D[startF+174][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes5Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,174)
            histo2D[startF+175][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes5Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,175)
            histo2D[startF+176][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes6Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,176)
            histo2D[startF+177][x]    = makeFinalVariable2D(dfwwx0cat[x],"ngood_jetsJes6Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,177)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 6
                histoNonPrompt[0+startNonPrompt] = dfwwx0cat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwwx0cat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwwx0cat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwwx0cat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwwx0cat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwwx0cat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte2")

            startF = 400
            for nv in range(0,152):
                histo2D[startF+nv][x] = makeFinalVariable2D(dfztt0cat[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,nv)
            histo2D[startF+152][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes0Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,152)
            histo2D[startF+153][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes0Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,153)
            histo2D[startF+154][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJerUp"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,154)
            histo2D[startF+155][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJerDown"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,155)
            histo2D[startF+156][x]    = makeFinalVariable2D(dfztt0catMuonMomUp      [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,156)
            histo2D[startF+157][x]    = makeFinalVariable2D(dfztt0catMuonMomDown    [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,157)
            histo2D[startF+158][x]    = makeFinalVariable2D(dfztt0catElectronMomUp  [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,158)
            histo2D[startF+159][x]    = makeFinalVariable2D(dfztt0catElectronMomDown[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,159)
            histo2D[startF+160][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,160)
            histo2D[startF+161][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,161)
            histo2D[startF+162][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,162)
            histo2D[startF+163][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,163)
            histo2D[startF+164][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,164)
            histo2D[startF+165][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,165)
            histo2D[startF+166][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes1Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,166)
            histo2D[startF+167][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes1Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,167)
            histo2D[startF+168][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes2Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,168)
            histo2D[startF+169][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes2Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,169)
            histo2D[startF+170][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes3Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,170)
            histo2D[startF+171][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes3Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,171)
            histo2D[startF+172][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes4Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,172)
            histo2D[startF+173][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes4Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,173)
            histo2D[startF+174][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes5Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,174)
            histo2D[startF+175][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes5Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,175)
            histo2D[startF+176][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes6Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,176)
            histo2D[startF+177][x]    = makeFinalVariable2D(dfztt0cat[x],"ngood_jetsJes6Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,177)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 12
                histoNonPrompt[0+startNonPrompt] = dfztt0cat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfztt0cat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfztt0cat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfztt0cat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfztt0cat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfztt0cat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte2")

            startF = 600
            for nv in range(0,152):
                histo2D[startF+nv][x] = makeFinalVariable2D(dftop0cat[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,nv)
            histo2D[startF+152][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes0Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,152)
            histo2D[startF+153][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes0Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,153)
            histo2D[startF+154][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJerUp"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,154)
            histo2D[startF+155][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJerDown"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,155)
            histo2D[startF+156][x]    = makeFinalVariable2D(dftop0catMuonMomUp      [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,156)
            histo2D[startF+157][x]    = makeFinalVariable2D(dftop0catMuonMomDown    [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,157)
            histo2D[startF+158][x]    = makeFinalVariable2D(dftop0catElectronMomUp  [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,158)
            histo2D[startF+159][x]    = makeFinalVariable2D(dftop0catElectronMomDown[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,159)
            histo2D[startF+160][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,160)
            histo2D[startF+161][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,161)
            histo2D[startF+162][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,162)
            histo2D[startF+163][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,163)
            histo2D[startF+164][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,164)
            histo2D[startF+165][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,165)
            histo2D[startF+166][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes1Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,166)
            histo2D[startF+167][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes1Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,167)
            histo2D[startF+168][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes2Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,168)
            histo2D[startF+169][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes2Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,169)
            histo2D[startF+170][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes3Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,170)
            histo2D[startF+171][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes3Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,171)
            histo2D[startF+172][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes4Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,172)
            histo2D[startF+173][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes4Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,173)
            histo2D[startF+174][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes5Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,174)
            histo2D[startF+175][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes5Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,175)
            histo2D[startF+176][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes6Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,176)
            histo2D[startF+177][x]    = makeFinalVariable2D(dftop0cat[x],"ngood_jetsJes6Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,177)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 18
                histoNonPrompt[0+startNonPrompt] = dftop0cat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dftop0cat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dftop0cat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dftop0cat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dftop0cat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dftop0cat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte2")

            startF = 800
            for nv in range(0,152):
                histo2D[startF+nv][x] = makeFinalVariable2D(dftop1cat[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,nv)
            histo2D[startF+152][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes0Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,152)
            histo2D[startF+153][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes0Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,153)
            histo2D[startF+154][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJerUp"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,154)
            histo2D[startF+155][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJerDown"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,155)
            histo2D[startF+156][x]    = makeFinalVariable2D(dftop1catMuonMomUp      [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,156)
            histo2D[startF+157][x]    = makeFinalVariable2D(dftop1catMuonMomDown    [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,157)
            histo2D[startF+158][x]    = makeFinalVariable2D(dftop1catElectronMomUp  [x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,158)
            histo2D[startF+159][x]    = makeFinalVariable2D(dftop1catElectronMomDown[x],"ngood_jets","theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,159)
            histo2D[startF+160][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,160)
            histo2D[startF+161][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,161)
            histo2D[startF+162][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,162)
            histo2D[startF+163][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,163)
            histo2D[startF+164][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,164)
            histo2D[startF+165][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jets"		    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,165)
            histo2D[startF+166][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes1Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,166)
            histo2D[startF+167][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes1Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,167)
            histo2D[startF+168][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes2Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,168)
            histo2D[startF+169][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes2Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,169)
            histo2D[startF+170][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes3Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,170)
            histo2D[startF+171][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes3Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,171)
            histo2D[startF+172][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes4Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,172)
            histo2D[startF+173][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes4Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,173)
            histo2D[startF+174][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes5Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,174)
            histo2D[startF+175][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes5Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,175)
            histo2D[startF+176][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes6Up"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,176)
            histo2D[startF+177][x]    = makeFinalVariable2D(dftop1cat[x],"ngood_jetsJes6Down"	    ,"theGenCat",theCat,startF,x,BinXF,minXF,maxXF,BinYF,minYF,maxYF,177)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 24
                histoNonPrompt[0+startNonPrompt] = dftop1cat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dftop1cat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dftop1cat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dftop1cat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dftop1cat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dftop1cat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte2")

            BinXF1 = 25
            minXF1 = 85
            maxXF1 = 385
            if(makeDataCards >= 2):
                startF = 1000
                for nv in range(0,152):
                    histo2D[startF+nv][x] = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==0")        ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,nv)
                histo2D[startF+152][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes0Up==0")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,152)
                histo2D[startF+153][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes0Down==0")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,153)
                histo2D[startF+154][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJerUp==0")      ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,154)
                histo2D[startF+155][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJerDown==0")    ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,155)
                histo2D[startF+156][x]    = makeFinalVariable2D(dfwwx0catMuonMomUp	[x].Filter("ngood_jets==0"),"mllMuonMomUp"	,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,156)
                histo2D[startF+157][x]    = makeFinalVariable2D(dfwwx0catMuonMomDown	[x].Filter("ngood_jets==0"),"mllMuonMomDown"	,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,157)
                histo2D[startF+158][x]    = makeFinalVariable2D(dfwwx0catElectronMomUp  [x].Filter("ngood_jets==0"),"mllElectronMomUp"  ,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,158)
                histo2D[startF+159][x]    = makeFinalVariable2D(dfwwx0catElectronMomDown[x].Filter("ngood_jets==0"),"mllElectronMomDown","theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,159)
                histo2D[startF+160][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==0")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,160)
                histo2D[startF+161][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==0")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,161)
                histo2D[startF+162][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==0")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,162)
                histo2D[startF+163][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==0")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,163)
                histo2D[startF+164][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==0")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,164)
                histo2D[startF+165][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==0")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,165)
                histo2D[startF+166][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes1Up==0")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,166)
                histo2D[startF+167][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes1Down==0")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,167)
                histo2D[startF+168][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes2Up==0")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,168)
                histo2D[startF+169][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes2Down==0")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,169)
                histo2D[startF+170][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes3Up==0")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,170)
                histo2D[startF+171][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes3Down==0")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,171)
                histo2D[startF+172][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes4Up==0")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,172)
                histo2D[startF+173][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes4Down==0")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,173)
                histo2D[startF+174][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes5Up==0")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,174)
                histo2D[startF+175][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes5Down==0")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,175)
                histo2D[startF+176][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes6Up==0")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,176)
                histo2D[startF+177][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes6Down==0")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,177)
                if(x == plotCategory("kPlotNonPrompt")):
                    startNonPrompt = 30
                    histoNonPrompt[0+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==0").Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm0")
                    histoNonPrompt[1+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==0").Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm1")
                    histoNonPrompt[2+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==0").Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm2")
                    histoNonPrompt[3+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==0").Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte0")
                    histoNonPrompt[4+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==0").Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte1")
                    histoNonPrompt[5+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==0").Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte2")

                startF = 1200
                for nv in range(0,152):
                    histo2D[startF+nv][x] = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==1")        ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,nv)
                histo2D[startF+152][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes0Up==1")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,152)
                histo2D[startF+153][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes0Down==1")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,153)
                histo2D[startF+154][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJerUp==1")      ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,154)
                histo2D[startF+155][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJerDown==1")    ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,155)
                histo2D[startF+156][x]    = makeFinalVariable2D(dfwwx0catMuonMomUp	[x].Filter("ngood_jets==1"),"mllMuonMomUp"	,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,156)
                histo2D[startF+157][x]    = makeFinalVariable2D(dfwwx0catMuonMomDown	[x].Filter("ngood_jets==1"),"mllMuonMomDown"	,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,157)
                histo2D[startF+158][x]    = makeFinalVariable2D(dfwwx0catElectronMomUp  [x].Filter("ngood_jets==1"),"mllElectronMomUp"  ,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,158)
                histo2D[startF+159][x]    = makeFinalVariable2D(dfwwx0catElectronMomDown[x].Filter("ngood_jets==1"),"mllElectronMomDown","theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,159)
                histo2D[startF+160][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==1")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,160)
                histo2D[startF+161][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==1")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,161)
                histo2D[startF+162][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==1")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,162)
                histo2D[startF+163][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==1")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,163)
                histo2D[startF+164][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==1")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,164)
                histo2D[startF+165][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets==1")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,165)
                histo2D[startF+166][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes1Up==1")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,166)
                histo2D[startF+167][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes1Down==1")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,167)
                histo2D[startF+168][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes2Up==1")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,168)
                histo2D[startF+169][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes2Down==1")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,169)
                histo2D[startF+170][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes3Up==1")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,170)
                histo2D[startF+171][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes3Down==1")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,171)
                histo2D[startF+172][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes4Up==1")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,172)
                histo2D[startF+173][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes4Down==1")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,173)
                histo2D[startF+174][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes5Up==1")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,174)
                histo2D[startF+175][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes5Down==1")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,175)
                histo2D[startF+176][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes6Up==1")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,176)
                histo2D[startF+177][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes6Down==1")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,177)
                if(x == plotCategory("kPlotNonPrompt")):
                    startNonPrompt = 36
                    histoNonPrompt[0+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==1").Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm0")
                    histoNonPrompt[1+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==1").Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm1")
                    histoNonPrompt[2+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==1").Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm2")
                    histoNonPrompt[3+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==1").Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte0")
                    histoNonPrompt[4+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==1").Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte1")
                    histoNonPrompt[5+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets==1").Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte2")

                startF = 1400
                for nv in range(0,152):
                    histo2D[startF+nv][x] = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets>=2")        ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,nv)
                histo2D[startF+152][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes0Up>=2")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,152)
                histo2D[startF+153][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes0Down>=2")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,153)
                histo2D[startF+154][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJerUp>=2")      ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,154)
                histo2D[startF+155][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJerDown>=2")    ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,155)
                histo2D[startF+156][x]    = makeFinalVariable2D(dfwwx0catMuonMomUp	[x].Filter("ngood_jets>=2"),"mllMuonMomUp"	,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,156)
                histo2D[startF+157][x]    = makeFinalVariable2D(dfwwx0catMuonMomDown	[x].Filter("ngood_jets>=2"),"mllMuonMomDown"	,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,157)
                histo2D[startF+158][x]    = makeFinalVariable2D(dfwwx0catElectronMomUp  [x].Filter("ngood_jets>=2"),"mllElectronMomUp"  ,"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,158)
                histo2D[startF+159][x]    = makeFinalVariable2D(dfwwx0catElectronMomDown[x].Filter("ngood_jets>=2"),"mllElectronMomDown","theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,159)
                histo2D[startF+160][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets>=2")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,160)
                histo2D[startF+161][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets>=2")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,161)
                histo2D[startF+162][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets>=2")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,162)
                histo2D[startF+163][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets>=2")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,163)
                histo2D[startF+164][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets>=2")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,164)
                histo2D[startF+165][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jets>=2")	       ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,165)
                histo2D[startF+166][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes1Up>=2")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,166)
                histo2D[startF+167][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes1Down>=2")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,167)
                histo2D[startF+168][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes2Up>=2")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,168)
                histo2D[startF+169][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes2Down>=2")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,169)
                histo2D[startF+170][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes3Up>=2")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,170)
                histo2D[startF+171][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes3Down>=2")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,171)
                histo2D[startF+172][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes4Up>=2")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,172)
                histo2D[startF+173][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes4Down>=2")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,173)
                histo2D[startF+174][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes5Up>=2")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,174)
                histo2D[startF+175][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes5Down>=2")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,175)
                histo2D[startF+176][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes6Up>=2")     ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,176)
                histo2D[startF+177][x]    = makeFinalVariable2D(dfwwx0cat[x].Filter("ngood_jetsJes6Down>=2")   ,"mll{0}".format(altMass),"theGenCat",theCat,startF,x,BinXF1,minXF1,maxXF1,BinYF,minYF,maxYF,177)
                if(x == plotCategory("kPlotNonPrompt")):
                    startNonPrompt = 42
                    histoNonPrompt[0+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets>=2").Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm0")
                    histoNonPrompt[1+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets>=2").Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm1")
                    histoNonPrompt[2+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets>=2").Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAltm2")
                    histoNonPrompt[3+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets>=2").Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte0")
                    histoNonPrompt[4+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets>=2").Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte1")
                    histoNonPrompt[5+startNonPrompt] = dfwwx0cat[x].Filter("ngood_jets>=2").Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF1,minXF1,maxXF1), "mll{0}".format(altMass),"weightFakeAlte2")

    report = []
    for x in range(nCat):
        report.append(dfwwx0cat[x].Report())
        if(x != theCat): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    if(makeDataCards >= 1):
        for j in range(0,1000):
            for x in range(nCat):
                histoMVA[j][x] = ROOT.TH1D("histoMVA_{0}_{1}".format(j,x), "histoMVA_{0}_{1}".format(j,x), BinXF,minXF,maxXF)
        for j in range(1000,nHistoMVA):
            for x in range(nCat):
                histoMVA[j][x] = ROOT.TH1D("histoMVA_{0}_{1}".format(j,x), "histoMVA_{0}_{1}".format(j,x), BinXF1,minXF1,maxXF1)

    for j in range(nHistoMVA):
        for x in range(nCat):
            if(histo2D[j][x] == 0):
                histoMVA[j][x] = 0
                continue
            for i in range(histo2D[j][x].GetNbinsX()):
                histo2D[j][x].SetBinContent(i+1,histo2D[j][x].GetNbinsY(),histo2D[j][x].GetBinContent(i+1,histo2D[j][x].GetNbinsY())+histo2D[j][x].GetBinContent(i+1,histo2D[j][x].GetNbinsY()+1))
                histo2D[j][x].SetBinError  (i+1,histo2D[j][x].GetNbinsY(),pow(pow(histo2D[j][x].GetBinError(i+1,histo2D[j][x].GetNbinsY()),2)+pow(histo2D[j][x].GetBinError(i+1,histo2D[j][x].GetNbinsY()+1),2),0.5))
                histo2D[j][x].SetBinContent(i+1,histo2D[j][x].GetNbinsY()+1,0.0)
                histo2D[j][x].SetBinError  (i+1,histo2D[j][x].GetNbinsY()+1,0.0)

            for i in range(histo2D[j][x].GetNbinsY()):
                histo2D[j][x].SetBinContent(histo2D[j][x].GetNbinsX(),i+1,histo2D[j][x].GetBinContent(histo2D[j][x].GetNbinsX(),i+1)+histo2D[j][x].GetBinContent(histo2D[j][x].GetNbinsX()+1,i+1))
                histo2D[j][x].SetBinError  (histo2D[j][x].GetNbinsX(),i+1,pow(pow(histo2D[j][x].GetBinError(histo2D[j][x].GetNbinsX(),i+1),2)+pow(histo2D[j][x].GetBinError(histo2D[j][x].GetNbinsX()+1,i+1),2),0.5))
                histo2D[j][x].SetBinContent(histo2D[j][x].GetNbinsX()+1,i+1,0.0)
                histo2D[j][x].SetBinError  (histo2D[j][x].GetNbinsX()+1,i+1,0.0)

            if(x == plotCategory("kPlotqqWW") or x == plotCategory("kPlotggWW")):
                for i in range(histoMVA[j][x].GetNbinsX()):
                    histoMVA[j][plotCategory("kPlotqqWW")].SetBinContent(i+1,histoMVA[j][plotCategory("kPlotqqWW")].GetBinContent(i+1)+histo2D[j][x].GetBinContent(i+1,1))
                    histoMVA[j][plotCategory("kPlotqqWW")].SetBinError  (i+1,pow(pow(histoMVA[j][plotCategory("kPlotqqWW")].GetBinError(i+1),2)+pow(histo2D[j][x].GetBinError(i+1,1),2),0.5))

                    histoMVA[j][plotCategory("kPlotSignal0")].SetBinContent(i+1,histoMVA[j][plotCategory("kPlotSignal0")].GetBinContent(i+1)+histo2D[j][x].GetBinContent(i+1,2))
                    histoMVA[j][plotCategory("kPlotSignal0")].SetBinError  (i+1,pow(pow(histoMVA[j][plotCategory("kPlotSignal0")].GetBinError(i+1),2)+pow(histo2D[j][x].GetBinError(i+1,2),2),0.5))

                    histoMVA[j][plotCategory("kPlotSignal1")].SetBinContent(i+1,histoMVA[j][plotCategory("kPlotSignal1")].GetBinContent(i+1)+histo2D[j][x].GetBinContent(i+1,3))
                    histoMVA[j][plotCategory("kPlotSignal1")].SetBinError  (i+1,pow(pow(histoMVA[j][plotCategory("kPlotSignal1")].GetBinError(i+1),2)+pow(histo2D[j][x].GetBinError(i+1,4),2),0.5))

                    histoMVA[j][plotCategory("kPlotSignal2")].SetBinContent(i+1,histoMVA[j][plotCategory("kPlotSignal2")].GetBinContent(i+1)+histo2D[j][x].GetBinContent(i+1,4))
                    histoMVA[j][plotCategory("kPlotSignal2")].SetBinError  (i+1,pow(pow(histoMVA[j][plotCategory("kPlotSignal2")].GetBinError(i+1),2)+pow(histo2D[j][x].GetBinError(i+1,5),2),0.5))

            else:
                for i in range(histoMVA[j][x].GetNbinsX()):
                    histoMVA[j][x].SetBinContent(i+1,histoMVA[j][x].GetBinContent(i+1)+histo2D[j][x].GetBinContent(i+1,1))
                    histoMVA[j][x].SetBinError  (i+1,pow(pow(histoMVA[j][x].GetBinError(i+1),2)+pow(histo2D[j][x].GetBinError(i+1,1),2),0.5))

    for x in range(nCat):
        for i in range(histo[60][x].GetNbinsX()):
            diff = abs(histo[61][x].GetBinContent(i+1)-histo[62][x].GetBinContent(i+1))/2.
            histo[60][x].SetBinError(i+1,pow(pow(histo[60][x].GetBinError(i+1),2)+pow(diff,2),0.5))
        histo[61][x] = 0
        histo[62][x] = 0
        for i in range(histo[63][x].GetNbinsX()):
            diff = abs(histo[64][x].GetBinContent(i+1)-histo[65][x].GetBinContent(i+1))/2.
            histo[63][x].SetBinError(i+1,pow(pow(histo[63][x].GetBinError(i+1),2)+pow(diff,2),0.5))
        histo[64][x] = 0
        histo[65][x] = 0
        for i in range(histo[66][x].GetNbinsX()):
            diff = abs(histo[67][x].GetBinContent(i+1)-histo[68][x].GetBinContent(i+1))/2.
            histo[66][x].SetBinError(i+1,pow(pow(histo[66][x].GetBinError(i+1),2)+pow(diff,2),0.5))
        histo[67][x] = 0
        histo[68][x] = 0

    myfile = ROOT.TFile("fillhisto_wwAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].Write()
        for j in range(nHistoMVA):
            if(histoMVA[j][i] == 0): continue
            histoMVA[j][i].Write()
    for i in range(nhistoNonPrompt):
        if(histoNonPrompt[i] == 0): continue
        histoNonPrompt[i].Write()
    myfile.Close()

def readMCSample(sampleNOW,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    files = getMClist(sampleNOW, skimType)
    print("Total files: {0}".format(len(files)))

    runTree = ROOT.TChain("Runs")
    for f in range(len(files)):
        runTree.AddFile(files[f])

    genEventSumWeight = 0
    genEventSumNoWeight = 0
    nTheoryReplicas = [103, 9, 4]
    genEventSumLHEScaleWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    genEventSumPSWeight = [0, 0, 0, 0, 0]
    for i in range(runTree.GetEntries()):
        runTree.GetEntry(i)
        genEventSumWeight += runTree.genEventSumw
        genEventSumNoWeight += runTree.genEventCount
        if(runTree.FindBranch("nLHEPdfSumw") and runTree.nLHEPdfSumw < nTheoryReplicas[0]):
            nTheoryReplicas[0] = runTree.nLHEPdfSumw
        for n in range(9):
            if(n < runTree.nLHEScaleSumw):
                genEventSumLHEScaleWeight[n] += runTree.LHEScaleSumw[n]
            else:
                genEventSumLHEScaleWeight[n] += 1.0
                nTheoryReplicas[1] = runTree.nLHEScaleSumw
        for n in range(4):
            if(n < runTree.nPSSumw):
                genEventSumPSWeight[n] += runTree.PSSumw[n]
            else:
                genEventSumPSWeight[n] += 1.0
                nTheoryReplicas[2] = runTree.nPSSumw
        genEventSumPSWeight[4] += 1
    print("Number of Theory replicas: {0} / {1} / {2}".format(nTheoryReplicas[0],nTheoryReplicas[1],nTheoryReplicas[2]))

    genEventSumLHEScaleRenorm = [1, 1, 1, 1, 1, 1]
    genEventSumPSRenorm = [1, 1, 1, 1]
    if(SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotqqWW") or
       SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotggWW") or
       SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotTop") or
       SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotDY") or
       SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotWZ") or
       SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotEWKWZ") or
       SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotZZ")):
        genEventSumLHEScaleRenorm[0] = genEventSumLHEScaleWeight[0] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[1] = genEventSumLHEScaleWeight[1] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[2] = genEventSumLHEScaleWeight[3] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[3] = genEventSumLHEScaleWeight[5] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[4] = genEventSumLHEScaleWeight[7] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[5] = genEventSumLHEScaleWeight[8] / genEventSumLHEScaleWeight[4]
        for n in range(4):
            genEventSumPSRenorm[n] = genEventSumPSWeight[n] / genEventSumPSWeight[4]
    print("genEventSumLHEScaleRenorm: ",genEventSumLHEScaleRenorm)
    print("genEventSumPSRenorm: ",genEventSumPSRenorm)

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

    print("genEventSum({0}): {1} / Events(total/ntuple): {2} / {3}".format(runTree.GetEntries(),genEventSumWeight,genEventSumNoWeight,nevents))
    print("WeightExact/Approx %f / %f / Cross section: %f" %(weight, weightApprox, SwitchSample(sampleNOW, skimType)[1]))

    PDType = os.path.basename(SwitchSample(sampleNOW, skimType)[0]).split('+')[0]

    analysis(df,sampleNOW,SwitchSample(sampleNOW,skimType)[2],weight,year,PDType,"false",whichJob,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

def readDASample(sampleNOW,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    PDType = "0"
    if  (sampleNOW >= 1000 and sampleNOW <= 1009): PDType = "SingleMuon"
    elif(sampleNOW >= 1010 and sampleNOW <= 1019): PDType = "DoubleMuon"
    elif(sampleNOW >= 1020 and sampleNOW <= 1029): PDType = "MuonEG"
    elif(sampleNOW >= 1030 and sampleNOW <= 1039): PDType = "EGamma"
    elif(sampleNOW >= 1040 and sampleNOW <= 1049): PDType = "Muon"
    elif(sampleNOW >= 1050 and sampleNOW <= 1059): PDType = "MET"

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

    genEventSumLHEScaleRenorm = [1, 1, 1, 1, 1, 1]
    genEventSumPSRenorm = [1, 1, 1, 1]

    weight=1.
    nevents = df.Count().GetValue()
    print("%s entries in the dataset" %nevents)

    analysis(df,sampleNOW,sampleNOW,weight,year,PDType,"true",whichJob,0,genEventSumLHEScaleRenorm,genEventSumPSRenorm,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

if __name__ == "__main__":

    group = 10

    skimType = "2l"
    year = 2022
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

    puWeights = []
    puPath = "data/puWeights_UL_{0}.root".format(year)
    fPuFile = ROOT.TFile(puPath)
    puWeights.append(fPuFile.Get("puWeights"))
    puWeights.append(fPuFile.Get("puWeightsUp"))
    puWeights.append(fPuFile.Get("puWeightsDown"))
    for x in range(3):
        puWeights[x].SetDirectory(0)
    fPuFile.Close()

    histoFakeEtaPt_mu = []
    histoFakeEtaPt_el = []
    fakePath = "data/histoFakeEtaPt_{0}.root".format(year)
    fFakeFile = ROOT.TFile(fakePath)
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1001_anaType1".format(muSelChoice)))
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1002_anaType1".format(muSelChoice)))
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1003_anaType1".format(muSelChoice)))
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1001_anaType2".format(muSelChoice)))
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1002_anaType2".format(muSelChoice)))
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1003_anaType2".format(muSelChoice)))
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1001_anaType3".format(muSelChoice)))
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1002_anaType3".format(muSelChoice)))
    histoFakeEtaPt_mu.append(fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}_fakeAnalysis1003_anaType3".format(muSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1001_anaType1".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1002_anaType1".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1003_anaType1".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1001_anaType2".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1002_anaType2".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1003_anaType2".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1001_anaType3".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1002_anaType3".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1003_anaType3".format(elSelChoice)))
    for x in range(9):
        histoFakeEtaPt_mu[x].SetDirectory(0)
        histoFakeEtaPt_el[x].SetDirectory(0)
    fFakeFile.Close()

    lepSFPath = "data/histoLepSFEtaPt_{0}{1}.root".format(year,correctionString)
    fLepSFFile = ROOT.TFile(lepSFPath)
    histoLepSFEtaPt_mu = fLepSFFile.Get("histoLepSFEtaPt_0_{0}".format(muSelChoice))
    histoLepSFEtaPt_el = fLepSFFile.Get("histoLepSFEtaPt_1_{0}".format(elSelChoice))
    histoLepSFEtaPt_mu.SetDirectory(0)
    histoLepSFEtaPt_el.SetDirectory(0)
    fLepSFFile.Close()

    triggerSFPath = "data/histoTriggerSFEtaPt_{0}.root".format(year)
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
    fBTVEffPathFile = ROOT.TFile(BTVEffPath)
    histoBTVEffEtaPtLF = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_{0}".format(0+3*bTagSel))
    histoBTVEffEtaPtCJ = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_{0}".format(1+3*bTagSel))
    histoBTVEffEtaPtBJ = fBTVEffPathFile.Get("histoBtagEffSelEtaPt_{0}".format(2+3*bTagSel))
    histoBTVEffEtaPtLF.SetDirectory(0)
    histoBTVEffEtaPtCJ.SetDirectory(0)
    histoBTVEffEtaPtBJ.SetDirectory(0)
    fBTVEffPathFile.Close()

    try:
        if(process >= 0 and process < 1000):
            readMCSample(process,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
        elif(process >= 1000):
            readDASample(process,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
    except Exception as e:
        print("FAILED {0}".format(e))

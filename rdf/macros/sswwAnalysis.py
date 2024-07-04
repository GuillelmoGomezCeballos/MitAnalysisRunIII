import ROOT
import os, sys, getopt, json

ROOT.ROOT.EnableImplicitMT(10)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection2LVar, selectionTrigger2L, selectionElMu, selectionWeigths, makeFinalVariable
import tmva_helper_xml

correctionString = "_correction"
makeDataCards = 2

doNtuples = False
# 0 = T, 1 = M, 2 = L
bTagSel = 2
useBTaggingWeights = 1

useFR = 1
whichAna = 1

selectionJsonPath = "config/selection.json"
if(not os.path.exists(selectionJsonPath)):
    selectionJsonPath = "selection.json"

with open(selectionJsonPath) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

JSON = jsonObject['JSON']

BARRELphotons = jsonObject['BARRELphotons']
ENDCAPphotons = jsonObject['ENDCAPphotons']

VBSSEL = jsonObject['VBSSEL']
VBSQCDSEL = jsonObject['VBSQCDSEL']

muSelChoice = 8
FAKE_MU   = jsonObject['FAKE_MU']
TIGHT_MU = jsonObject['TIGHT_MU{0}'.format(muSelChoice)]
MUOWP = "Medium"

elSelChoice = 7
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

def selectionLL(df,year,PDType,isData,count):

    overallTriggers = jsonObject['triggers']
    TRIGGERMUEG = getTriggerFromJson(overallTriggers, "TRIGGERMUEG", year)
    TRIGGERDMU  = getTriggerFromJson(overallTriggers, "TRIGGERDMU", year)
    TRIGGERSMU  = getTriggerFromJson(overallTriggers, "TRIGGERSMU", year)
    TRIGGERDEL  = getTriggerFromJson(overallTriggers, "TRIGGERDEL", year)
    TRIGGERSEL  = getTriggerFromJson(overallTriggers, "TRIGGERSEL", year)

    dftag = selectionTrigger2L(df,year,PDType,JSON,isData,TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU,FAKE_EL,TIGHT_EL)

    dftag =(dftag.Filter("nLoose == 2","Only two loose leptons")
                 .Filter("nFake == 2","Two fake leptons")
                 .Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) != 0", "Sign-sign leptons")
                 .Define("eventNum", "event")
                 )

    if(useFR == 0):
        dftag = dftag.Filter("nTight == 2","Two tight leptons")

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData,count,5.0)
    dftag = selection2LVar  (dftag,year,isData)

    dftag = (dftag.Filter("ptl1 > 25 && ptl2 > 20","ptl1 > 25 && ptl2 > 20")
                  .Filter("mll > 20","mll > 20 GeV")
                  )

    return dftag

def analysis(df,count,category,weight,year,PDType,isData,whichJob,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,wsWeights,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")
    if(theCat == plotCategory("kPlotqqWW") or theCat == plotCategory("kPlotggWW") or
       theCat == plotCategory("kPlotDY") or theCat == plotCategory("kPlotTT") or
       theCat == plotCategory("kPlotTW")):
        theCat = plotCategory("kPlotWS")
    elif(theCat == plotCategory("kPlotHiggs")):
        theCat = plotCategory("kPlotVVV")

    nCat, nHisto, nhistoWS, nhistoNonPrompt = plotCategory("kPlotCategories"), 600, 4, 30
    histo = [[0 for y in range(nCat)] for x in range(nHisto)]
    histoWS = [0 for y in range(nhistoWS)]
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
    ROOT.initHisto2D(wsWeights[2],39)
    ROOT.initHisto1D(puWeights[0],0)
    ROOT.initHisto1D(puWeights[1],1)
    ROOT.initHisto1D(puWeights[2],2)
    ROOT.initHisto1D(wsWeights[0],8)
    ROOT.initHisto1D(wsWeights[1],9)

    ROOT.initJSONSFs(year)

    branchList = ROOT.vector('string')()
    for branchName in [
            "eventNum",
            "weight",
            "theCat",
            "ngood_jets",
            "vbs_mjj",
            "vbs_ptjj",
            "vbs_detajj",
            "vbs_dphijj",
            "vbs_ptj1",
            "vbs_ptj2",
            "vbs_etaj1",
            "vbs_etaj2",
            "vbs_zepvv",
            "vbs_zepmax",
            "vbs_sumHT",
            "vbs_ptvv",
            "vbs_pttot",
            "vbs_detavvj1",
            "vbs_detavvj2",
	    "vbs_ptbalance"
    ]:
        branchList.push_back(branchName)

    #ROOT.gInterpreter.ProcessLine('''
    #TMVA::Experimental::RReader model("weights_mva/bdt_BDTG_vbfinc_v0.weights.xml");
    #computeModel = TMVA::Experimental::Compute<15, float>(model);
    #''')
    #variables = ROOT.model.GetVariableNames()
    #print(variables)

    MVAweights = "weights_mva/bdt_BDTG_vbfinc_v0.weights.xml"
    tmva_helper = tmva_helper_xml.TMVAHelperXML(MVAweights)
    print(tmva_helper.variables)

    dftag = selectionLL(df,year,PDType,isData,count)

    dfbase = selectionWeigths(dftag,isData,year,PDType,weight,useFR,bTagSel,useBTaggingWeights,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,MUOWP,ELEWP,correctionString,whichAna)

    dfbase = (dfbase.Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                    .Define("kPlotWS", "{0}".format(plotCategory("kPlotWS")))
                    .Define("theCat","compute_category({0},kPlotNonPrompt,kPlotWS,nFake,nTight,nWS)".format(theCat))
                   #.Define("bdt_vbfinc", ROOT.computeModel, ROOT.model.GetVariableNames())
                    )
    dfbase = tmva_helper.run_inference(dfbase,"bdt_vbfinc")

    dfwwcat = []
    dfwwbcat = []
    dfwwvbscat = []
    dfwwbvbscat = []
    dfwwjjcat = []
    dfwwbjjcat = []

    dfwwvbscatMuonMomUp       = []
    dfwwvbscatElectronMomUp   = []
    dfwwvbscatJes00Up	      = []
    dfwwvbscatJes01Up	      = []
    dfwwvbscatJes02Up	      = []
    dfwwvbscatJes03Up	      = []
    dfwwvbscatJes04Up	      = []
    dfwwvbscatJes05Up	      = []
    dfwwvbscatJes06Up	      = []
    dfwwvbscatJes07Up	      = []
    dfwwvbscatJes08Up	      = []
    dfwwvbscatJes09Up	      = []
    dfwwvbscatJes10Up	      = []
    dfwwvbscatJes11Up	      = []
    dfwwvbscatJes12Up	      = []
    dfwwvbscatJes13Up	      = []
    dfwwvbscatJes14Up	      = []
    dfwwvbscatJes15Up	      = []
    dfwwvbscatJes16Up	      = []
    dfwwvbscatJes17Up	      = []
    dfwwvbscatJes18Up	      = []
    dfwwvbscatJes19Up	      = []
    dfwwvbscatJes20Up	      = []
    dfwwvbscatJes21Up	      = []
    dfwwvbscatJes22Up	      = []
    dfwwvbscatJes23Up	      = []
    dfwwvbscatJes24Up	      = []
    dfwwvbscatJes25Up	      = []
    dfwwvbscatJes26Up	      = []
    dfwwvbscatJes27Up	      = []
    dfwwvbscatJerUp           = []
    dfwwvbscatJERUp           = []
    dfwwvbscatJESUp           = []
    dfwwvbscatUnclusteredUp   = []

    dfwwbvbscatMuonMomUp      = []
    dfwwbvbscatElectronMomUp  = []
    dfwwbvbscatJes00Up	      = []
    dfwwbvbscatJes01Up	      = []
    dfwwbvbscatJes02Up	      = []
    dfwwbvbscatJes03Up	      = []
    dfwwbvbscatJes04Up	      = []
    dfwwbvbscatJes05Up	      = []
    dfwwbvbscatJes06Up	      = []
    dfwwbvbscatJes07Up	      = []
    dfwwbvbscatJes08Up	      = []
    dfwwbvbscatJes09Up	      = []
    dfwwbvbscatJes10Up	      = []
    dfwwbvbscatJes11Up	      = []
    dfwwbvbscatJes12Up	      = []
    dfwwbvbscatJes13Up	      = []
    dfwwbvbscatJes14Up	      = []
    dfwwbvbscatJes15Up	      = []
    dfwwbvbscatJes16Up	      = []
    dfwwbvbscatJes17Up	      = []
    dfwwbvbscatJes18Up	      = []
    dfwwbvbscatJes19Up	      = []
    dfwwbvbscatJes20Up	      = []
    dfwwbvbscatJes21Up	      = []
    dfwwbvbscatJes22Up	      = []
    dfwwbvbscatJes23Up	      = []
    dfwwbvbscatJes24Up	      = []
    dfwwbvbscatJes25Up	      = []
    dfwwbvbscatJes26Up	      = []
    dfwwbvbscatJes27Up	      = []
    dfwwbvbscatJerUp          = []
    dfwwbvbscatJERUp          = []
    dfwwbvbscatJESUp          = []
    dfwwbvbscatUnclusteredUp  = []
    for x in range(nCat):
        dfwwcat.append(dfbase.Filter("theCat=={0}".format(x), "correct category ({0})".format(x)))

        dfwwvbscatMuonMomUp    .append(dfwwcat[x])
        dfwwvbscatElectronMomUp.append(dfwwcat[x])
        dfwwvbscatJes00Up      .append(dfwwcat[x])
        dfwwvbscatJes01Up      .append(dfwwcat[x])
        dfwwvbscatJes02Up      .append(dfwwcat[x])
        dfwwvbscatJes03Up      .append(dfwwcat[x])
        dfwwvbscatJes04Up      .append(dfwwcat[x])
        dfwwvbscatJes05Up      .append(dfwwcat[x])
        dfwwvbscatJes06Up      .append(dfwwcat[x])
        dfwwvbscatJes07Up      .append(dfwwcat[x])
        dfwwvbscatJes08Up      .append(dfwwcat[x])
        dfwwvbscatJes09Up      .append(dfwwcat[x])
        dfwwvbscatJes10Up      .append(dfwwcat[x])
        dfwwvbscatJes11Up      .append(dfwwcat[x])
        dfwwvbscatJes12Up      .append(dfwwcat[x])
        dfwwvbscatJes13Up      .append(dfwwcat[x])
        dfwwvbscatJes14Up      .append(dfwwcat[x])
        dfwwvbscatJes15Up      .append(dfwwcat[x])
        dfwwvbscatJes16Up      .append(dfwwcat[x])
        dfwwvbscatJes17Up      .append(dfwwcat[x])
        dfwwvbscatJes18Up      .append(dfwwcat[x])
        dfwwvbscatJes19Up      .append(dfwwcat[x])
        dfwwvbscatJes20Up      .append(dfwwcat[x])
        dfwwvbscatJes21Up      .append(dfwwcat[x])
        dfwwvbscatJes22Up      .append(dfwwcat[x])
        dfwwvbscatJes23Up      .append(dfwwcat[x])
        dfwwvbscatJes24Up      .append(dfwwcat[x])
        dfwwvbscatJes25Up      .append(dfwwcat[x])
        dfwwvbscatJes26Up      .append(dfwwcat[x])
        dfwwvbscatJes27Up      .append(dfwwcat[x])
        dfwwvbscatJerUp        .append(dfwwcat[x])
        dfwwvbscatJERUp        .append(dfwwcat[x])
        dfwwvbscatJESUp        .append(dfwwcat[x])
        dfwwvbscatUnclusteredUp.append(dfwwcat[x])

        dfwwbvbscatMuonMomUp    .append(dfwwcat[x])
        dfwwbvbscatElectronMomUp.append(dfwwcat[x])
        dfwwbvbscatJes00Up      .append(dfwwcat[x])
        dfwwbvbscatJes01Up      .append(dfwwcat[x])
        dfwwbvbscatJes02Up      .append(dfwwcat[x])
        dfwwbvbscatJes03Up      .append(dfwwcat[x])
        dfwwbvbscatJes04Up      .append(dfwwcat[x])
        dfwwbvbscatJes05Up      .append(dfwwcat[x])
        dfwwbvbscatJes06Up      .append(dfwwcat[x])
        dfwwbvbscatJes07Up      .append(dfwwcat[x])
        dfwwbvbscatJes08Up      .append(dfwwcat[x])
        dfwwbvbscatJes09Up      .append(dfwwcat[x])
        dfwwbvbscatJes10Up      .append(dfwwcat[x])
        dfwwbvbscatJes11Up      .append(dfwwcat[x])
        dfwwbvbscatJes12Up      .append(dfwwcat[x])
        dfwwbvbscatJes13Up      .append(dfwwcat[x])
        dfwwbvbscatJes14Up      .append(dfwwcat[x])
        dfwwbvbscatJes15Up      .append(dfwwcat[x])
        dfwwbvbscatJes16Up      .append(dfwwcat[x])
        dfwwbvbscatJes17Up      .append(dfwwcat[x])
        dfwwbvbscatJes18Up      .append(dfwwcat[x])
        dfwwbvbscatJes19Up      .append(dfwwcat[x])
        dfwwbvbscatJes20Up      .append(dfwwcat[x])
        dfwwbvbscatJes21Up      .append(dfwwcat[x])
        dfwwbvbscatJes22Up      .append(dfwwcat[x])
        dfwwbvbscatJes23Up      .append(dfwwcat[x])
        dfwwbvbscatJes24Up      .append(dfwwcat[x])
        dfwwbvbscatJes25Up      .append(dfwwcat[x])
        dfwwbvbscatJes26Up      .append(dfwwcat[x])
        dfwwbvbscatJes27Up      .append(dfwwcat[x])
        dfwwbvbscatJerUp        .append(dfwwcat[x])
        dfwwbvbscatJERUp        .append(dfwwcat[x])
        dfwwbvbscatJESUp        .append(dfwwcat[x])
        dfwwbvbscatUnclusteredUp.append(dfwwcat[x])

        dfwwvbscatMuonMomUp     [x] = dfwwvbscatMuonMomUp     [x].Filter("mllMuonMomUp     > 20 && ptl1MuonMomUp     > 25 && ptl2MuonMomUp     > 20 && (DiLepton_flavor != 2 || abs(mllMuonMomUp     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets        >= 2 && vbs_mjj        > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt	            > 30")
        dfwwvbscatElectronMomUp [x] = dfwwvbscatElectronMomUp [x].Filter("mllElectronMomUp > 20 && ptl1ElectronMomUp > 25 && ptl2ElectronMomUp > 20 && (DiLepton_flavor != 2 || abs(mllElectronMomUp -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets        >= 2 && vbs_mjj        > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt	            > 30")
        dfwwvbscatJes00Up	[x] = dfwwvbscatJes00Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes00Up >= 2 && vbs_mjjJes00Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes01Up	[x] = dfwwvbscatJes01Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes01Up >= 2 && vbs_mjjJes01Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes02Up	[x] = dfwwvbscatJes02Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes02Up >= 2 && vbs_mjjJes02Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes03Up	[x] = dfwwvbscatJes03Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes03Up >= 2 && vbs_mjjJes03Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes04Up	[x] = dfwwvbscatJes04Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes04Up >= 2 && vbs_mjjJes04Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes05Up	[x] = dfwwvbscatJes05Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes05Up >= 2 && vbs_mjjJes05Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes06Up	[x] = dfwwvbscatJes06Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes06Up >= 2 && vbs_mjjJes06Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes07Up	[x] = dfwwvbscatJes07Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes07Up >= 2 && vbs_mjjJes07Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes08Up	[x] = dfwwvbscatJes08Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes08Up >= 2 && vbs_mjjJes08Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes09Up	[x] = dfwwvbscatJes09Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes09Up >= 2 && vbs_mjjJes09Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes10Up	[x] = dfwwvbscatJes10Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes10Up >= 2 && vbs_mjjJes10Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes11Up	[x] = dfwwvbscatJes11Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes11Up >= 2 && vbs_mjjJes11Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes12Up	[x] = dfwwvbscatJes12Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes12Up >= 2 && vbs_mjjJes12Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes13Up	[x] = dfwwvbscatJes13Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes13Up >= 2 && vbs_mjjJes13Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes14Up	[x] = dfwwvbscatJes14Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes14Up >= 2 && vbs_mjjJes14Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes15Up	[x] = dfwwvbscatJes15Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes15Up >= 2 && vbs_mjjJes15Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes16Up	[x] = dfwwvbscatJes16Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes16Up >= 2 && vbs_mjjJes16Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes17Up	[x] = dfwwvbscatJes17Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes17Up >= 2 && vbs_mjjJes17Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes18Up	[x] = dfwwvbscatJes18Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes18Up >= 2 && vbs_mjjJes18Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes19Up	[x] = dfwwvbscatJes19Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes19Up >= 2 && vbs_mjjJes19Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes20Up	[x] = dfwwvbscatJes20Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes20Up >= 2 && vbs_mjjJes20Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes21Up	[x] = dfwwvbscatJes21Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes21Up >= 2 && vbs_mjjJes21Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes22Up	[x] = dfwwvbscatJes22Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes22Up >= 2 && vbs_mjjJes22Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes23Up	[x] = dfwwvbscatJes23Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes23Up >= 2 && vbs_mjjJes23Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes24Up	[x] = dfwwvbscatJes24Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes24Up >= 2 && vbs_mjjJes24Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes25Up	[x] = dfwwvbscatJes25Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes25Up >= 2 && vbs_mjjJes25Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes26Up	[x] = dfwwvbscatJes26Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes26Up >= 2 && vbs_mjjJes26Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJes27Up	[x] = dfwwvbscatJes27Up       [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes27Up >= 2 && vbs_mjjJes27Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJerUp  	[x] = dfwwvbscatJerUp	      [x].Filter("mll		   > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJerUp   >= 2 && vbs_mjjJerUp	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt              > 30")
        dfwwvbscatJERUp         [x] = dfwwvbscatJERUp	      [x].Filter("mll              > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets        >= 2 && vbs_mjj        > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptJERUp	    > 30")
        dfwwvbscatJESUp         [x] = dfwwvbscatJESUp	      [x].Filter("mll              > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets        >= 2 && vbs_mjj        > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptJESUp	    > 30")
        dfwwvbscatUnclusteredUp [x] = dfwwvbscatUnclusteredUp [x].Filter("mll              > 20 && ptl1 	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll 	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets        >= 2 && vbs_mjj        > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptUnclusteredUp > 30")

        dfwwbvbscatMuonMomUp    [x] = dfwwbvbscatMuonMomUp    [x].Filter("mllMuonMomUp     > 20 && ptl1MuonMomUp     > 25 && ptl2MuonMomUp     > 20 && (DiLepton_flavor != 2 || abs(mllMuonMomUp     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets	 >= 2 && vbs_mjj	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatElectronMomUp[x] = dfwwbvbscatElectronMomUp[x].Filter("mllElectronMomUp > 20 && ptl1ElectronMomUp > 25 && ptl2ElectronMomUp > 20 && (DiLepton_flavor != 2 || abs(mllElectronMomUp -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets	 >= 2 && vbs_mjj	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes00Up	[x] = dfwwbvbscatJes00Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes00Up >= 2 && vbs_mjjJes00Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes01Up	[x] = dfwwbvbscatJes01Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes01Up >= 2 && vbs_mjjJes01Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes02Up	[x] = dfwwbvbscatJes02Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes02Up >= 2 && vbs_mjjJes02Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes03Up	[x] = dfwwbvbscatJes03Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes03Up >= 2 && vbs_mjjJes03Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes04Up	[x] = dfwwbvbscatJes04Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes04Up >= 2 && vbs_mjjJes04Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes05Up	[x] = dfwwbvbscatJes05Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes05Up >= 2 && vbs_mjjJes05Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes06Up	[x] = dfwwbvbscatJes06Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes06Up >= 2 && vbs_mjjJes06Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes07Up	[x] = dfwwbvbscatJes07Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes07Up >= 2 && vbs_mjjJes07Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes08Up	[x] = dfwwbvbscatJes08Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes08Up >= 2 && vbs_mjjJes08Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes09Up	[x] = dfwwbvbscatJes09Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes09Up >= 2 && vbs_mjjJes09Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes10Up	[x] = dfwwbvbscatJes10Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes10Up >= 2 && vbs_mjjJes10Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes11Up	[x] = dfwwbvbscatJes11Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes11Up >= 2 && vbs_mjjJes11Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes12Up	[x] = dfwwbvbscatJes12Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes12Up >= 2 && vbs_mjjJes12Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes13Up	[x] = dfwwbvbscatJes13Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes13Up >= 2 && vbs_mjjJes13Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes14Up	[x] = dfwwbvbscatJes14Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes14Up >= 2 && vbs_mjjJes14Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes15Up	[x] = dfwwbvbscatJes15Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes15Up >= 2 && vbs_mjjJes15Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes16Up	[x] = dfwwbvbscatJes16Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes16Up >= 2 && vbs_mjjJes16Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes17Up	[x] = dfwwbvbscatJes17Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes17Up >= 2 && vbs_mjjJes17Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes18Up	[x] = dfwwbvbscatJes18Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes18Up >= 2 && vbs_mjjJes18Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes19Up	[x] = dfwwbvbscatJes19Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes19Up >= 2 && vbs_mjjJes19Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes20Up	[x] = dfwwbvbscatJes20Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes20Up >= 2 && vbs_mjjJes20Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes21Up	[x] = dfwwbvbscatJes21Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes21Up >= 2 && vbs_mjjJes21Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes22Up	[x] = dfwwbvbscatJes22Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes22Up >= 2 && vbs_mjjJes22Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes23Up	[x] = dfwwbvbscatJes23Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes23Up >= 2 && vbs_mjjJes23Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes24Up	[x] = dfwwbvbscatJes24Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes24Up >= 2 && vbs_mjjJes24Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes25Up	[x] = dfwwbvbscatJes25Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes25Up >= 2 && vbs_mjjJes25Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes26Up	[x] = dfwwbvbscatJes26Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes26Up >= 2 && vbs_mjjJes26Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJes27Up	[x] = dfwwbvbscatJes27Up      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes27Up >= 2 && vbs_mjjJes27Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJerUp  	[x] = dfwwbvbscatJerUp	      [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJerUp   >= 2 && vbs_mjjJerUp	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwwbvbscatJERUp        [x] = dfwwbvbscatJERUp        [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets	 >= 2 && vbs_mjj	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptJERUp	    > 30")
        dfwwbvbscatJESUp        [x] = dfwwbvbscatJESUp        [x].Filter("mll		   > 20 && ptl1  	     > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets	 >= 2 && vbs_mjj	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptJESUp	    > 30")
        dfwwbvbscatUnclusteredUp[x] = dfwwbvbscatUnclusteredUp[x].Filter("mll  	           > 20 && ptl1	             > 25 && ptl2	       > 20 && (DiLepton_flavor != 2 || abs(mll     	     -91.1876) > 15) && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets	 >= 2 && vbs_mjj	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptUnclusteredUp > 30")

        histo[ 0][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x),40, 20, 220), "mll","weightNoBTag")
        dfwwcat[x] = dfwwcat[x].Filter("DiLepton_flavor != 2 || abs(mll-91.1876) > 15","Z veto")

        dfwwbcat.append(dfwwcat[x].Filter("nbtag_goodbtag_Jet_bjet > 0","at least one good b-jets"))

        histo[ 1][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x), 5,-0.5 ,4.5),     "nbtag_goodbtag_Jet_bjet","weight")
        dfwwcat[x] = dfwwcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0","no good b-jets")

        histo[ 2][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x), 4,-0.5, 3.5), "ltype","weight")
        histo[ 3][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x), 4,-0.5, 3.5), "ltype","weight")
        histo[ 4][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x), 6,-0.5, 5.5), "ngood_jets","weight")
        histo[ 5][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x), 6,-0.5, 5.5), "ngood_jets","weight")

        dfwwcat[x]  = dfwwcat[x] .Filter("nvbs_jets >= 2 && vbs_mjj > 200", "At least two VBS jets")
        dfwwbcat[x] = dfwwbcat[x].Filter("nvbs_jets >= 2 && vbs_mjj > 200", "At least two VBS jets")
        histo[ 6][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x), 4,-0.5, 3.5), "ltype","weight")
        histo[ 7][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x), 4,-0.5, 3.5), "ltype","weight")
        histo[ 8][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[ 9][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[10][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 20,200,2200), "vbs_mjj","weight")
        histo[11][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 20,200,2200), "vbs_mjj","weight")
        histo[12][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 19,0.0,9.5), "vbs_detajj","weight")
        histo[13][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 19,0.0,9.5), "vbs_detajj","weight")
        histo[14][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 20,0,2), "vbs_zepvv","weight")
        histo[15][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 20,0,2), "vbs_zepvv","weight")

        for ltype in range(4):
            histo[60+ltype][x] = dfwwcat[x] .Filter("ltype == {0}".format(ltype)).Histo1D(("histo_{0}_{1}".format(60+ltype,x), "histo_{0}_{1}".format(60+ltype,x),20, 25, 225), "ptl1","weight")
            histo[64+ltype][x] = dfwwbcat[x].Filter("ltype == {0}".format(ltype)).Histo1D(("histo_{0}_{1}".format(64+ltype,x), "histo_{0}_{1}".format(64+ltype,x),20, 25, 225), "ptl1","weight")
            histo[68+ltype][x] = dfwwcat[x] .Filter("ltype == {0}".format(ltype)).Histo1D(("histo_{0}_{1}".format(68+ltype,x), "histo_{0}_{1}".format(68+ltype,x),20, 20, 120), "ptl2","weight")
            histo[72+ltype][x] = dfwwbcat[x].Filter("ltype == {0}".format(ltype)).Histo1D(("histo_{0}_{1}".format(72+ltype,x), "histo_{0}_{1}".format(72+ltype,x),20, 20, 120), "ptl2","weight")
            histo[76+ltype][x] = dfwwcat[x] .Filter("ltype == {0}".format(ltype)).Histo1D(("histo_{0}_{1}".format(76+ltype,x), "histo_{0}_{1}".format(76+ltype,x),25, 0, 2.5), "etal1","weight")
            histo[80+ltype][x] = dfwwbcat[x].Filter("ltype == {0}".format(ltype)).Histo1D(("histo_{0}_{1}".format(80+ltype,x), "histo_{0}_{1}".format(80+ltype,x),25, 0, 2.5), "etal1","weight")
            histo[84+ltype][x] = dfwwcat[x] .Filter("ltype == {0}".format(ltype)).Histo1D(("histo_{0}_{1}".format(84+ltype,x), "histo_{0}_{1}".format(84+ltype,x),25, 0, 2.5), "etal2","weight")
            histo[88+ltype][x] = dfwwbcat[x].Filter("ltype == {0}".format(ltype)).Histo1D(("histo_{0}_{1}".format(88+ltype,x), "histo_{0}_{1}".format(88+ltype,x),25, 0, 2.5), "etal2","weight")

        dfwwvbscat .append(dfwwcat[x] .Filter(VBSSEL, "VBS selection"))
        dfwwbvbscat.append(dfwwbcat[x].Filter(VBSSEL, "VBS selection"))
        histo[16][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x),25,  0, 250), "thePuppiMET_pt","weight")
        histo[17][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(17,x), "histo_{0}_{1}".format(17,x),25,  0, 250), "thePuppiMET_pt","weight")

        dfwwvbscat[x]  = dfwwvbscat[x] .Filter("thePuppiMET_pt > 30", "thePuppiMET_pt > 30")
        dfwwbvbscat[x] = dfwwbvbscat[x].Filter("thePuppiMET_pt > 30", "thePuppiMET_pt > 30")
        histo[18][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(18,x), "histo_{0}_{1}".format(18,x), 4,-0.5, 3.5), "ltype","weight")
        histo[19][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(19,x), "histo_{0}_{1}".format(19,x), 4,-0.5, 3.5), "ltype","weight")
        histo[20][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(20,x), "histo_{0}_{1}".format(20,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[21][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(21,x), "histo_{0}_{1}".format(21,x), 4, 1.5, 5.5), "ngood_jets","weight")

        histo[22][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(22,x), "histo_{0}_{1}".format(22,x), 10,500,2500), "vbs_mjj","weight")
        histo[23][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(23,x), "histo_{0}_{1}".format(23,x), 10,500,2500), "vbs_mjj","weight")
        histo[24][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(24,x), "histo_{0}_{1}".format(24,x), 14,2.5,9.5), "vbs_detajj","weight")
        histo[25][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(25,x), "histo_{0}_{1}".format(25,x), 14,2.5,9.5), "vbs_detajj","weight")
        histo[26][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(26,x), "histo_{0}_{1}".format(26,x), 10,0,3.1416), "vbs_dphijj","weight")
        histo[27][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(27,x), "histo_{0}_{1}".format(27,x), 10,0,3.1416), "vbs_dphijj","weight")
        histo[28][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(28,x), "histo_{0}_{1}".format(28,x), 10,0,1), "vbs_zepvv","weight")
        histo[29][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(29,x), "histo_{0}_{1}".format(29,x), 10,0,1), "vbs_zepvv","weight")
        histo[30][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(30,x), "histo_{0}_{1}".format(30,x), 20,-1,1), "bdt_vbfinc","weight")
        histo[31][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(31,x), "histo_{0}_{1}".format(31,x), 20,-1,1), "bdt_vbfinc","weight")
        histo[32][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(32,x), "histo_{0}_{1}".format(32,x),25, 50, 300), "vbs_ptj1","weight")
        histo[33][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(33,x), "histo_{0}_{1}".format(33,x),25, 50, 300), "vbs_ptj1","weight")
        histo[34][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(34,x), "histo_{0}_{1}".format(34,x),25, 50, 300), "vbs_ptj2","weight")
        histo[35][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(35,x), "histo_{0}_{1}".format(35,x),25, 50, 300), "vbs_ptj2","weight")
        histo[36][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(36,x), "histo_{0}_{1}".format(36,x),25, 0, 5), "vbs_etaj1","weight")
        histo[37][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(37,x), "histo_{0}_{1}".format(37,x),25, 0, 5), "vbs_etaj1","weight")
        histo[38][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(38,x), "histo_{0}_{1}".format(38,x),25, 0, 5), "vbs_etaj2","weight")
        histo[39][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(39,x), "histo_{0}_{1}".format(39,x),25, 0, 5), "vbs_etaj2","weight")

        dfwwjjcat .append(dfwwcat[x] .Filter("thePuppiMET_pt > 30", "thePuppiMET_pt > 30").Filter(VBSQCDSEL, "dijet non-vbf selection"))
        dfwwbjjcat.append(dfwwbcat[x].Filter("thePuppiMET_pt > 30", "thePuppiMET_pt > 30").Filter(VBSQCDSEL, "dijet non-vbf selection"))
        histo[40][x] = dfwwjjcat[x] .Histo1D(("histo_{0}_{1}".format(40,x), "histo_{0}_{1}".format(40,x), 14,0.0,7), "vbs_detajj","weight")
        histo[41][x] = dfwwbjjcat[x].Histo1D(("histo_{0}_{1}".format(41,x), "histo_{0}_{1}".format(41,x), 14,0.0,7), "vbs_detajj","weight")
        histo[42][x] = dfwwjjcat[x] .Histo1D(("histo_{0}_{1}".format(42,x), "histo_{0}_{1}".format(42,x), 4,-0.5, 3.5), "ltype","weight")
        histo[43][x] = dfwwbjjcat[x].Histo1D(("histo_{0}_{1}".format(43,x), "histo_{0}_{1}".format(43,x), 4,-0.5, 3.5), "ltype","weight")
        histo[44][x] = dfwwjjcat[x] .Histo1D(("histo_{0}_{1}".format(44,x), "histo_{0}_{1}".format(44,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[45][x] = dfwwbjjcat[x].Histo1D(("histo_{0}_{1}".format(45,x), "histo_{0}_{1}".format(45,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[46][x] = dfwwjjcat[x] .Histo1D(("histo_{0}_{1}".format(46,x), "histo_{0}_{1}".format(46,x),25, 50, 300), "vbs_ptj1","weight")
        histo[47][x] = dfwwbjjcat[x].Histo1D(("histo_{0}_{1}".format(47,x), "histo_{0}_{1}".format(47,x),25, 50, 300), "vbs_ptj1","weight")
        histo[48][x] = dfwwjjcat[x] .Histo1D(("histo_{0}_{1}".format(48,x), "histo_{0}_{1}".format(48,x),25, 50, 300), "vbs_ptj2","weight")
        histo[49][x] = dfwwbjjcat[x].Histo1D(("histo_{0}_{1}".format(49,x), "histo_{0}_{1}".format(49,x),25, 50, 300), "vbs_ptj2","weight")
        histo[50][x] = dfwwjjcat[x] .Histo1D(("histo_{0}_{1}".format(50,x), "histo_{0}_{1}".format(50,x),25, 0, 5), "vbs_etaj1","weight")
        histo[51][x] = dfwwbjjcat[x].Histo1D(("histo_{0}_{1}".format(51,x), "histo_{0}_{1}".format(51,x),25, 0, 5), "vbs_etaj1","weight")
        histo[52][x] = dfwwjjcat[x] .Histo1D(("histo_{0}_{1}".format(52,x), "histo_{0}_{1}".format(52,x),25, 0, 5), "vbs_etaj2","weight")
        histo[53][x] = dfwwbjjcat[x].Histo1D(("histo_{0}_{1}".format(53,x), "histo_{0}_{1}".format(53,x),25, 0, 5), "vbs_etaj2","weight")

        if(doNtuples == True and x == theCat):
            outputFile = "ntupleSSWWAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob)
            dfwwvbscat[x].Snapshot("events", outputFile, branchList)

        histo[90][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(90,x), "histo_{0}_{1}".format(90,x), 8,500,2500), "vbs_mjj","weight")
        histo[91][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(91,x), "histo_{0}_{1}".format(91,x), 8,500,2500), "vbs_mjj","weight0")
        histo[92][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(92,x), "histo_{0}_{1}".format(92,x), 8,500,2500), "vbs_mjj","weight1")
        histo[93][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(93,x), "histo_{0}_{1}".format(93,x), 8,500,2500), "vbs_mjj","weight2")
        histo[94][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(94,x), "histo_{0}_{1}".format(94,x), 8,500,2500), "vbs_mjj","weight3")
        histo[95][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(95,x), "histo_{0}_{1}".format(95,x), 8,500,2500), "vbs_mjj","weight4")
        histo[96][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(96,x), "histo_{0}_{1}".format(96,x), 8,500,2500), "vbs_mjj","weight5")
        histo[97][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(97,x), "histo_{0}_{1}".format(97,x), 8,500,2500), "vbs_mjj","weight6")
        histo[98][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(98,x), "histo_{0}_{1}".format(98,x), 8,500,2500), "vbs_mjj","weightWSUnc0")
        histo[99][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format(99,x), "histo_{0}_{1}".format(99,x), 8,500,2500), "vbs_mjj","weightWSUnc1")

        startF = 200
        BinXF = 8
        minXF = 500
        maxXF = 2500
        if(makeDataCards == 1):
            startF = 200
            BinXF = 8
            minXF = 500
            maxXF = 2500
            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwwvbscat[x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwwvbscatMuonMomUp    [x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwwvbscatElectronMomUp[x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwwvbscatJes00Up	   [x],"vbs_mjjJes00Up"  ,theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwwvbscatJes01Up	   [x],"vbs_mjjJes01Up"  ,theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwwvbscatJes02Up	   [x],"vbs_mjjJes02Up"  ,theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwwvbscatJes03Up	   [x],"vbs_mjjJes03Up"  ,theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwwvbscatJes04Up	   [x],"vbs_mjjJes04Up"  ,theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwwvbscatJes05Up	   [x],"vbs_mjjJes05Up"  ,theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwwvbscatJes06Up	   [x],"vbs_mjjJes06Up"  ,theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwwvbscatJes07Up	   [x],"vbs_mjjJes07Up"  ,theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwwvbscatJes08Up	   [x],"vbs_mjjJes08Up"  ,theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwwvbscatJes09Up	   [x],"vbs_mjjJes09Up"  ,theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwwvbscatJes10Up	   [x],"vbs_mjjJes10Up"  ,theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwwvbscatJes11Up	   [x],"vbs_mjjJes11Up"  ,theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwwvbscatJes12Up	   [x],"vbs_mjjJes12Up"  ,theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwwvbscatJes13Up	   [x],"vbs_mjjJes13Up"  ,theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwwvbscatJes14Up	   [x],"vbs_mjjJes14Up"  ,theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwwvbscatJes15Up	   [x],"vbs_mjjJes15Up"  ,theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwwvbscatJes16Up	   [x],"vbs_mjjJes16Up"  ,theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwwvbscatJes17Up	   [x],"vbs_mjjJes17Up"  ,theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwwvbscatJes18Up	   [x],"vbs_mjjJes18Up"  ,theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwwvbscatJes19Up	   [x],"vbs_mjjJes19Up"  ,theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwwvbscatJes20Up	   [x],"vbs_mjjJes20Up"  ,theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwwvbscatJes21Up	   [x],"vbs_mjjJes21Up"  ,theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwwvbscatJes22Up	   [x],"vbs_mjjJes22Up"  ,theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwwvbscatJes23Up	   [x],"vbs_mjjJes23Up"  ,theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwwvbscatJes24Up	   [x],"vbs_mjjJes24Up"  ,theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwwvbscatJes25Up	   [x],"vbs_mjjJes25Up"  ,theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwwvbscatJes26Up	   [x],"vbs_mjjJes26Up"  ,theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwwvbscatJes27Up	   [x],"vbs_mjjJes27Up"  ,theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwwvbscatJerUp  	   [x],"vbs_mjjJerUp"	 ,theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwwvbscatJERUp	   [x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwwvbscatJESUp	   [x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwwvbscatUnclusteredUp[x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotWS")):
                startWS = 0
                histoWS[0+startWS] = dfwwvbscat[x].Histo1D(("histoWS_{0}".format(0+startWS), "histoWS_{0}".format(0+startWS), BinXF,minXF,maxXF), "vbs_mjj","weightWSUnc0")
                histoWS[1+startWS] = dfwwvbscat[x].Histo1D(("histoWS_{0}".format(1+startWS), "histoWS_{0}".format(1+startWS), BinXF,minXF,maxXF), "vbs_mjj","weightWSUnc1")
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 0
                histoNonPrompt[0+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAlte2")

            startF = 400
            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwwbvbscat[x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwwbvbscatMuonMomUp    [x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwwbvbscatElectronMomUp[x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwwbvbscatJes00Up	    [x],"vbs_mjjJes00Up"  ,theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwwbvbscatJes01Up	    [x],"vbs_mjjJes01Up"  ,theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwwbvbscatJes02Up	    [x],"vbs_mjjJes02Up"  ,theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwwbvbscatJes03Up	    [x],"vbs_mjjJes03Up"  ,theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwwbvbscatJes04Up	    [x],"vbs_mjjJes04Up"  ,theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwwbvbscatJes05Up	    [x],"vbs_mjjJes05Up"  ,theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwwbvbscatJes06Up	    [x],"vbs_mjjJes06Up"  ,theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwwbvbscatJes07Up	    [x],"vbs_mjjJes07Up"  ,theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwwbvbscatJes08Up	    [x],"vbs_mjjJes08Up"  ,theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwwbvbscatJes09Up	    [x],"vbs_mjjJes09Up"  ,theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwwbvbscatJes10Up	    [x],"vbs_mjjJes10Up"  ,theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwwbvbscatJes11Up	    [x],"vbs_mjjJes11Up"  ,theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwwbvbscatJes12Up	    [x],"vbs_mjjJes12Up"  ,theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwwbvbscatJes13Up	    [x],"vbs_mjjJes13Up"  ,theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwwbvbscatJes14Up	    [x],"vbs_mjjJes14Up"  ,theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwwbvbscatJes15Up	    [x],"vbs_mjjJes15Up"  ,theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwwbvbscatJes16Up	    [x],"vbs_mjjJes16Up"  ,theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwwbvbscatJes17Up	    [x],"vbs_mjjJes17Up"  ,theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwwbvbscatJes18Up	    [x],"vbs_mjjJes18Up"  ,theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwwbvbscatJes19Up	    [x],"vbs_mjjJes19Up"  ,theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwwbvbscatJes20Up	    [x],"vbs_mjjJes20Up"  ,theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwwbvbscatJes21Up	    [x],"vbs_mjjJes21Up"  ,theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwwbvbscatJes22Up	    [x],"vbs_mjjJes22Up"  ,theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwwbvbscatJes23Up	    [x],"vbs_mjjJes23Up"  ,theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwwbvbscatJes24Up	    [x],"vbs_mjjJes24Up"  ,theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwwbvbscatJes25Up	    [x],"vbs_mjjJes25Up"  ,theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwwbvbscatJes26Up	    [x],"vbs_mjjJes26Up"  ,theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwwbvbscatJes27Up	    [x],"vbs_mjjJes27Up"  ,theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwwbvbscatJerUp	    [x],"vbs_mjjJerUp"    ,theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwwbvbscatJERUp	    [x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwwbvbscatJESUp	    [x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwwbvbscatUnclusteredUp[x],"vbs_mjj",theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotWS")):
                startWS = 2
                histoWS[0+startWS] = dfwwbvbscat[x].Histo1D(("histoWS_{0}".format(0+startWS), "histoWS_{0}".format(0+startWS), BinXF,minXF,maxXF), "vbs_mjj","weightWSUnc0")
                histoWS[1+startWS] = dfwwbvbscat[x].Histo1D(("histoWS_{0}".format(1+startWS), "histoWS_{0}".format(1+startWS), BinXF,minXF,maxXF), "vbs_mjj","weightWSUnc1")
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 6
                histoNonPrompt[0+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "vbs_mjj","weightFakeAlte2")

        elif(makeDataCards == 2):
            startF = 200
            BinXF = 16
            minXF = -0.5
            maxXF = 15.5

            # Making final variable
            dfwwvbscat             [x] = dfwwvbscat             [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,0)")
            dfwwvbscatMuonMomUp    [x] = dfwwvbscatMuonMomUp    [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mllMuonMomUp,0)")
            dfwwvbscatElectronMomUp[x] = dfwwvbscatElectronMomUp[x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mllElectronMomUp,0)")
            dfwwvbscatJes00Up      [x] = dfwwvbscatJes00Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes00Up,vbs_detajj,mll,0)")
            dfwwvbscatJes01Up      [x] = dfwwvbscatJes01Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes01Up,vbs_detajj,mll,0)")
            dfwwvbscatJes02Up      [x] = dfwwvbscatJes02Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes02Up,vbs_detajj,mll,0)")
            dfwwvbscatJes03Up      [x] = dfwwvbscatJes03Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes03Up,vbs_detajj,mll,0)")
            dfwwvbscatJes04Up      [x] = dfwwvbscatJes04Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes04Up,vbs_detajj,mll,0)")
            dfwwvbscatJes05Up      [x] = dfwwvbscatJes05Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes05Up,vbs_detajj,mll,0)")
            dfwwvbscatJes06Up      [x] = dfwwvbscatJes06Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes06Up,vbs_detajj,mll,0)")
            dfwwvbscatJes07Up      [x] = dfwwvbscatJes07Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes07Up,vbs_detajj,mll,0)")
            dfwwvbscatJes08Up      [x] = dfwwvbscatJes08Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes08Up,vbs_detajj,mll,0)")
            dfwwvbscatJes09Up      [x] = dfwwvbscatJes09Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes09Up,vbs_detajj,mll,0)")
            dfwwvbscatJes10Up      [x] = dfwwvbscatJes10Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes10Up,vbs_detajj,mll,0)")
            dfwwvbscatJes11Up      [x] = dfwwvbscatJes11Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes11Up,vbs_detajj,mll,0)")
            dfwwvbscatJes12Up      [x] = dfwwvbscatJes12Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes12Up,vbs_detajj,mll,0)")
            dfwwvbscatJes13Up      [x] = dfwwvbscatJes13Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes13Up,vbs_detajj,mll,0)")
            dfwwvbscatJes14Up      [x] = dfwwvbscatJes14Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes14Up,vbs_detajj,mll,0)")
            dfwwvbscatJes15Up      [x] = dfwwvbscatJes15Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes15Up,vbs_detajj,mll,0)")
            dfwwvbscatJes16Up      [x] = dfwwvbscatJes16Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes16Up,vbs_detajj,mll,0)")
            dfwwvbscatJes17Up      [x] = dfwwvbscatJes17Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes17Up,vbs_detajj,mll,0)")
            dfwwvbscatJes18Up      [x] = dfwwvbscatJes18Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes18Up,vbs_detajj,mll,0)")
            dfwwvbscatJes19Up      [x] = dfwwvbscatJes19Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes19Up,vbs_detajj,mll,0)")
            dfwwvbscatJes20Up      [x] = dfwwvbscatJes20Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes20Up,vbs_detajj,mll,0)")
            dfwwvbscatJes21Up      [x] = dfwwvbscatJes21Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes21Up,vbs_detajj,mll,0)")
            dfwwvbscatJes22Up      [x] = dfwwvbscatJes22Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes22Up,vbs_detajj,mll,0)")
            dfwwvbscatJes23Up      [x] = dfwwvbscatJes23Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes23Up,vbs_detajj,mll,0)")
            dfwwvbscatJes24Up      [x] = dfwwvbscatJes24Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes24Up,vbs_detajj,mll,0)")
            dfwwvbscatJes25Up      [x] = dfwwvbscatJes25Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes25Up,vbs_detajj,mll,0)")
            dfwwvbscatJes26Up      [x] = dfwwvbscatJes26Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes26Up,vbs_detajj,mll,0)")
            dfwwvbscatJes27Up      [x] = dfwwvbscatJes27Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes27Up,vbs_detajj,mll,0)")
            dfwwvbscatJerUp        [x] = dfwwvbscatJerUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJerUp,vbs_detajj,mll,0)")
            dfwwvbscatJERUp        [x] = dfwwvbscatJERUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,0)")
            dfwwvbscatJESUp        [x] = dfwwvbscatJESUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,0)")
            dfwwvbscatUnclusteredUp[x] = dfwwvbscatUnclusteredUp[x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,0)")

            dfwwbvbscat             [x] = dfwwbvbscat             [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,0)")
            dfwwbvbscatMuonMomUp    [x] = dfwwbvbscatMuonMomUp    [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mllMuonMomUp,0)")
            dfwwbvbscatElectronMomUp[x] = dfwwbvbscatElectronMomUp[x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mllElectronMomUp,0)")
            dfwwbvbscatJes00Up      [x] = dfwwbvbscatJes00Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes00Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes01Up      [x] = dfwwbvbscatJes01Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes01Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes02Up      [x] = dfwwbvbscatJes02Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes02Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes03Up      [x] = dfwwbvbscatJes03Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes03Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes04Up      [x] = dfwwbvbscatJes04Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes04Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes05Up      [x] = dfwwbvbscatJes05Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes05Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes06Up      [x] = dfwwbvbscatJes06Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes06Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes07Up      [x] = dfwwbvbscatJes07Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes07Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes08Up      [x] = dfwwbvbscatJes08Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes08Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes09Up      [x] = dfwwbvbscatJes09Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes09Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes10Up      [x] = dfwwbvbscatJes10Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes10Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes11Up      [x] = dfwwbvbscatJes11Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes11Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes12Up      [x] = dfwwbvbscatJes12Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes12Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes13Up      [x] = dfwwbvbscatJes13Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes13Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes14Up      [x] = dfwwbvbscatJes14Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes14Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes15Up      [x] = dfwwbvbscatJes15Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes15Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes16Up      [x] = dfwwbvbscatJes16Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes16Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes17Up      [x] = dfwwbvbscatJes17Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes17Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes18Up      [x] = dfwwbvbscatJes18Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes18Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes19Up      [x] = dfwwbvbscatJes19Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes19Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes20Up      [x] = dfwwbvbscatJes20Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes20Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes21Up      [x] = dfwwbvbscatJes21Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes21Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes22Up      [x] = dfwwbvbscatJes22Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes22Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes23Up      [x] = dfwwbvbscatJes23Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes23Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes24Up      [x] = dfwwbvbscatJes24Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes24Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes25Up      [x] = dfwwbvbscatJes25Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes25Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes26Up      [x] = dfwwbvbscatJes26Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes26Up,vbs_detajj,mll,0)")
            dfwwbvbscatJes27Up      [x] = dfwwbvbscatJes27Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes27Up,vbs_detajj,mll,0)")
            dfwwbvbscatJerUp        [x] = dfwwbvbscatJerUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJerUp,vbs_detajj,mll,0)")
            dfwwbvbscatJERUp        [x] = dfwwbvbscatJERUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,0)")
            dfwwbvbscatJESUp        [x] = dfwwbvbscatJESUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,0)")
            dfwwbvbscatUnclusteredUp[x] = dfwwbvbscatUnclusteredUp[x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,0)")

            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwwvbscat[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwwvbscatMuonMomUp    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwwvbscatElectronMomUp[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwwvbscatJes00Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwwvbscatJes01Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwwvbscatJes02Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwwvbscatJes03Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwwvbscatJes04Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwwvbscatJes05Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwwvbscatJes06Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwwvbscatJes07Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwwvbscatJes08Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwwvbscatJes09Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwwvbscatJes10Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwwvbscatJes11Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwwvbscatJes12Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwwvbscatJes13Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwwvbscatJes14Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwwvbscatJes15Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwwvbscatJes16Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwwvbscatJes17Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwwvbscatJes18Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwwvbscatJes19Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwwvbscatJes20Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwwvbscatJes21Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwwvbscatJes22Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwwvbscatJes23Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwwvbscatJes24Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwwvbscatJes25Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwwvbscatJes26Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwwvbscatJes27Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwwvbscatJerUp        [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwwvbscatJERUp	       [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwwvbscatJESUp	       [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwwvbscatUnclusteredUp[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotWS")):
                startWS = 0
                histoWS[0+startWS] = dfwwvbscat[x].Histo1D(("histoWS_{0}".format(0+startWS), "histoWS_{0}".format(0+startWS), BinXF,minXF,maxXF), "finalVar","weightWSUnc0")
                histoWS[1+startWS] = dfwwvbscat[x].Histo1D(("histoWS_{0}".format(1+startWS), "histoWS_{0}".format(1+startWS), BinXF,minXF,maxXF), "finalVar","weightWSUnc1")
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 0
                histoNonPrompt[0+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwwvbscat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte2")

            startF = 400
            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwwbvbscat[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwwbvbscatMuonMomUp    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwwbvbscatElectronMomUp[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwwbvbscatJes00Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwwbvbscatJes01Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwwbvbscatJes02Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwwbvbscatJes03Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwwbvbscatJes04Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwwbvbscatJes05Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwwbvbscatJes06Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwwbvbscatJes07Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwwbvbscatJes08Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwwbvbscatJes09Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwwbvbscatJes10Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwwbvbscatJes11Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwwbvbscatJes12Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwwbvbscatJes13Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwwbvbscatJes14Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwwbvbscatJes15Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwwbvbscatJes16Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwwbvbscatJes17Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwwbvbscatJes18Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwwbvbscatJes19Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwwbvbscatJes20Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwwbvbscatJes21Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwwbvbscatJes22Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwwbvbscatJes23Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwwbvbscatJes24Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwwbvbscatJes25Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwwbvbscatJes26Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwwbvbscatJes27Up	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwwbvbscatJerUp	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwwbvbscatJERUp	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwwbvbscatJESUp	    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwwbvbscatUnclusteredUp[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotWS")):
                startWS = 2
                histoWS[0+startWS] = dfwwbvbscat[x].Histo1D(("histoWS_{0}".format(0+startWS), "histoWS_{0}".format(0+startWS), BinXF,minXF,maxXF), "finalVar","weightWSUnc0")
                histoWS[1+startWS] = dfwwbvbscat[x].Histo1D(("histoWS_{0}".format(1+startWS), "histoWS_{0}".format(1+startWS), BinXF,minXF,maxXF), "finalVar","weightWSUnc1")
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 6
                histoNonPrompt[0+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwwbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte2")

    report = []
    for x in range(nCat):
        report.append(dfwwvbscat[x].Report())
        if(x != theCat): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    myfile = ROOT.TFile("fillhisto_sswwAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].Write()
    for i in range(nhistoWS):
        if(histoWS[i] == 0): continue
        histoWS[i].Write()
    for i in range(nhistoNonPrompt):
        if(histoNonPrompt[i] == 0): continue
        histoNonPrompt[i].Write()
    myfile.Close()

def readMCSample(sampleNOW,year,skimType,whichJob,group,wsWeights,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

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
    if(SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotEWKSSWW")):
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

    analysis(df,sampleNOW,SwitchSample(sampleNOW,skimType)[2],weight,year,PDType,"false",whichJob,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,wsWeights,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

def readDASample(sampleNOW,year,skimType,whichJob,group,wsWeights,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

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

    analysis(df,sampleNOW,sampleNOW,weight,year,PDType,"true",whichJob,0,genEventSumLHEScaleRenorm,genEventSumPSRenorm,wsWeights,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

if __name__ == "__main__":

    group = 10

    skimType = "3l"
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

    wsWeights = []
    wsPath = "data/histoWSSF_{0}.root".format(year)
    fwsFile = ROOT.TFile(wsPath)
    wsWeights.append(fwsFile.Get("histoWSEtaSF"))
    wsWeights.append(fwsFile.Get("histoWSEtaSF_unc"))
    wsWeights.append(fwsFile.Get("histoWSEtaPtSF"))
    for x in range(3):
        wsWeights[x].SetDirectory(0)
    fwsFile.Close()

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
    histoTriggerSFEtaPt_0_0 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_0_0")
    histoTriggerSFEtaPt_0_1 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_0_1")
    histoTriggerSFEtaPt_0_2 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_0_2")
    histoTriggerSFEtaPt_0_3 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_0_3")
    histoTriggerSFEtaPt_1_0 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_1_0")
    histoTriggerSFEtaPt_1_1 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_1_1")
    histoTriggerSFEtaPt_1_2 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_1_2")
    histoTriggerSFEtaPt_1_3 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_1_3")
    histoTriggerSFEtaPt_2_0 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_2_0")
    histoTriggerSFEtaPt_2_1 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_2_1")
    histoTriggerSFEtaPt_2_2 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_2_2")
    histoTriggerSFEtaPt_2_3 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_2_3")
    histoTriggerSFEtaPt_3_0 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_3_0")
    histoTriggerSFEtaPt_3_1 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_3_1")
    histoTriggerSFEtaPt_3_2 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_3_2")
    histoTriggerSFEtaPt_3_3 = fTriggerSFFile.Get("histoTriggerV1SFEtaPt_3_3")
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
            readMCSample(process,year,skimType,whichJob,group,wsWeights,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
        elif(process >= 1000):
            readDASample(process,year,skimType,whichJob,group,wsWeights,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
    except Exception as e:
        print("FAILED {0}".format(e))

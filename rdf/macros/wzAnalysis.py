import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(4)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection3LVar, selectionTrigger2L, selectionElMu, selectionWeigths, makeFinalVariable
import tmva_helper_xml

makeDataCards = 3
correctionString = ""

doNtuples = False
# 0 = T, 1 = M, 2 = L
bTagSel = 0
useBTaggingWeights = 1

useFR = 1
whichAna = 0

altMass = "Def"

jetEtaCut = 2.5

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

muSelChoice = 2
FAKE_MU   = jsonObject['FAKE_MU']
TIGHT_MU = jsonObject['TIGHT_MU{0}'.format(muSelChoice)]
MUOWP = "Medium"

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

def selectionLL(df,year,PDType,isData,count):

    overallTriggers = jsonObject['triggers']
    TRIGGERMUEG = getTriggerFromJson(overallTriggers, "TRIGGERMUEG", year)
    TRIGGERDMU  = getTriggerFromJson(overallTriggers, "TRIGGERDMU", year)
    TRIGGERSMU  = getTriggerFromJson(overallTriggers, "TRIGGERSMU", year)
    TRIGGERDEL  = getTriggerFromJson(overallTriggers, "TRIGGERDEL", year)
    TRIGGERSEL  = getTriggerFromJson(overallTriggers, "TRIGGERSEL", year)

    dftag = selectionTrigger2L(df,year,PDType,JSON,isData,TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU,FAKE_EL,TIGHT_EL)

    dftag =(dftag.Filter("nLoose == 3","Only three loose leptons")
                 .Filter("nFake == 3","Three fake leptons")
                 .Filter("abs(Sum(fake_Muon_charge)+Sum(fake_Electron_charge)) == 1", "+/- 1 net charge")
                 .Define("eventNum", "event")
                 .Filter("(Sum(fake_mu) > 0 and Max(fake_Muon_pt) > 25) or (Sum(fake_el) > 0 and Max(fake_Electron_pt) > 25)","At least one high pt lepton")
                 )

    if(useFR == 0):
        dftag = dftag.Filter("nTight == 3","Three tight leptons")

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData,count,jetEtaCut)
    dftag = selection3LVar  (dftag,year,isData)

    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    xPtTrgBins = array('d', [10,15,20,25,30,35,40,50,60,70,80,90,105,120,150,200])

    nCat, nHisto, nhistoNonPrompt = plotCategory("kPlotCategories"), 700, 50
    histo    = [[0 for y in range(nCat)] for x in range(nHisto)]
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
                    .Define("theCat","compute_category({0},kPlotNonPrompt,kPlotWS,nFake,nTight,0)".format(theCat))
		    #.Define("bdt_vbfinc", ROOT.computeModel, ROOT.model.GetVariableNames())
                    )

    dfbase = tmva_helper.run_inference(dfbase,"bdt_vbfinc")

    dfwzcatMuonMomUp        = []
    dfwzcatElectronMomUp    = []
    dfwzcatJERUp            = []
    dfwzcatJESUp            = []
    dfwzcatUnclusteredUp    = []
    dfwzbcatMuonMomUp       = []
    dfwzbcatElectronMomUp   = []
    dfwzbcatJERUp           = []
    dfwzbcatJESUp           = []
    dfwzbcatUnclusteredUp   = []
    dfwzcat = []
    dfwzbcat = []
    dfwzjjcat = []
    dfwzbjjcat = []
    dfwzvbscat = []
    dfwzbvbscat = []
    dfzgcat = []
    dfwhcat = []
    dfwzvbsBDTcat = []
    dfEMMcat = []
    dfMEEcat = []

    dfwzvbscatMuonMomUp       = []
    dfwzvbscatElectronMomUp   = []
    dfwzvbscatJes00Up	      = []
    dfwzvbscatJes01Up	      = []
    dfwzvbscatJes02Up	      = []
    dfwzvbscatJes03Up	      = []
    dfwzvbscatJes04Up	      = []
    dfwzvbscatJes05Up	      = []
    dfwzvbscatJes06Up	      = []
    dfwzvbscatJes07Up	      = []
    dfwzvbscatJes08Up	      = []
    dfwzvbscatJes09Up	      = []
    dfwzvbscatJes10Up	      = []
    dfwzvbscatJes11Up	      = []
    dfwzvbscatJes12Up	      = []
    dfwzvbscatJes13Up	      = []
    dfwzvbscatJes14Up	      = []
    dfwzvbscatJes15Up	      = []
    dfwzvbscatJes16Up	      = []
    dfwzvbscatJes17Up	      = []
    dfwzvbscatJes18Up	      = []
    dfwzvbscatJes19Up	      = []
    dfwzvbscatJes20Up	      = []
    dfwzvbscatJes21Up	      = []
    dfwzvbscatJes22Up	      = []
    dfwzvbscatJes23Up	      = []
    dfwzvbscatJes24Up	      = []
    dfwzvbscatJes25Up	      = []
    dfwzvbscatJes26Up	      = []
    dfwzvbscatJes27Up	      = []
    dfwzvbscatJerUp           = []
    dfwzvbscatJERUp           = []
    dfwzvbscatJESUp           = []
    dfwzvbscatUnclusteredUp   = []

    dfwzbvbscatMuonMomUp      = []
    dfwzbvbscatElectronMomUp  = []
    dfwzbvbscatJes00Up	      = []
    dfwzbvbscatJes01Up	      = []
    dfwzbvbscatJes02Up	      = []
    dfwzbvbscatJes03Up	      = []
    dfwzbvbscatJes04Up	      = []
    dfwzbvbscatJes05Up	      = []
    dfwzbvbscatJes06Up	      = []
    dfwzbvbscatJes07Up	      = []
    dfwzbvbscatJes08Up	      = []
    dfwzbvbscatJes09Up	      = []
    dfwzbvbscatJes10Up	      = []
    dfwzbvbscatJes11Up	      = []
    dfwzbvbscatJes12Up	      = []
    dfwzbvbscatJes13Up	      = []
    dfwzbvbscatJes14Up	      = []
    dfwzbvbscatJes15Up	      = []
    dfwzbvbscatJes16Up	      = []
    dfwzbvbscatJes17Up	      = []
    dfwzbvbscatJes18Up	      = []
    dfwzbvbscatJes19Up	      = []
    dfwzbvbscatJes20Up	      = []
    dfwzbvbscatJes21Up	      = []
    dfwzbvbscatJes22Up	      = []
    dfwzbvbscatJes23Up	      = []
    dfwzbvbscatJes24Up	      = []
    dfwzbvbscatJes25Up	      = []
    dfwzbvbscatJes26Up	      = []
    dfwzbvbscatJes27Up	      = []
    dfwzbvbscatJerUp          = []
    dfwzbvbscatJERUp          = []
    dfwzbvbscatJESUp          = []
    dfwzbvbscatUnclusteredUp  = []
    for x in range(nCat):
        dfwzcat.append(dfbase.Filter("theCat=={0}".format(x), "correct category ({0})".format(x)))

        dfwzvbscatMuonMomUp    .append(dfwzcat[x])
        dfwzvbscatElectronMomUp.append(dfwzcat[x])
        dfwzvbscatJes00Up      .append(dfwzcat[x])
        dfwzvbscatJes01Up      .append(dfwzcat[x])
        dfwzvbscatJes02Up      .append(dfwzcat[x])
        dfwzvbscatJes03Up      .append(dfwzcat[x])
        dfwzvbscatJes04Up      .append(dfwzcat[x])
        dfwzvbscatJes05Up      .append(dfwzcat[x])
        dfwzvbscatJes06Up      .append(dfwzcat[x])
        dfwzvbscatJes07Up      .append(dfwzcat[x])
        dfwzvbscatJes08Up      .append(dfwzcat[x])
        dfwzvbscatJes09Up      .append(dfwzcat[x])
        dfwzvbscatJes10Up      .append(dfwzcat[x])
        dfwzvbscatJes11Up      .append(dfwzcat[x])
        dfwzvbscatJes12Up      .append(dfwzcat[x])
        dfwzvbscatJes13Up      .append(dfwzcat[x])
        dfwzvbscatJes14Up      .append(dfwzcat[x])
        dfwzvbscatJes15Up      .append(dfwzcat[x])
        dfwzvbscatJes16Up      .append(dfwzcat[x])
        dfwzvbscatJes17Up      .append(dfwzcat[x])
        dfwzvbscatJes18Up      .append(dfwzcat[x])
        dfwzvbscatJes19Up      .append(dfwzcat[x])
        dfwzvbscatJes20Up      .append(dfwzcat[x])
        dfwzvbscatJes21Up      .append(dfwzcat[x])
        dfwzvbscatJes22Up      .append(dfwzcat[x])
        dfwzvbscatJes23Up      .append(dfwzcat[x])
        dfwzvbscatJes24Up      .append(dfwzcat[x])
        dfwzvbscatJes25Up      .append(dfwzcat[x])
        dfwzvbscatJes26Up      .append(dfwzcat[x])
        dfwzvbscatJes27Up      .append(dfwzcat[x])
        dfwzvbscatJerUp        .append(dfwzcat[x])
        dfwzvbscatJERUp        .append(dfwzcat[x])
        dfwzvbscatJESUp        .append(dfwzcat[x])
        dfwzvbscatUnclusteredUp.append(dfwzcat[x])

        dfwzbvbscatMuonMomUp    .append(dfwzcat[x])
        dfwzbvbscatElectronMomUp.append(dfwzcat[x])
        dfwzbvbscatJes00Up      .append(dfwzcat[x])
        dfwzbvbscatJes01Up      .append(dfwzcat[x])
        dfwzbvbscatJes02Up      .append(dfwzcat[x])
        dfwzbvbscatJes03Up      .append(dfwzcat[x])
        dfwzbvbscatJes04Up      .append(dfwzcat[x])
        dfwzbvbscatJes05Up      .append(dfwzcat[x])
        dfwzbvbscatJes06Up      .append(dfwzcat[x])
        dfwzbvbscatJes07Up      .append(dfwzcat[x])
        dfwzbvbscatJes08Up      .append(dfwzcat[x])
        dfwzbvbscatJes09Up      .append(dfwzcat[x])
        dfwzbvbscatJes10Up      .append(dfwzcat[x])
        dfwzbvbscatJes11Up      .append(dfwzcat[x])
        dfwzbvbscatJes12Up      .append(dfwzcat[x])
        dfwzbvbscatJes13Up      .append(dfwzcat[x])
        dfwzbvbscatJes14Up      .append(dfwzcat[x])
        dfwzbvbscatJes15Up      .append(dfwzcat[x])
        dfwzbvbscatJes16Up      .append(dfwzcat[x])
        dfwzbvbscatJes17Up      .append(dfwzcat[x])
        dfwzbvbscatJes18Up      .append(dfwzcat[x])
        dfwzbvbscatJes19Up      .append(dfwzcat[x])
        dfwzbvbscatJes20Up      .append(dfwzcat[x])
        dfwzbvbscatJes21Up      .append(dfwzcat[x])
        dfwzbvbscatJes22Up      .append(dfwzcat[x])
        dfwzbvbscatJes23Up      .append(dfwzcat[x])
        dfwzbvbscatJes24Up      .append(dfwzcat[x])
        dfwzbvbscatJes25Up      .append(dfwzcat[x])
        dfwzbvbscatJes26Up      .append(dfwzcat[x])
        dfwzbvbscatJes27Up      .append(dfwzcat[x])
        dfwzbvbscatJerUp        .append(dfwzcat[x])
        dfwzbvbscatJERUp        .append(dfwzcat[x])
        dfwzbvbscatJESUp        .append(dfwzcat[x])
        dfwzbvbscatUnclusteredUp.append(dfwzcat[x])

        dfwzvbscatMuonMomUp     [x] = dfwzvbscatMuonMomUp     [x].Filter("mllZMuonMomUp     < 15 && m3lMuonMomUp     > 100 && ptlWMuonMomUp	> 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets	 >= 2 && vbs_mjj	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  	    > 30")
        dfwzvbscatElectronMomUp [x] = dfwzvbscatElectronMomUp [x].Filter("mllZElectronMomUp < 15 && m3lElectronMomUp > 100 && ptlWElectronMomUp > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets	 >= 2 && vbs_mjj	> 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt  		 > 30")
        dfwzvbscatJes00Up	[x] = dfwzvbscatJes00Up       [x].Filter("mllZ{0}           < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes00Up >= 2 && vbs_mjjJes00Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes01Up	[x] = dfwzvbscatJes01Up       [x].Filter("mllZ{0}           < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes01Up >= 2 && vbs_mjjJes01Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes02Up	[x] = dfwzvbscatJes02Up       [x].Filter("mllZ{0}           < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes02Up >= 2 && vbs_mjjJes02Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes03Up	[x] = dfwzvbscatJes03Up       [x].Filter("mllZ{0}           < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes03Up >= 2 && vbs_mjjJes03Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes04Up	[x] = dfwzvbscatJes04Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes04Up >= 2 && vbs_mjjJes04Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes05Up	[x] = dfwzvbscatJes05Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes05Up >= 2 && vbs_mjjJes05Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes06Up	[x] = dfwzvbscatJes06Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes06Up >= 2 && vbs_mjjJes06Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes07Up	[x] = dfwzvbscatJes07Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes07Up >= 2 && vbs_mjjJes07Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes08Up	[x] = dfwzvbscatJes08Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes08Up >= 2 && vbs_mjjJes08Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes09Up	[x] = dfwzvbscatJes09Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes09Up >= 2 && vbs_mjjJes09Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes10Up	[x] = dfwzvbscatJes10Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes10Up >= 2 && vbs_mjjJes10Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes11Up	[x] = dfwzvbscatJes11Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes11Up >= 2 && vbs_mjjJes11Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes12Up	[x] = dfwzvbscatJes12Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes12Up >= 2 && vbs_mjjJes12Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes13Up	[x] = dfwzvbscatJes13Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes13Up >= 2 && vbs_mjjJes13Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes14Up	[x] = dfwzvbscatJes14Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes14Up >= 2 && vbs_mjjJes14Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes15Up	[x] = dfwzvbscatJes15Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes15Up >= 2 && vbs_mjjJes15Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes16Up	[x] = dfwzvbscatJes16Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes16Up >= 2 && vbs_mjjJes16Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes17Up	[x] = dfwzvbscatJes17Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes17Up >= 2 && vbs_mjjJes17Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes18Up	[x] = dfwzvbscatJes18Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes18Up >= 2 && vbs_mjjJes18Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes19Up	[x] = dfwzvbscatJes19Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes19Up >= 2 && vbs_mjjJes19Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes20Up	[x] = dfwzvbscatJes20Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes20Up >= 2 && vbs_mjjJes20Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes21Up	[x] = dfwzvbscatJes21Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes21Up >= 2 && vbs_mjjJes21Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes22Up	[x] = dfwzvbscatJes22Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes22Up >= 2 && vbs_mjjJes22Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes23Up	[x] = dfwzvbscatJes23Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes23Up >= 2 && vbs_mjjJes23Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes24Up	[x] = dfwzvbscatJes24Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes24Up >= 2 && vbs_mjjJes24Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes25Up	[x] = dfwzvbscatJes25Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes25Up >= 2 && vbs_mjjJes25Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes26Up	[x] = dfwzvbscatJes26Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes26Up >= 2 && vbs_mjjJes26Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJes27Up	[x] = dfwzvbscatJes27Up       [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJes27Up >= 2 && vbs_mjjJes27Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJerUp  	[x] = dfwzvbscatJerUp	      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jetsJerUp   >= 2 && vbs_mjjJerUp   > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzvbscatJERUp         [x] = dfwzvbscatJERUp	      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets        >= 2 && vbs_mjj	     > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptJERUp	 > 30".format(altMass))
        dfwzvbscatJESUp         [x] = dfwzvbscatJESUp	      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets        >= 2 && vbs_mjj	     > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptJESUp	 > 30".format(altMass))
        dfwzvbscatUnclusteredUp [x] = dfwzvbscatUnclusteredUp [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet == 0 && nvbs_jets        >= 2 && vbs_mjj	     > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptUnclusteredUp > 30".format(altMass))

        dfwzbvbscatMuonMomUp    [x] = dfwzbvbscatMuonMomUp    [x].Filter("mllZMuonMomUp     < 15 && m3lMuonMomUp     > 100 && ptlWMuonMomUp	> 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets     >= 2 && vbs_mjj	     > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30")
        dfwzbvbscatElectronMomUp[x] = dfwzbvbscatElectronMomUp[x].Filter("mllZElectronMomUp < 15 && m3lElectronMomUp > 100 && ptlWElectronMomUp > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets     >= 2 && vbs_mjj	     > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30")
        dfwzbvbscatJes00Up	[x] = dfwzbvbscatJes00Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes00Up >= 2 && vbs_mjjJes00Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes01Up	[x] = dfwzbvbscatJes01Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes01Up >= 2 && vbs_mjjJes01Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes02Up	[x] = dfwzbvbscatJes02Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes02Up >= 2 && vbs_mjjJes02Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes03Up	[x] = dfwzbvbscatJes03Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes03Up >= 2 && vbs_mjjJes03Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes04Up	[x] = dfwzbvbscatJes04Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes04Up >= 2 && vbs_mjjJes04Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes05Up	[x] = dfwzbvbscatJes05Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes05Up >= 2 && vbs_mjjJes05Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes06Up	[x] = dfwzbvbscatJes06Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes06Up >= 2 && vbs_mjjJes06Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes07Up	[x] = dfwzbvbscatJes07Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes07Up >= 2 && vbs_mjjJes07Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes08Up	[x] = dfwzbvbscatJes08Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes08Up >= 2 && vbs_mjjJes08Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes09Up	[x] = dfwzbvbscatJes09Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes09Up >= 2 && vbs_mjjJes09Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes10Up	[x] = dfwzbvbscatJes10Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes10Up >= 2 && vbs_mjjJes10Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes11Up	[x] = dfwzbvbscatJes11Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes11Up >= 2 && vbs_mjjJes11Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes12Up	[x] = dfwzbvbscatJes12Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes12Up >= 2 && vbs_mjjJes12Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes13Up	[x] = dfwzbvbscatJes13Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes13Up >= 2 && vbs_mjjJes13Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes14Up	[x] = dfwzbvbscatJes14Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes14Up >= 2 && vbs_mjjJes14Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes15Up	[x] = dfwzbvbscatJes15Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes15Up >= 2 && vbs_mjjJes15Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes16Up	[x] = dfwzbvbscatJes16Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes16Up >= 2 && vbs_mjjJes16Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes17Up	[x] = dfwzbvbscatJes17Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes17Up >= 2 && vbs_mjjJes17Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes18Up	[x] = dfwzbvbscatJes18Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes18Up >= 2 && vbs_mjjJes18Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes19Up	[x] = dfwzbvbscatJes19Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes19Up >= 2 && vbs_mjjJes19Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes20Up	[x] = dfwzbvbscatJes20Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes20Up >= 2 && vbs_mjjJes20Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes21Up	[x] = dfwzbvbscatJes21Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes21Up >= 2 && vbs_mjjJes21Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes22Up	[x] = dfwzbvbscatJes22Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes22Up >= 2 && vbs_mjjJes22Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes23Up	[x] = dfwzbvbscatJes23Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes23Up >= 2 && vbs_mjjJes23Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes24Up	[x] = dfwzbvbscatJes24Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes24Up >= 2 && vbs_mjjJes24Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes25Up	[x] = dfwzbvbscatJes25Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes25Up >= 2 && vbs_mjjJes25Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes26Up	[x] = dfwzbvbscatJes26Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes26Up >= 2 && vbs_mjjJes26Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJes27Up	[x] = dfwzbvbscatJes27Up      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJes27Up >= 2 && vbs_mjjJes27Up > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJerUp  	[x] = dfwzbvbscatJerUp	      [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jetsJerUp   >= 2 && vbs_mjjJerUp   > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_pt		 > 30".format(altMass))
        dfwzbvbscatJERUp        [x] = dfwzbvbscatJERUp        [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets        >= 2 && vbs_mjj	     > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptJERUp	 > 30".format(altMass))
        dfwzbvbscatJESUp        [x] = dfwzbvbscatJESUp        [x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets        >= 2 && vbs_mjj	     > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptJESUp	 > 30".format(altMass))
        dfwzbvbscatUnclusteredUp[x] = dfwzbvbscatUnclusteredUp[x].Filter("mllZ{0}	    < 15 && m3l{0}	  > 100 && ptlW{0}	     > 20 && nbtag_goodbtag_Jet_bjet >  0 && nvbs_jets        >= 2 && vbs_mjj	     > 500 && vbs_detajj > 2.5 && vbs_zepvv < 1.0 && thePuppiMET_ptUnclusteredUp > 30".format(altMass))

        dfzgcat.append(dfwzcat[x].Filter("mll{0} > 10 && mll{0} < 110 && ptl1Z{0} > 25 && ptl2Z{0} > 20 && ptlW{0} > 20".format(altMass)))

        dfwhcat.append(dfwzcat[x].Filter("mll{0} == -1 && mllmin{0} > 10".format(altMass)))

        dfwzcat[x] = dfwzcat[x].Filter("mll{0} > 0".format(altMass),"mll > 0")

        histo[ 0][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x),120,  0, 120), "mllmin{0}".format(altMass),"weightNoBTag")
        dfwzcat[x] = dfwzcat[x].Filter("mllmin{0} > 1".format(altMass),"mllmin cut")

        dfEMMcat.append(dfwzcat[x].Filter("TriLepton_flavor == 1 && triggerSEL > 0 && fake_Electron_pt[0] > 30")
	                          .Define("pttag","Max(fake_Electron_pt)")
	                          .Define("ptmax","Max(fake_Muon_pt)")
	                          .Define("ptmin","Min(fake_Muon_pt)")
                                  )
        dfMEEcat.append(dfwzcat[x].Filter("TriLepton_flavor == 2 && triggerSMU > 0 && fake_Muon_pt[0] > 30")
	                          .Define("pttag","Max(fake_Muon_pt)")
	                          .Define("ptmax","Max(fake_Electron_pt)")
	                          .Define("ptmin","Min(fake_Electron_pt)")
                                  )
        histo[61][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(61,x), "histo_{0}_{1}".format(61,x), 20, 30, 130), "pttag","weightNoBTag")
        histo[62][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(62,x), "histo_{0}_{1}".format(62,x), 20, 30, 130), "pttag","weightNoBTag")

        dfEMMcat[x] = dfEMMcat[x].Filter("hasTriggerMatch(fake_Electron_eta[0],fake_Electron_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,1)")
        dfMEEcat[x] = dfMEEcat[x].Filter("hasTriggerMatch(fake_Muon_eta[0],fake_Muon_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,1)")

        histo[63][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(63,x), "histo_{0}_{1}".format(63,x), 20, 30, 130), "pttag","weightNoBTag")
        histo[64][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(64,x), "histo_{0}_{1}".format(64,x), 20, 30, 130), "pttag","weightNoBTag")

        histo[65][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(65,x), "histo_{0}_{1}".format(65,x), len(xPtTrgBins)-1, xPtTrgBins), "ptmax","weightNoBTag")
        histo[66][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(66,x), "histo_{0}_{1}".format(66,x), len(xPtTrgBins)-1, xPtTrgBins), "ptmin","weightNoBTag")
        histo[67][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(67,x), "histo_{0}_{1}".format(67,x), len(xPtTrgBins)-1, xPtTrgBins), "ptmax","weightNoBTag")
        histo[68][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(68,x), "histo_{0}_{1}".format(68,x), len(xPtTrgBins)-1, xPtTrgBins), "ptmin","weightNoBTag")

        dfEMMcat[x] = dfEMMcat[x].Filter("triggerDMU > 0")
        dfMEEcat[x] = dfMEEcat[x].Filter("triggerDEL > 0")

        histo[69][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(69,x), "histo_{0}_{1}".format(69,x), len(xPtTrgBins)-1, xPtTrgBins), "ptmax","weightNoBTag")
        histo[70][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(70,x), "histo_{0}_{1}".format(70,x), len(xPtTrgBins)-1, xPtTrgBins), "ptmin","weightNoBTag")
        histo[71][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(71,x), "histo_{0}_{1}".format(71,x), len(xPtTrgBins)-1, xPtTrgBins), "ptmax","weightNoBTag")
        histo[72][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(72,x), "histo_{0}_{1}".format(72,x), len(xPtTrgBins)-1, xPtTrgBins), "ptmin","weightNoBTag")

        dfwzcatMuonMomUp     .append(dfwzcat[x])
        dfwzcatElectronMomUp .append(dfwzcat[x])
        dfwzbcatMuonMomUp    .append(dfwzcat[x])
        dfwzbcatElectronMomUp.append(dfwzcat[x])

        histo[ 1][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x),100,  0, 100), "mllZ{0}".format(altMass),"weightNoBTag")
        dfwzcat                [x] = dfwzcat                [x].Filter("mllZ{0}             < 15".format(altMass),"mllZ cut")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("mllZMuonMomUp       < 15")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("mllZElectronMomUp   < 15")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("mllZMuonMomUp	    < 15")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("mllZElectronMomUp   < 15")

        histo[ 2][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x), 50, 70, 270), "m3l{0}".format(altMass),"weightNoBTag")
        dfwzcat                [x] = dfwzcat                [x].Filter("m3l{0}             > 100".format(altMass),"m3l cut")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("m3lMuonMomUp	   > 100")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("m3lElectronMomUp   > 100")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("m3lMuonMomUp	   > 100")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("m3lElectronMomUp   > 100")

        histo[73][x] = dfwzcat[x].Filter("(TriLepton_flavor==0||TriLepton_flavor==2) && ptlW{0} < 110".format(altMass)).Histo1D(("histo_{0}_{1}".format(73,x), "histo_{0}_{1}".format(73,x),40, 10, 110), "ptlW{0}".format(altMass),"weight")
        histo[74][x] = dfwzcat[x].Filter("(TriLepton_flavor==1||TriLepton_flavor==3) && ptlW{0} < 110".format(altMass)).Histo1D(("histo_{0}_{1}".format(74,x), "histo_{0}_{1}".format(74,x),40, 10, 110), "ptlW{0}".format(altMass),"weight")
        histo[75][x] = dfwzcat[x].Filter("(TriLepton_flavor==0||TriLepton_flavor==2) && ptlW{0} < 40".format(altMass)).Histo1D(("histo_{0}_{1}".format(75,x), "histo_{0}_{1}".format(75,x),25, 0.0, 2.5), "etalW","weight")
        histo[76][x] = dfwzcat[x].Filter("(TriLepton_flavor==1||TriLepton_flavor==3) && ptlW{0} < 40".format(altMass)).Histo1D(("histo_{0}_{1}".format(76,x), "histo_{0}_{1}".format(76,x),25, 0.0, 2.5), "etalW","weight")

        histo[ 3][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x), 50, 10, 210), "ptlW{0}".format(altMass),"weightNoBTag")
        dfwzcat                [x] = dfwzcat                [x].Filter("ptlW{0}             > 20".format(altMass),"ptlW cut")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("ptlWMuonMomUp       > 20")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("ptlWElectronMomUp   > 20")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("ptlWMuonMomUp	    > 20")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("ptlWElectronMomUp   > 20")

        dfwzbcat.append(dfwzcat[x].Filter("nbtag_goodbtag_Jet_bjet > 0","at least one good b-jet"))

        histo[ 4][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x), 4,-0.5 ,3.5), "nbtag_goodbtag_Jet_bjet","weight")
        dfwzcat[x]                 = dfwzcat                [x].Filter("nbtag_goodbtag_Jet_bjet == 0","no good b-jets")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("nbtag_goodbtag_Jet_bjet == 0")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("nbtag_goodbtag_Jet_bjet == 0")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("nbtag_goodbtag_Jet_bjet > 0")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("nbtag_goodbtag_Jet_bjet > 0")

        histo[15][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 40,  0, 200), "thePuppiMET_pt","weight")
        histo[16][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x), 40,  0, 200), "thePuppiMET_pt","weight")

        dfwzcatJERUp	      .append(dfwzcat[x].Filter("thePuppiMET_ptJERUp	       > 30"))
        dfwzcatJESUp	      .append(dfwzcat[x].Filter("thePuppiMET_ptJESUp	       > 30"))
        dfwzcatUnclusteredUp  .append(dfwzcat[x].Filter("thePuppiMET_ptUnclusteredUp   > 30"))

        dfwzbcatJERUp	       .append(dfwzbcat[x].Filter("thePuppiMET_ptJERUp           > 30"))
        dfwzbcatJESUp	       .append(dfwzbcat[x].Filter("thePuppiMET_ptJESUp           > 30"))
        dfwzbcatUnclusteredUp  .append(dfwzbcat[x].Filter("thePuppiMET_ptUnclusteredUp   > 30"))

        dfwzcat[x]                 = dfwzcat                [x].Filter("thePuppiMET_pt > 30","thePuppiMET_pt > 30")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("thePuppiMET_pt > 30")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("thePuppiMET_pt > 30")
        dfwzbcat[x]                = dfwzbcat               [x].Filter("thePuppiMET_pt > 30","thePuppiMET_pt > 30")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("thePuppiMET_pt > 30")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("thePuppiMET_pt > 30")

        histo[ 5][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x), 40, 25, 225), "ptl1Z{0}".format(altMass),"weight")
        histo[ 6][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x), 40, 25, 225), "ptl1Z{0}".format(altMass),"weight")
        histo[ 7][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x), 40, 10, 210), "ptl2Z{0}".format(altMass),"weight")
        histo[ 8][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x), 40, 10, 210), "ptl2Z{0}".format(altMass),"weight")
        histo[ 9][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x), 40,  0, 200), "mtW{0}".format(altMass),"weight")
        histo[10][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 40,  0, 200), "mtW{0}".format(altMass),"weight")
        histo[11][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 4,-0.5, 3.5), "TriLepton_flavor","weight")
        histo[12][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 4,-0.5, 3.5), "TriLepton_flavor","weight")
        histo[13][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 4,-0.5, 3.5), "ngood_jets","weight")
        histo[14][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 4,-0.5, 3.5), "ngood_jets","weight")

        dfwzjjcat .append(dfwzcat[x] .Filter("nvbs_jets >= 2", "At least two VBS jets"))
        dfwzbjjcat.append(dfwzbcat[x].Filter("nvbs_jets >= 2", "At least two VBS jets"))

        histo[17][x] = dfwzjjcat[x] .Histo1D(("histo_{0}_{1}".format(17,x), "histo_{0}_{1}".format(17,x), 4,1.5, 5.5), "ngood_jets","weight")
        histo[18][x] = dfwzbjjcat[x].Histo1D(("histo_{0}_{1}".format(18,x), "histo_{0}_{1}".format(18,x), 4,1.5, 5.5), "ngood_jets","weight")
        histo[19][x] = dfwzjjcat[x] .Histo1D(("histo_{0}_{1}".format(19,x), "histo_{0}_{1}".format(19,x), 40,0,2000), "vbs_mjj","weight")
        histo[20][x] = dfwzbjjcat[x].Histo1D(("histo_{0}_{1}".format(20,x), "histo_{0}_{1}".format(20,x), 40,0,2000), "vbs_mjj","weight")
        histo[21][x] = dfwzjjcat[x] .Histo1D(("histo_{0}_{1}".format(21,x), "histo_{0}_{1}".format(21,x), 40,0,10), "vbs_detajj","weight")
        histo[22][x] = dfwzbjjcat[x].Histo1D(("histo_{0}_{1}".format(22,x), "histo_{0}_{1}".format(22,x), 40,0,10), "vbs_detajj","weight")
        histo[23][x] = dfwzjjcat[x] .Histo1D(("histo_{0}_{1}".format(23,x), "histo_{0}_{1}".format(23,x), 40,0,3.1416), "vbs_dphijj","weight")
        histo[24][x] = dfwzbjjcat[x].Histo1D(("histo_{0}_{1}".format(24,x), "histo_{0}_{1}".format(24,x), 40,0,3.1416), "vbs_dphijj","weight")
        histo[25][x] = dfwzjjcat[x] .Histo1D(("histo_{0}_{1}".format(25,x), "histo_{0}_{1}".format(25,x), 20,-1,1), "bdt_vbfinc","weight")
        histo[26][x] = dfwzbjjcat[x].Histo1D(("histo_{0}_{1}".format(26,x), "histo_{0}_{1}".format(26,x), 20,-1,1), "bdt_vbfinc","weight")
        dfwzvbscat .append(dfwzjjcat[x] .Filter(VBSSEL, "VBS selection"))
        dfwzbvbscat.append(dfwzbjjcat[x].Filter(VBSSEL, "VBS selection"))

        histo[27][x] = dfwzvbscat[x] .Histo1D(("histo_{0}_{1}".format(27,x), "histo_{0}_{1}".format(27,x), 4,1.5, 5.5), "ngood_jets","weight")
        histo[28][x] = dfwzbvbscat[x].Histo1D(("histo_{0}_{1}".format(28,x), "histo_{0}_{1}".format(28,x), 4,1.5, 5.5), "ngood_jets","weight")
        histo[29][x] = dfwzvbscat[x] .Histo1D(("histo_{0}_{1}".format(29,x), "histo_{0}_{1}".format(29,x), 10,500,2500), "vbs_mjj","weight")
        histo[30][x] = dfwzbvbscat[x].Histo1D(("histo_{0}_{1}".format(30,x), "histo_{0}_{1}".format(30,x), 10,500,2500), "vbs_mjj","weight")
        histo[31][x] = dfwzvbscat[x] .Histo1D(("histo_{0}_{1}".format(31,x), "histo_{0}_{1}".format(31,x), 14,2.5,9.5), "vbs_detajj","weight")
        histo[32][x] = dfwzbvbscat[x].Histo1D(("histo_{0}_{1}".format(32,x), "histo_{0}_{1}".format(32,x), 14,2.5,9.5), "vbs_detajj","weight")
        histo[33][x] = dfwzvbscat[x] .Histo1D(("histo_{0}_{1}".format(33,x), "histo_{0}_{1}".format(33,x), 10,0,3.1416), "vbs_dphijj","weight")
        histo[34][x] = dfwzbvbscat[x].Histo1D(("histo_{0}_{1}".format(34,x), "histo_{0}_{1}".format(34,x), 10,0,3.1416), "vbs_dphijj","weight")
        histo[35][x] = dfwzvbscat[x] .Histo1D(("histo_{0}_{1}".format(35,x), "histo_{0}_{1}".format(35,x), 20,-1,1), "bdt_vbfinc","weight")
        histo[36][x] = dfwzbvbscat[x].Histo1D(("histo_{0}_{1}".format(36,x), "histo_{0}_{1}".format(36,x), 20,-1,1), "bdt_vbfinc","weight")

        if(doNtuples == True and x == theCat):
            outputFile = "ntupleWZAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob)
            dfwzvbscat[x].Snapshot("events", outputFile, branchList)
            dfwzvbsBDTcat.append(dfwzvbscat[x].Filter("bdt_vbfinc[0] >= 0","bdt_vbfinc[0] >= 0"))
            dfwzvbsBDTcat.append(dfwzvbscat[x].Filter("bdt_vbfinc[0] <  0","bdt_vbfinc[0] <  0"))
            histo[100][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(100,x), "histo_{0}_{1}".format(100,x), 5,1.5, 6.5), "ngood_jets","weight")
            histo[102][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(102,x), "histo_{0}_{1}".format(102,x), 80,500,4500), "vbs_mjj","weight")
            histo[104][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(104,x), "histo_{0}_{1}".format(104,x), 80,0,800), "vbs_ptjj","weight")
            histo[106][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(106,x), "histo_{0}_{1}".format(106,x), 60,2.5,8.5), "vbs_detajj","weight")
            histo[108][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(108,x), "histo_{0}_{1}".format(108,x), 62,0,3.2), "vbs_dphijj","weight")
            histo[110][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(110,x), "histo_{0}_{1}".format(110,x), 80,0,800), "vbs_ptj1","weight")
            histo[112][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(112,x), "histo_{0}_{1}".format(112,x), 80,0,400), "vbs_ptj2","weight")
            histo[114][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(114,x), "histo_{0}_{1}".format(114,x), 50,0,5), "vbs_etaj1","weight")
            histo[116][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(116,x), "histo_{0}_{1}".format(116,x), 50,0,5), "vbs_etaj2","weight")
            histo[118][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(118,x), "histo_{0}_{1}".format(118,x), 50,0,1), "vbs_zepvv","weight")
            histo[120][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(120,x), "histo_{0}_{1}".format(120,x), 50,0,2500), "vbs_sumHT","weight")
            histo[122][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(122,x), "histo_{0}_{1}".format(122,x), 50,0,1000), "vbs_ptvv","weight")
            histo[124][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(124,x), "histo_{0}_{1}".format(124,x), 60,0,300), "vbs_pttot","weight")
            histo[126][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(126,x), "histo_{0}_{1}".format(126,x), 80,0,8), "vbs_detavvj1","weight")
            histo[128][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(128,x), "histo_{0}_{1}".format(128,x), 80,0,8), "vbs_detavvj2","weight")
            histo[130][x] = dfwzvbsBDTcat[0].Histo1D(("histo_{0}_{1}".format(130,x), "histo_{0}_{1}".format(130,x), 80,-1,3), "vbs_ptbalance","weight")

            histo[101][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(101,x), "histo_{0}_{1}".format(101,x), 5,1.5, 6.5), "ngood_jets","weight")
            histo[103][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(103,x), "histo_{0}_{1}".format(103,x), 80,500,4500), "vbs_mjj","weight")
            histo[105][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(105,x), "histo_{0}_{1}".format(105,x), 80,0,800), "vbs_ptjj","weight")
            histo[107][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(107,x), "histo_{0}_{1}".format(107,x), 60,2.5,8.5), "vbs_detajj","weight")
            histo[109][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(109,x), "histo_{0}_{1}".format(109,x), 62,0,3.2), "vbs_dphijj","weight")
            histo[111][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(111,x), "histo_{0}_{1}".format(111,x), 80,0,800), "vbs_ptj1","weight")
            histo[113][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(113,x), "histo_{0}_{1}".format(113,x), 80,0,400), "vbs_ptj2","weight")
            histo[115][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(115,x), "histo_{0}_{1}".format(115,x), 50,0,5), "vbs_etaj1","weight")
            histo[117][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(117,x), "histo_{0}_{1}".format(117,x), 50,0,5), "vbs_etaj2","weight")
            histo[119][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(119,x), "histo_{0}_{1}".format(119,x), 50,0,1), "vbs_zepvv","weight")
            histo[121][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(121,x), "histo_{0}_{1}".format(121,x), 50,0,2500), "vbs_sumHT","weight")
            histo[123][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(123,x), "histo_{0}_{1}".format(123,x), 50,0,1000), "vbs_ptvv","weight")
            histo[125][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(125,x), "histo_{0}_{1}".format(125,x), 60,0,300), "vbs_pttot","weight")
            histo[127][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(127,x), "histo_{0}_{1}".format(127,x), 80,0,8), "vbs_detavvj1","weight")
            histo[129][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(129,x), "histo_{0}_{1}".format(129,x), 80,0,8), "vbs_detavvj2","weight")
            histo[131][x] = dfwzvbsBDTcat[1].Histo1D(("histo_{0}_{1}".format(131,x), "histo_{0}_{1}".format(131,x), 80,-1,3), "vbs_ptbalance","weight")

        histo[37][x] = dfzgcat[x].Histo1D(("histo_{0}_{1}".format(37,x), "histo_{0}_{1}".format(37,x), 40, 10, 210), "m3l{0}".format(altMass),"weight")
        dfzgcat[x] = dfzgcat[x].Filter("abs(m3l{0}-91.1876)<15".format(altMass))
        histo[38][x] = dfzgcat[x].Histo1D(("histo_{0}_{1}".format(38,x), "histo_{0}_{1}".format(38,x), 4,-0.5, 3.5), "TriLepton_flavor","weight")
        histo[39][x] = dfzgcat[x].Filter("TriLepton_flavor==0||TriLepton_flavor==2").Histo1D(("histo_{0}_{1}".format(39,x), "histo_{0}_{1}".format(39,x),20, 20, 120), "ptlW{0}".format(altMass),"weight")
        histo[40][x] = dfzgcat[x].Filter("TriLepton_flavor==1||TriLepton_flavor==3").Histo1D(("histo_{0}_{1}".format(40,x), "histo_{0}_{1}".format(40,x),20, 20, 120), "ptlW{0}".format(altMass),"weight")

        histo[51][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(51,x), "histo_{0}_{1}".format(51,x), 4,-0.5 ,3.5), "nbtag_goodbtag_Jet_bjet","weight")
        dfwhcat[x] = dfwhcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0")
        histo[52][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(52,x), "histo_{0}_{1}".format(52,x), 4,-0.5, 3.5), "ngood_jets","weight")
        dfwhcat[x] = dfwhcat[x].Filter("ngood_jets == 0")
        histo[53][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(53,x), "histo_{0}_{1}".format(53,x),4,-0.5, 3.5), "TriLepton_flavor","weight")
        histo[54][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(54,x), "histo_{0}_{1}".format(54,x),20, 10, 210), "mllmin{0}".format(altMass),"weight")
        histo[55][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(55,x), "histo_{0}_{1}".format(55,x),20,  0, 4), "drllmin","weight")
        histo[56][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(56,x), "histo_{0}_{1}".format(56,x),20, 10, 110), "ptl3{0}".format(altMass),"weight")

        histo[57][x] = dfwzcat[x].Filter("TriLepton_flavor==0").Histo1D(("histo_{0}_{1}".format(57,x), "histo_{0}_{1}".format(57,x), 4,-0.5, 3.5), "ngood_jets","weight")
        histo[58][x] = dfwzcat[x].Filter("TriLepton_flavor==1").Histo1D(("histo_{0}_{1}".format(58,x), "histo_{0}_{1}".format(58,x), 4,-0.5, 3.5), "ngood_jets","weight")
        histo[59][x] = dfwzcat[x].Filter("TriLepton_flavor==2").Histo1D(("histo_{0}_{1}".format(59,x), "histo_{0}_{1}".format(59,x), 4,-0.5, 3.5), "ngood_jets","weight")
        histo[60][x] = dfwzcat[x].Filter("TriLepton_flavor==3").Histo1D(("histo_{0}_{1}".format(60,x), "histo_{0}_{1}".format(60,x), 4,-0.5, 3.5), "ngood_jets","weight")

        #dfwzvbscat[x] = (dfwzvbscat[x].Redefine("vbs_mjj","vbs_mjjJes0Up")
	#	                      .Define("bdt_vbfincJes0Up", ROOT.computeModel, ROOT.model.GetVariableNames()))
        #histo[91][x] = dfwzvbscat[x].Histo1D(("histo_{0}_{1}".format(91,x), "histo_{0}_{1}".format(91,x), 20,-1,1), "bdt_vbfincJes0Up","weight")

        histo[91][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format(91,x), "histo_{0}_{1}".format(91,x), 4,-0.5, 3.5), "TriLepton_flavor","weight3")
        histo[92][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format(92,x), "histo_{0}_{1}".format(92,x), 4,-0.5, 3.5), "TriLepton_flavor","weight4")
        histo[93][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format(93,x), "histo_{0}_{1}".format(93,x), 4,-0.5, 3.5), "TriLepton_flavor","weightBTag")
        histo[94][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format(94,x), "histo_{0}_{1}".format(94,x), 4,-0.5, 3.5), "TriLepton_flavor","weightNoBTag")
        #histo[95][x] = dfwzcat[x].Filter("TriLepton_flavor==1").Histo1D(("histo_{0}_{1}".format(95,x), "histo_{0}_{1}".format(95,x), 4,-0.5, 3.5), "ngood_jets","weightNoBTVSF")
        #histo[96][x] = dfwzcat[x].Filter("TriLepton_flavor==2").Histo1D(("histo_{0}_{1}".format(96,x), "histo_{0}_{1}".format(96,x), 4,-0.5, 3.5), "ngood_jets","weightNoBTVSF")
        #histo[97][x] = dfwzcat[x].Filter("TriLepton_flavor==3").Histo1D(("histo_{0}_{1}".format(97,x), "histo_{0}_{1}".format(97,x), 4,-0.5, 3.5), "ngood_jets","weightNoBTVSF")

        if(makeDataCards == 1):
            BinXF = 4
            minXF = -0.5
            maxXF = 3.5

            startF = 300
            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwzcat[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwzcatMuonMomUp      [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwzcatElectronMomUp  [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes00Up"        ,theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes01Up"        ,theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes02Up"        ,theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes03Up"        ,theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes04Up"        ,theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes05Up"        ,theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes06Up"        ,theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes07Up"        ,theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes08Up"        ,theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes09Up"        ,theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes10Up"        ,theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes11Up"        ,theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes12Up"        ,theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes13Up"        ,theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes14Up"        ,theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes15Up"        ,theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes16Up"        ,theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes17Up"        ,theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes18Up"        ,theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes19Up"        ,theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes20Up"        ,theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes21Up"        ,theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes22Up"        ,theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes23Up"        ,theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes24Up"        ,theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes25Up"        ,theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes26Up"        ,theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes27Up"        ,theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJerUp"	      ,theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwzcatJERUp        [x],"ngood_jets"  ,theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwzcatJESUp        [x],"ngood_jets"  ,theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwzcatUnclusteredUp[x],"ngood_jets"  ,theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 0
                histoNonPrompt[0+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte2")

            startF = 500
            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwzbcat[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwzbcatMuonMomUp      [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwzbcatElectronMomUp  [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes00Up"        ,theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes01Up"        ,theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes02Up"        ,theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes03Up"        ,theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes04Up"        ,theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes05Up"        ,theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes06Up"        ,theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes07Up"        ,theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes08Up"        ,theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes09Up"        ,theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes10Up"        ,theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes11Up"        ,theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes12Up"        ,theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes13Up"        ,theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes14Up"        ,theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes15Up"        ,theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes16Up"        ,theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes17Up"        ,theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes18Up"        ,theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes19Up"        ,theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes20Up"        ,theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes21Up"        ,theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes22Up"        ,theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes23Up"        ,theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes24Up"        ,theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes25Up"        ,theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes26Up"        ,theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes27Up"        ,theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJerUp"	       ,theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwzbcatJERUp	     [x],"ngood_jets"  ,theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwzbcatJESUp	     [x],"ngood_jets"  ,theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwzbcatUnclusteredUp[x],"ngood_jets"  ,theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 6
                histoNonPrompt[0+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte2")


        elif(makeDataCards == 2):
            BinXF = 1
            minXF = -0.5
            maxXF = 3.5

            startF = 300
            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwzcat[x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwzcatMuonMomUp      [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwzcatElectronMomUp  [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwzcat[x]		 ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwzcatJERUp	      [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwzcatJESUp	      [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwzcatUnclusteredUp  [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 0
                histoNonPrompt[0+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAlte2")

            startF = 500
            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwzbcat[x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwzbcatMuonMomUp      [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwzbcatElectronMomUp  [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwzbcat[x]		  ,"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwzbcatJERUp	       [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwzbcatJESUp	       [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwzbcatUnclusteredUp  [x],"TriLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 6
                histoNonPrompt[0+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "TriLepton_flavor","weightFakeAlte2")

        elif(makeDataCards == 3):
            startF = 300
            BinXF = 12
            minXF = -0.5
            maxXF = 11.5

            # Making final variable
            dfwzvbscat             [x] = dfwzvbscat             [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,ngood_jets,10)")
            dfwzvbscatMuonMomUp    [x] = dfwzvbscatMuonMomUp    [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mllMuonMomUp,ngood_jets,10)")
            dfwzvbscatElectronMomUp[x] = dfwzvbscatElectronMomUp[x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mllElectronMomUp,ngood_jets,10)")
            dfwzvbscatJes00Up      [x] = dfwzvbscatJes00Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes00Up,vbs_detajj,mll,ngood_jetsJes00Up,10)")
            dfwzvbscatJes01Up      [x] = dfwzvbscatJes01Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes01Up,vbs_detajj,mll,ngood_jetsJes01Up,10)")
            dfwzvbscatJes02Up      [x] = dfwzvbscatJes02Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes02Up,vbs_detajj,mll,ngood_jetsJes02Up,10)")
            dfwzvbscatJes03Up      [x] = dfwzvbscatJes03Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes03Up,vbs_detajj,mll,ngood_jetsJes03Up,10)")
            dfwzvbscatJes04Up      [x] = dfwzvbscatJes04Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes04Up,vbs_detajj,mll,ngood_jetsJes04Up,10)")
            dfwzvbscatJes05Up      [x] = dfwzvbscatJes05Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes05Up,vbs_detajj,mll,ngood_jetsJes05Up,10)")
            dfwzvbscatJes06Up      [x] = dfwzvbscatJes06Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes06Up,vbs_detajj,mll,ngood_jetsJes06Up,10)")
            dfwzvbscatJes07Up      [x] = dfwzvbscatJes07Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes07Up,vbs_detajj,mll,ngood_jetsJes07Up,10)")
            dfwzvbscatJes08Up      [x] = dfwzvbscatJes08Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes08Up,vbs_detajj,mll,ngood_jetsJes08Up,10)")
            dfwzvbscatJes09Up      [x] = dfwzvbscatJes09Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes09Up,vbs_detajj,mll,ngood_jetsJes09Up,10)")
            dfwzvbscatJes10Up      [x] = dfwzvbscatJes10Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes10Up,vbs_detajj,mll,ngood_jetsJes10Up,10)")
            dfwzvbscatJes11Up      [x] = dfwzvbscatJes11Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes11Up,vbs_detajj,mll,ngood_jetsJes11Up,10)")
            dfwzvbscatJes12Up      [x] = dfwzvbscatJes12Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes12Up,vbs_detajj,mll,ngood_jetsJes12Up,10)")
            dfwzvbscatJes13Up      [x] = dfwzvbscatJes13Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes13Up,vbs_detajj,mll,ngood_jetsJes13Up,10)")
            dfwzvbscatJes14Up      [x] = dfwzvbscatJes14Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes14Up,vbs_detajj,mll,ngood_jetsJes14Up,10)")
            dfwzvbscatJes15Up      [x] = dfwzvbscatJes15Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes15Up,vbs_detajj,mll,ngood_jetsJes15Up,10)")
            dfwzvbscatJes16Up      [x] = dfwzvbscatJes16Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes16Up,vbs_detajj,mll,ngood_jetsJes16Up,10)")
            dfwzvbscatJes17Up      [x] = dfwzvbscatJes17Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes17Up,vbs_detajj,mll,ngood_jetsJes17Up,10)")
            dfwzvbscatJes18Up      [x] = dfwzvbscatJes18Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes18Up,vbs_detajj,mll,ngood_jetsJes18Up,10)")
            dfwzvbscatJes19Up      [x] = dfwzvbscatJes19Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes19Up,vbs_detajj,mll,ngood_jetsJes19Up,10)")
            dfwzvbscatJes20Up      [x] = dfwzvbscatJes20Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes20Up,vbs_detajj,mll,ngood_jetsJes20Up,10)")
            dfwzvbscatJes21Up      [x] = dfwzvbscatJes21Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes21Up,vbs_detajj,mll,ngood_jetsJes21Up,10)")
            dfwzvbscatJes22Up      [x] = dfwzvbscatJes22Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes22Up,vbs_detajj,mll,ngood_jetsJes22Up,10)")
            dfwzvbscatJes23Up      [x] = dfwzvbscatJes23Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes23Up,vbs_detajj,mll,ngood_jetsJes23Up,10)")
            dfwzvbscatJes24Up      [x] = dfwzvbscatJes24Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes24Up,vbs_detajj,mll,ngood_jetsJes24Up,10)")
            dfwzvbscatJes25Up      [x] = dfwzvbscatJes25Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes25Up,vbs_detajj,mll,ngood_jetsJes25Up,10)")
            dfwzvbscatJes26Up      [x] = dfwzvbscatJes26Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes26Up,vbs_detajj,mll,ngood_jetsJes26Up,10)")
            dfwzvbscatJes27Up      [x] = dfwzvbscatJes27Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes27Up,vbs_detajj,mll,ngood_jetsJes27Up,10)")
            dfwzvbscatJerUp        [x] = dfwzvbscatJerUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJerUp,vbs_detajj,mll,ngood_jetsJerUp,10)")
            dfwzvbscatJERUp        [x] = dfwzvbscatJERUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,ngood_jets,10)")
            dfwzvbscatJESUp        [x] = dfwzvbscatJESUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,ngood_jets,10)")
            dfwzvbscatUnclusteredUp[x] = dfwzvbscatUnclusteredUp[x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,ngood_jets,10)")

            dfwzbvbscat             [x] = dfwzbvbscat             [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,ngood_jets,10)")
            dfwzbvbscatMuonMomUp    [x] = dfwzbvbscatMuonMomUp    [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mllMuonMomUp,ngood_jets,10)")
            dfwzbvbscatElectronMomUp[x] = dfwzbvbscatElectronMomUp[x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mllElectronMomUp,ngood_jets,10)")
            dfwzbvbscatJes00Up      [x] = dfwzbvbscatJes00Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes00Up,vbs_detajj,mll,ngood_jetsJes00Up,10)")
            dfwzbvbscatJes01Up      [x] = dfwzbvbscatJes01Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes01Up,vbs_detajj,mll,ngood_jetsJes01Up,10)")
            dfwzbvbscatJes02Up      [x] = dfwzbvbscatJes02Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes02Up,vbs_detajj,mll,ngood_jetsJes02Up,10)")
            dfwzbvbscatJes03Up      [x] = dfwzbvbscatJes03Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes03Up,vbs_detajj,mll,ngood_jetsJes03Up,10)")
            dfwzbvbscatJes04Up      [x] = dfwzbvbscatJes04Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes04Up,vbs_detajj,mll,ngood_jetsJes04Up,10)")
            dfwzbvbscatJes05Up      [x] = dfwzbvbscatJes05Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes05Up,vbs_detajj,mll,ngood_jetsJes05Up,10)")
            dfwzbvbscatJes06Up      [x] = dfwzbvbscatJes06Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes06Up,vbs_detajj,mll,ngood_jetsJes06Up,10)")
            dfwzbvbscatJes07Up      [x] = dfwzbvbscatJes07Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes07Up,vbs_detajj,mll,ngood_jetsJes07Up,10)")
            dfwzbvbscatJes08Up      [x] = dfwzbvbscatJes08Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes08Up,vbs_detajj,mll,ngood_jetsJes08Up,10)")
            dfwzbvbscatJes09Up      [x] = dfwzbvbscatJes09Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes09Up,vbs_detajj,mll,ngood_jetsJes09Up,10)")
            dfwzbvbscatJes10Up      [x] = dfwzbvbscatJes10Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes10Up,vbs_detajj,mll,ngood_jetsJes10Up,10)")
            dfwzbvbscatJes11Up      [x] = dfwzbvbscatJes11Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes11Up,vbs_detajj,mll,ngood_jetsJes11Up,10)")
            dfwzbvbscatJes12Up      [x] = dfwzbvbscatJes12Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes12Up,vbs_detajj,mll,ngood_jetsJes12Up,10)")
            dfwzbvbscatJes13Up      [x] = dfwzbvbscatJes13Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes13Up,vbs_detajj,mll,ngood_jetsJes13Up,10)")
            dfwzbvbscatJes14Up      [x] = dfwzbvbscatJes14Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes14Up,vbs_detajj,mll,ngood_jetsJes14Up,10)")
            dfwzbvbscatJes15Up      [x] = dfwzbvbscatJes15Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes15Up,vbs_detajj,mll,ngood_jetsJes15Up,10)")
            dfwzbvbscatJes16Up      [x] = dfwzbvbscatJes16Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes16Up,vbs_detajj,mll,ngood_jetsJes16Up,10)")
            dfwzbvbscatJes17Up      [x] = dfwzbvbscatJes17Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes17Up,vbs_detajj,mll,ngood_jetsJes17Up,10)")
            dfwzbvbscatJes18Up      [x] = dfwzbvbscatJes18Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes18Up,vbs_detajj,mll,ngood_jetsJes18Up,10)")
            dfwzbvbscatJes19Up      [x] = dfwzbvbscatJes19Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes19Up,vbs_detajj,mll,ngood_jetsJes19Up,10)")
            dfwzbvbscatJes20Up      [x] = dfwzbvbscatJes20Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes20Up,vbs_detajj,mll,ngood_jetsJes20Up,10)")
            dfwzbvbscatJes21Up      [x] = dfwzbvbscatJes21Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes21Up,vbs_detajj,mll,ngood_jetsJes21Up,10)")
            dfwzbvbscatJes22Up      [x] = dfwzbvbscatJes22Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes22Up,vbs_detajj,mll,ngood_jetsJes22Up,10)")
            dfwzbvbscatJes23Up      [x] = dfwzbvbscatJes23Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes23Up,vbs_detajj,mll,ngood_jetsJes23Up,10)")
            dfwzbvbscatJes24Up      [x] = dfwzbvbscatJes24Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes24Up,vbs_detajj,mll,ngood_jetsJes24Up,10)")
            dfwzbvbscatJes25Up      [x] = dfwzbvbscatJes25Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes25Up,vbs_detajj,mll,ngood_jetsJes25Up,10)")
            dfwzbvbscatJes26Up      [x] = dfwzbvbscatJes26Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes26Up,vbs_detajj,mll,ngood_jetsJes26Up,10)")
            dfwzbvbscatJes27Up      [x] = dfwzbvbscatJes27Up      [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJes27Up,vbs_detajj,mll,ngood_jetsJes27Up,10)")
            dfwzbvbscatJerUp        [x] = dfwzbvbscatJerUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjjJerUp,vbs_detajj,mll,ngood_jetsJerUp,10)")
            dfwzbvbscatJERUp        [x] = dfwzbvbscatJERUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,ngood_jets,10)")
            dfwzbvbscatJESUp        [x] = dfwzbvbscatJESUp        [x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,ngood_jets,10)")
            dfwzbvbscatUnclusteredUp[x] = dfwzbvbscatUnclusteredUp[x].Define("finalVar", "compute_jet_lepton_final_var(vbs_mjj,vbs_detajj,mll,ngood_jets,10)")

            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwzvbscat[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwzvbscatMuonMomUp    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwzvbscatElectronMomUp[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwzvbscatJes00Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwzvbscatJes01Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwzvbscatJes02Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwzvbscatJes03Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwzvbscatJes04Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwzvbscatJes05Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwzvbscatJes06Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwzvbscatJes07Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwzvbscatJes08Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwzvbscatJes09Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwzvbscatJes10Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwzvbscatJes11Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwzvbscatJes12Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwzvbscatJes13Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwzvbscatJes14Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwzvbscatJes15Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwzvbscatJes16Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwzvbscatJes17Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwzvbscatJes18Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwzvbscatJes19Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwzvbscatJes20Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwzvbscatJes21Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwzvbscatJes22Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwzvbscatJes23Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwzvbscatJes24Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwzvbscatJes25Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwzvbscatJes26Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwzvbscatJes27Up      [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwzvbscatJerUp        [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwzvbscatJERUp	       [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwzvbscatJESUp	       [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwzvbscatUnclusteredUp[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 0
                histoNonPrompt[0+startNonPrompt] = dfwzvbscat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwzvbscat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwzvbscat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwzvbscat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwzvbscat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwzvbscat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte2")

            startF = 500
            for nv in range(0,135):
                histo[startF+nv][x] = makeFinalVariable(dfwzbvbscat[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+135][x]    = makeFinalVariable(dfwzbvbscatMuonMomUp    [x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwzbvbscatElectronMomUp[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwzbvbscatJes00Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwzbvbscatJes01Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwzbvbscatJes02Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwzbvbscatJes03Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwzbvbscatJes04Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwzbvbscatJes05Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwzbvbscatJes06Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwzbvbscatJes07Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwzbvbscatJes08Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwzbvbscatJes09Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwzbvbscatJes10Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwzbvbscatJes11Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwzbvbscatJes12Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwzbvbscatJes13Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwzbvbscatJes14Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwzbvbscatJes15Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwzbvbscatJes16Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwzbvbscatJes17Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwzbvbscatJes18Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwzbvbscatJes19Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwzbvbscatJes20Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwzbvbscatJes21Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwzbvbscatJes22Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfwzbvbscatJes23Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfwzbvbscatJes24Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfwzbvbscatJes25Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfwzbvbscatJes26Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfwzbvbscatJes27Up	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfwzbvbscatJerUp	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfwzbvbscatJERUp	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfwzbvbscatJESUp	[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfwzbvbscatUnclusteredUp[x],"finalVar",theCat,startF,x,BinXF,minXF,maxXF,168)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 6
                histoNonPrompt[0+startNonPrompt] = dfwzbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwzbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwzbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAltm2")
                histoNonPrompt[3+startNonPrompt] = dfwzbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte0")
                histoNonPrompt[4+startNonPrompt] = dfwzbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(4+startNonPrompt), "histoNonPrompt_{0}".format(4+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte1")
                histoNonPrompt[5+startNonPrompt] = dfwzbvbscat[x].Histo1D(("histoNonPrompt_{0}".format(5+startNonPrompt), "histoNonPrompt_{0}".format(5+startNonPrompt), BinXF,minXF,maxXF), "finalVar","weightFakeAlte2")
    report = []
    for x in range(nCat):
        report.append(dfwzvbscat[x].Report())
        if(x != theCat): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    myfile = ROOT.TFile("fillhisto_wzAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].Write()
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
    if(SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotWZ") or
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
            readMCSample(process,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
        elif(process >= 1000):
            readDASample(process,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
    except Exception as e:
        print("FAILED {0}".format(e))

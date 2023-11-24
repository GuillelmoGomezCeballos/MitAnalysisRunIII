import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(3)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection3LVar, selectionTrigger2L, selectionElMu, selectionWeigths, makeFinalVariable
import tmva_helper_xml

makeDataCards = True
correctionString = ""

doNtuples = False
# 0 = T, 1 = M, 2 = L
bTagSel = 0
useBTaggingWeights = 1

useFR = 1

altMass = "Def"

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
    dftag = selectionJetMet (dftag,year,bTagSel,isData,count,5.0)
    dftag = selection3LVar  (dftag,year,isData)

    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    xPtTrgbins = array('d', [10,15,20,25,30,35,40,50,60,70,80,90,105,120,150,200])

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
    ROOT.initHisto2D(histoFakeEtaPt_el[1],28)
    ROOT.initHisto2D(histoFakeEtaPt_el[2],29)
    ROOT.initHisto2D(histoFakeEtaPt_el[3],30)
    ROOT.initHisto2D(histoFakeEtaPt_el[4],31)
    ROOT.initHisto2D(histoFakeEtaPt_el[5],32)
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

    dfbase = selectionWeigths(dftag,isData,year,PDType,weight,useFR,bTagSel,useBTaggingWeights,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,MUOWP,ELEWP,correctionString,0)

    dfbase = (dfbase.Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                    .Define("kPlotWS", "{0}".format(plotCategory("kPlotWS")))
                    .Define("theCat","compute_category({0},kPlotNonPrompt,kPlotWS,nFake,nTight,0)".format(theCat))
		    #.Define("bdt_vbfinc", ROOT.computeModel, ROOT.model.GetVariableNames())
                    )

    dfbase = tmva_helper.run_inference(dfbase,"bdt_vbfinc")

    dfwzcatMuonMomUp        = []
    dfwzcatMuonMomDown      = []
    dfwzcatElectronMomUp    = []
    dfwzcatElectronMomDown  = []
    dfwzcatJERUp            = []
    dfwzcatJERDown          = []
    dfwzcatJESUp            = []
    dfwzcatJESDown          = []
    dfwzcatUnclusteredUp    = []
    dfwzcatUnclusteredDown  = []
    dfwzbcatMuonMomUp       = []
    dfwzbcatMuonMomDown     = []
    dfwzbcatElectronMomUp   = []
    dfwzbcatElectronMomDown = []
    dfwzbcatJERUp           = []
    dfwzbcatJERDown         = []
    dfwzbcatJESUp           = []
    dfwzbcatJESDown         = []
    dfwzbcatUnclusteredUp   = []
    dfwzbcatUnclusteredDown = []
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
    for x in range(nCat):
        dfwzcat.append(dfbase.Filter("theCat=={0}".format(x), "correct category ({0})".format(x)))

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

        histo[65][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(65,x), "histo_{0}_{1}".format(65,x), len(xPtTrgbins)-1, xPtTrgbins), "ptmax","weightNoBTag")
        histo[66][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(66,x), "histo_{0}_{1}".format(66,x), len(xPtTrgbins)-1, xPtTrgbins), "ptmin","weightNoBTag")
        histo[67][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(67,x), "histo_{0}_{1}".format(67,x), len(xPtTrgbins)-1, xPtTrgbins), "ptmax","weightNoBTag")
        histo[68][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(68,x), "histo_{0}_{1}".format(68,x), len(xPtTrgbins)-1, xPtTrgbins), "ptmin","weightNoBTag")

        dfEMMcat[x] = dfEMMcat[x].Filter("triggerDMU > 0")
        dfMEEcat[x] = dfMEEcat[x].Filter("triggerDEL > 0")

        histo[69][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(69,x), "histo_{0}_{1}".format(69,x), len(xPtTrgbins)-1, xPtTrgbins), "ptmax","weightNoBTag")
        histo[70][x] = dfEMMcat[x].Histo1D(("histo_{0}_{1}".format(70,x), "histo_{0}_{1}".format(70,x), len(xPtTrgbins)-1, xPtTrgbins), "ptmin","weightNoBTag")
        histo[71][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(71,x), "histo_{0}_{1}".format(71,x), len(xPtTrgbins)-1, xPtTrgbins), "ptmax","weightNoBTag")
        histo[72][x] = dfMEEcat[x].Histo1D(("histo_{0}_{1}".format(72,x), "histo_{0}_{1}".format(72,x), len(xPtTrgbins)-1, xPtTrgbins), "ptmin","weightNoBTag")

        dfwzcatMuonMomUp      .append(dfwzcat[x])
        dfwzcatMuonMomDown    .append(dfwzcat[x])
        dfwzcatElectronMomUp  .append(dfwzcat[x])
        dfwzcatElectronMomDown.append(dfwzcat[x])
        dfwzbcatMuonMomUp      .append(dfwzcat[x])
        dfwzbcatMuonMomDown    .append(dfwzcat[x])
        dfwzbcatElectronMomUp  .append(dfwzcat[x])
        dfwzbcatElectronMomDown.append(dfwzcat[x])

        histo[ 1][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x),100,  0, 100), "mllZ{0}".format(altMass),"weightNoBTag")
        dfwzcat                [x] = dfwzcat                [x].Filter("mllZ{0}             < 15".format(altMass),"mllZ cut")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("mllZMuonMomUp       < 15")
        dfwzcatMuonMomDown     [x] = dfwzcatMuonMomDown     [x].Filter("mllZMuonMomDown     < 15")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("mllZElectronMomUp   < 15")
        dfwzcatElectronMomDown [x] = dfwzcatElectronMomDown [x].Filter("mllZElectronMomDown < 15")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("mllZMuonMomUp	    < 15")
        dfwzbcatMuonMomDown    [x] = dfwzbcatMuonMomDown    [x].Filter("mllZMuonMomDown     < 15")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("mllZElectronMomUp   < 15")
        dfwzbcatElectronMomDown[x] = dfwzbcatElectronMomDown[x].Filter("mllZElectronMomDown < 15")

        histo[ 2][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x), 50, 70, 270), "m3l{0}".format(altMass),"weightNoBTag")
        dfwzcat                [x] = dfwzcat                [x].Filter("m3l{0}             > 100".format(altMass),"m3l cut")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("m3lMuonMomUp	   > 100")
        dfwzcatMuonMomDown     [x] = dfwzcatMuonMomDown     [x].Filter("m3lMuonMomDown     > 100")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("m3lElectronMomUp   > 100")
        dfwzcatElectronMomDown [x] = dfwzcatElectronMomDown [x].Filter("m3lElectronMomDown > 100")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("m3lMuonMomUp	   > 100")
        dfwzbcatMuonMomDown    [x] = dfwzbcatMuonMomDown    [x].Filter("m3lMuonMomDown     > 100")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("m3lElectronMomUp   > 100")
        dfwzbcatElectronMomDown[x] = dfwzbcatElectronMomDown[x].Filter("m3lElectronMomDown > 100")

        histo[73][x] = dfwzcat[x].Filter("(TriLepton_flavor==0||TriLepton_flavor==2) && ptlW{0} < 110".format(altMass)).Histo1D(("histo_{0}_{1}".format(73,x), "histo_{0}_{1}".format(73,x),40, 10, 110), "ptlW{0}".format(altMass),"weight")
        histo[74][x] = dfwzcat[x].Filter("(TriLepton_flavor==1||TriLepton_flavor==3) && ptlW{0} < 110".format(altMass)).Histo1D(("histo_{0}_{1}".format(74,x), "histo_{0}_{1}".format(74,x),40, 10, 110), "ptlW{0}".format(altMass),"weight")
        histo[75][x] = dfwzcat[x].Filter("(TriLepton_flavor==0||TriLepton_flavor==2) && ptlW{0} < 40".format(altMass)).Histo1D(("histo_{0}_{1}".format(75,x), "histo_{0}_{1}".format(75,x),25, 0.0, 2.5), "etalW","weight")
        histo[76][x] = dfwzcat[x].Filter("(TriLepton_flavor==1||TriLepton_flavor==3) && ptlW{0} < 40".format(altMass)).Histo1D(("histo_{0}_{1}".format(76,x), "histo_{0}_{1}".format(76,x),25, 0.0, 2.5), "etalW","weight")

        histo[ 3][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x), 50, 10, 210), "ptlW{0}".format(altMass),"weightNoBTag")
        dfwzcat                [x] = dfwzcat                [x].Filter("ptlW{0}             > 20".format(altMass),"ptlW cut")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("ptlWMuonMomUp       > 20")
        dfwzcatMuonMomDown     [x] = dfwzcatMuonMomDown     [x].Filter("ptlWMuonMomDown     > 20")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("ptlWElectronMomUp   > 20")
        dfwzcatElectronMomDown [x] = dfwzcatElectronMomDown [x].Filter("ptlWElectronMomDown > 20")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("ptlWMuonMomUp	    > 20")
        dfwzbcatMuonMomDown    [x] = dfwzbcatMuonMomDown    [x].Filter("ptlWMuonMomDown     > 20")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("ptlWElectronMomUp   > 20")
        dfwzbcatElectronMomDown[x] = dfwzbcatElectronMomDown[x].Filter("ptlWElectronMomDown > 20")

        dfwzbcat.append(dfwzcat[x].Filter("nbtag_goodbtag_Jet_bjet > 0","at least one good b-jet"))

        histo[ 4][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x), 5,-0.5 ,4.5), "nbtag_goodbtag_Jet_bjet","weight")
        dfwzcat[x]                 = dfwzcat                [x].Filter("nbtag_goodbtag_Jet_bjet == 0","no good b-jets")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("nbtag_goodbtag_Jet_bjet == 0")
        dfwzcatMuonMomDown     [x] = dfwzcatMuonMomDown     [x].Filter("nbtag_goodbtag_Jet_bjet == 0")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("nbtag_goodbtag_Jet_bjet == 0")
        dfwzcatElectronMomDown [x] = dfwzcatElectronMomDown [x].Filter("nbtag_goodbtag_Jet_bjet == 0")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("nbtag_goodbtag_Jet_bjet > 0")
        dfwzbcatMuonMomDown    [x] = dfwzbcatMuonMomDown    [x].Filter("nbtag_goodbtag_Jet_bjet > 0")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("nbtag_goodbtag_Jet_bjet > 0")
        dfwzbcatElectronMomDown[x] = dfwzbcatElectronMomDown[x].Filter("nbtag_goodbtag_Jet_bjet > 0")

        histo[15][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 40,  0, 200), "thePuppiMET_pt","weight")
        histo[16][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x), 40,  0, 200), "thePuppiMET_pt","weight")

        dfwzcatJERUp	      .append(dfwzcat[x].Filter("thePuppiMET_ptJERUp	       > 30"))
        dfwzcatJERDown        .append(dfwzcat[x].Filter("thePuppiMET_ptJERDown         > 30"))
        dfwzcatJESUp	      .append(dfwzcat[x].Filter("thePuppiMET_ptJESUp	       > 30"))
        dfwzcatJESDown        .append(dfwzcat[x].Filter("thePuppiMET_ptJESDown         > 30"))
        dfwzcatUnclusteredUp  .append(dfwzcat[x].Filter("thePuppiMET_ptUnclusteredUp   > 30"))
        dfwzcatUnclusteredDown.append(dfwzcat[x].Filter("thePuppiMET_ptUnclusteredDown > 30"))

        dfwzbcatJERUp	       .append(dfwzbcat[x].Filter("thePuppiMET_ptJERUp           > 30"))
        dfwzbcatJERDown        .append(dfwzbcat[x].Filter("thePuppiMET_ptJERDown         > 30"))
        dfwzbcatJESUp	       .append(dfwzbcat[x].Filter("thePuppiMET_ptJESUp           > 30"))
        dfwzbcatJESDown        .append(dfwzbcat[x].Filter("thePuppiMET_ptJESDown         > 30"))
        dfwzbcatUnclusteredUp  .append(dfwzbcat[x].Filter("thePuppiMET_ptUnclusteredUp   > 30"))
        dfwzbcatUnclusteredDown.append(dfwzbcat[x].Filter("thePuppiMET_ptUnclusteredDown > 30"))

        dfwzcat[x]                 = dfwzcat                [x].Filter("thePuppiMET_pt > 30","thePuppiMET_pt > 30")
        dfwzcatMuonMomUp       [x] = dfwzcatMuonMomUp       [x].Filter("thePuppiMET_pt > 30")
        dfwzcatMuonMomDown     [x] = dfwzcatMuonMomDown     [x].Filter("thePuppiMET_pt > 30")
        dfwzcatElectronMomUp   [x] = dfwzcatElectronMomUp   [x].Filter("thePuppiMET_pt > 30")
        dfwzcatElectronMomDown [x] = dfwzcatElectronMomDown [x].Filter("thePuppiMET_pt > 30")
        dfwzbcat[x]                = dfwzbcat               [x].Filter("thePuppiMET_pt > 30","thePuppiMET_pt > 30")
        dfwzbcatMuonMomUp      [x] = dfwzbcatMuonMomUp      [x].Filter("thePuppiMET_pt > 30")
        dfwzbcatMuonMomDown    [x] = dfwzbcatMuonMomDown    [x].Filter("thePuppiMET_pt > 30")
        dfwzbcatElectronMomUp  [x] = dfwzbcatElectronMomUp  [x].Filter("thePuppiMET_pt > 30")
        dfwzbcatElectronMomDown[x] = dfwzbcatElectronMomDown[x].Filter("thePuppiMET_pt > 30")

        histo[ 5][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x), 40, 25, 225), "ptl1Z{0}".format(altMass),"weight")
        histo[ 6][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x), 40, 25, 225), "ptl1Z{0}".format(altMass),"weight")
        histo[ 7][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x), 40, 10, 210), "ptl2Z{0}".format(altMass),"weight")
        histo[ 8][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x), 40, 10, 210), "ptl2Z{0}".format(altMass),"weight")
        histo[ 9][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x), 40,  0, 200), "mtW{0}".format(altMass),"weight")
        histo[10][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 40,  0, 200), "mtW{0}".format(altMass),"weight")
        histo[11][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 4,-0.5, 3.5), "TriLepton_flavor","weight")
        histo[12][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 4,-0.5, 3.5), "TriLepton_flavor","weight")
        histo[13][x] = dfwzcat[x] .Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 6,-0.5, 5.5), "ngood_jets","weight")
        histo[14][x] = dfwzbcat[x].Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 6,-0.5, 5.5), "ngood_jets","weight")

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

        histo[51][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(51,x), "histo_{0}_{1}".format(51,x), 5,-0.5 ,4.5), "nbtag_goodbtag_Jet_bjet","weight")
        dfwhcat[x] = dfwhcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0")
        histo[52][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(52,x), "histo_{0}_{1}".format(52,x), 6,-0.5, 5.5), "ngood_jets","weight")
        dfwhcat[x] = dfwhcat[x].Filter("ngood_jets == 0")
        histo[53][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(53,x), "histo_{0}_{1}".format(53,x),4,-0.5, 3.5), "TriLepton_flavor","weight")
        histo[54][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(54,x), "histo_{0}_{1}".format(54,x),20, 10, 210), "mllmin{0}".format(altMass),"weight")
        histo[55][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(55,x), "histo_{0}_{1}".format(55,x),20,  0, 4), "drllmin","weight")
        histo[56][x] = dfwhcat[x].Histo1D(("histo_{0}_{1}".format(56,x), "histo_{0}_{1}".format(56,x),20, 10, 110), "ptl3{0}".format(altMass),"weight")

        histo[57][x] = dfwzcat[x].Filter("TriLepton_flavor==0").Histo1D(("histo_{0}_{1}".format(57,x), "histo_{0}_{1}".format(57,x), 6,-0.5, 5.5), "ngood_jets","weight")
        histo[58][x] = dfwzcat[x].Filter("TriLepton_flavor==1").Histo1D(("histo_{0}_{1}".format(58,x), "histo_{0}_{1}".format(58,x), 6,-0.5, 5.5), "ngood_jets","weight")
        histo[59][x] = dfwzcat[x].Filter("TriLepton_flavor==2").Histo1D(("histo_{0}_{1}".format(59,x), "histo_{0}_{1}".format(59,x), 6,-0.5, 5.5), "ngood_jets","weight")
        histo[60][x] = dfwzcat[x].Filter("TriLepton_flavor==3").Histo1D(("histo_{0}_{1}".format(60,x), "histo_{0}_{1}".format(60,x), 6,-0.5, 5.5), "ngood_jets","weight")

        #dfwzvbscat[x] = (dfwzvbscat[x].Redefine("vbs_mjj","vbs_mjjJes0Up")
	#	                      .Define("bdt_vbfincJes0Up", ROOT.computeModel, ROOT.model.GetVariableNames()))
        #histo[91][x] = dfwzvbscat[x].Histo1D(("histo_{0}_{1}".format(91,x), "histo_{0}_{1}".format(91,x), 20,-1,1), "bdt_vbfincJes0Up","weight")

        histo[91][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format(91,x), "histo_{0}_{1}".format(91,x), 4,-0.5, 3.5), "TriLepton_flavor","weight3")
        histo[92][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format(92,x), "histo_{0}_{1}".format(92,x), 4,-0.5, 3.5), "TriLepton_flavor","weight4")
        histo[93][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format(93,x), "histo_{0}_{1}".format(93,x), 4,-0.5, 3.5), "TriLepton_flavor","weightBTag")
        histo[94][x] = dfwzcat[x].Histo1D(("histo_{0}_{1}".format(94,x), "histo_{0}_{1}".format(94,x), 4,-0.5, 3.5), "TriLepton_flavor","weightNoBTag")
        #histo[95][x] = dfwzcat[x].Filter("TriLepton_flavor==1").Histo1D(("histo_{0}_{1}".format(95,x), "histo_{0}_{1}".format(95,x), 6,-0.5, 5.5), "ngood_jets","weightNoBTVSF")
        #histo[96][x] = dfwzcat[x].Filter("TriLepton_flavor==2").Histo1D(("histo_{0}_{1}".format(96,x), "histo_{0}_{1}".format(96,x), 6,-0.5, 5.5), "ngood_jets","weightNoBTVSF")
        #histo[97][x] = dfwzcat[x].Filter("TriLepton_flavor==3").Histo1D(("histo_{0}_{1}".format(97,x), "histo_{0}_{1}".format(97,x), 6,-0.5, 5.5), "ngood_jets","weightNoBTVSF")

        if(makeDataCards == True):
            BinXF = 4
            minXF = -0.5
            maxXF = 3.5

            startF = 300
            for nv in range(0,134):
                histo[startF+nv][x] = makeFinalVariable(dfwzcat[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+134][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes0Up"  ,theCat,startF,x,BinXF,minXF,maxXF,134)
            histo[startF+135][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes0Down",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJerUp"  ,theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJerDown",theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwzcatMuonMomUp      [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwzcatMuonMomDown    [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwzcatElectronMomUp  [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwzcatElectronMomDown[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwzcatJERUp	      [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwzcatJERDown        [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwzcatJESUp	      [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwzcatJESDown        [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwzcatUnclusteredUp  [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwzcatUnclusteredDown[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes1Up"  ,theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes1Down",theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes2Up"  ,theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes2Down",theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes3Up"  ,theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes3Down",theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes4Up"  ,theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes4Down",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes5Up"  ,theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes5Down",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes6Up"  ,theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwzcat[x],"ngood_jetsJes6Down",theCat,startF,x,BinXF,minXF,maxXF,159)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 0
                histoNonPrompt[0+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[3+startNonPrompt] = dfwzcat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")

            startF = 500
            for nv in range(0,134):
                histo[startF+nv][x] = makeFinalVariable(dfwzbcat[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+134][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes0Up"  ,theCat,startF,x,BinXF,minXF,maxXF,134)
            histo[startF+135][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes0Down",theCat,startF,x,BinXF,minXF,maxXF,135)
            histo[startF+136][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJerUp"  ,theCat,startF,x,BinXF,minXF,maxXF,136)
            histo[startF+137][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJerDown",theCat,startF,x,BinXF,minXF,maxXF,137)
            histo[startF+138][x]    = makeFinalVariable(dfwzbcatMuonMomUp      [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,138)
            histo[startF+139][x]    = makeFinalVariable(dfwzbcatMuonMomDown    [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,139)
            histo[startF+140][x]    = makeFinalVariable(dfwzbcatElectronMomUp  [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,140)
            histo[startF+141][x]    = makeFinalVariable(dfwzbcatElectronMomDown[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,141)
            histo[startF+142][x]    = makeFinalVariable(dfwzbcatJERUp	       [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,142)
            histo[startF+143][x]    = makeFinalVariable(dfwzbcatJERDown        [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,143)
            histo[startF+144][x]    = makeFinalVariable(dfwzbcatJESUp	       [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,144)
            histo[startF+145][x]    = makeFinalVariable(dfwzbcatJESDown        [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,145)
            histo[startF+146][x]    = makeFinalVariable(dfwzbcatUnclusteredUp  [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,146)
            histo[startF+147][x]    = makeFinalVariable(dfwzbcatUnclusteredDown[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,147)
            histo[startF+148][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes1Up"  ,theCat,startF,x,BinXF,minXF,maxXF,148)
            histo[startF+149][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes1Down",theCat,startF,x,BinXF,minXF,maxXF,149)
            histo[startF+150][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes2Up"  ,theCat,startF,x,BinXF,minXF,maxXF,150)
            histo[startF+151][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes2Down",theCat,startF,x,BinXF,minXF,maxXF,151)
            histo[startF+152][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes3Up"  ,theCat,startF,x,BinXF,minXF,maxXF,152)
            histo[startF+153][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes3Down",theCat,startF,x,BinXF,minXF,maxXF,153)
            histo[startF+154][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes4Up"  ,theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes4Down",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes5Up"  ,theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes5Down",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes6Up"  ,theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfwzbcat[x],"ngood_jetsJes6Down",theCat,startF,x,BinXF,minXF,maxXF,159)
            if(x == plotCategory("kPlotNonPrompt")):
                startNonPrompt = 4
                histoNonPrompt[0+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(0+startNonPrompt), "histoNonPrompt_{0}".format(0+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm0")
                histoNonPrompt[1+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(1+startNonPrompt), "histoNonPrompt_{0}".format(1+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAltm1")
                histoNonPrompt[2+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(2+startNonPrompt), "histoNonPrompt_{0}".format(2+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte0")
                histoNonPrompt[3+startNonPrompt] = dfwzbcat[x].Histo1D(("histoNonPrompt_{0}".format(3+startNonPrompt), "histoNonPrompt_{0}".format(3+startNonPrompt), BinXF,minXF,maxXF), "ngood_jets","weightFakeAlte1")

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
       SwitchSample(sampleNOW,skimType)[2] == plotCategory("kPlotEWKWZ")):
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
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1001_anaType1".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1002_anaType1".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1003_anaType1".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1001_anaType2".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1002_anaType2".format(elSelChoice)))
    histoFakeEtaPt_el.append(fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}_fakeAnalysis1003_anaType2".format(elSelChoice)))
    for x in range(6):
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

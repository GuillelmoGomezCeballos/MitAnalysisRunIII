import ROOT
import os, sys, getopt, json, time

ROOT.ROOT.EnableImplicitMT(4)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection4LVar, selectionTrigger2L, selectionElMu, selectionWeigths, makeFinalVariable

makeDataCards = 2

doNtuples = False
# 0 = T, 1 = M, 2 = L
bTagSel = 0
useBTaggingWeights = 0

useFR = 0

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
TIGHT_MU_TIGHT = jsonObject['TIGHT_MU5']
MUOWP = "Medium"

elSelChoice = 0
FAKE_EL   = jsonObject['FAKE_EL']
TIGHT_EL = jsonObject['TIGHT_EL{0}'.format(elSelChoice)]
TIGHT_EL_TIGHT = jsonObject['TIGHT_EL4']
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

    dftag =(dftag.Filter("nLoose == 4","Only four loose leptons")
                 .Filter("nFake == 4","Four fake leptons")
                 .Filter("abs(Sum(fake_Muon_charge)+Sum(fake_Electron_charge)) == 0", "0 net charge")
                 .Define("vtight_mu","{0}".format(TIGHT_MU_TIGHT))
                 .Define("vtight_el","{0}".format(TIGHT_EL_TIGHT))
                 .Define("eventNum", "event")
                 .Define("ptl1","30.0f")
                 .Define("ptl2","30.0f")
                 .Define("etal1","1.0f")
                 .Define("etal2","1.0f")
                 )

    if(useFR == 0):
        dftag = dftag.Filter("nTight == 4","Four tight leptons")

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData,count,5.0)
    dftag = selection4LVar  (dftag,year,isData)

    dftag = (dftag.Filter("ptlmax{0} > 25".format(altMass), "ptlmax > 25")
		  )
    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 500
    histo    = [[0 for y in range(nCat)] for x in range(nHisto)]

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

    ROOT.gInterpreter.ProcessLine('''
    TMVA::Experimental::RReader model("weights_mva/bdt_BDTG_vbfinc_v0.weights.xml");
    computeModel = TMVA::Experimental::Compute<15, float>(model);
    ''')

    variables = ROOT.model.GetVariableNames()
    print(variables)

    dftag = selectionLL(df,year,PDType,isData,count)

    dfbase = selectionWeigths(dftag,isData,year,PDType,weight,useFR,bTagSel,useBTaggingWeights,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm,MUOWP,ELEWP,"",0)

    dfbase = (dfbase.Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                    .Define("kPlotWS", "{0}".format(plotCategory("kPlotWS")))
                    .Define("theCat","compute_category({0},kPlotNonPrompt,kPlotWS,nFake,nTight,0)".format(theCat))
		    .Define("bdt_vbfinc", ROOT.computeModel, ROOT.model.GetVariableNames())
                    )

    dfzzcatMuonMomUp       = []
    dfzzcatMuonMomDown     = []
    dfzzcatElectronMomUp   = []
    dfzzcatElectronMomDown = []
    dfzzcat = []
    dfzzxycat = []
    dfzzjjcat = []
    dfzzvbscat = []
    for x in range(nCat):
        dfzzcat.append(dfbase.Filter("theCat=={0}".format(x), "correct category ({0})".format(x)))

        histo[ 0][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x),120,  0, 120), "mllmin{0}".format(altMass),"weight")
        dfzzcat[x] = dfzzcat[x].Filter("mllmin{0} > 5".format(altMass),"mllmin cut")

        histo[21][x] = dfzzcat[x].Filter("mllZ1 == -1 && Sum(vtight_mu)+Sum(vtight_el) == 4").Histo1D(("histo_{0}_{1}".format(21,x), "histo_{0}_{1}".format(21,x),3,-0.5, 2.5), "FourLepton_flavor","weight")
        histo[22][x] = dfzzcat[x].Filter("mllZ1 == -1 && Sum(vtight_mu)+Sum(vtight_el) == 4").Histo1D(("histo_{0}_{1}".format(22,x), "histo_{0}_{1}".format(22,x),10, 0, 500), "m4l","weight")
        histo[23][x] = dfzzcat[x].Filter("mllZ1 == -1 && Sum(vtight_mu)+Sum(vtight_el) == 4").Histo1D(("histo_{0}_{1}".format(23,x), "histo_{0}_{1}".format(23,x),5,-0.5 ,4.5), "nbtag_goodbtag_Jet_bjet","weightBTag")

        histo[ 1][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x),100,  0, 100), "mllZ1{0}".format(altMass),"weight")
        dfzzcat[x] = dfzzcat[x].Filter("mllZ1{0} < 10000 && mllZ1{0} > 0".format(altMass),"mllZ1 cut")

        dfzzxycat.append(dfzzcat[x].Filter("mllxy{0} > 0 && Sum(vtight_mu)+Sum(vtight_el) == 4 && mllZ1{0} < 15".format(altMass)))

        histo[ 2][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x),100,  0, 100), "mllZ2{0}".format(altMass),"weight")
        dfzzcat[x] = dfzzcat[x].Filter("mllZ2{0} < 10000".format(altMass),"mllZ2 cut")

        histo[ 3][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x), 40, 10, 210), "ptl1Z1{0}".format(altMass),"weight")
        histo[ 4][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x), 20, 10, 110), "ptl2Z1{0}".format(altMass),"weight")
        histo[ 5][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x), 40, 10, 210), "ptl1Z2{0}".format(altMass),"weight")
        histo[ 6][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x), 20, 10, 110), "ptl2Z2{0}".format(altMass),"weight")
        histo[ 7][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x), 40,150, 550), "m4l{0}".format(altMass),"weight")
        histo[ 8][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x),3,-0.5, 2.5), "FourLepton_flavor","weight")
        histo[ 9][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x), 6,-0.5, 5.5), "ngood_jets","weight")
        histo[10][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 40,  0, 200), "thePuppiMET_pt","weight")

        dfzzjjcat .append(dfzzcat[x] .Filter("nvbs_jets >= 2", "At least two VBS jets"))
        histo[11][x] = dfzzjjcat[x]  .Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 4,1.5, 5.5), "ngood_jets","weight")
        histo[12][x] = dfzzjjcat[x]  .Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 20,0,2000), "vbs_mjj","weight")
        histo[13][x] = dfzzjjcat[x]  .Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 20,0,10), "vbs_detajj","weight")
        histo[14][x] = dfzzjjcat[x]  .Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 20,0,3.1416), "vbs_dphijj","weight")
        histo[15][x] = dfzzjjcat[x]  .Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 20,-1,1), "bdt_vbfinc","weight")

        dfzzvbscat .append(dfzzjjcat[x] .Filter(VBSSEL, "VBS selection"))
        histo[16][x] = dfzzvbscat[x] .Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x), 4,1.5, 5.5), "ngood_jets","weight")
        histo[17][x] = dfzzvbscat[x] .Histo1D(("histo_{0}_{1}".format(17,x), "histo_{0}_{1}".format(17,x), 10,500,2500), "vbs_mjj","weight")
        histo[18][x] = dfzzvbscat[x] .Histo1D(("histo_{0}_{1}".format(18,x), "histo_{0}_{1}".format(18,x), 14,2.5,9.5), "vbs_detajj","weight")
        histo[19][x] = dfzzvbscat[x] .Histo1D(("histo_{0}_{1}".format(19,x), "histo_{0}_{1}".format(19,x), 10,0,3.1416), "vbs_dphijj","weight")
        histo[20][x] = dfzzvbscat[x] .Histo1D(("histo_{0}_{1}".format(20,x), "histo_{0}_{1}".format(20,x), 20,-1,1), "bdt_vbfinc","weight")

        if(doNtuples == True and x == theCat):
            outputFile = "ntupleZZAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob)
            dfzzvbscat[x].Snapshot("events", outputFile, branchList)

        histo[24][x] = dfzzxycat[x].Histo1D(("histo_{0}_{1}".format(24,x), "histo_{0}_{1}".format(24,x),5,-0.5 ,4.5), "nbtag_goodbtag_Jet_bjet","weightBTag")
        histo[25][x] = dfzzxycat[x].Filter("nbtag_goodbtag_Jet_bjet  > 0").Histo1D(("histo_{0}_{1}".format(25,x), "histo_{0}_{1}".format(25,x),20, 0, 500), "m4l","weightBTag")

        dfzzxycat[x] = dfzzxycat[x].Filter("nbtag_goodbtag_Jet_bjet == 0")

        histo[26][x] = dfzzxycat[x].Histo1D(("histo_{0}_{1}".format(26,x), "histo_{0}_{1}".format(26,x),3,-0.5, 2.5), "FourLepton_flavor","weightBTag")
        histo[27][x] = dfzzxycat[x].Histo1D(("histo_{0}_{1}".format(27,x), "histo_{0}_{1}".format(27,x),20, 5, 205), "mllxy{0}".format(altMass),"weightBTag")
        histo[28][x] = dfzzxycat[x].Histo1D(("histo_{0}_{1}".format(28,x), "histo_{0}_{1}".format(28,x),20, 0, 200), "thePuppiMET_pt","weightBTag")
        histo[29][x] = dfzzxycat[x].Histo1D(("histo_{0}_{1}".format(29,x), "histo_{0}_{1}".format(29,x),20, 0, 500), "m4l{0}".format(altMass),"weightBTag")
        histo[30][x] = dfzzxycat[x].Histo1D(("histo_{0}_{1}".format(30,x), "histo_{0}_{1}".format(30,x),20, 0, 200), "ptZ2{0}".format(altMass),"weightBTag")
        histo[31][x] = dfzzxycat[x].Histo1D(("histo_{0}_{1}".format(31,x), "histo_{0}_{1}".format(31,x),20, 0, 200), "mtxy{0}".format(altMass),"weightBTag")

        histo[91][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format(91,x), "histo_{0}_{1}".format(91,x),3,-0.5, 2.5), "FourLepton_flavor","weight3")
        histo[92][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format(92,x), "histo_{0}_{1}".format(92,x),3,-0.5, 2.5), "FourLepton_flavor","weight4")
        histo[93][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format(93,x), "histo_{0}_{1}".format(93,x),3,-0.5, 2.5), "FourLepton_flavor","weightBTag")
        histo[94][x] = dfzzcat[x].Histo1D(("histo_{0}_{1}".format(94,x), "histo_{0}_{1}".format(94,x),3,-0.5, 2.5), "FourLepton_flavor","weightNoBTag")

        if(makeDataCards == 1):
            dfzzcatMuonMomUp      .append(dfzzcat[x])
            dfzzcatMuonMomDown    .append(dfzzcat[x])
            dfzzcatElectronMomUp  .append(dfzzcat[x])
            dfzzcatElectronMomDown.append(dfzzcat[x])
            dfzzcat		  [x] = dfzzcat 	      [x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4l{0}             > 150".format(altMass)," nbjets == 0 && m4l > 150")
            dfzzcatMuonMomUp	  [x] = dfzzcatMuonMomUp      [x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4lMuonMomUp       > 150")
            dfzzcatMuonMomDown    [x] = dfzzcatMuonMomDown    [x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4lMuonMomDown     > 150")
            dfzzcatElectronMomUp  [x] = dfzzcatElectronMomUp  [x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4lElectronMomUp   > 150")
            dfzzcatElectronMomDown[x] = dfzzcatElectronMomDown[x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4lElectronMomDown > 150")
            BinXF = 4
            minXF = -0.5
            maxXF = 3.5

            startF = 300
            for nv in range(0,154):
                histo[startF+nv][x] = makeFinalVariable(dfzzcat[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+154][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes0Up"  ,theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes0Down",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfzzcat[x]	  ,"ngood_jetsJerUp"  ,theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfzzcat[x]	  ,"ngood_jetsJerDown",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfzzcatMuonMomUp      [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfzzcatMuonMomDown    [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfzzcatElectronMomUp  [x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfzzcatElectronMomDown[x],"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfzzcat[x]		 ,"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfzzcat[x]		 ,"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfzzcat[x]		 ,"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfzzcat[x]		 ,"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfzzcat[x]		 ,"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfzzcat[x]		 ,"ngood_jets",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes1Up"  ,theCat,startF,x,BinXF,minXF,maxXF,168)
            histo[startF+169][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes1Down",theCat,startF,x,BinXF,minXF,maxXF,169)
            histo[startF+170][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes2Up"  ,theCat,startF,x,BinXF,minXF,maxXF,170)
            histo[startF+171][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes2Down",theCat,startF,x,BinXF,minXF,maxXF,171)
            histo[startF+172][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes3Up"  ,theCat,startF,x,BinXF,minXF,maxXF,172)
            histo[startF+173][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes3Down",theCat,startF,x,BinXF,minXF,maxXF,173)
            histo[startF+174][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes4Up"  ,theCat,startF,x,BinXF,minXF,maxXF,174)
            histo[startF+175][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes4Down",theCat,startF,x,BinXF,minXF,maxXF,175)
            histo[startF+176][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes5Up"  ,theCat,startF,x,BinXF,minXF,maxXF,176)
            histo[startF+177][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes5Down",theCat,startF,x,BinXF,minXF,maxXF,177)
            histo[startF+178][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes6Up"  ,theCat,startF,x,BinXF,minXF,maxXF,178)
            histo[startF+179][x]    = makeFinalVariable(dfzzcat[x]	 ,"ngood_jetsJes6Down",theCat,startF,x,BinXF,minXF,maxXF,179)

        elif(makeDataCards == 2):
            dfzzcatMuonMomUp      .append(dfzzcat[x])
            dfzzcatMuonMomDown    .append(dfzzcat[x])
            dfzzcatElectronMomUp  .append(dfzzcat[x])
            dfzzcatElectronMomDown.append(dfzzcat[x])
            dfzzcat		  [x] = dfzzcat 	      [x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4l{0}             > 150".format(altMass)," nbjets == 0 && m4l > 150")
            dfzzcatMuonMomUp	  [x] = dfzzcatMuonMomUp      [x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4lMuonMomUp       > 150")
            dfzzcatMuonMomDown    [x] = dfzzcatMuonMomDown    [x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4lMuonMomDown     > 150")
            dfzzcatElectronMomUp  [x] = dfzzcatElectronMomUp  [x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4lElectronMomUp   > 150")
            dfzzcatElectronMomDown[x] = dfzzcatElectronMomDown[x].Filter("nbtag_goodbtag_Jet_bjet == 0 && m4lElectronMomDown > 150")
            BinXF = 3
            minXF = -0.5
            maxXF = 2.5

            startF = 300
            for nv in range(0,154):
                histo[startF+nv][x] = makeFinalVariable(dfzzcat[x],"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,nv)
            histo[startF+154][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,154)
            histo[startF+155][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,155)
            histo[startF+156][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,156)
            histo[startF+157][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,157)
            histo[startF+158][x]    = makeFinalVariable(dfzzcatMuonMomUp      [x],"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,158)
            histo[startF+159][x]    = makeFinalVariable(dfzzcatMuonMomDown    [x],"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,159)
            histo[startF+160][x]    = makeFinalVariable(dfzzcatElectronMomUp  [x],"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,160)
            histo[startF+161][x]    = makeFinalVariable(dfzzcatElectronMomDown[x],"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,161)
            histo[startF+162][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,162)
            histo[startF+163][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,163)
            histo[startF+164][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,164)
            histo[startF+165][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,165)
            histo[startF+166][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,166)
            histo[startF+167][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,167)
            histo[startF+168][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,168)
            histo[startF+169][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,169)
            histo[startF+170][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,170)
            histo[startF+171][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,171)
            histo[startF+172][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,172)
            histo[startF+173][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,173)
            histo[startF+174][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,174)
            histo[startF+175][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,175)
            histo[startF+176][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,176)
            histo[startF+177][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,177)
            histo[startF+178][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,178)
            histo[startF+179][x]    = makeFinalVariable(dfzzcat[x]		 ,"FourLepton_flavor",theCat,startF,x,BinXF,minXF,maxXF,179)

    report = []
    for x in range(nCat):
        report.append(dfzzvbscat[x].Report())
        if(x != theCat): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    myfile = ROOT.TFile("fillhisto_zzAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].Write()
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

    lepSFPath = "data/histoLepSFEtaPt_{0}.root".format(year)
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

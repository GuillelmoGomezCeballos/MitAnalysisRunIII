import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(4)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection2LVar, selectionTrigger2L, selectionElMu, selectionWeigths
#from utilsAna import loadCorrectionSet

# 0 = T, 1 = M, 2 = L
bTagSel = 2
useBTaggingWeights = 1

useFR = 1

altMass = "Def"

selectionJsonPath = "config/selection.json"

with open(selectionJsonPath) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

JSON = jsonObject['JSON']

BARRELphotons = jsonObject['BARRELphotons']
ENDCAPphotons = jsonObject['ENDCAPphotons']

VBSSEL = jsonObject['VBSSEL']

muSelChoice = 5
FAKE_MU   = jsonObject['FAKE_MU']
TIGHT_MU = jsonObject['TIGHT_MU{0}'.format(muSelChoice)]

elSelChoice = 4
FAKE_EL   = jsonObject['FAKE_EL']
TIGHT_EL = jsonObject['TIGHT_EL{0}'.format(elSelChoice)]

def selectionLL(df,year,PDType,isData,TRIGGERMUEG,TRIGGERDMU,TRIGGERSMU,TRIGGERDEL,TRIGGERSEL,count):

    dftag = selectionTrigger2L(df,year,PDType,JSON,isData,TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU,FAKE_EL,TIGHT_EL)

    dftag = (dftag.Filter("nLoose >= 2","At least two loose leptons")
                  .Filter("nLoose == 2","Only two loose leptons")
                  .Filter("nFake == 2","Two fake leptons")

                  .Filter("Sum(fake_mu) == 1 && Sum(fake_el) == 1","e-mu events")

                  )

    global useFR
    if(year == 2023): useFR = 0
    if(useFR == 0):
        dftag = dftag.Filter("nTight == 2","Two tight leptons")

    dftag = selection2LVar  (dftag,year,isData)
                  
    dftag = dftag.Filter("mll > 20 && ptl1 > 25 && ptl2 > 20","mll > 20 && ptl1 > 25 && ptl2 > 20")

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData,count)

    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob,nPDFReplicas,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    xPtbins = array('d', [10,15,20,25,30,35,40,50,60,70,85,100,200,1000])
    xEtabins = array('d', [0.0,1.0,1.5,2.0,2.5])

    xPtTrgbins = array('d', [25,30,35,40,45,50,55,60,65,70,75,80,90,105,120,150,200])

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 500
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
    ROOT.initHisto2F(histoElRecoSF,0)
    ROOT.initHisto2F(histoElSelSF,1)
    ROOT.initHisto2F(histoMuIDSF,2)
    ROOT.initHisto2F(histoMuISOSF,3)
    ROOT.initHisto1D(puWeights,0)
    ROOT.initHisto2D(histoBTVEffEtaPtLF,20)
    ROOT.initHisto2D(histoBTVEffEtaPtCJ,21)
    ROOT.initHisto2D(histoBTVEffEtaPtBJ,22)

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
    dfbase = selectionWeigths(dfbase,isData,year,PDType,weight,useFR,bTagSel,useBTaggingWeights,nPDFReplicas)

    overallMETFilters = jsonObject['met_filters']
    METFILTERS = getTriggerFromJson(overallMETFilters, "All", year)
    dfbase = dfbase.Define("METFILTERS", "{0}".format(METFILTERS)).Filter("METFILTERS > 0","METFILTERS > 0")

    dfcat = []
    dfssxcat = []
    dfwwxcat = []
    dfzttcat = []
    dftopcat = []
    for x in range(nCat):
        dfcat.append(dfbase.Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
        		   .Define("theCat{0}".format(x), "compute_category({0},kPlotNonPrompt,nFake,nTight)".format(theCat))
        		   .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x))
        		   )

        if(x == plotCategory("kPlotTop")):
            dfcat[x] = dfcat[x].Define("weightWW", "weight*0.90")
        else:
            dfcat[x] = dfcat[x].Define("weightWW", "weight")

        dfssxcat.append(dfcat[x].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) != 0", "Same-sign leptons"))

        histo[ 0][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x), 60, 20, 320), "mll","weightWW")
        histo[ 1][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x), 50,  0, 200), "ptll","weightWW")
        histo[ 2][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjet","weightWW")

        dfcat[x] = dfcat[x].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) == 0", "Opposite-sign leptons")

        histo[ 3][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x), 60, 20, 320), "mll","weightWW")
        histo[ 4][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x), 50,  0, 200), "ptll","weightWW")
        histo[ 5][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x), 5,-0.5,4.5), "nbtag_goodbtag_Jet_bjet","weightWW")

        dfwwxcat.append(dfcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0", "No b-jets")
                                .Filter("ptll > 30", "ptll > 30")
                                )

        dfzttcat.append(dfcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0", "No b-jets")
                                .Filter("ptll <= 30 && mll < 90", "ptll <= 30 && mll < 90")
                                )

        dftopcat.append(dfcat[x].Filter("nbtag_goodbtag_Jet_bjet != 0", "b-jets")
                                .Filter("ptll > 30", "ptll > 30")
                                )

        histo[38][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(38,x), "histo_{0}_{1}".format(38,x), 50,  0, 3.1416), "dPhilMETMin","weightWW")
        histo[39][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(39,x), "histo_{0}_{1}".format(39,x), 50,  0, 3.1416), "dPhilMETMin","weightWW")
        histo[40][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(40,x), "histo_{0}_{1}".format(40,x), 50,  0, 3.1416), "dPhilMETMin","weightWW")
        histo[41][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(41,x), "histo_{0}_{1}".format(41,x), 50,  0, 3.1416), "dPhilMETMin","weightWW")

        histo[42][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(42,x), "histo_{0}_{1}".format(42,x), 100, 0, 200), "minPMET","weightWW")
        histo[43][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(43,x), "histo_{0}_{1}".format(43,x), 100, 0, 200), "minPMET","weightWW")
        histo[44][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(44,x), "histo_{0}_{1}".format(44,x), 100, 0, 200), "minPMET","weightWW")
        histo[45][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(45,x), "histo_{0}_{1}".format(45,x), 100, 0, 200), "minPMET","weightWW")

        histo[34][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(34,x), "histo_{0}_{1}".format(34,x), 100, 0, 200), "PuppiMET_pt","weightWW")
        histo[35][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(35,x), "histo_{0}_{1}".format(35,x), 100, 0, 200), "PuppiMET_pt","weightWW")
        histo[36][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(36,x), "histo_{0}_{1}".format(36,x), 100, 0, 200), "PuppiMET_pt","weightWW")
        histo[37][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(37,x), "histo_{0}_{1}".format(37,x), 100, 0, 200), "PuppiMET_pt","weightWW")

        dfssxcat[x] = dfssxcat[x].Filter("minPMET > 20", "minPMET > 20")
        dfwwxcat[x] = dfwwxcat[x].Filter("minPMET > 20", "minPMET > 20")
        #dfzttcat[x] = dfzttcat[x].Filter("minPMET > 20", "minPMET > 20")
        dftopcat[x] = dftopcat[x].Filter("minPMET > 20", "minPMET > 20")

        histo[ 6][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x), 50,  0, 5), "drll","weightWW")
        histo[ 7][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x), 50,  0, 5), "drll","weightWW")
        histo[ 8][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x), 50,  0, 5), "drll","weightWW")
        histo[ 9][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x), 50,  0, 5), "drll","weightWW")

        histo[10][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 50,  0, 3.1416), "dphill","weightWW")
        histo[11][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 50,  0, 3.1416), "dphill","weightWW")
        histo[12][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 50,  0, 3.1416), "dphill","weightWW")
        histo[13][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 50,  0, 3.1416), "dphill","weightWW")

        histo[14][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 40, 25, 225), "ptl1","weightWW")
        histo[15][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 40, 25, 225), "ptl1","weightWW")
        histo[16][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x), 40, 25, 225), "ptl1","weightWW")
        histo[17][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(17,x), "histo_{0}_{1}".format(17,x), 40, 25, 225), "ptl1","weightWW")

        histo[18][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(18,x), "histo_{0}_{1}".format(18,x), 40, 20, 220), "ptl2","weightWW")
        histo[19][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(19,x), "histo_{0}_{1}".format(19,x), 40, 20, 220), "ptl2","weightWW")
        histo[20][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(20,x), "histo_{0}_{1}".format(20,x), 40, 20, 220), "ptl2","weightWW")
        histo[21][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(21,x), "histo_{0}_{1}".format(21,x), 40, 20, 220), "ptl2","weightWW")

        histo[22][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(22,x), "histo_{0}_{1}".format(22,x), 25,  0,2.5), "etal1","weightWW")
        histo[23][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(23,x), "histo_{0}_{1}".format(23,x), 25,  0,2.5), "etal1","weightWW")
        histo[24][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(24,x), "histo_{0}_{1}".format(24,x), 25,  0,2.5), "etal1","weightWW")
        histo[25][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(25,x), "histo_{0}_{1}".format(25,x), 25,  0,2.5), "etal1","weightWW")

        histo[26][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(26,x), "histo_{0}_{1}".format(26,x), 25,  0,2.5), "etal2","weightWW")
        histo[27][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(27,x), "histo_{0}_{1}".format(27,x), 25,  0,2.5), "etal2","weightWW")
        histo[28][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(28,x), "histo_{0}_{1}".format(28,x), 25,  0,2.5), "etal2","weightWW")
        histo[29][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(29,x), "histo_{0}_{1}".format(29,x), 25,  0,2.5), "etal2","weightWW")

        histo[30][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(30,x), "histo_{0}_{1}".format(30,x), 6,-0.5,5.5), "ngood_jets","weightWW")
        histo[31][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(31,x), "histo_{0}_{1}".format(31,x), 6,-0.5,5.5), "ngood_jets","weightWW")
        histo[32][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(32,x), "histo_{0}_{1}".format(32,x), 6,-0.5,5.5), "ngood_jets","weightWW")
        histo[33][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(33,x), "histo_{0}_{1}".format(33,x), 6,-0.5,5.5), "ngood_jets","weightWW")

        histo[46][x] = dfssxcat[x].Histo1D(("histo_{0}_{1}".format(46,x), "histo_{0}_{1}".format(46,x), 60, 20, 320), "mll","weightWW")
        histo[47][x] = dfwwxcat[x].Histo1D(("histo_{0}_{1}".format(47,x), "histo_{0}_{1}".format(47,x), 60, 20, 320), "mll","weightWW")
        histo[48][x] = dfzttcat[x].Histo1D(("histo_{0}_{1}".format(48,x), "histo_{0}_{1}".format(48,x), 35, 20,  90), "mll","weightWW")
        histo[49][x] = dftopcat[x].Histo1D(("histo_{0}_{1}".format(49,x), "histo_{0}_{1}".format(49,x), 60, 20, 320), "mll","weightWW")

    report = []
    for x in range(nCat):
        report.append(dfwwxcat[x].Report())
        if(x != theCat): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    #for i in range(nCat):
    #    if(histo[5][i].GetSumOfWeights() != 0): print("AAA({0}) {1}".format(i,histo[5][i].GetSumOfWeights()))
    myfile = ROOT.TFile("fillhisto_wwAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].Write()
        for j in range(nHisto):
            if(histo2D[j][i] == 0): continue
            #if(histo2D[j][i].GetSumOfWeights() > 0): print("({0},{1}): {2}".format(j,i,histo2D[j][i].GetSumOfWeights()))
            histo2D[j][i].Write()
    myfile.Close()

def readMCSample(sampleNOW,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    files = getMClist(sampleNOW, skimType)
    print("Total files: {0}".format(len(files)))

    runTree = ROOT.TChain("Runs")
    for f in range(len(files)):
        runTree.AddFile(files[f])

    genEventSumWeight = 0
    genEventSumNoWeight = 0
    nPDFReplicas = 0
    for i in range(runTree.GetEntries()):
        runTree.GetEntry(i)
        genEventSumWeight += runTree.genEventSumw
        genEventSumNoWeight += runTree.genEventCount
        if(i == 0 and runTree.FindBranch("nLHEPdfSumw")):
            nPDFReplicas = runTree.nLHEPdfSumw
    print("Number of PDF replicas: {0}".format(nPDFReplicas))

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

    analysis(df,sampleNOW,SwitchSample(sampleNOW,skimType)[2],weight,year,PDType,"false",whichJob,nPDFReplicas,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

def readDASample(sampleNOW,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

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

    weight=1.
    nevents = df.Count().GetValue()
    print("%s entries in the dataset" %nevents)

    analysis(df,sampleNOW,sampleNOW,weight,year,PDType,"true",whichJob,0,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)

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

    puPath = "data/puWeights_UL_{0}.root".format(year)
    fPuFile = ROOT.TFile(puPath)
    puWeights = fPuFile.Get("puWeights")
    puWeights.SetDirectory(0)
    fPuFile.Close()

    recoElPath = "data/electronReco_UL_{0}.root".format(year)
    fRecoElFile = ROOT.TFile(recoElPath)
    histoElRecoSF = fRecoElFile.Get("EGamma_SF2D")
    histoElRecoSF.SetDirectory(0)
    fRecoElFile.Close()

    selElPath = "data/electronMediumID_UL_{0}.root".format(year)
    fSelElFile = ROOT.TFile(selElPath)
    histoElSelSF = fSelElFile.Get("EGamma_SF2D")
    histoElSelSF.SetDirectory(0)
    fSelElFile.Close()

    idMuPath = "data/Efficiencies_muon_generalTracks_Z_Run{0}_UL_ID.root".format(year)
    fidMuFile = ROOT.TFile(idMuPath)
    histoMuIDSF = fidMuFile.Get("NUM_MediumID_DEN_TrackerMuons_abseta_pt")
    histoMuIDSF.SetDirectory(0)
    fidMuFile.Close()

    isoMuPath = "data/Efficiencies_muon_generalTracks_Z_Run{0}_UL_ISO.root".format(year)
    fisoMuFile = ROOT.TFile(isoMuPath)
    histoMuISOSF = fisoMuFile.Get("NUM_TightRelIso_DEN_MediumID_abseta_pt")
    histoMuISOSF.SetDirectory(0)
    fisoMuFile.Close()

    fakePath = "data/histoFakeEtaPt_{0}_anaType3.root".format(year)
    fFakeFile = ROOT.TFile(fakePath)
    histoFakeEtaPt_mu = fFakeFile.Get("histoFakeEffSelEtaPt_0_{0}".format(muSelChoice))
    histoFakeEtaPt_el = fFakeFile.Get("histoFakeEffSelEtaPt_1_{0}".format(elSelChoice))
    histoFakeEtaPt_mu.SetDirectory(0)
    histoFakeEtaPt_el.SetDirectory(0)
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
        elif(process >= 1000):
            readDASample(process,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
    except Exception as e:
        print("Error sample: {0}".format(e))

import ROOT
import os, sys, getopt, json

ROOT.ROOT.EnableImplicitMT(3)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection2LVar, selectionTrigger2L, selectionElMu, selectionWeigths, makeFinalVariable

doNtuples = False
# 0 = T, 1 = M, 2 = L
bTagSel = 0
useBTaggingWeights = 1

useFR = 1

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

    dftag = selectionTrigger2L(df,year,PDType,JSON,isData,TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU6,FAKE_EL,TIGHT_EL7)

    dftag =(dftag.Filter("nLoose == 2","Only two loose leptons")
                 .Filter("nFake == 2","Two fake leptons")
                 .Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) != 0", "Sign-sign leptons")
                #.Filter("nTight == 2","Two tight leptons")
                 .Define("eventNum", "event")
                 )

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData)
    dftag = selection2LVar  (dftag,year)

    dftag = (dftag.Filter("ptl1 > 25 && ptl2 > 20","ptl1 > 25 && ptl2 > 20")
                  .Filter("mll > 20","mll > 20 GeV")
		  )

    return dftag

def analysis(df,count,category,weight,year,PDType,isData,whichJob,nPDFReplicas,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 500
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


    dftag = selectionLL(df,year,PDType,isData)

    dfbase = selectionWeigths(dftag,isData,year,PDType,weight,useFR,bTagSel,useBTaggingWeights,nPDFReplicas)

    dfbase = (dfbase.Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                    .Define("theCat","compute_category({0},kPlotNonPrompt,nFake,nTight)".format(theCat))
		    .Define("bdt_vbfinc", ROOT.computeModel, ROOT.model.GetVariableNames())
                    )
    dfwwcat = []
    dfwwbcat = []
    dfwwvbscat = []
    dfwwbvbscat = []
    for x in range(nCat):
        dfwwcat.append(dfbase.Filter("theCat=={0}".format(x), "correct category ({0})".format(x)))

        histo[ 0][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x),40, 20, 220), "mll","weightNoBTag")
        dfwwcat[x] = dfwwcat[x].Filter("DiLepton_flavor != 2 || abs(mll-91.1876) > 15","Z veto")

        dfwwbcat.append(dfwwcat[x].Filter("nbtag_goodbtag_Jet_bjet > 0","at least one good b-jets"))

        histo[ 1][x] = dfwwcat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x), 5,-0.5 ,4.5),     "nbtag_goodbtag_Jet_bjet","weight")
        dfwwcat[x] = dfwwcat[x].Filter("nbtag_goodbtag_Jet_bjet == 0","no good b-jets")

        histo[ 2][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x),100,  0, 200), "MET_pt","weight")
        histo[ 3][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x),100,  0, 200), "MET_pt","weight")
        histo[ 4][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x), 3,-0.5, 2.5), "DiLepton_flavor","weight")
        histo[ 5][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x), 3,-0.5, 2.5), "DiLepton_flavor","weight")
        histo[ 6][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x), 6,-0.5, 5.5), "ngood_jets","weight")
        histo[ 7][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x), 6,-0.5, 5.5), "ngood_jets","weight")

        dfwwcat[x]  = dfwwcat[x] .Filter("nvbs_jets >= 2", "At least two VBS jets")
        dfwwbcat[x] = dfwwbcat[x].Filter("nvbs_jets >= 2", "At least two VBS jets")
        histo[ 8][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x), 4,-0.5, 3.5), "ltype","weight")
        histo[ 9][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x), 4,-0.5, 3.5), "ltype","weight")
        histo[10][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[11][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[12][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 40,0,2000), "vbs_mjj","weight")
        histo[13][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 40,0,2000), "vbs_mjj","weight")
        histo[14][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 40,0,10), "vbs_detajj","weight")
        histo[15][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 40,0,10), "vbs_detajj","weight")
        histo[16][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x), 40,0,3.1416), "vbs_dphijj","weight")
        histo[17][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format(17,x), "histo_{0}_{1}".format(17,x), 40,0,3.1416), "vbs_dphijj","weight")
        histo[18][x] = dfwwcat[x] .Histo1D(("histo_{0}_{1}".format(18,x), "histo_{0}_{1}".format(18,x), 20,-1,1), "bdt_vbfinc","weight")
        histo[19][x] = dfwwbcat[x].Histo1D(("histo_{0}_{1}".format(19,x), "histo_{0}_{1}".format(19,x), 20,-1,1), "bdt_vbfinc","weight")

        dfwwvbscat .append(dfwwcat[x] .Filter(VBSSEL, "VBS selection"))
        dfwwbvbscat.append(dfwwbcat[x].Filter(VBSSEL, "VBS selection"))
        histo[20][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(20,x), "histo_{0}_{1}".format(20,x), 4,-0.5, 3.5), "ltype","weight")
        histo[21][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(21,x), "histo_{0}_{1}".format(21,x), 4,-0.5, 3.5), "ltype","weight")
        histo[22][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(22,x), "histo_{0}_{1}".format(22,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[23][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(23,x), "histo_{0}_{1}".format(23,x), 4, 1.5, 5.5), "ngood_jets","weight")
        histo[24][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(24,x), "histo_{0}_{1}".format(24,x), 10,500,2500), "vbs_mjj","weight")
        histo[25][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(25,x), "histo_{0}_{1}".format(25,x), 10,500,2500), "vbs_mjj","weight")
        histo[26][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(26,x), "histo_{0}_{1}".format(26,x), 14,2.5,9.5), "vbs_detajj","weight")
        histo[27][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(27,x), "histo_{0}_{1}".format(27,x), 14,2.5,9.5), "vbs_detajj","weight")
        histo[28][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(28,x), "histo_{0}_{1}".format(28,x), 10,0,3.1416), "vbs_dphijj","weight")
        histo[29][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(29,x), "histo_{0}_{1}".format(29,x), 10,0,3.1416), "vbs_dphijj","weight")
        histo[30][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(30,x), "histo_{0}_{1}".format(30,x), 10,0,1), "vbs_zepvv","weight")
        histo[31][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(31,x), "histo_{0}_{1}".format(31,x), 10,0,1), "vbs_zepvv","weight")
        histo[32][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(32,x), "histo_{0}_{1}".format(32,x), 20,-1,1), "bdt_vbfinc","weight")
        histo[33][x] = dfwwbvbscat[x].Histo1D(("histo_{0}_{1}".format(33,x), "histo_{0}_{1}".format(33,x), 20,-1,1), "bdt_vbfinc","weight")

        if(doNtuples == True and x == theCat):
            outputFile = "ntupleSSWWAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob)
            dfwwvbscat[x].Snapshot("events", outputFile, branchList)

        #histo[92][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(92,x), "histo_{0}_{1}".format(92,x), 4,-0.5, 3.5), "ltype","weightNoPURecoSF")
        #histo[93][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(93,x), "histo_{0}_{1}".format(93,x), 4,-0.5, 3.5), "ltype","weightNoLepSF")
        #histo[94][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(94,x), "histo_{0}_{1}".format(94,x), 4,-0.5, 3.5), "ltype","weightNoTriggerSF")
        #histo[95][x] = dfwwvbscat[x] .Histo1D(("histo_{0}_{1}".format(95,x), "histo_{0}_{1}".format(95,x), 4,-0.5, 3.5), "ltype","weightNoBTVSF")

        startF = 300
        BinF = 50
        minF = 500
        maxF = 2500
        histo[startF+0][x] = makeFinalVariable(dfwwvbscat[x],"vbs_mjj",startF,x,BinF,minF,maxF,0)
        if(isData == False):
            for nv in range(1,129):
                histo[startF+nv][x] = makeFinalVariable(dfwwvbscat[x],"vbs_mjj",startF,x,BinF,minF,maxF,nv)
            histo[startF+129][x]    = makeFinalVariable(dfwwvbscat[x],"vbs_mjjJesUp"  ,startF,x,BinF,minF,maxF,129)
            histo[startF+130][x]    = makeFinalVariable(dfwwvbscat[x],"vbs_mjjJesDown",startF,x,BinF,minF,maxF,130)
            histo[startF+131][x]    = makeFinalVariable(dfwwvbscat[x],"vbs_mjjJerUp"  ,startF,x,BinF,minF,maxF,131)
            histo[startF+132][x]    = makeFinalVariable(dfwwvbscat[x],"vbs_mjjJerDown",startF,x,BinF,minF,maxF,132)

    report = []
    for x in range(nCat):
        report.append(dfwwvbscat[x].Report())
        if(x != theCat and x != plotCategory("kPlotNonPrompt")): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    myfile = ROOT.TFile("fillhisto_sswwAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].Write()
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
    if  (sampleNOW >= 1001 and sampleNOW <= 1004): PDType = "SingleMuon"
    elif(sampleNOW >= 1005 and sampleNOW <= 1008): PDType = "DoubleMuon"
    elif(sampleNOW >= 1009 and sampleNOW <= 1012): PDType = "MuonEG"
    elif(sampleNOW >= 1013 and sampleNOW <= 1016): PDType = "EGamma"
    elif(sampleNOW >= 1017 and sampleNOW <= 1020): PDType = "Muon"
    elif(sampleNOW >= 1021 and sampleNOW <= 1024): PDType = "MET"

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
    histoFakeEtaPt_mu = fFakeFile.Get("histoFakeEffSelEtaPt_0_6")
    histoFakeEtaPt_el = fFakeFile.Get("histoFakeEffSelEtaPt_1_7")
    histoFakeEtaPt_mu.SetDirectory(0)
    histoFakeEtaPt_el.SetDirectory(0)
    fFakeFile.Close()

    lepSFPath = "data/histoLepSFEtaPt_{0}.root".format(year)
    if(not os.path.exists(lepSFPath)):
        lepSFPath = "histoLepSFEtaPt_{0}.root".format(year)
    fLepSFFile = ROOT.TFile(lepSFPath)
    histoLepSFEtaPt_mu = fLepSFFile.Get("histoLepSFEtaPt_0_6")
    histoLepSFEtaPt_el = fLepSFFile.Get("histoLepSFEtaPt_1_7")
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

import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(4)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionJetMet, selectionElMu, selectionTrigger1L

# 0 = T, 1 = M, 2 = L
bTagSel = 1

useFR = 1

selectionJsonPath = "config/selection.json"

with open(selectionJsonPath) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

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
TIGHT_MU8 = jsonObject['TIGHT_MU8']

FAKE_EL   = jsonObject['FAKE_EL']
TIGHT_EL0 = jsonObject['TIGHT_EL0']
TIGHT_EL1 = jsonObject['TIGHT_EL1']
TIGHT_EL2 = jsonObject['TIGHT_EL2']
TIGHT_EL3 = jsonObject['TIGHT_EL3']
TIGHT_EL4 = jsonObject['TIGHT_EL4']
TIGHT_EL5 = jsonObject['TIGHT_EL5']
TIGHT_EL6 = jsonObject['TIGHT_EL6']
TIGHT_EL7 = jsonObject['TIGHT_EL7']
TIGHT_EL8 = jsonObject['TIGHT_EL8']

def selection1L(df,year,PDType,isData,TRIGGERFAKEMU,TRIGGERFAKEEL,count):

    dftag = selectionTrigger1L(df,year,PDType,JSON,isData,TRIGGERFAKEMU,TRIGGERFAKEEL)

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU0,FAKE_EL,TIGHT_EL0)

    dftag =(dftag.Filter("nLoose == 1","Only one loose lepton")
                 .Filter("nFake == 1","Only one fake lepton")
                 .Define("tight_mu0", "{0}".format(TIGHT_MU0))
                 .Define("tight_mu1", "{0}".format(TIGHT_MU1))
                 .Define("tight_mu2", "{0}".format(TIGHT_MU2))
                 .Define("tight_mu3", "{0}".format(TIGHT_MU3))
                 .Define("tight_mu4", "{0}".format(TIGHT_MU4))
                 .Define("tight_mu5", "{0}".format(TIGHT_MU5))
                 .Define("tight_mu6", "{0}".format(TIGHT_MU6))
                 .Define("tight_mu7", "{0}".format(TIGHT_MU7))
                 .Define("tight_mu8", "{0}".format(TIGHT_MU8))
                 .Define("tight_el0", "{0}".format(TIGHT_EL0))
                 .Define("tight_el1", "{0}".format(TIGHT_EL1))
                 .Define("tight_el2", "{0}".format(TIGHT_EL2))
                 .Define("tight_el3", "{0}".format(TIGHT_EL3))
                 .Define("tight_el4", "{0}".format(TIGHT_EL4))
                 .Define("tight_el5", "{0}".format(TIGHT_EL5))
                 .Define("tight_el6", "{0}".format(TIGHT_EL6))
                 .Define("tight_el7", "{0}".format(TIGHT_EL7))
                 .Define("tight_el8", "{0}".format(TIGHT_EL8))
                 .Define("mt"      ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, PuppiMET_pt, PuppiMET_phi,0)")
                 .Define("dphilmet","compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, PuppiMET_pt, PuppiMET_phi,1)")
                 .Define("mtfix"   ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, PuppiMET_pt, PuppiMET_phi,2)")
                 .Define("ptl"     ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, PuppiMET_pt, PuppiMET_phi,3)")
                 .Define("etal"    ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, PuppiMET_pt, PuppiMET_phi,4)")
                 .Define("phil"    ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, PuppiMET_pt, PuppiMET_phi,5)")
                 .Define("absetal" ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, PuppiMET_pt, PuppiMET_phi,6)")
                 .Define("ptlcone" ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, PuppiMET_pt, PuppiMET_phi,7)")
                 .Define("sumMETMT","PuppiMET_pt+mt")
                )

    dftag = selectionJetMet(dftag,year,bTagSel,isData,count,5.0)

    return dftag

def analysis(df,count,category,weight,year,PDType,isData,whichJob,puWeights):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    xPtBins = array('d', [10.0, 15.0, 20.0, 25.0, 30.0, 40.0])
    xEtaBins = array('d', [0.0, 0.5, 1.0, 1.5, 2.0, 2.5])

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    sumMETMTCut = 50

    nCat, nHisto = plotCategory("kPlotCategories"), 500
    histo   = [[0 for y in range(nCat)] for x in range(nHisto)]
    histo2D = [[0 for y in range(nCat)] for x in range(nHisto)]

    ROOT.initHisto1D(puWeights,0)

    ROOT.initJSONSFs(year)

    overallTriggers = jsonObject['triggers']
    TRIGGERFAKEMU = getTriggerFromJson(overallTriggers, "TRIGGERFAKEMU", year)
    TRIGGERFAKEEL = getTriggerFromJson(overallTriggers, "TRIGGERFAKEEL", year)

    list_TRIGGERFAKEMU = TRIGGERFAKEMU.split('(')[1].split(')')[0].split('||')
    list_TRIGGERFAKEEL = TRIGGERFAKEEL.split('(')[1].split(')')[0].split('||')
    list_TRIGGERFAKE = list_TRIGGERFAKEMU
    list_TRIGGERFAKE.extend(list_TRIGGERFAKEEL)
    print("Total number of fake trigger paths: {0}".format(len(list_TRIGGERFAKE)))

    dfbase = selection1L(df,year,PDType,isData,TRIGGERFAKEMU,TRIGGERFAKEEL,count)

    if(theCat == plotCategory("kPlotData")):
        dfbase = (dfbase.Define("weight","1.0")
                        .Define("weightFakeSel0", "1.0")
                        .Define("weightFakeSel1", "1.0")
                        .Define("weightFakeSel2", "1.0")
                        )
    elif(theCat == plotCategory("kPlotNonPrompt")):
        dfbase =(dfbase.Define("PDType","\"{0}\"".format(PDType))
                       .Define("fake_Muon_genPartFlav","Muon_genPartFlav[fake_mu]")
                       .Define("fake_Electron_genPartFlav","Electron_genPartFlav[fake_el]")
                       .Define("weightPURecoSF","compute_PURecoSF(fake_Muon_pt,fake_Muon_eta,fake_Electron_pt,fake_Electron_eta,Pileup_nTrueInt,0)")
                       .Define("weight","compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,-1)*weightPURecoSF".format(weight,0))
                       .Filter("weight != 0","good weight")
                       .Define("weightFakeSel0", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,0)*weightPURecoSF".format(weight,0))
                       .Define("weightFakeSel1", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,1)*weightPURecoSF".format(weight,0))
                       .Define("weightFakeSel2", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,2)*weightPURecoSF".format(weight,0))
                       )
    else:
        dfbase =(dfbase.Define("PDType","\"{0}\"".format(PDType))
                       .Define("fake_Muon_genPartFlav","Muon_genPartFlav[fake_mu]")
                       .Define("fake_Electron_genPartFlav","Electron_genPartFlav[fake_el]")
                       .Define("weightPURecoSF","compute_PURecoSF(fake_Muon_pt,fake_Muon_eta,fake_Electron_pt,fake_Electron_eta,Pileup_nTrueInt,0)")
                       .Define("weight","compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,-1)*weightPURecoSF".format(weight,useFR))
                       .Filter("weight != 0","good weight")
                       .Define("weightFakeSel0", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,0)*weightPURecoSF".format(weight,useFR))
                       .Define("weightFakeSel1", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,1)*weightPURecoSF".format(weight,useFR))
                       .Define("weightFakeSel2", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,2)*weightPURecoSF".format(weight,useFR))
                       )

    FILTERMU0 = "(Sum(fake_mu) == 1 && ptl <  20 && HLT_Mu8_TrkIsoVVL)"
    FILTERMU1 = "(Sum(fake_mu) == 1 && ptl >= 20 && HLT_Mu17_TrkIsoVVL)"
    FILTEREL0 = "(Sum(fake_el) == 1 && ptl <  15 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30)"
    FILTEREL1 = "(Sum(fake_el) == 1 && ptl >= 15 && HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30)"
    FILTERLEP = "({0}||{1}||{2}||{3})".format(FILTERMU0,FILTERMU1,FILTEREL0,FILTEREL1)
    FILTERLEP0 = "({0}||{1})".format(FILTERMU0,FILTEREL0)
    FILTERLEP1 = "({0}||{1})".format(FILTERMU1,FILTEREL1)
    list_FILTERLEP = [FILTERLEP0, FILTERLEP1]
    print("FILTERMU0: {0}".format(FILTERMU0))
    print("FILTERMU1: {0}".format(FILTERMU1))
    print("FILTEREL0: {0}".format(FILTEREL0))
    print("FILTEREL1: {0}".format(FILTEREL1))

    tagTriggerMuSel0 = "(Sum(fake_mu) == 1 and hasTriggerMatch(fake_Muon_eta[0],fake_Muon_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,0))"
    tagTriggerElSel0 = "(Sum(fake_el) == 1 and hasTriggerMatch(fake_Electron_eta[0],fake_Electron_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,0))"
    tagTriggerSel0 = "({0} || {1})".format(tagTriggerMuSel0,tagTriggerElSel0)

    tagTriggerMuSel1 = "(Sum(fake_mu) == 1 and hasTriggerMatch(fake_Muon_eta[0],fake_Muon_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,1))"
    tagTriggerElSel1 = "(Sum(fake_el) == 1 and hasTriggerMatch(fake_Electron_eta[0],fake_Electron_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,1))"
    tagTriggerSel1 = "({0} || {1})".format(tagTriggerMuSel1,tagTriggerElSel1)

    tagTriggerMuSel2 = "(Sum(fake_mu) == 1 and hasTriggerMatch(fake_Muon_eta[0],fake_Muon_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,2))"
    tagTriggerElSel2 = "(Sum(fake_el) == 1 and hasTriggerMatch(fake_Electron_eta[0],fake_Electron_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,2))"
    tagTriggerSel2 = "({0} || {1})".format(tagTriggerMuSel2,tagTriggerElSel2)

    tagTriggerMuSel3 = "(Sum(fake_mu) == 1 and hasTriggerMatch(fake_Muon_eta[0],fake_Muon_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,0,0))"
    tagTriggerElSel3 = "(Sum(fake_el) == 1 and hasTriggerMatch(fake_Electron_eta[0],fake_Electron_phi[0],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,0,0))"
    tagTriggerSel3 = "({0} || {1})".format(tagTriggerMuSel3,tagTriggerElSel3)

    dfcat = []
    dffakecat = []
    dfjet30cat = []
    dfjet50cat = []
    dfbjet20cat = []
    dftrgcat = []
    for y in range(nCat):
        for ltype in range(2):
            dfcat.append(dfbase.Filter("Sum(fake_mu)+2*Sum(fake_el)-1=={0}".format(ltype), "flavor type == {0}".format(ltype))
                               .Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                               .Define("kPlotWS", "{0}".format(plotCategory("kPlotWS")))
                               .Define("theCat{0}".format(y), "compute_category({0},kPlotNonPrompt,kPlotWS,1,1,0)".format(theCat))
                               .Filter("theCat{0}=={1}".format(y,y), "correct category ({0})".format(y))
                               )

            for trgfake in range(3):
                if(ltype == 0):
                    dftrgcat.append(dfcat[2*y+ltype].Filter("{0}".format(list_TRIGGERFAKEMU[trgfake])))
                else:
                    dftrgcat.append(dfcat[2*y+ltype].Filter("{0}".format(list_TRIGGERFAKEEL[trgfake])))

                histo[trgfake+3*ltype+24][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+24,y), "histo_{0}_{1}".format(trgfake+3*ltype+24,y),40, 0, 160), "mt","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+30][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+30,y), "histo_{0}_{1}".format(trgfake+3*ltype+30,y),40, 0, 160), "PuppiMET_pt","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+36][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+36,y), "histo_{0}_{1}".format(trgfake+3*ltype+36,y),40, 0, 160), "mtfix","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+42][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+42,y), "histo_{0}_{1}".format(trgfake+3*ltype+42,y),50, 10, 60), "ptl","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+48][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+48,y), "histo_{0}_{1}".format(trgfake+3*ltype+48,y),50,0.0,2.5), "absetal","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+54][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+54,y), "histo_{0}_{1}".format(trgfake+3*ltype+54,y),5,-0.5,4.5), "ngood_jets","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+60][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+60,y), "histo_{0}_{1}".format(trgfake+3*ltype+60,y),5,-0.5,4.5), "nbtag_goodbtag_Jet_bjet","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+66][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+66,y), "histo_{0}_{1}".format(trgfake+3*ltype+66,y),50, 10, 60), "ptlcone","weightFakeSel{0}".format(trgfake))

            dfcat[2*y+ltype] = dfcat[2*y+ltype].Filter(FILTERLEP).Filter("mtfix < 160", "mtfix < 160")

            histo[ltype+ 0][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,y), "histo_{0}_{1}".format(ltype+ 0,y),40, 0, 160), "mt","weight")
            histo[ltype+ 2][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 2,y), "histo_{0}_{1}".format(ltype+ 2,y),32,  0, 3.1416), "dphilmet","weight")
            histo[ltype+ 4][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 4,y), "histo_{0}_{1}".format(ltype+ 4,y),40, 0, 160), "PuppiMET_pt","weight")
            histo[ltype+ 6][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,y), "histo_{0}_{1}".format(ltype+ 6,y),40, 0, 160), "mtfix","weight")
            histo[ltype+ 8][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 8,y), "histo_{0}_{1}".format(ltype+ 8,y),50, 10, 60), "ptl","weight")
            histo[ltype+10][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+10,y), "histo_{0}_{1}".format(ltype+10,y),50,0.0,2.5), "absetal","weight")
            histo[ltype+12][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+12,y), "histo_{0}_{1}".format(ltype+12,y),50, 10, 60), "ptlcone","weight")
            histo[ltype+14][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+14,y), "histo_{0}_{1}".format(ltype+14,y),80, 0, 160), "sumMETMT","weight")

            histo[ltype+16][y] = dfcat[2*y+ltype].Filter("{0}".format(tagTriggerSel0)).Histo1D(("histo_{0}_{1}".format(ltype+16,y), "histo_{0}_{1}".format(ltype+16,y),50, 10, 60), "ptl","weight")
            histo[ltype+18][y] = dfcat[2*y+ltype].Filter("{0}".format(tagTriggerSel1)).Histo1D(("histo_{0}_{1}".format(ltype+18,y), "histo_{0}_{1}".format(ltype+18,y),50, 10, 60), "ptl","weight")
            histo[ltype+20][y] = dfcat[2*y+ltype].Filter("{0}".format(tagTriggerSel2)).Histo1D(("histo_{0}_{1}".format(ltype+20,y), "histo_{0}_{1}".format(ltype+20,y),50, 10, 60), "ptl","weight")
            histo[ltype+22][y] = dfcat[2*y+ltype].Filter("{0}".format(tagTriggerSel3)).Histo1D(("histo_{0}_{1}".format(ltype+22,y), "histo_{0}_{1}".format(ltype+22,y),50, 10, 60), "ptl","weight")

            dfjet30cat .append(dfcat[2*y+ltype].Filter("ngood_jets > 0","at least one jet").Define("drljet","deltaR(good_Jet_eta[0],good_Jet_phi[0],etal,phil)"))
            dfjet50cat .append(dfcat[2*y+ltype].Filter("nvbs_jets > 0","at least one jet").Define("drljet","deltaR(vbs_Jet_eta[0],vbs_Jet_phi[0],etal,phil)"))
            dfbjet20cat.append(dfcat[2*y+ltype].Filter("nbtag_goodbtag_Jet_bjet > 0","at least one btagjet").Define("drljet","deltaR(goodbtag_Jet_eta[0],goodbtag_Jet_phi[0],etal,phil)"))

            histo[ltype+72][y] = dfjet30cat [2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+72,y), "histo_{0}_{1}".format(ltype+72,y),50,0,5.0), "drljet","weight")
            histo[ltype+74][y] = dfbjet20cat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+74,y), "histo_{0}_{1}".format(ltype+74,y),50,0,5.0), "drljet","weight")

            dfjet30cat [2*y+ltype] = dfjet30cat [2*y+ltype].Filter("drljet > 0.7", "drljet > 0.7")
            dfjet50cat [2*y+ltype] = dfjet50cat [2*y+ltype].Filter("drljet > 0.7", "drljet > 0.7")
            dfbjet20cat[2*y+ltype] = dfbjet20cat[2*y+ltype].Filter("drljet > 0.7", "drljet > 0.7")

            strLep = "mu"
            chosenSel = "6"
            if(ltype == 1):
               strLep = "el"
               chosenSel = "4"

            histo[ltype+76][y] = dfjet30cat [2*y+ltype].Filter("PuppiMET_pt < 30 && ptl < 70 && Sum(tight_{0}{1})==1".format(strLep,chosenSel)).Histo1D(("histo_{0}_{1}".format(ltype+76,y), "histo_{0}_{1}".format(ltype+76,y), 50, 0, 100), "mt","weight")
            histo[ltype+78][y] = dfbjet20cat[2*y+ltype].Filter("PuppiMET_pt < 30 && ptl < 70 && Sum(tight_{0}{1})==1".format(strLep,chosenSel)).Histo1D(("histo_{0}_{1}".format(ltype+78,y), "histo_{0}_{1}".format(ltype+78,y), 50, 0, 100), "mt","weight")
            histo[ltype+80][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+80,y), "histo_{0}_{1}".format(ltype+80,y), 80,-0.5,79.5), "PV_npvsGood","weight")

            for ptbin in range(2):
                for lepSel in range(9):
                    histo[ltype+100+2*ptbin+2*2*lepSel][y] = dfjet30cat[2*y+ltype].Filter("{0} && Sum(tight_{1}{2})==1".format(list_FILTERLEP[ptbin],strLep,lepSel)).Histo1D(("histo_{0}_{1}".format(ltype+100+2*ptbin+2*2*lepSel,y), "histo_{0}_{1}".format(ltype+100+2*ptbin+2*2*lepSel,y),40, 0, 160), "mtfix","weight")

            dffakecat.append(dfcat[2*y+ltype].Filter("sumMETMT < {0} && ptl < {1}".format(sumMETMTCut,xPtBins[len(xPtBins)-1]), "sumMETMT < X && ptl < Y"))
            dfjet30cat [2*y+ltype] = dfjet30cat [2*y+ltype].Filter("sumMETMT < {0} && ptl < {1}".format(sumMETMTCut,xPtBins[len(xPtBins)-1]), "sumMETMT < X && ptl < Y")
            dfbjet20cat[2*y+ltype] = dfbjet20cat[2*y+ltype].Filter("sumMETMT < {0} && ptl < {1}".format(sumMETMTCut,xPtBins[len(xPtBins)-1]), "sumMETMT < X && ptl < Y")
            dfjet50cat [2*y+ltype] = dfjet50cat [2*y+ltype].Filter("sumMETMT < {0} && ptl < {1}".format(sumMETMTCut,xPtBins[len(xPtBins)-1]), "sumMETMT < X && ptl < Y")

            for ptbin in range(2):
                nHist = ptbin*100
                ptVar = "ptl"
                if(ptbin == 1):
                    ptVar = "ptlcone"
                histo2D[ltype+nHist+ 0][y] = dffakecat[2*y+ltype]                                            .Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 0,y), "histo2d_{0}_{1}".format(ltype+nHist+ 0,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+ 2][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}0)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 2,y), "histo2d_{0}_{1}".format(ltype+nHist+ 2,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+ 4][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}1)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 4,y), "histo2d_{0}_{1}".format(ltype+nHist+ 4,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+ 6][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}2)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 6,y), "histo2d_{0}_{1}".format(ltype+nHist+ 6,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+ 8][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}3)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 8,y), "histo2d_{0}_{1}".format(ltype+nHist+ 8,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+10][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}4)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+10,y), "histo2d_{0}_{1}".format(ltype+nHist+10,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+12][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}5)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+12,y), "histo2d_{0}_{1}".format(ltype+nHist+12,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+14][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}6)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+14,y), "histo2d_{0}_{1}".format(ltype+nHist+14,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+16][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}7)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+16,y), "histo2d_{0}_{1}".format(ltype+nHist+16,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+18][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}8)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+18,y), "histo2d_{0}_{1}".format(ltype+nHist+18,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")

                histo2D[ltype+nHist+20][y] = dfjet30cat[2*y+ltype]					       .Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+20,y), "histo2d_{0}_{1}".format(ltype+nHist+20,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+22][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}0)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+22,y), "histo2d_{0}_{1}".format(ltype+nHist+22,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+24][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}1)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+24,y), "histo2d_{0}_{1}".format(ltype+nHist+24,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+26][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}2)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+26,y), "histo2d_{0}_{1}".format(ltype+nHist+26,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+28][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}3)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+28,y), "histo2d_{0}_{1}".format(ltype+nHist+28,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+30][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}4)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+30,y), "histo2d_{0}_{1}".format(ltype+nHist+30,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+32][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}5)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+32,y), "histo2d_{0}_{1}".format(ltype+nHist+32,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+34][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}6)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+34,y), "histo2d_{0}_{1}".format(ltype+nHist+34,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+36][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}7)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+36,y), "histo2d_{0}_{1}".format(ltype+nHist+36,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+38][y] = dfjet30cat[2*y+ltype] .Filter("Sum(tight_{0}8)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+38,y), "histo2d_{0}_{1}".format(ltype+nHist+38,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")

                histo2D[ltype+nHist+40][y] = dfbjet20cat[2*y+ltype]					       .Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+40,y), "histo2d_{0}_{1}".format(ltype+nHist+40,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+42][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}0)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+42,y), "histo2d_{0}_{1}".format(ltype+nHist+42,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+44][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}1)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+44,y), "histo2d_{0}_{1}".format(ltype+nHist+44,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+46][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}2)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+46,y), "histo2d_{0}_{1}".format(ltype+nHist+46,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+48][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}3)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+48,y), "histo2d_{0}_{1}".format(ltype+nHist+48,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+50][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}4)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+50,y), "histo2d_{0}_{1}".format(ltype+nHist+50,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+52][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}5)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+52,y), "histo2d_{0}_{1}".format(ltype+nHist+52,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+54][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}6)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+54,y), "histo2d_{0}_{1}".format(ltype+nHist+54,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+56][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}7)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+56,y), "histo2d_{0}_{1}".format(ltype+nHist+56,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+58][y] = dfbjet20cat[2*y+ltype].Filter("Sum(tight_{0}8)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+58,y), "histo2d_{0}_{1}".format(ltype+nHist+58,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")

                histo2D[ltype+nHist+60][y] = dfjet50cat[2*y+ltype]					       .Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+60,y), "histo2d_{0}_{1}".format(ltype+nHist+60,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+62][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}0)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+62,y), "histo2d_{0}_{1}".format(ltype+nHist+62,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+64][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}1)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+64,y), "histo2d_{0}_{1}".format(ltype+nHist+64,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+66][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}2)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+66,y), "histo2d_{0}_{1}".format(ltype+nHist+66,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+68][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}3)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+68,y), "histo2d_{0}_{1}".format(ltype+nHist+68,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+70][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}4)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+70,y), "histo2d_{0}_{1}".format(ltype+nHist+70,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+72][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}5)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+72,y), "histo2d_{0}_{1}".format(ltype+nHist+72,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+74][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}6)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+74,y), "histo2d_{0}_{1}".format(ltype+nHist+74,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+76][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}7)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+76,y), "histo2d_{0}_{1}".format(ltype+nHist+76,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+78][y] = dfjet50cat[2*y+ltype] .Filter("Sum(tight_{0}8)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+78,y), "histo2d_{0}_{1}".format(ltype+nHist+78,y), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "absetal", "{0}".format(ptVar),"weight")

    report = []
    for y in range(nCat):
        for ltype in range(2):
            report.append(dfjet30cat[2*y+ltype].Report())
            if(y != theCat): continue
            print("---------------- SUMMARY 2*{0}+{1} = {2} -------------".format(y,ltype,2*y+ltype))
            report[2*y+ltype].Print()

    myfile = ROOT.TFile("fillhisto_fakeAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            #if(histo[j][i].GetSumOfWeights() > 0): print("({0},{1}): {2}".format(j,i,histo[j][i].GetSumOfWeights()))
            histo[j][i].Write()
        for j in range(nHisto):
            if(histo2D[j][i] == 0): continue
            #if(histo2D[j][i].GetSumOfWeights() > 0): print("({0},{1}): {2}".format(j,i,histo2D[j][i].GetSumOfWeights()))
            histo2D[j][i].Write()
    myfile.Close()

def readMCSample(sampleNOW, year, skimType, whichJob, group, puWeights):

    files = getMClist(sampleNOW, skimType)
    print("Total files: {0}".format(len(files)))

    runTree = ROOT.TChain("Runs")
    for f in range(len(files)):
        runTree.AddFile(files[f])

    genEventSumWeight = 0
    genEventSumNoWeight = 0
    for i in range(runTree.GetEntries()):
        runTree.GetEntry(i)
        genEventSumWeight += runTree.genEventSumw
        genEventSumNoWeight += runTree.genEventCount

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

    analysis(df, sampleNOW, SwitchSample(sampleNOW, skimType)[2], weight, year, PDType, "false", whichJob, puWeights)

def readDASample(sampleNOW, year, skimType, whichJob, group, puWeights):

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

    analysis(df, sampleNOW, sampleNOW, weight, year, PDType, "true", whichJob, puWeights)

if __name__ == "__main__":

    group = 10

    skimType = "1l"
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

    try:
        if(process >= 0 and process < 1000):
            readMCSample(process,year,skimType,whichJob,group, puWeights)
        elif(process >= 1000):
            readDASample(process,year,skimType,whichJob,group, puWeights)
    except Exception as e:
        print("FAILED {0}".format(e))

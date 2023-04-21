import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(3)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionJetMet, selectionElMu, selectionWeigths, selectionTrigger1L

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

FAKE_EL   = jsonObject['FAKE_EL']
TIGHT_EL0 = jsonObject['TIGHT_EL0']
TIGHT_EL1 = jsonObject['TIGHT_EL1']
TIGHT_EL2 = jsonObject['TIGHT_EL2']
TIGHT_EL3 = jsonObject['TIGHT_EL3']
TIGHT_EL4 = jsonObject['TIGHT_EL4']
TIGHT_EL5 = jsonObject['TIGHT_EL5']
TIGHT_EL6 = jsonObject['TIGHT_EL6']
TIGHT_EL7 = jsonObject['TIGHT_EL7']

def selection1L(df,year,PDType,isData,TRIGGERFAKEMU,TRIGGERFAKEEL):

    dftag = selectionTrigger1L(df,year,PDType,JSON,isData,TRIGGERFAKEMU,TRIGGERFAKEEL)

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU0,FAKE_EL,TIGHT_EL0)

    dftag =(dftag.Filter("nLoose == 1","Only one loose lepton")
                 .Filter("nFake == 1","Only one fake lepton")
                 #.Filter("{0}".format(FILTERLEP),"trigger/lepton requirement")
                 .Define("tight_mu0", "{0}".format(TIGHT_MU0))
                 .Define("tight_mu1", "{0}".format(TIGHT_MU1))
                 .Define("tight_mu2", "{0}".format(TIGHT_MU2))
                 .Define("tight_mu3", "{0}".format(TIGHT_MU3))
                 .Define("tight_mu4", "{0}".format(TIGHT_MU4))
                 .Define("tight_mu5", "{0}".format(TIGHT_MU5))
                 .Define("tight_mu6", "{0}".format(TIGHT_MU6))
                 .Define("tight_mu7", "{0}".format(TIGHT_MU7))
                 .Define("tight_el0", "{0}".format(TIGHT_EL0))
                 .Define("tight_el1", "{0}".format(TIGHT_EL1))
                 .Define("tight_el2", "{0}".format(TIGHT_EL2))
                 .Define("tight_el3", "{0}".format(TIGHT_EL3))
                 .Define("tight_el4", "{0}".format(TIGHT_EL4))
                 .Define("tight_el5", "{0}".format(TIGHT_EL5))
                 .Define("tight_el6", "{0}".format(TIGHT_EL6))
                 .Define("tight_el7", "{0}".format(TIGHT_EL7))
                 .Define("mt"      ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, MET_pt, MET_phi,0)")
                 .Define("dphilmet","compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, MET_pt, MET_phi,1)")
                 .Define("mtfix"   ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, MET_pt, MET_phi,2)")
                 .Define("ptl"     ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, MET_pt, MET_phi,3)")
                 .Define("etal"    ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, MET_pt, MET_phi,4)")
                 .Define("phil"    ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, MET_pt, MET_phi,5)")
                 .Define("absetal" ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, MET_pt, MET_phi,6)")
                 .Define("ptlcone" ,"compute_lmet_var(fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_jetRelIso, fake_Electron_pt, fake_Electron_eta, fake_Electron_phi, fake_Electron_jetRelIso, MET_pt, MET_phi,7)")
                 .Define("maxMETMT","max(MET_pt,mt)")
                )

    dftag = selectionJetMet(dftag,year,bTagSel,isData)

    return dftag

def analysis(df,count,category,weight,year,PDType,isData,whichJob):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    xPtbins = array('d', [10.0, 15.0, 20.0, 25.0, 30.0, 35.0])
    xEtabins = array('d', [0.0, 0.5, 1.0, 1.5, 2.0, 2.5])

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    maxMETMTCut = 30

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo   = [[0 for y in range(nCat)] for x in range(nHisto)]
    histo2D = [[0 for y in range(nCat)] for x in range(nHisto)]

    overallTriggers = jsonObject['triggers']
    TRIGGERFAKEMU = getTriggerFromJson(overallTriggers, "TRIGGERFAKEMU", year)
    TRIGGERFAKEEL = getTriggerFromJson(overallTriggers, "TRIGGERFAKEEL", year)

    list_TRIGGERFAKEMU = TRIGGERFAKEMU.split('(')[1].split(')')[0].split('||')
    list_TRIGGERFAKEEL = TRIGGERFAKEEL.split('(')[1].split(')')[0].split('||')
    list_TRIGGERFAKE = list_TRIGGERFAKEMU
    list_TRIGGERFAKE.extend(list_TRIGGERFAKEEL)
    print("Total number of fake trigger paths: {0}".format(len(list_TRIGGERFAKE)))

    dfbase = selection1L(df,year,PDType,isData,TRIGGERFAKEMU,TRIGGERFAKEEL)

    if(theCat == plotCategory("kPlotData")):
        dfbase = (dfbase.Define("weight","1.0")
                        .Define("weightFakeSel0", "1.0")
                        .Define("weightFakeSel1", "1.0")
                        .Define("weightFakeSel2", "1.0")
                        )
    else:
        dfbase =(dfbase.Define("PDType","\"{0}\"".format(PDType))
                       .Define("fake_Muon_genPartFlav","Muon_genPartFlav[fake_mu]")
                       .Define("fake_Electron_genPartFlav","Electron_genPartFlav[fake_el]")
                       .Define("weight","compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,-1)".format(weight,useFR))
                       .Filter("weight != 0","good weight")
                       .Define("weightFakeSel0", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,0)".format(weight,useFR))
                       .Define("weightFakeSel1", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,1)".format(weight,useFR))
                       .Define("weightFakeSel2", "compute_weights({0},genWeight,PDType,fake_Muon_genPartFlav,fake_Electron_genPartFlav,{1})*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,2)".format(weight,useFR))
                       )

    FILTERMU0 = "(Sum(fake_mu) == 1 && ptl <  20 && HLT_Mu8_TrkIsoVVL)"
    FILTERMU1 = "(Sum(fake_mu) == 1 && ptl >= 20 && HLT_Mu17_TrkIsoVVL)"
    FILTEREL0 = "(Sum(fake_el) == 1 && ptl <  15 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30)"
    FILTEREL1 = "(Sum(fake_el) == 1 && ptl >= 15 && HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30)"
    FILTERLEP = "{0}||{1}||{2}||{3}".format(FILTERMU0,FILTERMU1,FILTEREL0,FILTEREL1)
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
    dfjetcat = []
    dfbjetcat = []
    dftrgcat = []
    for y in range(nCat):
        for ltype in range(2):
            dfcat.append(dfbase.Filter("Sum(fake_mu)+2*Sum(fake_el)-1=={0}".format(ltype), "flavor type == {0}".format(ltype))
                               .Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                               .Define("theCat{0}".format(y), "compute_category({0},kPlotNonPrompt,1,1)".format(theCat))
                               .Filter("theCat{0}=={1}".format(y,y), "correct category ({0})".format(y))
                               )

            for trgfake in range(3):
                if(ltype == 0):
                    dftrgcat.append(dfcat[2*y+ltype].Filter("{0}".format(list_TRIGGERFAKEMU[trgfake])))
                else:
                    dftrgcat.append(dfcat[2*y+ltype].Filter("{0}".format(list_TRIGGERFAKEEL[trgfake])))

                histo[trgfake+3*ltype+100][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+100,y), "histo_{0}_{1}".format(trgfake+3*ltype+100,y),100, 0, 200), "mt","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+106][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+106,y), "histo_{0}_{1}".format(trgfake+3*ltype+106,y),100, 0, 200), "MET_pt","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+112][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+112,y), "histo_{0}_{1}".format(trgfake+3*ltype+112,y),100, 0, 200), "mtfix","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+118][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+118,y), "histo_{0}_{1}".format(trgfake+3*ltype+118,y),50, 10, 60), "ptl","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+124][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+124,y), "histo_{0}_{1}".format(trgfake+3*ltype+124,y),50,0.0,2.5), "absetal","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+130][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+130,y), "histo_{0}_{1}".format(trgfake+3*ltype+130,y),5,-0.5,4.5), "ngood_jets","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+136][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+136,y), "histo_{0}_{1}".format(trgfake+3*ltype+136,y),5,-0.5,4.5), "nbtag_goodbtag_Jet_bjet","weightFakeSel{0}".format(trgfake))
                histo[trgfake+3*ltype+142][y] = dftrgcat[6*y+3*ltype+trgfake].Histo1D(("histo_{0}_{1}".format(trgfake+3*ltype+142,y), "histo_{0}_{1}".format(trgfake+3*ltype+142,y),50, 10, 60), "ptlcone","weightFakeSel{0}".format(trgfake))

            dfcat[2*y+ltype] = dfcat[2*y+ltype].Filter(FILTERLEP)

            histo[ltype+ 0][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,y), "histo_{0}_{1}".format(ltype+ 0,y),100, 0, 200), "mt","weight")
            histo[ltype+ 2][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 2,y), "histo_{0}_{1}".format(ltype+ 2,y),32,  0, 3.1416), "dphilmet","weight")
            histo[ltype+ 4][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 4,y), "histo_{0}_{1}".format(ltype+ 4,y),100, 0, 200), "MET_pt","weight")
            histo[ltype+ 6][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,y), "histo_{0}_{1}".format(ltype+ 6,y),100, 0, 200), "mtfix","weight")
            histo[ltype+ 8][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 8,y), "histo_{0}_{1}".format(ltype+ 8,y),50, 10, 60), "ptl","weight")
            histo[ltype+10][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+10,y), "histo_{0}_{1}".format(ltype+10,y),50,0.0,2.5), "absetal","weight")
            histo[ltype+12][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+12,y), "histo_{0}_{1}".format(ltype+12,y),50, 10, 60), "ptlcone","weight")
            histo[ltype+14][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+14,y), "histo_{0}_{1}".format(ltype+14,y),100, 0, 200), "maxMETMT","weight")

            histo[ltype+16][y] = dfcat[2*y+ltype].Filter("{0}".format(tagTriggerSel0)).Histo1D(("histo_{0}_{1}".format(ltype+16,y), "histo_{0}_{1}".format(ltype+16,y),50, 10, 60), "ptl","weight")
            histo[ltype+18][y] = dfcat[2*y+ltype].Filter("{0}".format(tagTriggerSel1)).Histo1D(("histo_{0}_{1}".format(ltype+18,y), "histo_{0}_{1}".format(ltype+18,y),50, 10, 60), "ptl","weight")
            histo[ltype+20][y] = dfcat[2*y+ltype].Filter("{0}".format(tagTriggerSel2)).Histo1D(("histo_{0}_{1}".format(ltype+20,y), "histo_{0}_{1}".format(ltype+20,y),50, 10, 60), "ptl","weight")
            histo[ltype+22][y] = dfcat[2*y+ltype].Filter("{0}".format(tagTriggerSel3)).Histo1D(("histo_{0}_{1}".format(ltype+22,y), "histo_{0}_{1}".format(ltype+22,y),50, 10, 60), "ptl","weight")

            strLep = "mu"
            if(ltype == 1):
               strLep = "el"

            for ptbin in range(len(xPtbins)-1):
                histo[ltype+24+2*ptbin][y] = dfcat[2*y+ltype].Filter("ptl > {0} && ptl < {1}".format(xPtbins[ptbin],xPtbins[ptbin+1]))                             .Histo1D(("histo_{0}_{1}".format(ltype+24+2*ptbin,y), "histo_{0}_{1}".format(ltype+24+2*ptbin,y),100, 0, 200), "mtfix","weight")
                histo[ltype+34+2*ptbin][y] = dfcat[2*y+ltype].Filter("ptl > {0} && ptl < {1} && Sum(tight_{2}3)==1".format(xPtbins[ptbin],xPtbins[ptbin+1],strLep)).Histo1D(("histo_{0}_{1}".format(ltype+34+2*ptbin,y), "histo_{0}_{1}".format(ltype+34+2*ptbin,y),100, 0, 200), "mtfix","weight")
                histo[ltype+44+2*ptbin][y] = dfcat[2*y+ltype].Filter("ptl > {0} && ptl < {1}".format(xPtbins[ptbin],xPtbins[ptbin+1]))                             .Histo1D(("histo_{0}_{1}".format(ltype+44+2*ptbin,y), "histo_{0}_{1}".format(ltype+44+2*ptbin,y),100, 0, 200), "mtfix","weight")
                histo[ltype+54+2*ptbin][y] = dfcat[2*y+ltype].Filter("ptl > {0} && ptl < {1} && Sum(tight_{2}3)==1".format(xPtbins[ptbin],xPtbins[ptbin+1],strLep)).Histo1D(("histo_{0}_{1}".format(ltype+54+2*ptbin,y), "histo_{0}_{1}".format(ltype+54+2*ptbin,y),100, 0, 200), "mtfix","weight")

            dffakecat.append(dfcat[2*y+ltype].Filter("maxMETMT < {0}".format(maxMETMTCut), "maxMETMT < {0}".format(maxMETMTCut)))
            dfjetcat.append(dffakecat[2*y+ltype].Filter("ngood_jets > 0","at least one jet").Define("drljet","deltaR(good_Jet_eta[0],good_Jet_phi[0],etal,phil)"))
            dfbjetcat.append(dffakecat[2*y+ltype].Filter("nbtag_goodbtag_Jet_bjet > 0","at least one btagjet").Define("drljet","deltaR(goodbtag_Jet_eta[0],goodbtag_Jet_phi[0],etal,phil)"))

            histo[ltype+64][y] = dfjetcat [2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+64,y), "histo_{0}_{1}".format(ltype+64,y),50,0,5.0), "drljet","weight")
            histo[ltype+66][y] = dfbjetcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+66,y), "histo_{0}_{1}".format(ltype+66,y),50,0,5.0), "drljet","weight")

            dfjetcat [2*y+ltype] = dfjetcat [2*y+ltype].Filter("drljet > 0.7", "drljet > 0.7")
            dfbjetcat[2*y+ltype] = dfbjetcat[2*y+ltype].Filter("drljet > 0.7", "drljet > 0.7")

            for ptbin in range(2):
                nHist = ptbin*100
                ptVar = "ptl"
                if(ptbin == 1):
                    ptVar = "ptlcone"
                histo2D[ltype+nHist+ 0][y] = dffakecat[2*y+ltype]                                            .Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 0,y), "histo2d_{0}_{1}".format(ltype+nHist+ 0,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+ 2][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}0)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 2,y), "histo2d_{0}_{1}".format(ltype+nHist+ 2,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+ 4][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}1)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 4,y), "histo2d_{0}_{1}".format(ltype+nHist+ 4,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+ 6][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}2)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 6,y), "histo2d_{0}_{1}".format(ltype+nHist+ 6,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+ 8][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}3)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+ 8,y), "histo2d_{0}_{1}".format(ltype+nHist+ 8,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+10][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}4)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+10,y), "histo2d_{0}_{1}".format(ltype+nHist+10,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+12][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}5)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+12,y), "histo2d_{0}_{1}".format(ltype+nHist+12,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+14][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}6)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+14,y), "histo2d_{0}_{1}".format(ltype+nHist+14,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+16][y] = dffakecat[2*y+ltype].Filter("Sum(tight_{0}7)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+16,y), "histo2d_{0}_{1}".format(ltype+nHist+16,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")

                histo2D[ltype+nHist+18][y] = dfjetcat[2*y+ltype]                                             .Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+18,y), "histo2d_{0}_{1}".format(ltype+nHist+18,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+20][y] = dfjetcat[2*y+ltype] .Filter("Sum(tight_{0}0)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+20,y), "histo2d_{0}_{1}".format(ltype+nHist+20,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+22][y] = dfjetcat[2*y+ltype] .Filter("Sum(tight_{0}1)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+22,y), "histo2d_{0}_{1}".format(ltype+nHist+22,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+24][y] = dfjetcat[2*y+ltype] .Filter("Sum(tight_{0}2)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+24,y), "histo2d_{0}_{1}".format(ltype+nHist+24,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+26][y] = dfjetcat[2*y+ltype] .Filter("Sum(tight_{0}3)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+26,y), "histo2d_{0}_{1}".format(ltype+nHist+26,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+28][y] = dfjetcat[2*y+ltype] .Filter("Sum(tight_{0}4)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+28,y), "histo2d_{0}_{1}".format(ltype+nHist+28,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+30][y] = dfjetcat[2*y+ltype] .Filter("Sum(tight_{0}5)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+30,y), "histo2d_{0}_{1}".format(ltype+nHist+30,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+32][y] = dfjetcat[2*y+ltype] .Filter("Sum(tight_{0}6)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+32,y), "histo2d_{0}_{1}".format(ltype+nHist+32,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+34][y] = dfjetcat[2*y+ltype] .Filter("Sum(tight_{0}7)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+34,y), "histo2d_{0}_{1}".format(ltype+nHist+34,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")

                histo2D[ltype+nHist+36][y] = dfbjetcat[2*y+ltype]                                            .Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+36,y), "histo2d_{0}_{1}".format(ltype+nHist+36,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+38][y] = dfbjetcat[2*y+ltype].Filter("Sum(tight_{0}0)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+38,y), "histo2d_{0}_{1}".format(ltype+nHist+38,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+40][y] = dfbjetcat[2*y+ltype].Filter("Sum(tight_{0}1)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+40,y), "histo2d_{0}_{1}".format(ltype+nHist+40,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+42][y] = dfbjetcat[2*y+ltype].Filter("Sum(tight_{0}2)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+42,y), "histo2d_{0}_{1}".format(ltype+nHist+42,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+44][y] = dfbjetcat[2*y+ltype].Filter("Sum(tight_{0}3)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+44,y), "histo2d_{0}_{1}".format(ltype+nHist+44,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+46][y] = dfbjetcat[2*y+ltype].Filter("Sum(tight_{0}4)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+46,y), "histo2d_{0}_{1}".format(ltype+nHist+46,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+48][y] = dfbjetcat[2*y+ltype].Filter("Sum(tight_{0}5)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+48,y), "histo2d_{0}_{1}".format(ltype+nHist+48,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+50][y] = dfbjetcat[2*y+ltype].Filter("Sum(tight_{0}6)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+50,y), "histo2d_{0}_{1}".format(ltype+nHist+50,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")
                histo2D[ltype+nHist+52][y] = dfbjetcat[2*y+ltype].Filter("Sum(tight_{0}7)==1".format(strLep)).Histo2D(("histo2d_{0}_{1}".format(ltype+nHist+52,y), "histo2d_{0}_{1}".format(ltype+nHist+52,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "absetal", "{0}".format(ptVar),"weight")

    report = []
    for y in range(nCat):
        for ltype in range(2):
            report.append(dfjetcat[2*y+ltype].Report())
            if(y != theCat): continue
            print("---------------- SUMMARY 2*{0}+{1} = {2} -------------".format(y,ltype,2*y+ltype))
            report[2*y+ltype].Print()

    myfile = ROOT.TFile("fillhisto_fakeAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            if(histo[j][i].GetSumOfWeights() > 0): print("({0},{1}): {2}".format(j,i,histo[j][i].GetSumOfWeights()))
            histo[j][i].Write()
        for j in range(nHisto):
            if(histo2D[j][i] == 0): continue
            if(histo2D[j][i].GetSumOfWeights() > 0): print("({0},{1}): {2}".format(j,i,histo2D[j][i].GetSumOfWeights()))
            histo2D[j][i].Write()
    myfile.Close()

def readMCSample(sampleNOW, year, skimType, whichJob, group):

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

    #puPath = "../datapuWeights_UL_{0}.root".format(year)
    #fPUFile = ROOT.TFile(puPath)
    #fhDPU     = fPUFile.Get("puWeights")
    #fhDPUUp   = fPUFile.Get("puWeightsUp")
    #fhDPUDown = fPUFile.Get("puWeightsDown")
    #fhDPU    .SetDirectory(0);
    #fhDPUUp  .SetDirectory(0);
    #fhDPUDown.SetDirectory(0);
    #fPUFile.Close()

    PDType = os.path.basename(SwitchSample(sampleNOW, skimType)[0]).split('+')[0]

    analysis(df, sampleNOW, SwitchSample(sampleNOW, skimType)[2], weight, year, PDType, "false", whichJob)

def readDASample(sampleNOW, year, skimType, whichJob, group):

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

    analysis(df, sampleNOW, sampleNOW, weight, year, PDType, "true", whichJob)

if __name__ == "__main__":

    group = 10

    skimType = "1l"
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

    try:
        if(process >= 0 and process < 1000):
            readMCSample(process,year,skimType,whichJob,group)
        elif(process >= 1000):
            readDASample(process,year,skimType,whichJob,group)
    except Exception as e:
        print("Error sample: {0}".format(e))

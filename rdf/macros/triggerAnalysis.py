import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(4)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection2LVar, selectionTrigger1L, selectionTrigger2L, selectionElMu, selectionWeigths
#from utilsAna import loadCorrectionSet

# 0 = T, 1 = M, 2 = L
bTagSel = 1
useBTaggingWeights = 0

useFR = 0

selectionJsonPath = "config/selection.json"

with open(selectionJsonPath) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

JSON = jsonObject['JSON']

BARRELphotons = jsonObject['BARRELphotons']
ENDCAPphotons = jsonObject['ENDCAPphotons']

VBSSEL = jsonObject['VBSSEL']

FAKE_MU0   = "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true"
FAKE_MU1   = "abs(fake_Muon_eta) < 2.4 && fake_Muon_pt > 10 && fake_Muon_looseId == true"
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

FAKE_EL0   = "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1"
FAKE_EL1   = "abs(fake_Electron_eta) < 2.5 && fake_Electron_pt > 10 && fake_Electron_cutBased >= 1"
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

def selectionLL(df,year,PDType,isData,TRIGGERMUEG,TRIGGERDMU,TRIGGERSMU,TRIGGERDEL,TRIGGERSEL):

    dftag = selectionTrigger2L(df,year,PDType,JSON,isData,TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    # This is a hack to avoid fakeable objects
    dftag = selectionElMu(dftag,year,FAKE_MU0,FAKE_MU1,FAKE_EL0,FAKE_EL1)

    dftag = (dftag.Define("tight_mu0", "{0}".format(TIGHT_MU0))
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

                  .Filter("nLoose == 2","Only two loose leptons")
                  .Filter("nFake == 2","Two fake leptons")
                  .Filter("nTight == 2","Two tight leptons")

                  .Filter("(Sum(fake_mu) == 2 and Max(fake_Muon_pt) > 30) or (Sum(fake_el) == 2 and Max(fake_Electron_pt) > 30)","At least one high pt lepton")
                  )

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData)
    dftag = selection2LVar  (dftag,year)

    dftag = (dftag.Filter("abs(mll-91.1876) < 15","mll cut")
                  .Filter("(Sum(fake_mu) == 2 and triggerSMU > 0) or (Sum(fake_el) == 2 and triggerSEL > 0)","Single trigger requirement")
                  )

    return dftag

def selectionFF(df,year,PDType,isData,TRIGGERFAKEMU,TRIGGERFAKEEL):

    dftag = selectionTrigger1L(df,year,PDType,JSON,isData,TRIGGERFAKEMU,TRIGGERFAKEEL)

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU1,FAKE_EL,TIGHT_EL1)

    dftag = (dftag.Filter("nLoose == 2","Only two loose leptons")
                  .Filter("nFake == 2","Two fake leptons")
                  .Filter("nTight == 2","Two tight leptons")
                  .Filter("(Sum(fake_mu) == 2 and triggerFAKEMU > 0 and Sum(fake_Muon_charge) == 0 and fake_Muon_pt[0] > 30 and fake_Muon_pt[1] > 30) or (Sum(fake_el) == 2 and triggerFAKEEL > 0 and Sum(fake_Electron_charge) == 0 and fake_Electron_pt[0] > 30 and fake_Electron_pt[1] > 30)","Two high pt leptons")
                  )

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData)
    dftag = selection2LVar  (dftag,year)

    dftag = (dftag.Filter("abs(mll-91.1876) < 15","mll cut")
                  )

    return dftag

def analysis(df,count,category,weight,year,PDType,isData,whichJob,nPDFReplicas,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    xPtbins = array('d', [10,15,20,25,30,35,40,45,50,55,60,70,80,90,100,150,200,250])
    xEtabins = array('d', [0.0,0.5,1.0,1.5,2.0,2.5])

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
    print("Total number of lepton trigger paths: {0}".format(len(list_TRIGGER)))

    dfbase = selectionLL(df,year,PDType,isData,TRIGGERMUEG,TRIGGERDMU,TRIGGERSMU,TRIGGERDEL,TRIGGERSEL)

    dfbase = selectionWeigths(dfbase,isData,year,PDType,weight,useFR,bTagSel,useBTaggingWeights,nPDFReplicas)

    TRIGGERFAKEMU = getTriggerFromJson(overallTriggers, "TRIGGERFAKEMU", year)
    TRIGGERFAKEEL = getTriggerFromJson(overallTriggers, "TRIGGERFAKEEL", year)

    list_TRIGGERFAKEMU = TRIGGERFAKEMU.split('(')[1].split(')')[0].split('||')
    list_TRIGGERFAKEEL = TRIGGERFAKEEL.split('(')[1].split(')')[0].split('||')
    list_TRIGGERFAKE = list_TRIGGERFAKEMU
    list_TRIGGERFAKE.extend(list_TRIGGERFAKEEL)
    print("Total number of fake trigger paths: {0}".format(len(list_TRIGGERFAKE)))

    dffake = selectionFF(df,year,PDType,isData,TRIGGERFAKEMU,TRIGGERFAKEEL)

    dffake = selectionWeigths(dffake,isData,year,PDType,weight,useFR,bTagSel,useBTaggingWeights,nPDFReplicas)
    if(theCat == plotCategory("kPlotData")):
        dffake = (dffake.Define("weightFakeSel0", "weight")
                        .Define("weightFakeSel1", "weight")
                        .Define("weightFakeSel2", "weight")
                        )
    else:
        dffake = (dffake.Define("weightFakeSel0", "weight*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,0)")
                        .Define("weightFakeSel1", "weight*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,1)")
                        .Define("weightFakeSel2", "weight*compute_lumiFakeRate(fake_Muon_pt,fake_Electron_pt,2)")
                        )

    xMllMin = [91.1876-15, 91.1876-15]
    xMllMax = [91.1876+15, 91.1876+15]
    dfcat = []
    dfzoscat = []
    dfzsscat = []
    dffakecat = []
    for x in range(nCat):
        for ltype in range(2):
            dfcat.append(dfbase.Filter("DiLepton_flavor=={0}".format(2*ltype), "flavor type == {0}".format(2*ltype))
                               .Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                               .Define("theCat{0}".format(x), "compute_category({0},kPlotNonPrompt,nFake,nTight)".format(theCat))
                               .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x))
                               )
            dffakecat.append(dffake.Filter("DiLepton_flavor=={0}".format(2*ltype), "flavor type == {0}".format(2*ltype))
                                   .Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                                   .Define("theCat{0}".format(x), "compute_category({0},kPlotNonPrompt,nFake,nTight)".format(theCat))
                                   .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x))
                                   )
            # Fake lepton study
            for trgfake in range(3):
                if(ltype == 0):
                    histo[ltype+50+2*trgfake][x] = dffakecat[2*x+ltype].Filter("{0}".format(list_TRIGGERFAKEMU[trgfake])).Histo1D(("histo_{0}_{1}".format(ltype+50+2*trgfake,x), "histo_{0}_{1}".format(ltype+50+2*trgfake,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightFakeSel{0}".format(trgfake))
                    histo[ltype+56+2*trgfake][x] = dffakecat[2*x+ltype].Filter("{0}".format(list_TRIGGERFAKEMU[trgfake])).Filter("{0}".format(TRIGGERSMU)).Histo1D(("histo_{0}_{1}".format(ltype+56+2*trgfake,x), "histo_{0}_{1}".format(ltype+56+2*trgfake,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightFakeSel{0}".format(trgfake))
                else:
                    histo[ltype+50+2*trgfake][x] = dffakecat[2*x+ltype].Filter("{0}".format(list_TRIGGERFAKEEL[trgfake])).Histo1D(("histo_{0}_{1}".format(ltype+50+2*trgfake,x), "histo_{0}_{1}".format(ltype+50+2*trgfake,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightFakeSel{0}".format(trgfake))
                    histo[ltype+56+2*trgfake][x] = dffakecat[2*x+ltype].Filter("{0}".format(list_TRIGGERFAKEEL[trgfake])).Filter("{0}".format(TRIGGERSEL)).Histo1D(("histo_{0}_{1}".format(ltype+56+2*trgfake,x), "histo_{0}_{1}".format(ltype+56+2*trgfake,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightFakeSel{0}".format(trgfake))

            for ltag in range(2):
                # Real lepton study
                theLeptonSel = "((Sum(fake_mu) == 2 and tight_mu6[{0}] == true) or (Sum(fake_el) == 2 and tight_el3[{1}] == true))".format(ltag,ltag)
                dfzoscat.append(dfcat[2*x+ltype].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) == 0 and {0}".format(theLeptonSel), "Opposite-sign leptons ({0})".format(ltag)))
                dfzsscat.append(dfcat[2*x+ltype].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) != 0 and {0}".format(theLeptonSel), "Same-sign leptons ({0})".format(ltag)))

                tagTriggerMuSel = "(Sum(fake_mu) == 2 and hasTriggerMatch(    fake_Muon_eta[{0}],    fake_Muon_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,1))".format(ltag,ltag)
                tagTriggerElSel = "(Sum(fake_el) == 2 and hasTriggerMatch(fake_Electron_eta[{0}],fake_Electron_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,1))".format(ltag,ltag)

                dfzoscat[4*x+2*ltype+ltag] = dfzoscat[4*x+2*ltype+ltag].Filter("{0} or {1}".format(tagTriggerMuSel,tagTriggerElSel),"Tag trigger match ({0})".format(ltag))
                dfzsscat[4*x+2*ltype+ltag] = dfzsscat[4*x+2*ltype+ltag].Filter("{0} or {1}".format(tagTriggerMuSel,tagTriggerElSel),"Tag trigger match ({0})".format(ltag))

                histo[2*ltype+ltag+ 0][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+ 0,x), "histo_{0}_{1}".format(2*ltype+ltag+ 0,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightNoLepSF")
                histo[2*ltype+ltag+ 4][x] = dfzsscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+ 4,x), "histo_{0}_{1}".format(2*ltype+ltag+ 4,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightNoLepSF")

                lprobe = 1
                if(ltag == 1): lprobe = 0

                lflavor = "tight_mu"
                if(ltype == 1): lflavor = "tight_el"

                histo2D[2*ltype+ltag+ 0][x] = dfzoscat[4*x+2*ltype+ltag]                                                   .Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+ 0, x), "histo2d_{0}_{1}".format(2*ltype+ltag+ 0, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+ 4][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}0[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+ 4, x), "histo2d_{0}_{1}".format(2*ltype+ltag+ 4, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+ 8][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}1[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+ 8, x), "histo2d_{0}_{1}".format(2*ltype+ltag+ 8, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+12][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}2[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+12, x), "histo2d_{0}_{1}".format(2*ltype+ltag+12, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+16][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}3[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+16, x), "histo2d_{0}_{1}".format(2*ltype+ltag+16, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+20][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}4[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+20, x), "histo2d_{0}_{1}".format(2*ltype+ltag+20, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+24][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}5[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+24, x), "histo2d_{0}_{1}".format(2*ltype+ltag+24, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+28][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}6[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+28, x), "histo2d_{0}_{1}".format(2*ltype+ltag+28, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+32][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}7[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+32, x), "histo2d_{0}_{1}".format(2*ltype+ltag+32, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                histo2D[2*ltype+ltag+36][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}8[{1}] == true".format(lflavor,lprobe)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+36, x), "histo2d_{0}_{1}".format(2*ltype+ltag+36, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weightNoLepSF")

                histo[2*ltype+ltag+ 8][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+ 8,x), "histo_{0}_{1}".format(2*ltype+ltag+ 8,x), len(xPtbins)-1, xPtbins), "ptl{0}".format(lprobe+1),"weightNoLepSF")

                histo[2*ltype+ltag+16][x] = dfzoscat[4*x+2*ltype+ltag].Filter("ptl{0} > 10 && ptl{0} < 15".format(lprobe+1)).Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+16,x), "histo_{0}_{1}".format(2*ltype+ltag+16,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightNoLepSF")
                histo[2*ltype+ltag+20][x] = dfzoscat[4*x+2*ltype+ltag].Filter("ptl{0} > 15 && ptl{0} < 20".format(lprobe+1)).Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+20,x), "histo_{0}_{1}".format(2*ltype+ltag+20,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightNoLepSF")
                histo[2*ltype+ltag+24][x] = dfzoscat[4*x+2*ltype+ltag].Filter("ptl{0} > 20 && ptl{0} < 25".format(lprobe+1)).Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+24,x), "histo_{0}_{1}".format(2*ltype+ltag+24,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightNoLepSF")
                histo[2*ltype+ltag+28][x] = dfzoscat[4*x+2*ltype+ltag].Filter("ptl{0} > 25 && ptl{0} < 30".format(lprobe+1)).Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+28,x), "histo_{0}_{1}".format(2*ltype+ltag+28,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightNoLepSF")
                if(theCat != plotCategory("kPlotData")):
                     if(ltype == 0):
                         histo[2*ltype+ltag+32][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+32,x), "histo_{0}_{1}".format(2*ltype+ltag+32,x), 60, xMllMin[ltype], xMllMax[ltype]), "mllMuonMomUp","weightNoLepSF")
                         histo[2*ltype+ltag+36][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+36,x), "histo_{0}_{1}".format(2*ltype+ltag+36,x), 60, xMllMin[ltype], xMllMax[ltype]), "mllMuonMomDown","weightNoLepSF")
                     else:
                         histo[2*ltype+ltag+32][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+32,x), "histo_{0}_{1}".format(2*ltype+ltag+32,x), 60, xMllMin[ltype], xMllMax[ltype]), "mllElectronMomUp","weightNoLepSF")
                         histo[2*ltype+ltag+36][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+36,x), "histo_{0}_{1}".format(2*ltype+ltag+36,x), 60, xMllMin[ltype], xMllMax[ltype]), "mllElectronMomDown","weightNoLepSF")
                else:
                     histo[2*ltype+ltag+32][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+32,x), "histo_{0}_{1}".format(2*ltype+ltag+32,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightNoLepSF")
                     histo[2*ltype+ltag+36][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+36,x), "histo_{0}_{1}".format(2*ltype+ltag+36,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weightNoLepSF")

                # tighter ID to perform trigger efficiency measurements
                dfzoscat[4*x+2*ltype+ltag] = dfzoscat[4*x+2*ltype+ltag].Filter("{0}1[{1}] == true".format(lflavor,lprobe),"tight id({0}1[{1}])".format(lflavor,lprobe))
                dfzsscat[4*x+2*ltype+ltag] = dfzsscat[4*x+2*ltype+ltag].Filter("{0}1[{1}] == true".format(lflavor,lprobe),"tight id({0}1[{1}])".format(lflavor,lprobe))

                histo[2*ltype+ltag+12][x] = dfzoscat[4*x+2*ltype+ltag].Histo1D(("histo_{0}_{1}".format(2*ltype+ltag+12,x), "histo_{0}_{1}".format(2*ltype+ltag+12,x), len(xPtbins)-1, xPtbins), "ptl{0}".format(lprobe+1),"weightNoLepSF")
                probeTriggerSMuSel  = "(Sum(fake_mu) == 2 and hasTriggerMatch(    fake_Muon_eta[{0}],    fake_Muon_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,1))".format(lprobe,lprobe)
                probeTriggerSElSel  = "(Sum(fake_el) == 2 and hasTriggerMatch(fake_Electron_eta[{0}],fake_Electron_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,1))".format(lprobe,lprobe)
                probeTriggerDMuSel  = "(Sum(fake_mu) == 2 and hasTriggerMatch(    fake_Muon_eta[{0}],    fake_Muon_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,0))".format(lprobe,lprobe)
                probeTriggerDElSel  = "(Sum(fake_el) == 2 and hasTriggerMatch(fake_Electron_eta[{0}],fake_Electron_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,0))".format(lprobe,lprobe)
                probeTrigger1MuSel0 = "(Sum(fake_mu) == 2 and hasTriggerMatch(    fake_Muon_eta[{0}],    fake_Muon_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,2) &&     fake_Muon_pt[{2}] > 10 && HLT_Mu8_TrkIsoVVL)".format(lprobe,lprobe,lprobe)
                probeTrigger1ElSel0 = "(Sum(fake_el) == 2 and hasTriggerMatch(fake_Electron_eta[{0}],fake_Electron_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,2) && fake_Electron_pt[{2}] > 10 && HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30)".format(lprobe,lprobe,lprobe)
                probeTrigger1MuSel1 = "(Sum(fake_mu) == 2 and hasTriggerMatch(    fake_Muon_eta[{0}],    fake_Muon_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,2) &&     fake_Muon_pt[{2}] > 20 && HLT_Mu17_TrkIsoVVL)".format(lprobe,lprobe,lprobe)
                probeTrigger1ElSel1 = "(Sum(fake_el) == 2 and hasTriggerMatch(fake_Electron_eta[{0}],fake_Electron_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,2) && fake_Electron_pt[{2}] > 15 && HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30)".format(lprobe,lprobe,lprobe)
                probeTrigger1MuSel2 = "(Sum(fake_mu) == 2 and hasTriggerMatch(    fake_Muon_eta[{0}],    fake_Muon_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,13,2) &&     fake_Muon_pt[{2}] > 20 && HLT_Mu19_TrkIsoVVL)".format(lprobe,lprobe,lprobe)
                probeTrigger1ElSel2 = "(Sum(fake_el) == 2 and hasTriggerMatch(fake_Electron_eta[{0}],fake_Electron_phi[{1}],TrigObj_eta,TrigObj_phi,TrigObj_id,TrigObj_filterBits,11,2) && fake_Electron_pt[{2}] > 25 && HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30)".format(lprobe,lprobe,lprobe)

                histo2D[2*ltype+ltag+40][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0} or {1}".format(probeTriggerSMuSel,probeTriggerSElSel)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+40, x), "histo2d_{0}_{1}".format(2*ltype+ltag+40, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weight")
                histo2D[2*ltype+ltag+44][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0} or {1}".format(probeTriggerDMuSel,probeTriggerDElSel)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+44, x), "histo2d_{0}_{1}".format(2*ltype+ltag+44, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weight")
                histo2D[2*ltype+ltag+48][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0} or {1}".format(probeTriggerDMuSel,probeTriggerDElSel)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+48, x), "histo2d_{0}_{1}".format(2*ltype+ltag+48, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weight")
                histo2D[2*ltype+ltag+52][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0} or {1}".format(probeTriggerDMuSel,probeTriggerDElSel)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+52, x), "histo2d_{0}_{1}".format(2*ltype+ltag+52, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weight")
                histo2D[2*ltype+ltag+56][x] = dfzoscat[4*x+2*ltype+ltag].Filter("{0} or {1}".format(probeTriggerDMuSel,probeTriggerDElSel)).Histo2D(("histo2d_{0}_{1}".format(2*ltype+ltag+56, x), "histo2d_{0}_{1}".format(2*ltype+ltag+56, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal{0}".format(lprobe+1), "ptl{0}".format(lprobe+1),"weight")

    report = []
    for x in range(nCat):
        for ltype in range(2):
            for ltag in range(2):
                report.append(dfzoscat[4*x+2*ltype+ltag].Report())
                if(x != theCat): continue
                print("---------------- SUMMARY 4*{0}+2*{1}+{2} = {3} -------------".format(x,ltype,ltag,4*x+2*ltype+ltag))
                report[4*x+2*ltype+ltag].Print()

    myfile = ROOT.TFile("fillhisto_triggerAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
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

    #puPath = "data/puWeights_UL_{0}.root".format(year)
    puPath = "data/npvWeights_{0}.root".format(year)
    fPuFile = ROOT.TFile(puPath)
    #puWeights = fPuFile.Get("puWeights")
    puWeights = fPuFile.Get("npvWeights")
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
    histoFakeEtaPt_mu = fFakeFile.Get("histoFakeEffSelEtaPt_0_6")
    histoFakeEtaPt_el = fFakeFile.Get("histoFakeEffSelEtaPt_0_7")
    histoFakeEtaPt_mu.SetDirectory(0)
    histoFakeEtaPt_el.SetDirectory(0)
    fFakeFile.Close()

    lepSFPath = "data/histoLepSFEtaPt_{0}.root".format(year)
    fLepSFFile = ROOT.TFile(lepSFPath)
    histoLepSFEtaPt_mu = fLepSFFile.Get("histoLepSFEtaPt_0_6")
    histoLepSFEtaPt_el = fLepSFFile.Get("histoLepSFEtaPt_0_7")
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

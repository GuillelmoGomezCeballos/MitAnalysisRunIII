import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(4)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson, getLumi
from utilsSelection import selectionTauVeto, selectionPhoton, selectionJetMet, selection2LVar, selectionTrigger2L, selectionElMu, selectionWeigths
#from utilsAna import loadCorrectionSet

# 0 = T, 1 = M, 2 = L
bTagSel = 1

useFR = 0

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

FAKE_MU   = "(abs(Muon_dxy) < 0.2 && abs(Muon_dz) < 0.5 && abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mediumId == true && Muon_pfIsoId >= 4)"
TIGHT_MU0 = jsonObject['TIGHT_MU0']
TIGHT_MU1 = jsonObject['TIGHT_MU1']
TIGHT_MU2 = jsonObject['TIGHT_MU2']
TIGHT_MU3 = jsonObject['TIGHT_MU3']
TIGHT_MU4 = jsonObject['TIGHT_MU4']
TIGHT_MU5 = jsonObject['TIGHT_MU5']
TIGHT_MU6 = jsonObject['TIGHT_MU6']
TIGHT_MU7 = jsonObject['TIGHT_MU7']

FAKE_EL   = "(abs(Electron_dxy) < 0.2 && abs(Electron_dz) < 0.5 && abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_cutBased >= 3)"
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

    dftag = selectionElMu(dftag,year,FAKE_MU,TIGHT_MU0,FAKE_EL,TIGHT_EL0)

    dftag = (dftag.Define("tight_mu0", "{0}".format(TIGHT_MU0))
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

                  .Filter("nLoose >= 2","At least two loose leptons")
                  .Filter("nLoose == 2","Only two loose leptons")
                  .Filter("nFake == 2","Two fake leptons")
                  .Filter("nTight == 2","Two tight leptons")

                  .Filter("(Sum(fake_mu) > 0 and Max(fake_Muon_pt) > 25) or (Sum(fake_el) > 0 and Max(fake_Electron_pt) > 25)","At least one high pt lepton")
                  )

    dftag = selectionTauVeto(dftag,year,isData)
    dftag = selectionPhoton (dftag,year,BARRELphotons,ENDCAPphotons)
    dftag = selectionJetMet (dftag,year,bTagSel,isData)
    dftag = selection2LVar  (dftag,year)

    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob,nPDFReplicas,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    xPtbins = array('d', [10,15,20,25,30,35,40,50,60,70,85,100,200,1000])
    xEtabins = array('d', [0.0,1.0,1.5,2.0,2.5])

    xPtTrgbins = array('d', [10,15,20,25,30,35,40,50,60,70,90,120,200,1000])

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 300
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

    dfbase = selectionLL(df,year,PDType,isData)

    dfbase = selectionWeigths(dfbase,isData,year,PDType,weight,useFR,bTagSel,nPDFReplicas)

    xMllMin = [91.1876-15,  30, 91.1876-15]
    xMllMax = [91.1876+15, 330, 91.1876+15]
    dfcat = []
    dfzllcat = []
    dfjetcat = []
    dfzgcat = []
    dfzemcat = []
    dfzmecat = []
    for x in range(nCat):
        for ltype in range(3):
            dfcat.append(dfbase.Filter("DiLepton_flavor=={0}".format(ltype), "flavor type == {0}".format(ltype))
                               .Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                               .Define("theCat{0}".format(x), "compute_category({0},kPlotNonPrompt,nFake,nTight)".format(theCat))
                               .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x))
                               )

            dfzgcat.append(dfcat[3*x+ltype].Filter("Sum(fake_Muon_charge)+Sum(fake_Muon_charge) == 0 && ptl1 > 25 && ptl2 > 20 && mll > 10 && Sum(good_Photons) > 0 && Max(good_Photons_pt) > 20")
              .Define("kPlotDY", "{0}".format(plotCategory("kPlotDY")))
              .Filter("theCat{0}!=kPlotDY".format(x))
              .Define("ptg", "compute_met_lepton_gamma_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, MET_pt, MET_phi, good_Photons_pt, good_Photons_eta, good_Photons_phi, 6)")
              .Define("mllg","compute_met_lepton_gamma_var(good_Jet_pt, good_Jet_eta, good_Jet_phi, good_Jet_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, fake_Muon_pt, fake_Muon_eta, fake_Muon_phi, fake_Muon_mass, MET_pt, MET_phi, good_Photons_pt, good_Photons_eta, good_Photons_phi, 7)")
            )

            dfcat[3*x+ltype] = dfcat[3*x+ltype].Filter("(DiLepton_flavor != 1 && abs(mll-91.1876) < 15) || (DiLepton_flavor == 1 && mll > 30 && tight_mu6[0] == 1 && tight_el4[0] == 1)","mll cut")

            dfzllcat.append(dfcat[3*x+ltype].Filter("Sum(fake_Muon_charge)+Sum(fake_Electron_charge) == 0", "Opposite-sign leptons"))

            dfjetcat.append(dfzllcat[3*x+ltype].Filter("ngood_jets >= 2", "At least two jets"))

            histo[ltype+ 0][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,x), "histo_{0}_{1}".format(ltype+ 0,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+ 3][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 3,x), "histo_{0}_{1}".format(ltype+ 3,x), 50,  0, 200), "ptll","weight")
            histo[ltype+ 6][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,x), "histo_{0}_{1}".format(ltype+ 6,x), 50,  0, 5),   "drll","weight")
            histo[ltype+ 9][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 9,x), "histo_{0}_{1}".format(ltype+ 9,x), 50,  0, 3.1416), "dphill","weight")
            histo[ltype+12][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+12,x), "histo_{0}_{1}".format(ltype+12,x), 40,  0, 200), "ptl1","weight")
            histo[ltype+15][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+15,x), "histo_{0}_{1}".format(ltype+15,x), 40,  0, 200), "ptl2","weight")
            histo[ltype+18][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+18,x), "histo_{0}_{1}".format(ltype+18,x), 25,  0,2.5), "etal1","weight")
            histo[ltype+21][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+21,x), "histo_{0}_{1}".format(ltype+21,x), 25,  0,2.5), "etal2","weight")
            histo[ltype+24][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+24,x), "histo_{0}_{1}".format(ltype+24,x), 10,-0.5, 9.5), "ngood_jets","weight")
            histo[ltype+27][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+27,x), "histo_{0}_{1}".format(ltype+27,x), 10,-0.5, 9.5), "nbtag_goodbtag_Jet_bjet","weight")
            histo[ltype+30][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+30,x), "histo_{0}_{1}".format(ltype+30,x), 80,-0.5,79.5), "PV_npvsGood","weight")

            histo[ltype+33][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+33,x), "histo_{0}_{1}".format(ltype+33,x), 50,0,2000), "mjj","weight")
            histo[ltype+36][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+36,x), "histo_{0}_{1}".format(ltype+36,x), 50,0,400), "ptjj","weight")
            histo[ltype+39][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+39,x), "histo_{0}_{1}".format(ltype+39,x), 50,0,10), "detajj","weight")
            histo[ltype+42][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+42,x), "histo_{0}_{1}".format(ltype+42,x), 50,0,3.1416), "dphijj","weight")
            histo[ltype+45][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+45,x), "histo_{0}_{1}".format(ltype+45,x), 50,0,1), "good_Jet_btagDeepB","weight")
            histo[ltype+48][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+48,x), "histo_{0}_{1}".format(ltype+48,x), 50,30,230), "good_Jet_pt","weight")
            histo[ltype+51][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+51,x), "histo_{0}_{1}".format(ltype+51,x), 50,-5.0,5.0), "good_Jet_eta","weight")
            histo[ltype+54][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+54,x), "histo_{0}_{1}".format(ltype+54,x), 100, 0, 200), "CaloMET_pt","weight")
            histo[ltype+57][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+57,x), "histo_{0}_{1}".format(ltype+57,x), 100, 0, 200), "ChsMET_pt","weight")

            if(ltype == 2):
                histo[61][x] = dfcat[3*x+ltype].Filter("Sum(fake_Muon_charge)+Sum(fake_Muon_charge) == 0&&DiLepton_flavor==2&&tight_el7[0]==true&&tight_el7[1]==true")\
                 .Histo1D(("histo_{0}_{1}".format(61,x), "histo_{0}_{1}".format(61,x), 60, 91.1876-15, 91.1876+15), "mll","weight")
                histo[62][x] = dfcat[3*x+ltype].Filter("Sum(fake_Muon_charge)+Sum(fake_Muon_charge) != 0&&DiLepton_flavor==2&&tight_el7[0]==true&&tight_el7[1]==true")\
                 .Histo1D(("histo_{0}_{1}".format(62,x), "histo_{0}_{1}".format(62,x), 60, 91.1876-15, 91.1876+15), "mll","weight")
                coutWSStudy = 0
                for j1 in (0.0, 0.5, 1.0, 1.5, 2.0):
                    for j2 in (0.0, 0.5, 1.0, 1.5, 2.0):
                        histo[63+coutWSStudy][x] = dfcat[3*x+ltype].Filter("Sum(fake_Muon_charge)+Sum(fake_Muon_charge) == 0&&DiLepton_flavor==2&&tight_el7[0]==true&&tight_el7[1]==true")\
                         .Filter("etal1>=0.0+{0}&&etal1<0.5+{0}&&etal2>=0.0+{1}&&etal2<0.5+{1}".format(j1,j2))\
                         .Histo1D(("histo_{0}_{1}".format(63+coutWSStudy,x), "histo_{0}_{1}".format(63+coutWSStudy,x), 60, 91.1876-15, 91.1876+15), "mll","weight")
                        histo[64+coutWSStudy][x] = dfcat[3*x+ltype].Filter("Sum(fake_Muon_charge)+Sum(fake_Muon_charge) != 0&&DiLepton_flavor==2&&tight_el7[0]==true&&tight_el7[1]==true")\
                         .Filter("etal1>=0.0+{0}&&etal1<0.5+{0}&&etal2>=0.0+{1}&&etal2<0.5+{1}".format(j1,j2))\
                         .Histo1D(("histo_{0}_{1}".format(64+coutWSStudy,x), "histo_{0}_{1}".format(64+coutWSStudy,x), 60, 91.1876-15, 91.1876+15), "mll","weight")
                        coutWSStudy = coutWSStudy + 2

            histo[ltype+130][x] = dfzllcat[3*x+ltype].Filter("etal1<1.5").Histo1D(("histo_{0}_{1}".format(ltype+130,x), "histo_{0}_{1}".format(ltype+130,x), 256, -0.5, 255.5), "muid1","weight")
            histo[ltype+133][x] = dfzllcat[3*x+ltype].Filter("etal1>1.5").Histo1D(("histo_{0}_{1}".format(ltype+133,x), "histo_{0}_{1}".format(ltype+133,x), 256, -0.5, 255.5), "muid1","weight")
            histo[ltype+136][x] = dfzllcat[3*x+ltype].Filter("etal2<1.5").Histo1D(("histo_{0}_{1}".format(ltype+136,x), "histo_{0}_{1}".format(ltype+136,x), 256, -0.5, 255.5), "muid2","weight")
            histo[ltype+139][x] = dfzllcat[3*x+ltype].Filter("etal2>1.5").Histo1D(("histo_{0}_{1}".format(ltype+139,x), "histo_{0}_{1}".format(ltype+139,x), 256, -0.5, 255.5), "muid2","weight")
            histo[ltype+142][x] = dfzllcat[3*x+ltype].Filter("etal1<1.5").Histo1D(("histo_{0}_{1}".format(ltype+142,x), "histo_{0}_{1}".format(ltype+142,x), 256, -0.5, 255.5), "elid1","weight")
            histo[ltype+145][x] = dfzllcat[3*x+ltype].Filter("etal1>1.5").Histo1D(("histo_{0}_{1}".format(ltype+145,x), "histo_{0}_{1}".format(ltype+145,x), 256, -0.5, 255.5), "elid1","weight")
            histo[ltype+148][x] = dfzllcat[3*x+ltype].Filter("etal2<1.5").Histo1D(("histo_{0}_{1}".format(ltype+148,x), "histo_{0}_{1}".format(ltype+148,x), 256, -0.5, 255.5), "elid2","weight")
            histo[ltype+151][x] = dfzllcat[3*x+ltype].Filter("etal2>1.5").Histo1D(("histo_{0}_{1}".format(ltype+151,x), "histo_{0}_{1}".format(ltype+151,x), 256, -0.5, 255.5), "elid2","weight")

            histo[ltype+154][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+154,x), "histo_{0}_{1}".format(ltype+154,x), 100, 0, 200), "MET_pt","weight")
            histo[ltype+157][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+157,x), "histo_{0}_{1}".format(ltype+157,x), 100, 0, 200), "PuppiMET_pt","weight")

            if(ltype == 0):
                histo[160][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(160,x), "histo_{0}_{1}".format(160,x), 100, 0, 1.0), "fake_Muon_mvaTTH","weight")
            if(ltype == 2):
                histo[161][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(161,x), "histo_{0}_{1}".format(161,x), 100, 0, 1.0), "fake_Muon_mvaTTH","weight")

            histo[ltype+170][x] = dfzgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+170,x), "histo_{0}_{1}".format(ltype+170,x), 40, 10, 210), "mllg","weight")
            dfzgcat[3*x+ltype] = dfzgcat[3*x+ltype].Filter("abs(mllg-91.1876)<15")
            histo[ltype+173][x] = dfzgcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+173,x), "histo_{0}_{1}".format(ltype+173,x), 20, 20, 120), "ptg","weight")

            histo[ltype+176][x] = dfzllcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+176,x), "histo_{0}_{1}".format(ltype+176,x), 100, 0, 200), "TkMET_pt","weight")

            histo[ltype+179][x] = dfzllcat[3*x+ltype].Filter("triggerMUEG> 0").Histo1D(("histo_{0}_{1}".format(ltype+179,x), "histo_{0}_{1}".format(ltype+179,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+182][x] = dfzllcat[3*x+ltype].Filter("triggerDMU > 0").Histo1D(("histo_{0}_{1}".format(ltype+182,x), "histo_{0}_{1}".format(ltype+182,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+185][x] = dfzllcat[3*x+ltype].Filter("triggerSMU > 0").Histo1D(("histo_{0}_{1}".format(ltype+185,x), "histo_{0}_{1}".format(ltype+185,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+188][x] = dfzllcat[3*x+ltype].Filter("triggerDEL > 0").Histo1D(("histo_{0}_{1}".format(ltype+188,x), "histo_{0}_{1}".format(ltype+188,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+191][x] = dfzllcat[3*x+ltype].Filter("triggerSEL > 0").Histo1D(("histo_{0}_{1}".format(ltype+191,x), "histo_{0}_{1}".format(ltype+191,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+194][x] = dfzllcat[3*x+ltype].Filter("triggerMUEG == 0 && triggerDMU > 0")                                                         .Histo1D(("histo_{0}_{1}".format(ltype+194,x), "histo_{0}_{1}".format(ltype+194,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+197][x] = dfzllcat[3*x+ltype].Filter("triggerMUEG == 0 && triggerDMU == 0 && triggerSMU > 0")                                      .Histo1D(("histo_{0}_{1}".format(ltype+197,x), "histo_{0}_{1}".format(ltype+197,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+200][x] = dfzllcat[3*x+ltype].Filter("triggerMUEG == 0 && triggerDMU == 0 && triggerSMU == 0 && triggerDEL > 0")                   .Histo1D(("histo_{0}_{1}".format(ltype+200,x), "histo_{0}_{1}".format(ltype+200,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            histo[ltype+203][x] = dfzllcat[3*x+ltype].Filter("triggerMUEG == 0 && triggerDMU == 0 && triggerSMU == 0 && triggerDEL == 0 && triggerSEL > 0").Histo1D(("histo_{0}_{1}".format(ltype+203,x), "histo_{0}_{1}".format(ltype+203,x), 60, xMllMin[ltype], xMllMax[ltype]), "mll","weight")
            if(ltype == 1):
                dfzmecat.append(dfzllcat[3*x+ltype].Filter("triggerSMU > 0 && fake_Muon_pt[0] > 30")
                                                  .Define("pttag","Max(fake_Muon_pt)")
                                                  .Define("ptprobe","Max(fake_Electron_pt)")
                                                  )
                dfzemcat.append(dfzllcat[3*x+ltype].Filter("triggerSEL > 0 && fake_Electron_pt[0] > 30")
                                                  .Define("pttag","Max(fake_Electron_pt)")
                                                  .Define("ptprobe","Max(fake_Muon_pt)")
                                                  )
                histo[206][x] = dfzmecat[x].Histo1D(("histo_{0}_{1}".format(206,x), "histo_{0}_{1}".format(206,x), 20, 30, 130), "pttag","weight")
                histo[207][x] = dfzemcat[x].Histo1D(("histo_{0}_{1}".format(207,x), "histo_{0}_{1}".format(207,x), 20, 30, 130), "pttag","weight")

                dfzmecat[x] = dfzmecat[x].Filter("hasTriggerMatch(fake_Muon_eta[0],fake_Muon_phi[0],TrigObj_eta,TrigObj_phi)")
                dfzemcat[x] = dfzemcat[x].Filter("hasTriggerMatch(fake_Electron_eta[0],fake_Electron_phi[0],TrigObj_eta,TrigObj_phi)")

                histo[208][x] = dfzmecat[x].Histo1D(("histo_{0}_{1}".format(208,x), "histo_{0}_{1}".format(208,x), 20, 30, 130), "pttag","weight")
                histo[209][x] = dfzemcat[x].Histo1D(("histo_{0}_{1}".format(209,x), "histo_{0}_{1}".format(209,x), 20, 30, 130), "pttag","weight")
                histo[210][x] = dfzmecat[x].Histo1D(("histo_{0}_{1}".format(210,x), "histo_{0}_{1}".format(210,x), len(xPtTrgbins)-1, xPtTrgbins), "ptprobe","weight")
                histo[211][x] = dfzemcat[x].Histo1D(("histo_{0}_{1}".format(211,x), "histo_{0}_{1}".format(211,x), len(xPtTrgbins)-1, xPtTrgbins), "ptprobe","weight")

                histo[212][x] = dfzmecat[x].Filter("triggerMUEG > 0").Histo1D(("histo_{0}_{1}".format(212,x), "histo_{0}_{1}".format(212,x), len(xPtTrgbins)-1, xPtTrgbins), "ptprobe","weight")
                histo[213][x] = dfzemcat[x].Filter("triggerMUEG > 0").Histo1D(("histo_{0}_{1}".format(213,x), "histo_{0}_{1}".format(213,x), len(xPtTrgbins)-1, xPtTrgbins), "ptprobe","weight")

                histo[214][x] = dfzmecat[x].Filter("triggerSEL  > 0").Histo1D(("histo_{0}_{1}".format(214,x), "histo_{0}_{1}".format(214,x), len(xPtTrgbins)-1, xPtTrgbins), "ptprobe","weight")
                histo[215][x] = dfzemcat[x].Filter("triggerSMU  > 0").Histo1D(("histo_{0}_{1}".format(215,x), "histo_{0}_{1}".format(215,x), len(xPtTrgbins)-1, xPtTrgbins), "ptprobe","weight")

            if(ltype == 0):
                histo2D[ 0][x] = dfzllcat[3*x+ltype]                               .Histo2D(("histo2d_{0}_{1}".format( 0, x), "histo2d_{0}_{1}".format( 0, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[ 1][x] = dfzllcat[3*x+ltype].Filter("tight_mu0[0] == true").Histo2D(("histo2d_{0}_{1}".format( 1, x), "histo2d_{0}_{1}".format( 1, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[ 2][x] = dfzllcat[3*x+ltype].Filter("tight_mu1[0] == true").Histo2D(("histo2d_{0}_{1}".format( 2, x), "histo2d_{0}_{1}".format( 2, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[ 3][x] = dfzllcat[3*x+ltype].Filter("tight_mu2[0] == true").Histo2D(("histo2d_{0}_{1}".format( 3, x), "histo2d_{0}_{1}".format( 3, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[ 4][x] = dfzllcat[3*x+ltype].Filter("tight_mu3[0] == true").Histo2D(("histo2d_{0}_{1}".format( 4, x), "histo2d_{0}_{1}".format( 4, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[ 5][x] = dfzllcat[3*x+ltype].Filter("tight_mu4[0] == true").Histo2D(("histo2d_{0}_{1}".format( 5, x), "histo2d_{0}_{1}".format( 5, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[ 6][x] = dfzllcat[3*x+ltype].Filter("tight_mu5[0] == true").Histo2D(("histo2d_{0}_{1}".format( 6, x), "histo2d_{0}_{1}".format( 6, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[ 7][x] = dfzllcat[3*x+ltype].Filter("tight_mu6[0] == true").Histo2D(("histo2d_{0}_{1}".format( 7, x), "histo2d_{0}_{1}".format( 7, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[ 8][x] = dfzllcat[3*x+ltype].Filter("tight_mu7[0] == true").Histo2D(("histo2d_{0}_{1}".format( 8, x), "histo2d_{0}_{1}".format( 8, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")

                histo2D[10][x] = dfzllcat[3*x+ltype]                               .Histo2D(("histo2d_{0}_{1}".format(10, x), "histo2d_{0}_{1}".format(10, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[11][x] = dfzllcat[3*x+ltype].Filter("tight_mu0[1] == true").Histo2D(("histo2d_{0}_{1}".format(11, x), "histo2d_{0}_{1}".format(11, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[12][x] = dfzllcat[3*x+ltype].Filter("tight_mu1[1] == true").Histo2D(("histo2d_{0}_{1}".format(12, x), "histo2d_{0}_{1}".format(12, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[13][x] = dfzllcat[3*x+ltype].Filter("tight_mu2[1] == true").Histo2D(("histo2d_{0}_{1}".format(13, x), "histo2d_{0}_{1}".format(13, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[14][x] = dfzllcat[3*x+ltype].Filter("tight_mu3[1] == true").Histo2D(("histo2d_{0}_{1}".format(14, x), "histo2d_{0}_{1}".format(14, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[15][x] = dfzllcat[3*x+ltype].Filter("tight_mu4[1] == true").Histo2D(("histo2d_{0}_{1}".format(15, x), "histo2d_{0}_{1}".format(15, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[16][x] = dfzllcat[3*x+ltype].Filter("tight_mu5[1] == true").Histo2D(("histo2d_{0}_{1}".format(16, x), "histo2d_{0}_{1}".format(16, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[17][x] = dfzllcat[3*x+ltype].Filter("tight_mu6[1] == true").Histo2D(("histo2d_{0}_{1}".format(17, x), "histo2d_{0}_{1}".format(17, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[18][x] = dfzllcat[3*x+ltype].Filter("tight_mu7[1] == true").Histo2D(("histo2d_{0}_{1}".format(18, x), "histo2d_{0}_{1}".format(18, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")

            if(ltype == 2):
                histo2D[20][x] = dfzllcat[3*x+ltype]                               .Histo2D(("histo2d_{0}_{1}".format(20, x), "histo2d_{0}_{1}".format(20, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[21][x] = dfzllcat[3*x+ltype].Filter("tight_el0[0] == true").Histo2D(("histo2d_{0}_{1}".format(21, x), "histo2d_{0}_{1}".format(21, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[22][x] = dfzllcat[3*x+ltype].Filter("tight_el1[0] == true").Histo2D(("histo2d_{0}_{1}".format(22, x), "histo2d_{0}_{1}".format(22, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[23][x] = dfzllcat[3*x+ltype].Filter("tight_el2[0] == true").Histo2D(("histo2d_{0}_{1}".format(23, x), "histo2d_{0}_{1}".format(23, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[24][x] = dfzllcat[3*x+ltype].Filter("tight_el3[0] == true").Histo2D(("histo2d_{0}_{1}".format(24, x), "histo2d_{0}_{1}".format(24, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[25][x] = dfzllcat[3*x+ltype].Filter("tight_el4[0] == true").Histo2D(("histo2d_{0}_{1}".format(25, x), "histo2d_{0}_{1}".format(25, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[26][x] = dfzllcat[3*x+ltype].Filter("tight_el5[0] == true").Histo2D(("histo2d_{0}_{1}".format(26, x), "histo2d_{0}_{1}".format(26, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[27][x] = dfzllcat[3*x+ltype].Filter("tight_el6[0] == true").Histo2D(("histo2d_{0}_{1}".format(27, x), "histo2d_{0}_{1}".format(27, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")
                histo2D[28][x] = dfzllcat[3*x+ltype].Filter("tight_el7[0] == true").Histo2D(("histo2d_{0}_{1}".format(28, x), "histo2d_{0}_{1}".format(28, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal1", "ptl1","weight")

                histo2D[30][x] = dfzllcat[3*x+ltype]                               .Histo2D(("histo2d_{0}_{1}".format(30, x), "histo2d_{0}_{1}".format(30, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[31][x] = dfzllcat[3*x+ltype].Filter("tight_el0[1] == true").Histo2D(("histo2d_{0}_{1}".format(31, x), "histo2d_{0}_{1}".format(31, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[32][x] = dfzllcat[3*x+ltype].Filter("tight_el1[1] == true").Histo2D(("histo2d_{0}_{1}".format(32, x), "histo2d_{0}_{1}".format(32, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[33][x] = dfzllcat[3*x+ltype].Filter("tight_el2[1] == true").Histo2D(("histo2d_{0}_{1}".format(33, x), "histo2d_{0}_{1}".format(33, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[34][x] = dfzllcat[3*x+ltype].Filter("tight_el3[1] == true").Histo2D(("histo2d_{0}_{1}".format(34, x), "histo2d_{0}_{1}".format(34, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[35][x] = dfzllcat[3*x+ltype].Filter("tight_el4[1] == true").Histo2D(("histo2d_{0}_{1}".format(35, x), "histo2d_{0}_{1}".format(35, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[36][x] = dfzllcat[3*x+ltype].Filter("tight_el5[1] == true").Histo2D(("histo2d_{0}_{1}".format(36, x), "histo2d_{0}_{1}".format(36, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[37][x] = dfzllcat[3*x+ltype].Filter("tight_el6[1] == true").Histo2D(("histo2d_{0}_{1}".format(37, x), "histo2d_{0}_{1}".format(37, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")
                histo2D[38][x] = dfzllcat[3*x+ltype].Filter("tight_el7[1] == true").Histo2D(("histo2d_{0}_{1}".format(38, x), "histo2d_{0}_{1}".format(38, x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "etal2", "ptl2","weight")

    report = []
    for x in range(nCat):
        for ltype in range(3):
            report.append(dfjetcat[3*x+ltype].Report())
            if(x != theCat): continue
            print("---------------- SUMMARY 3*{0}+{1} = {2} -------------".format(x,ltype,3*x+ltype))
            report[3*x+ltype].Print()

    myfile = ROOT.TFile("fillhisto_zAnalysis_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
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
        elif(process > 1000):
            readDASample(process,year,skimType,whichJob,group,puWeights,histoBTVEffEtaPtLF,histoBTVEffEtaPtCJ,histoBTVEffEtaPtBJ,histoElRecoSF,histoElSelSF,histoMuIDSF,histoMuISOSF,histoFakeEtaPt_mu,histoFakeEtaPt_el,histoLepSFEtaPt_mu,histoLepSFEtaPt_el,histoTriggerSFEtaPt_0_0,histoTriggerSFEtaPt_0_1,histoTriggerSFEtaPt_0_2,histoTriggerSFEtaPt_0_3,histoTriggerSFEtaPt_1_0,histoTriggerSFEtaPt_1_1,histoTriggerSFEtaPt_1_2,histoTriggerSFEtaPt_1_3,histoTriggerSFEtaPt_2_0,histoTriggerSFEtaPt_2_1,histoTriggerSFEtaPt_2_2,histoTriggerSFEtaPt_2_3,histoTriggerSFEtaPt_3_0,histoTriggerSFEtaPt_3_1,histoTriggerSFEtaPt_3_2,histoTriggerSFEtaPt_3_3)
    except Exception as e:
        print("Error sample: {0}".format(e))

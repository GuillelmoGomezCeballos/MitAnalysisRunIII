import ROOT
import os, sys, getopt
from array import array

ROOT.ROOT.EnableImplicitMT(3)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles

lumi = [0.1, 0.1, 0.1]

TRIGGERFAKEMU = "(HLT_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL)"
TRIGGERFAKEEL = "(HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele15_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30)"

JSON = "isGoodRunLS(isData, run, luminosityBlock)"

def selectionLL(df,year,PDType,isData):

    TRIGGERFAKE = "0"

    if(year == 2018 and PDType == "DoubleMuon"):
        TRIGGERFAKE = TRIGGERFAKEMU
    elif(year == 2018 and PDType == "EGamma"):
        TRIGGERFAKE =  TRIGGERFAKEEL
    elif(year == 2018):
        TRIGGERFAKE = "{0} or {1}".format(TRIGGERFAKEMU,TRIGGERFAKEEL)
    else:
        print("PROBLEM with triggers!!!")

    print("TRIGGERFAKE: {0}".format(TRIGGERFAKE))

    dftag = df.Define("isData","{}".format(isData))\
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")\
              .Define("trigger","{0}".format(TRIGGERFAKE))\
              .Filter("trigger > 0","Passed trigger1l")\
              .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")\
              .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")\
              .Filter("Sum(loose_mu)+Sum(loose_el) == 1","One skim lepton")\
              .Define("fake_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 1 && Muon_miniIsoId >= 1")\
              .Define("fakemu_pt",    "Muon_pt[fake_mu]")\
              .Define("fakemu_eta",   "abs(Muon_eta[fake_mu])")\
              .Define("fakemu_phi",   "Muon_phi[fake_mu]")\
              .Define("fakemu_mass",  "Muon_mass[fake_mu]")\
              .Define("fakemu_charge","Muon_charge[fake_mu]")\
              .Define("tight_mu0", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mediumId == true && Muon_pfIsoId >= 4")\
              .Define("tight_mu1", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_tightId == true && Muon_pfIsoId >= 4")\
              .Define("tight_mu2", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 2 && Muon_miniIsoId >= 2")\
              .Define("tight_mu3", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 3 && Muon_miniIsoId >= 3")\
              .Define("tight_mu4", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 2 && Muon_miniIsoId >= 3")\
              .Define("tight_mu5", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 3 && Muon_pfIsoId >= 4")\
              .Define("tight_mu6", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_tightId == true && Muon_mvaTTH > 0.7")\
              .Define("tight_mu7", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 4 && Muon_miniIsoId >= 4")\
              .Define("fake_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2")\
              .Define("fakeel_pt",    "Electron_pt[fake_el]")\
              .Define("fakeel_eta",   "abs(Electron_eta[fake_el])")\
              .Define("fakeel_phi",   "Electron_phi[fake_el]")\
              .Define("fakeel_mass",  "Electron_mass[fake_el]")\
              .Define("fakeel_charge","Electron_charge[fake_el]")\
              .Define("tight_el0", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_cutBased >= 3")\
              .Define("tight_el1", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_cutBased >= 4")\
              .Define("tight_el2", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaFall17V2Iso_WP90 == true")\
              .Define("tight_el3", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaFall17V2Iso_WP80 == true")\
              .Define("tight_el4", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaTTH > 0.7")\
              .Define("tight_el5", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_cutBased >= 4 && Electron_tightCharge == 2")\
              .Define("tight_el6", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaFall17V2Iso_WP80 == true && Electron_tightCharge == 2")\
              .Define("tight_el7", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaTTH > 0.7 && Electron_tightCharge == 2")\
              .Filter("Sum(fake_mu)+Sum(fake_el) == 1","One fake lepton")\
              .Define("jet_mask1", "cleaningMask(Muon_jetIdx[fake_mu],nJet)")\
              .Define("jet_mask2", "cleaningMask(Electron_jetIdx[fake_el],nJet)")\
              .Define("good_jet", "abs(Jet_eta) < 4.7 && Jet_pt > 30 && jet_mask1 && jet_mask2")\
              .Define("ngood_jets", "Sum(good_jet)")\
              .Define("goodjet_pt",    "Jet_pt[good_jet]")\
              .Define("goodjet_eta",   "Jet_eta[good_jet]")\
              .Define("goodjet_phi",   "Jet_phi[good_jet]")\
              .Define("goodjet_mass",  "Jet_mass[good_jet]")\
              .Define("mt",      "compute_lmet_var(fakemu_pt, fakemu_phi, fakeel_pt, fakeel_phi, MET_pt, MET_phi,0)")\
              .Define("dphilmet","compute_lmet_var(fakemu_pt, fakemu_phi, fakeel_pt, fakeel_phi, MET_pt, MET_phi,1)")\
              .Define("mtfix",   "compute_lmet_var(fakemu_pt, fakemu_phi, fakeel_pt, fakeel_phi, MET_pt, MET_phi,2)")\
              .Define("maxmtmet","compute_lmet_var(fakemu_pt, fakemu_phi, fakeel_pt, fakeel_phi, MET_pt, MET_phi,3)")\
              .Define("minmtmet","compute_lmet_var(fakemu_pt, fakemu_phi, fakeel_pt, fakeel_phi, MET_pt, MET_phi,4)")

    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    xPtbins = array('d', [10.0, 15.0, 20.0, 25.0, 30.0, 35.0])
    xEtabins = array('d', [0.0, 1.0, 1.5, 2.0, 2.5])

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 100
    histo   = [[0 for y in range(nCat)] for x in range(nHisto)]
    histo2D = [[0 for y in range(nCat)] for x in range(nHisto)]

    dfbase = selectionLL(df,year,PDType,isData)

    if(theCat == plotCategory("kPlotData")):
        dfbase = dfbase.Define("weight","1.0")
    else:
        dfbase = dfbase.Define("PDType","\"{0}\"".format(PDType))\
                       .Define("weight","compute_weights({0},genWeight,PDType)".format(weight))

    dfcat = []
    for y in range(nCat):
        for ltype in range(2):
            dfcat.append(dfbase.Filter("Sum(fake_mu)+2*Sum(fake_el)-1=={0}".format(ltype), "flavor type == {0}".format(ltype))
                               .Define("theCat{0}".format(y), "compute_category({0})".format(theCat))
                               .Filter("theCat{0}=={1}".format(y,y), "correct category ({0})".format(y)))

            histo[ltype+ 0][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,y), "histo_{0}_{1}".format(ltype+ 0,y),100, 0, 200), "mt","weight")
            histo[ltype+ 2][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 2,y), "histo_{0}_{1}".format(ltype+ 2,y),50,  0, 3.1416), "dphilmet","weight")
            histo[ltype+ 4][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 4,y), "histo_{0}_{1}".format(ltype+ 4,y),100, 0, 200), "MET_pt","weight")
            histo[ltype+ 6][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,y), "histo_{0}_{1}".format(ltype+ 6,y),100, 0, 200), "mtfix","weight")
            if(ltype == 0):
                histo[ltype+ 8][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 8,y), "histo_{0}_{1}".format(ltype+ 8,y),50, 10, 60), "fakemu_pt","weight")
                histo[ltype+10][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+10,y), "histo_{0}_{1}".format(ltype+10,y),50,0.0,2.5), "fakemu_eta","weight")
                histo[ltype+12][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1").Histo1D(("histo_{0}_{1}".format(ltype+12,y), "histo_{0}_{1}".format(ltype+12,y),50, 10, 60), "fakemu_pt","weight")
                histo[ltype+14][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1").Histo1D(("histo_{0}_{1}".format(ltype+14,y), "histo_{0}_{1}".format(ltype+14,y),50,0.0,2.5), "fakemu_eta","weight")
                histo[ltype+16][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 10 && Max(fakemu_pt) < 15 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+16,y), "histo_{0}_{1}".format(ltype+16,y),100, 0, 200), "mtfix","weight")
                histo[ltype+18][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 15 && Max(fakemu_pt) < 20 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+18,y), "histo_{0}_{1}".format(ltype+18,y),100, 0, 200), "mtfix","weight")
                histo[ltype+20][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 20 && Max(fakemu_pt) < 25 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+20,y), "histo_{0}_{1}".format(ltype+20,y),100, 0, 200), "mtfix","weight")
                histo[ltype+22][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 25 && Max(fakemu_pt) < 30 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+22,y), "histo_{0}_{1}".format(ltype+22,y),100, 0, 200), "mtfix","weight")
                histo[ltype+24][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 30 && Max(fakemu_pt) < 35 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+24,y), "histo_{0}_{1}".format(ltype+24,y),100, 0, 200), "mtfix","weight")
                histo[ltype+26][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 35 && Max(fakemu_pt) < 40 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+26,y), "histo_{0}_{1}".format(ltype+26,y),100, 0, 200), "mtfix","weight")
                histo[ltype+28][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 10 && Max(fakemu_pt) < 15").Histo1D(("histo_{0}_{1}".format(ltype+28,y), "histo_{0}_{1}".format(ltype+28,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+30][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 15 && Max(fakemu_pt) < 20").Histo1D(("histo_{0}_{1}".format(ltype+30,y), "histo_{0}_{1}".format(ltype+30,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+32][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 20 && Max(fakemu_pt) < 25").Histo1D(("histo_{0}_{1}".format(ltype+32,y), "histo_{0}_{1}".format(ltype+32,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+34][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 25 && Max(fakemu_pt) < 30").Histo1D(("histo_{0}_{1}".format(ltype+34,y), "histo_{0}_{1}".format(ltype+34,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+36][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 30 && Max(fakemu_pt) < 35").Histo1D(("histo_{0}_{1}".format(ltype+36,y), "histo_{0}_{1}".format(ltype+36,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+38][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 35 && Max(fakemu_pt) < 40").Histo1D(("histo_{0}_{1}".format(ltype+38,y), "histo_{0}_{1}".format(ltype+38,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+40][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && Max(fakemu_eta) < 1.5 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+40,y), "histo_{0}_{1}".format(ltype+40,y), len(xPtbins)-1, xPtbins), "fakemu_pt","weight")

                histo2D[ltype+ 0][y] = dfcat[2*y+ltype].Filter("maxmtmet < 30")                     .Histo2D(("histo2d_{0}_{1}".format(ltype+ 0,y), "histo2d_{0}_{1}".format(ltype+ 0,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+ 2][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu0)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 2,y), "histo2d_{0}_{1}".format(ltype+ 2,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+ 4][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu1)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 4,y), "histo2d_{0}_{1}".format(ltype+ 4,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+ 6][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu2)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 6,y), "histo2d_{0}_{1}".format(ltype+ 6,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+ 8][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu3)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 8,y), "histo2d_{0}_{1}".format(ltype+ 8,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+10][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu4)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+10,y), "histo2d_{0}_{1}".format(ltype+10,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+12][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu5)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+12,y), "histo2d_{0}_{1}".format(ltype+12,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+14][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu6)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+14,y), "histo2d_{0}_{1}".format(ltype+14,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+16][y] = dfcat[2*y+ltype].Filter("Sum(tight_mu7)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+16,y), "histo2d_{0}_{1}".format(ltype+16,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")

            else:
                histo[ltype+ 8][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 8,y), "histo_{0}_{1}".format(ltype+ 8,y),50, 10, 60), "fakeel_pt","weight")
                histo[ltype+10][y] = dfcat[2*y+ltype].Histo1D(("histo_{0}_{1}".format(ltype+10,y), "histo_{0}_{1}".format(ltype+10,y),50,0.0,2.5), "fakeel_eta","weight")
                histo[ltype+12][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1").Histo1D(("histo_{0}_{1}".format(ltype+12,y), "histo_{0}_{1}".format(ltype+12,y),50, 10, 60), "fakeel_pt","weight")
                histo[ltype+14][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1").Histo1D(("histo_{0}_{1}".format(ltype+14,y), "histo_{0}_{1}".format(ltype+14,y),50,0.0,2.5), "fakeel_eta","weight")
                histo[ltype+16][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 10 && Max(fakeel_pt) < 15 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+16,y), "histo_{0}_{1}".format(ltype+16,y),100, 0, 200), "mtfix","weight")
                histo[ltype+18][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 15 && Max(fakeel_pt) < 20 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+18,y), "histo_{0}_{1}".format(ltype+18,y),100, 0, 200), "mtfix","weight")
                histo[ltype+20][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 20 && Max(fakeel_pt) < 25 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+20,y), "histo_{0}_{1}".format(ltype+20,y),100, 0, 200), "mtfix","weight")
                histo[ltype+22][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 25 && Max(fakeel_pt) < 30 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+22,y), "histo_{0}_{1}".format(ltype+22,y),100, 0, 200), "mtfix","weight")
                histo[ltype+24][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 30 && Max(fakeel_pt) < 35 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+24,y), "histo_{0}_{1}".format(ltype+24,y),100, 0, 200), "mtfix","weight")
                histo[ltype+26][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 35 && Max(fakeel_pt) < 40 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+26,y), "histo_{0}_{1}".format(ltype+26,y),100, 0, 200), "mtfix","weight")
                histo[ltype+28][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 10 && Max(fakeel_pt) < 15").Histo1D(("histo_{0}_{1}".format(ltype+28,y), "histo_{0}_{1}".format(ltype+28,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+30][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 15 && Max(fakeel_pt) < 20").Histo1D(("histo_{0}_{1}".format(ltype+30,y), "histo_{0}_{1}".format(ltype+30,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+32][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 20 && Max(fakeel_pt) < 25").Histo1D(("histo_{0}_{1}".format(ltype+32,y), "histo_{0}_{1}".format(ltype+32,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+34][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 25 && Max(fakeel_pt) < 30").Histo1D(("histo_{0}_{1}".format(ltype+34,y), "histo_{0}_{1}".format(ltype+34,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+36][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 30 && Max(fakeel_pt) < 35").Histo1D(("histo_{0}_{1}".format(ltype+36,y), "histo_{0}_{1}".format(ltype+36,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+38][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 35 && Max(fakeel_pt) < 40").Histo1D(("histo_{0}_{1}".format(ltype+38,y), "histo_{0}_{1}".format(ltype+38,y),100, 0, 200), "maxmtmet","weight")
                histo[ltype+40][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && Max(fakeel_eta) < 1.5 && minmtmet > 60").Histo1D(("histo_{0}_{1}".format(ltype+40,y), "histo_{0}_{1}".format(ltype+40,y), len(xPtbins)-1, xPtbins), "fakeel_pt","weight")

                histo2D[ltype+ 0][y] = dfcat[2*y+ltype].Filter("maxmtmet < 30") 		    .Histo2D(("histo2d_{0}_{1}".format(ltype+ 0,y), "histo2d_{0}_{1}".format(ltype+ 0,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+ 2][y] = dfcat[2*y+ltype].Filter("Sum(tight_el0)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 2,y), "histo2d_{0}_{1}".format(ltype+ 2,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+ 4][y] = dfcat[2*y+ltype].Filter("Sum(tight_el1)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 4,y), "histo2d_{0}_{1}".format(ltype+ 4,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+ 6][y] = dfcat[2*y+ltype].Filter("Sum(tight_el2)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 6,y), "histo2d_{0}_{1}".format(ltype+ 6,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+ 8][y] = dfcat[2*y+ltype].Filter("Sum(tight_el3)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 8,y), "histo2d_{0}_{1}".format(ltype+ 8,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+10][y] = dfcat[2*y+ltype].Filter("Sum(tight_el4)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+10,y), "histo2d_{0}_{1}".format(ltype+10,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+12][y] = dfcat[2*y+ltype].Filter("Sum(tight_el5)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+12,y), "histo2d_{0}_{1}".format(ltype+12,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+14][y] = dfcat[2*y+ltype].Filter("Sum(tight_el6)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+14,y), "histo2d_{0}_{1}".format(ltype+14,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+16][y] = dfcat[2*y+ltype].Filter("Sum(tight_el7)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+16,y), "histo2d_{0}_{1}".format(ltype+16,y), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")

    report = []
    for y in range(nCat):
        for ltype in range(2):
            report.append(dfcat[2*y+ltype].Report())
            if(y != theCat): continue
            print("---------------- SUMMARY 2*{0}+{1} = {2} -------------".format(y,ltype,2*y+ltype))
            report[2*y+ltype].Print()

    myfile = ROOT.TFile("fillhistoFakeAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
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

    weight = (SwitchSample(sampleNOW, skimType)[1] / genEventSumWeight)*lumi[year-2016]
    weightApprox = (SwitchSample(sampleNOW, skimType)[1] / genEventSumNoWeight)*lumi[year-2016]

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

def readDataSample(sampleNOW, year, skimType, whichJob, group):

    PDType = "0"
    if  (sampleNOW >= 1001 and sampleNOW <= 1004): PDType = "SingleMuon"
    elif(sampleNOW >= 1005 and sampleNOW <= 1008): PDType = "DoubleMuon"
    elif(sampleNOW >= 1009 and sampleNOW <= 1012): PDType = "MuonEG"
    elif(sampleNOW >= 1012 and sampleNOW <= 1016): PDType = "EGamma"

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
            sys.exit(0)
        elif(process > 1000):
            readDataSample(process,year,skimType,whichJob,group)
            sys.exit(0)
    except Exception as e:
        print("Error sample: {0}".format(e))

    for i in 1005,1006,1007,1008,1013,1014,1015,1016:
        try:
            readDataSample(i,year,skimType,whichJob,group)
        except Exception as e:
            print("Error sampleDA({0}): {1}".format(i,e))

    for i in range(4):
        try:
            readMCSample(i,year,skimType,whichJob,group)
        except Exception as e:
            print("Error sampleMC({0}): {1}".format(i,e))

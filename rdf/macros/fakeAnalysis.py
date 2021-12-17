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
              .Define("tight_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 3 && Muon_miniIsoId >= 3")\
              .Define("fake_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2")\
              .Define("fakeel_pt",    "Electron_pt[fake_el]")\
              .Define("fakeel_eta",   "abs(Electron_eta[fake_el])")\
              .Define("fakeel_phi",   "Electron_phi[fake_el]")\
              .Define("fakeel_mass",  "Electron_mass[fake_el]")\
              .Define("fakeel_charge","Electron_charge[fake_el]")\
              .Define("tight_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaFall17V2Iso_WP80 == 1")\
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
    histo   = [[0 for x in range(nCat)] for y in range(nHisto)]
    histo2D = [[0 for x in range(nCat)] for y in range(nHisto)]

    dfbase = selectionLL(df,year,PDType,isData)

    if(theCat == plotCategory("kPlotData")):
        dfbase = dfbase.Define("weight","1.0")
    else:
        dfbase = dfbase.Define("PDType","\"{0}\"".format(PDType))\
                       .Define("weight","compute_weights({0},genWeight,PDType)".format(weight))

    dfcat = []
    for x in range(nCat):
        for ltype in range(2):
            dfcat.append(dfbase.Filter("Sum(fake_mu)+2*Sum(fake_el)-1=={0}".format(ltype), "flavor type == {0}".format(ltype))
                               .Define("theCat{0}".format(x), "compute_category({0})".format(theCat))
                               .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x)))

            histo[ltype+ 0][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,x), "histo_{0}_{1}".format(ltype+ 0,x),100, 0, 200), "mt","weight")
            histo[ltype+ 2][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 2,x), "histo_{0}_{1}".format(ltype+ 2,x),50,  0, 3.1416), "dphilmet","weight")
            histo[ltype+ 4][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 4,x), "histo_{0}_{1}".format(ltype+ 4,x),100, 0, 200), "MET_pt","weight")
            histo[ltype+ 6][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,x), "histo_{0}_{1}".format(ltype+ 6,x),100, 0, 200), "mtfix","weight")
            if(ltype == 0):
                histo[ltype+ 8][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 8,x), "histo_{0}_{1}".format(ltype+ 8,x),50, 10, 60), "fakemu_pt","weight")
                histo[ltype+10][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+10,x), "histo_{0}_{1}".format(ltype+10,x),50,0.0,2.5), "fakemu_eta","weight")
                histo[ltype+12][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+12,x), "histo_{0}_{1}".format(ltype+12,x),50, 10, 60), "fakemu_pt","weight")
                histo[ltype+14][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+14,x), "histo_{0}_{1}".format(ltype+14,x),50,0.0,2.5), "fakemu_eta","weight")
                histo[ltype+16][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 10 && Max(fakemu_pt) < 15 && minmtmet > 60", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+16,x), "histo_{0}_{1}".format(ltype+16,x),100, 0, 200), "mtfix","weight")
                histo[ltype+18][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 15 && Max(fakemu_pt) < 20 && minmtmet > 60", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+18,x), "histo_{0}_{1}".format(ltype+18,x),100, 0, 200), "mtfix","weight")
                histo[ltype+20][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 20 && Max(fakemu_pt) < 25 && minmtmet > 60", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+20,x), "histo_{0}_{1}".format(ltype+20,x),100, 0, 200), "mtfix","weight")
                histo[ltype+22][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 25 && Max(fakemu_pt) < 30 && minmtmet > 60", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+22,x), "histo_{0}_{1}".format(ltype+22,x),100, 0, 200), "mtfix","weight")
                histo[ltype+24][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 30 && Max(fakemu_pt) < 35 && minmtmet > 60", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+24,x), "histo_{0}_{1}".format(ltype+24,x),100, 0, 200), "mtfix","weight")
                histo[ltype+26][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 35 && Max(fakemu_pt) < 40 && minmtmet > 60", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+26,x), "histo_{0}_{1}".format(ltype+26,x),100, 0, 200), "mtfix","weight")
                histo[ltype+28][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 10 && Max(fakemu_pt) < 15", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+28,x), "histo_{0}_{1}".format(ltype+28,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+30][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 15 && Max(fakemu_pt) < 20", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+30,x), "histo_{0}_{1}".format(ltype+30,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+32][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 20 && Max(fakemu_pt) < 25", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+32,x), "histo_{0}_{1}".format(ltype+32,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+34][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 25 && Max(fakemu_pt) < 30", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+34,x), "histo_{0}_{1}".format(ltype+34,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+36][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 30 && Max(fakemu_pt) < 35", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+36,x), "histo_{0}_{1}".format(ltype+36,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+38][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && Max(fakemu_pt) > 35 && Max(fakemu_pt) < 40", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+38,x), "histo_{0}_{1}".format(ltype+38,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+40][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && Max(fakemu_eta) < 1.5 && minmtmet > 60","tight_mu==1 and MET").Histo1D(("histo_{0}_{1}".format(ltype+40,x), "histo_{0}_{1}".format(ltype+40,x), len(xPtbins)-1, xPtbins), "fakemu_pt","weight")

                histo2D[ltype+ 0][x] = dfcat[2*x+ltype].Filter("maxmtmet < 30")                    .Histo2D(("histo2d_{0}_{1}".format(ltype+ 0,x), "histo2d_{0}_{1}".format(ltype+ 0,x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")
                histo2D[ltype+ 2][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 2,x), "histo2d_{0}_{1}".format(ltype+ 2,x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakemu_eta", "fakemu_pt","weight")

            else:
                histo[ltype+ 8][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 8,x), "histo_{0}_{1}".format(ltype+ 8,x),50, 10, 60), "fakeel_pt","weight")
                histo[ltype+10][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+10,x), "histo_{0}_{1}".format(ltype+10,x),50,0.0,2.5), "fakeel_eta","weight")
                histo[ltype+12][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+12,x), "histo_{0}_{1}".format(ltype+12,x),50, 10, 60), "fakeel_pt","weight")
                histo[ltype+14][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+14,x), "histo_{0}_{1}".format(ltype+14,x),50,0.0,2.5), "fakeel_eta","weight")
                histo[ltype+16][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 10 && Max(fakeel_pt) < 15 && minmtmet > 60", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+16,x), "histo_{0}_{1}".format(ltype+16,x),100, 0, 200), "mtfix","weight")
                histo[ltype+18][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 15 && Max(fakeel_pt) < 20 && minmtmet > 60", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+18,x), "histo_{0}_{1}".format(ltype+18,x),100, 0, 200), "mtfix","weight")
                histo[ltype+20][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 20 && Max(fakeel_pt) < 25 && minmtmet > 60", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+20,x), "histo_{0}_{1}".format(ltype+20,x),100, 0, 200), "mtfix","weight")
                histo[ltype+22][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 25 && Max(fakeel_pt) < 30 && minmtmet > 60", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+22,x), "histo_{0}_{1}".format(ltype+22,x),100, 0, 200), "mtfix","weight")
                histo[ltype+24][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 30 && Max(fakeel_pt) < 35 && minmtmet > 60", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+24,x), "histo_{0}_{1}".format(ltype+24,x),100, 0, 200), "mtfix","weight")
                histo[ltype+26][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 35 && Max(fakeel_pt) < 40 && minmtmet > 60", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+26,x), "histo_{0}_{1}".format(ltype+26,x),100, 0, 200), "mtfix","weight")
                histo[ltype+28][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 10 && Max(fakeel_pt) < 15", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+28,x), "histo_{0}_{1}".format(ltype+28,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+30][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 15 && Max(fakeel_pt) < 20", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+30,x), "histo_{0}_{1}".format(ltype+30,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+32][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 20 && Max(fakeel_pt) < 25", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+32,x), "histo_{0}_{1}".format(ltype+32,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+34][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 25 && Max(fakeel_pt) < 30", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+34,x), "histo_{0}_{1}".format(ltype+34,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+36][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 30 && Max(fakeel_pt) < 35", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+36,x), "histo_{0}_{1}".format(ltype+36,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+38][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && Max(fakeel_pt) > 35 && Max(fakeel_pt) < 40", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+38,x), "histo_{0}_{1}".format(ltype+38,x),100, 0, 200), "maxmtmet","weight")
                histo[ltype+40][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && Max(fakeel_eta) < 1.5 && minmtmet > 60","tight_el==1 and MET").Histo1D(("histo_{0}_{1}".format(ltype+40,x), "histo_{0}_{1}".format(ltype+40,x), len(xPtbins)-1, xPtbins), "fakeel_pt","weight")

                histo2D[ltype+ 0][x] = dfcat[2*x+ltype].Filter("maxmtmet < 30")                    .Histo2D(("histo2d_{0}_{1}".format(ltype+ 0,x), "histo2d_{0}_{1}".format(ltype+ 0,x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")
                histo2D[ltype+ 2][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1 && maxmtmet < 30").Histo2D(("histo2d_{0}_{1}".format(ltype+ 2,x), "histo2d_{0}_{1}".format(ltype+ 2,x), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins), "fakeel_eta", "fakeel_pt","weight")

    report = []
    for x in range(nCat):
        for ltype in range(2):
            report.append(dfcat[2*x+ltype].Report())
            if(x != theCat): continue
            print("---------------- SUMMARY 2*{0}+{1} = {2} -------------".format(x,ltype,2*x+ltype))
            report[2*x+ltype].Print()

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
    if  (sampleNOW >= 101 and sampleNOW <= 104): PDType = "SingleMuon"
    elif(sampleNOW >= 105 and sampleNOW <= 108): PDType = "DoubleMuon"
    elif(sampleNOW >= 109 and sampleNOW <= 112): PDType = "MuonEG"
    elif(sampleNOW >= 112 and sampleNOW <= 116): PDType = "EGamma"

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
        if(process >= 0 and process < 100):
            readMCSample(process,year,skimType,whichJob,group)
            sys.exit(0)
        elif(process > 100):
            readDataSample(process,year,skimType,whichJob,group)
            sys.exit(0)
    except Exception as e:
        print("Error sample: {0}".format(e))

    for i in 105,106,107,108,113,114,115,116:
        try:
            readDataSample(i,year,skimType,whichJob,group)
        except Exception as e:
            print("Error sampleDA({0}): {1}".format(i,e))

    for i in range(4):
        try:
            readMCSample(i,year,skimType,whichJob,group)
        except Exception as e:
            print("Error sampleMC({0}): {1}".format(i,e))

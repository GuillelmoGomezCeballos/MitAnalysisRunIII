import ROOT
import os, sys, getopt

ROOT.ROOT.EnableImplicitMT(5)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample

#lumi = [36.1, 41.5, 60.0]
lumi = [36.1, 41.5, 1.0]

TRIGGERFAKEMU = "(HLT_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL)"
TRIGGERFAKEEL = "(HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele15_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30)"

JSON = "isGoodRunLS(isData, run, luminosityBlock)"

def selectionLL(df,year,PDType,isData):

    TRIGGERFAKE = "0"

    if(year == 2018 and PDType == "DoubleMuon"):
        TRIGGERFAKE = TRIGGERFAKEMU
    elif(year == 2018 and PDType == "Egamma"):
        TRIGGERFAKE =  TRIGGERFAKEEL
    elif(year == 2018 and PDType == "All"):
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
              .Define("fakemu_eta",   "Muon_eta[fake_mu]")\
              .Define("fakemu_phi",   "Muon_phi[fake_mu]")\
              .Define("fakemu_mass",  "Muon_mass[fake_mu]")\
              .Define("fakemu_charge","Muon_charge[fake_mu]")\
              .Define("tight_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 3 && Muon_miniIsoId >= 3")\
              .Define("fake_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2")\
              .Define("fakeel_pt",    "Electron_pt[fake_el]")\
              .Define("fakeel_eta",   "Electron_eta[fake_el]")\
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
              .Define("mt",   "compute_lmet_var(fakemu_pt, fakemu_phi, fakeel_pt, fakeel_phi, MET_pt, MET_phi,0)")\
              .Define("dphilmet",   "compute_lmet_var(fakemu_pt, fakemu_phi, fakeel_pt, fakeel_phi, MET_pt, MET_phi,1)")\
              .Define("mtfix",   "compute_lmet_var(fakemu_pt, fakemu_phi, fakeel_pt, fakeel_phi, MET_pt, MET_phi,2)")

    return dftag


def analysis(df,count,category,weight,year,PDType,isData):

    print("starting {0} / {1} / {2} / {3} / {4} / {5}".format(count,category,weight,year,PDType,isData))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 50
    histo = [[0 for x in range(nCat)] for y in range(nHisto)]

    dfbase = selectionLL(df,year,PDType,isData)

    if(theCat == plotCategory("kPlotData")):
        dfbase = dfbase.Define("weight","1.0")
    else:
        dfbase = dfbase.Define("weight","compute_weights({0},genWeight)".format(weight))
    histo[0][0] = dfbase.Histo1D(("histo_{0}_{1}".format(0+ 0,0), "histo_{0}_{1}".format(0+ 0,0),100,  0, 100), "MET_pt","weight")
    dfcat = []
    for x in range(nCat):
        for ltype in range(2):
            dfcat.append(dfbase.Filter("Sum(fake_mu)+2*Sum(fake_el)-1=={0}".format(ltype), "flavor type == {0}".format(ltype))
                               .Define("theCat{0}".format(x), "compute_category({0})".format(theCat))
                               .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x)))

            histo[ltype+ 0][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,x), "histo_{0}_{1}".format(ltype+ 0,x),100,  0, 200), "mt","weight")
            histo[ltype+ 2][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 2,x), "histo_{0}_{1}".format(ltype+ 2,x),100,  0, 3.1416), "dphilmet","weight")
            histo[ltype+ 4][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 4,x), "histo_{0}_{1}".format(ltype+ 4,x),100,  0, 200), "MET_pt","weight")
            histo[ltype+ 6][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,x), "histo_{0}_{1}".format(ltype+ 6,x),100,  0, 200), "mtfix","weight")
            if(ltype == 0):
                histo[ltype+ 8][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 8,x), "histo_{0}_{1}".format(ltype+ 8,x),100,  0, 100), "fakemu_pt","weight")
                histo[ltype+10][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+10,x), "histo_{0}_{1}".format(ltype+10,x),100,-2.5,2.5), "fakemu_eta","weight")
                histo[ltype+12][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+12,x), "histo_{0}_{1}".format(ltype+12,x),100,  0, 100), "fakemu_pt","weight")
                histo[ltype+14][x] = dfcat[2*x+ltype].Filter("Sum(tight_mu)==1", "tight_mu==1").Histo1D(("histo_{0}_{1}".format(ltype+14,x), "histo_{0}_{1}".format(ltype+14,x),100,-2.5,2.5), "fakemu_eta","weight")
                
            else:
                histo[ltype+ 8][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 8,x), "histo_{0}_{1}".format(ltype+ 8,x),100,  0, 100), "fakeel_pt","weight")
                histo[ltype+10][x] = dfcat[2*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+10,x), "histo_{0}_{1}".format(ltype+10,x),100,-2.5,2.5), "fakeel_eta","weight")
                histo[ltype+12][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+12,x), "histo_{0}_{1}".format(ltype+12,x),100,  0, 100), "fakeel_pt","weight")
                histo[ltype+14][x] = dfcat[2*x+ltype].Filter("Sum(tight_el)==1", "tight_el==1").Histo1D(("histo_{0}_{1}".format(ltype+14,x), "histo_{0}_{1}".format(ltype+14,x),100,-2.5,2.5), "fakeel_eta","weight")

    report = []
    for x in range(nCat):
        for ltype in range(2):
            report.append(dfcat[2*x+ltype].Report())
            if(x != theCat): continue
            print("---------------- SUMMARY 2*{0}+{1} = {2} -------------".format(x,ltype,2*x+ltype))
            report[2*x+ltype].Print()

    myfile = ROOT.TFile("fillhistoFakeAna_sample{0}_year{1}.root".format(count,year),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
	    if(histo[j][i] == 0): continue
            if(histo[j][i].GetSumOfWeights() > 0): print("({0},{1}): {2}".format(j,i,histo[j][i].GetSumOfWeights()))
            histo[j][i].Write()
    myfile.Close()


def readMCSample(sampleNOW, year, PDType):

    files = getMClist(sampleNOW)
    print(len(files))
    df = ROOT.RDataFrame("Events", files)

    runTree = ROOT.TChain("Runs")
    for f in range(len(files)):
        runTree.AddFile(files[f])

    genEventSum = 0
    for i in range(runTree.GetEntries()):
        runTree.GetEntry(i)
        genEventSum += runTree.genEventSumw

    weight = (SwitchSample(sampleNOW)[1] / genEventSum)*lumi[year-2016]

    nevents = df.Count().GetValue()

    print("genEventSum({0}): {1} / Events: {2}".format(runTree.GetEntries(),genEventSum,nevents))
    print("Weight %f / Cross section: %f" %(weight,SwitchSample(sampleNOW)[1]))

    #puPath = "../datapuWeights_UL_{0}.root".format(year)
    #fPUFile = ROOT.TFile(puPath)
    #fhDPU     = fPUFile.Get("puWeights")
    #fhDPUUp   = fPUFile.Get("puWeightsUp")
    #fhDPUDown = fPUFile.Get("puWeightsDown")
    #fhDPU    .SetDirectory(0);
    #fhDPUUp  .SetDirectory(0);
    #fhDPUDown.SetDirectory(0);
    #fPUFile.Close()

    analysis(df, sampleNOW, SwitchSample(sampleNOW)[2], weight, year, PDType, "false")

def readDataSample(sampleNOW, year, PDType):

    files = getDATAlist(sampleNOW, year, PDType)
    print(len(files))

    df = ROOT.RDataFrame("Events", files)

    weight=1.
    nevents = df.Count().GetValue()
    print("%s entries in the dataset" %nevents)

    analysis(df, sampleNOW, sampleNOW, weight, year, PDType, "true")

if __name__ == "__main__":

    year = 2018
    test = 0

    valid = ['year=', "test=", 'help']
    usage  =  "Usage: ana.py --year=<{0}>\n".format(year)
    usage +=  "              --test=<{0}>".format(test)
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
        if opt == "--test":
            test = int(arg)

    if(test == 1):
        #readMCSample(10,2018,"All")
        readMCSample(1,2018,"All")
        #readDataSample(103,2018,"Egamma")
        sys.exit(0)
    elif(test > 100):
        readDataSample(test,2018,"Egamma")
        sys.exit(0)

    anaNamesDict = dict()
    anaNamesDict.update({"2":[102,2018,"DoubleMuon"]})
    anaNamesDict.update({"4":[104,2018,"Egamma"]})
    #anaNamesDict.update({"5":[105,2018,"Egamma"]})
    #anaNamesDict.update({"6":[106,2018,"Egamma"]})
    #anaNamesDict.update({"7":[107,2018,"Egamma"]})
    for key in anaNamesDict:
        try:
            readDataSample(anaNamesDict[key][0],anaNamesDict[key][1],anaNamesDict[key][2])
        except Exception as e:
            print("Error sampleDA({0}): {1}".format(key,e))

    for i in range(4):
        try:
            readMCSample(i,2018,"All")
        except Exception as e:
            print("Error sampleMC({0}): {1}".format(i,e))

import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(5)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist, getLumi
from utilsAna import SwitchSample
from utilsSelection import getBTagCut

selectionJsonPath = "config/selection.json"
if(not os.path.exists(selectionJsonPath)):
    selectionJsonPath = "selection.json"

with open(selectionJsonPath) as jsonFile:
    jsonObject = json.load(jsonFile)
    jsonFile.close()

JSON = jsonObject['JSON']

VBSSEL = jsonObject['VBSSEL']

FAKE_MU   = jsonObject['FAKE_MU']
TIGHT_MU0 = jsonObject['TIGHT_MU0']

FAKE_EL   = jsonObject['FAKE_EL']
TIGHT_EL0 = jsonObject['TIGHT_EL0']

def analysis(df,count,category,weight,year,PDType,isData):

    xPtbins = array('d', [20,25,30,35,40,50,60,70,80,90,100,125,150,175,200,300,400,500,1000])
    xEtabins = array('d', [0.0,1.0,1.5,2.0,2.5])

    print("starting {0} / {1} / {2} / {3} / {4} / {5}".format(count,category,weight,year,PDType,isData))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo   = [[0 for x in range(nCat)] for y in range(nHisto)]
    histo2D = [[0 for y in range(nCat)] for x in range(nHisto)]

    dfcat = df.Define("PDType","\"{0}\"".format(PDType))\
              .Define("weight","{0}".format(1.0))\
              .Filter("weight != 0","good weight")

    x = 0
    histo[ 0][x] = dfcat.Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x), 100,  0, 100), "Pileup_nTrueInt","weight")

    dfgen = (dfcat
          .Define("gen_z", "GenPart_pdgId == 23 && GenPart_status == 62")
          .Filter("Sum(gen_z) >= 1","nZ >= 1")
          .Filter("Sum(gen_z) == 1","nZ == 1")
          .Define("Zpt", "GenPart_pt[gen_z]")
          .Define("Zeta", "GenPart_eta[gen_z]")
          .Define("Zphi", "abs(GenPart_phi[gen_z])")
          .Define("Zmass", "GenPart_mass[gen_z]")
          .Filter("abs(Zmass[0]-91.1876) < 15","abs(Zmass[0]-91.1876) < 15")
          .Define("Zrap", "abs(makeRapidity(Zpt[0],Zeta[0],Zphi[0],Zmass[0]))")
            )

    dfcat = (dfcat
          .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")
          .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")
          .Filter("Sum(loose_mu)+Sum(loose_el) == 2","Two loose leptons")
          .Define("fake_mu","{0}".format(FAKE_MU))
          .Define("fake_el","{0}".format(FAKE_EL))
          .Define("nFake","Sum(fake_mu)+Sum(fake_el)")
          .Filter("nFake == 2","Two fake leptons")

          .Define("jet_mask1", "cleaningMask(Muon_jetIdx[fake_mu],nJet)")
          .Define("jet_mask2", "cleaningMask(Electron_jetIdx[fake_el],nJet)")
          .Define("goodloose_jet", "abs(Jet_eta) < 2.5 && Jet_pt > 20 && jet_mask1 && jet_mask2")
          .Define("ngoodloose_jets", "Sum(goodloose_jet)")
          .Define("goodloosejet_pt",           "Jet_pt[goodloose_jet]")
          .Define("goodloosejet_eta",          "abs(Jet_eta[goodloose_jet])")
          .Define("goodloosejet_phi",          "Jet_phi[goodloose_jet]")
          .Define("goodloosejet_mass",         "Jet_mass[goodloose_jet]")
          .Define("goodloosejet_hadronFlavour","Jet_hadronFlavour[goodloose_jet]")
          .Define("goodloosejet_btagDeepB",    "Jet_btagDeepB[goodloose_jet]")
          .Define("goodloosejet_lf",   "goodloosejet_hadronFlavour == 0")
          .Define("goodloosejet_cj",   "goodloosejet_hadronFlavour == 4")
          .Define("goodloosejet_bj",   "goodloosejet_hadronFlavour == 5")
          .Define("goodloosejet_lf_t", "goodloosejet_hadronFlavour == 0 && goodloosejet_btagDeepB > {0}".format(getBTagCut(0)))
          .Define("goodloosejet_cj_t", "goodloosejet_hadronFlavour == 4 && goodloosejet_btagDeepB > {0}".format(getBTagCut(0)))
          .Define("goodloosejet_bj_t", "goodloosejet_hadronFlavour == 5 && goodloosejet_btagDeepB > {0}".format(getBTagCut(0)))
          .Define("goodloosejet_lf_m", "goodloosejet_hadronFlavour == 0 && goodloosejet_btagDeepB > {0}".format(getBTagCut(1)))
          .Define("goodloosejet_cj_m", "goodloosejet_hadronFlavour == 4 && goodloosejet_btagDeepB > {0}".format(getBTagCut(1)))
          .Define("goodloosejet_bj_m", "goodloosejet_hadronFlavour == 5 && goodloosejet_btagDeepB > {0}".format(getBTagCut(1)))
          .Define("goodloosejet_lf_l", "goodloosejet_hadronFlavour == 0 && goodloosejet_btagDeepB > {0}".format(getBTagCut(2)))
          .Define("goodloosejet_cj_l", "goodloosejet_hadronFlavour == 4 && goodloosejet_btagDeepB > {0}".format(getBTagCut(2)))
          .Define("goodloosejet_bj_l", "goodloosejet_hadronFlavour == 5 && goodloosejet_btagDeepB > {0}".format(getBTagCut(2)))
          .Define("goodloosejet_pt_lf",   "goodloosejet_pt[goodloosejet_lf]")
          .Define("goodloosejet_pt_cj",   "goodloosejet_pt[goodloosejet_cj]")
          .Define("goodloosejet_pt_bj",   "goodloosejet_pt[goodloosejet_bj]")
          .Define("goodloosejet_pt_lf_t", "goodloosejet_pt[goodloosejet_lf_t]")
          .Define("goodloosejet_pt_cj_t", "goodloosejet_pt[goodloosejet_cj_t]")
          .Define("goodloosejet_pt_bj_t", "goodloosejet_pt[goodloosejet_bj_t]")
          .Define("goodloosejet_pt_lf_m", "goodloosejet_pt[goodloosejet_lf_m]")
          .Define("goodloosejet_pt_cj_m", "goodloosejet_pt[goodloosejet_cj_m]")
          .Define("goodloosejet_pt_bj_m", "goodloosejet_pt[goodloosejet_bj_m]")
          .Define("goodloosejet_pt_lf_l", "goodloosejet_pt[goodloosejet_lf_l]")
          .Define("goodloosejet_pt_cj_l", "goodloosejet_pt[goodloosejet_cj_l]")
          .Define("goodloosejet_pt_bj_l", "goodloosejet_pt[goodloosejet_bj_l]")
          .Define("goodloosejet_eta_lf",  "goodloosejet_eta[goodloosejet_lf]")
          .Define("goodloosejet_eta_cj",  "goodloosejet_eta[goodloosejet_cj]")
          .Define("goodloosejet_eta_bj",  "goodloosejet_eta[goodloosejet_bj]")
          .Define("goodloosejet_eta_lf_t","goodloosejet_eta[goodloosejet_lf_t]")
          .Define("goodloosejet_eta_cj_t","goodloosejet_eta[goodloosejet_cj_t]")
          .Define("goodloosejet_eta_bj_t","goodloosejet_eta[goodloosejet_bj_t]")
          .Define("goodloosejet_eta_lf_m","goodloosejet_eta[goodloosejet_lf_m]")
          .Define("goodloosejet_eta_cj_m","goodloosejet_eta[goodloosejet_cj_m]")
          .Define("goodloosejet_eta_bj_m","goodloosejet_eta[goodloosejet_bj_m]")
          .Define("goodloosejet_eta_lf_l","goodloosejet_eta[goodloosejet_lf_l]")
          .Define("goodloosejet_eta_cj_l","goodloosejet_eta[goodloosejet_cj_l]")
          .Define("goodloosejet_eta_bj_l","goodloosejet_eta[goodloosejet_bj_l]")
          )

    dfcat = dfcat.Define("nbtag","Sum(goodloosejet_lf)").Filter("nbtag > 0","nbtag > 0")

    histo2D[ 0][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 0,x),"histo2d_{0}_{1}".format( 0,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_lf"  ,"goodloosejet_pt_lf"  ,"weight")
    histo2D[ 1][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 1,x),"histo2d_{0}_{1}".format( 1,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_cj"  ,"goodloosejet_pt_cj"  ,"weight")
    histo2D[ 2][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 2,x),"histo2d_{0}_{1}".format( 2,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_bj"  ,"goodloosejet_pt_bj"  ,"weight")
    histo2D[ 3][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 3,x),"histo2d_{0}_{1}".format( 3,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_lf_t","goodloosejet_pt_lf_t","weight")
    histo2D[ 4][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 4,x),"histo2d_{0}_{1}".format( 4,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_cj_t","goodloosejet_pt_cj_t","weight")
    histo2D[ 5][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 5,x),"histo2d_{0}_{1}".format( 5,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_bj_t","goodloosejet_pt_bj_t","weight")
    histo2D[ 6][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 6,x),"histo2d_{0}_{1}".format( 6,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_lf_m","goodloosejet_pt_lf_m","weight")
    histo2D[ 7][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 7,x),"histo2d_{0}_{1}".format( 7,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_cj_m","goodloosejet_pt_cj_m","weight")
    histo2D[ 8][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 8,x),"histo2d_{0}_{1}".format( 8,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_bj_m","goodloosejet_pt_bj_m","weight")
    histo2D[ 9][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format( 9,x),"histo2d_{0}_{1}".format( 9,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_lf_l","goodloosejet_pt_lf_l","weight")
    histo2D[10][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format(10,x),"histo2d_{0}_{1}".format(10,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_cj_l","goodloosejet_pt_cj_l","weight")
    histo2D[11][x] = dfcat.Histo2D(("histo2d_{0}_{1}".format(11,x),"histo2d_{0}_{1}".format(11,x),len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),"goodloosejet_eta_bj_l","goodloosejet_pt_bj_l","weight")

    histo[10][x] = dfgen.Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 60, 91.1876-15, 91.1876+15), "Zmass","weight")
    histo[11][x] = dfgen.Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 50, 0., 100.), "Zpt","weight")
    histo[12][x] = dfgen.Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 50, 0., 5.0), "Zrap","weight")
    histo2D[100][x] = dfgen.Histo2D(("histo2d_{0}_{1}".format(100,x),"histo2d_{0}_{1}".format(100,x),10, 0, 5, 40, 0, 100),"Zrap","Zpt","weight")

    dfgen = (dfgen
          .Define("genLep", "(abs(GenDressedLepton_pdgId) == 11 || abs(GenDressedLepton_pdgId) == 13)")
          .Filter("Sum(genLep) == 2","genLep == 2")
          .Define("filter_GenDressedLepton_pt", "GenDressedLepton_pt[genLep]")
          .Define("filter_GenDressedLepton_eta", "GenDressedLepton_eta[genLep]")
            )

    dfgen = dfgen.Filter("abs(filter_GenDressedLepton_eta[0]) < 2.5 && abs(filter_GenDressedLepton_eta[1]) < 2.5","eta requirements")
    dfgen = dfgen.Filter("filter_GenDressedLepton_pt[0] > 10 && filter_GenDressedLepton_pt[1] > 10","Minimal pt requirements")

    histo[13][x] = dfgen.Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 50, 0., 100.), "Zpt","weight")
    histo[14][x] = dfgen.Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 50, 0., 5.0), "Zrap","weight")

    dfgen = dfgen.Filter("filter_GenDressedLepton_pt[0] > 25 && filter_GenDressedLepton_pt[1] > 25","Tighter pt requirements")

    histo[15][x] = dfgen.Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 50, 0., 100.), "Zpt","weight")
    histo[16][x] = dfgen.Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x), 50, 0., 5.0), "Zrap","weight")
    histo2D[101][x] = dfgen.Histo2D(("histo2d_{0}_{1}".format(101,x),"histo2d_{0}_{1}".format(100,x),10, 0, 5, 40, 0, 101),"Zrap","Zpt","weight")

    #branches = ["nElectron", "nPhoton", "nMuon", "Photon_pt", "Muon_pt", "PuppiMET_pt", "nbtag"]
    #dfcat.Snapshot("Events", "test.root", branches)

    report0 = dfcat.Report()
    report1 = dfgen.Report()
    print("---------------- SUMMARY -------------")
    report0.Print()
    report1.Print()

    myfile = ROOT.TFile("fillhisto_puAnalysis_sample{0}_year{1}.root".format(count,year),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            if(j==0): histo[j][i].SetNameTitle("pileup","pileup")
            histo[j][i].Write()
        for j in range(nHisto):
            if(histo2D[j][i] == 0): continue
            histo2D[j][i].Write()
    myfile.Close()

    print("ending {0} / {1} / {2} / {3} / {4} / {5}".format(count,category,weight,year,PDType,isData))

def readMCSample(sampleNOW, year, PDType, skimType):

    files = getMClist(sampleNOW, skimType)
    print("Total files: {0}".format(len(files)))

    df = ROOT.RDataFrame("Events", files)

    runTree = ROOT.TChain("Runs")
    for f in range(len(files)):
        runTree.AddFile(files[f])

    genEventSum = 0
    for i in range(runTree.GetEntries()):
        runTree.GetEntry(i)
        genEventSum += runTree.genEventSumw

    weight = (SwitchSample(sampleNOW,skimType)[1] / genEventSum)*getLumi(year)

    nevents = df.Count().GetValue()

    print("genEventSum({0}): {1} / Events: {2}".format(runTree.GetEntries(),genEventSum,nevents))
    print("Weight %f / Cross section: %f" %(weight,SwitchSample(sampleNOW,skimType)[1]))

    analysis(df, sampleNOW, SwitchSample(sampleNOW,skimType)[2], weight, year, PDType, "false")

if __name__ == "__main__":

    year = 2022
    process = 399
    skimType = "2l"

    valid = ['year=', "process=", 'help']
    usage  =  "Usage: ana.py --year=<{0}>\n".format(year)
    usage +=  "              --process=<{0}>".format(process)
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

    try:
        readMCSample(process,year,"All", skimType)
    except Exception as e:
        print("Error sample: {0}".format(e))

import ROOT
import os, sys, getopt

ROOT.ROOT.EnableImplicitMT(3)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles

lumi = [36.1, 41.5, 60.0]

BARRELphotons = "Photon_pt>20 and Photon_isScEtaEB and (Photon_cutBased & 2) and Photon_electronVeto"
ENDCAPphotons = "Photon_pt>20 and Photon_isScEtaEE and (Photon_cutBased & 2) and Photon_electronVeto"

TRIGGERMUEG = "(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)"
TRIGGERDMU  = "(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)"
TRIGGERSMU  = "(HLT_IsoMu24||HLT_IsoMu27||HLT_Mu50)"
TRIGGERDEL  = "(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_DoubleEle25_CaloIdL_MW||HLT_DoublePhoton70)"
TRIGGERSEL  = "(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf||HLT_Ele115_CaloIdVT_GsfTrkIdT)"

FAKE_MU   = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mediumId == true && Muon_pfIsoId >= 1)"
TIGHT_MU0 = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mediumId == true && Muon_pfIsoId >= 4)"
TIGHT_MU1 = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_tightId == true && Muon_pfIsoId >= 4)"
TIGHT_MU2 = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 2 && Muon_miniIsoId >= 2)"
TIGHT_MU3 = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 3 && Muon_miniIsoId >= 3)"
TIGHT_MU4 = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 2 && Muon_miniIsoId >= 3)"
TIGHT_MU5 = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 3 && Muon_pfIsoId >= 4)"
TIGHT_MU6 = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_tightId == true && Muon_mvaTTH > 0.7)"
TIGHT_MU7 = "(abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true && Muon_mvaId >= 4 && Muon_miniIsoId >= 4)"

FAKE_EL   = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2)"
TIGHT_EL0 = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_cutBased >= 3)"
TIGHT_EL1 = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_cutBased >= 4)"
TIGHT_EL2 = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaFall17V2Iso_WP90 == true)"
TIGHT_EL3 = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaFall17V2Iso_WP80 == true)"
TIGHT_EL4 = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaTTH > 0.7)"
TIGHT_EL5 = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_cutBased >= 4 && Electron_tightCharge == 2)"
TIGHT_EL6 = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaFall17V2Iso_WP80 == true && Electron_tightCharge == 2)"
TIGHT_EL7 = "(abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 2 && Electron_mvaTTH > 0.7 && Electron_tightCharge == 2)"

JSON = "isGoodRunLS(isData, run, luminosityBlock)"

def selectionLL(df,year,PDType,isData):

    TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    if(year == 2018 and PDType == "MuonEG"):
        TRIGGERLEP = "{0}".format(TRIGGERMUEG)
    elif(year == 2018 and PDType == "DoubleMuon"):
        TRIGGERLEP = "{0} and not {1}".format(TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "SingleMuon"):
        TRIGGERLEP = "{0} and not {1} and not {2}".format(TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "EGamma"):
        TRIGGERLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018):
        TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    else:
        print("PROBLEM with triggers!!!")

    print("TRIGGERLEP: {0}".format(TRIGGERLEP))

    dftag =(df.Define("isData","{}".format(isData))
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")
              .Define("trigger","{0}".format(TRIGGERLEP))
              .Filter("trigger > 0","Passed trigger")

              .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")
              .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")
              .Filter("Sum(loose_mu)+Sum(loose_el) == 4","Four loose leptons")

              .Define("fake_mu", "{0}".format(FAKE_MU))
              .Define("fakemu_pt",    "Muon_pt[fake_mu]")
              .Define("fakemu_eta",   "abs(Muon_eta[fake_mu])")
              .Define("fakemu_phi",   "Muon_phi[fake_mu]")
              .Define("fakemu_mass",  "Muon_mass[fake_mu]")
              .Define("fakemu_charge","Muon_charge[fake_mu]")
              .Define("tight_mu", "{0}".format(TIGHT_MU6))

              .Define("fake_el", "{0}".format(FAKE_EL))
              .Define("fakeel_pt",    "Electron_pt[fake_el]")
              .Define("fakeel_eta",   "abs(Electron_eta[fake_el])")
              .Define("fakeel_phi",   "Electron_phi[fake_el]")
              .Define("fakeel_mass",  "Electron_mass[fake_el]")
              .Define("fakeel_charge","Electron_charge[fake_el]")
              .Define("tight_el", "{0}".format(TIGHT_EL4))

              .Filter("Sum(fake_mu)+Sum(fake_el) == 4","Four fake leptons")
              .Filter("Sum(tight_mu)+Sum(tight_el) == 4","Four tight leptons")

              .Define("good_tau", "abs(Tau_eta) < 2.3 && Tau_pt > 20 && ((Tau_idDeepTau2017v2p1VSe & 8) != 0) && ((Tau_idDeepTau2017v2p1VSjet & 16) != 0) && ((Tau_idDeepTau2017v2p1VSmu & 8) != 0)")
              .Filter("Sum(good_tau) == 0","No selected hadronic taus")

              .Define("FourLepton_flavor", "Sum(fake_mu)+4*Sum(fake_el)-4")
              .Define("m4l",   "compute_4l_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi, 0)")
              .Define("mllmin","compute_4l_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi, 1)")
              .Define("mllZ1", "compute_4l_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi, 2)")
              .Define("mllZ2", "compute_4l_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi, 3)")
              .Filter("mllZ2 < 100","Found two Z boson candidates")
              .Define("ptl1Z1","compute_4l_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi, 4)")
              .Define("ptl2Z1","compute_4l_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi, 5)")
              .Define("ptl1Z2","compute_4l_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi, 6)")
              .Define("ptl2Z2","compute_4l_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi, 7)")
              .Filter("ptl1Z1 > 25 or ptl1Z2 > 25","ptl > 25 for one of the leptons")

              .Define("jet_mask1", "cleaningMask(Muon_jetIdx[fake_mu],nJet)")
              .Define("jet_mask2", "cleaningMask(Electron_jetIdx[fake_el],nJet)")
              .Define("good_jet", "abs(Jet_eta) < 4.7 && Jet_pt > 30 && jet_mask1 && jet_mask2")
              .Define("ngood_jets", "Sum(good_jet)")
              .Define("goodjet_pt",    "Jet_pt[good_jet]")
              .Define("goodjet_eta",   "Jet_eta[good_jet]")
              .Define("goodjet_phi",   "Jet_phi[good_jet]")
              .Define("goodjet_mass",  "Jet_mass[good_jet]")
              .Define("goodjet_btagCSVV2",     "Jet_btagCSVV2[good_jet]")
              .Define("goodjet_btagDeepB",     "Jet_btagDeepB[good_jet]")
              .Define("goodjet_btagDeepFlavB", "Jet_btagDeepFlavB[good_jet]")
              .Define("mjj",    "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 0)")
              .Define("ptjj",   "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 1)")
              .Define("detajj", "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 2)")
              .Define("dphijj", "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 3)")
              .Define("btagjetmax",     "Max(goodjet_btagDeepB)")
              )
    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo = [[0 for y in range(nCat)] for x in range(nHisto)]

    dftag = selectionLL(df,year,PDType,isData)

    if(theCat == plotCategory("kPlotData")):
        dfbase = dftag.Define("weight","1.0")
    else:
        dfbase = dftag.Define("PDType","\"{0}\"".format(PDType))\
                       .Define("weight","compute_weights({0},genWeight,PDType)".format(weight))

    dfcat = []
    for x in range(nCat):
        dfcat.append(dfbase.Define("theCat{0}".format(x), "compute_category({0})".format(theCat))
                           .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x)))

        histo[ 0][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x),120,  0, 120), "mllmin","weight")
        dfcat[x] = dfcat[x].Filter("mllmin > 4","mllmin cut")

        histo[ 1][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 1,x), "histo_{0}_{1}".format( 1,x),100,  0, 100), "mllZ1","weight")
        dfcat[x] = dfcat[x].Filter("mllZ1 < 100","mllZ1 cut")

        histo[ 2][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 2,x), "histo_{0}_{1}".format( 2,x),100,  0, 100), "mllZ2","weight")
        dfcat[x] = dfcat[x].Filter("mllZ2 < 100","mllZ2 cut")

        histo[ 3][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 3,x), "histo_{0}_{1}".format( 3,x), 40, 10, 210), "ptl1Z1","weight")
        histo[ 4][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 4,x), "histo_{0}_{1}".format( 4,x), 40, 10, 210), "ptl2Z1","weight")
        histo[ 5][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 5,x), "histo_{0}_{1}".format( 5,x), 40, 10, 210), "ptl1Z2","weight")
        histo[ 6][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 6,x), "histo_{0}_{1}".format( 6,x), 40, 10, 210), "ptl2Z2","weight")
        histo[ 7][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 7,x), "histo_{0}_{1}".format( 7,x),100, 50, 550), "m4l","weight")
        histo[ 8][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 8,x), "histo_{0}_{1}".format( 8,x),13,-0.5, 12.5), "FourLepton_flavor","weight")
        histo[ 9][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 9,x), "histo_{0}_{1}".format( 9,x), 6,-0.5, 5.5), "ngood_jets","weight")
        histo[10][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 40,  0, 200), "MET_pt","weight")

    report = []
    for x in range(nCat):
        report.append(dfcat[x].Report())
        if(x != theCat): continue
        print("---------------- SUMMARY {0} -------------".format(x))
        report[x].Print()

    myfile = ROOT.TFile("fillhistoZZAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].Write()
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

    try:
        if(process >= 0 and process < 1000):
            readMCSample(process,year,skimType,whichJob,group)
            sys.exit(0)
        elif(process > 1000):
            readDataSample(process,year,skimType,whichJob,group)
            sys.exit(0)
    except Exception as e:
        print("Error sample: {0}".format(e))

    for i in 1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012,1013,1014,1015,1016:
        try:
            readDataSample(i,year,skimType,whichJob,group)
        except Exception as e:
            print("Error sampleDA({0}): {1}".format(i,e))

    for i in range(4):
        try:
            readMCSample(i,year,skimType,whichJob,group)
        except Exception as e:
            print("Error sampleMC({0}): {1}".format(i,e))

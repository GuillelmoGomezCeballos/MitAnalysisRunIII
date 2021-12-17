import ROOT
import os, sys, getopt

ROOT.ROOT.EnableImplicitMT(5)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample

lumi = [36.1, 41.5, 60.0]

BARRELphotons = "Photon_pt>20 and Photon_isScEtaEB and (Photon_cutBased & 2) and Photon_electronVeto"
ENDCAPphotons = "Photon_pt>20 and Photon_isScEtaEE and (Photon_cutBased & 2) and Photon_electronVeto"

TRIGGERMUEG = "(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)"
TRIGGERDMU  = "(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)"
TRIGGERSMU  = "(HLT_IsoMu24||HLT_IsoMu27||HLT_Mu50)"
TRIGGERDEL  = "(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_DoubleEle25_CaloIdL_MW||HLT_DoublePhoton70)"
TRIGGERSEL  = "(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf||HLT_Ele115_CaloIdVT_GsfTrkIdT)"

JSON = "isGoodRunLS(isData, run, luminosityBlock)"

def selectionLL(df,weight,year,PDType,isData):

    TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    if(year == 2018 and PDType == "MuonEG"):
        TRIGGERLEP = "{0}".format(TRIGGERMUEG)
    elif(year == 2018 and PDType == "DoubleMuon"):
        TRIGGERLEP = "{0} and not {1}".format(TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "SingleMuon"):
        TRIGGERLEP = "{0} and not {1} and not {2}".format(TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "Egamma"):
        TRIGGERLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    elif(year == 2018 and PDType == "All"):
        TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)
    else:
        print("PROBLEM with triggers!!!")

    print("TRIGGERLEP: {0}".format(TRIGGERLEP))

    dftag = df.Define("isData","{}".format(isData))\
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")\
              .Define("trigger","{0}".format(TRIGGERLEP))\
              .Filter("trigger > 0","Passed trigger")\
              .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")\
              .Define("loose_highpt_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 20 && Muon_looseId == true")\
              .Define("good_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 20 && Muon_looseId == true && Muon_mvaId >= 1 && Muon_miniIsoId >= 1")\
              .Define("goodmu_pt",    "Muon_pt[good_mu]")\
              .Define("goodmu_eta",   "Muon_eta[good_mu]")\
              .Define("goodmu_phi",   "Muon_phi[good_mu]")\
              .Define("goodmu_mass",  "Muon_mass[good_mu]")\
              .Define("goodmu_charge","Muon_charge[good_mu]")\
              .Define("goodmu_mediumId","Muon_mediumId[good_mu]")\
              .Define("goodmu_tightId","Muon_tightId[good_mu]")\
              .Define("goodmu_pfIsoId","Muon_pfIsoId[good_mu]")\
              .Define("goodmu_mvaId","Muon_mvaId[good_mu]")\
              .Define("goodmu_miniIsoId","Muon_miniIsoId[good_mu]")\
              .Define("goodmu_mvaTTH","Muon_mvaTTH[good_mu]")\
              .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")\
              .Define("loose_highpt_el", "abs(Electron_eta) < 2.5 && Electron_pt > 20 && Electron_cutBased >= 1")\
              .Define("good_el", "abs(Electron_eta) < 2.5 && Electron_pt > 20 && Electron_cutBased >= 2")\
              .Define("goodel_pt",    "Electron_pt[good_el]")\
              .Define("goodel_eta",   "Electron_eta[good_el]")\
              .Define("goodel_phi",   "Electron_phi[good_el]")\
              .Define("goodel_mass",  "Electron_mass[good_el]")\
              .Define("goodel_charge","Electron_charge[good_el]")\
              .Define("goodel_cutBased","Electron_cutBased[good_el]")\
              .Define("goodel_mvaFall17V2Iso_WP90","Electron_mvaFall17V2Iso_WP90[good_el]")\
              .Define("goodel_mvaFall17V2Iso_WP80","Electron_mvaFall17V2Iso_WP80[good_el]")\
              .Define("goodel_tightCharge","Electron_tightCharge[good_el]")\
              .Define("goodel_mvaTTH","Electron_mvaTTH[good_el]")\
              .Filter("Sum(loose_mu)+Sum(loose_el) >= 2","At least two loose leptons")\
              .Filter("Sum(loose_mu)+Sum(loose_el) == 2","Only two loose leptons")\
              .Filter("Sum(loose_highpt_mu)+Sum(loose_highpt_el) == 2","Only two loose high pt leptons")\
              .Filter("Sum(good_mu)+Sum(good_el) == 2","Two good leptons")\
              .Define("good_tau", "abs(Tau_eta) < 2.3 && Tau_pt > 20 && ((Tau_idDeepTau2017v2p1VSe & 8) != 0) && ((Tau_idDeepTau2017v2p1VSjet & 16) != 0) && ((Tau_idDeepTau2017v2p1VSmu & 8) != 0)")\
              .Filter("Sum(good_tau) == 0","No selected hadronic taus")\
              .Define("mll",    "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,0)")\
              .Define("DiLepton_flavor", "Sum(good_mu)+2*Sum(good_el)-2")\
              .Filter("mll > 30 && (DiLepton_flavor == 1 || abs(mll-91.1876) < 15)","mll > 30 GeV && (emu ||abd (mll-mZ)<15)")\
              .Define("ptll",   "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,1)")\
              .Define("drll",   "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,2)")\
              .Define("dphill", "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,3)")\
              .Define("ptl1",   "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,4)")\
              .Define("ptl2",   "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,5)")\
              .Define("etal1",  "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,6)")\
              .Define("etal2",  "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,7)")\
              .Define("jet_mask1", "cleaningMask(Muon_jetIdx[good_mu],nJet)")\
              .Define("jet_mask2", "cleaningMask(Electron_jetIdx[good_el],nJet)")\
              .Define("good_jet", "abs(Jet_eta) < 4.7 && Jet_pt > 30 && jet_mask1 && jet_mask2")\
              .Define("ngood_jets", "Sum(good_jet)")\
              .Define("goodjet_pt",    "Jet_pt[good_jet]")\
              .Define("goodjet_eta",   "Jet_eta[good_jet]")\
              .Define("goodjet_phi",   "Jet_phi[good_jet]")\
              .Define("goodjet_mass",  "Jet_mass[good_jet]")\
              .Define("goodjet_btagCSVV2",     "Jet_btagCSVV2[good_jet]")\
              .Define("goodjet_btagDeepB",     "Jet_btagDeepB[good_jet]")\
              .Define("goodjet_btagDeepFlavB", "Jet_btagDeepFlavB[good_jet]")\
              .Define("weight","compute_weights({0},genWeight)".format(weight))\
              .Define("mjj",    "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 0)")\
              .Define("ptjj",   "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 1)")\
              .Define("detajj", "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 2)")\
              .Define("dphijj", "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 3)")\
              .Define("muid1",  "compute_muid_var(goodmu_mediumId, goodmu_tightId, goodmu_pfIsoId, goodmu_mvaId, goodmu_miniIsoId, goodmu_mvaTTH, 0)")\
              .Define("muid2",  "compute_muid_var(goodmu_mediumId, goodmu_tightId, goodmu_pfIsoId, goodmu_mvaId, goodmu_miniIsoId, goodmu_mvaTTH, 1)")\
              .Define("elid1",  "compute_elid_var(goodel_cutBased, goodel_mvaFall17V2Iso_WP90, goodel_mvaFall17V2Iso_WP80, goodel_tightCharge, goodel_mvaTTH, 0)")\
              .Define("elid2",  "compute_elid_var(goodel_cutBased, goodel_mvaFall17V2Iso_WP90, goodel_mvaFall17V2Iso_WP80, goodel_tightCharge, goodel_mvaTTH, 1)")

    return dftag

def analysis(df,count,category,weight,year,PDType,isData):

    print("starting {0} / {1} / {2} / {3} / {4} / {5}".format(count,category,weight,year,PDType,isData))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo = [[0 for x in range(nCat)] for y in range(nHisto)]

    dftag = df.Define("weight","compute_weights({0},genWeight)".format(weight))

    dfcat = []
    for x in range(nCat):
        dfcat.append(dftag.Define("theCat{0}".format(x), "compute_category({0})".format(theCat))
                          .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x)))

        histo[ 0][x] = dfcat[x].Histo1D(("histo_{0}_{1}".format( 0,x), "histo_{0}_{1}".format( 0,x), 100,  0, 100), "Pileup_nTrueInt","weight")


    myfile = ROOT.TFile("fillhistoPUAna_sample{0}_year{1}.root".format(count,year),'RECREATE')
    for i in range(nCat):
        if(i != 4): continue
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
            histo[j][i].SetNameTitle("pileup","pileup")
            histo[j][i].Write()
    myfile.Close()

    print("ending {0} / {1} / {2} / {3} / {4} / {5}".format(count,category,weight,year,PDType,isData))

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
        readMCSample(0,2018,"All")
        sys.exit(0)

    readMCSample(0,2018,"All")

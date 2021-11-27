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

    dftag = df.Define("isData","{}".format(isData))\
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")\
              .Define("weight","{}".format(weight))

    if(year == 2018 and PDType == "MuonEG"):
        dftag = dftag.Define("trigger","{0}".format(TRIGGERMUEG))
    elif(year == 2018 and PDType == "DoubleMuon"):
        dftag = dftag.Define("trigger","{0} and not {1}".format(TRIGGERDMU,TRIGGERMUEG))
    if(year == 2018 and PDType == "SingleMuon"):
        dftag = dftag.Define("trigger","{0} and not {1} and not {2}".format(TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG))
    elif(year == 2018 and PDType == "Egamma"):
        dftag = dftag.Define("trigger","({0} or {1}) and not {2} and not {3} and not {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG))
    elif(year == 2018 and PDType == "All"):
        dftag = dftag.Define("trigger","{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG))

    dftag = dftag.Filter("trigger > 0","Passed trigger")\
                 .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")\
                 .Define("loose_highpt_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 20 && Muon_looseId == true")\
                 .Define("good_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 20 && Muon_looseId == true && Muon_mvaId >= 2 && Muon_miniIsoId >= 2")\
                 .Define("goodmu_pt",    "Muon_pt[good_mu]")\
                 .Define("goodmu_eta",   "Muon_eta[good_mu]")\
                 .Define("goodmu_phi",   "Muon_phi[good_mu]")\
                 .Define("goodmu_mass",  "Muon_mass[good_mu]")\
                 .Define("goodmu_charge","Muon_charge[good_mu]")\
                 .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")\
                 .Define("loose_highpt_el", "abs(Electron_eta) < 2.5 && Electron_pt > 20 && Electron_cutBased >= 1")\
                 .Define("good_el", "abs(Electron_eta) < 2.5 && Electron_pt > 20 && Electron_cutBased >= 1 && Electron_mvaFall17V2Iso_WP90 == 1")\
                 .Define("goodel_pt",    "Electron_pt[good_el]")\
                 .Define("goodel_eta",   "Electron_eta[good_el]")\
                 .Define("goodel_phi",   "Electron_phi[good_el]")\
                 .Define("goodel_mass",  "Electron_mass[good_el]")\
                 .Define("goodel_charge","Electron_charge[good_el]")\
                 .Filter("Sum(loose_mu)+Sum(loose_el) >= 2","At least two loose leptons")\
                 .Filter("Sum(loose_mu)+Sum(loose_el) == 2","Only two loose leptons")\
                 .Filter("Sum(loose_highpt_mu)+Sum(loose_highpt_el) == 2","Only two loose high pt leptons")\
                 .Filter("Sum(good_mu)+Sum(good_el) == 2 && Sum(goodmu_charge)+Sum(goodel_charge) == 0","Two opposite-sign good leptons")\
                 .Define("good_tau", "abs(Tau_eta) < 2.3 && Tau_pt > 20 && ((Tau_idDeepTau2017v2p1VSe & 8) != 0) && ((Tau_idDeepTau2017v2p1VSjet & 16) != 0) && ((Tau_idDeepTau2017v2p1VSmu & 8) != 0)")\
                 .Filter("Sum(good_tau) == 0","No selected hadronic taus")\
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
                 .Define("mjj",    "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 0)")\
                 .Define("ptjj",   "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 1)")\
                 .Define("detajj", "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 2)")\
                 .Define("dphijj", "compute_jet_var(goodjet_pt, goodjet_eta, goodjet_phi, goodjet_mass, 3)")\
                 .Define("mll",    "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,0)")\
                 .Define("ptll",   "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,1)")\
                 .Define("drll",   "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,2)")\
                 .Define("dphill", "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,3)")\
                 .Define("ptl1",   "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,4)")\
                 .Define("ptl2",   "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,5)")\
                 .Define("etal1",  "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,6)")\
                 .Define("etal2",  "compute_ll_var(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass,7)")\
                 .Define("DiLepton_flavor", "Sum(good_mu)+2*Sum(good_el)-2")\
                 .Filter("mll > 50","mll > 50 GeV")

    return dftag


def analysis(df,count,category,weight,year,PDType,isData):

    print("starting {0} / {1} / {2} / {3} / {4} / {5}".format(count,category,weight,year,PDType,isData))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 48
    histo = [[0 for x in range(nCat)] for y in range(nHisto)]

    dftag = selectionLL(df,weight,year,PDType,isData)

    dfbase = (dftag.Define("goodPhotons", "{}".format(BARRELphotons)+" or {}".format(ENDCAPphotons) )
              .Define("goodPhotons_pt", "Photon_pt[goodPhotons]")
              .Define("goodPhotons_eta", "Photon_eta[goodPhotons]")
              .Define("goodPhotons_phi", "Photon_phi[goodPhotons]")
          )

    dfcat = []
    dfjetcat = []
    for x in range(nCat):
        for ltype in range(3):
            dfcat.append(dfbase.Filter("DiLepton_flavor=={0}".format(ltype), "flavor type == {0}".format(ltype))
                               .Define("theCat{0}".format(x), "compute_category({0})".format(theCat))
                               .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x)))
            histo[ltype+ 0][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,x), "histo_{0}_{1}".format(ltype+ 0,x), 50, 50, 150), "mll","weight")
            histo[ltype+ 3][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 3,x), "histo_{0}_{1}".format(ltype+ 3,x), 50,  0, 200), "ptll","weight")
            histo[ltype+ 6][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,x), "histo_{0}_{1}".format(ltype+ 6,x), 50,  0, 5),   "drll","weight")
            histo[ltype+ 9][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 9,x), "histo_{0}_{1}".format(ltype+ 9,x), 50,  0, 3.1416), "dphill","weight")
            histo[ltype+12][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+12,x), "histo_{0}_{1}".format(ltype+12,x), 40,  0, 200), "ptl1","weight")
            histo[ltype+15][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+15,x), "histo_{0}_{1}".format(ltype+15,x), 40,  0, 200), "ptl2","weight")
            histo[ltype+18][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+18,x), "histo_{0}_{1}".format(ltype+18,x), 40,-2.5,2.5), "etal1","weight")
            histo[ltype+21][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+21,x), "histo_{0}_{1}".format(ltype+21,x), 40,-2.5,2.5), "etal2","weight")
            histo[ltype+24][x] = dfcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+24,x), "histo_{0}_{1}".format(ltype+24,x), 10,-0.5, 9.5), "ngood_jets","weight")

            dfjetcat.append(dfcat[3*x+ltype].Filter("ngood_jets >= 2", "At least two jets"))
            histo[ltype+27][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+27,x), "histo_{0}_{1}".format(ltype+27,x), 50,0,2000), "mjj","weight")
            histo[ltype+30][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+30,x), "histo_{0}_{1}".format(ltype+30,x), 50,0,400), "ptjj","weight")
            histo[ltype+33][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+33,x), "histo_{0}_{1}".format(ltype+33,x), 50,0,10), "detajj","weight")
            histo[ltype+36][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+36,x), "histo_{0}_{1}".format(ltype+36,x), 50,0,3.1416), "dphijj","weight")
            histo[ltype+39][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+39,x), "histo_{0}_{1}".format(ltype+39,x), 50,0,1), "goodjet_btagCSVV2","weight")
            histo[ltype+42][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+42,x), "histo_{0}_{1}".format(ltype+42,x), 50,0,1), "goodjet_btagDeepB","weight")
            histo[ltype+45][x] = dfjetcat[3*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+45,x), "histo_{0}_{1}".format(ltype+45,x), 50,0,1), "goodjet_btagDeepFlavB","weight")

    report = []
    for x in range(nCat):
        for ltype in range(3):
            report.append(dfjetcat[3*x+ltype].Report())
            if(x != theCat): continue
            print("---------------- SUMMARY 3*{0}+{1} = {2} -------------".format(x,ltype,3*x+ltype))
            report[3*x+ltype].Print()

    myfile = ROOT.TFile("fillhistoZAna_sample{0}_year{1}.root".format(count,year),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            histo[j][i].Write()
    myfile.Close()


def readMCSample(sampleNOW, year, PDType):

    files = getMClist(sampleNOW)
    print(len(files))
    df = ROOT.RDataFrame("Events", files)

    nevents = df.Count().GetValue()  ## later with negative weights
    weight = (SwitchSample(sampleNOW)[1] / nevents)*lumi[year-2016]

    print("%f entries in the dataset" %nevents)
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
        #readMCSample(10,2018,"All")
        readMCSample(2,2018,"All")
        #readDataSample(103,2018,"Egamma")
        sys.exit(0)
    elif(test > 100):
        readDataSample(test,2018,"Egamma")
        sys.exit(0)

    anaNamesDict = dict()
    anaNamesDict.update({"1":[101,2018,"SingleMuon"]})
    anaNamesDict.update({"2":[102,2018,"DoubleMuon"]})
    anaNamesDict.update({"3":[103,2018,"MuonEG"]})
    anaNamesDict.update({"4":[104,2018,"Egamma"]})
    anaNamesDict.update({"5":[105,2018,"Egamma"]})
    anaNamesDict.update({"6":[106,2018,"Egamma"]})
    anaNamesDict.update({"7":[107,2018,"Egamma"]})
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

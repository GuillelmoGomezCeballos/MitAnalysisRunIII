import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(3)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample, groupFiles, getTriggerFromJson

lumi = [36.1, 41.5, 60.0]

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

def selectionLL(df,year,PDType,isData):

    overallTriggers = jsonObject['triggers']
    TRIGGERMET = getTriggerFromJson(overallTriggers, "TRIGGERMET", year)

    TRIGGERMUEG = getTriggerFromJson(overallTriggers, "TRIGGERMUEG", year)
    TRIGGERDMU  = getTriggerFromJson(overallTriggers, "TRIGGERDMU", year)
    TRIGGERSMU  = getTriggerFromJson(overallTriggers, "TRIGGERSMU", year)
    TRIGGERDEL  = getTriggerFromJson(overallTriggers, "TRIGGERDEL", year)
    TRIGGERSEL  = getTriggerFromJson(overallTriggers, "TRIGGERSEL", year)

    TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    dftag =(df.Define("isData","{}".format(isData))
              .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")
              .Define("trigger","{0}".format(TRIGGERMET))
              .Filter("trigger > 0","Passed trigger")

              .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")
              .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")
              .Filter("Sum(loose_mu)+Sum(loose_el) >= 2 and Sum(loose_mu)+Sum(loose_el) <= 4","Between two and four loose leptons")

              .Define("fake_mu"           ,"{0}".format(FAKE_MU))
              .Define("fakemu_pt"         ,"Muon_pt[fake_mu]")
              .Define("fakemu_eta"        ,"Muon_eta[fake_mu]")
              .Define("fakemu_phi"        ,"Muon_phi[fake_mu]")
              .Define("fakemu_mass"       ,"Muon_mass[fake_mu]")
              .Define("fakemu_charge"     ,"Muon_charge[fake_mu]")
              .Define("fakemu_dxy"        ,"Muon_dxy[fake_mu]")
              .Define("fakemu_dz"         ,"Muon_dz[fake_mu]")
              .Define("fakemu_looseId"    ,"Muon_looseId[fake_mu]")
              .Define("fakemu_mediumId"   ,"Muon_mediumId[fake_mu]")
              .Define("fakemu_tightId"    ,"Muon_tightId[fake_mu]")
              .Define("fakemu_pfIsoId"    ,"Muon_pfIsoId[fake_mu]")
              .Define("fakemu_mvaId"      ,"Muon_mvaId[fake_mu]")
              .Define("fakemu_miniIsoId"  ,"Muon_miniIsoId[fake_mu]")
              .Define("fakemu_mvaTTH"     ,"Muon_mvaTTH[fake_mu]")
              .Define("tight_mu"          ,"{0}".format(TIGHT_MU0))

              .Define("fake_el"                   ,"{0}".format(FAKE_EL))
              .Define("fakeel_pt"                 ,"Electron_pt[fake_el]")
              .Define("fakeel_eta"                ,"Electron_eta[fake_el]")
              .Define("fakeel_phi"                ,"Electron_phi[fake_el]")
              .Define("fakeel_mass"               ,"Electron_mass[fake_el]")
              .Define("fakeel_charge"             ,"Electron_charge[fake_el]")
              .Define("fakeel_dxy"                ,"Electron_dxy[fake_el]")
              .Define("fakeel_dz"                 ,"Electron_dz[fake_el]")
              .Define("fakeel_cutBased"           ,"Electron_cutBased[fake_el]")
              .Define("fakeel_mvaFall17V2Iso_WP90","Electron_mvaFall17V2Iso_WP90[fake_el]")
              .Define("fakeel_mvaFall17V2Iso_WP80","Electron_mvaFall17V2Iso_WP80[fake_el]")
              .Define("fakeel_tightCharge"        ,"Electron_tightCharge[fake_el]")
              .Define("fakeel_mvaTTH"             ,"Electron_mvaTTH[fake_el]")
              .Define("tight_el"                  ,"{0}".format(TIGHT_EL0))

              .Filter("Sum(fake_mu)+Sum(fake_el) >= 2 and Sum(fake_mu)+Sum(fake_el) <= 4","Between two and four tight leptons")
              .Filter("(Sum(fake_mu) > 0 and Max(fakemu_pt) > 25) or (Sum(fake_el) > 0 and Max(fakeel_pt) > 25)","At least one high pt lepton")
              .Define("MultiLepton_flavor", "Sum(fake_mu)+4*Sum(fake_el)-2")\
              .Define("mtot",  "compute_nl_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi,0)")
              .Define("mllmin","compute_nl_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi,1)")
              .Filter("mllmin > 10")
              .Define("ltype",  "compute_nl_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi,2)")
              .Define("ptlmax", "compute_nl_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi,3)")
              .Define("ptlmin", "compute_nl_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi,4)")
              .Define("etalmax","compute_nl_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi,5)")
              .Define("etalmin","compute_nl_var(fakemu_pt, fakemu_eta, fakemu_phi, fakemu_mass, fakemu_charge, fakeel_pt, fakeel_eta, fakeel_phi, fakeel_mass, fakeel_charge, MET_pt, MET_phi,6)")
              .Define("triggerl","{0}".format(TRIGGERLEP))
             )

    return dftag


def analysis(df,count,category,weight,year,PDType,isData,whichJob):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    xPtMaxBins = array('d', [         25,30,35,40,55,115,1000])
    xPtMinBins = array('d', [10,15,20,25,30,35,40,55,115,1000])
    xPtBins = array('d', [10,25,35,55,1000])
    xEtaBins = array('d', [0.0,1.5,2.5])

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo   = [[0 for y in range(nCat)] for x in range(nHisto)]
    histo2D = [[0 for y in range(nCat)] for x in range(nHisto)]

    dfbase = selectionLL(df,year,PDType,isData)

    if(theCat == plotCategory("kPlotData")):
        dfbase = dfbase.Define("weight","1.0")
    else:
        dfbase = dfbase.Define("PDType","\"{0}\"".format(PDType))\
                       .Define("weight","1.0")

    dfcat = []
    for x in range(nCat):
        for ltype in range(6):
            dfcat.append(dfbase.Filter("ltype=={0}".format(ltype), "flavor type == {0}".format(ltype))
                               .Define("kPlotNonPrompt", "{0}".format(plotCategory("kPlotNonPrompt")))
                               .Define("theCat{0}".format(x), "compute_category({0},kPlotNonPrompt,2,2)".format(theCat))
                               .Filter("theCat{0}=={1}".format(x,x), "correct category ({0})".format(x)))

            histo[ltype+ 0][x] = dfcat[6*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 0,x), "histo_{0}_{1}".format(ltype+ 0,x), 100,  0, 500), "mtot","weight")
            histo[ltype+ 6][x] = dfcat[6*x+ltype].Histo1D(("histo_{0}_{1}".format(ltype+ 6,x), "histo_{0}_{1}".format(ltype+ 6,x), 100,  0, 200), "mllmin","weight")

            histo2D[ltype+ 0][x] = dfcat[6*x+ltype].Filter("etalmax <= 1.5 && etalmin <= 1.5")                       .Histo2D(("histo2d_{0}_{1}".format(ltype+ 0, x), "histo2d_{0}_{1}".format(ltype+ 0, x), len(xPtMaxBins)-1, xPtMaxBins, len(xPtMinBins)-1, xPtMinBins), "ptlmax", "ptlmin","weight")
            histo2D[ltype+ 6][x] = dfcat[6*x+ltype].Filter("etalmax <= 1.5 && etalmin <= 1.5").Filter("triggerl > 0").Histo2D(("histo2d_{0}_{1}".format(ltype+ 6, x), "histo2d_{0}_{1}".format(ltype+ 6, x), len(xPtMaxBins)-1, xPtMaxBins, len(xPtMinBins)-1, xPtMinBins), "ptlmax", "ptlmin","weight")

            histo2D[ltype+12][x] = dfcat[6*x+ltype].Filter("etalmax >  1.5 && etalmin <= 1.5")                       .Histo2D(("histo2d_{0}_{1}".format(ltype+12, x), "histo2d_{0}_{1}".format(ltype+12, x), len(xPtMaxBins)-1, xPtMaxBins, len(xPtMinBins)-1, xPtMinBins), "ptlmax", "ptlmin","weight")
            histo2D[ltype+18][x] = dfcat[6*x+ltype].Filter("etalmax >  1.5 && etalmin <= 1.5").Filter("triggerl > 0").Histo2D(("histo2d_{0}_{1}".format(ltype+18, x), "histo2d_{0}_{1}".format(ltype+18, x), len(xPtMaxBins)-1, xPtMaxBins, len(xPtMinBins)-1, xPtMinBins), "ptlmax", "ptlmin","weight")

            histo2D[ltype+24][x] = dfcat[6*x+ltype].Filter("etalmax <= 1.5 && etalmin >  1.5")                       .Histo2D(("histo2d_{0}_{1}".format(ltype+24, x), "histo2d_{0}_{1}".format(ltype+24, x), len(xPtMaxBins)-1, xPtMaxBins, len(xPtMinBins)-1, xPtMinBins), "ptlmax", "ptlmin","weight")
            histo2D[ltype+30][x] = dfcat[6*x+ltype].Filter("etalmax <= 1.5 && etalmin >  1.5").Filter("triggerl > 0").Histo2D(("histo2d_{0}_{1}".format(ltype+30, x), "histo2d_{0}_{1}".format(ltype+30, x), len(xPtMaxBins)-1, xPtMaxBins, len(xPtMinBins)-1, xPtMinBins), "ptlmax", "ptlmin","weight")

            histo2D[ltype+36][x] = dfcat[6*x+ltype].Filter("etalmax >  1.5 && etalmin >  1.5")                       .Histo2D(("histo2d_{0}_{1}".format(ltype+36, x), "histo2d_{0}_{1}".format(ltype+36, x), len(xPtMaxBins)-1, xPtMaxBins, len(xPtMinBins)-1, xPtMinBins), "ptlmax", "ptlmin","weight")
            histo2D[ltype+42][x] = dfcat[6*x+ltype].Filter("etalmax >  1.5 && etalmin >  1.5").Filter("triggerl > 0").Histo2D(("histo2d_{0}_{1}".format(ltype+42, x), "histo2d_{0}_{1}".format(ltype+42, x), len(xPtMaxBins)-1, xPtMaxBins, len(xPtMinBins)-1, xPtMinBins), "ptlmax", "ptlmin","weight")

            histo2D[ltype+48][x] = dfcat[6*x+ltype]                       .Histo2D(("histo2d_{0}_{1}".format(ltype+48, x), "histo2d_{0}_{1}".format(ltype+48, x), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "etalmin", "ptlmin","weight")
            histo2D[ltype+54][x] = dfcat[6*x+ltype].Filter("triggerl > 0").Histo2D(("histo2d_{0}_{1}".format(ltype+54, x), "histo2d_{0}_{1}".format(ltype+54, x), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins), "etalmin", "ptlmin","weight")

    report = []
    for x in range(nCat):
        for ltype in range(6):
            report.append(dfcat[6*x+ltype].Report())
            if(x != theCat): continue
            print("---------------- SUMMARY 6*{0}+{1} = {2} -------------".format(x,ltype,6*x+ltype))
            report[6*x+ltype].Print()

    myfile = ROOT.TFile("fillhistoMETAna_sample{0}_year{1}_job{2}.root".format(count,year,whichJob),'RECREATE')
    for i in range(nCat):
        for j in range(nHisto):
            if(histo[j][i] == 0): continue
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

    PDType = os.path.basename(SwitchSample(sampleNOW, skimType)[0]).split('+')[0]

    analysis(df, sampleNOW, SwitchSample(sampleNOW, skimType)[2], weight, year, PDType, "false", whichJob)

def readDASample(sampleNOW, year, skimType, whichJob, group):

    PDType = "0"
    if  (sampleNOW >= 1001 and sampleNOW <= 1004): PDType = "SingleMuon"
    elif(sampleNOW >= 1005 and sampleNOW <= 1008): PDType = "DoubleMuon"
    elif(sampleNOW >= 1009 and sampleNOW <= 1012): PDType = "MuonEG"
    elif(sampleNOW >= 1012 and sampleNOW <= 1016): PDType = "EGamma"
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

    analysis(df, sampleNOW, sampleNOW, weight, year, PDType, "true", whichJob)

if __name__ == "__main__":

    group = 10

    skimType = "met"
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
        elif(process > 1000):
            readDASample(process,year,skimType,whichJob,group)
    except Exception as e:
        print("Error sample: {0}".format(e))
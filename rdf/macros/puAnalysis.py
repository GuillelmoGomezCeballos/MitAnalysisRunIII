import ROOT
import os, sys, getopt

ROOT.ROOT.EnableImplicitMT(5)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample

lumi = [36.1, 41.5, 60.0]

def analysis(df,count,category,weight,year,PDType,isData,whichJob):

    print("starting {0} / {1} / {2} / {3} / {4} / {5} / {6}".format(count,category,weight,year,PDType,isData,whichJob))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo = [[0 for x in range(nCat)] for y in range(nHisto)]

    dftag = df.Define("PDType","\"{0}\"".format(PDType))\
              .Define("weight","compute_weights({0},genWeight,PDType,fakemu_genPartFlav,fakeel_genPartFlav,0)".format(weight))\
              .Filter("weight != 0","good weight")

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

    weight = (SwitchSample(sampleNOW,skimType)[1] / genEventSum)*lumi[year-2016]

    nevents = df.Count().GetValue()

    print("genEventSum({0}): {1} / Events: {2}".format(runTree.GetEntries(),genEventSum,nevents))
    print("Weight %f / Cross section: %f" %(weight,SwitchSample(sampleNOW,skimType)[1]))

    analysis(df, sampleNOW, SwitchSample(sampleNOW,skimType)[2], weight, year, PDType, "false")

if __name__ == "__main__":

    year = 2018
    process = 0
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

    readMCSample(process,2018,"All", skimType)

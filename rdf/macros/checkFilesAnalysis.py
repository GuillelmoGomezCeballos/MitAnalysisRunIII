import ROOT
import os, sys, getopt

ROOT.ROOT.EnableImplicitMT(5)
from utilsAna import plotCategory
from utilsAna import getMClist, getDATAlist
from utilsAna import SwitchSample

def readMCSample(sampleNOW, year, PDType, skimType):

    files = getMClist(sampleNOW, skimType)
    print(len(files))

    for f in range(len(files)):
        try:
            df = ROOT.RDataFrame("Events", files[f])
            nevents = df.Count().GetValue()
            del df
        except Exception as e:
            print("{0} {1}".format(files[f].replace("root://t3serv017.mit.edu/","/mnt/T3_US_MIT/hadoop"),e))

def readDataSample(sampleNOW, year, PDType, skimType):

    files = getDATAlist(sampleNOW, year, PDType, skimType)
    print(len(files))

    for f in range(len(files)):
        try:
            df = ROOT.RDataFrame("Events", files[f])
            nevents = df.Count().GetValue()
            del df
        except Exception as e:
            print("{0} {1}".format(files[f].replace("root://t3serv017.mit.edu/","/mnt/T3_US_MIT/hadoop"),e))

if __name__ == "__main__":

    year = 2018
    skimType = "1l"
    test = 0

    valid = ["year=", "skimType=", "test=", 'help']
    usage  =  "Usage: ana.py --year=<{0}>\n".format(year)
    usage +=  "              --skimType=<{0}>\n".format(skimType)
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
        if opt == "--skimType":
            skimType = str(arg)
        if opt == "--test":
            test = int(arg)

    if(test == 1):
        #readMCSample(10,2018,"All")
        readMCSample(1,2018,"All",skimType)
        sys.exit(0)
    elif(test == 101):
        readDataSample(test,2018,"SingleMuon",skimType)
        sys.exit(0)
    elif(test == 102):
        readDataSample(test,2018,"DoubleMuon",skimType)
        sys.exit(0)
    elif(test == 102):
        readDataSample(test,2018,"MuonEG",skimType)
        sys.exit(0)
    elif(test == 104):
        readDataSample(test,2018,"Egamma",skimType)
        sys.exit(0)

    anaNamesDict = dict()
    anaNamesDict.update({"1":[101,2018,"SingleMuon"]})
    anaNamesDict.update({"2":[102,2018,"DoubleMuon"]})
    anaNamesDict.update({"3":[103,2018,"MuonEG"]})
    anaNamesDict.update({"4":[104,2018,"Egamma"]})
    for key in anaNamesDict:
        try:
            readDataSample(anaNamesDict[key][0],anaNamesDict[key][1],anaNamesDict[key][2],skimType)
        except Exception as e:
            print("Error sampleDA({0}): {1}".format(key,e))

    for i in range(4):
        try:
            readMCSample(i,2018,"All",skimType)
        except Exception as e:
            print("Error sampleMC({0}): {1}".format(i,e))

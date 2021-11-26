import ROOT
import os, json
from subprocess import call,check_output

def plotCategory(key):
    plotCategoryDict = dict()
    plotCategoryDict.update({"kPlotData"      :[ 0]})
    plotCategoryDict.update({"kPlotqqWW"      :[ 1]})
    plotCategoryDict.update({"kPlotggWW"      :[ 2]})
    plotCategoryDict.update({"kPlotTop"       :[ 3]})
    plotCategoryDict.update({"kPlotDY"        :[ 4]})
    plotCategoryDict.update({"kPlotEWKSSWW"   :[ 5]})
    plotCategoryDict.update({"kPlotQCDSSWW"   :[ 6]})
    plotCategoryDict.update({"kPlotEWKWZ"     :[ 7]})
    plotCategoryDict.update({"kPlotWZ"        :[ 8]})
    plotCategoryDict.update({"kPlotZZ"        :[ 9]})
    plotCategoryDict.update({"kPlotNonPrompt" :[10]})
    plotCategoryDict.update({"kPlotVVV"       :[11]})
    plotCategoryDict.update({"kPlotTVX"       :[12]})
    plotCategoryDict.update({"kPlotVG"        :[13]})
    plotCategoryDict.update({"kPlotHiggs"     :[14]})
    plotCategoryDict.update({"kPlotDPSWW"     :[15]})
    plotCategoryDict.update({"kPlotWS"        :[16]})
    plotCategoryDict.update({"kPlotEM"        :[17]})
    plotCategoryDict.update({"kPlotOther"     :[18]})
    plotCategoryDict.update({"kPlotBSM"       :[19]})
    plotCategoryDict.update({"kPlotSignal0"   :[20]})
    plotCategoryDict.update({"kPlotSignal1"   :[21]})
    plotCategoryDict.update({"kPlotSignal2"   :[22]})
    plotCategoryDict.update({"kPlotSignal3"   :[23]})
    plotCategoryDict.update({"kPlotCategories":[24]})

    try:
        return plotCategoryDict[key][0]
    except Exception as e:
        print("Wrong key({0}): {1}".format(key,e))

if "/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("functions.cc","k")

def loadJSON(fIn):

    if not os.path.isfile(fIn):
        print("JSON file %s does not exist" % fIn)
        return

    if not hasattr(ROOT, "jsonMap"):
        print("jsonMap not found in ROOT dict")
        return

    info = json.load(open(fIn))
    print("JSON file %s loaded" % fIn)
    for k,v in info.items():

        vec = ROOT.std.vector["std::pair<unsigned int, unsigned int>"]()
        for combo in v:
            pair = ROOT.std.pair["unsigned int", "unsigned int"](*[int(c) for c in combo])
            vec.push_back(pair)
            ROOT.jsonMap[int(k)] = vec

def findDataset(name):

    DASclient = "dasgoclient -query '%(query)s'"
    cmd= DASclient%{'query':'file dataset=%s'%name}
    print(cmd)
    check_output(cmd,shell=True)
    fileList=[ 'root://xrootd-cms.infn.it//'+x for x in check_output(cmd,shell=True).split() ]

    files_ROOT = ROOT.vector('string')()
    for f in fileList: files_ROOT.push_back(f)

    return files_ROOT

def findDIR(directory):

    print(directory)

    counter = 0
    rootFiles = ROOT.vector('string')()
    for root, directories, filenames in os.walk(directory):
        for f in filenames:

            counter+=1
            isBadFile = False
            filePath = os.path.join(os.path.abspath(root), f)
            if "failed/" in filePath: continue
            if "log/" in filePath: continue
            if(("XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" in filePath) or
	       
               ("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" in filePath)
	       ): isBadFile = True

            if(isBadFile == True):
                print("Bad file: {0}".format(filePath))
                counter-=1
                continue
            rootFiles.push_back(filePath)
#            if counter>3000: break
#            if counter>50: break
#            if counter>5: break

    return rootFiles

def findMany(basedir, regex):

    if basedir[-1] == "/": basedir = basedir[:-1]
    regex = basedir + "/" + regex

    rootFiles = ROOT.vector('string')()
    for root, directories, filenames in os.walk(basedir):

        for f in filenames:

            filePath = os.path.join(os.path.abspath(root), f)
            if "failed/" in filePath: continue
            if "log/" in filePath: continue
            if fnmatch.fnmatch(filePath, regex): rootFiles.push_back(filePath)

    return rootFiles

def concatenate(result, tmp1):
    for f in tmp1:
        result.push_back(f)


def getMClist(sampleNOW):

    files = findDIR("{}".format(SwitchSample(sampleNOW)[0]))
    return files

def getDATAlist(type, year, PDType):

    loadJSON("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt")
    files1 = []
    files2 = []
    files3 = []
    files4 = []
    if(year == 2018 and PDType == "SingleMuon"):
        files1 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/SingleMuon+Run2018B-UL2018_MiniAODv2-v2+MINIAOD")
        files2 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/SingleMuon+Run2018C-UL2018_MiniAODv2-v2+MINIAOD")
        files3 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/SingleMuon+Run2018D-UL2018_MiniAODv2-v3+MINIAOD")
        files4 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/SingleMuon+Run2018A-UL2018_MiniAODv2-v2+MINIAOD")
    elif(year == 2018 and PDType == "DoubleMuon"):
        files1 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/DoubleMuon+Run2018A-UL2018_MiniAODv2-v1+MINIAOD")
        files2 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/DoubleMuon+Run2018B-UL2018_MiniAODv2-v1+MINIAOD")
        files3 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/DoubleMuon+Run2018C-UL2018_MiniAODv2-v1+MINIAOD")
        files4 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/DoubleMuon+Run2018D-UL2018_MiniAODv2-v1+MINIAOD")
    elif(year == 2018 and PDType == "MuonEG"):
        files1 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/MuonEG+Run2018A-UL2018_MiniAODv2-v1+MINIAOD")
        files2 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/MuonEG+Run2018B-UL2018_MiniAODv2-v1+MINIAOD")
        files3 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/MuonEG+Run2018C-UL2018_MiniAODv2-v1+MINIAOD")
        files4 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/MuonEG+Run2018D-UL2018_MiniAODv2-v1+MINIAOD")
    elif(year == 2018 and PDType == "Egamma" and type == 104):
        files1 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/EGamma+Run2018A-UL2018_MiniAODv2-v1+MINIAOD")
    elif(year == 2018 and PDType == "Egamma" and type == 105):
        files2 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/EGamma+Run2018B-UL2018_MiniAODv2-v1+MINIAOD")
    elif(year == 2018 and PDType == "Egamma" and type == 106):
        files3 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/EGamma+Run2018C-UL2018_MiniAODv2-v1+MINIAOD")
    elif(year == 2018 and PDType == "Egamma" and type == 107):
        files4 = findDIR("/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/EGamma+Run2018D-UL2018_MiniAODv2-v2+MINIAOD")

    files = ROOT.vector('string')()
    concatenate(files, files1)
    concatenate(files, files2)
    concatenate(files, files3)
    concatenate(files, files4)

    return files

def SwitchSample(argument):

    dirT2 = "/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/"
    dirLocal = "/work/submit/mariadlf/Hrare/OCT14/"

    switch = {
        0: (dirT2+"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v1+MINIAODSIM",6067*1000,plotCategory("kPlotDY")),
        1: (dirT2+"WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",53870.0*1000,plotCategory("kPlotOther")),
        2: (dirT2+"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",88.2*1000,plotCategory("kPlotTop")),
        3: (dirT2+"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2+MINIAODSIM",365.3452*1000,plotCategory("kPlotTop")),
        10:(dirLocal+"ZLLphigamma_pythia8_genFix",0.10*1000,plotCategory("kPlotBSM"))

    }
    return switch.get(argument, "BKGdefault, xsecDefault, category")

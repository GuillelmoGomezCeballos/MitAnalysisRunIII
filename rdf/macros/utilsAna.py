import ROOT
import os, json
from subprocess import call,check_output
from XRootD import client

lumi = [36.1, 41.5, 60.0]

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

    maxFiles = 1000000000
    if("TTToSemiLeptonic" in directory):
        maxFiles = 300

    counter = 0
    rootFiles = ROOT.vector('string')()

    if("/mnt/T3_US_MIT/hadoop" in directory):
        fs = client.FileSystem('root://t3serv017.mit.edu/')
        lsst = fs.dirlist(directory.replace("/mnt/T3_US_MIT/hadoop",""))
        for e in lsst[1]:
            filePath = directory.replace("/mnt/T3_US_MIT/hadoop","root://t3serv017.mit.edu/") + e.name
            if "failed/" in filePath: continue
            if "log/" in filePath: continue
            if ".txt" in filePath: continue
            counter+=1
            if(counter > maxFiles): break
            rootFiles.push_back(filePath)

    else:
        for root, directories, filenames in os.walk(directory):
            for f in filenames:

                isBadFile = False
                filePath = os.path.join(os.path.abspath(root), f)
                filePath = filePath.replace("/mnt/T3_US_MIT/hadoop","root://t3serv017.mit.edu/")
                if "failed/" in filePath: continue
                if "log/" in filePath: continue
                if ".txt" in filePath: continue
                if(("XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX" in filePath) or

                   ("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" in filePath)
                   ): isBadFile = True

                if(isBadFile == True):
                    print("Bad file: {0}".format(filePath))
                    continue
                counter+=1
                if(counter > maxFiles): break
                rootFiles.push_back(filePath)

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

# split fIns files in group files
def groupFiles(fIns, group):

    ret =  [fIns[i::group] for i in range(group)]

    return ret

def concatenate(result, tmp1):
    for f in tmp1:
        result.push_back(f)

def getMClist(sampleNOW, skimType):

    files = findDIR("{}".format(SwitchSample(sampleNOW, skimType)[0]))
    return files

def getDATAlist(type, year, skimType):

    #dirT2 = "/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/"
    dirT2 = "/mnt/T3_US_MIT/hadoop/scratch/ceballos/nanoaod/skims_submit/" + skimType

    if(year == 2018):
        jsnName = "Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
        if os.path.exists(os.path.join("../skimming/jsns/",jsnName)):
            loadJSON(os.path.join("../skimming/jsns",jsnName))
        else:
            loadJSON(jsnName)

    files1 = []
    if(year == 2018 and type == 101):
        files1 = findDIR("{0}/SingleMuon+Run2018A-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 102):
        files1 = findDIR("{0}/SingleMuon+Run2018B-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 103):
        files1 = findDIR("{0}/SingleMuon+Run2018C-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 104):
        files1 = findDIR("{0}/SingleMuon+Run2018D-UL2018_MiniAODv2-v3+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 105):
        files1 = findDIR("{0}/DoubleMuon+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 106):
        files1 = findDIR("{0}/DoubleMuon+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 107):
        files1 = findDIR("{0}/DoubleMuon+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 108):
        files1 = findDIR("{0}/DoubleMuon+Run2018D-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 109):
        files1 = findDIR("{0}/MuonEG+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 110):
        files1 = findDIR("{0}/MuonEG+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 111):
        files1 = findDIR("{0}/MuonEG+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 112):
        files1 = findDIR("{0}/MuonEG+Run2018D-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 113):
        files1 = findDIR("{0}/EGamma+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 114):
        files1 = findDIR("{0}/EGamma+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 115):
        files1 = findDIR("{0}/EGamma+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 116):
        files1 = findDIR("{0}/EGamma+Run2018D-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))

    files = ROOT.vector('string')()
    concatenate(files, files1)

    return files

def SwitchSample(argument, skimType):

    #dirT2 = "/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/"
    dirT2 = "/mnt/T3_US_MIT/hadoop/scratch/ceballos/nanoaod/skims_submit/" + skimType
    dirLocal = "/work/submit/mariadlf/Hrare/OCT14"

    switch = {
        0: (dirT2+"/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v1+MINIAODSIM",2008.4*3*1000,plotCategory("kPlotDY")),
        1: (dirT2+"/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",20508.9*3*1000,plotCategory("kPlotOther")),
        2: (dirT2+"/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",831.76*0.1086*0.1086*9*1000,plotCategory("kPlotTop")),
        3: (dirT2+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2+MINIAODSIM",831.76*0.1086*3*(1-0.1086*3)*2*1000,plotCategory("kPlotTop")),
        10:(dirLocal+"/ZLLphigamma_pythia8_genFix",0.10*1000,plotCategory("kPlotBSM"))

    }
    return switch.get(argument, "BKGdefault, xsecDefault, category")

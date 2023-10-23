import ROOT
import os, json, sys
from utilsCategory import plotCategory
from subprocess import call,check_output
#from correctionlib import _core
import correctionlib
correctionlib.register_pyroot_binding()
#ROOT.gInterpreter.Declare('#include "mysf.h"')
#ROOT.gInterpreter.Load("mysf.so")

useXROOTD = False

def getLumi(year):
    lumi = [36.1, 41.5, 60.0, 8.2, 26.0, 17.1, 9.5]

    lumiBit = -999
    if(year == 2016): lumiBit = 0
    elif(year == 2017): lumiBit = 1
    elif(year == 2018): lumiBit = 2
    elif(year == 20220): lumiBit = 3
    elif(year == 20221): lumiBit = 4
    elif(year == 20230): lumiBit = 5
    elif(year == 20231): lumiBit = 6

    print("lumi({0}/{1}) = {2}".format(year,lumiBit,lumi[lumiBit]))

    return lumi[lumiBit]

if "/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("functions.cc","k")

#def loadCorrectionSet(year):
#    ROOT.gInterpreter.Load("mysf.so")
#    ROOT.gInterpreter.Declare('#include "mysf.h"')
#    ROOT.gInterpreter.ProcessLine('auto corr_sf = MyCorrections(%d);' % (year))

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

def getTriggerFromJson(overall, type, year ):

    if(year > 10000): year = year // 10

    for trigger in overall:
        if(trigger['name'] == type and trigger['year'] == year): return trigger['definition']

def getMesonFromJson(overall, type, cat ):

    for meson in overall:
        if meson['name'] == type and meson['type'] == cat: return meson['definition']

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

    if(useXROOTD == True and "/data/submit/cms" in directory):
        xrd = "root://submit50.mit.edu"
        xrdpath = directory.replace("/data/submit/cms","")
        f = check_output(['xrdfs', f'{xrd}', 'ls', xrdpath]).decode(sys.stdout.encoding)
        stringFiles = f.split()
        for e in range(len(stringFiles)):
            filePath = os.path.join(xrd,stringFiles[e])
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

    #print(rootFiles)
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

    if(year > 10000): year = year // 10

    #dirT2 = "/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/"
    #dirT2 = "/mnt/T3_US_MIT/hadoop/scratch/ceballos/nanoaod/skims_submit/" + skimType
    dirT2 = "/data/submit/cms/store/user/ceballos/nanoaod/skims_submit/" + skimType
    dirTest = "/data/submit/cms/store/user/ceballos/test/test/"

    jsnName = ""
    if(year == 2016):
        jsnName = "Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt"
    elif(year == 2017):
        jsnName = "Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt"
    elif(year == 2018):
        jsnName = "Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
    elif(year == 2022):
        jsnName = "Cert_Collisions2022_355100_362760_Golden.json"
    elif(year == 2023):
        jsnName = "Cert_Collisions2023_366442_370790_Golden.json"

    if os.path.exists(os.path.join("jsns",jsnName)):
        loadJSON(os.path.join("jsns",jsnName))
    else:
        loadJSON(jsnName)

    filesL = []
    ##### 2018 ####
    if(year == 2018 and type == 1000):
        filesL = findDIR("{0}/SingleMuon+Run2018A-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1001):
        filesL = findDIR("{0}/SingleMuon+Run2018B-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1002):
        filesL = findDIR("{0}/SingleMuon+Run2018C-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1003):
        filesL = findDIR("{0}/SingleMuon+Run2018D-UL2018_MiniAODv2-v3+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 1010):
        filesL = findDIR("{0}/DoubleMuon+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1011):
        filesL = findDIR("{0}/DoubleMuon+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1012):
        filesL = findDIR("{0}/DoubleMuon+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1013):
        filesL = findDIR("{0}/DoubleMuon+Run2018D-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 1020):
        filesL = findDIR("{0}/MuonEG+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1021):
        filesL = findDIR("{0}/MuonEG+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1022):
        filesL = findDIR("{0}/MuonEG+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1023):
        filesL = findDIR("{0}/MuonEG+Run2018D-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 1030):
        filesL = findDIR("{0}/EGamma+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1031):
        filesL = findDIR("{0}/EGamma+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1032):
        filesL = findDIR("{0}/EGamma+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1033):
        filesL = findDIR("{0}/EGamma+Run2018D-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 1050):
        filesL = findDIR("{0}/MET+Run2018A-UL2018_MiniAODv2_NanoAODv9-v2+NANOAOD".format(dirT2))
    elif(year == 2018 and type == 1051):
        filesL = findDIR("{0}/MET+Run2018B-UL2018_MiniAODv2_NanoAODv9-v2+NANOAOD".format(dirT2))
    elif(year == 2018 and type == 1052):
        filesL = findDIR("{0}/MET+Run2018C-UL2018_MiniAODv2_NanoAODv9-v1+NANOAOD".format(dirT2))
    elif(year == 2018 and type == 1053):
        filesL = findDIR("{0}/MET+Run2018D-UL2018_MiniAODv2_NanoAODv9-v1+NANOAOD".format(dirT2))

    ##### 2022 ####
    elif(year == 2022 and type == 1001):
        filesL = findDIR("{0}/SingleMuon+Run2022B-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1002):
        filesL = findDIR("{0}/SingleMuon+Run2022C-22Sep2023-v1+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 1011):
        filesL = findDIR("{0}/DoubleMuon+Run2022B-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1012):
        filesL = findDIR("{0}/DoubleMuon+Run2022C-22Sep2023-v1+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 1021):
        filesL = findDIR("{0}/MuonEG+Run2022B-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1022):
        filesL = findDIR("{0}/MuonEG+Run2022C-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1023):
        filesL = findDIR("{0}/MuonEG+Run2022D-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1024):
        filesL = findDIR("{0}/MuonEG+Run2022E-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1025):
        filesL = findDIR("{0}/MuonEG+Run2022F-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1026):
        filesL = findDIR("{0}/MuonEG+Run2022G-22Sep2023-v1+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 1031):
        filesL = findDIR("{0}/EGamma+Run2022B-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1032):
        filesL = findDIR("{0}/EGamma+Run2022C-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1033):
        filesL = findDIR("{0}/EGamma+Run2022D-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1034):
        filesL = findDIR("{0}/EGamma+Run2022E-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1035):
        filesL = findDIR("{0}/EGamma+Run2022F-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1036):
        filesL = findDIR("{0}/EGamma+Run2022G-22Sep2023-v1+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 1042):
        filesL = findDIR("{0}/Muon+Run2022C-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1043):
        filesL = findDIR("{0}/Muon+Run2022D-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1044):
        filesL = findDIR("{0}/Muon+Run2022E-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1045):
        filesL = findDIR("{0}/Muon+Run2022F-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1046):
        filesL = findDIR("{0}/Muon+Run2022G-22Sep2023-v1+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 1051):
        filesL = findDIR("{0}/MET+Run2022B-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1052):
        filesL = findDIR("{0}/MET+Run2022C-22Sep2023-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/JetMET+Run2022C-22Sep2023-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
    elif(year == 2022 and type == 1053):
        filesL = findDIR("{0}/JetMET+Run2022D-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1054):
        filesL = findDIR("{0}/JetMET+Run2022E-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1055):
        filesL = findDIR("{0}/JetMET+Run2022F-22Sep2023-v1+NANOAOD".format(dirT2))
    elif(year == 2022 and type == 1056):
        filesL = findDIR("{0}/JetMET+Run2022G-22Sep2023-v1+NANOAOD".format(dirT2))

    ##### 2023 ####
    elif(year == 2023 and type == 1022):
        filesL = findDIR("{0}/MuonEG+Run2023C-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/MuonEG+Run2023C-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/MuonEG+Run2023C-22Sep2023_v3-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/MuonEG+Run2023C-22Sep2023_v4-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
    elif(year == 2023 and type == 1023):
        filesL = findDIR("{0}/MuonEG+Run2023D-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/MuonEG+Run2023D-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)

    elif(year == 2023 and type == 1032):
        filesL   = findDIR("{0}/EGamma0+Run2023C-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/EGamma0+Run2023C-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/EGamma0+Run2023C-22Sep2023_v3-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/EGamma0+Run2023C-22Sep2023_v4-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/EGamma1+Run2023C-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/EGamma1+Run2023C-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/EGamma1+Run2023C-22Sep2023_v3-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/EGamma1+Run2023C-22Sep2023_v4-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
    elif(year == 2023 and type == 1033):
        filesL   = findDIR("{0}/EGamma0+Run2023D-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/EGamma0+Run2023D-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/EGamma1+Run2023D-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/EGamma1+Run2023D-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)

    elif(year == 2023 and type == 1042):
        filesL   = findDIR("{0}/Muon0+Run2023C-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/Muon0+Run2023C-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/Muon0+Run2023C-22Sep2023_v3-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/Muon0+Run2023C-22Sep2023_v4-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/Muon1+Run2023C-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/Muon1+Run2023C-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/Muon1+Run2023C-22Sep2023_v3-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/Muon1+Run2023C-22Sep2023_v4-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
    elif(year == 2023 and type == 1043):
        filesL   = findDIR("{0}/Muon0+Run2023D-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/Muon0+Run2023D-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/Muon1+Run2023D-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/Muon1+Run2023D-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)

    elif(year == 2023 and type == 1052):
        filesL   = findDIR("{0}/JetMET0+Run2023C-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/JetMET0+Run2023C-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/JetMET0+Run2023C-22Sep2023_v3-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/JetMET0+Run2023C-22Sep2023_v4-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/JetMET1+Run2023C-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/JetMET1+Run2023C-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/JetMET1+Run2023C-22Sep2023_v3-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/JetMET1+Run2023C-22Sep2023_v4-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
    elif(year == 2023 and type == 1053):
        filesL   = findDIR("{0}/JetMET0+Run2023D-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        filesAux = findDIR("{0}/JetMET0+Run2023D-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/JetMET1+Run2023D-22Sep2023_v1-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)
        filesAux = findDIR("{0}/JetMET1+Run2023D-22Sep2023_v2-v1+NANOAOD".format(dirT2))
        for x in filesAux:
            filesL.push_back(x)

    elif(year == 2022 and type == 9999):
        filesL = findDIR("{0}".format(dirTest))

    files = ROOT.vector('string')()
    concatenate(files, filesL)

    return files

def SwitchSample(argument, skimType):

    #dirT2 = "/scratch/submit/cms/ceballos/nanoaod/skims_submit/" + skimType
    dirT2 = "/data/submit/cms/store/user/ceballos/nanoaod/skims_submit/" + skimType
    dirLocal = "/work/submit/mariadlf/Hrare/D01"

    switch = {
       100: (dirT2+"/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",19982.5*1000,plotCategory("kPlotDY")),
       101: (dirT2+"/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",6345.99*1000,plotCategory("kPlotDY")),
       102: (dirT2+"/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",(118.7*1.06-3.51313)*0.1086*0.1086*9*1000,plotCategory("kPlotqqWW")),
       103: (dirT2+"/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",4.924*1.08*1000,plotCategory("kPlotWZ")),
       104: (dirT2+"/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",7.568*1.08*1000,plotCategory("kPlotWZ")),
       105: (dirT2+"/ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",6.788*1.19*1000,plotCategory("kPlotZZ")),
       106: (dirT2+"/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",1.031*1.16*1000,plotCategory("kPlotZZ")),
       107: (dirT2+"/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",1.390*1.19*1000,plotCategory("kPlotZZ")),
       108: (dirT2+"/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.95*923.6*0.1086*0.1086*9*1000,plotCategory("kPlotTop")),
       109: (dirT2+"/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.95*923.6*0.1086*3*(1-0.1086*3)*2*1000,plotCategory("kPlotTop")),
       110: (dirT2+"/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5_ext1-v2+NANOAODSIM",1000000*0.95*923.6*(1-0.1086*3)*(1-0.1086*3)*1000,plotCategory("kPlotNonPrompt")),
       111: (dirT2+"/TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",24.2*1000,plotCategory("kPlotTop")),
       112: (dirT2+"/TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",24.2*1000,plotCategory("kPlotTop")),
       113: (dirT2+"/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",64481.58*1000,plotCategory("kPlotOther")),
       114: (dirT2+"/WWW_4F_TuneCP5_13p6TeV_amcatnlo-madspin-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.23280*1000,plotCategory("kPlotVVV")),
       115: (dirT2+"/WWZ_4F_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.18510*1000,plotCategory("kPlotVVV")),
       116: (dirT2+"/WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.06206*1000,plotCategory("kPlotVVV")),
       117: (dirT2+"/ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.01591*1000,plotCategory("kPlotVVV")),
       118: (dirT2+"/WZGtoLNuZG_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.08425*1000,plotCategory("kPlotVVV")),
       119: (dirT2+"/TTWW_TuneCP5_13p6TeV_madgraph-madspin-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.0081651*1000,plotCategory("kPlotTVX")),
       120: (dirT2+"/TTZZ_TuneCP5_13p6TeV_madgraph-madspin-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.0015617*1000,plotCategory("kPlotTVX")),
       121: (dirT2+"/GluGluHtoZZto4L_M-125_TuneCP5_13p6TeV_powheg2-JHUGenV752-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",52.230*0.0264*0.101*0.101*1000,plotCategory("kPlotHiggs")),
       122: (dirT2+"/VBFHto2Zto4L_M125_TuneCP5_13p6TeV_powheg-jhugenv752-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",4.0780*0.0264*0.101*0.101*1000,plotCategory("kPlotHiggs")),
       123: (dirT2+"/TTLL_MLL-4to50_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.03949*1000,plotCategory("kPlotTVX")),
       124: (dirT2+"/TTLL_MLL-50_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.08646*1000,plotCategory("kPlotTVX")),
       125: (dirT2+"/ggWWto2L2Nu_OS_PolarizationLL_TuneCP5_13p6TeV_madgraph-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.24053*1.4*1000,plotCategory("kPlotqqWW")),
       126: (dirT2+"/ggWWto2L2Nu_OS_PolarizationLT_TuneCP5_13p6TeV_madgraph-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.08268*1.4*1000,plotCategory("kPlotqqWW")),
       127: (dirT2+"/ggWWto2L2Nu_OS_PolarizationTL_TuneCP5_13p6TeV_madgraph-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.08268*1.4*1000,plotCategory("kPlotqqWW")),
       128: (dirT2+"/ggWWto2L2Nu_OS_PolarizationTT_TuneCP5_13p6TeV_madgraph-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",3.10724*1.4*1000,plotCategory("kPlotqqWW")),
       129: (dirT2+"/DYGto2LG-1Jets_MLL-50_PTG-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",124.18762*1000,plotCategory("kPlotVG")),
       130: (dirT2+"/DYGto2LG-1Jets_MLL-50_PTG-50to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",2.08977*1000,plotCategory("kPlotVG")),
       131: (dirT2+"/DYGto2LG-1Jets_MLL-50_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.34767*1000,plotCategory("kPlotVG")),
       132: (dirT2+"/DYGto2LG-1Jets_MLL-50_PTG-200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.04734*1000,plotCategory("kPlotVG")),
       133: (dirT2+"/WGtoLNuG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",668.91538*1000,plotCategory("kPlotVG")),
       134: (dirT2+"/WGtoLNuG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",2.22141*1000,plotCategory("kPlotVG")),
       135: (dirT2+"/WGtoLNuG-1Jets_PTG-200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",0.31679*1000,plotCategory("kPlotVG")),
       136: (dirT2+"/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",1000000*(118.7*1.06-3.51313)*(1-0.1086*3)*(1-0.1086*3)*1000,plotCategory("kPlotNonPrompt")),
       137: (dirT2+"/GluGluHToTauTau_M-125_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",52.230*0.0632*1000,plotCategory("kPlotHiggs")),
       138: (dirT2+"/VBFHToTauTau_M125_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22NanoAODv12-130X_mcRun3_2022_realistic_v5-v2+NANOAODSIM",4.0780*0.0632*1000,plotCategory("kPlotHiggs")),

       200: (dirT2+"/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",19982.5*1000,plotCategory("kPlotDY")),
       201: (dirT2+"/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",6345.99*1000,plotCategory("kPlotDY")),
       202: (dirT2+"/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",(118.7*1.06-3.51313)*0.1086*0.1086*9*1000,plotCategory("kPlotqqWW")),
       203: (dirT2+"/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",4.924*1.08*1000,plotCategory("kPlotWZ")),
       204: (dirT2+"/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",7.568*1.08*1000,plotCategory("kPlotWZ")),
       205: (dirT2+"/ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",6.788*1.19*1000,plotCategory("kPlotZZ")),
       206: (dirT2+"/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",1.031*1.16*1000,plotCategory("kPlotZZ")),
       207: (dirT2+"/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",1.390*1.19*1000,plotCategory("kPlotZZ")),
       208: (dirT2+"/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.95*923.6*0.1086*0.1086*9*1000,plotCategory("kPlotTop")),
       209: (dirT2+"/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.95*923.6*0.1086*3*(1-0.1086*3)*2*1000,plotCategory("kPlotTop")),
       210: (dirT2+"/TTto4Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",1000000*0.95*923.6*(1-0.1086*3)*(1-0.1086*3)*1000,plotCategory("kPlotNonPrompt")),
       211: (dirT2+"/TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",24.2*1000,plotCategory("kPlotTop")),
       212: (dirT2+"/TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",24.2*1000,plotCategory("kPlotTop")),
       213: (dirT2+"/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",64481.58*1000,plotCategory("kPlotOther")),
       214: (dirT2+"/WWW_4F_TuneCP5_13p6TeV_amcatnlo-madspin-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.23280*1000,plotCategory("kPlotVVV")),
       215: (dirT2+"/WWZ_4F_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.18510*1000,plotCategory("kPlotVVV")),
       216: (dirT2+"/WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.06206*1000,plotCategory("kPlotVVV")),
       217: (dirT2+"/ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.01591*1000,plotCategory("kPlotVVV")),
       218: (dirT2+"/WZGtoLNuZG_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.08425*1000,plotCategory("kPlotVVV")),
       219: (dirT2+"/TTWW_TuneCP5_13p6TeV_madgraph-madspin-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.0081651*1000,plotCategory("kPlotTVX")),
       220: (dirT2+"/TTZZ_TuneCP5_13p6TeV_madgraph-madspin-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.0015617*1000,plotCategory("kPlotTVX")),
       221: (dirT2+"/GluGluHtoZZto4L_M-125_TuneCP5_13p6TeV_powheg2-JHUGenV752-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",52.230*0.0264*0.101*0.101*1000,plotCategory("kPlotHiggs")),
       222: (dirT2+"/VBFHto2Zto4L_M125_TuneCP5_13p6TeV_powheg-jhugenv752-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",4.0780*0.0264*0.101*0.101*1000,plotCategory("kPlotHiggs")),
       223: (dirT2+"/TTLL_MLL-4to50_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.03949*1000,plotCategory("kPlotTVX")),
       224: (dirT2+"/TTLL_MLL-50_TuneCP5_13p6TeV_amcatnlo-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.08646*1000,plotCategory("kPlotTVX")),
       225: (dirT2+"/ggWWto2L2Nu_OS_PolarizationLL_TuneCP5_13p6TeV_madgraph-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.24053*1.4*1000,plotCategory("kPlotqqWW")),
       226: (dirT2+"/ggWWto2L2Nu_OS_PolarizationLT_TuneCP5_13p6TeV_madgraph-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.08268*1.4*1000,plotCategory("kPlotqqWW")),
       227: (dirT2+"/ggWWto2L2Nu_OS_PolarizationTL_TuneCP5_13p6TeV_madgraph-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.08268*1.4*1000,plotCategory("kPlotqqWW")),
       228: (dirT2+"/ggWWto2L2Nu_OS_PolarizationTT_TuneCP5_13p6TeV_madgraph-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",3.10724*1.4*1000,plotCategory("kPlotqqWW")),
       229: (dirT2+"/DYGto2LG-1Jets_MLL-50_PTG-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",124.18762*1000,plotCategory("kPlotVG")),
       230: (dirT2+"/DYGto2LG-1Jets_MLL-50_PTG-50to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1+NANOAODSIM",2.08977*1000,plotCategory("kPlotVG")),
       231: (dirT2+"/DYGto2LG-1Jets_MLL-50_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.34767*1000,plotCategory("kPlotVG")),
       232: (dirT2+"/DYGto2LG-1Jets_MLL-50_PTG-200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v1+NANOAODSIM",0.04734*1000,plotCategory("kPlotVG")),
       233: (dirT2+"/WGtoLNuG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",668.91538*1000,plotCategory("kPlotVG")),
       234: (dirT2+"/WGtoLNuG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",2.22141*1000,plotCategory("kPlotVG")),
       235: (dirT2+"/WGtoLNuG-1Jets_PTG-200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",0.31679*1000,plotCategory("kPlotVG")),
       236: (dirT2+"/WWto4Q_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",1000000*(118.7*1.06-3.51313)*(1-0.1086*3)*(1-0.1086*3)*1000,plotCategory("kPlotNonPrompt")),
       237: (dirT2+"/GluGluHToTauTau_M-125_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",52.230*0.0632*1000,plotCategory("kPlotHiggs")),
       238: (dirT2+"/VBFHToTauTau_M125_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv12-130X_mcRun3_2022_realistic_postEE_v6-v2+NANOAODSIM",4.0780*0.0632*1000,plotCategory("kPlotHiggs")),

         0: (dirT2+"/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",2008.4*3*3.78*1000,plotCategory("kPlotDY")),
         1: (dirT2+"/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",2008.4*3*1000,plotCategory("kPlotDY")),

         2: (dirT2+"/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",20508.9*3*1000,plotCategory("kPlotOther")),

         3: (dirT2+"/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",831.76*0.1086*0.1086*9*1000,plotCategory("kPlotTop")),
         4: (dirT2+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2+MINIAODSIM",831.76*0.1086*3*(1-0.1086*3)*2*1000,plotCategory("kPlotTop")),
         5: (dirT2+"/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",35.6*(1.0-((1-0.1086*3)*(1-0.1086*3)))*1000,plotCategory("kPlotTop")),
         6: (dirT2+"/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",35.6*(1.0-((1-0.1086*3)*(1-0.1086*3)))*1000,plotCategory("kPlotTop")),

         7: (dirT2+"/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",(118.7-3.974)*0.1086*0.1086*9*1000,plotCategory("kPlotqqWW")),
         8: (dirT2+"/GluGluToWWToENEN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),
         9: (dirT2+"/GluGluToWWToENMN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),
        10: (dirT2+"/GluGluToWWToENTN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),
        11: (dirT2+"/GluGluToWWToMNEN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),
        12: (dirT2+"/GluGluToWWToMNMN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),
        13: (dirT2+"/GluGluToWWToMNTN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),
        14: (dirT2+"/GluGluToWWToTNEN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),
        15: (dirT2+"/GluGluToWWToTNMN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),
        16: (dirT2+"/GluGluToWWToTNTN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotqqWW")),

        17: (dirT2+"/WZTo3LNu_mllmin4p0_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",4.658*1.109*1000,plotCategory("kPlotWZ")),
        18: (dirT2+"/WZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",9.302*1000,plotCategory("kPlotWZ")),
        19: (dirT2+"/WZJJ_EWK_InclusivePolarization_TuneCP5_13TeV_madgraph-madspin-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.01654*1000,plotCategory("kPlotEWKWZ")),

        20: (dirT2+"/ZZTo2L2Nu_TuneCP5_13TeV_powheg_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.600*1000,plotCategory("kPlotZZ")),
        21: (dirT2+"/GluGluToContinToZZTo2e2nu_TuneCP5_13TeV-mcfm701-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.001720*2.3*1000,plotCategory("kPlotZZ")),
        22: (dirT2+"/GluGluToContinToZZTo2mu2nu_TuneCP5_13TeV-mcfm701-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.001720*2.3*1000,plotCategory("kPlotZZ")),

        23: (dirT2+"/ZZTo4L_TuneCP5_13TeV_powheg_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",1.256*1000,plotCategory("kPlotZZ")),
        24: (dirT2+"/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.001586*2.3*1000,plotCategory("kPlotZZ")),
        25: (dirT2+"/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.001586*2.3*1000,plotCategory("kPlotZZ")),
        26: (dirT2+"/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.001586*2.3*1000,plotCategory("kPlotZZ")),
        27: (dirT2+"/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.003194*2.3*1000,plotCategory("kPlotZZ")),
        28: (dirT2+"/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.003194*2.3*1000,plotCategory("kPlotZZ")),
        29: (dirT2+"/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.003194*2.3*1000,plotCategory("kPlotZZ")),
        30: (dirT2+"/ZZTo2Q2L_mllmin4p0_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.74*1000,plotCategory("kPlotZZ")),

        31: (dirT2+"/GluGluHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",48.580*0.0632*1000,plotCategory("kPlotHiggs")),
        32: (dirT2+"/GluGluHToWWTo2L2Nu_M-125_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",48.580*0.2150*0.1086*0.1086*9*1000,plotCategory("kPlotHiggs")),
        33: (dirT2+"/GluGluHToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",48.580*0.0264*0.101*0.101*1000,plotCategory("kPlotHiggs")),
        34: (dirT2+"/VBFHToTauTau_M125_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.7820*0.0632*1000,plotCategory("kPlotHiggs")),
        35: (dirT2+"/VBFHToWWTo2L2Nu_M-125_TuneCP5_13TeV-powheg-jhugen727-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.7820*0.2150*0.1086*0.1086*9*1000,plotCategory("kPlotHiggs")),
        36: (dirT2+"/VBF_HToZZTo4L_M125_TuneCP5_13TeV_powheg2_JHUGenV7011_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.7820*0.0264*0.101*0.101*1000,plotCategory("kPlotHiggs")),
        37: (dirT2+"/VHToNonbb_M125_TuneCP5_13TeV-amcatnloFXFX_madspin_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",(0.8839+0.8400+0.5328)*(1-0.577)*1000,plotCategory("kPlotHiggs")),
        38: (dirT2+"/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.5071*(1-0.577)*1000,plotCategory("kPlotHiggs")),

        39: (dirT2+"/TTGJets_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",4.322*1000,plotCategory("kPlotTop")),
        40: (dirT2+"/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.21845*1000,plotCategory("kPlotTVX")),
        41: (dirT2+"/TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.43171*1000,plotCategory("kPlotTVX")),
        42: (dirT2+"/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.24320*1000,plotCategory("kPlotTVX")),
        43: (dirT2+"/TTZToQQ_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.51040*1000,plotCategory("kPlotTVX")),
        44: (dirT2+"/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.07358*1000,plotCategory("kPlotTVX")),

        45: (dirT2+"/WGToLNuG_01J_5f_PDFWeights_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",179.21574*1000,plotCategory("kPlotVG")),
        46: (dirT2+"/ZGToLLG_01J_5f_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",50.43*1000,plotCategory("kPlotVG")),

        47: (dirT2+"/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.20860*1000,plotCategory("kPlotVVV")),
        48: (dirT2+"/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.16510*1000,plotCategory("kPlotVVV")),
        49: (dirT2+"/WZZ_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.05565*1000,plotCategory("kPlotVVV")),
        50: (dirT2+"/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.01398*1000,plotCategory("kPlotVVV")),
        51: (dirT2+"/WWG_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.21470*1000,plotCategory("kPlotVVV")),
        52: (dirT2+"/WZG_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.04345*1000,plotCategory("kPlotVVV")),

        53: (dirT2+"/SSWW_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.02982*1000,plotCategory("kPlotEWKSSWW")),

        61: (dirT2+"/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",2008.4*3*1000,plotCategory("kPlotDY")),
        62: (dirT2+"/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.92*4.658*1.109*1000,plotCategory("kPlotWZ")),
        63: (dirT2+"/WWJJToLNuLNu_EWK_noTop_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.09283*1000,plotCategory("kPlotqqWW")),
        64: (dirT2+"/WWJJToLNuLNu_QCD_noTop_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",2.19000*1000,plotCategory("kPlotqqWW")),

        65: (dirT2+"/DYJetsToLL_Pt-50To100_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",1.5*445.0*1000,plotCategory("kPlotDY")),
        66: (dirT2+"/DYJetsToLL_Pt-100To250_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",1.5*71.85*1000,plotCategory("kPlotDY")),
        67: (dirT2+"/DYJetsToLL_Pt-250To400_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",1.5*4.348*1000,plotCategory("kPlotDY")),
        68: (dirT2+"/DYJetsToLL_Pt-400To650_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",1.5*0.6236*1000,plotCategory("kPlotDY")),
        69: (dirT2+"/DYJetsToLL_Pt-650ToInf_MatchEWPDG20_TuneCP5_13TeV-amcatnloFXFX-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",1.5*0.04511*1000,plotCategory("kPlotDY")),

        70: (dirT2+"/TTHH_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.0007408*1000,plotCategory("kPlotTVX")),
        71: (dirT2+"/TTTT_TuneCP5_13TeV-amcatnlo-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.0120000*1000,plotCategory("kPlotTVX")),
        72: (dirT2+"/TTWW_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.0078820*1000,plotCategory("kPlotTVX")),
        73: (dirT2+"/TTZZ_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.0015720*1000,plotCategory("kPlotTVX")),
        74: (dirT2+"/TTTW_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.0007330*1000,plotCategory("kPlotTVX")),
        75: (dirT2+"/TTWH_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.0013590*1000,plotCategory("kPlotTVX")),
        76: (dirT2+"/TTWZ_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",0.0029740*1000,plotCategory("kPlotTVX")),
        77: (dirT2+"/TTZH_TuneCP5_13TeV-madgraph-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",0.0012530*1000,plotCategory("kPlotTVX")),

        78: (dirT2+"/GJets_DR-0p4_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",5027.300*1000,plotCategory("kPlotOther")),
        79: (dirT2+"/GJets_DR-0p4_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",1124.133*1000,plotCategory("kPlotOther")),
        80: (dirT2+"/GJets_DR-0p4_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",125.088*1000,plotCategory("kPlotOther")),
        81: (dirT2+"/GJets_DR-0p4_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",40.685*1000,plotCategory("kPlotOther")),
        82: (dirT2+"/QCD_Pt-15to7000_TuneCP5_Flat2018_13TeV_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",1000*1000,plotCategory("kPlotNonPrompt")),

        99:(dirLocal+"/2018/vbf-hphigamma-powheg/NANOAOD_01",1.0*1000,plotCategory("kPlotBSM")),
       199:(dirLocal+"/2018/vbf-hrhogamma-powheg/NANOAOD_01",1.0*1000,plotCategory("kPlotBSM")),
       299:(dirLocal+"/2018/vbf-hphiKLKSgamma-powheg/NANOAOD_01",1.0*1000,plotCategory("kPlotBSM")),
       396:("/data/submit/cms/store/user/ceballos/test_samples/DY_2022_preEE",1.0*1000,plotCategory("kPlotDY")),
       397:("/data/submit/cms/store/user/ceballos/test_samples/DY_2022_postEE",1.0*1000,plotCategory("kPlotDY")),
       398:("/data/submit/cms/store/user/ceballos/test_samples/qqWW_2022_postEE",1.0*1000,plotCategory("kPlotBSM")),
       399:("/data/submit/cms/store/user/ceballos/test_samples/qqWW_2016_preVFP",1.0*1000,plotCategory("kPlotBSM")),

    }
    return switch.get(argument, "BKGdefault, xsecDefault, category")

import ROOT
import os, json
from subprocess import call,check_output
from XRootD import client
#from correctionlib import _core
import correctionlib
correctionlib.register_pyroot_binding()
#ROOT.gInterpreter.Declare('#include "mysf.h"')
#ROOT.gInterpreter.Load("mysf.so")

useXROOTD = False

def getLumi(year):
    lumi = [36.1, 41.5, 60.0, 3.0]

    lumiBit = -1
    if(lumiBit == 2016): lumiBit = 0
    elif(lumiBit == 2017): lumiBit = 1
    elif(lumiBit == 2018): lumiBit = 2
    elif(lumiBit == 2022): lumiBit = 3

    return lumi[lumiBit]

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
        fs = client.FileSystem('root://submit50.mit.edu/')
        lsst = fs.dirlist(directory.replace("/data/submit/cms",""))
        for e in lsst[1]:
            filePath = os.path.join(directory.replace("/data/submit/cms","root://submit50.mit.edu/"),e.name)
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

    if os.path.exists(os.path.join("jsns",jsnName)):
        loadJSON(os.path.join("jsns",jsnName))
    else:
        loadJSON(jsnName)

    files1 = []
    if(year == 2018 and type == 1001):
        files1 = findDIR("{0}/SingleMuon+Run2018A-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1002):
        files1 = findDIR("{0}/SingleMuon+Run2018B-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1003):
        files1 = findDIR("{0}/SingleMuon+Run2018C-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1004):
        files1 = findDIR("{0}/SingleMuon+Run2018D-UL2018_MiniAODv2-v3+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 1005):
        files1 = findDIR("{0}/DoubleMuon+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1006):
        files1 = findDIR("{0}/DoubleMuon+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1007):
        files1 = findDIR("{0}/DoubleMuon+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1008):
        files1 = findDIR("{0}/DoubleMuon+Run2018D-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 1009):
        files1 = findDIR("{0}/MuonEG+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1010):
        files1 = findDIR("{0}/MuonEG+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1011):
        files1 = findDIR("{0}/MuonEG+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1012):
        files1 = findDIR("{0}/MuonEG+Run2018D-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 1013):
        files1 = findDIR("{0}/EGamma+Run2018A-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1014):
        files1 = findDIR("{0}/EGamma+Run2018B-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1015):
        files1 = findDIR("{0}/EGamma+Run2018C-UL2018_MiniAODv2-v1+MINIAOD".format(dirT2))
    elif(year == 2018 and type == 1016):
        files1 = findDIR("{0}/EGamma+Run2018D-UL2018_MiniAODv2-v2+MINIAOD".format(dirT2))

    elif(year == 2018 and type == 1021):
        files1 = findDIR("{0}/MET+Run2018A-UL2018_MiniAODv2_NanoAODv9-v2+NANOAOD".format(dirT2))
    elif(year == 2018 and type == 1022):
        files1 = findDIR("{0}/MET+Run2018B-UL2018_MiniAODv2_NanoAODv9-v2+NANOAOD".format(dirT2))
    elif(year == 2018 and type == 1023):
        files1 = findDIR("{0}/MET+Run2018C-UL2018_MiniAODv2_NanoAODv9-v1+NANOAOD".format(dirT2))
    elif(year == 2018 and type == 1024):
        files1 = findDIR("{0}/MET+Run2018D-UL2018_MiniAODv2_NanoAODv9-v1+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 1009):
        files1 = findDIR("{0}/MuonEG+Run2022G-PromptNanoAODv11_v1-v2+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 1013):
        files1 = findDIR("{0}/EGamma+Run2022G-PromptNanoAODv11_v1-v2+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 1017):
        files1 = findDIR("{0}/Muon+Run2022G-PromptNanoAODv11_v1-v2+NANOAOD".format(dirT2))

    elif(year == 2022 and type == 9999):
        files1 = findDIR("{0}".format(dirTest))

    files = ROOT.vector('string')()
    concatenate(files, files1)

    return files

def SwitchSample(argument, skimType):

    #dirT2 = "/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/"
    #dirT2 = "/mnt/T3_US_MIT/hadoop/scratch/ceballos/nanoaod/skims_submit/" + skimType
    dirT2 = "/data/submit/cms/store/user/ceballos/nanoaod/skims_submit/" + skimType
    dirLocal = "/work/submit/mariadlf/Hrare/D01"

    switch = {
         0: (dirT2+"/DYJetsToLL_M-10to50_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18NanoAODv9-20UL18JMENano_106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",2008.4*3*3.78*1000,plotCategory("kPlotDY")),
         1: (dirT2+"/DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",2008.4*3*1000,plotCategory("kPlotDY")),

         2: (dirT2+"/WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM",20508.9*3*1000,plotCategory("kPlotOther")),

         3: (dirT2+"/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",831.76*0.1086*0.1086*9*1000,plotCategory("kPlotTop")),
         4: (dirT2+"/TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2+MINIAODSIM",831.76*0.1086*3*(1-0.1086*3)*2*1000,plotCategory("kPlotTop")),
         5: (dirT2+"/ST_tW_antitop_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",35.6*(1.0-((1-0.1086*3)*(1-0.1086*3)))*1000,plotCategory("kPlotTop")),
         6: (dirT2+"/ST_tW_top_5f_NoFullyHadronicDecays_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",35.6*(1.0-((1-0.1086*3)*(1-0.1086*3)))*1000,plotCategory("kPlotTop")),

         7: (dirT2+"/WWTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",(118.7-3.974)*0.1086*0.1086*9*1000,plotCategory("kPlotqqWW")),
         8: (dirT2+"/GluGluToWWToENEN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),
         9: (dirT2+"/GluGluToWWToENMN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),
        10: (dirT2+"/GluGluToWWToENTN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),
        11: (dirT2+"/GluGluToWWToMNEN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),
        12: (dirT2+"/GluGluToWWToMNMN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),
        13: (dirT2+"/GluGluToWWToMNTN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),
        14: (dirT2+"/GluGluToWWToTNEN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),
        15: (dirT2+"/GluGluToWWToTNMN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),
        16: (dirT2+"/GluGluToWWToTNTN_TuneCP5_13TeV_MCFM701_pythia8+RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2+NANOAODSIM",3.974*0.1086*0.1086*1.4*1000,plotCategory("kPlotggWW")),

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
       399:("testsample",1.0*1000,plotCategory("kPlotBSM")),

       100: (dirT2+"/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1+NANOAODSIM",19317.5*1000,plotCategory("kPlotDY")),
       101: (dirT2+"/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1+NANOAODSIM",6221.3*1000,plotCategory("kPlotDY")),
       102: (dirT2+"/WW_TuneCP5_13p6TeV_pythia8+Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1+NANOAODSIM",122.3*1000,plotCategory("kPlotqqWW")),
       103: (dirT2+"/WZ_TuneCP5_13p6TeV_pythia8+Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1+NANOAODSIM",54.3*1000,plotCategory("kPlotWZ")),
       104: (dirT2+"/ZZ_TuneCP5_13p6TeV_pythia8+Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1+NANOAODSIM",16.7*1000,plotCategory("kPlotZZ")),
       105: (dirT2+"/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1+NANOAODSIM",923.6*0.1086*0.1086*9*1000,plotCategory("kPlotTop")),
       106: (dirT2+"/TTtoLNu2Q_MT-175p5_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1+NANOAODSIM",923.6*0.1086*3*(1-0.1086*3)*2*1000,plotCategory("kPlotTop")),
       107: (dirT2+"/TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1+NANOAODSIM",24.2*1000,plotCategory("kPlotTop")),
       108: (dirT2+"/TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8+Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1+NANOAODSIM",24.2*1000,plotCategory("kPlotTop")),
       109: (dirT2+"/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8+Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v1+NANOAODSIM",63199.9*1000,plotCategory("kPlotOther")),

    }
    return switch.get(argument, "BKGdefault, xsecDefault, category")

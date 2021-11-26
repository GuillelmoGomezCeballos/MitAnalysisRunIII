import ROOT
import os,json, sys
from subprocess import call,check_output
import fnmatch
import math

ROOT.ROOT.EnableImplicitMT(5)

if "/functions_skim.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("functions_skim.cc","k")

TRIGGERMUEG = "(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)"
TRIGGERDMU  = "(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)"
TRIGGERSMU  = "(HLT_IsoMu24||HLT_IsoMu27||HLT_Mu50)"
TRIGGERDEL  = "(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_DoubleEle25_CaloIdL_MW||HLT_DoublePhoton70)"
TRIGGERSEL  = "(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf||HLT_Ele115_CaloIdVT_GsfTrkIdT)"

def findDIR(directory):

    print(directory)

    counter = 0
    rootFiles = ROOT.vector('string')()
    for root, directories, filenames in os.walk(directory):
        for f in filenames:

            counter+=1
            filePath = os.path.join(os.path.abspath(root), f)
            if "failed/" in filePath: continue
            if "log/" in filePath: continue
            rootFiles.push_back(filePath)

    return rootFiles

def groupFiles(fIns, group):

    ret = [fIns[x:x+group] for x in range(0, len(fIns), group)]

    return ret

if __name__ == "__main__":

    group = 50
    fOutDir = "/work/submit/ceballos/skims/dil"
    dirT2 = "/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/"

    inputFolders = []
    inputFolders.append(dirT2+"SingleMuon+Run2018B-UL2018_MiniAODv2-v2+MINIAOD")
    inputFolders.append(dirT2+"SingleMuon+Run2018C-UL2018_MiniAODv2-v2+MINIAOD")
    inputFolders.append(dirT2+"SingleMuon+Run2018D-UL2018_MiniAODv2-v3+MINIAOD")
    inputFolders.append(dirT2+"SingleMuon+Run2018A-UL2018_MiniAODv2-v2+MINIAOD")

    inputFolders.append(dirT2+"DoubleMuon+Run2018A-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"DoubleMuon+Run2018B-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"DoubleMuon+Run2018C-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"DoubleMuon+Run2018D-UL2018_MiniAODv2-v1+MINIAOD")

    inputFolders.append(dirT2+"EGamma+Run2018A-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"EGamma+Run2018B-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"EGamma+Run2018C-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"EGamma+Run2018D-UL2018_MiniAODv2-v2+MINIAOD")

    inputFolders.append(dirT2+"MuonEG+Run2018A-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"MuonEG+Run2018B-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"MuonEG+Run2018C-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"MuonEG+Run2018D-UL2018_MiniAODv2-v1+MINIAOD")

    inputFolders.append(dirT2+"MuonEG+Run2018A-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"MuonEG+Run2018B-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"MuonEG+Run2018C-UL2018_MiniAODv2-v1+MINIAOD")
    inputFolders.append(dirT2+"MuonEG+Run2018D-UL2018_MiniAODv2-v1+MINIAOD")

    inputFolders.append(dirT2+"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v1+MINIAODSIM")
    inputFolders.append(dirT2+"WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM")
    inputFolders.append(dirT2+"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM")
    inputFolders.append(dirT2+"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2+MINIAODSIM")

    for inp in range(0, len(inputFolders)):
        if(inp == 999): continue
        files =findDIR(inputFolders[inp])
        basenameInput = os.path.basename(inputFolders[inp])
        finalOutputDir = os.path.join(fOutDir, basenameInput)
        print("Files to skim: {0} / input: {1} / output: {2}".format(len(files),inputFolders[inp],finalOutputDir))

        if not os.path.exists(finalOutputDir):
            try:
                os.makedirs(finalOutputDir)
            except Exception as e:
                print(e)

        groupedFiles = groupFiles(files, group)

        for i, groupedFile in enumerate(groupedFiles):
            try:
                fOutNameTEMP = "%s/temp_output_%d.root" % (finalOutputDir,i)
                fOutName     = "%s/output_%d.root"      % (finalOutputDir,i)

                msg = "python haddnanoaod.py %s" % (fOutNameTEMP)
                for f in range(len(groupedFile)):
                    msg = msg + " " + groupedFile[f]
                os.system(msg)

                print("Create {0}".format(fOutName))
                rdf = ROOT.RDataFrame("Events", fOutNameTEMP)\
                            .Define("trigger","{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG))\
                            .Filter("trigger > 0","Passed trigger")\
                            .Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 20 && Muon_looseId == true")\
                            .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 20 && Electron_cutBased >= 1")\
                            .Filter("Sum(loose_mu)+Sum(loose_el) >= 2","At least two loose leptons")\
                            .Define("goodmu_pt",    "Muon_pt[loose_mu]")\
                            .Define("goodmu_eta",   "Muon_eta[loose_mu]")\
                            .Define("goodmu_phi",   "Muon_phi[loose_mu]")\
                            .Define("goodmu_mass",  "Muon_mass[loose_mu]")\
                            .Define("goodel_pt",    "Electron_pt[loose_el]")\
                            .Define("goodel_eta",   "Electron_eta[loose_el]")\
                            .Define("goodel_phi",   "Electron_phi[loose_el]")\
                            .Define("goodel_mass",  "Electron_mass[loose_el]")\
                            .Define("skim",    "applySkim(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass)")\
                            .Filter("skim > 0","mll > 10 GeV or at least three loose leptons")\
                            .Snapshot("Events", fOutName)

                os.remove(fOutNameTEMP)

                del rdf

            except Exception as e:
                print("PROBLEM {0} / {1} / {2}".format(finalOutputDir,i,e))

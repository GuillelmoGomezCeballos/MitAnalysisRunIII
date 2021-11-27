import ROOT
from ROOT import TFile
import os, sys, getopt, json
from subprocess import call,check_output
import fnmatch
import math

ROOT.ROOT.EnableImplicitMT(5)

if "../macros/functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("../macros/functions.cc","k")

TRIGGERMUEG = "(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)"
TRIGGERDMU  = "(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)"
TRIGGERSMU  = "(HLT_IsoMu24||HLT_IsoMu27||HLT_Mu50)"
TRIGGERDEL  = "(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_DoubleEle25_CaloIdL_MW||HLT_DoublePhoton70)"
TRIGGERSEL  = "(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf||HLT_Ele115_CaloIdVT_GsfTrkIdT)"

TRIGGERFAKEMU = "(HLT_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL)"
TRIGGERFAKEEL = "(HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele15_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30)"

JSON = "isGoodRunLS(isData, run, luminosityBlock)"

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
    fOutDir0 = "/work/submit/ceballos/skims/dil"
    fOutDir1 = "/work/submit/ceballos/skims/ss_3l"
    fOutDir2 = "/work/submit/ceballos/skims/onel"
    dirT2 = "/mnt/T2_US_MIT/hadoop/cms/store/user/paus/nanohr/D00/"

    year   = 2018
    isData = 1

    valid = ['year=', "isData=", 'help']
    usage  =  "Usage: ana.py --year=<{0}>\n".format(year)
    usage +=  "              --isData=<{0}>".format(isData)
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
        if opt == "--isData":
            isData = int(arg)

    inputFolders = []
    if(year == 2018 and isData == 1):
        loadJSON("/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/13TeV/Legacy_2018/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt")
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

    elif(year == 2018 and isData == 0):
        inputFolders.append(dirT2+"DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1_ext1-v1+MINIAODSIM")
        inputFolders.append(dirT2+"WJetsToLNu_TuneCP5_13TeV-madgraphMLM-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM")
        inputFolders.append(dirT2+"TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v1+MINIAODSIM")
        inputFolders.append(dirT2+"TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8+RunIISummer20UL18MiniAODv2-106X_upgrade2018_realistic_v16_L1v1-v2+MINIAODSIM")

    for inp in range(0, len(inputFolders)):
        if(inp == 999): continue
        files =findDIR(inputFolders[inp])
        basenameInput = os.path.basename(inputFolders[inp])
        finalOutputDir0 = os.path.join(fOutDir0, basenameInput)
        finalOutputDir1 = os.path.join(fOutDir1, basenameInput)
        finalOutputDir2 = os.path.join(fOutDir2, basenameInput)
        print("Files to skim: {0} / input: {1} / output0: {2} / output1: {3} / output2: {4}".format(len(files),inputFolders[inp],finalOutputDir0,finalOutputDir1,finalOutputDir2))

        if not os.path.exists(finalOutputDir0):
            try:
                os.makedirs(finalOutputDir0)
            except Exception as e:
                print(e)

        if not os.path.exists(finalOutputDir1):
            try:
                os.makedirs(finalOutputDir1)
            except Exception as e:
                print(e)

        if not os.path.exists(finalOutputDir2):
            try:
                os.makedirs(finalOutputDir2)
            except Exception as e:
                print(e)

        groupedFiles = groupFiles(files, group)

        for i, groupedFile in enumerate(groupedFiles):
            if(i == 999): continue;
            try:
                fOutNameTEMP = "%s/temp_output_%d.root" % (finalOutputDir0,i)
                fOutName0    = "%s/output_%d.root"      % (finalOutputDir0,i)
                fOutName1    = "%s/output_%d.root"      % (finalOutputDir1,i)
                fOutName2    = "%s/output_%d.root"      % (finalOutputDir2,i)

                msg = "python haddnanoaod.py %s" % (fOutNameTEMP)
                for f in range(len(groupedFile)):
                    msg = msg + " " + groupedFile[f]
                os.system(msg)

                print("Create {0} / {1} / {2}".format(fOutName0,fOutName1,fOutName2))
                rdf = ROOT.RDataFrame("Events", fOutNameTEMP)\
                            .Define("isData","{}".format(isData))\
                            .Define("applyJson","{}".format(JSON)).Filter("applyJson","pass JSON")

                rdf_ll = rdf.Define("loose_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 20 && Muon_looseId == true")\
                            .Define("loose_el", "abs(Electron_eta) < 2.5 && Electron_pt > 20 && Electron_cutBased >= 1")\
                            .Define("trigger2l","{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG))\
                            .Filter("trigger2l > 0","Passed trigger2l")\
                            .Filter("Sum(loose_mu)+Sum(loose_el) >= 2","At least two loose leptons")\
                            .Define("goodmu_pt",    "Muon_pt[loose_mu]")\
                            .Define("goodmu_eta",   "Muon_eta[loose_mu]")\
                            .Define("goodmu_phi",   "Muon_phi[loose_mu]")\
                            .Define("goodmu_mass",  "Muon_mass[loose_mu]")\
                            .Define("goodmu_charge","Muon_charge[loose_mu]")\
                            .Define("goodel_pt",    "Electron_pt[loose_el]")\
                            .Define("goodel_eta",   "Electron_eta[loose_el]")\
                            .Define("goodel_phi",   "Electron_phi[loose_el]")\
                            .Define("goodel_mass",  "Electron_mass[loose_el]")\
                            .Define("goodel_charge","Electron_charge[loose_el]")\
                            .Define("good_lep_charge","Sum(goodmu_charge)+Sum(goodel_charge)")\
                            .Define("skim","applySkim(goodmu_pt, goodmu_eta, goodmu_phi, goodmu_mass, goodel_pt, goodel_eta, goodel_phi, goodel_mass, good_lep_charge, MET_pt)")

                rdf_dil = rdf_ll.Filter("skim >= 2","Two loose leptons with mll > 10 GeV")\
                                .Snapshot("Events", fOutName0)

                rdf_ss_3l = rdf_ll.Filter("skim == 1 || skim == 2 || skim == 3",">=3, q(l1+l2)!=0, met>50/ptll>50")\
                                  .Snapshot("Events", fOutName1)

                TRIGGERFAKE0 = TRIGGERFAKEMU
                TRIGGERFAKE1 = TRIGGERFAKEEL
                if(("SingleMuon+Run" in inputFolders[inp]) or ("DoubleMuon+Run" in inputFolders[inp]) or ("MuonEG+Run" in inputFolders[inp])):
                    TRIGGERFAKE1 = TRIGGERFAKEMU
                elif(("EGamma+Run" in inputFolders[inp]) or ("SingleElectron+Run" in inputFolders[inp]) or ("DoubleEG+Run" in inputFolders[inp])):
                    TRIGGERFAKE0 = TRIGGERFAKEEL

                print("triggerFake: {0} / {1}".format(TRIGGERFAKE0,TRIGGERFAKE1))
                rdf_onel = rdf.Define("trigger1l","{0} or {1}".format(TRIGGERFAKE0,TRIGGERFAKE1))\
                              .Filter("trigger1l > 0","Passed trigger1l")\
                              .Define("fake_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")\
                              .Define("fake_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")\
                              .Filter("Sum(fake_mu)+Sum(fake_el) == 1","One fake leptons")\
                              .Snapshot("Events", fOutName2)

                del rdf, rdf_ll, rdf_dil, rdf_ss_3l, rdf_onel

                fOutTEMP = TFile(fOutNameTEMP)
                runTree = fOutTEMP.Get("Runs")

                fOut0 = TFile(fOutName0,"UPDATE")
                fOut0.cd()
                runTreeCopy0 = runTree.CopyTree("");
                runTreeCopy0.Write()
                fOut0.Close()

                fOut1 = TFile(fOutName1,"UPDATE")
                fOut1.cd()
                runTreeCopy1 = runTree.CopyTree("");
                runTreeCopy1.Write()
                fOut1.Close()

                fOut2 = TFile(fOutName2,"UPDATE")
                fOut2.cd()
                runTreeCopy2 = runTree.CopyTree("");
                runTreeCopy2.Write()
                fOut2.Close()

                os.remove(fOutNameTEMP)

            except Exception as e:
                print("PROBLEM {0} / {1} / {2} / {3} / {4}".format(finalOutputDir0,finalOutputDir1,finalOutputDir2,i,e))

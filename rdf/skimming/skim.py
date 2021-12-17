import ROOT
import os, sys, getopt, json, time, subprocess, socket
import fnmatch
import math

ROOT.ROOT.EnableImplicitMT(2)

if "./functions.so" not in ROOT.gSystem.GetLibraries():
    ROOT.gSystem.CompileMacro("./functions.cc","k")

TRIGGERMUEG = "(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL||HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ)"
TRIGGERDMU  = "(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8||HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8)"
TRIGGERSMU  = "(HLT_IsoMu24||HLT_IsoMu27||HLT_Mu50)"
TRIGGERDEL  = "(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ||HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL||HLT_DoubleEle25_CaloIdL_MW||HLT_DoublePhoton70)"
TRIGGERSEL  = "(HLT_Ele27_WPTight_Gsf||HLT_Ele32_WPTight_Gsf||HLT_Ele32_WPTight_Gsf_L1DoubleEG||HLT_Ele35_WPTight_Gsf||HLT_Ele115_CaloIdVT_GsfTrkIdT)"

TRIGGERFAKEMU = "(HLT_Mu8_TrkIsoVVL||HLT_Mu17_TrkIsoVVL)"
TRIGGERFAKEEL = "(HLT_Ele8_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele15_CaloIdL_TrackIdL_IsoVL_PFJet30||HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30)"

JSON = "isGoodRunLS(isSkimData, run, luminosityBlock)"

def buildcommand(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, error = p.communicate()
    print("command {0}, out {1}, error{2}, returncode {3}".format(command,out,error,p.returncode))
    return p.returncode

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

# split fIns files in groups of group files 
def groupFiles(fIns, group):

    ret = [fIns[x:x+group] for x in range(0, len(fIns), group)]

    return ret

if __name__ == "__main__":

    copyFilesToFS = True

    outputDir = "root://t3serv017.mit.edu//scratch/ceballos/nanoaod/skims_submit"
    inputSamplesCfg = "skim_input_samples.cfg"
    inputFilesCfg = "skim_input_files.cfg"
    whichSample = 1
    whichJob = -1
    group = 10

    valid = ['outputDir=', "inputSamplesCfg=", "inputFilesCfg=", "whichSample=", "whichJob=", "group=", 'help']
    usage  =  "Usage: ana.py --outputDir=<{0}>\n".format(outputDir)
    usage +=  "              --inputSamplesCfg=<{0}>\n".format(inputSamplesCfg)
    usage +=  "              --inputFilesCfg=<{0}>\n".format(inputFilesCfg)
    usage +=  "              --whichSample=<{0}>\n".format(whichSample)
    usage +=  "              --whichJob=<{0}>".format(whichJob)
    usage +=  "              --group=<{0}>".format(group)
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
        if opt == "--outputDir":
            outputDir = str(arg)
        if opt == "--inputSamplesCfg":
            inputSamplesCfg = str(arg)
        if opt == "--inputFilesCfg":
            inputFilesCfg = str(arg)
        if opt == "--whichSample":
            whichSample = int(arg)
        if opt == "--whichJob":
            whichJob = int(arg)
        if opt == "--group":
            group = int(arg)

    theHost = socket.gethostname()
    msgCPInput  = "xrdcp --force"
    msgCPOutput = "xrdcp --force"
    isLocal = False
    if(("t3deskxxx" in theHost) or ("t3btchxxx" in theHost)):
        outputDir = outputDir.replace("root://t3serv017.mit.edu/","/mnt/hadoop")
        msgCPOutput = "cp"
        isLocal = True
        print("T3 node ({0}), outputDir = {1} / msgCPOutput = {2}".format(theHost,outputDir,msgCPOutput))

    elif("submitxxx" in theHost):
        outputDir = outputDir.replace("root://t3serv017.mit.edu/","/mnt/T3_US_MIT/hadoop")
        msgCPOutput = "cp"
        isLocal = True
        print("submit node ({0}), outputDir = {1} / msgCPOutput = {2}".format(theHost,outputDir,msgCPOutput))

    # Reading which sample we want to skim
    inputSamplesFile = open(inputSamplesCfg, 'r')
    linesSamplesFile = inputSamplesFile.readlines()
    if(whichSample < 0 or whichSample >= len(linesSamplesFile)):
        print("Incorrect whichSample: {0}".format(whichSample))
        sys.exit(1)
    sampleToSkim = linesSamplesFile[whichSample].strip()
    print("Sample to skim: {0}".format(sampleToSkim))

    year = -1
    isSkimData = -1
    if("Run2018" in sampleToSkim):
        year = 2018
        isSkimData = 1
    elif("RunIISummer20UL18" in sampleToSkim):
        year = 2018
        isSkimData = 0

    if(year == -1 or isSkimData == -1):
        print("Incorrect year/isSkimData: {0} / {1}".format(year, isSkimData))
        sys.exit(1)

    if(year == 2018):
        jsnName = "Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt"
        if os.path.exists(os.path.join("jsns",jsnName)):
            loadJSON(os.path.join("jsns",jsnName))
        else:
            loadJSON(jsnName)

    rootFiles = ROOT.vector('string')()
    inputFilesFile = open(inputFilesCfg, 'r')
    while True:
        line = inputFilesFile.readline().strip()
        if not line:
            break
        if(sampleToSkim not in line):
            continue
        rootFiles.push_back(line)

    groupedFiles = groupFiles(rootFiles, group)
    finalOutputDir1 = os.path.join(outputDir, "1l", sampleToSkim)
    finalOutputDir2 = os.path.join(outputDir, "2l", sampleToSkim)
    finalOutputDir3 = os.path.join(outputDir, "3l", sampleToSkim)
    print("Files to skim/jobs: {0}/{1} / outputDir: {2}".format(len(rootFiles),len(groupedFiles),outputDir))

    TRIGGERLEP = "{0} or {1} or {2} or {3} or {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    if("MuonEG+Run" in sampleToSkim):
        TRIGGERLEP = "{0}".format(TRIGGERMUEG)

    elif("DoubleMuon+Run" in sampleToSkim):
        TRIGGERLEP = "{0} and not {1}".format(TRIGGERDMU,TRIGGERMUEG)

    elif("SingleMuon+Run" in sampleToSkim):
        TRIGGERLEP = "{0} and not {1} and not {2}".format(TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    elif("EGamma+Run" in sampleToSkim):
        TRIGGERLEP = "({0} or {1}) and not {2} and not {3} and not {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    elif("DoubleEG+Run" in sampleToSkim):
        TRIGGERLEP = "{0} and not {1} and not {2} and not {3}".format(TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    elif("SingleElectron+Run" in sampleToSkim):
        TRIGGERLEP = "{0} and not {1} and not {2} and not {3} and not {4}".format(TRIGGERSEL,TRIGGERDEL,TRIGGERSMU,TRIGGERDMU,TRIGGERMUEG)

    elif("+Run20" in sampleToSkim):
        print("PROBLEM with triggers!!!")

    print("TRIGGERLEP: {0}".format(TRIGGERLEP))

    TRIGGERFAKE0 = TRIGGERFAKEMU
    TRIGGERFAKE1 = TRIGGERFAKEEL
    if(("SingleMuon+Run" in sampleToSkim) or ("DoubleMuon+Run" in sampleToSkim) or ("MuonEG+Run" in sampleToSkim)):
        TRIGGERFAKE1 = TRIGGERFAKEMU
    elif(("EGamma+Run" in sampleToSkim) or ("DoubleEG+Run" in sampleToSkim) or ("SingleElectron+Run" in sampleToSkim)):
        TRIGGERFAKE0 = TRIGGERFAKEEL

    print("TRIGGERFAKE: {0} / {1}".format(TRIGGERFAKE0,TRIGGERFAKE1))

    for i, groupedFile in enumerate(groupedFiles):
        passJob = whichJob == -1 or whichJob == i
        if(passJob == False): continue
        try:
            atLeastOneFile = [False, False, False]

            fOutName1 = "output_1l_%d_%d.root" % (whichSample,i)
            fOutName2 = "output_2l_%d_%d.root" % (whichSample,i)
            fOutName3 = "output_3l_%d_%d.root" % (whichSample,i)

            print("Create {0} / {1} / {2}".format(fOutName1,fOutName2,fOutName3))

            msgMerge1 = "python haddnanoaod.py %s" % (fOutName1)
            msgMerge2 = "python haddnanoaod.py %s" % (fOutName2)
            msgMerge3 = "python haddnanoaod.py %s" % (fOutName3)
            msgRm = "rm -f"

            isJobFailure = False

            for nf in range(len(groupedFile)):
                fOutIndivName1 = "output_1l_{0}_{1}_{2}.root".format(whichSample,i,nf)
                fOutIndivName2 = "output_2l_{0}_{1}_{2}.root".format(whichSample,i,nf)
                fOutIndivName3 = "output_3l_{0}_{1}_{2}.root".format(whichSample,i,nf)

                msgRm = msgRm + " " + fOutIndivName1
                msgRm = msgRm + " " + fOutIndivName2
                msgRm = msgRm + " " + fOutIndivName3

                inputSingleFile = groupedFile[nf]
                inputSingleFileBase = os.path.basename(inputSingleFile)
                copycommand = "%s %s %s" % (msgCPInput,inputSingleFile, inputSingleFileBase)

                copy_result = False
                n_retries = 0
                while n_retries < 5 and copy_result is False:
                    returncode = buildcommand(copycommand)
                    if os.path.exists(inputSingleFileBase) and returncode == 0:
                        copy_result = True
                    else:
                        print("Copying file {0} failed ({1}), retrying".format(inputSingleFileBase,returncode))
                        n_retries+=1
                        time.sleep(15)

                if(copy_result == False):
                    print("Copying file {0} failed completely, exiting the loop".format(inputSingleFileBase))
                    isJobFailure = True
                    break

                print("Processing({0}): {1}".format(nf,inputSingleFile))
                rdf = ROOT.RDataFrame("Events", inputSingleFileBase)\
                            .Define("isSkimData","{}".format(isSkimData))\
                            .Define("applyDataJson","{}".format(JSON)).Filter("applyDataJson","pass JSON")

                rdf_ll = rdf.Define("skim_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")\
                            .Define("skim_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")\
                            .Define("trigger2l","{0}".format(TRIGGERLEP))\
                            .Filter("trigger2l > 0","Passed trigger2l")\
                            .Filter("Sum(skim_mu)+Sum(skim_el) >= 2","At least two loose leptons")\
                            .Define("skimmu_pt",        "Muon_pt[skim_mu]")\
                            .Define("skimmu_eta",       "Muon_eta[skim_mu]")\
                            .Define("skimmu_phi",       "Muon_phi[skim_mu]")\
                            .Define("skimmu_mass",  "Muon_mass[skim_mu]")\
                            .Define("skimmu_charge","Muon_charge[skim_mu]")\
                            .Define("skimel_pt",        "Electron_pt[skim_el]")\
                            .Define("skimel_eta",       "Electron_eta[skim_el]")\
                            .Define("skimel_phi",       "Electron_phi[skim_el]")\
                            .Define("skimel_mass",  "Electron_mass[skim_el]")\
                            .Define("skimel_charge","Electron_charge[skim_el]")\
                            .Define("skim_lep_charge","Sum(skimmu_charge)+Sum(skimel_charge)")\
                            .Define("skim","applySkim(skimmu_pt, skimmu_eta, skimmu_phi, skimmu_mass, skimel_pt, skimel_eta, skimel_phi, skimel_mass, skim_lep_charge, MET_pt)")

                rdf_2l = rdf_ll.Filter("skim >= 2","Two loose leptons with mll > 10 GeV")\
                               .Snapshot("Events", fOutIndivName2)

                rdf_3l = rdf_ll.Filter("skim == 1 || skim == 2 || skim == 3",">=3, q(l1+l2)!=0, met>50/ptll>50")\
                               .Snapshot("Events", fOutIndivName3)

                rdf_1l = rdf.Define("trigger1l","{0} or {1}".format(TRIGGERFAKE0,TRIGGERFAKE1))\
                            .Filter("trigger1l > 0","Passed trigger1l")\
                            .Define("skim_fake_mu", "abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_looseId == true")\
                            .Define("skim_fake_el", "abs(Electron_eta) < 2.5 && Electron_pt > 10 && Electron_cutBased >= 1")\
                            .Filter("Sum(skim_fake_mu)+Sum(skim_fake_el) == 1","One fake lepton")\
                            .Snapshot("Events", fOutIndivName1)

                eventCounts = [0, 0, 0]
                try:
                    eventCounts[0] = rdf_1l.Count().GetValue()
                except Exception as e:
                    print("No selected events in {0}".format(fOutIndivName1))
                try:
                    eventCounts[1] = rdf_2l.Count().GetValue()
                except Exception as e:
                    print("No selected events in {0}".format(fOutIndivName2))
                try:
                    eventCounts[2] = rdf_3l.Count().GetValue()
                except Exception as e:
                    print("No selected events in {0}".format(fOutIndivName3))

                del rdf, rdf_ll, rdf_2l, rdf_3l, rdf_1l

                runTree = ROOT.TChain("Runs")
                runTree.AddFile(inputSingleFileBase)

                if(isSkimData == 0 or eventCounts[0] > 0):
                    fOut1 = ROOT.TFile(fOutIndivName1,"UPDATE")
                    fOut1.cd()
                    runTreeCopy1 = runTree.CopyTree("");
                    runTreeCopy1.Write()
                    fOut1.Close()
                    atLeastOneFile[0] = True
                    msgMerge1 = msgMerge1 + " " + fOutIndivName1

                if(isSkimData == 0 or eventCounts[1] > 0):
                    fOut2 = ROOT.TFile(fOutIndivName2,"UPDATE")
                    fOut2.cd()
                    runTreeCopy2 = runTree.CopyTree("");
                    runTreeCopy2.Write()
                    fOut2.Close()
                    atLeastOneFile[1] = True
                    msgMerge2 = msgMerge2 + " " + fOutIndivName2

                if(isSkimData == 0 or eventCounts[2] > 0):
                    fOut3 = ROOT.TFile(fOutIndivName3,"UPDATE")
                    fOut3.cd()
                    runTreeCopy3 = runTree.CopyTree("");
                    runTreeCopy3.Write()
                    fOut3.Close()
                    atLeastOneFile[2] = True
                    msgMerge3 = msgMerge3 + " " + fOutIndivName3

                os.remove(inputSingleFileBase)

            if(isJobFailure == True):
                print("Job ({0}/{1}) failed completely".format(outputDir,i))
                continue

            # haddnanoaod1
            copy_result = False
            n_retries = 0
            while n_retries < 5 and copy_result is False:
                returncode = 0
                if(atLeastOneFile[0] == True):
                    returncode = buildcommand(msgMerge1)
                if returncode == 0:
                    copy_result = True
                    if(isSkimData == 1):
                        try:
                            dftest = ROOT.RDataFrame("Events", fOutName1)
                            nevents = dftest.Count().GetValue()
                            del dftest
                        except Exception as e:
                            os.remove(fOutName1)
                            fOutName1 = "output_1l_%d_%d.txt" % (whichSample,i)
                            returntestcode = buildcommand("touch {0}".format(fOutName1))
                else:
                    print("haddnanoaod output file1 {0} failed ({1}), retrying".format(fOutName1,returncode))
                    n_retries+=1
                    time.sleep(15)
            if(copy_result == False):
                print("haddnanoaod output file1 {0} failed completely, exiting the loop".format(fOutName1))
                os.remove(fOutName1)

            # haddnanoaod2
            copy_result = False
            n_retries = 0
            while n_retries < 5 and copy_result is False:
                returncode = 0
                if(atLeastOneFile[1] == True):
                    returncode = buildcommand(msgMerge2)
                if returncode == 0:
                    copy_result = True
                    if(isSkimData == 1):
                        try:
                            dftest = ROOT.RDataFrame("Events", fOutName2)
                            nevents = dftest.Count().GetValue()
                            del dftest
                        except Exception as e:
                            os.remove(fOutName2)
                            fOutName2 = "output_2l_%d_%d.txt" % (whichSample,i)
                            returntestcode = buildcommand("touch {0}".format(fOutName2))
                else:
                    print("haddnanoaod output file2 {0} failed ({1}), retrying".format(fOutName2,returncode))
                    n_retries+=1
                    time.sleep(15)
            if(copy_result == False):
                print("haddnanoaod output file2 {0} failed completely, exiting the loop".format(fOutName2))
                os.remove(fOutName2)

            # haddnanoaod3
            copy_result = False
            n_retries = 0
            while n_retries < 5 and copy_result is False:
                returncode = 0
                if(atLeastOneFile[2] == True):
                    returncode = buildcommand(msgMerge3)
                if returncode == 0:
                    copy_result = True
                    if(isSkimData == 1):
                        try:
                            dftest = ROOT.RDataFrame("Events", fOutName3)
                            nevents = dftest.Count().GetValue()
                            del dftest
                        except Exception as e:
                            os.remove(fOutName3)
                            fOutName3 = "output_3l_%d_%d.txt" % (whichSample,i)
                            returntestcode = buildcommand("touch {0}".format(fOutName3))
                else:
                    print("haddnanoaod output file3 {0} failed ({1}), retrying".format(fOutName3,returncode))
                    n_retries+=1
                    time.sleep(15)
            if(copy_result == False):
                print("haddnanoaod output file3 {0} failed completely, exiting the loop".format(fOutName3))
                os.remove(fOutName3)

            if(copyFilesToFS == True):
                # copying output file1
                copycommand = "%s %s %s/%s" % (msgCPOutput,fOutName1,finalOutputDir1,fOutName1)
                if(isLocal == True and (not os.path.exists(finalOutputDir1))):
                    os.makedirs(finalOutputDir1)

                copy_result = False
                n_retries = 0
                while n_retries < 5 and copy_result is False:
                    returncode = buildcommand(copycommand)
                    if returncode == 0:
                        copy_result = True
                    else:
                        print("Copying output file1 {0} failed ({1}), retrying".format(fOutName1,returncode))
                        n_retries+=1
                        time.sleep(15)
                if(copy_result == False):
                    print("Copying output file1 {0} failed completely, exiting the loop".format(fOutName1))

                os.remove(fOutName1)

                # copying output file2
                copycommand = "%s %s %s/%s" % (msgCPOutput,fOutName2,finalOutputDir2,fOutName2)
                if(isLocal == True and (not os.path.exists(finalOutputDir2))):
                    os.makedirs(finalOutputDir2)

                copy_result = False
                n_retries = 0
                while n_retries < 5 and copy_result is False:
                    returncode = buildcommand(copycommand)
                    if returncode == 0:
                        copy_result = True
                    else:
                        print("Copying output file2 {0} failed ({1}), retrying".format(fOutName2,returncode))
                        n_retries+=1
                        time.sleep(15)
                if(copy_result == False):
                    print("Copying output file2 {0} failed completely, exiting the loop".format(fOutName2))

                os.remove(fOutName2)

                # copying output file3
                copycommand = "%s %s %s/%s" % (msgCPOutput,fOutName3,finalOutputDir3,fOutName3)
                if(isLocal == True and (not os.path.exists(finalOutputDir3))):
                    os.makedirs(finalOutputDir3)

                copy_result = False
                n_retries = 0
                while n_retries < 5 and copy_result is False:
                    returncode = buildcommand(copycommand)
                    if returncode == 0:
                        copy_result = True
                    else:
                        print("Copying output file3 {0} failed ({1}), retrying".format(fOutName3,returncode))
                        n_retries+=1
                        time.sleep(15)
                if(copy_result == False):
                    print("Copying output file3 {0} failed completely, exiting the loop".format(fOutName3))

                os.remove(fOutName3)

            # Delete used files
            print(msgRm)
            os.system(msgRm)

        except Exception as e:
            print("PROBLEM {0} / {1} / {2}".format(outputDir,i,e))

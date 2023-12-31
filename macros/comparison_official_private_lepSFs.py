import ROOT
import correctionlib
import os, sys, getopt, glob
from array import array

etaVal = array('d', [0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4])
ptVal = array('d', [10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,95.0,100.0])
yearVal = [20220, 20221]

if __name__ == "__main__":
    input = "data"

    valid = ['input=', 'help']
    usage  =  "Usage: ana.py --input=<{0}>".format(input)
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
        if opt == "--input":
            input = str(arg)

    histo_mu = [0 for x in range(len(yearVal))]
    histo_el = [0 for x in range(len(yearVal))]
    for ny in range(len(yearVal)):
        lepSFPath = "{0}/histoLepSFEtaPt_{1}.root".format(input,yearVal[ny])
        fLepSFFile = ROOT.TFile(lepSFPath)
        histoLepSFEtaPt_mu = fLepSFFile.Get("histoLepSFEtaPt_0_{0}".format(2))
        histoLepSFEtaPt_el = fLepSFFile.Get("histoLepSFEtaPt_1_{0}".format(3))
        histoLepSFEtaPt_mu.SetDirectory(0)
        histoLepSFEtaPt_el.SetDirectory(0)
        fLepSFFile.Close()

        muIDTag = "NUM_MediumID_DEN_TrackerMuons"
        muISOTag = "NUM_TightPFIso_DEN_MediumID"
        elTag = ""
        jsnFolder = ""
        if(yearVal[ny] == 20220):
            elTag = "2022Re-recoBCD"
            jsnFolder = "2022_Summer22"
        elif(yearVal[ny] == 20221):
            elTag = "2022Re-recoE+PromptFG"
            jsnFolder = "2022_Summer22EE"

        print("************** {0} **************".format(yearVal[ny]))

        evaluator_el = correctionlib._core.CorrectionSet.from_file("jsonpog-integration/POG/EGM/{0}/electron.json.gz".format(jsnFolder))
        evaluator_mu = correctionlib._core.CorrectionSet.from_file("jsonpog-integration/POG/MUO/{0}/muon_Z.json.gz".format(jsnFolder))

        histo_mu[ny] = ROOT.TH2D("histo_{0}_mu".format(yearVal[ny]), "histo_{0}_mu".format(yearVal[ny]), len(etaVal)-1, etaVal, len(ptVal)-1, ptVal)
        histo_el[ny] = ROOT.TH2D("histo_{0}_el".format(yearVal[ny]), "histo_{0}_el".format(yearVal[ny]), len(etaVal)-1, etaVal, len(ptVal)-1, ptVal)

        sfPri_mu = []
        sfPri_el = []
        sfOff_mu = []
        sfOff_el = []
        count = -1
        for eta in range(len(etaVal)-1):
            for pt in range(len(ptVal)-1):
                count = count + 1

                binX = histoLepSFEtaPt_mu.GetXaxis().FindFixBin(etaVal[eta]+0.001)
                binY = histoLepSFEtaPt_mu.GetYaxis().FindFixBin(ptVal[pt]+0.001)
                sfPri_mu.append(histoLepSFEtaPt_mu.GetBinContent(binX,binY))
                sfOff_mu.append(evaluator_mu[muIDTag].evaluate(etaVal[eta]+0.001,max(ptVal[pt]+0.001,15.001),"nominal")*evaluator_mu[muISOTag].evaluate(etaVal[eta]+0.001,max(ptVal[pt]+0.001,15.001),"nominal"))
                sfm = sfOff_mu[count]/sfPri_mu[count]
                histo_mu[ny].SetBinContent(eta+1,pt+1,sfm)

                binX = histoLepSFEtaPt_el.GetXaxis().FindFixBin(etaVal[eta]+0.001)
                binY = histoLepSFEtaPt_el.GetYaxis().FindFixBin(ptVal[pt]+0.001)
                sfPri_el.append(histoLepSFEtaPt_el.GetBinContent(binX,binY))
                sfOff_el.append(evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","wp80iso",etaVal[eta]+0.001,ptVal[pt]+0.001))
                sfe = sfOff_el[count]/sfPri_el[count]
                histo_el[ny].SetBinContent(eta+1,pt+1,sfe)

                print("SF({0:.1f}/{1:.0f}) {2:.3f} / {3:.3f} = {4:.3f}  |  {5:.3f} / {6:.3f} = {7:.3f}".format(etaVal[eta],ptVal[pt],sfOff_mu[count],sfPri_mu[count],sfOff_el[count],sfm,sfPri_el[count],sfe))


    fileLepEffCompName = "histoLepSFComparison.root"
    outFileLepEffComp = ROOT.TFile(fileLepEffCompName,"recreate")
    outFileLepEffComp.cd()
    for ny in range(len(yearVal)):
        histo_mu[ny].Write()    
        histo_el[ny].Write()    
    outFileLepEffComp.Close()

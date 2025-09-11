import ROOT
import correctionlib
import os, sys, getopt, glob
from array import array

xPtBins = array('d', [10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,95.0,100.0])
xEtaBins = array('d', [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2.0,2.1,2.2,2.3,2.4])
xMuPtBins = array('d', [10.0,15.0,20.0,25.0,30.0,40.0,50.0,60.0,120.0,200.0])
xMuEtaBins = array('d', [0.0,0.9,1.2,2.1,2.5])
#yearVal = [20220, 20221, 20230, 20231, 20240]
yearVal = [20240]

if __name__ == "__main__":
    input = "data/"
    binOption = 0
    debug = 0

    valid = ['input=', "binOption=", "debug=", 'help']
    usage  =  "Usage: ana.py --input=<{0}>\n".format(input)
    usage +=  "              --binOption=<{0}>\n".format(binOption)
    usage +=  "              --debug=<{0}>".format(debug)
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
        if opt == "--debug":
            debug = int(arg)
        if opt == "--binOption":
            binOption = int(arg)

    histo_mu = [0 for x in range(len(yearVal))]
    for ny in range(len(yearVal)):
        lepSFPath = "{0}histoLepSFEtaPt_{1}_correction.root".format(input,yearVal[ny])
        fLepSFFile = ROOT.TFile(lepSFPath)
        histoLepSFEtaPt_mu = fLepSFFile.Get("histoLepSFEtaPt_0_{0}".format(8)) # Muon_promptMVA > 0.7
        histoLepSFEtaPt_mu.SetDirectory(0)
        fLepSFFile.Close()

        muIDTag = "NUM_promptMVA_WP64ID_DEN_MediumID"
        jsnFolder = ""
        if(yearVal[ny] == 20220):
            jsnFolder = "2022_Summer22"
        elif(yearVal[ny] == 20221):
            jsnFolder = "2022_Summer22EE"
        elif(yearVal[ny] == 20230):
            jsnFolder = "2023_Summer23"
        elif(yearVal[ny] == 20231):
            jsnFolder = "2023_Summer23BPix"
        elif(yearVal[ny] == 20240):
            jsnFolder = "2024_Winter24"

        print("************** {0} **************".format(yearVal[ny]))

        evaluator_mu = correctionlib._core.CorrectionSet.from_file("jsonpog-integration/POG/MUO/{0}/muon_Z.json.gz".format(jsnFolder))

        phiVal = 0.5 # electrons

        for ltype in range(1):
            etaVal = xEtaBins
            ptVal = xPtBins
            if(binOption == 1 and ltype == 0):
                etaVal = xMuEtaBins
                ptVal = xMuPtBins

            print("ltype: {0} / etaBins: {1} / ptBins: {2} -> {3}".format(ltype,len(etaVal)-1,len(ptVal)-1,(len(etaVal)-1)*(len(ptVal)-1)))
            histo_mu[ny] = ROOT.TH2D("histo_{0}_mu".format(yearVal[ny]), "histo_{0}_mu".format(yearVal[ny]), len(etaVal)-1, etaVal, len(ptVal)-1, ptVal)

            for eta in range(len(etaVal)-1):
                for pt in range(len(ptVal)-1):

                    sfOff = 1.0
                    sfPri = 1.0
                    sf = 1.0
                    binX = histoLepSFEtaPt_mu.GetXaxis().FindFixBin(etaVal[eta]+0.001)
                    binY = histoLepSFEtaPt_mu.GetYaxis().FindFixBin(ptVal[pt]+0.001)
                    sfPri = histoLepSFEtaPt_mu.GetBinContent(binX,binY)
                    sfOff = evaluator_mu[muIDTag].evaluate(etaVal[eta]+0.001,max(ptVal[pt]+0.001,15.001),"nominal")
                    sf = sfOff/sfPri
                    histo_mu[ny].SetBinContent(eta+1,pt+1,sf)

                    if(debug == 1):
                        print("SF({0:1d}/{1:.1f}/{2:.0f}) {3:.3f} / {4:.3f} = {5:.3f}".format(ltype,etaVal[eta],ptVal[pt],sfOff,sfPri,sf))


    fileLepEffCompName = "histoMuonMVASFComparison.root"
    outFileLepEffComp = ROOT.TFile(fileLepEffCompName,"recreate")
    outFileLepEffComp.cd()
    for ny in range(len(yearVal)):
        histo_mu[ny].Write()    
    outFileLepEffComp.Close()

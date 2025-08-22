import ROOT
import correctionlib
import os, sys, getopt, glob
from array import array

xPtBins = array('d', [20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,95.0,100.0])
xEtaBins = array('d', [0.5,1.0,1.5])
yearVal = [20220, 20221, 20230, 20231, 20240]


if __name__ == "__main__":
    debug = 0

    valid = ["debug=", 'help']
    usage  =  "Usage: ana.py --debug=<{0}>".format(debug)
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
        if opt == "--debug":
            debug = int(arg)


    workingPoint = ["T", "M", "L"]

    histo_btv_hf = [[[0 for y in range(len(yearVal))] for x in range(len(xEtaBins))] for z in range(len(workingPoint))]
    histo_btv_lf = [[[0 for y in range(len(yearVal))] for x in range(len(xEtaBins))] for z in range(len(workingPoint))]

    for ny in range(len(yearVal)):
        jsnFolder = ""
        fileHFName = ""
        btaggerHFName = ""
        fileLFName = ""
        btaggerLFName = ""
        if(yearVal[ny] == 20220):
            jsnFolder = "2022_Summer22"
            fileHFName = "btagging.json.gz"
            btaggerHFName = "robustParticleTransformer_comb"
            fileLFName = "btagging.json.gz"
            btaggerLFName = "robustParticleTransformer_light"
        elif(yearVal[ny] == 20221):
            jsnFolder = "2022_Summer22EE"
            fileHFName = "btagging.json.gz"
            btaggerHFName = "robustParticleTransformer_comb"
            fileLFName = "btagging.json.gz"
            btaggerLFName = "robustParticleTransformer_light"
        elif(yearVal[ny] == 20230):
            jsnFolder = "2023_Summer23"
            fileHFName = "btagging.json.gz"
            btaggerHFName = "robustParticleTransformer_comb"
            fileLFName = "btagging.json.gz"
            btaggerLFName = "robustParticleTransformer_light"
        elif(yearVal[ny] == 20231):
            jsnFolder = "2023_Summer23BPix"
            fileHFName = "btagging.json.gz"
            btaggerHFName = "robustParticleTransformer_comb"
            fileLFName = "btagging.json.gz"
            btaggerLFName = "robustParticleTransformer_light"
        elif(yearVal[ny] == 20240):
            jsnFolder = "2024_Winter24"
            fileHFName = "btagging_preliminary.json.gz"
            btaggerHFName = "UParTAK4_kinfit"
            fileLFName = "btagging.json.gz"
            btaggerLFName = "robustParticleTransformer_light"

        print("************** {0} **************".format(yearVal[ny]))

        evaluator_btv_hf = correctionlib._core.CorrectionSet.from_file("jsonpog-integration/POG/BTV/{0}/{1}".format(jsnFolder,fileHFName))
        evaluator_btv_lf = correctionlib._core.CorrectionSet.from_file("jsonpog-integration/POG/BTV/{0}/{1}".format(jsnFolder,fileLFName))

        for eta in range(len(xEtaBins)):
            for wp in range(len(workingPoint)):
                histo_btv_hf[wp][eta][ny] = ROOT.TH1D("histo_btv_hf_{0}_{1}_{2}".format(workingPoint[wp],eta,yearVal[ny]), "histo_btv_hf_{0}_{1}_{2}".format(workingPoint[wp],eta,yearVal[ny]), len(xPtBins)-1, xPtBins)
                histo_btv_lf[wp][eta][ny] = ROOT.TH1D("histo_btv_lf_{0}_{1}_{2}".format(workingPoint[wp],eta,yearVal[ny]), "histo_btv_lf_{0}_{1}_{2}".format(workingPoint[wp],eta,yearVal[ny]), len(xPtBins)-1, xPtBins)

                syst = [0, 0]
                for pt in range(len(xPtBins)-1):
                    syst[0] = evaluator_btv_hf[btaggerHFName].evaluate("central" , workingPoint[wp], 5, xEtaBins[eta], xPtBins[pt]+0.001)
                    syst[1] = evaluator_btv_lf[btaggerLFName].evaluate("central" , workingPoint[wp], 0, xEtaBins[eta], xPtBins[pt]+0.001)
                    histo_btv_hf[wp][eta][ny].SetBinContent(pt+1,syst[0])
                    histo_btv_lf[wp][eta][ny].SetBinContent(pt+1,syst[1])
                    if(debug == 1):
                        print("SF({0}/{1:.1f}/{2:.0f}) ({3:.3f}/{4:.3f})".format(workingPoint[wp],xEtaBins[eta],xPtBins[pt],syst[0],syst[1]))

        theWorkingPoint = workingPoint[2]
        for npt in range(20):
            for neta in range(25):
                theEta = float(neta)/10.
                thePt = float(npt)*10+20
                val = evaluator_btv_hf[btaggerHFName].evaluate("central", theWorkingPoint, 5, theEta, thePt)
                if(debug == 2):
                    print("SF({0}/{1:.1f}/{2:.0f}) {3:.5f}".format(theWorkingPoint,theEta,thePt,val))

    fileBTVSFsName = "histoBTVSFs.root"
    outFileBTVSFs = ROOT.TFile(fileBTVSFsName,"recreate")
    outFileBTVSFs.cd()
    for ny in range(len(yearVal)):
        for eta in range(len(xEtaBins)):
            for wp in range(len(workingPoint)):
                histo_btv_hf[wp][eta][ny].Write()
                histo_btv_lf[wp][eta][ny].Write()
    outFileBTVSFs.Close()

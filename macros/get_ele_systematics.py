import ROOT
import correctionlib
import os, sys, getopt, glob
from array import array

xPtBins = array('d', [10.0,15.0,20.0,25.0,30.0,35.0,40.0,45.0,50.0,55.0,60.0,65.0,70.0,75.0,80.0,85.0,90.0,95.0,100.0])
xEtaBins = array('d', [-2.4,-2.2,-2.0,-1.8,-1.6,-1.4,-1.2,-1.0,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8,2.0,2.2,2.4])
yearVal = [20220, 20221, 20230, 20231]


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

    histo_el0 = [0 for x in range(len(yearVal))]
    histo_el1 = [0 for x in range(len(yearVal))]
    histo_el2 = [0 for x in range(len(yearVal))]
    for ny in range(len(yearVal)):
        elTag = ""
        jsnFolder = ""
        if(yearVal[ny] == 20220):
            elTag = "2022Re-recoBCD"
            jsnFolder = "2022_Summer22"
        elif(yearVal[ny] == 20221):
            elTag = "2022Re-recoE+PromptFG"
            jsnFolder = "2022_Summer22EE"
        elif(yearVal[ny] == 20230):
            elTag = "2023PromptC"
            jsnFolder = "2023_Summer23"
        elif(yearVal[ny] == 20231):
            elTag = "2023PromptD"
            jsnFolder = "2023_Summer23BPix"

        print("************** {0} **************".format(yearVal[ny]))

        evaluator_el = correctionlib._core.CorrectionSet.from_file("jsonpog-integration/POG/EGM/{0}/electron.json.gz".format(jsnFolder))

        etaVal = xEtaBins
        ptVal = xPtBins
        print("etaBins: {0} / ptBins: {1} -> {2}".format(len(etaVal)-1,len(ptVal)-1,(len(etaVal)-1)*(len(ptVal)-1)))
        histo_el0[ny] = ROOT.TH2D("histo_{0}_el0".format(yearVal[ny]), "histo_{0}_el0".format(yearVal[ny]), len(etaVal)-1, etaVal, len(ptVal)-1, ptVal)
        histo_el1[ny] = ROOT.TH2D("histo_{0}_el1".format(yearVal[ny]), "histo_{0}_el1".format(yearVal[ny]), len(etaVal)-1, etaVal, len(ptVal)-1, ptVal)
        histo_el2[ny] = ROOT.TH2D("histo_{0}_el2".format(yearVal[ny]), "histo_{0}_el2".format(yearVal[ny]), len(etaVal)-1, etaVal, len(ptVal)-1, ptVal)

        thePhi = 0.5 # electrons

        for eta in range(len(etaVal)-1):
            for pt in range(len(ptVal)-1):

                syste0 = 0
                syste1 = 0
                syste2 = 0
                if(yearVal[ny] // 10 <= 2022):
                    syste0 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","wp80iso",etaVal[eta]+0.001,ptVal[pt]+0.001)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","wp80iso",etaVal[eta]+0.001,ptVal[pt]+0.001)

                    syste1 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","Medium" ,etaVal[eta]+0.001,ptVal[pt]+0.001)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","Medium" ,etaVal[eta]+0.001,ptVal[pt]+0.001)

                    syste2 = 0
                    if(ptVal[pt]+0.001 < 20):
                        syste2 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","RecoBelow20",etaVal[eta]+0.001,ptVal[pt]+0.001)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","RecoBelow20",etaVal[eta]+0.001,ptVal[pt]+0.001)
                    elif(ptVal[pt]+0.001 < 75):
                        syste2 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","Reco20to75" ,etaVal[eta]+0.001,ptVal[pt]+0.001)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","Reco20to75" ,etaVal[eta]+0.001,ptVal[pt]+0.001)
                    else:
                        syste2 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","RecoAbove75",etaVal[eta]+0.001,ptVal[pt]+0.001)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","RecoAbove75",etaVal[eta]+0.001,ptVal[pt]+0.001)
                else:
                    syste0 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","wp80iso",etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","wp80iso",etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)

                    syste1 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","Medium" ,etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","Medium" ,etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)

                    syste2 = 0
                    if(ptVal[pt]+0.001 < 20):
                        syste2 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","RecoBelow20",etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","RecoBelow20",etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)
                    elif(ptVal[pt]+0.001 < 75):
                        syste2 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","Reco20to75" ,etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","Reco20to75" ,etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)
                    else:
                        syste2 = evaluator_el["Electron-ID-SF"].evaluate(elTag,"sfup","RecoAbove75",etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)-evaluator_el["Electron-ID-SF"].evaluate(elTag,"sf","RecoAbove75",etaVal[eta]+0.001,ptVal[pt]+0.001,thePhi)

                histo_el0[ny].SetBinContent(eta+1,pt+1,syste0)
                histo_el1[ny].SetBinContent(eta+1,pt+1,syste1)
                histo_el2[ny].SetBinContent(eta+1,pt+1,syste2)

                if(debug == 1):
                    print("SF({0:.1f}/{1:.0f}) {2:.3f} / {3:.3f} / {4:.3f}".format(etaVal[eta],ptVal[pt],syste0,syste1,syste2))


    fileEleEffSystName = "histoEleSFSystematics.root"
    outFileEleEffSyst = ROOT.TFile(fileEleEffSystName,"recreate")
    outFileEleEffSyst.cd()
    for ny in range(len(yearVal)):
        histo_el0[ny].Write()    
        histo_el1[ny].Write()    
        histo_el2[ny].Write()    
    outFileEleEffSyst.Close()

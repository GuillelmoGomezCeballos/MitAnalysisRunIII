import ROOT
from ROOT import TFile, TH1D, TH2D, TCanvas
import os, sys, getopt, glob, time
from array import array
import json
from utilsCategory import plotCategory

xPtBins = array('d', [10.0, 15.0, 20.0, 25.0, 30.0, 40.0])
xEtaBins = array('d', [0.0, 0.5, 1.0, 1.5, 2.0, 2.5])
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

if __name__ == "__main__":
    path = "fillhisto_fakeAnalysis1001"
    year = 2022
    inputDir = "anaZ"
    anaType = 0
    format = "pdf"
    isPseudoData = 0

    doSavePtEtaHist = False

    valid = ['path=', "year=", 'inputDir=', 'anaType=', 'isPseudoData=', 'format=', 'help']
    usage  =  "Usage: ana.py --path=<{0}>\n".format(path)
    usage +=  "              --year=<{0}>\n".format(year)
    usage +=  "              --inputDir=<{0}>\n".format(inputDir)
    usage +=  "              --anaType=<{0}>\n".format(anaType)
    usage +=  "              --isPseudoData=<{0}>\n".format(isPseudoData)
    usage +=  "              --format=<{0}>".format(format)
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
        if opt == "--path":
            path = str(arg)
        if opt == "--year":
            year = int(arg)
        if opt == "--inputDir":
            inputDir = str(arg)
        if opt == "--anaType":
            anaType = int(arg)
        if opt == "--isPseudoData":
            isPseudoData = int(arg)
        if opt == "--format":
            format = str(arg)

    if(path == "fillhisto_fakeAnalysis1001"):
        isPseudoData = 0
    elif(path == "fillhisto_fakeAnalysis1002"):
        isPseudoData = 1
    elif(path == "fillhisto_fakeAnalysis1003"):
        isPseudoData = 1
    print("isPseudoData: {0}".format(isPseudoData))

    startHisto = [0, 0]
    # no jet requirements
    if  (anaType%100 == 0):
        startHisto[0] = 0
        startHisto[1] = 0
    # njets30 > 0
    elif(anaType%100 == 1):
        startHisto[0] = 20
        startHisto[1] = 20
    # nbjets20 > 0
    elif(anaType%100 == 2):
        startHisto[0] = 40
        startHisto[1] = 40
    # nbjets50 > 0
    elif(anaType%100 == 3):
        startHisto[0] = 60
        startHisto[1] = 60
    else:
        print("Problem with anaType")
        sys.exit(1)

    if(anaType >= 100):
        startHisto[0] = startHisto[0] + 100
        startHisto[1] = startHisto[1] + 100

    nCat = plotCategory("kPlotCategories")
    dataCat = plotCategory("kPlotData")
    if(isPseudoData == 1):
        dataCat = plotCategory("kPlotNonPrompt")

    prescale = [[1.0 for y in range(len(xPtBins)-1)] for x in range(2)]
    print(prescale)

    #fileWLName = [0 for x in range(2)]
    #fileWLName[0] = "{0}/{1}_{2}_40.root".format(inputDir,path,year)
    #fileWLName[1] = "{0}/{1}_{2}_41.root".format(inputDir,path,year)
    #
    #myWLfile = [0 for x in range(2)]
    #for nf in range(2):
    #    myWLfile[nf] = TFile(fileWLName[nf])
    #    histoDA = myWLfile[nf].Get("histo{0}".format(dataCat))
    #    histoBG = myWLfile[nf].Get("histo{0}".format(plotCategory("kPlotSignal3")))
    #    for nc in range(nCat):
    #        if(nc == dataCat or nc == plotCategory("kPlotSignal3")): continue
    #        histoBG.Add(myWLfile[nf].Get("histo{0}".format(nc)))
    #
    #    print("Channel({0}) = {1}/{2}={3}".format(nf,histoDA.GetSumOfWeights(),histoBG.GetSumOfWeights(),histoDA.GetSumOfWeights()/histoBG.GetSumOfWeights()))
    #    for i in range(histoDA.GetNbinsX()):
    #        prescale[nf][i] = histoDA.GetBinContent(i+1)/histoBG.GetBinContent(i+1)
    #    myWLfile[nf].Close()
    #
    print("Prescales: ",prescale)

    numberOfSel = 9
    histoFakeEffSelEtaPt = [[0 for y in range(numberOfSel)] for x in range(2)]
    histoFakeEffSelPt    = [[[0 for z in range(len(xEtaBins)-1)] for y in range(numberOfSel)] for x in range(2)]
    histoFakeEffSelEta   = [[[0 for z in range(len(xPtBins)-1)] for y in range(numberOfSel)] for x in range(2)]

    fileTight = [[0 for y in range(numberOfSel)] for x in range(2)]

    fileLoose = [TFile("{0}/{1}_{2}_{3}_2d.root".format(inputDir,path,year,startHisto[0])), TFile("{0}/{1}_{2}_{3}_2d.root".format(inputDir,path,year,startHisto[1]+1))]
    for thePlot in range(2):
        for nsel in range(numberOfSel):
            fileTight[thePlot][nsel] = TFile("{0}/{1}_{2}_{3}_2d.root".format(inputDir,path,year,2+thePlot+nsel*2+startHisto[thePlot]))

    for thePlot in range(2):
        for j in range(numberOfSel):
            histoFakeEffSelEtaPt[thePlot][j] = TH2D("histoFakeEffSelEtaPt_{0}_{1}_{2}_anaType{3}".format(thePlot,j,path.split("fillhisto_")[1],anaType), "histoFakeEffSelEtaPt_{0}_{1}".format(thePlot,j), len(xEtaBins)-1, xEtaBins, len(xPtBins)-1, xPtBins)
            for neta in range(len(xEtaBins)-1):
                histoFakeEffSelPt[thePlot][j][neta] = TH1D("histoFakeEffSelPt_{0}_{1}_{2}_{3}_anaType{4}".format(thePlot,j,neta,path.split("fillhisto_")[1],anaType), "histoFakeEffSelPt_{0}_{1}_{2}".format(thePlot,j,neta), len(xPtBins)-1, xPtBins)
            for npt in range(len(xPtBins)-1):
                histoFakeEffSelEta[thePlot][j][npt] = TH1D("histoFakeEffSelEta_{0}_{1}_{2}_{3}_anaType{4}".format(thePlot,j,npt,path.split("fillhisto_")[1],anaType), "histoFakeEffSelEta_{0}_{1}_{2}".format(thePlot,j,npt), len(xEtaBins)-1, xEtaBins)

    fileFakeRateName = "histoFakeEtaPt_{0}_{1}_anaType{2}.root".format(path.split("fillhisto_")[1],year,anaType)
    outFileFakeRate = TFile(fileFakeRateName,"recreate")
    outFileFakeRate.cd()
    for thePlot in range(2):
        for nsel in range(numberOfSel):
            histoFakeDenDA = (fileLoose[thePlot].Get("histo2d{0}".format(dataCat))).Clone()
            histoFakeDenBG = (fileLoose[thePlot].Get("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()
            histoFakeNumDA = (fileTight[thePlot][nsel].Get("histo2d{0}".format(dataCat))).Clone()
            histoFakeNumBG = (fileTight[thePlot][nsel].Get("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()
            for nc in range(nCat):
                if(nc == dataCat or nc == plotCategory("kPlotSignal3")): continue
                histoFakeDenBG.Add(fileLoose[thePlot].Get("histo2d{0}".format(nc)))
                histoFakeNumBG.Add(fileTight[thePlot][nsel].Get("histo2d{0}".format(nc)))

            print("Channel({0},{1}) = ({2}-{3})/({4}-{5}) = {6}".format(thePlot,nsel,
                    histoFakeNumDA.GetSumOfWeights(),histoFakeNumBG.GetSumOfWeights() , histoFakeDenDA.GetSumOfWeights(),histoFakeDenBG.GetSumOfWeights(),
                   (histoFakeNumDA.GetSumOfWeights()-histoFakeNumBG.GetSumOfWeights())/(histoFakeDenDA.GetSumOfWeights()-histoFakeDenBG.GetSumOfWeights())))

            for i in range(histoFakeDenDA.GetNbinsX()):
                for j in range(histoFakeDenDA.GetNbinsY()):
                    den = histoFakeDenDA.GetBinContent(i+1,j+1) - histoFakeDenBG.GetBinContent(i+1,j+1)*prescale[thePlot][j]
                    num = histoFakeNumDA.GetBinContent(i+1,j+1) - histoFakeNumBG.GetBinContent(i+1,j+1)*prescale[thePlot][j]
                    eff = 1.0
                    unc = 0.0
                    if(den > 0 and num > 0 and num <= den):
                        eff = num / den
                        unc = pow(eff*(1-eff)/den,0.5)

                    elif(den > 0):
                        eff = 0.0
                        unc = min(pow(1.0/den,0.5),0.999)

                    histoFakeEffSelEtaPt[thePlot][nsel].SetBinContent(i+1,j+1,eff)
                    histoFakeEffSelEtaPt[thePlot][nsel].SetBinError  (i+1,j+1,unc)
                    print("({0},{1}): ({2:8.1f} - {3:8.1f}) / ({4:8.1f} - {5:8.1f}) = {6:8.1f} / {7:8.1f} = {8:0.3f} +/- {9:0.3f}".format(i+1,j+1,
                        histoFakeNumDA.GetBinContent(i+1,j+1),histoFakeNumBG.GetBinContent(i+1,j+1)*prescale[thePlot][j],
                        histoFakeDenDA.GetBinContent(i+1,j+1),histoFakeDenBG.GetBinContent(i+1,j+1)*prescale[thePlot][j],
                        num,den,eff,unc))
                    histoFakeEffSelPt[thePlot][nsel][i].SetBinContent(j+1,eff)
                    histoFakeEffSelPt[thePlot][nsel][i].SetBinError  (j+1,unc)
                    histoFakeEffSelEta[thePlot][nsel][j].SetBinContent(i+1,eff)
                    histoFakeEffSelEta[thePlot][nsel][j].SetBinError  (i+1,unc)

            histoFakeEffSelEtaPt[thePlot][nsel].Write()
            histoFakeEffSelEtaPt[thePlot][nsel].SetDirectory(0)
            if(doSavePtEtaHist == True):
              for neta in range(len(xEtaBins)-1):
                  histoFakeEffSelPt[thePlot][nsel][neta].Write()
                  histoFakeEffSelPt[thePlot][nsel][neta].SetDirectory(0)
              for npt in range(len(xEtaBins)-1):
                  histoFakeEffSelEta[thePlot][nsel][npt].Write()
                  histoFakeEffSelEta[thePlot][nsel][npt].SetDirectory(0)
    outFileFakeRate.Close()

    canvasEta = [0 for y in range(numberOfSel)]
    canvasPt = [0 for y in range(numberOfSel)]

    for nsel in range(numberOfSel):
        canvasPt[nsel] = TCanvas("canvasPt{0}".format(nsel), "canvasPt{0}".format(nsel), 10, 10, 500, 500)
        canvasPt[nsel].Divide(2,len(xPtBins)-1)
        for thePlot in range(2):
            for npt in range(len(xPtBins)-1):
                canvasPt[nsel].cd(thePlot+2*npt+1)
                #print(histoFakeEffSelPt[thePlot][nsel][npt].GetSumOfWeights())
                histoFakeEffSelPt[thePlot][nsel][npt].DrawCopy()
        canvasPt[nsel].Draw()
        canvasPt[nsel].SaveAs("histoFakePt_{0}_{1}_anaType{2}_nsel{3}.{4}".format(path.split("fillhisto_")[1],year,anaType,nsel,format))

        canvasEta[nsel] = TCanvas("canvasEta{0}".format(nsel), "canvasEta{0}".format(nsel), 10, 10, 500, 500)
        canvasEta[nsel].Divide(2,len(xEtaBins)-1)
        for thePlot in range(2):
            for neta in range(len(xEtaBins)-1):
                canvasEta[nsel].cd(thePlot+2*neta+1)
                #print(histoFakeEffSelEta[thePlot][nsel][neta].GetSumOfWeights())
                histoFakeEffSelEta[thePlot][nsel][neta].DrawCopy()
                canvasEta[nsel].Update()
        canvasEta[nsel].Draw()
        canvasEta[nsel].SaveAs("histoFakeEta_{0}_{1}_anaType{2}_nsel{3}.{4}".format(path.split("fillhisto_")[1],year,anaType,nsel,format))

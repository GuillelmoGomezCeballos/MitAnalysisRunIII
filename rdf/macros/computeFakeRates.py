import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
from array import array
from utilsAna import plotCategory

xEtabins = array('d', [0.0, 1.0, 1.5, 2.0, 2.5])
xPtbins = array('d', [10.0, 15.0, 20.0, 25.0, 30.0, 35.0])

if __name__ == "__main__":
    path = "fillhistoFakeAna1001"
    year = 2018
    output = "anaZ"

    valid = ['path=', "year=", 'output=', 'help']
    usage  =  "Usage: ana.py --path=<{0}>\n".format(path)
    usage +=  "              --year=<{0}>\n".format(year)
    usage +=  "              --output=<{0}>".format(output)
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
        if opt == "--output":
            output = str(arg)

    nCat = plotCategory("kPlotCategories")

    prescale = [[0 for x in range(len(xPtbins)-1)] for y in range(2)]
    print(prescale)

    fileWLName = [0 for x in range(2)]
    fileWLName[0] = "{0}/{1}_{2}_40.root".format(output,path,year)
    fileWLName[1] = "{0}/{1}_{2}_41.root".format(output,path,year)

    myWLfile = [0 for x in range(2)]
    for nf in range(2):
        myWLfile[nf] = TFile(fileWLName[nf])
        histoDA = myWLfile[nf].Get("histo{0}".format(plotCategory("kPlotData")))
        histoBG = myWLfile[nf].Get("histo{0}".format(plotCategory("kPlotSignal3")))
        for nc in range(nCat):
            if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotSignal3")): continue
            histoBG.Add(myWLfile[nf].Get("histo{0}".format(nc)))

        print("Channel({0}) = {1}/{2}={3}".format(nf,histoDA.GetSumOfWeights(),histoBG.GetSumOfWeights(),histoDA.GetSumOfWeights()/histoBG.GetSumOfWeights()))
        for i in range(histoDA.GetNbinsX()):
            prescale[nf][i] = histoDA.GetBinContent(i+1)/histoBG.GetBinContent(i+1)
        myWLfile[nf].Close()

    print("Prescales: ",prescale)

    fileLoose = [TFile("{0}/{1}_{2}_0_2d.root".format(output,path,year)),
                 TFile("{0}/{1}_{2}_1_2d.root".format(output,path,year))]
    fileTight = [TFile("{0}/{1}_{2}_2_2d.root".format(output,path,year)),
                 TFile("{0}/{1}_{2}_3_2d.root".format(output,path,year))]

    histoFakeEffSelEtaPt = [
        TH2D("histoFakeEffSelEtaPt_{0}".format(0), "histoFakeEffSelEtaPt_{0}".format(0), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins),
        TH2D("histoFakeEffSelEtaPt_{0}".format(1), "histoFakeEffSelEtaPt_{0}".format(1), len(xEtabins)-1, xEtabins, len(xPtbins)-1, xPtbins)]

    fileFakeRateName = "histoFakeEtaPt_{0}.root".format(year)
    outFileFakeRate = TFile(fileFakeRateName,"recreate")
    outFileFakeRate.cd()
    for thePlot in range(2):
        histoFakeDenDA = fileLoose[thePlot].Get("histo2d{0}".format(plotCategory("kPlotData")))
        histoFakeDenBG = fileLoose[thePlot].Get("histo2d{0}".format(plotCategory("kPlotSignal3")))
        histoFakeNumDA = fileTight[thePlot].Get("histo2d{0}".format(plotCategory("kPlotData")))
        histoFakeNumBG = fileTight[thePlot].Get("histo2d{0}".format(plotCategory("kPlotSignal3")))
        for nc in range(nCat):
            if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotSignal3")): continue
            histoFakeDenBG.Add(fileLoose[thePlot].Get("histo2d{0}".format(nc)))
            histoFakeNumBG.Add(fileTight[thePlot].Get("histo2d{0}".format(nc)))

        print("Channel({0}) = ({1}-{2})/({3}-{4})".format(thePlot,histoFakeNumDA.GetSumOfWeights(),histoFakeNumBG.GetSumOfWeights(),histoFakeDenDA.GetSumOfWeights(),histoFakeDenBG.GetSumOfWeights()))

        for i in range(histoFakeDenDA.GetNbinsX()):
            for j in range(histoFakeDenDA.GetNbinsY()):
                den = histoFakeDenDA.GetBinContent(i+1,j+1) - histoFakeDenBG.GetBinContent(i+1,j+1)*prescale[thePlot][j]
                num = histoFakeNumDA.GetBinContent(i+1,j+1) - histoFakeNumBG.GetBinContent(i+1,j+1)*prescale[thePlot][j]
                eff = 1.0
                unc = 0.0
                if(den > 0 and num > 0):
                    eff = num / den
                    unc = pow(eff*(1-eff)/den,0.5)

                elif(den > 0):
                    eff = 0.0
                    unc = min(pow(1.0/den,0.5),0.999)

                histoFakeEffSelEtaPt[thePlot].SetBinContent(i+1,j+1,eff);
                histoFakeEffSelEtaPt[thePlot].SetBinError  (i+1,j+1,unc);
                print("({0},{1}): ({2:8.1f} - {3:8.1f}) / ({4:8.1f} - {5:8.1f}) = {6:8.1f} / {7:8.1f} = {8:0.3f} +/- {9:0.3f}".format(i+1,j+1,
                    histoFakeNumDA.GetBinContent(i+1,j+1),histoFakeNumBG.GetBinContent(i+1,j+1)*prescale[thePlot][j],
                    histoFakeDenDA.GetBinContent(i+1,j+1),histoFakeDenBG.GetBinContent(i+1,j+1)*prescale[thePlot][j],
                    num,den,eff,unc))

        histoFakeEffSelEtaPt[thePlot].Write()

    outFileFakeRate.Close()

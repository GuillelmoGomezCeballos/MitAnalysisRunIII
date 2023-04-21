import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
from array import array
from utilsCategory import plotCategory

if __name__ == "__main__":
    path = "fillhisto_metAnalysis1001"
    year = 2022
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

    numberOfLep = 6
    numberOfSel = 5
    histoTriggerSFEtaPt = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoLepDenDA = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoLepDenDY = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoLepNumDA = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoLepNumDY = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]

    for nlep in range(numberOfLep):
        for nsel in range(numberOfSel):
            fileTriggerDEN = TFile("{0}/{1}_{2}_{3}_2d.root".format(output,path,year,  nlep+12*nsel))
            fileTriggerDEN.cd()

            histoTriggerSFEtaPt[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()

            histoLepDenDA[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepDenDY[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
            for nc in range(nCat):
                if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY") or nc == plotCategory("kPlotSignal3")): continue
                histoLepDenDY[nlep][nsel].Add(ROOT.gROOT.FindObject("histo2d{0}".format(nc)),1.0)

            histoTriggerSFEtaPt[nlep][nsel].SetDirectory(0)
            histoLepDenDA[nlep][nsel].SetDirectory(0)
            histoLepDenDY[nlep][nsel].SetDirectory(0)

            fileTriggerDEN.Close()

            fileTriggerNUM = TFile("{0}/{1}_{2}_{3}_2d.root".format(output,path,year,6+nlep+12*nsel))
            fileTriggerNUM.cd()

            histoLepNumDA[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepNumDY[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
            for nc in range(nCat):
                if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY")): continue
                histoLepNumDY[nlep][nsel].Add(ROOT.gROOT.FindObject("histo2d{0}".format(nc)),1.0)

            histoLepNumDA[nlep][nsel].SetDirectory(0)
            histoLepNumDY[nlep][nsel].SetDirectory(0)

            fileTriggerNUM.Close()

            print("({0},{1}) = {2}/{3} = {4}".format(nlep,nsel,
                  histoLepNumDA[nlep][nsel].GetSumOfWeights()/histoLepDenDA[nlep][nsel].GetSumOfWeights(),
                  histoLepNumDY[nlep][nsel].GetSumOfWeights()/histoLepDenDY[nlep][nsel].GetSumOfWeights(),
                 (histoLepNumDA[nlep][nsel].GetSumOfWeights()/histoLepDenDA[nlep][nsel].GetSumOfWeights())/
                 (histoLepNumDY[nlep][nsel].GetSumOfWeights()/histoLepDenDY[nlep][nsel].GetSumOfWeights())
                 ))

            for i in range(histoLepDenDA[nlep][nsel].GetNbinsX()):
                for j in range(histoLepDenDA[nlep][nsel].GetNbinsY()):
                    den0 = histoLepDenDA[nlep][nsel].GetBinContent(i+1,j+1)
                    num0 = histoLepNumDA[nlep][nsel].GetBinContent(i+1,j+1)
                    eff0 = 1.0
                    unc0 = 0.0
                    if(den0 > 0 and num0 > 0 and num0 <= den0):
                        eff0 = num0 / den0
                        unc0 = pow(eff0*(1-eff0)/den0,0.5)

                    elif(den0 > 0):
                        eff0 = 0.0
                        unc0 = min(pow(1.0/den0,0.5),0.999)

                    den1 = histoLepDenDY[nlep][nsel].GetBinContent(i+1,j+1)
                    num1 = histoLepNumDY[nlep][nsel].GetBinContent(i+1,j+1)
                    eff1 = 1.0
                    unc1 = 0.0
                    if(den1 > 0 and num1 > 0 and num1 <= den1):
                        eff1 = num1 / den1
                        unc1 = pow(eff1*(1-eff1)/den1,0.5)

                    elif(den1 > 0):
                        eff1 = 0.0
                        unc1 = min(pow(1.0/den1,0.5),0.999)

                    sf = 1.
                    sfe = 0.
                    if(eff0 > 0 and eff1 > 0):
                        sf = eff0/eff1
                        sfe = sf*pow(pow(unc0/eff0,2)+pow(unc1/eff1,2),0.5)

                    histoTriggerSFEtaPt[nlep][nsel].SetBinContent(i+1,j+1,sf)
                    histoTriggerSFEtaPt[nlep][nsel].SetBinError  (i+1,j+1,sfe)

                    print("({0:2d},{1:2d}): ({2:.3f} +/- {3:.3f}) / ({4:.3f} - {5:.3f}) = {6:.3f} / {7:.3f}".format(i+1,j+1,
                          eff0,unc0,eff1,unc1,sf,sfe))

    fileTriggerEffName = "histoTriggerSFEtaPt_{0}.root".format(year)
    outfileTriggerEff = TFile(fileTriggerEffName,"recreate")
    outfileTriggerEff.cd()
    for nlep in range(numberOfLep):
        for nsel in range(numberOfSel):
            histoTriggerSFEtaPt[nlep][nsel].SetNameTitle("histoTriggerSFEtaPt_{0}_{1}".format(nlep,nsel),      "histoTriggerSFEtaPt_{0}_{1}".format(nlep,nsel))
            histoTriggerSFEtaPt[nlep][nsel].Write()
    outfileTriggerEff.Close()

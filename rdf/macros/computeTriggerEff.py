import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
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
    histoTriggerLooseSFEtaPt = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoTriggerLooseDAEtaPt = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoTriggerLooseMCEtaPt = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoTriggerTightSFEtaPt = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoTriggerTightDAEtaPt = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoTriggerTightMCEtaPt = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoLepDenDA = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoLepDenDY = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoLepNumDA = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]
    histoLepNumDY = [[0 for y in range(numberOfSel)] for x in range(numberOfLep)]

    for nlep in range(numberOfLep):
        for nsel in range(numberOfSel):
            fileTriggerDEN = TFile("{0}/{1}_{2}_{3}_2d.root".format(output,path,year,  nlep+12*nsel))
            fileTriggerDEN.cd()

            histoTriggerLooseSFEtaPt[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()
            histoTriggerLooseDAEtaPt[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()
            histoTriggerLooseMCEtaPt[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()

            histoLepDenDA[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepDenDY[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
            for nc in range(nCat):
                if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY") or nc == plotCategory("kPlotSignal3")): continue
                histoLepDenDY[nlep][nsel].Add(ROOT.gROOT.FindObject("histo2d{0}".format(nc)),1.0)

            histoTriggerLooseSFEtaPt[nlep][nsel].SetDirectory(0)
            histoTriggerLooseDAEtaPt[nlep][nsel].SetDirectory(0)
            histoTriggerLooseMCEtaPt[nlep][nsel].SetDirectory(0)
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

            if(histoLepDenDA[nlep][nsel].GetSumOfWeights() > 0 and histoLepDenDY[nlep][nsel].GetSumOfWeights() > 0):
                print("AverageLoose({0},{1}) = {2} / {3} = {4}".format(nlep,nsel,
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

                    sf = 0.
                    sfe = 0.
                    if(eff0 > 0 and eff1 > 0):
                        sf = eff0/eff1
                        sfe = sf*pow(pow(unc0/eff0,2)+pow(unc1/eff1,2),0.5)
                    elif(histoLepDenDY[nlep][nsel].GetXaxis().GetBinCenter(i+1) >= histoLepDenDY[nlep][nsel].GetXaxis().GetBinCenter(j+1)):
                        sf = 1.0

                    histoTriggerLooseSFEtaPt[nlep][nsel].SetBinContent(i+1,j+1,sf)
                    histoTriggerLooseSFEtaPt[nlep][nsel].SetBinError  (i+1,j+1,sfe)
                    histoTriggerLooseDAEtaPt[nlep][nsel].SetBinContent(i+1,j+1,eff0)
                    histoTriggerLooseDAEtaPt[nlep][nsel].SetBinError  (i+1,j+1,unc0)
                    histoTriggerLooseMCEtaPt[nlep][nsel].SetBinContent(i+1,j+1,eff1)
                    histoTriggerLooseMCEtaPt[nlep][nsel].SetBinError  (i+1,j+1,unc1)

                    print("BinLoose({0:2d},{1:2d}): ( {2:.3f} +/- {3:.3f} ) / ( {4:.3f} - {5:.3f} ) = {6:.3f} / {7:.3f}".format(i+1,j+1,
                          eff0,unc0,eff1,unc1,sf,sfe))


    for nlep in range(numberOfLep):
        for nsel in range(numberOfSel):
            fileTriggerDEN = TFile("{0}/{1}_{2}_{3}_2d.root".format(output,path,year,  nlep+12*nsel+100))
            fileTriggerDEN.cd()

            histoTriggerTightSFEtaPt[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()
            histoTriggerTightDAEtaPt[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()
            histoTriggerTightMCEtaPt[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotSignal3")))).Clone()

            histoLepDenDA[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepDenDY[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
            for nc in range(nCat):
                if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY") or nc == plotCategory("kPlotSignal3")): continue
                histoLepDenDY[nlep][nsel].Add(ROOT.gROOT.FindObject("histo2d{0}".format(nc)),1.0)

            histoTriggerTightSFEtaPt[nlep][nsel].SetDirectory(0)
            histoTriggerTightDAEtaPt[nlep][nsel].SetDirectory(0)
            histoTriggerTightMCEtaPt[nlep][nsel].SetDirectory(0)
            histoLepDenDA[nlep][nsel].SetDirectory(0)
            histoLepDenDY[nlep][nsel].SetDirectory(0)

            fileTriggerDEN.Close()

            fileTriggerNUM = TFile("{0}/{1}_{2}_{3}_2d.root".format(output,path,year,6+nlep+12*nsel+100))
            fileTriggerNUM.cd()

            histoLepNumDA[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepNumDY[nlep][nsel] = (ROOT.gROOT.FindObject("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
            for nc in range(nCat):
                if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY")): continue
                histoLepNumDY[nlep][nsel].Add(ROOT.gROOT.FindObject("histo2d{0}".format(nc)),1.0)

            histoLepNumDA[nlep][nsel].SetDirectory(0)
            histoLepNumDY[nlep][nsel].SetDirectory(0)

            fileTriggerNUM.Close()

            if(histoLepDenDA[nlep][nsel].GetSumOfWeights() > 0 and histoLepDenDY[nlep][nsel].GetSumOfWeights() > 0):
                print("AverageTight({0},{1}) = {2} / {3} = {4}".format(nlep,nsel,
                      histoLepNumDA[nlep][nsel].GetSumOfWeights()/histoLepDenDA[nlep][nsel].GetSumOfWeights(),
                      histoLepNumDY[nlep][nsel].GetSumOfWeights()/histoLepDenDY[nlep][nsel].GetSumOfWeights(),
                     (histoLepNumDA[nlep][nsel].GetSumOfWeights()/histoLepDenDA[nlep][nsel].GetSumOfWeights())/
                     (histoLepNumDY[nlep][nsel].GetSumOfWeights()/histoLepDenDY[nlep][nsel].GetSumOfWeights())
                     ))

            for i in range(histoLepDenDA[nlep][nsel].GetNbinsX()):
                for j in range(histoLepDenDA[nlep][nsel].GetNbinsY()):
                    den0 = histoLepDenDA[nlep][nsel].GetBinContent(i+1,j+1)
                    num0 = histoLepNumDA[nlep][nsel].GetBinContent(i+1,j+1)
                    eff0 = 0.0
                    unc0 = 0.0
                    if(den0 > 0 and num0 > 0 and num0 <= den0):
                        eff0 = num0 / den0
                        unc0 = pow(eff0*(1-eff0)/den0,0.5)

                    elif(den0 > 0):
                        eff0 = 0.0
                        unc0 = min(pow(1.0/den0,0.5),0.999)

                    den1 = histoLepDenDY[nlep][nsel].GetBinContent(i+1,j+1)
                    num1 = histoLepNumDY[nlep][nsel].GetBinContent(i+1,j+1)
                    eff1 = 0.0
                    unc1 = 0.0
                    if(den1 > 0 and num1 > 0 and num1 <= den1):
                        eff1 = num1 / den1
                        unc1 = pow(eff1*(1-eff1)/den1,0.5)

                    elif(den1 > 0):
                        eff1 = 0.0
                        unc1 = min(pow(1.0/den1,0.5),0.999)

                    sf = 0.
                    sfe = 0.
                    if(eff0 > 0 and eff1 > 0):
                        sf = eff0/eff1
                        sfe = sf*pow(pow(unc0/eff0,2)+pow(unc1/eff1,2),0.5)
                    elif(histoLepDenDY[nlep][nsel].GetXaxis().GetBinCenter(i+1) >= histoLepDenDY[nlep][nsel].GetYaxis().GetBinCenter(j+1)):
                        sf = 1

                    histoTriggerTightSFEtaPt[nlep][nsel].SetBinContent(i+1,j+1,sf)
                    histoTriggerTightSFEtaPt[nlep][nsel].SetBinError  (i+1,j+1,sfe)
                    histoTriggerTightDAEtaPt[nlep][nsel].SetBinContent(i+1,j+1,eff0)
                    histoTriggerTightDAEtaPt[nlep][nsel].SetBinError  (i+1,j+1,unc0)
                    histoTriggerTightMCEtaPt[nlep][nsel].SetBinContent(i+1,j+1,eff1)
                    histoTriggerTightMCEtaPt[nlep][nsel].SetBinError  (i+1,j+1,unc1)

                    print("BinTight({0:2d},{1:2d}): ( {2:.3f} +/- {3:.3f} ) / ( {4:.3f} - {5:.3f} ) = {6:.3f} / {7:.3f}".format(i+1,j+1,
                          eff0,unc0,eff1,unc1,sf,sfe))

    fileTriggerEffName = "histoTriggerSFEtaPt_{0}.root".format(year)
    outfileTriggerEff = TFile(fileTriggerEffName,"recreate")
    outfileTriggerEff.cd()
    for nlep in range(numberOfLep):
        for nsel in range(numberOfSel):
            histoTriggerLooseSFEtaPt[nlep][nsel].SetNameTitle("histoTriggerLooseSFEtaPt_{0}_{1}".format(nlep,nsel),"histoTriggerLooseSFEtaPt_{0}_{1}".format(nlep,nsel))
            histoTriggerLooseSFEtaPt[nlep][nsel].Write()
            histoTriggerLooseDAEtaPt[nlep][nsel].SetNameTitle("histoTriggerLooseDAEtaPt_{0}_{1}".format(nlep,nsel),"histoTriggerLooseDAEtaPt_{0}_{1}".format(nlep,nsel))
            histoTriggerLooseDAEtaPt[nlep][nsel].Write()
            histoTriggerLooseMCEtaPt[nlep][nsel].SetNameTitle("histoTriggerLooseMCEtaPt_{0}_{1}".format(nlep,nsel),"histoTriggerLooseMCEtaPt_{0}_{1}".format(nlep,nsel))
            histoTriggerLooseMCEtaPt[nlep][nsel].Write()
            histoTriggerTightSFEtaPt[nlep][nsel].SetNameTitle("histoTriggerSFEtaPt_{0}_{1}".format(nlep,nsel),"histoTriggerSFEtaPt_{0}_{1}".format(nlep,nsel))
            histoTriggerTightSFEtaPt[nlep][nsel].Write()
            histoTriggerTightDAEtaPt[nlep][nsel].SetNameTitle("histoTriggerDAEtaPt_{0}_{1}".format(nlep,nsel),"histoTriggerDAEtaPt_{0}_{1}".format(nlep,nsel))
            histoTriggerTightDAEtaPt[nlep][nsel].Write()
            histoTriggerTightMCEtaPt[nlep][nsel].SetNameTitle("histoTriggerMCEtaPt_{0}_{1}".format(nlep,nsel),"histoTriggerMCEtaPt_{0}_{1}".format(nlep,nsel))
            histoTriggerTightMCEtaPt[nlep][nsel].Write()
    outfileTriggerEff.Close()

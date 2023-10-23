import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
from array import array
from utilsCategory import plotCategory

xPtbins = array('d', [10,15,20,25,30,35,40,50,60,70,85,100,200,1000])
xEtabins = array('d', [0.0,1.0,1.5,2.0,2.5])

if __name__ == "__main__":
    path = "fillhisto_zAnalysis1001"
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

    # MB, ME, EB, EE
    fileLep = [[TFile("{0}/{1}_{2}_loose_mu_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu0_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu1_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu2_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu3_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu4_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu5_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu6_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu7_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightmu8_2d.root".format(output,path,year))
               ],
               [TFile("{0}/{1}_{2}_loose_el_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel0_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel1_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel2_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel3_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel4_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel5_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel6_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel7_2d.root".format(output,path,year)),
                TFile("{0}/{1}_{2}_tightel8_2d.root".format(output,path,year))
               ]]
    print(fileLep[0][3].GetName())
    print(fileLep[1][3].GetName())
    print(fileLep[1][7].GetName())

    numberOfSel = 9
    histoLepEffSelDAEtaPt = [[0 for y in range(numberOfSel)] for x in range(2)]
    histoLepEffSelDYEtaPt = [[0 for y in range(numberOfSel)] for x in range(2)]
    histoLepSFEtaPt = [[0 for y in range(numberOfSel)] for x in range(2)]

    fileLepEffName = "histoLepSFEtaPt_{0}_correction.root".format(year)
    outFileLepEff = TFile(fileLepEffName,"recreate")
    outFileLepEff.cd()

    for nlep in range(2):
        histoLepDenDA = (fileLep[nlep][0].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
        histoLepDenDY = (fileLep[nlep][0].Get("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
        for nc in range(nCat):
            if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY")): continue
            histoLepDenDA.Add(fileLep[nlep][0].Get("histo2d{0}".format(nc)),-1.0)
        print("Den({0}) = {1}/{2} = {3}".format(nlep,histoLepDenDA.GetSumOfWeights(),histoLepDenDY.GetSumOfWeights(),
              histoLepDenDA.GetSumOfWeights()/histoLepDenDY.GetSumOfWeights()))

        for theSel in range(1,numberOfSel+1):
            histoLepEffSelDAEtaPt[nlep][theSel - 1] = (fileLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepEffSelDAEtaPt[nlep][theSel - 1] = (fileLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepEffSelDYEtaPt[nlep][theSel - 1] = (fileLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepEffSelDYEtaPt[nlep][theSel - 1] = (fileLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepSFEtaPt      [nlep][theSel - 1] = (fileLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepSFEtaPt      [nlep][theSel - 1] = (fileLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepNumDA = (fileLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoLepNumDY = (fileLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
            for nc in range(nCat):
                if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY")): continue
                histoLepNumDA.Add(fileLep[nlep][theSel].Get("histo2d{0}".format(nc)),-1.0)

            print("Num({0},{1}) = {2}/{3} = {4}".format(nlep,theSel-1,histoLepNumDA.GetSumOfWeights(),histoLepNumDY.GetSumOfWeights(),
                  histoLepNumDA.GetSumOfWeights()/histoLepNumDY.GetSumOfWeights()))

            for i in range(histoLepDenDA.GetNbinsX()):
                for j in range(histoLepDenDA.GetNbinsY()):
                    den0 = histoLepDenDA.GetBinContent(i+1,j+1)
                    num0 = histoLepNumDA.GetBinContent(i+1,j+1)
                    eff0 = 1.0
                    unc0 = 0.0
                    if(den0 > 0 and num0 > 0 and num0 <= den0):
                        eff0 = num0 / den0
                        unc0 = pow(eff0*(1-eff0)/den0,0.5)

                    elif(den0 > 0):
                        eff0 = 0.0
                        unc0 = min(pow(1.0/den0,0.5),0.999)

                    den1 = histoLepDenDY.GetBinContent(i+1,j+1)
                    num1 = histoLepNumDY.GetBinContent(i+1,j+1)
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

                    histoLepEffSelDAEtaPt[nlep][theSel - 1].SetBinContent(i+1,j+1,eff0)
                    histoLepEffSelDAEtaPt[nlep][theSel - 1].SetBinError  (i+1,j+1,unc0)
                    histoLepEffSelDYEtaPt[nlep][theSel - 1].SetBinContent(i+1,j+1,eff1)
                    histoLepEffSelDYEtaPt[nlep][theSel - 1].SetBinError  (i+1,j+1,unc1)
                    histoLepSFEtaPt      [nlep][theSel - 1].SetBinContent(i+1,j+1,sf)
                    histoLepSFEtaPt      [nlep][theSel - 1].SetBinError  (i+1,j+1,sfe)

                    print("({0:2d},{1:2d}): ({2:.3f} +/- {3:.3f}) / ({4:.3f} - {5:.3f}) = {6:.3f} / {7:.3f}".format(i+1,j+1,
                          eff0,unc0,eff1,unc1,sf,sfe))

            histoLepEffSelDAEtaPt[nlep][theSel - 1].SetNameTitle("histoLepEffSelDAEtaPt_{0}_{1}".format(nlep,theSel - 1),"histoLepEffSelDAEtaPt_{0}_{1}".format(nlep,theSel - 1))
            histoLepEffSelDYEtaPt[nlep][theSel - 1].SetNameTitle("histoLepEffSelDYEtaPt_{0}_{1}".format(nlep,theSel - 1),"histoLepEffSelDYEtaPt_{0}_{1}".format(nlep,theSel - 1))
            histoLepSFEtaPt      [nlep][theSel - 1].SetNameTitle("histoLepSFEtaPt_{0}_{1}".format(nlep,theSel - 1),      "histoLepSFEtaPt_{0}_{1}".format(nlep,theSel - 1))
            histoLepEffSelDAEtaPt[nlep][theSel - 1].Write()
            histoLepEffSelDYEtaPt[nlep][theSel - 1].Write()
            histoLepSFEtaPt      [nlep][theSel - 1].Write()

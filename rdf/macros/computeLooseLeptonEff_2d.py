import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
from array import array

def plotCategory(key):
    plotCategoryDict = dict()
    plotCategoryDict.update({"kPlotData"      :[ 0]})
    plotCategoryDict.update({"kPlotqqWW"      :[ 1]})
    plotCategoryDict.update({"kPlotggWW"      :[ 2]})
    plotCategoryDict.update({"kPlotTop"       :[ 3]})
    plotCategoryDict.update({"kPlotDY"        :[ 4]})
    plotCategoryDict.update({"kPlotEWKSSWW"   :[ 5]})
    plotCategoryDict.update({"kPlotQCDSSWW"   :[ 6]})
    plotCategoryDict.update({"kPlotEWKWZ"     :[ 7]})
    plotCategoryDict.update({"kPlotWZ"        :[ 8]})
    plotCategoryDict.update({"kPlotZZ"        :[ 9]})
    plotCategoryDict.update({"kPlotNonPrompt" :[10]})
    plotCategoryDict.update({"kPlotVVV"       :[11]})
    plotCategoryDict.update({"kPlotTVX"       :[12]})
    plotCategoryDict.update({"kPlotVG"        :[13]})
    plotCategoryDict.update({"kPlotHiggs"     :[14]})
    plotCategoryDict.update({"kPlotDPSWW"     :[15]})
    plotCategoryDict.update({"kPlotWS"        :[16]})
    plotCategoryDict.update({"kPlotEM"        :[17]})
    plotCategoryDict.update({"kPlotOther"     :[18]})
    plotCategoryDict.update({"kPlotBSM"       :[19]})
    plotCategoryDict.update({"kPlotSignal0"   :[20]})
    plotCategoryDict.update({"kPlotSignal1"   :[21]})
    plotCategoryDict.update({"kPlotSignal2"   :[22]})
    plotCategoryDict.update({"kPlotSignal3"   :[23]})
    plotCategoryDict.update({"kPlotCategories":[24]})

    try:
        return plotCategoryDict[key][0]
    except Exception as e:
        print("Wrong key({0}): {1}".format(key,e))

xPtbins = array('d', [10,15,20,25,30,35,40,45,50,60,70,80,90,100,200,300])
xEtabins = array('d', [0.0,0.5,1.0,1.5,2.0,2.5])

if __name__ == "__main__":
    path = "fillhisto_triggerAnalysis1001"
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

    # Lepton efficiency
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

    fileLepEffName = "histoLepSFEtaPt_{0}.root".format(year)
    outFileLepEff = TFile(fileLepEffName,"recreate")
    outFileLepEff.cd()

    numberOfSel = 9
    histoLepEffSelDAEtaPt = [[0 for y in range(numberOfSel)] for x in range(2)]
    histoLepEffSelDYEtaPt = [[0 for y in range(numberOfSel)] for x in range(2)]
    histoLepSFEtaPt = [[0 for y in range(numberOfSel)] for x in range(2)]

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
                        sfe = sf*pow(pow(unc0/eff0,0.5)+pow(unc1/eff1,0.5),2)

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

    # Trigger efficiency
    fileTriggerLep = [[TFile("{0}/{1}_{2}_tightmu1_2d.root".format(output,path,year)),
        	       TFile("{0}/{1}_{2}_triggerm0_2d.root".format(output,path,year)),
        	       TFile("{0}/{1}_{2}_triggerm1_2d.root".format(output,path,year))
                      ],
                      [TFile("{0}/{1}_{2}_tightel1_2d.root".format(output,path,year)),
        	       TFile("{0}/{1}_{2}_triggere0_2d.root".format(output,path,year)),
        	       TFile("{0}/{1}_{2}_triggere1_2d.root".format(output,path,year))
                      ]]
    print(fileTriggerLep[0][0].GetName())
    print(fileTriggerLep[1][0].GetName())
    print(fileTriggerLep[1][1].GetName())

    outFileLepEff.cd()

    numberOfTriggerSel = 2
    histoTriggerEffSelDAEtaPt = [[0 for y in range(numberOfTriggerSel)] for x in range(2)]
    histoTriggerEffSelDYEtaPt = [[0 for y in range(numberOfTriggerSel)] for x in range(2)]
    histoTriggerSFEtaPt = [[0 for y in range(numberOfTriggerSel)] for x in range(2)]

    for nlep in range(2):
        histoTriggerDenDA = (fileTriggerLep[nlep][0].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
        histoTriggerDenDY = (fileTriggerLep[nlep][0].Get("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
        for nc in range(nCat):
            if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY")): continue
            histoTriggerDenDA.Add(fileTriggerLep[nlep][0].Get("histo2d{0}".format(nc)),-1.0)
        print("Den({0}) = {1}/{2} = {3}".format(nlep,histoTriggerDenDA.GetSumOfWeights(),histoTriggerDenDY.GetSumOfWeights(),
              histoTriggerDenDA.GetSumOfWeights()/histoTriggerDenDY.GetSumOfWeights()))

        for theSel in range(1,numberOfTriggerSel+1):
            histoTriggerEffSelDAEtaPt[nlep][theSel - 1] = (fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoTriggerEffSelDAEtaPt[nlep][theSel - 1] = (fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoTriggerEffSelDYEtaPt[nlep][theSel - 1] = (fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoTriggerEffSelDYEtaPt[nlep][theSel - 1] = (fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoTriggerSFEtaPt      [nlep][theSel - 1] = (fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoTriggerSFEtaPt      [nlep][theSel - 1] = (fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoTriggerNumDA = (fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotData")))).Clone()
            histoTriggerNumDY = (fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(plotCategory("kPlotDY")))).Clone()
            for nc in range(nCat):
                if(nc == plotCategory("kPlotData") or nc == plotCategory("kPlotDY")): continue
                histoTriggerNumDA.Add(fileTriggerLep[nlep][theSel].Get("histo2d{0}".format(nc)),-1.0)

            print("Num({0},{1}) = {2}/{3} = {4}".format(nlep,theSel-1,histoTriggerNumDA.GetSumOfWeights(),histoTriggerNumDY.GetSumOfWeights(),
                  histoTriggerNumDA.GetSumOfWeights()/histoTriggerNumDY.GetSumOfWeights()))

            for i in range(histoTriggerDenDA.GetNbinsX()):
                for j in range(histoTriggerDenDA.GetNbinsY()):
                    den0 = histoTriggerDenDA.GetBinContent(i+1,j+1)
                    num0 = histoTriggerNumDA.GetBinContent(i+1,j+1)
                    eff0 = 1.0
                    unc0 = 0.0
                    if(den0 > 0 and num0 > 0 and num0 <= den0):
                        eff0 = num0 / den0
                        unc0 = pow(eff0*(1-eff0)/den0,0.5)

                    elif(den0 > 0):
                        eff0 = 0.0
                        unc0 = min(pow(1.0/den0,0.5),0.999)

                    den1 = histoTriggerDenDY.GetBinContent(i+1,j+1)
                    num1 = histoTriggerNumDY.GetBinContent(i+1,j+1)
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
                        sfe = sf*pow(pow(unc0/eff0,0.5)+pow(unc1/eff1,0.5),2)

                    histoTriggerEffSelDAEtaPt[nlep][theSel - 1].SetBinContent(i+1,j+1,eff0)
                    histoTriggerEffSelDAEtaPt[nlep][theSel - 1].SetBinError  (i+1,j+1,unc0)
                    histoTriggerEffSelDYEtaPt[nlep][theSel - 1].SetBinContent(i+1,j+1,eff1)
                    histoTriggerEffSelDYEtaPt[nlep][theSel - 1].SetBinError  (i+1,j+1,unc1)
                    histoTriggerSFEtaPt      [nlep][theSel - 1].SetBinContent(i+1,j+1,sf)
                    histoTriggerSFEtaPt      [nlep][theSel - 1].SetBinError  (i+1,j+1,sfe)

                    print("({0:2d},{1:2d}): ({2:.3f} +/- {3:.3f}) / ({4:.3f} - {5:.3f}) = {6:.3f} / {7:.3f}".format(i+1,j+1,
                          eff0,unc0,eff1,unc1,sf,sfe))

            histoTriggerEffSelDAEtaPt[nlep][theSel - 1].SetNameTitle("histoTriggerEffSelDAEtaPt_{0}_{1}".format(nlep,theSel - 1),"histoTriggerEffSelDAEtaPt_{0}_{1}".format(nlep,theSel - 1))
            histoTriggerEffSelDYEtaPt[nlep][theSel - 1].SetNameTitle("histoTriggerEffSelDYEtaPt_{0}_{1}".format(nlep,theSel - 1),"histoTriggerEffSelDYEtaPt_{0}_{1}".format(nlep,theSel - 1))
            histoTriggerSFEtaPt      [nlep][theSel - 1].SetNameTitle("histoTriggerSFEtaPt_{0}_{1}".format(nlep,theSel - 1),      "histoTriggerSFEtaPt_{0}_{1}".format(nlep,theSel - 1))
            histoTriggerEffSelDAEtaPt[nlep][theSel - 1].Write()
            histoTriggerEffSelDYEtaPt[nlep][theSel - 1].Write()
            histoTriggerSFEtaPt      [nlep][theSel - 1].Write()

    outFileLepEff.Close()

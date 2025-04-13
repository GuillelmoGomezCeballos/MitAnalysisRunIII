import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
from utilsCategory import plotCategory

if __name__ == "__main__":
    path = "fillhisto_sswwAnalysis1001"
    year = 2022
    output = "anaZ"
    showUnc = 0

    valid = ['path=', "year=", 'output=', "unc=", 'help']
    usage  =  "Usage: ana.py --path=<{0}>\n".format(path)
    usage +=  "              --year=<{0}>\n".format(year)
    usage +=  "              --output=<{0}>".format(output)
    usage +=  "              --unc=<{0}>".format(showUnc)
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
        if opt == "--unc":
            showUnc = int(arg)

    histo = []
    signalDict0 = []
    signalDict1 = []
    if('sswwAna' in path):
        histo.append(18)
        signalDict0.append(plotCategory("kPlotEWKSSWW"))
        signalDict1.append(plotCategory("kPlotEWKSSWW"))
        histo.append(19)
        signalDict0.append(plotCategory("kPlotEWKSSWW"))
        signalDict1.append(plotCategory("kPlotEWKSSWW"))
    elif('zzAna' in path):
        histo.append(8)
        signalDict0.append(plotCategory("kPlotZZ"))
        signalDict1.append(plotCategory("kPlotZZ"))
        histo.append(16)
        signalDict0.append(plotCategory("kPlotZZ"))
        signalDict1.append(plotCategory("kPlotZZ"))
    elif('wzAna' in path):
        histo.append(11)
        signalDict0.append(plotCategory("kPlotWZ"))
        signalDict1.append(plotCategory("kPlotWZ"))
        histo.append(12)
        signalDict0.append(plotCategory("kPlotWZ"))
        signalDict1.append(plotCategory("kPlotWZ"))
        histo.append(17)
        signalDict0.append(plotCategory("kPlotWZ"))
        signalDict1.append(plotCategory("kPlotWZ"))
        histo.append(18)
        signalDict0.append(plotCategory("kPlotWZ"))
        signalDict1.append(plotCategory("kPlotWZ"))
        histo.append(27)
        signalDict0.append(plotCategory("kPlotEWKWZ"))
        signalDict1.append(plotCategory("kPlotEWKWZ"))
        histo.append(28)
        signalDict0.append(plotCategory("kPlotEWKWZ"))
        signalDict1.append(plotCategory("kPlotEWKWZ"))
        #histo.append(77)
        #signalDict0.append(plotCategory("kPlotWZ"))
        #signalDict1.append(plotCategory("kPlotWZ"))
        #histo.append(81)
        #signalDict0.append(plotCategory("kPlotWZ"))
        #signalDict1.append(plotCategory("kPlotWZ"))
    elif('zmetAna' in path):
        histo.append(34)
        signalDict0.append(plotCategory("kPlotZZ"))
        signalDict1.append(plotCategory("kPlotZZ"))
        histo.append(35)
        signalDict0.append(plotCategory("kPlotZZ"))
        signalDict1.append(plotCategory("kPlotZZ"))
    elif('wwAna' in path):
        histo.append(42)
        signalDict0.append(plotCategory("kPlotNonPrompt"))
        signalDict1.append(plotCategory("kPlotNonPrompt"))
        histo.append(71)
        signalDict0.append(plotCategory("kPlotNonPrompt"))
        signalDict1.append(plotCategory("kPlotNonPrompt"))
        histo.append(72)
        signalDict0.append(plotCategory("kPlotNonPrompt"))
        signalDict1.append(plotCategory("kPlotNonPrompt"))
        histo.append(43)
        signalDict0.append(plotCategory("kPlotqqWW"))
        signalDict1.append(plotCategory("kPlotggWW"))
        histo.append(44)
        signalDict0.append(plotCategory("kPlotDY"))
        signalDict1.append(plotCategory("kPlotDY"))
        histo.append(45)
        signalDict0.append(plotCategory("kPlotTT"))
        signalDict1.append(plotCategory("kPlotTW"))
        histo.append(57)
        signalDict0.append(plotCategory("kPlotHiggs"))
        signalDict1.append(plotCategory("kPlotHiggs"))
    elif('zAna' in path):
        histo.append(27)
        signalDict0.append(plotCategory("kPlotDY"))
        signalDict1.append(plotCategory("kPlotDY"))
        histo.append(28)
        signalDict0.append(plotCategory("kPlotDY"))
        signalDict1.append(plotCategory("kPlotDY"))
        histo.append(29)
        signalDict0.append(plotCategory("kPlotDY"))
        signalDict1.append(plotCategory("kPlotDY"))

    nCat = plotCategory("kPlotCategories")
    for nh in range(len(histo)):
        print("**********HISTO: {0} **********".format(histo[nh]))
        histoSel = [0 for y in range(nCat)]
        inputFile = TFile("{0}/{1}_{2}_{3}.root".format(output,os.path.basename(path),year,histo[nh]),"w")
        theYields  = [0,0,0]
        theYieldsE = [0,0,0]
        theYieldsProcess     = [0 for y in range(nCat)]
        theYieldsProcessUnc  = [0 for y in range(nCat)]
        for i in range(nCat):
            histoSel[i] = (inputFile.Get("histo{0}".format(i))).Clone()
        for nb in range(1,histoSel[0].GetNbinsX()+1):
            streamYield = ""
            mcYield = 0
            processesWithEvents = []
            for i in range(nCat):
                if(histoSel[i].GetSumOfWeights() > 0 or i == plotCategory("kPlotData")):
                    if(showUnc == 0):
                        streamYield += " {0:7.1f}".format(histoSel[i].GetBinContent(nb))
                    else:
                        streamYield += " {0:7.1f} +/- {1:5.1f}".format(histoSel[i].GetBinContent(nb),histoSel[i].GetBinError(nb))
                    processesWithEvents.append(i)
                theYieldsProcess[i]     += histoSel[i].GetBinContent(nb)
                theYieldsProcessUnc[i]  += histoSel[i].GetBinError(nb)
                if(i == plotCategory("kPlotData")):
                    theYields[0]  += histoSel[i].GetBinContent(nb)
                    theYieldsE[0] += histoSel[i].GetBinError(nb)*histoSel[i].GetBinError(nb)
                elif(i == signalDict0[nh] or i == signalDict1[nh]):
                    theYields[1]  += histoSel[i].GetBinContent(nb)
                    theYieldsE[1] += histoSel[i].GetBinError(nb)*histoSel[i].GetBinError(nb)
                    mcYield += histoSel[i].GetBinContent(nb)
                else:
                    theYields[2]  += histoSel[i].GetBinContent(nb)
                    theYieldsE[2] += histoSel[i].GetBinError(nb)*histoSel[i].GetBinError(nb)
                    mcYield += histoSel[i].GetBinContent(nb)
            streamYield = "({0:2d}) {1:7.1f}".format(nb,mcYield) + streamYield
            if(nb == 1):
                streamProcess = "         "
                for pr in range(len(processesWithEvents)):
                    streamProcess += " {0:7d}".format(processesWithEvents[pr])
                print(streamProcess)
            print(streamYield)

        streamYield = ""
        for i in range(nCat):
            if(histoSel[i].GetSumOfWeights() > 0 or i == plotCategory("kPlotData")):
                if(showUnc == 0):
                    streamYield += " {0:7.1f}".format(theYieldsProcess[i])
                else:
                    streamYield += " {0:7.1f} +/- {1:5.1f}".format(theYieldsProcess[i],theYieldsProcessUnc[i])
        for i in range(3):
            theYieldsE[i] = pow(theYieldsE[i],0.5)
        streamYield = "(xx) {0:7.1f}".format(theYields[1]+theYields[2]) + streamYield
        print(streamYield)
        print("DA: {0:7.1f} +/- {1:4.1f} / SIG: {2:7.1f} +/- {3:4.1f} / BG: {4:7.1f} +/- {5:4.1f}".format(theYields[0],theYieldsE[0],theYields[1],theYieldsE[1],theYields[2],theYieldsE[2]))
        SB = theYields[1]/theYields[2]
        DataVsPred = theYields[0]/(theYields[1]+theYields[2])
        DataVsPredE = DataVsPred*pow(pow(theYieldsE[0]/theYields[0],2)+pow(theYieldsE[1]/(theYields[1]+theYields[2]),2)+pow(theYieldsE[2]/(theYields[1]+theYields[2]),2),0.5)
        print("SB: {0:.2f} / DataVsPred: {1:.2f} +/- {2:.2f}".format(SB,DataVsPred,DataVsPredE))

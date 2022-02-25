import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
from array import array
from utilsAna import plotCategory

if __name__ == "__main__":
    path = "fillhistoSSWWAna1001"
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

    histo = []
    signalDict = []
    if('SSWW' in path):
        histo.append(20)
        signalDict.append(plotCategory("kPlotEWKSSWW"))
        histo.append(21)
        signalDict.append(plotCategory("kPlotEWKSSWW"))
    elif('ZZ' in path):
        histo.append(8)
        signalDict.append(plotCategory("kPlotZZ"))
    elif('WZ' in path):
        histo.append(11)
        signalDict.append(plotCategory("kPlotWZ"))
        histo.append(12)
        signalDict.append(plotCategory("kPlotWZ"))
    elif('ZMET' in path):
        histo.append(24)
        signalDict.append(plotCategory("kPlotZZ"))
        histo.append(25)
        signalDict.append(plotCategory("kPlotZZ"))
        histo.append(26)
        signalDict.append(plotCategory("kPlotZZ"))

    nCat = plotCategory("kPlotCategories")
    for nh in range(len(histo)):
        print("**********HISTO: {0} **********".format(histo[nh]))
        histoSel = [0 for y in range(nCat)]
        inputFile = TFile("{0}/{1}_{2}_{3}.root".format(output,os.path.basename(path),year,histo[nh]),"w")
        theYields  = [0,0,0]
        theYieldsE = [0,0,0]
        theYieldsProcess  = [0 for y in range(nCat)]
        for i in range(nCat):
            histoSel[i] = (inputFile.Get("histo{0}".format(i))).Clone()
        for nb in range(1,histoSel[0].GetNbinsX()+1):
            streamYield = ""
            mcYield = 0
            processesWithEvents = []
            for i in range(nCat):
                if(histoSel[i].GetSumOfWeights() > 0 or i == plotCategory("kPlotData")):
                    streamYield += " {0:6.1f}".format(histoSel[i].GetBinContent(nb))
                    processesWithEvents.append(i)
                theYieldsProcess[i]  += histoSel[i].GetBinContent(nb)
                if(i == plotCategory("kPlotData")):
                    theYields[0]  += histoSel[i].GetBinContent(nb)
                    theYieldsE[0] += histoSel[i].GetBinError(nb)*histoSel[i].GetBinError(nb)
                elif(i == signalDict[nh]):
                    theYields[1]  += histoSel[i].GetBinContent(nb)
                    theYieldsE[1] += histoSel[i].GetBinError(nb)*histoSel[i].GetBinError(nb)
                    mcYield += histoSel[i].GetBinContent(nb)
                else:
                    theYields[2]  += histoSel[i].GetBinContent(nb)
                    theYieldsE[2] += histoSel[i].GetBinError(nb)*histoSel[i].GetBinError(nb)
                    mcYield += histoSel[i].GetBinContent(nb)
            streamYield = "({0:2d}) {1:6.1f}".format(nb,mcYield) + streamYield
            if(nb == 1):
                streamProcess = "         "
                for pr in range(len(processesWithEvents)):
                    streamProcess += " {0:6d}".format(processesWithEvents[pr])
                print(streamProcess)
            print(streamYield)

        streamYield = ""
        for i in range(nCat):
            if(histoSel[i].GetSumOfWeights() > 0 or i == plotCategory("kPlotData")):
                streamYield += " {0:6.1f}".format(theYieldsProcess[i])
        for i in range(3):
            theYieldsE[i] = pow(theYieldsE[i],0.5)
        streamYield = "(xx) {0:6.1f}".format(theYields[1]+theYields[2]) + streamYield
        print(streamYield)
        print("DA: {0:6.1f} +/- {1:4.1f} / SIG: {2:6.1f} +/- {3:4.1f} / BG: {4:6.1f} +/- {5:4.1f}".format(theYields[0],theYieldsE[0],theYields[1],theYieldsE[1],theYields[2],theYieldsE[2]))
        SB = theYields[1]/theYields[2]
        DataVsPred = theYields[0]/(theYields[1]+theYields[2])
        DataVsPredE = DataVsPred*pow(pow(theYieldsE[0]/theYields[0],2)+pow(theYieldsE[1]/(theYields[1]+theYields[2]),2)+pow(theYieldsE[2]/(theYields[1]+theYields[2]),2),0.5)
        print("SB: {0:.2f} / DataVsPred: {1:.2f} +/- {2:.2f}".format(SB,DataVsPred,DataVsPredE))

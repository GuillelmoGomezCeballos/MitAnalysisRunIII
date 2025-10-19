import ROOT
from array import array

def getFunVal(fitVal,x,debug):
    val = 0
    for nf in range(0, len(fitVal)):
        val = val + fitVal[nf] * pow(x, nf)
    if(debug == 1):
        print(x,val)
    return val

debug = 0

histoVal = []
histoValQCD = []

filename = ["data/dist_mjj_LO.dat", "data/dist_mjj_NLOQCD.dat", "data/dist_mjj_NLOEW.dat", "data/dist_mjj_NLOEWQCD.dat"]

for nf in range(0, len(filename)):
    with open(filename[nf], "r") as file:
        xBins = array('d')
        xVal = array('d')
        xValStat = array('d')
        xValQCD = array('d')
        count = 0
        for line in file:
            # Skip empty lines or comments
            if(not line.strip()):
                continue
            valueString = line.strip().split()

            count = count + 1
            if(count%2 == 1):
                xBins.append(float(valueString[1]))
                xVal.append(float(valueString[2]))
                xValStat.append(float(valueString[3]))
                xVal_qcd = [float(valueString[4]), float(valueString[5]), float(valueString[6]), float(valueString[7]), float(valueString[8]), float(valueString[9]), float(valueString[10])]
                xVal_qcd_max = 0
                for nqcd in range(0, 7):
                    xVal_qcd_max = max(xVal_qcd_max, abs(xVal_qcd[nqcd]-xVal[len(xBins)-1]))
                xValQCD.append(xVal_qcd_max)

        histoVal.append(ROOT.TH1D(filename[nf].replace(".dat", ""), filename[nf].replace(".dat", ""), len(xBins)-1, xBins))
        histoValQCD.append(ROOT.TH1D(filename[nf].replace(".dat", "_QCD"), filename[nf].replace(".dat", "_QCD"), len(xBins)-1, xBins))
        for nb in range(0, len(xBins)-1):
            histoVal[nf].SetBinContent(nb+1, xVal[nb])
            histoVal[nf].SetBinError  (nb+1, xValStat[nb])
            histoValQCD[nf].SetBinContent(nb+1, xValQCD[nb])
            histoValQCD[nf].SetBinError  (nb+1, xValQCD[nb]*xValStat[nb]/xVal[nb])
        if(debug == 1):
             print(nf,histoVal[nf].GetSumOfWeights(),histoValQCD[nf].GetSumOfWeights()/histoVal[nf].GetSumOfWeights())

histoKF     = histoVal[0].Clone()
histoKFUp   = histoVal[0].Clone()
histoKFDown = histoVal[0].Clone()
histoKF    .SetNameTitle("hWW13p6_KF_CMS",     "hWW13p6_KF_CMS")
histoKFUp  .SetNameTitle("hWW13p6_KF_CMSUp",   "hWW13p6_KF_CMSUp")
histoKFDown.SetNameTitle("hWW13p6_KF_CMSDown", "hWW13p6_KF_CMSDown")

histoKFRaw     = histoVal[0].Clone()
histoKFRawUp   = histoVal[0].Clone()
histoKFRaw  .SetNameTitle("hWW13p6_KFRaw_CMS",   "hWW13p6_KFRaw_CMS")
histoKFRawUp.SetNameTitle("hWW13p6_KFRaw_CMSUp", "hWW13p6_KFRaw_CMSUp")

for nb in range(histoKF.GetNbinsX()):
    val_nlo = histoVal[3].GetBinContent(nb+1)
    val_lo  = histoVal[0].GetBinContent(nb+1)
    val_kf = val_nlo/val_lo
    histoKFRaw    .SetBinContent(nb+1, val_kf)
    histoKFRaw    .SetBinError  (nb+1, histoVal[3]   .GetBinError  (nb+1)/histoVal[0].GetBinContent(nb+1))
    histoKFRawUp  .SetBinContent(nb+1, histoValQCD[3].GetBinContent(nb+1)/histoVal[0].GetBinContent(nb+1))
    histoKFRawUp  .SetBinError  (nb+1, histoValQCD[3].GetBinError  (nb+1)/histoVal[0].GetBinContent(nb+1))

histoKFRaw.Fit("pol6","","",500,4000)
fit_val = [
     1.58268,
 -0.00210506,
 2.46521e-06,
-1.56474e-09,
 5.47743e-13,
-9.90396e-17,
 7.20575e-21
]

histoKFRawUp.Fit("pol6","","",500,4000)
fit_val_unc = [
    0.144262,
 -0.00059717,
 9.28129e-07,
 -6.6234e-10,
 2.41098e-13,
-4.33941e-17,
 3.06288e-21
]

for nb in range(histoKF.GetNbinsX()):
    binX = histoKF.GetBinCenter(nb+1)
    if(binX > 3000): binX = 3000
    val     = getFunVal(fit_val,     binX, debug)
    val_unc = getFunVal(fit_val_unc, binX, debug)
    histoKF    .SetBinContent(nb+1, val)
    histoKFUp  .SetBinContent(nb+1, val * (1 + val_unc))
    histoKFDown.SetBinContent(nb+1, val / (1 + val_unc))

outFile = ROOT.TFile("WW13p6_NLO_LO_CMS_mjj.root","recreate")
outFile.cd()
histoKFRaw  .Write()
histoKFRawUp.Write()
histoKF     .Write()
histoKFUp   .Write()
histoKFDown .Write()
outFile.Clone()

if(debug == 1):
    canvas = ROOT.TCanvas("c1", "Canvas", 800, 600)
    canvas.Divide(2,3)
    canvas.cd(1)
    histoVal[0].Draw()
    histoValQCD[0].Draw("same,hist")
    canvas.cd(2)
    histoVal[1].Draw()
    histoValQCD[1].Draw("same,hist")
    canvas.cd(3)
    histoVal[2].Draw()
    histoValQCD[2].Draw("same,hist")
    canvas.cd(4)
    histoVal[3].Draw()
    histoValQCD[3].Draw("same,hist")
    canvas.cd(5)
    histoKFRaw.Draw()
    canvas.cd(6)
    histoKFRawUp.Draw()
    canvas.SaveAs("canvas_debug_kf.png")

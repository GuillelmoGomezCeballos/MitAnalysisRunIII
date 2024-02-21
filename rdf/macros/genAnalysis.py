import ROOT
import os, sys, getopt, json
from array import array

ROOT.ROOT.EnableImplicitMT(10)
from utilsCategory import plotCategory
from utilsAna import getMClist, getDATAlist, getTriggerFromJson, getLumi
from utilsAna import SwitchSample
from utilsSelection import selectionGenLepJet, selectionTheoryWeigths, makeFinalVariable

jetEtaCut = 2.5

def analysis(df,count,category,weight,year,PDType,isData,histo_wwpt,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm):

    xPtBins = array('d', [20,25,30,35,40,50,60,80,100,150,250,500,1000])
    xEtaBins = array('d', [0.0,0.3,0.6,0.9,1.2,1.5,1.8,2.1,2.5])

    print("starting {0} / {1} / {2} / {3} / {4} / {5}".format(count,category,weight,year,PDType,isData))

    theCat = category
    if(theCat > 100): theCat = plotCategory("kPlotData")

    nCat, nHisto = plotCategory("kPlotCategories"), 200
    histo   = [[0 for x in range(nCat)] for y in range(nHisto)]
    histo2D = [[0 for y in range(nCat)] for x in range(nHisto)]

    ROOT.initHisto1D(histo_wwpt[0],3)
    ROOT.initHisto1D(histo_wwpt[1],4)
    ROOT.initHisto1D(histo_wwpt[2],5)
    ROOT.initHisto1D(histo_wwpt[3],6)
    ROOT.initHisto1D(histo_wwpt[4],7)

    ROOT.initJSONSFs(year)

    dfcat = df.Define("PDType","\"{0}\"".format(PDType))\
              .Define("weightForBTag","1.0f")\
              .Define("weight","{0}*genWeight".format(weight/getLumi(year)))\
              .Filter("weight != 0","good weight")

    dfcat = selectionTheoryWeigths(dfcat,weight,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm)

    x = 0

    dfzllgen = (dfcat
          .Define("gen_z", "GenPart_pdgId == 23 && GenPart_status == 62")
          .Filter("Sum(gen_z) >= 1","nZ >= 1")
          .Filter("Sum(gen_z) == 1","nZ == 1")
          .Define("Zpt", "GenPart_pt[gen_z]")
          .Define("Zeta", "GenPart_eta[gen_z]")
          .Define("Zphi", "abs(GenPart_phi[gen_z])")
          .Define("Zmass", "GenPart_mass[gen_z]")
          .Filter("abs(Zmass[0]-91.1876) < 15","Zmass cut")
          .Define("Zrap", "abs(makeRapidity(Zpt[0],Zeta[0],Zphi[0],Zmass[0]))")
            )

    dfwwxgen = selectionGenLepJet(dfcat,20,30,jetEtaCut).Filter("ngood_GenDressedLeptons >= 2", "ngood_GenDressedLeptons >= 2")
    dfwwxgen = (dfwwxgen.Define("theGenCat0", "compute_gen_category({0},ngood_GenJets,ngood_GenDressedLeptons,good_GenDressedLepton_pdgId,good_GenDressedLepton_hasTauAnc,good_GenDressedLepton_pt,good_GenDressedLepton_eta,good_GenDressedLepton_phi,good_GenDressedLepton_mass,0)-1.0".format(0))
                      .Define("theGenCat1", "compute_gen_category({0},ngood_GenJets,ngood_GenDressedLeptons,good_GenDressedLepton_pdgId,good_GenDressedLepton_hasTauAnc,good_GenDressedLepton_pt,good_GenDressedLepton_eta,good_GenDressedLepton_phi,good_GenDressedLepton_mass,1)-1.0".format(0))
                      .Define("theGenCat2", "compute_gen_category({0},ngood_GenJets,ngood_GenDressedLeptons,good_GenDressedLepton_pdgId,good_GenDressedLepton_hasTauAnc,good_GenDressedLepton_pt,good_GenDressedLepton_eta,good_GenDressedLepton_phi,good_GenDressedLepton_mass,2)-1.0".format(0))
                      .Define("theGenCat" , "compute_gen_category({0},ngood_GenJets,ngood_GenDressedLeptons,good_GenDressedLepton_pdgId,good_GenDressedLepton_hasTauAnc,good_GenDressedLepton_pt,good_GenDressedLepton_eta,good_GenDressedLepton_phi,good_GenDressedLepton_mass,3)-1.0".format(0))
                      .Filter("theGenCat0 >= 0","theGenCat0 >= 0")
                      .Filter("theGenCat1 >= 0","theGenCat1 >= 0")
                      .Filter("theGenCat2 >= 0","theGenCat2 >= 0")
                      .Filter("theGenCat  >= 0","theGenCat  >= 0")
                      .Define("theNNLOWeight0", "weight*compute_ptww_weight(good_GenDressedLepton_pt,good_GenDressedLepton_phi,GenMET_pt,GenMET_phi,0)")
                      .Define("theNNLOWeight1", "weight*compute_ptww_weight(good_GenDressedLepton_pt,good_GenDressedLepton_phi,GenMET_pt,GenMET_phi,1)")
                      .Define("theNNLOWeight2", "weight*compute_ptww_weight(good_GenDressedLepton_pt,good_GenDressedLepton_phi,GenMET_pt,GenMET_phi,2)")
                      .Define("theNNLOWeight3", "weight*compute_ptww_weight(good_GenDressedLepton_pt,good_GenDressedLepton_phi,GenMET_pt,GenMET_phi,3)")
                      .Define("theNNLOWeight4", "weight*compute_ptww_weight(good_GenDressedLepton_pt,good_GenDressedLepton_phi,GenMET_pt,GenMET_phi,4)")
                      )

    histo[10][x] = dfzllgen.Histo1D(("histo_{0}_{1}".format(10,x), "histo_{0}_{1}".format(10,x), 60, 91.1876-15, 91.1876+15), "Zmass","weight")
    histo[11][x] = dfzllgen.Histo1D(("histo_{0}_{1}".format(11,x), "histo_{0}_{1}".format(11,x), 50, 0., 100.), "Zpt","weight")
    histo[12][x] = dfzllgen.Histo1D(("histo_{0}_{1}".format(12,x), "histo_{0}_{1}".format(12,x), 50, 0., 5.0), "Zrap","weight")
    histo2D[100][x] = dfzllgen.Histo2D(("histo2d_{0}_{1}".format(100,x),"histo2d_{0}_{1}".format(100,x),10, 0, 5, 40, 0, 100),"Zrap","Zpt","weight")

    dfzllgen = (dfzllgen
          .Define("genLep", "(abs(GenDressedLepton_pdgId) == 11 || abs(GenDressedLepton_pdgId) == 13)")
          .Filter("Sum(genLep) == 2","genLep == 2")
          .Define("filter_GenDressedLepton_pt", "GenDressedLepton_pt[genLep]")
          .Define("filter_GenDressedLepton_eta", "GenDressedLepton_eta[genLep]")
            )

    dfzllgen = dfzllgen.Filter("abs(filter_GenDressedLepton_eta[0]) < 2.5 && abs(filter_GenDressedLepton_eta[1]) < 2.5","eta requirements")
    dfzllgen = dfzllgen.Filter("filter_GenDressedLepton_pt[0] > 10 && filter_GenDressedLepton_pt[1] > 10","Minimal pt requirements")

    histo[13][x] = dfzllgen.Histo1D(("histo_{0}_{1}".format(13,x), "histo_{0}_{1}".format(13,x), 50, 0., 100.), "Zpt","weight")
    histo[14][x] = dfzllgen.Histo1D(("histo_{0}_{1}".format(14,x), "histo_{0}_{1}".format(14,x), 50, 0., 5.0), "Zrap","weight")

    dfzllgen = dfzllgen.Filter("filter_GenDressedLepton_pt[0] > 25 && filter_GenDressedLepton_pt[1] > 25","Tighter pt requirements")

    histo[15][x] = dfzllgen.Histo1D(("histo_{0}_{1}".format(15,x), "histo_{0}_{1}".format(15,x), 50, 0., 100.), "Zpt","weight")
    histo[16][x] = dfzllgen.Histo1D(("histo_{0}_{1}".format(16,x), "histo_{0}_{1}".format(16,x), 50, 0., 5.0), "Zrap","weight")
    histo2D[101][x] = dfzllgen.Histo2D(("histo2d_{0}_{1}".format(101,x),"histo2d_{0}_{1}".format(100,x),10, 0, 5, 40, 0, 101),"Zrap","Zpt","weight")

    BinXF = 3
    minXF = -0.5
    maxXF = 2.5

    startF = 0
    histo[startF+20][x] = dfwwxgen.Histo1D(("histo_{0}_{1}".format(startF+20,x), "histo_{0}_{1}".format(startF+20,x),BinXF,minXF,maxXF),"theGenCat","weight")
    for nv in range(1,114):
        histo[startF+20+nv][x] = makeFinalVariable(dfwwxgen,"theGenCat",theCat,startF+20,x,BinXF,minXF,maxXF,nv)

    histo[134][x] = dfwwxgen.Histo1D(("histo_{0}_{1}".format(134,x), "histo_{0}_{1}".format(134,x),BinXF,minXF,maxXF),"theGenCat","weight")
    histo[135][x] = dfwwxgen.Histo1D(("histo_{0}_{1}".format(135,x), "histo_{0}_{1}".format(135,x),BinXF,minXF,maxXF),"theGenCat","theNNLOWeight0")
    histo[136][x] = dfwwxgen.Histo1D(("histo_{0}_{1}".format(136,x), "histo_{0}_{1}".format(136,x),BinXF,minXF,maxXF),"theGenCat","theNNLOWeight1")
    histo[137][x] = dfwwxgen.Histo1D(("histo_{0}_{1}".format(137,x), "histo_{0}_{1}".format(137,x),BinXF,minXF,maxXF),"theGenCat","theNNLOWeight2")
    histo[138][x] = dfwwxgen.Histo1D(("histo_{0}_{1}".format(138,x), "histo_{0}_{1}".format(138,x),BinXF,minXF,maxXF),"theGenCat","theNNLOWeight3")
    histo[139][x] = dfwwxgen.Histo1D(("histo_{0}_{1}".format(139,x), "histo_{0}_{1}".format(139,x),BinXF,minXF,maxXF),"theGenCat","theNNLOWeight4")

    report0 = dfzllgen.Report()
    report1 = dfwwxgen.Report()
    print("---------------- SUMMARY -------------")
    report0.Print()
    report1.Print()

    myfile = ROOT.TFile("fillhisto_puAnalysis_sample{0}_year{1}_job-1.root".format(count,year),'RECREATE')
    for nc in range(nCat):
        for j in range(nHisto):
            if(histo[j][nc] == 0): continue

            histo[j][nc].SetBinContent(histo[j][nc].GetNbinsX(),histo[j][nc].GetBinContent(histo[j][nc].GetNbinsX())+histo[j][nc].GetBinContent(histo[j][nc].GetNbinsX()+1))
            histo[j][nc].SetBinError  (histo[j][nc].GetNbinsX(),pow(pow(histo[j][nc].GetBinError(histo[j][nc].GetNbinsX()),2)+pow(histo[j][nc].GetBinError(histo[j][nc].GetNbinsX()+1),2),0.5))
            histo[j][nc].SetBinContent(histo[j][nc].GetNbinsX()+1,0.0)
            histo[j][nc].SetBinError  (histo[j][nc].GetNbinsX()+1,0.0)

            histo[j][nc].Write()

        for j in range(nHisto):
            if(histo2D[j][nc] == 0): continue

            for i in range(histo2D[j][nc].GetNbinsX()):
               histo2D[j][nc].SetBinContent(i+1,histo2D[j][nc].GetNbinsY(),histo2D[j][nc].GetBinContent(i+1,histo2D[j][nc].GetNbinsY())+histo2D[j][nc].GetBinContent(i+1,histo2D[j][nc].GetNbinsY()+1))
               histo2D[j][nc].SetBinError  (i+1,histo2D[j][nc].GetNbinsY(),pow(pow(histo2D[j][nc].GetBinError(i+1,histo2D[j][nc].GetNbinsY()),2)+pow(histo2D[j][nc].GetBinError(i+1,histo2D[j][nc].GetNbinsY()+1),2),0.5))
               histo2D[j][nc].SetBinContent(i+1,histo2D[j][nc].GetNbinsY()+1,0.0)
               histo2D[j][nc].SetBinError  (i+1,histo2D[j][nc].GetNbinsY()+1,0.0)

            for i in range(histo2D[j][nc].GetNbinsY()):
               histo2D[j][nc].SetBinContent(histo2D[j][nc].GetNbinsX(),i+1,histo2D[j][nc].GetBinContent(histo2D[j][nc].GetNbinsX(),i+1)+histo2D[j][nc].GetBinContent(histo2D[j][nc].GetNbinsX()+1,i+1))
               histo2D[j][nc].SetBinError  (histo2D[j][nc].GetNbinsX(),i+1,pow(pow(histo2D[j][nc].GetBinError(histo2D[j][nc].GetNbinsX(),i+1),2)+pow(histo2D[j][nc].GetBinError(histo2D[j][nc].GetNbinsX()+1,i+1),2),0.5))
               histo2D[j][nc].SetBinContent(histo2D[j][nc].GetNbinsX()+1,i+1,0.0)
               histo2D[j][nc].SetBinError  (histo2D[j][nc].GetNbinsX()+1,i+1,0.0)

            histo2D[j][nc].Write()

    myfile.Close()

    print("ending {0} / {1} / {2} / {3} / {4} / {5}".format(count,category,weight,year,PDType,isData))

def readMCSample(sampleNOW, year, PDType, skimType, histo_wwpt):

    files = getMClist(sampleNOW, skimType)
    print("Total files: {0}".format(len(files)))

    df = ROOT.RDataFrame("Events", files)

    runTree = ROOT.TChain("Runs")
    for f in range(len(files)):
        runTree.AddFile(files[f])

    genEventSumWeight = 0
    genEventSumNoWeight = 0
    nTheoryReplicas = [103, 9, 4]
    genEventSumLHEScaleWeight = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    genEventSumPSWeight = [0, 0, 0, 0, 0]
    for i in range(runTree.GetEntries()):
        runTree.GetEntry(i)
        genEventSumWeight += runTree.genEventSumw
        genEventSumNoWeight += runTree.genEventCount
        if(runTree.FindBranch("nLHEPdfSumw") and runTree.nLHEPdfSumw < nTheoryReplicas[0]):
            nTheoryReplicas[0] = runTree.nLHEPdfSumw
        for n in range(9):
            if(n < runTree.nLHEScaleSumw):
                genEventSumLHEScaleWeight[n] += runTree.LHEScaleSumw[n]
            else:
                genEventSumLHEScaleWeight[n] += 1.0
                nTheoryReplicas[1] = runTree.nLHEScaleSumw
        for n in range(4):
            if(runTree.FindBranch("nPSSumw")):
                if(n < runTree.nPSSumw):
                    genEventSumPSWeight[n] += runTree.PSSumw[n]
                else:
                    genEventSumPSWeight[n] += 1.0
                    nTheoryReplicas[2] = runTree.nPSSumw
            else:
                genEventSumPSWeight[n] += 1.0
            genEventSumPSWeight[4] += 1
    print("Number of Theory replicas: {0} / {1} / {2}".format(nTheoryReplicas[0],nTheoryReplicas[1],nTheoryReplicas[2]))

    genEventSumLHEScaleRenorm = [1, 1, 1, 1, 1, 1]
    genEventSumPSRenorm = [1, 1, 1, 1]
    if(0):
        genEventSumLHEScaleRenorm[0] = genEventSumLHEScaleWeight[0] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[1] = genEventSumLHEScaleWeight[1] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[2] = genEventSumLHEScaleWeight[3] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[3] = genEventSumLHEScaleWeight[5] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[4] = genEventSumLHEScaleWeight[7] / genEventSumLHEScaleWeight[4]
        genEventSumLHEScaleRenorm[5] = genEventSumLHEScaleWeight[8] / genEventSumLHEScaleWeight[4]
        for n in range(4):
            genEventSumPSRenorm[n] = genEventSumPSWeight[n] / genEventSumPSWeight[4]
    print("genEventSumLHEScaleRenorm: ",genEventSumLHEScaleRenorm)
    print("genEventSumPSRenorm: ",genEventSumPSRenorm)

    weight = (SwitchSample(sampleNOW, skimType)[1] / genEventSumWeight)*getLumi(year)
    weightApprox = (SwitchSample(sampleNOW, skimType)[1] / genEventSumNoWeight)*getLumi(year)

    nevents = df.Count().GetValue()

    print("genEventSum({0}): {1} / Events(total/ntuple): {2} / {3}".format(runTree.GetEntries(),genEventSumWeight,genEventSumNoWeight,nevents))
    print("WeightExact/Approx %f / %f / Cross section: %f" %(weight, weightApprox, SwitchSample(sampleNOW, skimType)[1]))

    analysis(df, sampleNOW, SwitchSample(sampleNOW,skimType)[2], weight, year, PDType, "false",histo_wwpt,nTheoryReplicas,genEventSumLHEScaleRenorm,genEventSumPSRenorm)

if __name__ == "__main__":

    year = 2022
    process = 399
    skimType = "2l"

    valid = ['year=', "process=", 'help']
    usage  =  "Usage: ana.py --year=<{0}>\n".format(year)
    usage +=  "              --process=<{0}>".format(process)
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
        if opt == "--year":
            year = int(arg)
        if opt == "--process":
            process = int(arg)

    histo_wwpt = []
    fPtwwWeightPath = ROOT.TFile("data/MyRatioWWpTHistogramAll.root")
    histo_wwpt.append(fPtwwWeightPath.Get("wwpt"))
    histo_wwpt.append(fPtwwWeightPath.Get("wwpt_scaleup"))
    histo_wwpt.append(fPtwwWeightPath.Get("wwpt_scaledown"))
    histo_wwpt.append(fPtwwWeightPath.Get("wwpt_resumup"))
    histo_wwpt.append(fPtwwWeightPath.Get("wwpt_resumdown"))
    for x in range(5):
        histo_wwpt[x].SetDirectory(0)
    fPtwwWeightPath.Close()

    try:
        readMCSample(process,year,"All", skimType, histo_wwpt)
    except Exception as e:
        print("FAILED {0}".format(e))

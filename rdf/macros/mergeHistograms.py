import ROOT
from ROOT import TFile, TH1D, TH2D
import os, sys, getopt, glob
from utilsAna import plotCategory

path = "fillhistoZAna"
year = 2018
output = "anaZ"

valid = ['path=', "year=", 'output=', 'help']
usage  =  "Usage: ana.py --path=<{0}>\n".format(path)
usage +=  "		 --year=<{0}>".format(year)
usage +=  "		 --output=<{0}>".format(output)
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

paths_to_watch = path + "_sample*_year" + str(year) + ".root"
print("paths_to_watch: {0}".format(paths_to_watch))
inputDataFolders = glob.glob(paths_to_watch)
print(inputDataFolders)

nCat, nHisto = plotCategory("kPlotCategories"), 100

myfile = [0 for x in range(len(inputDataFolders))]
for nf in range(len(inputDataFolders)):
  myfile[nf] = TFile(inputDataFolders[nf])

if(not os.path.exists(output)):
     os.makedirs(output)
 
for nh in range(nHisto):
    histo = [0 for x in range(nCat)]
    for nc in range(nCat):
        histo[nc] = myfile[0].Get("histo_{0}_{1}".format(nh,nc))
        for nf in range(1,len(inputDataFolders)):
	    if(histo[nc]):
	        histo[nc].Add(myfile[nf].Get("histo_{0}_{1}".format(nh,nc)))

    if(histo[0]):
        outputFileName = "{0}/{1}_{2}_{3}.root".format(output,os.path.basename(path),year,nh)
        print("Making {0}".format(outputFileName))
        outputFile = TFile(outputFileName, "RECREATE")
	outputFile.cd()
        for nc in range(nCat):
            histo[nc].SetNameTitle("histo{0}".format(nc),"histo{0}".format(nc))
	    histo[nc].Write();
	outputFile.Close()

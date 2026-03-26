import ROOT
import os, sys, getopt, json, time, subprocess, socket
import fnmatch
import math


if __name__ == "__main__":

    years = [20220, 20221, 20230, 20231, 20240, 20250]
    wzPOW = [103, 203, 303, 403, 503, 503]
    zzPOW = [107, 207, 307, 407, 507, 507]
    wzMG  = [179, 279, 379, 479, 579, 579]
    zzMG  = [183, 283, 383, 483, 583, 583]

    wwNoPol  = [176, 276, 376, 476, 576, 576]
    wwPolLL  = [150, 250, 350, 450, 550, 550]
    wwPolLT  = [151, 251, 351, 451, 551, 551]
    wwPolTT  = [152, 252, 352, 452, 552, 552]

    inputCfg = "Analysis_input_condor_jobs.cfg"
    ana  = "zz"
    isWZMG = 1
    isZZMG = 1
    isWWPol = 0
    inputFolder = "."

    valid = ['outputDir=', "ana=", "isWZMG=", "isZZMG=", "isWWPol=", "inputFolder=", 'help']
    usage  =  "Usage: ana.py --ana=<{0}>\n".format(ana)
    usage +=  "              --isWZMG=<{0}>\n".format(isWZMG)
    usage +=  "              --isZZMG=<{0}>\n".format(isZZMG)
    usage +=  "              --isWWPol=<{0}>\n".format(isWWPol)
    usage +=  "              --inputFolder=<{0}>".format(inputFolder)
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
        if opt == "--ana":
            ana = str(arg)
        if opt == "--isWZMG":
            isWZMG = int(arg)
        if opt == "--isZZMG":
            isZZMG = int(arg)
        if opt == "--isWWPol":
            isWWPol = int(arg)
        if opt == "--inputFolder":
            inputFolder = str(arg)

    if(isWWPol == 1):
        isWZMG = 1
        isZZMG = 1

    inputSamplesCfg = inputFolder + "/" + ana + inputCfg
    if(not os.path.exists(inputSamplesCfg)):
        print("File {0} does not exist".format(inputSamplesCfg))
        sys.exit(1)

    outputSamplesCfg = inputSamplesCfg.replace(".cfg","_new.cfg")
    outputSamplesFile = open(outputSamplesCfg, 'w')

    for x in range(len(years)):
        if(isWZMG == 1):
            outputSamplesFile.write("{0} {1}\n".format(wzMG[x],years[x]))
        else:
            outputSamplesFile.write("{0} {1}\n".format(wzPOW[x],years[x]))

        if(isZZMG == 1):
            outputSamplesFile.write("{0} {1}\n".format(zzMG[x],years[x]))
        else:
            outputSamplesFile.write("{0} {1}\n".format(zzPOW[x],years[x]))

        if(isWWPol == 1):
            outputSamplesFile.write("{0} {1}\n".format(wwPolLL[x],years[x]))
            outputSamplesFile.write("{0} {1}\n".format(wwPolLT[x],years[x]))
            outputSamplesFile.write("{0} {1}\n".format(wwPolTT[x],years[x]))
        else:
            outputSamplesFile.write("{0} {1}\n".format(wwNoPol[x],years[x]))

    inputSamplesFile = open(inputSamplesCfg, 'r')
    while True:
        lineFull  = inputSamplesFile.readline().strip()
        lineSplit = lineFull.split()

        if not lineFull:
            break

        goodLine = True
        for x in range(len(years)):
            # Must remove all vvMG and vvPOW and ww*Pol* lines
            if  (wzMG[x]  == int(lineSplit[0])): goodLine = False
            elif(zzMG[x]  == int(lineSplit[0])): goodLine = False
            elif(wzPOW[x] == int(lineSplit[0])): goodLine = False
            elif(zzPOW[x] == int(lineSplit[0])): goodLine = False
            elif(wwPolLL[x] == int(lineSplit[0])): goodLine = False
            elif(wwPolLT[x] == int(lineSplit[0])): goodLine = False
            elif(wwPolTT[x] == int(lineSplit[0])): goodLine = False
            elif(wwNoPol[x] == int(lineSplit[0])): goodLine = False

        if(goodLine == False):
            continue
        #print(lineFull)
        outputSamplesFile.write(lineFull+"\n")

    outputSamplesFile.close()

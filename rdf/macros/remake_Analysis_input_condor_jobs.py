import ROOT
import os, sys, getopt, json, time, subprocess, socket
import fnmatch
import math


if __name__ == "__main__":

    years = [20220, 20221, 20230, 20231, 20240]
    wzPOW = ["103 ", "203 ", "303 ", "403 ", "503 "]
    zzPOW = ["107 ", "207 ", "307 ", "407 ", "507 "]
    wzMG  = ["179 ", "279 ", "379 ", "479 ", "579 "]
    zzMG  = ["183 ", "283 ", "383 ", "483 ", "583 "]

    inputCfg = "Analysis_input_condor_jobs.cfg"
    ana  = "zz"
    isWZMG = 1
    isZZMG = 1
    inputFolder = "."

    valid = ['outputDir=', "ana=", "isWZMG=", "isZZMG=", "inputFolder=", 'help']
    usage  =  "Usage: ana.py --ana=<{0}>\n".format(ana)
    usage +=  "              --isWZMG=<{0}>\n".format(isWZMG)
    usage +=  "              --isZZMG=<{0}>\n".format(isZZMG)
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
        if opt == "--inputFolder":
            inputFolder = str(arg)

    inputSamplesCfg = inputFolder + "/" + ana + inputCfg
    if(not os.path.exists(inputSamplesCfg)):
        print("File {0} does not exist".format(inputSamplesCfg))
        sys.exit(1)

    outputSamplesCfg = inputSamplesCfg.replace(".cfg","_new.cfg")
    outputSamplesFile = open(outputSamplesCfg, 'w')

    inputSamplesFile = open(inputSamplesCfg, 'r')
    while True:
        line = inputSamplesFile.readline().strip()
        if not line:
            break
        goodLine = True
        for x in range(len(years)):
            if  (isWZMG == 0 and wzMG[x]  in line): goodLine = False
            elif(isZZMG == 0 and zzMG[x]  in line): goodLine = False
            elif(isWZMG == 1 and wzPOW[x] in line): goodLine = False
            elif(isZZMG == 1 and zzPOW[x] in line): goodLine = False
        if(goodLine == False):
            continue
        print(line)
        outputSamplesFile.write(line+"\n")

    for x in range(len(years)):
        if(isWZMG == 1):
            outputSamplesFile.write("{0}{1}\n".format(wzMG[x],years[x]))
        else:
            outputSamplesFile.write("{0}{1}\n".format(wzPOW[x],years[x]))

        if(isZZMG == 1):
            outputSamplesFile.write("{0}{1}\n".format(zzMG[x],years[x]))
        else:
            outputSamplesFile.write("{0}{1}\n".format(zzPOW[x],years[x]))

    outputSamplesFile.close()

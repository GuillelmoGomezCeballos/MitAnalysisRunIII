import os, sys, getopt, time

if __name__ == "__main__":

    outputDir = "/mnt/T3_US_MIT/hadoop/scratch/ceballos/nanoaod/skims_submit"
    outputForCondorCfg = "skim_input_condor_jobs.cfg"
    missingFilesCfg = "skim_input_condor_missing_jobs.cfg"
    debug = 0

    valid = ['outputDir=', "outputForCondorCfg=", "missingFilesCfg=", "debug=", "help"]
    usage  =  "Usage: ana.py --outputDir=<{0}>\n".format(outputDir)
    usage +=  "              --outputForCondorCfg=<{0}>\n".format(outputForCondorCfg)
    usage +=  "              --missingFilesCfg=<{0}>\n".format(missingFilesCfg)
    usage +=  "              --debug=<{0}>".format(debug)
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
        if opt == "--outputDir":
            outputDir = str(arg)
        if opt == "--outputForCondorCfg":
            outputForCondorCfg = str(arg)
        if opt == "--missingFilesCfg":
            missingFilesCfg = str(arg)
        if opt == "--debug":
            debug = int(arg)

    missingFile = open(missingFilesCfg, 'w')

    countMissingFiles = [0, 0, 0, 0]
    outputFile = open(outputForCondorCfg, 'r')
    while True:
        lineRaw = outputFile.readline()
        line = lineRaw.strip().split(None, 4)
        if not line:
            break

        isMissingFile = [True, True, True]
        # 1l
        fileNameA = os.path.join(outputDir, "1l", line[3], "output_1l_{0}.root".format(line[1]))
        fileNameB = os.path.join(outputDir, "1l", line[3], "output_1l_{0}_{1}.root".format(line[0],line[1]))
        fileNameC = os.path.join(outputDir, "1l", line[3], "output_1l_{0}_{1}.txt".format(line[0],line[1]))

        if((os.path.exists(fileNameA) and os.path.getsize(fileNameA) > 1000) or
           (os.path.exists(fileNameB) and os.path.getsize(fileNameB) > 1000)):
            isMissingFile[0] = False
        else:
            countMissingFiles[0] += 1
            if(debug == 1): print(fileNameB)

        # 2l
        fileNameA = os.path.join(outputDir, "2l", line[3], "output_2l_{0}.root".format(line[1]))
        fileNameB = os.path.join(outputDir, "2l", line[3], "output_2l_{0}_{1}.root".format(line[0],line[1]))
        fileNameC = os.path.join(outputDir, "2l", line[3], "output_2l_{0}_{1}.txt".format(line[0],line[1]))

        if((os.path.exists(fileNameA) and os.path.getsize(fileNameA) > 1000) or
           (os.path.exists(fileNameB) and os.path.getsize(fileNameB) > 1000)):
            isMissingFile[1] = False
        else:
            countMissingFiles[1] += 1
            if(debug == 1): print(fileNameB)

        # 3l
        fileNameA = os.path.join(outputDir, "3l", line[3], "output_3l_{0}.root".format(line[1]))
        fileNameB = os.path.join(outputDir, "3l", line[3], "output_3l_{0}_{1}.root".format(line[0],line[1]))
        fileNameC = os.path.join(outputDir, "3l", line[3], "output_3l_{0}_{1}.txt".format(line[0],line[1]))

        if((os.path.exists(fileNameA) and os.path.getsize(fileNameA) > 1000) or
           (os.path.exists(fileNameB) and os.path.getsize(fileNameB) > 1000)):
            isMissingFile[2] = False
        else:
            countMissingFiles[2] += 1
            if(debug == 1): print(fileNameB)

        if(isMissingFile[0] == True or isMissingFile[1] == True or isMissingFile[2] == True):
            missingFile.writelines(lineRaw)
            countMissingFiles[3] += 1

    missingFile.close()

    print("missingFiles: {0} / {1} / {2} / {3}".format(countMissingFiles[0],countMissingFiles[1],countMissingFiles[2],countMissingFiles[3]))
    os.system("wc {0};wc {1}".format(outputForCondorCfg,missingFilesCfg))

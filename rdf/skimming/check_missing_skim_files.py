import os, sys, getopt, time

if __name__ == "__main__":

    outputDir = "/mnt/T3_US_MIT/hadoop/scratch/ceballos/nanoaod/Skims"
    outputForCondorCfg = "skim_input_condor_jobs.cfg"
    missingFilesCfg = "skim_input_condor_missing_jobs.cfg"

    valid = ['outputDir=', "outputForCondorCfg=", "missingFilesCfg=", 'help']
    usage  =  "Usage: ana.py --outputDir=<{0}>\n".format(outputDir)
    usage +=  "              --outputForCondorCfg=<{0}>\n".format(outputForCondorCfg)
    usage +=  "              --missingFilesCfg=<{0}>".format(missingFilesCfg)
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

    missingFile = open(missingFilesCfg, 'w')

    countSamples = 0
    outputFile = open(outputForCondorCfg, 'r')
    while True:
        lineRaw = outputFile.readline()
        line = lineRaw.strip().split(None, 4)
        if not line:
            break
        fileName1 = os.path.join(outputDir, "1l", line[3], "output_1l_{0}.root".format(line[1]))
        fileName2 = os.path.join(outputDir, "2l", line[3], "output_2l_{0}.root".format(line[1]))
        fileName3 = os.path.join(outputDir, "3l", line[3], "output_3l_{0}.root".format(line[1]))
	isMissingFile = False
	if  (not(os.path.exists(fileName1) and os.path.getsize(fileName1) > 0)): isMissingFile = True
	elif(not(os.path.exists(fileName2) and os.path.getsize(fileName2) > 0)): isMissingFile = True
	elif(not(os.path.exists(fileName3) and os.path.getsize(fileName3) > 0)): isMissingFile = True
        if(isMissingFile == True):
            missingFile.writelines(lineRaw)

    missingFile.close()

    os.system("wc {0};wc {1}".format(outputForCondorCfg,missingFilesCfg))

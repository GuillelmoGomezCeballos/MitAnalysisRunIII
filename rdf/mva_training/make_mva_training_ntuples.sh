#/bin/sh

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

if [ $1 = "00" ]; then

cp zAnalysis.py zAnalysis_without_ntuples.py
sed -i 's/doNtuples = False/doNtuples = True/' zAnalysis.py

nohup ./analysis_slurm.sh 1001 20220 -1 1001 zAnalysis >& logz_01&
nohup ./analysis_slurm.sh 1002 20220 -1 1001 zAnalysis >& logz_02&
nohup ./analysis_slurm.sh 1011 20220 -1 1001 zAnalysis >& logz_03&
nohup ./analysis_slurm.sh 1012 20220 -1 1001 zAnalysis >& logz_04&
nohup ./analysis_slurm.sh 1021 20220 -1 1001 zAnalysis >& logz_05&
nohup ./analysis_slurm.sh 1022 20220 -1 1001 zAnalysis >& logz_06&
nohup ./analysis_slurm.sh 1023 20220 -1 1001 zAnalysis >& logz_07&
nohup ./analysis_slurm.sh 1031 20220 -1 1001 zAnalysis >& logz_08&
nohup ./analysis_slurm.sh 1032 20220 -1 1001 zAnalysis >& logz_09&
nohup ./analysis_slurm.sh 1033 20220 -1 1001 zAnalysis >& logz_10&
nohup ./analysis_slurm.sh 1042 20220 -1 1001 zAnalysis >& logz_11&
nohup ./analysis_slurm.sh 1043 20220 -1 1001 zAnalysis >& logz_12&
nohup ./analysis_slurm.sh 1024 20221 -1 1001 zAnalysis >& logz_13&
nohup ./analysis_slurm.sh 1025 20221 -1 1001 zAnalysis >& logz_14&
nohup ./analysis_slurm.sh 1026 20221 -1 1001 zAnalysis >& logz_15&
nohup ./analysis_slurm.sh 1034 20221 -1 1001 zAnalysis >& logz_16&
nohup ./analysis_slurm.sh 1035 20221 -1 1001 zAnalysis >& logz_17&
nohup ./analysis_slurm.sh 1036 20221 -1 1001 zAnalysis >& logz_18&
nohup ./analysis_slurm.sh 1044 20221 -1 1001 zAnalysis >& logz_19&
nohup ./analysis_slurm.sh 1045 20221 -1 1001 zAnalysis >& logz_20&
nohup ./analysis_slurm.sh 1046 20221 -1 1001 zAnalysis >& logz_21&
nohup ./analysis_slurm.sh 1022 20230 -1 1001 zAnalysis >& logz_22&
nohup ./analysis_slurm.sh 1032 20230 -1 1001 zAnalysis >& logz_23&
nohup ./analysis_slurm.sh 1042 20230 -1 1001 zAnalysis >& logz_24&
nohup ./analysis_slurm.sh 1023 20231 -1 1001 zAnalysis >& logz_25&
nohup ./analysis_slurm.sh 1033 20231 -1 1001 zAnalysis >& logz_26&
nohup ./analysis_slurm.sh 1043 20231 -1 1001 zAnalysis >& logz_27&

elif [ $1 = "01" ]; then

cp zAnalysis.py zAnalysis_without_ntuples.py
sed -i 's/doNtuples = False/doNtuples = True/' zAnalysis.py

nohup ./analysis_slurm.sh 1022 20240 -1 1001 zAnalysis >& logz_28&
nohup ./analysis_slurm.sh 1023 20240 -1 1001 zAnalysis >& logz_29&
nohup ./analysis_slurm.sh 1024 20240 -1 1001 zAnalysis >& logz_30&
nohup ./analysis_slurm.sh 1025 20240 -1 1001 zAnalysis >& logz_31&
nohup ./analysis_slurm.sh 1026 20240 -1 1001 zAnalysis >& logz_32&
nohup ./analysis_slurm.sh 1027 20240 -1 1001 zAnalysis >& logz_33&
nohup ./analysis_slurm.sh 1028 20240 -1 1001 zAnalysis >& logz_34&
nohup ./analysis_slurm.sh 1032 20240 -1 1001 zAnalysis >& logz_35&
nohup ./analysis_slurm.sh 1033 20240 -1 1001 zAnalysis >& logz_36&
nohup ./analysis_slurm.sh 1034 20240 -1 1001 zAnalysis >& logz_37&
nohup ./analysis_slurm.sh 1035 20240 -1 1001 zAnalysis >& logz_38&
nohup ./analysis_slurm.sh 1036 20240 -1 1001 zAnalysis >& logz_39&
nohup ./analysis_slurm.sh 1037 20240 -1 1001 zAnalysis >& logz_40&
nohup ./analysis_slurm.sh 1038 20240 -1 1001 zAnalysis >& logz_41&
nohup ./analysis_slurm.sh 1042 20240 -1 1001 zAnalysis >& logz_42&
nohup ./analysis_slurm.sh 1043 20240 -1 1001 zAnalysis >& logz_43&
nohup ./analysis_slurm.sh 1044 20240 -1 1001 zAnalysis >& logz_44&
nohup ./analysis_slurm.sh 1045 20240 -1 1001 zAnalysis >& logz_45&
nohup ./analysis_slurm.sh 1046 20240 -1 1001 zAnalysis >& logz_46&
nohup ./analysis_slurm.sh 1047 20240 -1 1001 zAnalysis >& logz_47&
nohup ./analysis_slurm.sh 1048 20240 -1 1001 zAnalysis >& logz_48&
#nohup ./analysis_slurm.sh 1021 20250 -1 1001 zAnalysis >& logz_49&
#nohup ./analysis_slurm.sh 1022 20250 -1 1001 zAnalysis >& logz_50&
#nohup ./analysis_slurm.sh 1023 20250 -1 1001 zAnalysis >& logz_51&
#nohup ./analysis_slurm.sh 1024 20250 -1 1001 zAnalysis >& logz_52&
#nohup ./analysis_slurm.sh 1025 20250 -1 1001 zAnalysis >& logz_53&
#nohup ./analysis_slurm.sh 1026 20250 -1 1001 zAnalysis >& logz_54&
#nohup ./analysis_slurm.sh 1031 20250 -1 1001 zAnalysis >& logz_55&
#nohup ./analysis_slurm.sh 1032 20250 -1 1001 zAnalysis >& logz_56&
#nohup ./analysis_slurm.sh 1033 20250 -1 1001 zAnalysis >& logz_57&
#nohup ./analysis_slurm.sh 1034 20250 -1 1001 zAnalysis >& logz_58&
#nohup ./analysis_slurm.sh 1035 20250 -1 1001 zAnalysis >& logz_59&
#nohup ./analysis_slurm.sh 1036 20250 -1 1001 zAnalysis >& logz_60&
#nohup ./analysis_slurm.sh 1041 20250 -1 1001 zAnalysis >& logz_61&
#nohup ./analysis_slurm.sh 1042 20250 -1 1001 zAnalysis >& logz_62&
#nohup ./analysis_slurm.sh 1043 20250 -1 1001 zAnalysis >& logz_63&
#nohup ./analysis_slurm.sh 1044 20250 -1 1001 zAnalysis >& logz_64&
#nohup ./analysis_slurm.sh 1045 20250 -1 1001 zAnalysis >& logz_65&
#nohup ./analysis_slurm.sh 1046 20250 -1 1001 zAnalysis >& logz_66&

elif [ $1 = "1" ]; then

cp wzAnalysis.py wzAnalysis_without_ntuples.py
sed -i 's/doNtuples = False/doNtuples = True/' wzAnalysis.py

nohup ./analysis_slurm.sh 103 20220 -1 1001 wzAnalysis >& logwz_00&
nohup ./analysis_slurm.sh 149 20220 -1 1001 wzAnalysis >& logwz_01&
nohup ./analysis_slurm.sh 178 20220 -1 1001 wzAnalysis >& logwz_02&
nohup ./analysis_slurm.sh 179 20220 -1 1001 wzAnalysis >& logwz_03&
nohup ./analysis_slurm.sh 203 20221 -1 1001 wzAnalysis >& logwz_04&
nohup ./analysis_slurm.sh 249 20221 -1 1001 wzAnalysis >& logwz_05&
nohup ./analysis_slurm.sh 278 20221 -1 1001 wzAnalysis >& logwz_06&
nohup ./analysis_slurm.sh 279 20221 -1 1001 wzAnalysis >& logwz_07&
nohup ./analysis_slurm.sh 303 20230 -1 1001 wzAnalysis >& logwz_08&
nohup ./analysis_slurm.sh 349 20230 -1 1001 wzAnalysis >& logwz_09&
nohup ./analysis_slurm.sh 378 20230 -1 1001 wzAnalysis >& logwz_10&
nohup ./analysis_slurm.sh 379 20230 -1 1001 wzAnalysis >& logwz_11&
nohup ./analysis_slurm.sh 403 20231 -1 1001 wzAnalysis >& logwz_12&
nohup ./analysis_slurm.sh 449 20231 -1 1001 wzAnalysis >& logwz_13&
nohup ./analysis_slurm.sh 478 20231 -1 1001 wzAnalysis >& logwz_14&
nohup ./analysis_slurm.sh 479 20231 -1 1001 wzAnalysis >& logwz_15&
nohup ./analysis_slurm.sh 503 20240 -1 1001 wzAnalysis >& logwz_16&
nohup ./analysis_slurm.sh 549 20240 -1 1001 wzAnalysis >& logwz_17&
nohup ./analysis_slurm.sh 578 20240 -1 1001 wzAnalysis >& logwz_18&
nohup ./analysis_slurm.sh 579 20240 -1 1001 wzAnalysis >& logwz_19&

elif [ $1 = "3" ]; then

cp sswwAnalysis.py sswwAnalysis_without_ntuples.py
sed -i 's/doNtuples = False/doNtuples = True/' sswwAnalysis.py

nohup ./analysis_slurm.sh 103 20220 -1 1001 sswwAnalysis >& logssww_00&
nohup ./analysis_slurm.sh 176 20220 -1 1001 sswwAnalysis >& logssww_01&
nohup ./analysis_slurm.sh 177 20220 -1 1001 sswwAnalysis >& logssww_02&
nohup ./analysis_slurm.sh 178 20220 -1 1001 sswwAnalysis >& logssww_03&
nohup ./analysis_slurm.sh 179 20220 -1 1001 sswwAnalysis >& logssww_04&
nohup ./analysis_slurm.sh 203 20221 -1 1001 sswwAnalysis >& logssww_05&
nohup ./analysis_slurm.sh 276 20221 -1 1001 sswwAnalysis >& logssww_06&
nohup ./analysis_slurm.sh 277 20221 -1 1001 sswwAnalysis >& logssww_07&
nohup ./analysis_slurm.sh 278 20221 -1 1001 sswwAnalysis >& logssww_08&
nohup ./analysis_slurm.sh 279 20221 -1 1001 sswwAnalysis >& logssww_09&
nohup ./analysis_slurm.sh 303 20230 -1 1001 sswwAnalysis >& logssww_10&
nohup ./analysis_slurm.sh 376 20230 -1 1001 sswwAnalysis >& logssww_11&
nohup ./analysis_slurm.sh 377 20230 -1 1001 sswwAnalysis >& logssww_12&
nohup ./analysis_slurm.sh 378 20230 -1 1001 sswwAnalysis >& logssww_13&
nohup ./analysis_slurm.sh 379 20230 -1 1001 sswwAnalysis >& logssww_14&
nohup ./analysis_slurm.sh 403 20231 -1 1001 sswwAnalysis >& logssww_15&
nohup ./analysis_slurm.sh 476 20231 -1 1001 sswwAnalysis >& logssww_16&
nohup ./analysis_slurm.sh 477 20231 -1 1001 sswwAnalysis >& logssww_17&
nohup ./analysis_slurm.sh 478 20231 -1 1001 sswwAnalysis >& logssww_18&
nohup ./analysis_slurm.sh 479 20231 -1 1001 sswwAnalysis >& logssww_19&
nohup ./analysis_slurm.sh 503 20240 -1 1001 sswwAnalysis >& logssww_20&
nohup ./analysis_slurm.sh 576 20240 -1 1001 sswwAnalysis >& logssww_21&
nohup ./analysis_slurm.sh 577 20240 -1 1001 sswwAnalysis >& logssww_22&
nohup ./analysis_slurm.sh 578 20240 -1 1001 sswwAnalysis >& logssww_23&
nohup ./analysis_slurm.sh 579 20240 -1 1001 sswwAnalysis >& logssww_24&

nohup ./analysis_slurm.sh 150 20220 -1 1001 sswwAnalysis >& logssww_200&
nohup ./analysis_slurm.sh 151 20220 -1 1001 sswwAnalysis >& logssww_201&
nohup ./analysis_slurm.sh 152 20220 -1 1001 sswwAnalysis >& logssww_202&
nohup ./analysis_slurm.sh 250 20221 -1 1001 sswwAnalysis >& logssww_203&
nohup ./analysis_slurm.sh 251 20221 -1 1001 sswwAnalysis >& logssww_204&
nohup ./analysis_slurm.sh 252 20221 -1 1001 sswwAnalysis >& logssww_205&
nohup ./analysis_slurm.sh 350 20230 -1 1001 sswwAnalysis >& logssww_206&
nohup ./analysis_slurm.sh 351 20230 -1 1001 sswwAnalysis >& logssww_207&
nohup ./analysis_slurm.sh 352 20230 -1 1001 sswwAnalysis >& logssww_208&
nohup ./analysis_slurm.sh 450 20231 -1 1001 sswwAnalysis >& logssww_209&
nohup ./analysis_slurm.sh 451 20231 -1 1001 sswwAnalysis >& logssww_210&
nohup ./analysis_slurm.sh 452 20231 -1 1001 sswwAnalysis >& logssww_211&
nohup ./analysis_slurm.sh 550 20240 -1 1001 sswwAnalysis >& logssww_212&
nohup ./analysis_slurm.sh 551 20240 -1 1001 sswwAnalysis >& logssww_213&
nohup ./analysis_slurm.sh 552 20240 -1 1001 sswwAnalysis >& logssww_214&

elif [ $1 = "10" ]; then

mv wzAnalysis_without_ntuples.py wzAnalysis.py
mv sswwAnalysis_without_ntuples.py sswwAnalysis.py
hadd -f /work/submit/ceballos/mva_samples/ntupleWWPolAna_year2027.root ntupleSSWWAna_sample?5*root
rm -f ntupleSSWWAna_sample?5*.root
hadd -f /work/submit/ceballos/mva_samples/ntupleWZAna_year2027.root ntupleWZAna_*.root
rm -f ntupleWZAna_*.root
hadd -f /work/submit/ceballos/mva_samples/ntupleWWAna_year2027.root ntupleSSWWAna_*.root
rm -f ntupleSSWWAna_*.root

elif [ $1 = "11" ]; then

mv zAnalysis_without_ntuples.py zAnalysis.py
hadd -f /work/submit/ceballos/mva_samples/ntupleZAna_ltype0_year2027.root ntupleZAna_sample*_ltype0_*.root
hadd -f /work/submit/ceballos/mva_samples/ntupleZAna_ltype1_year2027.root ntupleZAna_sample*_ltype1_*.root
hadd -f /work/submit/ceballos/mva_samples/ntupleZAna_ltype2_year2027.root ntupleZAna_sample*_ltype2_*.root

fi

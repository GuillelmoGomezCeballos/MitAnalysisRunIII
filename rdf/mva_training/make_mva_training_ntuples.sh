#/bin/sh

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

if [ $1 = "1" ]; then

cp wzAnalysis.py wzAnalysis_with_ntuples.py
sed -i 's/doNtuples = False/doNtuples = True/' wzAnalysis.py
sed -i 's/useFR = 1/useFR = 0/' wzAnalysis.py

nohup ./analysis_slurm.sh 103 20220 -1 1001 wzAnalysis >& logwz_00&
nohup ./analysis_slurm.sh 108 20220 -1 1001 wzAnalysis >& logwz_01&
nohup ./analysis_slurm.sh 149 20220 -1 1001 wzAnalysis >& logwz_02&
nohup ./analysis_slurm.sh 178 20220 -1 1001 wzAnalysis >& logwz_03&
nohup ./analysis_slurm.sh 179 20220 -1 1001 wzAnalysis >& logwz_04&
nohup ./analysis_slurm.sh 203 20221 -1 1001 wzAnalysis >& logwz_05&
nohup ./analysis_slurm.sh 208 20221 -1 1001 wzAnalysis >& logwz_06&
nohup ./analysis_slurm.sh 249 20221 -1 1001 wzAnalysis >& logwz_07&
nohup ./analysis_slurm.sh 278 20221 -1 1001 wzAnalysis >& logwz_08&
nohup ./analysis_slurm.sh 279 20221 -1 1001 wzAnalysis >& logwz_09&
nohup ./analysis_slurm.sh 303 20230 -1 1001 wzAnalysis >& logwz_10&
nohup ./analysis_slurm.sh 308 20230 -1 1001 wzAnalysis >& logwz_11&
nohup ./analysis_slurm.sh 349 20230 -1 1001 wzAnalysis >& logwz_12&
nohup ./analysis_slurm.sh 378 20230 -1 1001 wzAnalysis >& logwz_13&
nohup ./analysis_slurm.sh 379 20230 -1 1001 wzAnalysis >& logwz_14&
nohup ./analysis_slurm.sh 403 20231 -1 1001 wzAnalysis >& logwz_15&
nohup ./analysis_slurm.sh 408 20231 -1 1001 wzAnalysis >& logwz_16&
nohup ./analysis_slurm.sh 449 20231 -1 1001 wzAnalysis >& logwz_17&
nohup ./analysis_slurm.sh 478 20231 -1 1001 wzAnalysis >& logwz_18&
nohup ./analysis_slurm.sh 479 20231 -1 1001 wzAnalysis >& logwz_19&
nohup ./analysis_slurm.sh 503 20240 -1 1001 wzAnalysis >& logwz_20&
nohup ./analysis_slurm.sh 508 20240 -1 1001 wzAnalysis >& logwz_21&
nohup ./analysis_slurm.sh 549 20240 -1 1001 wzAnalysis >& logwz_22&
nohup ./analysis_slurm.sh 578 20240 -1 1001 wzAnalysis >& logwz_23&
nohup ./analysis_slurm.sh 579 20240 -1 1001 wzAnalysis >& logwz_24&

elif [ $1 = "3" ]; then

cp sswwAnalysis.py sswwAnalysis_with_ntuples.py
sed -i 's/doNtuples = False/doNtuples = True/' sswwAnalysis.py
sed -i 's/useFR = 1/useFR = 0/' sswwAnalysis.py

nohup ./analysis_slurm.sh 103 20220 -1 1001 sswwAnalysis >& logssww_00&
nohup ./analysis_slurm.sh 109 20220 -1 1001 sswwAnalysis >& logssww_01&
nohup ./analysis_slurm.sh 176 20220 -1 1001 sswwAnalysis >& logssww_02&
nohup ./analysis_slurm.sh 177 20220 -1 1001 sswwAnalysis >& logssww_03&
nohup ./analysis_slurm.sh 178 20220 -1 1001 sswwAnalysis >& logssww_04&
nohup ./analysis_slurm.sh 179 20220 -1 1001 sswwAnalysis >& logssww_05&
nohup ./analysis_slurm.sh 203 20221 -1 1001 sswwAnalysis >& logssww_06&
nohup ./analysis_slurm.sh 209 20221 -1 1001 sswwAnalysis >& logssww_07&
nohup ./analysis_slurm.sh 276 20221 -1 1001 sswwAnalysis >& logssww_08&
nohup ./analysis_slurm.sh 277 20221 -1 1001 sswwAnalysis >& logssww_09&
nohup ./analysis_slurm.sh 278 20221 -1 1001 sswwAnalysis >& logssww_10&
nohup ./analysis_slurm.sh 279 20221 -1 1001 sswwAnalysis >& logssww_11&
nohup ./analysis_slurm.sh 303 20230 -1 1001 sswwAnalysis >& logssww_12&
nohup ./analysis_slurm.sh 309 20230 -1 1001 sswwAnalysis >& logssww_13&
nohup ./analysis_slurm.sh 376 20230 -1 1001 sswwAnalysis >& logssww_14&
nohup ./analysis_slurm.sh 377 20230 -1 1001 sswwAnalysis >& logssww_15&
nohup ./analysis_slurm.sh 378 20230 -1 1001 sswwAnalysis >& logssww_16&
nohup ./analysis_slurm.sh 379 20230 -1 1001 sswwAnalysis >& logssww_17&
nohup ./analysis_slurm.sh 403 20231 -1 1001 sswwAnalysis >& logssww_18&
nohup ./analysis_slurm.sh 409 20231 -1 1001 sswwAnalysis >& logssww_19&
nohup ./analysis_slurm.sh 476 20231 -1 1001 sswwAnalysis >& logssww_20&
nohup ./analysis_slurm.sh 477 20231 -1 1001 sswwAnalysis >& logssww_21&
nohup ./analysis_slurm.sh 478 20231 -1 1001 sswwAnalysis >& logssww_22&
nohup ./analysis_slurm.sh 479 20231 -1 1001 sswwAnalysis >& logssww_23&
nohup ./analysis_slurm.sh 503 20240 -1 1001 sswwAnalysis >& logssww_24&
nohup ./analysis_slurm.sh 509 20240 -1 1001 sswwAnalysis >& logssww_25&
nohup ./analysis_slurm.sh 576 20240 -1 1001 sswwAnalysis >& logssww_26&
nohup ./analysis_slurm.sh 577 20240 -1 1001 sswwAnalysis >& logssww_27&
nohup ./analysis_slurm.sh 578 20240 -1 1001 sswwAnalysis >& logssww_28&
nohup ./analysis_slurm.sh 579 20240 -1 1001 sswwAnalysis >& logssww_29&

elif [ $1 = "10" ]; then

mv wzAnalysis_with_ntuples.py wzAnalysis.py
mv sswwAnalysis_with_ntuples.py sswwAnalysis.py
hadd -f /work/submit/ceballos/mva_samples/ntupleWZAna_year2027.root ntupleWZAna_*.root
hadd -f /work/submit/ceballos/mva_samples/ntupleWWAna_year2027.root ntupleSSWWAna_*.root

fi

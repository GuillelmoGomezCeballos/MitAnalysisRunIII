#/bin/sh

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

rm -rf /scratch/submit/cms/ceballos/analysis/macros1002
rm -rf /scratch/submit/cms/ceballos/analysis/macros1003
rm -rf /scratch/submit/cms/ceballos/analysis/macros1004
rm -rf /scratch/submit/cms/ceballos/analysis/macros1005
rm -rf /scratch/submit/cms/ceballos/analysis/macros1006
rm -rf /scratch/submit/cms/ceballos/analysis/macros1007
rm -rf /scratch/submit/cms/ceballos/analysis/macros1008
rm -rf /scratch/submit/cms/ceballos/analysis/macros1009

cp -r ../macros /scratch/submit/cms/ceballos/analysis/macros1002
cp -r ../macros /scratch/submit/cms/ceballos/analysis/macros1003
cp -r ../macros /scratch/submit/cms/ceballos/analysis/macros1004
cp -r ../macros /scratch/submit/cms/ceballos/analysis/macros1005
cp -r ../macros /scratch/submit/cms/ceballos/analysis/macros1006
cp -r ../macros /scratch/submit/cms/ceballos/analysis/macros1007
cp -r ../macros /scratch/submit/cms/ceballos/analysis/macros1008
cp -r ../macros /scratch/submit/cms/ceballos/analysis/macros1009

#makeDataCards = 1 # 1 (mjj diff), 2 (mll diff), 3 (njets diff), 4 (detajj diff), 5 (dphijj diff), 6 (mjj), 7 (mll), 8 (detajj), 9 (dphijj)
sed -i 's/makeDataCards = 1/makeDataCards = 2/'  /scratch/submit/cms/ceballos/analysis/macros1002/sswwAnalysis.py 
sed -i 's/makeDataCards = 1/makeDataCards = 3/'  /scratch/submit/cms/ceballos/analysis/macros1003/sswwAnalysis.py 
sed -i 's/makeDataCards = 1/makeDataCards = 4/'  /scratch/submit/cms/ceballos/analysis/macros1004/sswwAnalysis.py 
sed -i 's/makeDataCards = 1/makeDataCards = 5/'  /scratch/submit/cms/ceballos/analysis/macros1005/sswwAnalysis.py 
sed -i 's/makeDataCards = 1/makeDataCards = 6/'  /scratch/submit/cms/ceballos/analysis/macros1006/sswwAnalysis.py 
sed -i 's/makeDataCards = 1/makeDataCards = 7/'  /scratch/submit/cms/ceballos/analysis/macros1007/sswwAnalysis.py 
sed -i 's/makeDataCards = 1/makeDataCards = 8/'  /scratch/submit/cms/ceballos/analysis/macros1008/sswwAnalysis.py 
sed -i 's/makeDataCards = 1/makeDataCards = 9/'  /scratch/submit/cms/ceballos/analysis/macros1009/sswwAnalysis.py 

#makeDataCards = 4 # 1 (njets), 2-1006 (lepton flavor), 3-1002 (3D), 4-1001 (BDT 2D), 5-1003 (BDT 1D), 6-1004 (mjj), 7-1005 (mjj diff)
sed -i 's/makeDataCards = 4/makeDataCards = 3/'  /scratch/submit/cms/ceballos/analysis/macros1002/wzAnalysis.py
sed -i 's/makeDataCards = 4/makeDataCards = 5/'  /scratch/submit/cms/ceballos/analysis/macros1003/wzAnalysis.py
sed -i 's/makeDataCards = 4/makeDataCards = 6/'  /scratch/submit/cms/ceballos/analysis/macros1004/wzAnalysis.py
sed -i 's/makeDataCards = 4/makeDataCards = 7/'  /scratch/submit/cms/ceballos/analysis/macros1005/wzAnalysis.py
sed -i 's/makeDataCards = 4/makeDataCards = 2/'  /scratch/submit/cms/ceballos/analysis/macros1006/wzAnalysis.py
rm -f /scratch/submit/cms/ceballos/analysis/macros1007/wzAnalysis.py
rm -f /scratch/submit/cms/ceballos/analysis/macros1008/wzAnalysis.py
rm -f /scratch/submit/cms/ceballos/analysis/macros1009/wzAnalysis.py

#makeDataCards = 3 # 1 (njets), 2 (lepton flavor), 3 (mjj)
rm -f /scratch/submit/cms/ceballos/analysis/macros1002/zzAnalysis.py
rm -f /scratch/submit/cms/ceballos/analysis/macros1003/zzAnalysis.py
rm -f /scratch/submit/cms/ceballos/analysis/macros1004/zzAnalysis.py
rm -f /scratch/submit/cms/ceballos/analysis/macros1005/zzAnalysis.py
sed -i 's/makeDataCards = 3/makeDataCards = 2/'  /scratch/submit/cms/ceballos/analysis/macros1006/zzAnalysis.py 
rm -f /scratch/submit/cms/ceballos/analysis/macros1007/zzAnalysis.py
rm -f /scratch/submit/cms/ceballos/analysis/macros1008/zzAnalysis.py
rm -f /scratch/submit/cms/ceballos/analysis/macros1009/zzAnalysis.py

cd /scratch/submit/cms/ceballos/analysis/macros1006
python3 remake_Analysis_input_condor_jobs.py --ana=zz --isWZMG=0 --isZZMG=0
python3 remake_Analysis_input_condor_jobs.py --ana=wz --isWZMG=0 --isZZMG=0
mv zzAnalysis_input_condor_jobs_new.cfg zzAnalysis_input_condor_jobs.cfg
mv wzAnalysis_input_condor_jobs_new.cfg wzAnalysis_input_condor_jobs.cfg
cd -

if [[ $1 == 1 ]]; then

diff -r ../macros /scratch/submit/cms/ceballos/analysis/macros1002
diff -r ../macros /scratch/submit/cms/ceballos/analysis/macros1003
diff -r ../macros /scratch/submit/cms/ceballos/analysis/macros1004
diff -r ../macros /scratch/submit/cms/ceballos/analysis/macros1005
diff -r ../macros /scratch/submit/cms/ceballos/analysis/macros1006
diff -r ../macros /scratch/submit/cms/ceballos/analysis/macros1007
diff -r ../macros /scratch/submit/cms/ceballos/analysis/macros1008
diff -r ../macros /scratch/submit/cms/ceballos/analysis/macros1009

fi

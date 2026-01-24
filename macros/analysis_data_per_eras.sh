#!/bin/sh

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

export OPTION=$2;

if [[ $1 == 1 ]]; then

cd /scratch/submit/cms/ceballos/analysis/macros1001

echo "*****Z1*****"
ls fillhisto_zAnalysis100?_sample1???_year20???_job*.root|wc
# z
hadd -f anaZ/fillhisto_zAnalysis_20220.root fillhisto_zAnalysis100?_sample1???_year20220_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20221.root fillhisto_zAnalysis100?_sample1???_year20221_job*.root

hadd -f anaZ/fillhisto_zAnalysis_20230.root fillhisto_zAnalysis100?_sample1???_year20230_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20231.root fillhisto_zAnalysis100?_sample1???_year20231_job*.root

hadd -f anaZ/fillhisto_zAnalysis_20240.root fillhisto_zAnalysis100?_sample10?2_year20240_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20241.root fillhisto_zAnalysis100?_sample10?3_year20240_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20242.root fillhisto_zAnalysis100?_sample10?4_year20240_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20243.root fillhisto_zAnalysis100?_sample10?5_year20240_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20244.root fillhisto_zAnalysis100?_sample10?6_year20240_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20245.root fillhisto_zAnalysis100?_sample10?7_year20240_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20246.root fillhisto_zAnalysis100?_sample10?8_year20240_job*.root

hadd -f anaZ/fillhisto_zAnalysis_20250.root fillhisto_zAnalysis100?_sample10?[1-2]_year20250_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20251.root fillhisto_zAnalysis100?_sample10?3_year20250_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20252.root fillhisto_zAnalysis100?_sample10?4_year20250_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20253.root fillhisto_zAnalysis100?_sample10?5_year20250_job*.root
hadd -f anaZ/fillhisto_zAnalysis_20254.root fillhisto_zAnalysis100?_sample10?6_year20250_job*.root

echo "*****WW*****"
ls fillhisto_wwAnalysis100?_sample1???_year20???_job*.root|wc
# ww
hadd -f anaZ/fillhisto_wwAnalysis_20220.root fillhisto_wwAnalysis?00?_sample1???_year20220_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20221.root fillhisto_wwAnalysis?00?_sample1???_year20221_job*.root

hadd -f anaZ/fillhisto_wwAnalysis_20230.root fillhisto_wwAnalysis?00?_sample1???_year20230_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20231.root fillhisto_wwAnalysis?00?_sample1???_year20231_job*.root

hadd -f anaZ/fillhisto_wwAnalysis_20240.root fillhisto_wwAnalysis?00?_sample10?2_year20240_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20241.root fillhisto_wwAnalysis?00?_sample10?3_year20240_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20242.root fillhisto_wwAnalysis?00?_sample10?4_year20240_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20243.root fillhisto_wwAnalysis?00?_sample10?5_year20240_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20244.root fillhisto_wwAnalysis?00?_sample10?6_year20240_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20245.root fillhisto_wwAnalysis?00?_sample10?7_year20240_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20246.root fillhisto_wwAnalysis?00?_sample10?8_year20240_job*.root

hadd -f anaZ/fillhisto_wwAnalysis_20250.root fillhisto_wwAnalysis?00?_sample10?[1-2]_year20250_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20251.root fillhisto_wwAnalysis?00?_sample10?3_year20250_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20252.root fillhisto_wwAnalysis?00?_sample10?4_year20250_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20253.root fillhisto_wwAnalysis?00?_sample10?5_year20250_job*.root
hadd -f anaZ/fillhisto_wwAnalysis_20254.root fillhisto_wwAnalysis?00?_sample10?6_year20250_job*.root

cd -

cd /scratch/submit/cms/ceballos/analysis/macros1002

echo "*****Z2*****"
ls fillhisto_zAnalysis100?_sample1???_year20???_job*.root|wc
# z
hadd -f anaZ/fillhisto_ztAnalysis_20220.root fillhisto_zAnalysis100?_sample1???_year20220_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20221.root fillhisto_zAnalysis100?_sample1???_year20221_job*.root

hadd -f anaZ/fillhisto_ztAnalysis_20230.root fillhisto_zAnalysis100?_sample1???_year20230_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20231.root fillhisto_zAnalysis100?_sample1???_year20231_job*.root

hadd -f anaZ/fillhisto_ztAnalysis_20240.root fillhisto_zAnalysis100?_sample10?2_year20240_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20241.root fillhisto_zAnalysis100?_sample10?3_year20240_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20242.root fillhisto_zAnalysis100?_sample10?4_year20240_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20243.root fillhisto_zAnalysis100?_sample10?5_year20240_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20244.root fillhisto_zAnalysis100?_sample10?6_year20240_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20245.root fillhisto_zAnalysis100?_sample10?7_year20240_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20246.root fillhisto_zAnalysis100?_sample10?8_year20240_job*.root

hadd -f anaZ/fillhisto_ztAnalysis_20250.root fillhisto_zAnalysis100?_sample10?[1-2]_year20250_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20251.root fillhisto_zAnalysis100?_sample10?3_year20250_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20252.root fillhisto_zAnalysis100?_sample10?4_year20250_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20253.root fillhisto_zAnalysis100?_sample10?5_year20250_job*.root
hadd -f anaZ/fillhisto_ztAnalysis_20254.root fillhisto_zAnalysis100?_sample10?6_year20250_job*.root

cd -

cd /scratch/submit/cms/ceballos/analysis/macros1006

echo "*****ZZ*****"
ls fillhisto_zzAnalysis100?_sample1???_year20???_job*.root|wc
# zz
hadd -f anaZ/fillhisto_zzAnalysis_20220.root fillhisto_zzAnalysis100?_sample1???_year20220_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20221.root fillhisto_zzAnalysis100?_sample1???_year20221_job*.root

hadd -f anaZ/fillhisto_zzAnalysis_20230.root fillhisto_zzAnalysis100?_sample1???_year20230_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20231.root fillhisto_zzAnalysis100?_sample1???_year20231_job*.root

hadd -f anaZ/fillhisto_zzAnalysis_20240.root fillhisto_zzAnalysis100?_sample10?2_year20240_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20241.root fillhisto_zzAnalysis100?_sample10?3_year20240_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20242.root fillhisto_zzAnalysis100?_sample10?4_year20240_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20243.root fillhisto_zzAnalysis100?_sample10?5_year20240_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20244.root fillhisto_zzAnalysis100?_sample10?6_year20240_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20245.root fillhisto_zzAnalysis100?_sample10?7_year20240_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20246.root fillhisto_zzAnalysis100?_sample10?8_year20240_job*.root

hadd -f anaZ/fillhisto_zzAnalysis_20250.root fillhisto_zzAnalysis100?_sample10?[1-2]_year20250_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20251.root fillhisto_zzAnalysis100?_sample10?3_year20250_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20252.root fillhisto_zzAnalysis100?_sample10?4_year20250_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20253.root fillhisto_zzAnalysis100?_sample10?5_year20250_job*.root
hadd -f anaZ/fillhisto_zzAnalysis_20254.root fillhisto_zzAnalysis100?_sample10?6_year20250_job*.root

echo "*****WZ*****"
ls fillhisto_wzAnalysis100?_sample1???_year20???_job*.root|wc
# wz
hadd -f anaZ/fillhisto_wzAnalysis_20220.root fillhisto_wzAnalysis100?_sample1???_year20220_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20221.root fillhisto_wzAnalysis100?_sample1???_year20221_job*.root

hadd -f anaZ/fillhisto_wzAnalysis_20230.root fillhisto_wzAnalysis100?_sample1???_year20230_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20231.root fillhisto_wzAnalysis100?_sample1???_year20231_job*.root

hadd -f anaZ/fillhisto_wzAnalysis_20240.root fillhisto_wzAnalysis100?_sample10?2_year20240_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20241.root fillhisto_wzAnalysis100?_sample10?3_year20240_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20242.root fillhisto_wzAnalysis100?_sample10?4_year20240_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20243.root fillhisto_wzAnalysis100?_sample10?5_year20240_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20244.root fillhisto_wzAnalysis100?_sample10?6_year20240_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20245.root fillhisto_wzAnalysis100?_sample10?7_year20240_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20246.root fillhisto_wzAnalysis100?_sample10?8_year20240_job*.root

hadd -f anaZ/fillhisto_wzAnalysis_20250.root fillhisto_wzAnalysis100?_sample10?[1-2]_year20250_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20251.root fillhisto_wzAnalysis100?_sample10?3_year20250_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20252.root fillhisto_wzAnalysis100?_sample10?4_year20250_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20253.root fillhisto_wzAnalysis100?_sample10?5_year20250_job*.root
hadd -f anaZ/fillhisto_wzAnalysis_20254.root fillhisto_wzAnalysis100?_sample10?6_year20250_job*.root
cd -

fi

root -l -q -b ../../macros/analysis_data_per_eras.C

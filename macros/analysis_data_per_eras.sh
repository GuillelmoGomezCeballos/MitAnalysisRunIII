#!/bin/sh

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

export OPTION=$2;

if [[ $1 == 1 ]]; then

# z
hadd -f anaZ/fillhisto_zAnalysis_20220.root fillhisto_zAnalysis1001_sample1???_year20220_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20221.root fillhisto_zAnalysis1001_sample1???_year20221_job-1.root

hadd -f anaZ/fillhisto_zAnalysis_20230.root fillhisto_zAnalysis1001_sample1???_year20230_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20231.root fillhisto_zAnalysis1001_sample1???_year20231_job-1.root

hadd -f anaZ/fillhisto_zAnalysis_20240.root fillhisto_zAnalysis1001_sample10?2_year20240_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20241.root fillhisto_zAnalysis1001_sample10?3_year20240_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20242.root fillhisto_zAnalysis1001_sample10?4_year20240_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20243.root fillhisto_zAnalysis1001_sample10?5_year20240_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20244.root fillhisto_zAnalysis1001_sample10?6_year20240_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20245.root fillhisto_zAnalysis1001_sample10?7_year20240_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20246.root fillhisto_zAnalysis1001_sample10?8_year20240_job-1.root

hadd -f anaZ/fillhisto_zAnalysis_20250.root fillhisto_zAnalysis1001_sample10?[1-2]_year20250_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20251.root fillhisto_zAnalysis1001_sample10?3_year20250_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20252.root fillhisto_zAnalysis1001_sample10?4_year20250_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20253.root fillhisto_zAnalysis1001_sample10?5_year20250_job-1.root
hadd -f anaZ/fillhisto_zAnalysis_20254.root fillhisto_zAnalysis1001_sample10?6_year20250_job-1.root

# ww
hadd -f anaZ/fillhisto_wwAnalysis_20220.root fillhisto_wwAnalysis1001_sample1???_year20220_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20221.root fillhisto_wwAnalysis1001_sample1???_year20221_job-1.root

hadd -f anaZ/fillhisto_wwAnalysis_20230.root fillhisto_wwAnalysis1001_sample1???_year20230_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20231.root fillhisto_wwAnalysis1001_sample1???_year20231_job-1.root

hadd -f anaZ/fillhisto_wwAnalysis_20240.root fillhisto_wwAnalysis1001_sample10?2_year20240_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20241.root fillhisto_wwAnalysis1001_sample10?3_year20240_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20242.root fillhisto_wwAnalysis1001_sample10?4_year20240_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20243.root fillhisto_wwAnalysis1001_sample10?5_year20240_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20244.root fillhisto_wwAnalysis1001_sample10?6_year20240_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20245.root fillhisto_wwAnalysis1001_sample10?7_year20240_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20246.root fillhisto_wwAnalysis1001_sample10?8_year20240_job-1.root

hadd -f anaZ/fillhisto_wwAnalysis_20250.root fillhisto_wwAnalysis1001_sample10?[1-2]_year20250_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20251.root fillhisto_wwAnalysis1001_sample10?3_year20250_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20252.root fillhisto_wwAnalysis1001_sample10?4_year20250_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20253.root fillhisto_wwAnalysis1001_sample10?5_year20250_job-1.root
hadd -f anaZ/fillhisto_wwAnalysis_20254.root fillhisto_wwAnalysis1001_sample10?6_year20250_job-1.root

# zz
hadd -f anaZ/fillhisto_zzAnalysis_20220.root fillhisto_zzAnalysis1001_sample1???_year20220_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20221.root fillhisto_zzAnalysis1001_sample1???_year20221_job-1.root

hadd -f anaZ/fillhisto_zzAnalysis_20230.root fillhisto_zzAnalysis1001_sample1???_year20230_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20231.root fillhisto_zzAnalysis1001_sample1???_year20231_job-1.root

hadd -f anaZ/fillhisto_zzAnalysis_20240.root fillhisto_zzAnalysis1001_sample10?2_year20240_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20241.root fillhisto_zzAnalysis1001_sample10?3_year20240_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20242.root fillhisto_zzAnalysis1001_sample10?4_year20240_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20243.root fillhisto_zzAnalysis1001_sample10?5_year20240_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20244.root fillhisto_zzAnalysis1001_sample10?6_year20240_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20245.root fillhisto_zzAnalysis1001_sample10?7_year20240_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20246.root fillhisto_zzAnalysis1001_sample10?8_year20240_job-1.root

hadd -f anaZ/fillhisto_zzAnalysis_20250.root fillhisto_zzAnalysis1001_sample10?[1-2]_year20250_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20251.root fillhisto_zzAnalysis1001_sample10?3_year20250_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20252.root fillhisto_zzAnalysis1001_sample10?4_year20250_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20253.root fillhisto_zzAnalysis1001_sample10?5_year20250_job-1.root
hadd -f anaZ/fillhisto_zzAnalysis_20254.root fillhisto_zzAnalysis1001_sample10?6_year20250_job-1.root

# wz
hadd -f anaZ/fillhisto_wzAnalysis_20220.root fillhisto_wzAnalysis1001_sample1???_year20220_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20221.root fillhisto_wzAnalysis1001_sample1???_year20221_job-1.root

hadd -f anaZ/fillhisto_wzAnalysis_20230.root fillhisto_wzAnalysis1001_sample1???_year20230_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20231.root fillhisto_wzAnalysis1001_sample1???_year20231_job-1.root

hadd -f anaZ/fillhisto_wzAnalysis_20240.root fillhisto_wzAnalysis1001_sample10?2_year20240_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20241.root fillhisto_wzAnalysis1001_sample10?3_year20240_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20242.root fillhisto_wzAnalysis1001_sample10?4_year20240_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20243.root fillhisto_wzAnalysis1001_sample10?5_year20240_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20244.root fillhisto_wzAnalysis1001_sample10?6_year20240_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20245.root fillhisto_wzAnalysis1001_sample10?7_year20240_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20246.root fillhisto_wzAnalysis1001_sample10?8_year20240_job-1.root

hadd -f anaZ/fillhisto_wzAnalysis_20250.root fillhisto_wzAnalysis1001_sample10?[1-2]_year20250_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20251.root fillhisto_wzAnalysis1001_sample10?3_year20250_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20252.root fillhisto_wzAnalysis1001_sample10?4_year20250_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20253.root fillhisto_wzAnalysis1001_sample10?5_year20250_job-1.root
hadd -f anaZ/fillhisto_wzAnalysis_20254.root fillhisto_wzAnalysis1001_sample10?6_year20250_job-1.root

fi

root -l -q -b ../../macros/analysis_data_per_eras.C

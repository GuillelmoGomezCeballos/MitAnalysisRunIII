#!/bin/bash

if [ $# -lt 1 ]; then
   echo "TOO FEW PARAMETERS"
   exit
fi

if [[ $1 == 8 ]]; then

    time python3 genAnalysis.py --process=960 --sel=ww >& log_ww_960 &
    time python3 genAnalysis.py --process=961 --sel=ww >& log_ww_961 &
    time python3 genAnalysis.py --process=962 --sel=ww >& log_ww_962 &
    time python3 genAnalysis.py --process=963 --sel=ww >& log_ww_963 &
    time python3 genAnalysis.py --process=964 --sel=ww >& log_ww_964 &
    time python3 genAnalysis.py --process=965 --sel=ww >& log_ww_965 &
    time python3 genAnalysis.py --process=966 --sel=ww >& log_ww_966 &
    time python3 genAnalysis.py --process=967 --sel=ww >& log_ww_967 &
    time python3 genAnalysis.py --process=968 --sel=ww >& log_ww_968 &
    time python3 genAnalysis.py --process=969 --sel=ww >& log_ww_969 &
    time python3 genAnalysis.py --process=970 --sel=ww >& log_ww_970 &
    time python3 genAnalysis.py --process=971 --sel=ww >& log_ww_971 &
    time python3 genAnalysis.py --process=972 --sel=ww >& log_ww_972 &
    time python3 genAnalysis.py --process=973 --sel=ww >& log_ww_973 &
    time python3 genAnalysis.py --process=974 --sel=ww >& log_ww_974 &
    time python3 genAnalysis.py --process=975 --sel=ww >& log_ww_975 &
    time python3 genAnalysis.py --process=976 --sel=ww >& log_ww_976 &

elif [[ $1 == 3 ]]; then

    time python3 genAnalysis.py --process=977 --sel=vbs >& log_vbs_977 &
    time python3 genAnalysis.py --process=978 --sel=vbs >& log_vbs_978 &
    time python3 genAnalysis.py --process=979 --sel=vbs >& log_vbs_979 &
    time python3 genAnalysis.py --process=980 --sel=vbs >& log_vbs_980 &
    time python3 genAnalysis.py --process=981 --sel=vbs >& log_vbs_981 &
    time python3 genAnalysis.py --process=982 --sel=vbs >& log_vbs_982 &
    time python3 genAnalysis.py --process=983 --sel=vbs >& log_vbs_983 &

elif [[ $1 == 18 ]]; then

    hadd -f histo_ww_powheg.root fillhisto_genAnalysis_sample961_year20240_job-1.root

    hadd -f histo_ww_mcfm.root fillhisto_genAnalysis_sample96[2-9]_year20240_job-1.root fillhisto_genAnalysis_sample970_year20240_job-1.root

    hadd -f histo_ww_madgraph.root fillhisto_genAnalysis_sample97[1-4]_year20240_job-1.root
    
    hadd -f histo_ww_minnlo.root fillhisto_genAnalysis_sample976_year20240_job-1.root

    hadd -f histo_ww_powheg_mcfm.root histo_ww_powheg.root histo_ww_mcfm.root

    hadd -f histo_ww_powheg_madgraph.root histo_ww_powheg.root histo_ww_madgraph.root

    hadd -f histo_ww_minnlo_mcfm.root histo_ww_minnlo.root histo_ww_mcfm.root

    hadd -f histo_ww_minnlo_madgraph.root histo_ww_minnlo.root histo_ww_madgraph.root

elif [[ $1 == 13 ]]; then

    hadd -f histo_vbs_ewk_ssww_sherpa.root fillhisto_genAnalysis_sample983_year20240_job-1.root

    hadd -f histo_vbs_ewk_ssww.root fillhisto_genAnalysis_sample980_year20240_job-1.root

    hadd -f histo_vbs_ewk_wpwp_powheg.root fillhisto_genAnalysis_sample978_year20240_job-1.root

    hadd -f histo_vbs_ewk_wmwm_powheg.root fillhisto_genAnalysis_sample979_year20240_job-1.root

    hadd -f histo_vbs_ewk_wz.root fillhisto_genAnalysis_sample981_year20240_job-1.root

    hadd -f histo_vbs_ewk_wz_madgraph.root fillhisto_genAnalysis_sample982_year20240_job-1.root

    hadd -f histo_vbs_ewk_wz_powheg.root fillhisto_genAnalysis_sample977_year20240_job-1.root

fi

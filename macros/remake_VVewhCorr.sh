#/bin/sh

root -l -q -b ../../macros/remake_VVewkCorr.C;

python3 ../../macros/make_rootfiles_vbs_theory.py;

hadd -f VV_NLO_LO_CMS_mjj.root WW13p6_NLO_LO_CMS_mjj.root data/VV_NLO_LO_CMS_mjj_run2_new.root;

rm -f WW13p6_NLO_LO_CMS_mjj.root data/VV_NLO_LO_CMS_mjj_run2_new.root;

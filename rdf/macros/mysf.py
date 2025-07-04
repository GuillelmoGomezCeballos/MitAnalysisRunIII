import ROOT
import correctionlib

correctionlib.register_pyroot_binding()
ROOT.gInterpreter.Declare('#include "mysf.h"')
print("eval_20221")
ROOT.gInterpreter.ProcessLine('auto corr = MyCorrections(20231);')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSF((char*)"2023PromptD", (char*)"sf", (char*)"wp80iso", 1.1, 34.0,0.3)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSF((char*)"2023PromptD", (char*)"sfup", (char*)"wp80iso", 1.1, 34.0,0.3)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSF((char*)"2023PromptD", (char*)"sfdown", (char*)"Medium", 1.1, 34.0,0.3)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSF((char*)"2023PromptD", (char*)"sf", (char*)"RecoBelow20", 1.1, 19.999,0.3)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSF((char*)"2023PromptD", (char*)"sf", (char*)"Reco20to75", 1.1, 20.0,0.3)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSF((char*)"2023PromptD", (char*)"sf", (char*)"RecoAbove75", 1.1, 75.0,0.3)')
ROOT.gInterpreter.ProcessLine('corr.eval_photonSF((char*)"2023PromptD", (char*)"sf", (char*)"Medium", 1.1, 30.0,0.3)')
print("eval_el_scale_smeaer")
ROOT.gInterpreter.ProcessLine('corr.eval_electronScale((char*)"total_correction", 1, 357900, 0.5, 0.99, 40)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronScale((char*)"total_uncertainty", 1, 357900, 0.5, 0.99, 40)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronScale((char*)"total_uncertainty", 1, 1, 0.5, 0.99, 40)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSmearing((char*)"rho", 0.5, 0.99)')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSmearing((char*)"err_rho", 0.5, 0.99)')
print("eval_muon_med")
ROOT.gInterpreter.ProcessLine('corr.eval_muonTRKSF((double)0.9, 35, 35,(char*)"nominal")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonIDSF ((double)0.9, 35,    (char*)"nominal")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonISOSF((double)0.9, 35,    (char*)"nominal")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonTRKSF((double)0.9, 35, 35,(char*)"syst")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonIDSF ((double)0.9, 35,    (char*)"syst")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonISOSF((double)0.9, 35,    (char*)"syst")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonTRKSF((double)0.9, 35, 35,(char*)"stat")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonIDSF ((double)0.9, 35,    (char*)"stat")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonISOSF((double)0.9, 35,    (char*)"stat")')
print("eval_muon_high")
ROOT.gInterpreter.ProcessLine('corr.eval_muonTRKSF((double)0.9, 350, 350,(char*)"nominal")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonIDSF ((double)0.9, 350,     (char*)"nominal")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonISOSF((double)0.9, 350,     (char*)"nominal")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonTRKSF((double)0.9, 350, 350,(char*)"syst")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonIDSF ((double)0.9, 350,     (char*)"syst")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonISOSF((double)0.9, 350,     (char*)"syst")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonTRKSF((double)0.9, 350, 350,(char*)"stat")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonIDSF ((double)0.9, 350,     (char*)"stat")')
ROOT.gInterpreter.ProcessLine('corr.eval_muonISOSF((double)0.9, 350,     (char*)"stat")')
print("eval_btv")
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"central",(char*)"L",1.1,350.0,4)')
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"central",(char*)"L",1.1,350.0,5)')
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"central",(char*)"L",1.1,350.0,0)')
print("eval_up")
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"up",(char*)"L",1.1,35.0,5)')
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"up_statistic",(char*)"L",1.1,35.0,5)')
print("eval_down")
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"down",(char*)"L",1.1,35.0,5)')
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"down_statistic",(char*)"L",1.1,35.0,5)')
print("eval_tau")
ROOT.gInterpreter.ProcessLine('corr.eval_tauJETSF(65.2,11,5,"Tight","Tight","nom")')
print("eval_jetCORR")
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 0)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 1)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 2)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 3)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 4)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 5)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 6)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 7)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 8)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30, 9)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,10)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,11)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,12)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,13)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,14)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,15)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,16)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,17)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,18)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,19)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,20)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,21)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,22)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,23)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,24)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,25)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,26)')
ROOT.gInterpreter.ProcessLine('corr.eval_jesUnc(1.5,30,27)')
print("eval_jetCORR_others")
ROOT.gInterpreter.ProcessLine('corr.eval_jetCORR(0.5,1.,2.,150,15,380000,3)')
ROOT.gInterpreter.ProcessLine('corr.eval_jerScaleFactor(1.5,30, 0)')
ROOT.gInterpreter.ProcessLine('corr.eval_jerScaleFactor(1.5,30,+1)')
ROOT.gInterpreter.ProcessLine('corr.eval_jerScaleFactor(1.5,30,-1)')
ROOT.gInterpreter.ProcessLine('corr.eval_jerPtResolution(2.5,20,30)')
ROOT.gInterpreter.ProcessLine('corr.eval_jerPtResolution(3.0,20,30)')
ROOT.gInterpreter.ProcessLine('corr.eval_jerPtResolution(3.5,20,30)')
ROOT.gInterpreter.ProcessLine('corr.eval_jetVetoMap(2.5,-2.2,3)')
ROOT.gInterpreter.ProcessLine('corr.eval_jetVetoMap(6.5,-2.2,3)')
ROOT.gInterpreter.ProcessLine('corr.eval_jetVetoMap(2.5,-6.2,3)')
print("eval_jetSel")
ROOT.gInterpreter.ProcessLine('corr.eval_jetSel(0,-0.2,0.4,0.25,0.1,0.15,0.1,1.0,2.0)')
ROOT.gInterpreter.ProcessLine('corr.eval_jetSel(1,-0.2,0.4,0.25,0.1,0.15,0.1,1.0,2.0)')
ROOT.gInterpreter.ProcessLine('corr.eval_jetSel(0,-4.2,0.4,0.25,0.1,0.15,0.1,0.0,2.0)')
ROOT.gInterpreter.ProcessLine('corr.eval_jetSel(1,-4.2,0.4,0.25,0.1,0.15,0.1,0.0,2.0)')
print("eval_muon_scale")
ROOT.gInterpreter.ProcessLine('corr.eval_muon_pt_scale(1, 30.0, 0.5, 2.5, -1)')
ROOT.gInterpreter.ProcessLine('corr.eval_muon_pt_scale(0, 30.0, 0.5, 2.5, -1)')
ROOT.gInterpreter.ProcessLine('corr.eval_muon_pt_resol(30.5, 0.5, 13)')
ROOT.gInterpreter.ProcessLine('corr.eval_muon_pt_scale_var(30.6, 0.5, 2.5, -1, "up")')
ROOT.gInterpreter.ProcessLine('corr.eval_muon_pt_scale_var(30.6, 0.5, 2.5, -1, "dn")')
ROOT.gInterpreter.ProcessLine('corr.eval_muon_pt_resol_var(30.5, 30.6, 0.5, "up")')
ROOT.gInterpreter.ProcessLine('corr.eval_muon_pt_resol_var(30.5, 30.6, 0.5, "dn")')

import ROOT
import correctionlib

correctionlib.register_pyroot_binding()
ROOT.gInterpreter.Declare('#include "mysf.h"')
ROOT.gInterpreter.Load("mysf.so")
ROOT.gInterpreter.ProcessLine('auto corr = MyCorrections(2018);')
ROOT.gInterpreter.ProcessLine('corr.eval_electronSF((char*)"2018", (char*)"sf", (char*)"Medium", 1.1, 34.0)')
ROOT.gInterpreter.ProcessLine('corr.eval_muonIDSF((char*)"2018_UL",(char*)"sf",(char*)"Medium", (double)1.1, 25.0)')
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"central",(char*)"T",1.1,35.0,4)')
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"central",(char*)"T",1.1,35.0,5)')
ROOT.gInterpreter.ProcessLine('corr.eval_btvSF((char*)"central",(char*)"T",1.1,35.0,0)')

#include "TH1D.h"
#include "TH2D.h"
#include "cmsstyle.C"

enum plotCategory {
  kPlotData      , // 0
  kPlotqqWW      , // 1
  kPlotggWW      , // 2
  kPlotTT        , // 3
  kPlotTW        , // 4
  kPlotDY        , // 5
  kPlotEWKSSWW   , // 6
  kPlotQCDSSWW   , // 7
  kPlotEWKWZ     , // 8
  kPlotWZ        , // 9
  kPlotZZ        , //10
  kPlotNonPrompt , //11
  kPlotVVV       , //12
  kPlotTVX       , //13
  kPlotVG        , //14
  kPlotHiggs     , //15
  kPlotWS        , //16
  kPlotOther     , //17
  kPlotEM        , //18
  kPlotBSM       , //19
  kPlotSignal0   , //20
  kPlotSignal1   , //21
  kPlotSignal2   , //22
  kPlotSignal3   , //23
  kPlotSignal4   , //24
  kPlotSignal5   , //25
  nPlotCategories
};

std::map<int, TString> plotBaseNames={
  { kPlotData	   , "Data" },
  { kPlotqqWW	   , "qqWW" },
  { kPlotggWW	   , "ggWW" },
  { kPlotTT	   , "TT" },
  { kPlotTW	   , "TW" },
  { kPlotDY	   , "DY" },
  { kPlotEWKSSWW   , "EWKSSWW" },
  { kPlotQCDSSWW   , "QCDSSWW" },
  { kPlotEWKWZ     , "EWKWZ" },
  { kPlotWZ	   , "WZ" },
  { kPlotZZ	   , "ZZ" },
  { kPlotNonPrompt , "NonPrompt" },
  { kPlotVVV	   , "VVV" },
  { kPlotTVX	   , "TVX" },
  { kPlotVG	   , "VG" },
  { kPlotHiggs     , "Higgs" },
  { kPlotWS	   , "WS" },
  { kPlotOther     , "Other" },
  { kPlotEM	   , "EM" },
  { kPlotBSM	   , "BSM" },
  { kPlotSignal0   , "Signal0" },
  { kPlotSignal1   , "Signal1" },
  { kPlotSignal2   , "Signal2" },
  { kPlotSignal3   , "Signal3" },
  { kPlotSignal4   , "Signal4" },
  { kPlotSignal5   , "Signal5" }
}; 

std::map<int, int> plotColors={
  { kPlotData	   , kBlack},
  { kPlotqqWW	   , cmsstyle::p10::kBlue},
  { kPlotggWW	   , cmsstyle::p10::kBlue-3},
  { kPlotTT	   , cmsstyle::p10::kYellow},
  { kPlotTW	   , cmsstyle::p10::kYellow-3},
  { kPlotDY	   , cmsstyle::p10::kAsh},
  { kPlotEWKSSWW   , kViolet},
  { kPlotQCDSSWW   , cmsstyle::p10::kBrown-3},
  { kPlotEWKWZ     , 841},
  { kPlotWZ	   , cmsstyle::p10::kRed},
  { kPlotZZ	   , cmsstyle::p10::kCyan},
  { kPlotNonPrompt , cmsstyle::p10::kGray},
  { kPlotVVV	   , cmsstyle::p10::kViolet},
  { kPlotTVX	   , cmsstyle::p10::kOrange},
  { kPlotVG	   , cmsstyle::p10::kBrown},
  { kPlotHiggs     , cmsstyle::p10::kGreen},
  { kPlotWS	   , 840},
  { kPlotOther     , kViolet+7},
  { kPlotEM	   , cmsstyle::p10::kCyan-3},
  { kPlotBSM	   , kAzure+1},
  { kPlotSignal0   , kAzure+2},
  { kPlotSignal1   , kAzure+3},
  { kPlotSignal2   , kAzure+4},
  { kPlotSignal3   , kAzure+5},
  { kPlotSignal4   , kAzure+6},
  { kPlotSignal5   , kAzure+7}
}; 

std::map<int, TString> plotNames={
    { kPlotData      , "Data"},
    { kPlotqqWW      , "WW"},
    { kPlotggWW      , "gg #rightarrow WW"},
    { kPlotTT	     , "Top quark"},
    { kPlotTW	     , "tW"},
    { kPlotDY	     , "Drell-Yan"},
    { kPlotEWKSSWW   , "W^{#pm}W^{#pm}"},
    { kPlotQCDSSWW   , "QCD W^{#pm}W^{#pm}"},
    { kPlotEWKWZ     , "EWK WZ"},
    { kPlotWZ	     , "WZ"},
    { kPlotZZ	     , "ZZ"},
    { kPlotNonPrompt , "Nonprompt"},
    { kPlotVVV       , "VVV"},
    { kPlotTVX       , "tVx"},
    { kPlotVG	     , "V#gamma" },
    { kPlotHiggs     , "Higgs boson"},
    { kPlotWS	     , "Wrong sign"},
    { kPlotOther     , "Other bkg."},
    { kPlotEM	     , "Nonresonant"},
    { kPlotBSM       , "BSM"},
    { kPlotSignal0   , "Signal 0"},
    { kPlotSignal1   , "Signal 1"},
    { kPlotSignal2   , "Signal 2"},
    { kPlotSignal3   , "Signal 3"},
    { kPlotSignal4   , "Signal 4"},
    { kPlotSignal5   , "Signal 5"}
};

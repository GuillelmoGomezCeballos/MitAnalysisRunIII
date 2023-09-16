#include "TH1D.h"
#include "TH2D.h"

enum plotCategory {
  kPlotData        , // 0
  kPlotqqWW        , // 1
  kPlotggWW        , // 2
  kPlotTop         , // 3
  kPlotDY          , // 4
  kPlotEWKSSWW     , // 5
  kPlotQCDSSWW     , // 6
  kPlotEWKWZ       , // 7
  kPlotWZ          , // 8
  kPlotZZ          , // 9
  kPlotNonPrompt   , //10
  kPlotVVV         , //11
  kPlotTVX         , //12
  kPlotVG          , //13
  kPlotHiggs       , //14
  kPlotDPSWW       , //15
  kPlotWS          , //16
  kPlotEM          , //17
  kPlotOther        ,//18
  kPlotBSM         , //19
  kPlotSignal0     , //20
  kPlotSignal1     , //21
  kPlotSignal2     , //22
  kPlotSignal3     , //23
  nPlotCategories
};

std::map<int, TString> plotBaseNames={
  { kPlotData	     , "Data" },
  { kPlotqqWW	     , "qqWW" },
  { kPlotggWW	     , "ggWW" },
  { kPlotTop	     , "Top" },
  { kPlotDY	     , "DY" },
  { kPlotEWKSSWW     , "EWKSSWW" },
  { kPlotQCDSSWW     , "QCDSSWW" },
  { kPlotEWKWZ	     , "EWKWZ" },
  { kPlotWZ	     , "WZ" },
  { kPlotZZ	     , "ZZ" },
  { kPlotNonPrompt   , "NonPrompt" },
  { kPlotVVV	     , "VVV" },
  { kPlotTVX	     , "TVX" },
  { kPlotVG	     , "VG" },
  { kPlotHiggs       , "Higgs" },
  { kPlotDPSWW       , "DPSWW" },
  { kPlotWS	     , "WS" },
  { kPlotEM	     , "EM" },
  { kPlotOther       , "Other" },
  { kPlotBSM	     , "BSM" },
  { kPlotSignal0     , "Signal0" },
  { kPlotSignal1     , "Signal1" },
  { kPlotSignal2     , "Signal2" },
  { kPlotSignal3     , "Signal3" }
}; 

std::map<int, int> plotColors={
  { kPlotData	     , kBlack},
  { kPlotqqWW	     , kAzure-9},
  { kPlotggWW	     , 901},
  { kPlotTop	     , kYellow},
  { kPlotDY	     , kAzure-2},
  { kPlotEWKSSWW     , TColor::GetColor(248,206,104)},
  { kPlotQCDSSWW     , TColor::GetColor(250,202,255)},
  { kPlotEWKWZ       , kCyan+3},
  { kPlotWZ	     , TColor::GetColor(222,90,106)},
  { kPlotZZ	     , kAzure-9},
  { kPlotNonPrompt   , TColor::GetColor(155,152,204)},
  { kPlotVVV	     , 840},
  { kPlotTVX	     , kViolet+6},
  { kPlotVG	     , kGreen-8},
  { kPlotHiggs       , 842},
  { kPlotDPSWW       , kGreen},
  { kPlotWS	     , kAzure+10},
  { kPlotEM	     , kGreen-5},
  { kPlotOther       , kGreen-5},
  { kPlotBSM	     , kGreen-4},
  { kPlotSignal0     , kBlue},
  { kPlotSignal1     , kMagenta+1},
  { kPlotSignal2     , kGreen-4},
  { kPlotSignal3     , kAzure-4}
}; 

std::map<int, TString> plotNames={
    { kPlotData        , "Data"},
    { kPlotqqWW        , "WW"},
    { kPlotggWW        , "gg #rightarrow WW"},
    { kPlotTop         , "Top quark"},
    { kPlotDY	       , "Drell-Yan"},
    { kPlotEWKSSWW     , "W^{#pm}W^{#pm}"},
    { kPlotQCDSSWW     , "QCD W^{#pm}W^{#pm}"},
    { kPlotEWKWZ       , "EWK WZ"},
    { kPlotWZ	       , "WZ"},
    { kPlotZZ	       , "ZZ"},
    { kPlotNonPrompt   , "Nonprompt"},
    { kPlotVVV         , "VVV"},
    { kPlotTVX         , "tVx"},
    { kPlotVG	       , "V#gamma" },
    { kPlotHiggs       , "VH"},
    { kPlotDPSWW       , "DPS W^{#pm}W^{#pm}"},
    { kPlotWS	       , "Wrong sign"},
    { kPlotEM	       , "Nonresonant"},
    { kPlotOther       , "Other bkg."},
    { kPlotBSM         , "BSM"},
    { kPlotSignal0     , "Signal 0"},
    { kPlotSignal1     , "W_{L}W_{L}"},
    { kPlotSignal2     , "W_{L}W_{T}"},
    { kPlotSignal3     , "W_{T}W_{T}"}
};

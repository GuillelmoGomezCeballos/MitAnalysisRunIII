#include <TROOT.h>
#include <TMVA/DataLoader.h>
#include <TMVA/Factory.h>
#include <TMVA/Types.h>
#include <TFile.h>
#include <TCut.h>
#include <TTree.h>
#include <TString.h>
#include <TStyle.h>

void ewkvbsPolMVA(
  int nsel = 0,
  int version = 0,
  bool moreMVAs = false,
  bool dodnn = false
) {

  TString extraString = Form("vbfpol_nsel%d_v%d",nsel,version);

  gROOT->ProcessLine("TMVA::gConfig().GetVariablePlotting().fMaxNumOfAllowedVariablesForScatterPlots = 50");
  TFile *output_file;
  TMVA::Factory *factory;
  TString trainTreeEventSplitStr="(eventNum % 10)<5";
  TString testTreeEventSplitStr="(eventNum % 10)>=5";

  TChain *mvaTree = new TChain("events");
  mvaTree->Add("/work/submit/ceballos/mva_samples/ntupleWWPolAna_year2027.root");
  
  // Initialize the factory
  output_file=TFile::Open(Form("MVA_%s.root",extraString.Data()), "RECREATE");
  factory = new TMVA::Factory("bdt", output_file, "!V:!Silent:DrawProgressBar:Transformations=I;D;P;G,D:AnalysisType=Multiclass");
  TString factoryOptions="!V:!Silent:DrawProgressBar";
  if(nsel != 0) factoryOptions+=":AnalysisType=Classification";
  factory = new TMVA::Factory("bdt", output_file, factoryOptions);
  TMVA::DataLoader *dataloader=new TMVA::DataLoader("MitEWKVBSAnalysis");

  if(nsel == 0){ // LL vs. LT vs. TT
    TCut cutTrainWWLL = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==%d)",trainTreeEventSplitStr.Data(),20);
    TCut cutTrainWWLT = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==%d)",trainTreeEventSplitStr.Data(),21);
    TCut cutTrainWWTT = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==%d)",trainTreeEventSplitStr.Data(),22);
    TCut cutTestWWLL  = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==%d)",testTreeEventSplitStr.Data(),20);
    TCut cutTestWWLT  = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==%d)",testTreeEventSplitStr.Data(),21);
    TCut cutTestWWTT  = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==%d)",testTreeEventSplitStr.Data(),22);

    dataloader->AddTree(mvaTree, "WWLL", 1.0, cutTrainWWLL, "train");
    dataloader->AddTree(mvaTree, "WWLT", 1.0, cutTrainWWLT, "train");
    dataloader->AddTree(mvaTree, "WWTT", 1.0, cutTrainWWTT, "train");
    dataloader->AddTree(mvaTree, "WWLL", 1.0, cutTestWWLL , "test");
    dataloader->AddTree(mvaTree, "WWLT", 1.0, cutTestWWLT , "test");
    dataloader->AddTree(mvaTree, "WWTT", 1.0, cutTestWWTT , "test");
    dataloader->SetWeightExpression("1.0", "WWLL");
    dataloader->SetWeightExpression("1.0", "WWLT");
    dataloader->SetWeightExpression("1.0", "WWTT");
  }
  else if(nsel == 1){ // LX vs. TT
    TCut cutTrainWWLX = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==20||theCat==21)",trainTreeEventSplitStr.Data());
    TCut cutTrainWWTT = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==22||theCat==0)",trainTreeEventSplitStr.Data());
    TCut cutTestWWLX  = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==20||theCat==21)",testTreeEventSplitStr.Data());
    TCut cutTestWWTT  = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==22||theCat==0)",testTreeEventSplitStr.Data());

    mvaTree->Add("/work/submit/ceballos/mva_samples/ntupleZAna_ltype0_year2027.root");
    mvaTree->Add("/work/submit/ceballos/mva_samples/ntupleZAna_ltype1_year2027.root");
    mvaTree->Add("/work/submit/ceballos/mva_samples/ntupleZAna_ltype2_year2027.root");

    dataloader->AddTree(mvaTree, "Signal"    , 1.0, cutTrainWWLX, "train");
    dataloader->AddTree(mvaTree, "Background", 1.0, cutTrainWWTT, "train");
    dataloader->AddTree(mvaTree, "Signal"    , 1.0, cutTestWWLX , "test");
    dataloader->AddTree(mvaTree, "Background", 1.0, cutTestWWTT , "test");
    //dataloader->SetWeightExpression("abs(weight)", "Signal"    );
    //dataloader->SetWeightExpression("abs(weight)", "Background");
    dataloader->SetWeightExpression("1.0", "Signal"    );
    dataloader->SetWeightExpression("1.0", "Background");
  }
  else if(nsel == 2){ // LL vs. TX
    TCut cutTrainWWLL = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==20)",trainTreeEventSplitStr.Data());
    TCut cutTrainWWTX = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==21||theCat==22||theCat==0)",trainTreeEventSplitStr.Data());
    TCut cutTestWWLL  = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==20)",testTreeEventSplitStr.Data());
    TCut cutTestWWTX  = Form("%s && vbs_ptj1 > 50 && vbs_ptj2 > 50 && (theCat==21||theCat==22||theCat==0)",testTreeEventSplitStr.Data());

    mvaTree->Add("/work/submit/ceballos/mva_samples/ntupleZAna_ltype0_year2027.root");
    mvaTree->Add("/work/submit/ceballos/mva_samples/ntupleZAna_ltype1_year2027.root");
    mvaTree->Add("/work/submit/ceballos/mva_samples/ntupleZAna_ltype2_year2027.root");

    dataloader->AddTree(mvaTree, "Signal"    , 1.0, cutTrainWWLL, "train");
    dataloader->AddTree(mvaTree, "Background", 1.0, cutTrainWWTX, "train");
    dataloader->AddTree(mvaTree, "Signal"    , 1.0, cutTestWWLL , "test");
    dataloader->AddTree(mvaTree, "Background", 1.0, cutTestWWTX , "test");
    //dataloader->SetWeightExpression("abs(weight)", "Signal"    );
    //dataloader->SetWeightExpression("abs(weight)", "Background");
    dataloader->SetWeightExpression("1.0", "Signal"    );
    dataloader->SetWeightExpression("1.0", "Background");
  }

  if(nsel == 0 || nsel == 1 || nsel == 2){
    if(version >= 10) dataloader->AddVariable("ngood_jets"    ,"ngood_jets"    ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_mjj"       ,"vbs_mjj"       ,"",'F');
    if(version >= 10) dataloader->AddVariable("vbs_ptjj"      ,"vbs_ptjj"      ,"",'F');
    if(version >=  8) dataloader->AddVariable("vbs_detajj"    ,"vbs_detajj"    ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_dphijj"    ,"vbs_dphijj"    ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_ptj1"      ,"vbs_ptj1"      ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_ptj2"      ,"vbs_ptj2"      ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_etaj1"     ,"vbs_etaj1"     ,"",'F');
    if(version >=  8) dataloader->AddVariable("vbs_etaj2"     ,"vbs_etaj2"     ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_zepvv"     ,"vbs_zepvv"     ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_zepmax"    ,"vbs_zepmax"    ,"",'F');
    if(version >=  9) dataloader->AddVariable("vbs_sumHT"     ,"vbs_sumHT"     ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_ptvv"      ,"vbs_ptvv"      ,"",'F');
    if(version >= 10) dataloader->AddVariable("vbs_pttot"     ,"vbs_pttot"     ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_detavvj1"  ,"vbs_detavvj1"  ,"",'F');
    if(version != 99) dataloader->AddVariable("vbs_detavvj2"  ,"vbs_detavvj2"  ,"",'F');
    if(version >= 10) dataloader->AddVariable("vbs_ptbalance" ,"vbs_ptbalance" ,"",'F');
    if(version != 99) dataloader->AddVariable("mllDef"	      ,"mllDef"        ,"",'F');
    if(version >=  9) dataloader->AddVariable("ptllDef"       ,"ptllDef"       ,"",'F');
    if(version != 99) dataloader->AddVariable("drllDef"       ,"drllDef"       ,"",'F');
    if(version != 99) dataloader->AddVariable("dphillDef"     ,"dphillDef"     ,"",'F');
    if(version != 99) dataloader->AddVariable("ptl1Def"       ,"ptl1Def"       ,"",'F');
    if(version != 99) dataloader->AddVariable("ptl2Def"       ,"ptl2Def"       ,"",'F');
    if(version != 99) dataloader->AddVariable("dPhilMETMinDef","dPhilMETMinDef","",'F');
    if(version >=  9) dataloader->AddVariable("minPMETDef"    ,"minPMETDef"    ,"",'F');
    if(version >=  9) dataloader->AddVariable("ptwwDef"       ,"ptwwDef"       ,"",'F');
    if(version >=  9) dataloader->AddVariable("mcollDef"      ,"mcollDef"      ,"",'F');
    if(version != 99) dataloader->AddVariable("mtwmaxDef"     ,"mtwmaxDef"     ,"",'F');
    if(version != 99) dataloader->AddVariable("mtwminDef"     ,"mtwminDef"     ,"",'F');
    if(version != 99) dataloader->AddVariable("PuppiMET_ptDef","PuppiMET_ptDef","",'F');
  }

  TString prepareOptions="NormMode=None";
    prepareOptions+=":SplitMode=Block"; // use e.g. all events selected by trainTreeEventSplitStr for training
    prepareOptions+=":MixMode=Random";
  dataloader->PrepareTrainingAndTestTree("", prepareOptions);

  TString hyperparameters;

  hyperparameters=
  "!H:!V:NTrees=1000:BoostType=Grad:MinNodeSize=5%:NegWeightTreatment=IgnoreNegWeightsInTraining:Shrinkage=0.10:UseBaggedBoost:GradBaggingFraction=0.3:nCuts=1000:MaxDepth=3";
  factory->BookMethod(dataloader, TMVA::Types::kBDT, Form("BDTG_%s",extraString.Data()), hyperparameters);

  TString layoutString ("Layout=TANH|100,TANH|50,TANH|10,LINEAR");

  TString training0 ("LearningRate=1e-1,Momentum=0.0,Repetitions=1,ConvergenceSteps=300,BatchSize=20,TestRepetitions=15,WeightDecay=0.001,Regularization=NONE,DropConfig=0.0+0.5+0.5+0.5,DropRepetitions=1,Multithreading=True");
  TString training1 ("LearningRate=1e-2,Momentum=0.5,Repetitions=1,ConvergenceSteps=300,BatchSize=30,TestRepetitions=7,WeightDecay=0.001,Regularization=L2,Multithreading=True,DropConfig=0.0+0.1+0.1+0.1,DropRepetitions=1");
  TString training2 ("LearningRate=1e-2,Momentum=0.3,Repetitions=1,ConvergenceSteps=300,BatchSize=40,TestRepetitions=7,WeightDecay=0.0001,Regularization=L2,Multithreading=True");
  TString training3 ("LearningRate=1e-3,Momentum=0.1,Repetitions=1,ConvergenceSteps=200,BatchSize=70,TestRepetitions=7,WeightDecay=0.0001,Regularization=NONE,Multithreading=True");
  
  TString trainingStrategyString ("TrainingStrategy=");
  //trainingStrategyString += training0 + "|" + training1 + "|" + training2 + "|" + training3;
  trainingStrategyString += training0 + "|" + training1 + "|" + training2;

  // General Options.
  TString dnnOptions ("!H:V:ErrorStrategy=CROSSENTROPY:VarTransform=N:"
                      "WeightInitialization=XAVIERUNIFORM");
  dnnOptions.Append (":"); dnnOptions.Append (layoutString);
  dnnOptions.Append (":"); dnnOptions.Append (trainingStrategyString);
  
  // Standard implementation, no dependencies.
  TString stdOptions = dnnOptions + ":Architecture=CPU";
  if(dodnn)
    factory->BookMethod(dataloader, TMVA::Types::kDNN, "DNN", stdOptions);

  if(moreMVAs){
  hyperparameters=
  "!H:!V:BoostType=AdaBoost:MinNodeSize=5%:NegWeightTreatment=IgnoreNegWeightsInTraining:SeparationType=MisClassificationError:NTrees=1000:MaxDepth=3:AdaBoostBeta=0.12:nCuts=10000";
  factory->BookMethod(dataloader, TMVA::Types::kBDT, Form("BDTA_%s",extraString.Data()), hyperparameters);

  hyperparameters=
  "!H:!V:VarTransform=None";
  factory->BookMethod(dataloader, TMVA::Types::kHMatrix, Form("HMatrix_%s",extraString.Data()), hyperparameters);

  hyperparameters=
  "!H:!V:!TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmooth=5:NAvEvtPerBin=70:VarTransform=PCA";
  factory->BookMethod(dataloader, TMVA::Types::kLikelihood, Form("LikelihoodPCA_%s",extraString.Data()), hyperparameters);

  hyperparameters=
  "!H:!V:TransformOutput:PDFInterpol=Spline2:NSmoothSig[0]=20:NSmoothBkg[0]=20:NSmoothBkg[1]=10:NSmooth=1:NAvEvtPerBin=70";
  factory->BookMethod(dataloader, TMVA::Types::kLikelihood, Form("Likelihood_%s",extraString.Data()), hyperparameters);

  hyperparameters=
  "!H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=40:NsmoothMVAPdf=10";
  factory->BookMethod(dataloader, TMVA::Types::kFisher, Form("Fisher_%s",extraString.Data()), hyperparameters);

  hyperparameters=
  "!H:!V:!TransformOutput:PDFInterpol=KDE:KDEtype=Gauss:KDEiter=Adaptive:KDEFineFactor=0.3:KDEborder=None:NAvEvtPerBin=70";
  factory->BookMethod(dataloader, TMVA::Types::kLikelihood, Form("LikelihoodKDE_%s",extraString.Data()), hyperparameters);

  hyperparameters=
  "H:!V:Boost_Num=30:Boost_Transform=log:Boost_Type=AdaBoost:Boost_AdaBoostBeta=0.3:!Boost_DetailedMonitoring";
  factory->BookMethod(dataloader, TMVA::Types::kFisher, Form("BoostedFisher_%s",extraString.Data()), hyperparameters);

   hyperparameters=
  "!H:!V:NeuronType=tanh:VarTransform=N:NCycles=1000:HiddenLayers=N+3:TestRate=5:!UseRegulator";
  factory->BookMethod(dataloader, TMVA::Types::kMLP, Form("MLP_%s",extraString.Data()), hyperparameters);
  }

  factory->TrainAllMethods();
  factory->TestAllMethods();
  factory->EvaluateAllMethods();
  output_file->Close();
}

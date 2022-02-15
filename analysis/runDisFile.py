import ROOT
import time
import subprocess
import os
import argparse
import re
from string import Template
import sys

# Command line options
parser = argparse.ArgumentParser(description="cmsDriver")
parser.add_argument("-a", "--action", default="del", help="del for Delete. run for Run.")
args = parser.parse_args()

action = args.action
# Timer
sw = ROOT.TStopwatch()
sw.Start()

DATASET = []

do2018 = True
do2017 = False

doMCspin2_du1p5 = False
doMCspin2_du1p9 = False
doMCspin2_du1p1 = False

doMC_SM = False
doMCspin0_du1p5 = False
doMCspin0_du1p9 = False
doMCspin0_du1p1 = False

doQCD = False
doGJets = False
doGGJets = False

#doAllBkg = doQCD and doGJets and doGGJets

numevents = 100000

#Templates
class_Ctemp     = "ClassTemplateisEBEB.C"
class_htemp     = "ClassTemplateisEBEB.h"
run_analyzetemp = "analyzeTemplate.C"

ntuple_path = "root://cmseos.fnal.gov//store/user/cuperez/"

# sm background
if doQCD:
    if do2017:
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/crab_QCD_Pt_50to80_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034131/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/crab_QCD_Pt_50to80_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v2__MINIAODSIM/201002_034115/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/crab_QCD_Pt_80to120_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v2__MINIAODSIM/201002_034149/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/crab_QCD_Pt_80to120_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034205/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/crab_QCD_Pt_120to170_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034223/0000//*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/crab_QCD_Pt_170to300_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034256/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/crab_QCD_Pt_170to300_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v2__MINIAODSIM/201002_034241/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/crab_QCD_Pt_300to470_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034332/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/crab_QCD_Pt_300to470_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v3__MINIAODSIM/201002_034315/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/crab_QCD_Pt_470to600_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034406/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/crab_QCD_Pt_470to600_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v3__MINIAODSIM/201002_034350/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_600to800_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034443/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_600to800_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v2__MINIAODSIM/201002_034426/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/crab_QCD_Pt_800to1000_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034517/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/crab_QCD_Pt_800to1000_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v2__MINIAODSIM/201002_034501/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v2__MINIAODSIM/201002_034535/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034552/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034609/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/3104b1c/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v3__MINIAODSIM/201002_033825/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034626/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/crab_QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034642/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/crab_QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM/201002_034717/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/crab_QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8__Fall17_94X_mc2017_realistic_v14_ext1-v1__MINIAODSIM/201002_034700/0000/*.root");

    if do2018:
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/crab_QCD_Pt_50to80_TuneCP5_13TeV_pythia8__Autumn18_ext1-v2__MINIAODSIM/201002_034734/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_50to80_TuneCP5_13TeV_pythia8/crab_QCD_Pt_50to80_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_034749/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_80to120_TuneCP5_13TeV_pythia8/crab_QCD_Pt_80to120_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_034807/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_120to170_TuneCP5_13TeV_pythia8/crab_QCD_Pt_120to170_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_034826/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_170to300_TuneCP5_13TeV_pythia8/crab_QCD_Pt_170to300_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_034843/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_300to470_TuneCP5_13TeV_pythia8/crab_QCD_Pt_300to470_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_034900/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/crab_QCD_Pt_470to600_TuneCP5_13TeV_pythia8__Autumn18_ext1-v2__MINIAODSIM/201002_034919/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_470to600_TuneCP5_13TeV_pythia8/crab_QCD_Pt_470to600_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_034934/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_600to800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_600to800_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_034951/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_800to1000_TuneCP5_13TeV_pythia8/crab_QCD_Pt_800to1000_TuneCP5_13TeV_pythia8__Autumn18_ext1-v2__MINIAODSIM/201002_035008/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1000to1400_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_035026/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8__Autumn18_ext1-v2__MINIAODSIM/201002_035043/0000/*.root");
        #// /QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1/MINIAODSIM is not available
        #// since the dataset has the same number of events as the other QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8 dataset and the dataset sizes are identical, just add the dataset twice
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1400to1800_TuneCP5_13TeV_pythia8__Autumn18_ext1-v2__MINIAODSIM/201002_035043/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_035134/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8/crab_QCD_Pt_1800to2400_TuneCP5_13TeV_pythia8__Autumn18_ext1-v2__MINIAODSIM/201002_035116/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/crab_QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_035207/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8/crab_QCD_Pt_2400to3200_TuneCP5_13TeV_pythia8__Autumn18_ext1-v2__MINIAODSIM/201002_035151/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/crab_QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8__Autumn18-v1__MINIAODSIM/201002_035243/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/dc44792/QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8/crab_QCD_Pt_3200toInf_TuneCP5_13TeV_pythia8__Autumn18_ext2-v2__MINIAODSIM/201002_035226/0000/*.root");

if doGJets:
    if do2017:
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8__Fall17-v2__MINIAODSIM_resub/200904_235904/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8__Fall17-v1__MINIAODSIM_resub/200905_000007/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8__Fall17-v1__MINIAODSIM_resub/200905_000330/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8__Fall17-v1__MINIAODSIM_resub/200905_000726/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8__Fall17-v2__MINIAODSIM_resub/200905_000637/0000/*.root");
    if do2018:
        DATASET.append(ntuple_path+"diphoton_closure/11c96ff/GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic/200821_031620/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/11c96ff/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIAutumn18MiniAOD-4cores5k_102X_upgrade2018/200821_021447/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/11c96ff/GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIAutumn18MiniAOD-102X_upgrade2018_realisti/200821_023518/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/11c96ff/GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIAutumn18MiniAOD-102X_upgrade2018_realisti/200821_025548/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/11c96ff/GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8/crab_GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8__RunIIAutumn18MiniAOD-102X_upgrade2018_realisti/200821_033205/0000/*.root");

if doGGJets:
    if do2017:
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GGJets_M-60To200_Pt-50_13TeV-sherpa/crab_GGJets_M-60To200_Pt-50_13TeV-sherpa__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM_resub/200904_233439/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GGJets_M-200To500_Pt-50_13TeV-sherpa/crab_GGJets_M-200To500_Pt-50_13TeV-sherpa__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM_resub/200904_232918/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GGJets_M-500To1000_Pt-50_13TeV-sherpa/crab_GGJets_M-500To1000_Pt-50_13TeV-sherpa__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM_resub/200904_233026/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GGJets_M-1000To2000_Pt-50_13TeV-sherpa/crab_GGJets_M-1000To2000_Pt-50_13TeV-sherpa__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM_resub/200904_232739/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GGJets_M-2000To4000_Pt-50_13TeV-sherpa/crab_GGJets_M-2000To4000_Pt-50_13TeV-sherpa__Fall17_94X_mc2017_realistic_v14-v2__MINIAODSIM_resub/200904_233559/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GGJets_M-4000To6000_Pt-50_13TeV-sherpa/crab_GGJets_M-4000To6000_Pt-50_13TeV-sherpa__Fall17_94X_mc2017_realistic_v14-v2__MINIAODSIM_resub/200904_233641/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GGJets_M-6000To8000_Pt-50_13TeV-sherpa/crab_GGJets_M-6000To8000_Pt-50_13TeV-sherpa__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM_resub/200904_233321/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/2c8bbea/GGJets_M-8000To13000_Pt-50_13TeV-sherpa/crab_GGJets_M-8000To13000_Pt-50_13TeV-sherpa__Fall17_94X_mc2017_realistic_v14-v1__MINIAODSIM_resub/200904_233735/0000/*.root");
    if do2018:
        DATASET.append(ntuple_path+"diphoton_closure/27a1c52/GGJets_M-500To1000_Pt-50_13TeV-sherpa/crab_GGJets_M-500To1000_Pt-50_13TeV-sherpa__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1__MINI/200730_042411/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/27a1c52/GGJets_M-8000To13000_Pt-50_13TeV-sherpa/crab_GGJets_M-8000To13000_Pt-50_13TeV-sherpa__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1__MI/200730_151230/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/27a1c52/GGJets_M-2000To4000_Pt-50_13TeV-sherpa/crab_GGJets_M-2000To4000_Pt-50_13TeV-sherpa__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1__MIN/200730_151014/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/27a1c52/GGJets_M-6000To8000_Pt-50_13TeV-sherpa/crab_GGJets_M-6000To8000_Pt-50_13TeV-sherpa__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1__MIN/200730_151138/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/27a1c52/GGJets_M-4000To6000_Pt-50_13TeV-sherpa/crab_GGJets_M-4000To6000_Pt-50_13TeV-sherpa__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1__MIN/200730_151111/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/27a1c52/GGJets_M-1000To2000_Pt-50_13TeV-sherpa/crab_GGJets_M-1000To2000_Pt-50_13TeV-sherpa__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1__MIN/200730_150946/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/27a1c52/GGJets_M-60To200_Pt-50_13TeV-sherpa/crab_GGJets_M-60To200_Pt-50_13TeV-sherpa__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1__MINIAO/200730_151203/0000/*.root");
        DATASET.append(ntuple_path+"diphoton_closure/27a1c52/GGJets_M-200To500_Pt-50_13TeV-sherpa/crab_GGJets_M-200To500_Pt-50_13TeV-sherpa__RunIIAutumn18MiniAOD-102X_upgrade2018_realistic_v15-v1__MINIA/200730_151042/0000/*.root");



# spin 0
if doMCspin0_du1p1:
    du_tag = ""
    if do2018:
        DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201633/0000/*.root");
	DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201654/0000/*.root");
	DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201715/0000/*.root");
	DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201735/0000/*.root");

	DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201756/0000/*.root");
	DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201816/0000/*.root");
	DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201836/0000/*.root");
	DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201856/0000/*.root");

	#DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201916/0000/*.root");
	#DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Autumn18-v2__MINIAODSIM/210930_201938/0000/*.root");
	#DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201958/0000/*.root");
	#DATASET.append(ntuple_path+"UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202036/0000/*.root");


for dset in DATASET:
    if "QCD" in dset:
        pattern = "crab_([^(]*)_Pt_([^(]*)_TuneCP5_13TeV_pythia8__([^(]*)"
        match = re.findall(pattern, dset)
        PH, pTrange, run_year = match[0]

        classname = "Class%s_pT%s_%s" %(PH, pTrange, run_year)
        classname = classname.replace('-', '_')
        an_func = "analyze_%s" %(classname)
        outfile = "%s.root" %(classname)

    if "GJets":
        pattern = "crab_([^(]*)_HT-([^(]*)_TuneCP5_13TeV-madgraphMLM-pythia8__([^(]*)"
        match = re.findall(pattern, dset)
        PH, hTrange, run_year = match[0]

        classname = "Class%s_pT%s_%s" %(PH, hTrange, run_year)
        classname = classname.replace('-', '_')
        an_func = "analyze_%s" %(classname)
        outfile = "%s.root" %(classname)

    if "GGJets":
        pattern = "crab_([^(]*)_M-([^(]*)_Pt-([^(]*)_13TeV-sherpa__([^(]*)MiniAOD-102X_upgrade2018_realistic_v15-v1__MINI"
        match = re.findall(pattern, dset)
        PH, massrange, pTcut run_year = match[0]

        classname = "Class%s_pT%s_%s" %(PH, hTrange, run_year)
        classname = classname.replace('-', '_')
        an_func = "analyze_%s" %(classname)
        outfile = "%s.root" %(classname)

    if "Unp" in dset:
        pattern = "crab_UnparToGG_Spin([^(]*)_du([^(]*)_LambdaU-([^(]*)_pT([^(]*)_M([^(]*)_TuneCP2_13TeV_pythia8__([^(]*)-v1"
        match = re.findall(pattern, dset)
        PH = "Unp"
        spin, du, LambdaU, pTcut, massrange, run_year = match[0]

    print match

    # Get Cross-section
    keypattern = "Test([^(]*)_GEN.root"
    matchkey = re.findall(keypattern, dset)
    #xseckey = matchkey[0]
    mrange = massrange.replace('-', '_')

    if "Unp" in dset:
        classname = "Class%s_spin%s_du%s_LU%s_pT%s_M%s_%s" %(PH, spin, du, LambdaU, pTcut, mrange, run_year)
        classname = classname.replace('-', '_')
        an_func = "analyze_%s" %(classname)
        outfile = "%s_spin%s_du%s_LU%s_pT%s_M%s_%s.root" %(PH, spin, du, LambdaU, pTcut, mrange, run_year)
        #print classname

    # Template Replacements
    cmssw_base = os.getenv("CMSSW_BASE")
    #print cmssw_base
    rep = {'ClassANGGJets': classname,
           "outputfile": outfile,
           "inputTree": dset,
           "analyzefunc": an_func,
           "numevents": numevents,
           }

    #Read and replace template file
    C_src = Template(open(class_Ctemp).read())
    C_sub = C_src.substitute(rep)

    h_src = Template(open(class_htemp).read())
    h_sub = h_src.substitute(rep)

    an_src = Template(open(run_analyzetemp).read())
    an_sub = an_src.substitute(rep)

    #write to file
    outfile_C = open("%s.C" %(classname), "w+")
    outfile_C.write(C_sub)

    outfile_h = open("%s.h" %(classname), "w+")
    outfile_h.write(h_sub)

    outfile_an = open("analyze_%s.C" %(classname), "w+")
    outfile_an.write(an_sub)

def RunAnalyze(file_list):
	for anFile in file_list:
		if anFile.startswith("analyze_Class") and anFile.endswith(".C"):
			root_cmd = "root -l -q %s" %(anFile)
			os.system(root_cmd)
def DelClassFiles(file_list):
    for classFile in file_list:
        if "Class_SM" in classFile:
            del_cmd = "rm %s" %(classFile)
            os.system(del_cmd)
        if "ClassUnp" in classFile:
            del_cmd = "rm %s" %(classFile)
            #print del_cmd
            os.system(del_cmd)
    print "deleted auxilliary files"

if action == "run":
    RunAnalyze(os.listdir('.'))
if action == "del":
    DelClassFiles(os.listdir('.'))

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"

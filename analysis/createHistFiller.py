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
parser.add_argument('-s', '--spin', help='spin 0 or 2', type=int, default=None)
parser.add_argument('-d', '--du', help='du 1p1, 1p5, 1p9 are available', type=str, default=None)
parser.add_argument('-b', '--background', help='run leading order background', type=bool, default=False)
parser.add_argument('-e', '--etaBin', help='BB or BE', type=str, default="BB")
parser.add_argument('-y', '--year', help='2017 and 2018', type=str, default="2017")
args = parser.parse_args()
#FIXME: Command line options for filler

action = args.action
etaBin = args.etaBin
year   = args.year

if etaBin == "BB":
    etaCut = "Photon1_isEB && Photon2_isEB"
if etaBin == "BE":
    etaCut = "( (Photon1_isEB && Photon2_isEE) || (Photon2_isEB &&  Photon1_isEE ))"

# Timer
sw = ROOT.TStopwatch()
sw.Start()

DATASET = []

# do2017 = True
doMCBkgGG = True if args.background else False
doMCspin0 = True if args.spin == 0 else False
doMCspin2 = True if args.spin == 2 else False
doMCdu1p1 = True if args.du == "1p1" else False
doMCdu1p5 = True if args.du == "1p5" else False
doMCdu1p9 = True if args.du == "1p9" else False
do2017    = True if year == "2017" else False
do2018    = True if year == "2018" else False

doMCspin2_du1p5_2017 = doMCspin2 and doMCdu1p5 and do2017
doMCspin2_du1p9_2017 = doMCspin2 and doMCdu1p9 and do2017
doMCspin2_du1p1_2017 = doMCspin2 and doMCdu1p1 and do2017

doMCspin0_du1p5_2017 = doMCspin0 and doMCdu1p5 and do2017
doMCspin0_du1p9_2017 = doMCspin0 and doMCdu1p5 and do2017
doMCspin0_du1p1_2017 = doMCspin0 and doMCdu1p5 and do2017

doMCspin2_du1p5_2018 = doMCspin2 and doMCdu1p5 and do2018
doMCspin2_du1p9_2018 = doMCspin2 and doMCdu1p9 and do2018
doMCspin2_du1p1_2018 = doMCspin2 and doMCdu1p1 and do2018

doMCspin0_du1p5_2018 = doMCspin0 and doMCdu1p5 and do2018
doMCspin0_du1p9_2018 = doMCspin0 and doMCdu1p5 and do2018
doMCspin0_du1p1_2018 = doMCspin0 and doMCdu1p5 and do2018

### Cannot Run Background and Signal at the same time
doSM_gg70_2017 = doMCBkgGG and do2017
doSM_gg70_2018 = doMCBkgGG and do2018

numevents = 100000

#Templates
class_Ctemp     = "Templates/ClassTemplate.C"
class_htemp     = "Templates/ClassTemplate.h"
run_analyzetemp = "Templates/analyzeTemplate.C"

# ntuple_path = "root://cmseos.fnal.gov//store/user/cuperez/"
# if doSM_gg70: ntuple_path = "root://cmseos.fnal.gov//store/user/cawest/"

baseDirectory = "root://cmseos.fnal.gov/"
#### 2018
if doSM_gg70_2018:
    DATASET.append(baseDirectory + "/store/user/cawest/diphoton/cba3996/GG_M-500To1000_Pt70_TuneCP2_13TeV-pythia8/crab_GG_M-500To1000_Pt70_TuneCP2_13TeV-pythia8__Autumn18-v1__MINIAODSIM/210715_213601/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cawest/diphoton/cba3996/GG_M-1000To2000_Pt70_TuneCP2_13TeV-pythia8/crab_GG_M-1000To2000_Pt70_TuneCP2_13TeV-pythia8__Autumn18-v1__MINIAODSIM/210715_213628/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cawest/diphoton/cba3996/GG_M-2000To4000_Pt70_TuneCP2_13TeV-pythia8/crab_GG_M-2000To4000_Pt70_TuneCP2_13TeV-pythia8__Autumn18-v1__MINIAODSIM/210715_213653/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cawest/diphoton/cba3996/GG_M-4000To13000_Pt70_TuneCP2_13TeV-pythia8/crab_GG_M-4000To13000_Pt70_TuneCP2_13TeV-pythia8__Autumn18-v1__MINIAODSIM/210715_213719/0000/*.root");

if doMCspin2_du1p1_2018:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202804/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202833/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202856/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202916/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202937/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202957/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203018/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203039/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203059/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203120/0000/*.root");

if doMCspin2_du1p5_2018:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203140/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203202/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203238/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203258/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203319/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203344/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v3__MINIAODSIM/210930_203404/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203425/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203445/0000/*.root");

if doMCspin2_du1p9_2018:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203527/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_203548/0000/*.root");
    #
    # DATASET.append(baseDirectory +
    # DATASET.append(baseDirectory +
    # DATASET.append(baseDirectory +
    #
    # DATASET.append(baseDirectory +
    # DATASET.append(baseDirectory +
    # DATASET.append(baseDirectory +
    # DATASET.append(baseDirectory +

if doMCspin0_du1p1_2018:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201633/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201654/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201715/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201735/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201756/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201816/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201836/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201856/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201916/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Autumn18-v2__MINIAODSIM/210930_201938/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M4000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_201958/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202036/0000/*.root");

if doMCspin0_du1p5_2018:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202057/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202117/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202138/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202200/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202221/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202241/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202303/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202324/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202344/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202405/0000/*.root");

if doMCspin0_du1p9_2018:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202440/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202501/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202522/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202542/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Autumn18-v2__MINIAODSIM/210930_202602/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202622/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202642/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202702/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202723/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Autumn18-v1__MINIAODSIM/210930_202744/0000/*.root");


#### 2017
if doMCspin2_du1p1_2017:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145957/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160036/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_150036/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_160050/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_150058/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160104/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_150120/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160117/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_160131/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_150205/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160145/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160159/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_150253/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160214/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_150315/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_160228/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p1_LambdaU-3000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160244/0000/*.root");
if doMCspin0_du1p1_2017:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAO/211005_144717/0000/*root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAO/211005_155103/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAO/211005_155146/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_144803/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155257/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_144838/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-10000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155314/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155328/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_144924/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155343/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_144946/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155358/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_145007/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-4000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_155413/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145032/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155426/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145054/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M2000-4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M2000-4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155441/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_145116/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M4000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M4000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155455/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_145141/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p1_LambdaU-8000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_155510/0000/*.root");

if doMCspin0_du1p9_2017:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145555/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155755/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155810/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_155824/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155838/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_145733/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155851/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v2__MINIAODS/211005_145755/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v2__MINIAODS/211005_155905/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145816/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155919/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145838/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155933/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_145900/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155946/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p9_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160002/0000/*.root");
if doMCspin2_du1p9_2017:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_150814/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160531/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_150837/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_160545/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160558/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_150922/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160612/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_160626/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_151007/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160640/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160654/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_151051/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160711/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_160731/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p9_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160751/0000/*.root");


if doMCspin2_du1p5_2017:
    #2000, 2500, 3000
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160258/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v2__MINIAODSIM/211005_150439/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v2__MINIAODSIM/211005_160313/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_150511/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160329/0000/*.root");

    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_150534/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160343/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_150554/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_160357/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_150622/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160414/0000/*.root");

    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_150646/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160433/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_150707/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_160448/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_160502/0000/*.root");

    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_150753/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cuperez/UnparticlesGG/UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin2_du1p5_LambdaU-3000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_160517/0000/*.root");

if doMCspin0_du1p5_2017:
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155527/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_145238/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155542/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_145259/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2000_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_155556/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145321/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155611/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155629/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-2500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_155643/0000/*.root");

    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145427/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M1000-2000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155657/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_145448/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M2000-3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAOD/211005_155713/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_145509/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M3000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODSIM/211005_155727/0000/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_145531/*.root");
    DATASET.append(baseDirectory + "/store/user/cuperez/UnparticlesGG/UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8/crab_UnparToGG_Spin0_du1p5_LambdaU-3500_pT70_M500-1000_TuneCP2_13TeV_pythia8__Fall17_PU2017-v1__MINIAODS/211005_155741/*.root");

if doSM_gg70_2017:
    DATASET.append(baseDirectory+"/store/user/cawest/diphoton/cba3996/GG_M-500To1000_Pt70_TuneCP2_13TeV-pythia8/crab_GG_M-500To1000_Pt70_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/210715_233628/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cawest/diphoton/cba3996/GG_M-1000To2000_Pt70_TuneCP2_13TeV-pythia8/crab_GG_M-1000To2000_Pt70_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/210715_213442/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cawest/diphoton/cba3996/GG_M-2000To4000_Pt70_TuneCP2_13TeV-pythia8/crab_GG_M-2000To4000_Pt70_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/210715_213509/0000/*.root");
    DATASET.append(baseDirectory+"/store/user/cawest/diphoton/cba3996/GG_M-4000To13000_Pt70_TuneCP2_13TeV-pythia8/crab_GG_M-4000To13000_Pt70_TuneCP2_13TeV-pythia8__Fall17_PU2017-v1__MINIAODSIM/210715_213535/0000/*.root");

##### Filenames and Processing
for dset in DATASET:
    # if "GG" in dset:
    if doMCBkgGG:
        pattern = "crab_([^(]*)_M-([^(]*)_Pt([^(]*)_TuneCP2_13TeV-pythia8__([^(]*)-v1__MINIAODSIM"
        match = re.findall(pattern, dset)
        PH, massrange, pTcut, run_year = match[0]

        classname = "Class%s_pT%s_M%s_%s_%s" %(PH, pTcut, massrange, run_year, etaBin)
        classname = classname.replace('-', '_')
        an_func = "analyze_%s" %(classname, )
        outfile = "%s_pT%s_M%s_%s_%s.root" %(PH, pTcut, massrange, year, etaBin)

    if "Unp" in dset:

        pattern = "crab_UnparToGG_Spin([^(]*)_du([^(]*)_LambdaU-([^(]*)_pT([^(]*)_M([^(]*)_TuneCP2_13TeV_pythia8__([^(]*)-v"
        match = re.findall(pattern, dset)
        PH = "Unp"
        spin, du, LambdaU, pTcut, massrange, run_year = match[0]

    print match

    # Get Cross-section
    keypattern = "Test([^(]*)_GEN.root"
    matchkey = re.findall(keypattern, dset)
    #xseckey = matchkey[0]
    if "GJets" not in dset:
        mrange = massrange.replace('-', '_')

    if "Unp" in dset:
        classname = "Class%s_spin%s_du%s_LU%s_pT%s_M%s_%s_%s" %(PH, spin, du, LambdaU, pTcut, mrange, run_year, etaBin)
        classname = classname.replace('-', '_')
        an_func = "analyze_%s" %(classname)
        outfile = "%s_spin%s_du%s_LU%s_pT%s_M%s_%s_%s.root" %(PH, spin, du, LambdaU, pTcut, mrange, year, etaBin)
        #print classname

    # Template Replacements
    cmssw_base = os.getenv("CMSSW_BASE")
    #print cmssw_base
    rep = {'ClassANGGJets': classname,
           "outputfile": outfile,
           "inputTree": dset,
           "analyzefunc": an_func,
           "numevents": numevents,
           "etaCut": etaCut
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
        if "ClassGG" in classFile:
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

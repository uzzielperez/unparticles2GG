#!/usr/bin/python

import ROOT
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
import re
#from hep_plt.Sensitivityfunctions import CalcSensitivity
from hep_plt.Plotfunctions import *

sw = ROOT.TStopwatch()
sw.Start()
gStyle.SetOptStat(0)

doSM = False
dospin0du1p5 = False
dospin0du1p1 = True
dospin0du1p9 = False

dospin2du1p1 = False
dospin2du1p5 = False
dospin2du1p9 = False

HISTS_TO_OVERLAY, labelList = [], []
TempHistsList, templabelList = [None]*4, [None]*4

infile_path = "../analysis/"

def PlotSets(output="overlay"):
    histA, labelA = Stitch(DATASET_A, "gendiphotonMinv")
    histB, labelB = Stitch(DATASET_B, "gendiphotonMinv")
    histC, labelC = Stitch(DATASET_C, "gendiphotonMinv")

    TempHistsList[1], templabelList[1] = histA, labelA
    TempHistsList[2], templabelList[2] = histB, labelB
    TempHistsList[3], templabelList[3] = histC, labelC

    HISTS_TO_OVERLAY.append(histA)
    HISTS_TO_OVERLAY.append(histB)
    HISTS_TO_OVERLAY.append(histC)

    labelList.append(labelA)
    labelList.append(labelB)
    labelList.append(labelC)

    # Calculate Sensitivity
    #CalcSensitivity("gendiphotonMinv", TempHistsList, 137, templabelList)
    # Plot Histograms (Overlay)
    if output == "overlay":
    	OverlayHists("gendiphotonMinv", TempHistsList, templabelList)

if doSM:
    DATASETSM = []
    DATASETSM.append(infile_path+"OUTSM_pT70_M500_1000.root")
    DATASETSM.append(infile_path+"OUTSM_pT70_M1000_2000.root")
    DATASETSM.append(infile_path+"OUTSM_pT70_M2000_4000.root")
    DATASETSM.append(infile_path+"OUTSM_pT70_M4000.root")

    histSM, labelSM = Stitch(DATASETSM, "gendiphotonMinv")
    HISTS_TO_OVERLAY.append(histSM)
    labelList.append(labelSM)
    TempHistsList[0], templabelList[0] = histSM, labelSM
    print type(histSM)

if dospin2du1p1:
    DATASET_A, DATASET_B, DATASET_C = [], [], []
    DATASET_A.append(infile_path+"OUTUnp_spin0_du1p1_LU10000_pT70_M500_1000.root")
    DATASET_A.append(infile_path+"OUTUnp_spin0_du1p1_LU10000_pT70_M1000_2000_Autumn18.root")
    DATASET_A.append(infile_path+"OUTUnp_spin0_du1p1_LU10000_pT70_M2000_4000_Autumn18.root")
    DATASET_A.append(infile_path+"OUTUnp_spin0_du1p1_LU10000_pT70_M4000_Autumn18.root")

    DATASET_B.append(infile_path+"OUTUnp_spin0_du1p1_LU4000_pT70_M500_1000_Autumn18.root")
    DATASET_B.append(infile_path+"OUTUnp_spin0_du1p1_LU4000_pT70_M1000_2000_Autumn18.root")
    DATASET_B.append(infile_path+"OUTUnp_spin0_du1p1_LU4000_pT70_M2000_4000_Autumn18.root")
    DATASET_B.append(infile_path+"OUTUnp_spin0_du1p1_LU4000_pT70_M4000_Autumn18.root")

    DATASET_C.append(infile_path+"OUTUnp_spin0_du1p1_LU4000_pT70_M500_1000_Autumn18.root")
    DATASET_C.append(infile_path+"OUTUnp_spin0_du1p1_LU4000_pT70_M1000_2000_Autumn18.root")
    DATASET_C.append(infile_path+"OUTUnp_spin0_du1p1_LU4000_pT70_M2000_4000_Autumn18.root")
    DATASET_C.append(infile_path+"OUTUnp_spin0_du1p1_LU4000_pT70_M4000_Autumn18.root")

PlotSets("overlay")
#CalcSensitivity("gendiphotonMinv", HISTS_TO_OVERLAY, 137, labelList)

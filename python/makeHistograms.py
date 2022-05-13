
#!/usr/bin/python

import os
import ROOT
import argparse
import re
import glob
from hep_plt.basicPlots import *

# Register command line options
parser = argparse.ArgumentParser(description='plotting processing options.')
parser.add_argument('-i','--input', help='Input file/s.',default="../analysis/*root", type=str)
parser.add_argument('-o', '--object', help='Object type', default="diphotonMinv", type=str)
parser.add_argument('-s', '--spin', help='spin 0 or 2', type=int)
parser.add_argument('-d', '--du', help='du 1p1, 1p5, 1p9 are available', type=str)
parser.add_argument('-e', '--etaBin', help='BB or BE', type=str, default="BB")
parser.add_argument('-y', '--year', help='2017 and 2018', type=str, default="2017")
parser.add_argument('-a', '--all', help="Run on all", action='store_true')


args = parser.parse_args()

files  = args.input
obj    = args.object
spin   = str(args.spin)
du     = args.du
etaBin = args.etaBin
year   = args.year
run_all = args.all

# insert BB or BE to filename
i = files.find("root")
files = files[:i] + "%s_%s." %(year, etaBin) + files[i:]

spin_du_LambdaMap = { ("0", "1p1") : ["10000", "8000", "4000"],
                      ("0", "1p5") : ["3500", "2500", "2000"],
                      ("0", "1p9") : ["3500", "2500", "2000"],
                      ("2", "1p1") : ["3000", "2500", "2000"],
                      ("2", "1p5") : ["3000", "2500", "2000"],
                      ("2", "1p9") : ["3500", "2500", "2000"]}

LambdaU_values = {'spin0_du1p1' : {4000, 8000, 10000},
                  'spin0_du1p5' : {2000, 2500, 3500},
                  'spin0_du1p9' : {2000, 2500, 3500},
                  'spin2_du1p1' : {2000, 2500, 3000},
                  'spin2_du1p5' : {2000, 2500, 3000},
                  'spin2_du1p9' : {2000, 2500, 3500}}

dimensions = []
dimensions.extend(['spin0_du1p1', 'spin0_du1p5', 'spin0_du1p9', 'spin2_du1p1', 'spin2_du1p5', 'spin2_du1p9'])

if run_all:
    print "Preparing all files"
    print files

    rootname = "Minv_histos_%s_%s.root" %(etaBin, year)
    outfile  = ROOT.TFile(rootname, "RECREATE")
    outfile.cd()

    hB = stitchBkg("GG", obj, files)

    for dimension in dimensions:
        for LambdaU_val in LambdaU_values[dimension]:
            outfile.cd()
            # OUTUnp_spin0_du1p1_LU10000_pT70_M1000_2000_2017_BB.root
            name = "OUTUnp_%s_LU%s--%s_%s.root" %(dimension, LambdaU_val, year, etaBin)

            spin = re.search('spin(.*)_', dimension).group(1)
            du   = re.search('du(.*)', dimension).group(1)
            LU   = re.search('LU(.*)--', name).group(1)

            print "Stitching %s from %s files, spin%s_du%s_LU%s" %(dimension, name, spin, du, LU)
            hS = stitchUnpar(spin , du, LU, files="../analysis/*%s_%s*.root" %(year, etaBin))
            outfile.WriteObject(hS, "Spin%s_du%s_LambdaU-%s" %(spin, du, LU))
    outfile.WriteObject(hB, "hB")
    outfile.Write()
    outfile.Close()

else:
    print ("Preparing spin %s, du %s, Lambdas: " %(spin, du), spin_du_LambdaMap[(spin, du)])

    rootname = "Minv_histos_Spin%s_du%s_%s_%s.root" %(spin, du, etaBin, year)
    outfile  = ROOT.TFile(rootname, "RECREATE")
    outfile.cd()
    print ("Stitching: ", files )
    hB = stitchBkg("GG", obj, files)
    hS1 = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][0], obj, files)
    hS2 = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][1], obj, files)
    hS3 = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][2], obj, files)

    outfile.WriteObject(hB, "hB")
    outfile.WriteObject(hS1, "hS1")
    outfile.WriteObject(hS2, "hS2")
    outfile.WriteObject(hS3, "hS3")

    hR2 = createRatio(hS2, hS1)
    hR3 = createRatio(hS3, hS1)

    outfile.WriteObject(hR2, "hR2")
    outfile.WriteObject(hR3, "hR3")

    outfile.Write()
    outfile.Close()

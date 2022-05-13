#!/usr/bin/python

import os
import ROOT
import argparse
import re
import glob
import csv
import subprocess
from string import Template
import math
from hep_plt.basicPlots import *
from hep_plt.Sensitivityfunctions import *

# Register command line options
parser = argparse.ArgumentParser(description='plotting processing options.')
parser.add_argument('-i','--input', help='Input file/s.',default="../analysis/*root", type=str)
parser.add_argument('-t', '--template', help='Template Data card', default="templates/basicDataCardTemplate.txt")
parser.add_argument('-o', '--object', help='Object type', default="diphotonMinv", type=str)
parser.add_argument('-s', '--spin', help='spin 0 or 2', type=int)
parser.add_argument('-d', '--du', help='du 1p1, 1p5, 1p9 are available', type=str)
parser.add_argument('-l', '--low', help='min mass GeV', default=2000, type=int)
parser.add_argument('-m', '--max', help='max mass GeV', default=13000, type=int)

args = parser.parse_args()

files = args.input
obj   = args.object
spin  = str(args.spin)
du    = args.du
minMass = args.low
maxMass = args.max

### Set up Yields
spin_du_LambdaMap = { ("0", "1p1") : ["10000", "8000", "4000"],
                      ("0", "1p5") : ["3500", "2500", "2000"],
                      ("0", "1p9") : ["3500", "2500", "2000"],
                      ("2", "1p1") : ["3000", "2500", "2000"],
                      ("2", "1p5") : ["3000", "2500", "2000"],
                      ("2", "1p9") : ["3500", "2500", "2000"]}

hB = stitchBkg("GG", obj, files)
Nb  = getHistEvtYields(hB, minMass, maxMass)

### Make Data Card for Model Point Specified

for lambdaV in spin_du_LambdaMap[(spin, du)]:
    hSignal = stitchUnpar(spin, du, lambdaV, obj, files)
    hSignal.Add(hB, -1.0)
    Ns =  getHistEvtYields(hSignal, minMass, maxMass)

    mpoint = "UnparSpin%s_du%s_LU%s" %(spin, du, lambdaV)
    datacardOutName = mpoint +".txt"
    print "Generating data card for %s" %(datacardOutName), Nb, Ns

    ### Substitute Yields to Placeholders in Datacard Template
    dict = {'n_obs':Nb, 'modelPoint': mpoint, 'S':Ns, 'B':Nb}
    datacardTemplate = open(args.template)
    outfile = open(datacardOutName, "w+")
    src  = Template(datacardTemplate.read())
    sub  = src.substitute(dict)
    outfile.write(sub)
    outfile.close()
    datacardTemplate.close()

    # print "Generated %s" %(datacardOutName), Nb, Ns

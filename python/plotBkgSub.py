
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


args = parser.parse_args()

files = args.input
obj   = args.object
spin  = str(args.spin)
du    = args.du
etaBin = args.etaBin

# insert BB or BE to filename
i = files.find("root")
files = files[:i] + "%s." %(etaBin) + files[i:]

# print(files)
# # rootfiles = glob.glob(files)
# # print (rootfiles)

spin_du_LambdaMap = { ("0", "1p1") : ["10000", "8000", "4000"],
                      ("0", "1p5") : ["3500", "2500", "2000"],
                      ("0", "1p9") : ["3500", "2500", "2000"],
                      ("2", "1p1") : ["3000", "2500", "2000"],
                      ("2", "1p5") : ["3000", "2500", "2000"],
                      ("2", "1p9") : ["3500", "2500", "2000"]}

print ("Plotting spin %s, du %s, Lambdas: " %(spin, du), spin_du_LambdaMap[(spin, du)])

canvas = ROOT.TCanvas("canvas")
canvas.cd()
canvas.SetLogy()

hB = stitchBkg("GG", obj, files)
hB.SetLineColor(7)
hB.SetFillColor(7)
hB.Draw("HIST")

hS1b = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][0], obj, files)
hS1b.SetLineColor(2)
hS1b.Add(hB, -1.0)
hS1b.Draw("SAME")

hS2b = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][1], obj, files)
hS2b.SetLineColor(3)
hS2b.Add(hB, -1.0)
hS2b.Draw("SAME")

hS3b = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][2], obj, files)
hS3b.SetLineColor(4)
hS3b.Add(hB, -1.0)
hS3b.Draw("SAME")

t = ROOT.TLatex()
t.SetNDC()
t.SetTextFont( 62 )
t.SetTextColor( 36 )
t.SetTextSize( 0.08 )
t.SetTextAlign( 12 )
t.SetTextSize( 0.05 )
t.DrawLatex( 0.6, 0.70, 'BB, Spin %s, du = %s' %(spin, du) )

legend = ROOT.TLegend(0.7,0.4,0.85,0.65)
legend.AddEntry(hS3b, "#Lambda_{U} = %s" %(spin_du_LambdaMap[(spin, du)][0]))
legend.AddEntry(hS2b, "#Lambda_{U} = %s" %(spin_du_LambdaMap[(spin, du)][1]))
legend.AddEntry(hS1b, "#Lambda_{U} = %s" %(spin_du_LambdaMap[(spin, du)][2]))

legend.AddEntry(hB, "GG")
legend.SetLineWidth(0)
legend.Draw("same")

canvas.SaveAs("out/bkgSub_Unp_Spin%s_Du%s_%s.pdf" %(spin, du, etaBin))

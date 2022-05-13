
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


args = parser.parse_args()

files  = args.input
obj    = args.object
spin   = str(args.spin)
du     = args.du
etaBin = args.etaBin
year   = args.year

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


c = ROOT.TCanvas("c", "c", 800, 800)

pad1 = ROOT.TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
pad1.SetBottomMargin(0)  # joins upper and lower plot
pad1.SetLogy()
pad1.Draw()

c.cd()
pad2 = ROOT.TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
pad2.SetTopMargin(0)  # joins upper and lower plot
pad2.SetBottomMargin(0.2)
pad2.SetGridy()
pad2.Draw()

pad1.cd()
hB = stitchBkg("GG", obj, files)
hB.SetLineColor(7)
hB.SetFillColor(7)
hB.Draw("HIST")

hS1 = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][0], obj, files)
hS1.SetLineColor(2)
hS1.Draw("SAME")

hS2 = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][1], obj, files)
hS2.SetLineColor(3)
hS2.Draw("SAME")

hS3 = stitchUnpar(spin, du, spin_du_LambdaMap[(spin, du)][2], obj, files)
hS3.SetLineColor(4)
hS3.Draw("SAME")

t = ROOT.TLatex()
t.SetNDC()
t.SetTextFont( 62 )
t.SetTextColor( 36 )
t.SetTextSize( 0.08 )
t.SetTextAlign( 12 )
t.SetTextSize( 0.05 )
t.DrawLatex( 0.6, 0.70, 'BB, Spin %s, du = %s' %(spin, du))

legend = ROOT.TLegend(0.7,0.4,0.85,0.65)
legend.AddEntry(hS3, "#Lambda_{U} = %s" %(spin_du_LambdaMap[(spin, du)][2]))
legend.AddEntry(hS2, "#Lambda_{U} = %s" %(spin_du_LambdaMap[(spin, du)][1]) )
legend.AddEntry(hS1, "#Lambda_{U} = %s" %(spin_du_LambdaMap[(spin, du)][0]) )
legend.AddEntry(hB, "GG")
legend.SetLineWidth(0)
legend.Draw("same")

pad2.cd()
hR1 = createRatio(hS1, hB)
hR2 = createRatio(hS2, hB)
hR3 = createRatio(hS3, hB)


y = hR1.GetYaxis()
y.SetRangeUser(0, 2)
y.SetTitle("Ratio")
y.SetTitleSize(20)
y.SetTitleFont(43)
x = hR1.GetXaxis()

hR1.Draw("SAME")
hR2.Draw("SAME")
hR3.Draw("SAME")

c.SaveAs("out/ratioUnp_Spin%s_Du%s_%s_%s.pdf" %(spin, du, etaBin, year))

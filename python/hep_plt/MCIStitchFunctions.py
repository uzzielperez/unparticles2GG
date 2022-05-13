#!/usr/bin/python
import ROOT
from ROOT import TClass,TKey, TIter,TCanvas, TPad,TFile, TPaveText, TColor, TGaxis, TH1F, TPad, TH1D, TLegend
#from ROOT import kBlack, kBlue, kRed, kGreen, kMagenta, kCyan, kOrange, kViolet, kSpring
from ROOT import kBlue, kOrange, kCyan, kRed, kMagenta, kGreen, kViolet, kSpring, kPink, kAzure
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
#from legend import *
#from plotsHelpercomp import *
import re
from datetime import date

import sys
CMSlumiPath = '/uscms_data/d3/cuperez/CMSSW_8_0_25/src/scripts/pyroot'
sys.path.append(CMSlumiPath)
from CMSlumi import CMS_lumi, set_CMS_lumi
import argparse

def PlotDatasets(obj, DATASET):

	#drawstyle = "hist, same"
	drawstyle = "same"
	intlumi = 137
	today = str(date.today())
	print today
	xtratag = "ALL"
	#xtratag = ""
	#xtratag = "b"
	SM = True
	UNP = True
	BKG = []
	#BKG.append("%s/Unparticles_SM_M_500-2000.root" %(path))
	#BKG.append("%s/Unparticles_SM_M-2000.root" %(path))
	BKG.append("../EBEBEBEEEEE/OUTSM_M2000.root")
	BKG.append("../EBEBEBEEEEE/OUTSM_M500_2000.root")
	# OUTSM_M2000.root
	# OUTSM_M500_2000.root
	bkgf = []
	for fi in BKG:
		bkgf.append(ROOT.TFile(fi, "READ"))

	uf = []
	for datafile in DATASET:
		uf.append(ROOT.TFile(datafile, "READ"))

	canvas = ROOT.TCanvas()


	uh = []
	bkgh = []

	for ofile in bkgf:
		bkgh.append(ofile.Get(obj))

	for openfile in uf:
		uh.append(openfile.Get(obj))

	xpos1, ypos1, xpos2, ypos2 = .55, 0.58, .85, .88
	leg = TLegend(xpos1, ypos1, xpos2, ypos2)
	if "Minv" in obj:
		canvas.SetLogy()
		xtitle = r"m_{#gamma#gamma}#scale[1.0]{(GeV)}"
		ytitle = r"#scale[1.0]{Nevents}"
		xmin, xmax = 500, 13000
	if "chidiphoton" in obj:
		xtitle = r"#Chi_{#gamma#gamma}"
		ytitle = r"#scale[1.0]{Nevents}"
		xmin, xmax = 1, 20
	if "Pt" in obj:
		canvas.SetLogy()
		ytitle = r"#scale[1.0]{Nevents}"
		if "1" in obj:
				xtitle = r"p_{T}_{1}#scale[1.0]{(GeV)}"
		if "2" in obj:
				xtitle = r"p_{T}_{2}#scale[1.0]{(GeV)}"
		xmin, xmax = 1000, 13000
	if "costhetastar" in obj:
		xtitle = r"cos#theta^{*}"
		ytitle = r"#scale[1.0]{Nevents}"
		xmin, xmax = -1, 1
	if "Eta" in obj:
		ytitle = r"#scale[1.0]{Nevents}"
		if "1" in obj:
			xtitle = r"#eta_{1}"
		if "2" in obj:
			xtitle = r"#eta_{2}"
		xpos1, ypos1, xpos2, ypos2 = .60, 0.58, .95, .88
		xmin, xmax = -3, 3
	if SM:
		tag = "SM"
		histSM = bkgh[0].Clone("histSM")
		histSM.Add(bkgh[1], 1.0)
		histSM.SetFillStyle(3144)
		histSM.SetFillColor(7)
		histSM.Scale(intlumi)
		histSM.Draw("hist")
		label = "SM"
		leg.AddEntry(histSM, "%s" %(label), "f")
		print "Drawn", label

	colorlist = [kRed, kBlue, kMagenta, kGreen, kViolet, kOrange, kSpring, kPink, kAzure, kBlue+4, kOrange+3, kRed+5, kMagenta+7]
	labels = []
	histClones = []
	iset = 0
	icolor = 0
	i = 0
	while iset < len(DATASET):
		#if "Unp" in datafile:
		dset = DATASET[iset]
		pattern = 'OUTLU([^(]*)_du([^(]*)_spin([^(]*)_M([^(]*).root'
		#pattern = 'OUT([^(]*)_LU([^(]*)_du([^(]*)_spin([^(]*)-([^(]*)_M([^(]*).root'
		match = re.findall(pattern,dset)
		print match
		LU, du, spin, massrange = match[0]
		print match
		#LU = LU.replace('00', '')
		#t = iter(LU)
		#LU = 'p'.join(a+b for a,b in zip(t, t))
		dulabel = du.replace('.', 'p')
		#print LU, du, spin, switch, massrange
		label = r"#Lambda_{U}=%s, spin-%s" %(LU, spin)
		#label = r"#Lambda_{U}=%s, d_{u}=%s" %(LU, dulabel)

		#label = r"d_{u}=%s, spin-%s" %(dulabel, spin)
		labels.append(label)
    		tag = label
    		iset = iset + 1

	while i < len(DATASET):
    		histClone = uh[i].Clone("hist%s" %(labels[i]))
    		histClone.Add(uh[i+1], 1.0)
    		histClones.append(histClone)
    		i = i + 2

	j = 0
	eventsmaxlist = []
	for histclone in histClones:
		eventsmaxlist.append(histclone.GetMaximum())
		histclone.SetLineColor(colorlist[icolor])
		histclone.Scale(intlumi)
		histclone.Draw(drawstyle)
		print labels[j], histclone.GetEntries()
    		leg.AddEntry(histclone, "%s" %(labels[j]), "l")

		j = j+2
    		icolor = icolor + 1

	print eventsmaxlist

	histSM.SetMaximum(max(eventsmaxlist)*intlumi)
	histSM.GetYaxis().SetTitle(ytitle)
	histSM.GetYaxis().SetTitleOffset(1.0)
	histSM.GetXaxis().SetTitle(xtitle)
	histSM.GetXaxis().SetRangeUser(xmin, xmax)

	#legendtitle = "#bf{Constant #Lambda_{U}} = %s" %(LU)
	legendtitle = "#bf{Constant d_{U}} = %s" %(du)
	# legendtitle = "#bf{Scaling dimension:} %s" %(dulabel)
	#legendtitle = "#bf{Scaling dimension:} %s (%s)" %(dulabel, xtratag)
	leg.SetHeader(legendtitle, "R")
	leg.SetBorderSize(0)
	leg.SetFillColor(0)
	leg.SetFillStyle(0)
	leg.SetTextFont(42)
	leg.SetTextSize(0.035)

	leg.Draw()
	set_CMS_lumi(canvas, 4, 11, intlumi)
	canvas.Update()
	canvas.Draw()
	#canvas.Print("Unparticles_du%s_spin0y2_%sfb-1_%s%s.pdf" %(dutag, intlumi,obj, xtratag))
	canvas.Print("Plot%s%s.pdf" %(obj, "ALL"))

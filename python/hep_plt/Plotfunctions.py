#!/usr/bin/python

import ROOT
from ROOT import TClass,TKey, TIter,TCanvas, TPad,TFile, TPaveText, TColor, TGaxis, TH1F, TPad, TH1D, TLegend
from ROOT import kBlack, kBlue, kRed, kGreen, kMagenta, kCyan, kOrange, kViolet, kSpring
from ROOT import kBlue, kOrange, kCyan, kRed, kMagenta, kGreen, kViolet, kSpring, kPink, kAzure
from ROOT import gBenchmark, gStyle, gROOT, gDirectory
#from legend import *
#from plotsHelpercomp import *
import re
from ROOT import TMath
import sys
#CMSlumiPath = '/uscms_data/d3/cuperez/CMSSW_8_0_25/src/scripts/pyroot'
#sys.path.append(CMSlumiPath)
from CMSlumi import CMS_lumi, set_CMS_lumi
import argparse
from LambdaUcalc import xsecRatio

sw = ROOT.TStopwatch()
sw.Start()

LambdaT = "ALL"
SMPythia8 = True
SM = False
ADD = True

tag = "b"
zoom = False
#drawstyle = "hist, same"
drawstyle = "same"
intlumi = 137
# Draw Options
DrawAsHi = False
gStyle.SetOptStat(0)

def createHist(obj, sample):
	file1 = ROOT.TFile(sample, "READ")
	hist = file1.Get(obj)
	pattern = "OUTUnp_spin([^(]*)_du([^(]*)_LU([^(]*)p0_m([^(]*)_pT([^(]*)_M([^(]*).root"
	match = re.findall(pattern, sample)
	spin, du, LU, mCut, pTcut, massmin = match[0]
	hist.Scale(intlumi)
	hist.SetDirectory(0)
	return hist, match[0]

def Stitch(toStitchList, obj):

    openFileList, labelList = [], []
    for data in toStitchList:
		if "SM" in data:
			pattern = "OUT([^(]*)_pT70_"
			match = re.findall(pattern, data)
			label = match[0]
			#labelList.append(match[0])
		if "Unp" in data:
			pattern = "OUT([^(]*)_spin([^(]*)_du([^(]*)_LU([^(]*)_pT([^(]*)_M"
			match = re.findall(pattern, data)
			#labelList.append(match[0])
			PH, spin, du, LU, pT = match[0]
			label = PH, spin, du, LU, pT
		# Open ROOT files
        	openFileList.append(ROOT.TFile(data, "READ"))
    labelList.append(label)

    # Get Histogram objects
    hists = []
    for openfile in openFileList:
	histo = openfile.Get(obj)
	histo.SetDirectory(0)
        hists.append(histo)
	#print type(histo)
    # Stitching
    i = 1
    hist = hists[0].Clone("hist")
    #print type(histo), "this?"
    while i < len(hists):
        hist.Add(hists[i], 1.0)
        i = i + 1

    hist.SetDirectory(0)
    #print type(hist), "stitched?"
    #stitchedhist.SetDirectory[0]
    return  hist, labelList

def LabelMaker(obj, canvas):
	binSize = "125 GeV"
	if "Minv" in obj:
		canvas.SetLogy()
	      	xtitle = r"m_{#gamma#gamma}#scale[1.0]{(GeV)}"
	      	ytitle = r"#scale[1.0]{Nevents/%s}" %(binSize)
	      	xmin, xmax = 1000, 13000
      	if "Pt" in obj:
      		canvas.SetLogy()
      		xtitle = r"p_{T}#scale[1.0]{(GeV)}"
      		ytitle = r"#scale[1.0]{Nevents}"
      		xmin, xmax = 1000, 13000
      	if "chidiphoton" in obj:
	      	xtitle = r"#Chi_{#gamma#gamma}"
	     	ytitle = r"#scale[1.0]{Nevents}"
	      	xmin, xmax = 1, 20
      	if "costhetastar" in obj:
	      	xtitle = r"cos#theta^{*}"
	      	ytitle = r"#scale[1.0]{Nevents}"
	      	xmin, xmax = -1, 1
              	#xpos1, ypos1, xpos2, ypos2 = .30, 0.30, .65, .50
              	xpos1, ypos1, xpos2, ypos2 = .30, 0.50, .65, .70
      	if "Eta" in obj:
	      	xtitle = r"#eta"
	      	ytitle = r"#scale[1.0]{Nevents}"
	      	xmin, xmax = -4, 4
	return canvas, xtitle, ytitle, xmin, xmax

def OverlayHists(obj, histlist, labelList):
  	 canvas = ROOT.TCanvas()
	 canvas, xtitle, ytitle, xmin, xmax = LabelMaker(obj, canvas)
	 xpos1, ypos1, xpos2, ypos2 = .55, 0.58, .80, .88
	 if "costhetastar" in obj:
			 xpos1, ypos1, xpos2, ypos2 = .30, 0.50, .65, .70
	 leg = TLegend(xpos1, ypos1, xpos2, ypos2)
     	 colorlist = [kBlue, kOrange, kViolet+3, kRed,
	 			  kMagenta, kGreen, kViolet, kSpring,
				  kPink, kAzure, kOrange+8, kGreen+8,
				  kRed+8, kViolet+8, kMagenta+5]
       	 labels, histClones, iset, icolor, i = [], [], 0, 0, 0
	 while i < len(histlist):
		 histClone = histlist[i].Clone("hist%s" %(str(i)))
		 histClones.append(histClone)
	         i = i + 1
	 i = 0
	 eventsmaxlist = []
	 for histclone in histClones:
		label = labelList[i][0]
         	eventsmaxlist.append(histclone.GetMaximum())
      		if "SM" in label:
	     		histSM = histclone
	      		histSM.SetFillStyle(3144)
	      		histSM.SetFillColor(7+i)
	      		histSM.Scale(intlumi)
		        leg.AddEntry(histSM, "%s" %(r"SM M_{gg} > 500 GeV"), "f")
	     		histSM.Draw("hist same")
		else:
	      		histclone.SetLineColor(colorlist[icolor])
	     		histclone.Scale(intlumi)
	      		histclone.Draw(drawstyle)
			PH, spin, du, LU, pT = label
	      		leglabel = r"#Lambda_{U}=%s, d_{u}=%s, spin-%s" %(LU, du, spin)
   			leg.AddEntry(histclone, "%s" %(leglabel), "l")
     		i = i+1
   	        icolor = icolor + 1

	 Plot_outFileName = "Unparticles_spin%s_du%s.pdf" %(spin, du)

	 print eventsmaxlist
	 #legendtitle = "#bf{Renormalization Scale:} %s (%s)" %(LU, "isEBEB")
	 legendtitle = "#bf{Sensitivity Studies} (EB-EB)"
	 leg.SetHeader(legendtitle, "C")
	 leg.SetBorderSize(0)
	 leg.SetFillColor(0)
	 leg.SetFillStyle(0)
	 leg.SetTextFont(42)
	 leg.SetTextSize(0.035)

	 histSM.SetMaximum(max(eventsmaxlist)*intlumi)
	 histSM.GetYaxis().SetTitle(ytitle)
	 histSM.GetYaxis().SetTitleOffset(1.0)
	 histSM.GetXaxis().SetTitle(xtitle)
	 histSM.GetXaxis().SetRangeUser(xmin, xmax)


	 leg.Draw()
	 set_CMS_lumi(canvas, 4, 11, intlumi)
	 canvas.Update()
	 canvas.Draw()
	 canvas.Print(Plot_outFileName)

def OverlayDatasets(obj, DATASETS):
      uf = []
      for datafile in DATASETS:
	      uf.append(ROOT.TFile(datafile, "READ"))

      canvas = ROOT.TCanvas()
      uh = []
      bkgh = []

      for openfile in uf:
	      uh.append(openfile.Get(obj))

      canvas, xtitle, ytitle, xmin, xmax = LabelMaker(obj, canvas)
      # Legend Position
      xpos1, ypos1, xpos2, ypos2 = .55, 0.58, .80, .88
      if "costhetastar" in obj:
	xpos1, ypos1, xpos2, ypos2 = .30, 0.50, .65, .70

      #legendtitle = "#bf{Barrel-Barrel} Photons"
      leg = TLegend(xpos1, ypos1, xpos2, ypos2)

      colorlist = [kBlue, kOrange, kViolet+3, kRed, kMagenta, kGreen, kViolet, kSpring, kPink, kAzure, kOrange+8, kGreen+8, kRed+8, kViolet+8, kMagenta+5]
      labels = []
      histClones = []
      iset = 0
      icolor = 0
      i = 0

      while i < len(DATASETS):
	      histClone = uh[i].Clone("histdu%s" %(DATASETS[i]))
    	      histClones.append(histClone)
    	      i = i + 1

      j = 0
      eventsmaxlist = []
      for histclone in histClones:
	      eventsmaxlist.append(histclone.GetMaximum())
	      if "SM" in DATASETS[j]:

		      histSM = histclone
		      histSM.SetFillStyle(3144)
		      histSM.SetFillColor(7+j)
		      histSM.Scale(intlumi)
		      if "1000" in DATASETS[j]:
			      leg.AddEntry(histSM, "%s" %(r"SM M_{gg} > 1 TeV"), "f")
		      if "1500" in DATASETS[j]:
			      leg.AddEntry(histSM, "%s" %(r"SM M_{gg} > 1.5 TeV"), "f")
              	      if "2000" in DATASETS[j]:
 			      leg.AddEntry(histSM, "%s" %(r"SM M_{gg} > 2 TeV"), "f")
		      histSM.Draw("hist same")
	      else:
		      histclone.SetLineColor(colorlist[icolor])
		      histclone.Scale(intlumi)
		      histclone.Draw(drawstyle)
		      pattern = "../MINisEBEB/OUTUnp_spin([^(]*)_du([^(]*)_LU([^(]*)p0_m([^(]*)_pT([^(]*)_M([^(]*).root"
		      match = re.findall(pattern, DATASETS[j])
		      spinlabel, du, LambdaU, masscut, ptCut, massmin = match[0]
		      print match
		      leglabel = r"#Lambda_{U}=%s, d_{u}=%s, spin-%s" %(LambdaU, du, spinlabel)
    		      leg.AddEntry(histclone, "%s" %(leglabel), "l")
	      j = j+1
    	      icolor = icolor + 1

      print eventsmaxlist
      #legendtitle = "#bf{Renormalization Scale:} %s (%s)" %(LambdaU, "isEBEB")
      legendtitle = "#bf{Sensitivity Studies} (EB-EB)"
      leg.SetHeader(legendtitle, "C")
      leg.SetBorderSize(0)
      leg.SetFillColor(0)
      leg.SetFillStyle(0)
      leg.SetTextFont(42)
      leg.SetTextSize(0.035)

      histSM.SetMaximum(max(eventsmaxlist)*intlumi)
      histSM.GetYaxis().SetTitle(ytitle)
      histSM.GetYaxis().SetTitleOffset(1.0)
      histSM.GetXaxis().SetTitle(xtitle)
      histSM.GetXaxis().SetRangeUser(xmin, xmax)


      leg.Draw()
      set_CMS_lumi(canvas, 4, 11, intlumi)
      canvas.Update()
      canvas.Draw()
      canvas.Print("LOG%s_SMvsADD_%sfb-1_%s.pdf" %(intlumi, LambdaT, obj))

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetLineColor(kBlack)
    h3.SetMarkerStyle(21)
    h3.SetTitle("RATIO")
    #h3.SetMinimum(0.8)
    #h3.SetMaximum(2.5)
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    # Adjust y-axis settings
    y = h3.GetYaxis()
    y.SetTitle("ratio %s/%s" %(h1, h2))
    #y.SetTitleOffset(4.55)
    #y = h3.GetYaxis()
    #y.SetTitle("ratio h1/h2 ")
    y.SetNdivisions(505)
    y.SetTitleSize(20)
    y.SetTitleFont(43)
    y.SetTitleOffset(1.55)
    y.SetLabelFont(43)
    y.SetLabelSize(15)

    # Adjust x-axis settings
    x = h3.GetXaxis()
    x.SetTitleSize(40)
    x.SetTitleFont(43)
    x.SetTitleOffset(10.0)
    x.SetLabelFont(43)
    x.SetLabelSize(15)

    # return ratiohist
    return h3

def createCanvasPads():
    c = TCanvas("c", "canvas", 800, 800)
    # Upper histogram plot is pad1
    pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
    pad1.SetBottomMargin(0)  # joins upper and lower plot
    #pad1.SetGridx()
    pad1.SetLogy()
    pad1.Draw()
    # Lower ratio plot is pad2
    c.cd()  # returns to main canvas before defining pad2
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0)  # joins upper and lower plot
    pad2.SetBottomMargin(0.2)
    pad2.SetGridy()
    #pad2.SetGridx()
    pad2.Draw()

    return c, pad1, pad2



def createSignalOnly(obj, sample1, sample2):
        file1 = ROOT.TFile(sample1, "READ")
        file2 = ROOT.TFile(sample2, "READ")
        hdata = file1.Get(obj)
        hist2 = file2.Get(obj)

        hdata.Scale(intlumi)
        hist2.Scale(intlumi)
	hsigonly = hist2.Clone("Signal+B")
	hsigonly.Add(hdata, -1)
	b = hdata.Integral()

        s = hsigonly.Integral() #already scaled
    	pattern = "OUTUnp_spin([^(]*)_du([^(]*)_LU([^(]*)p0_m([^(]*)_pT([^(]*)_M([^(]*).root"
        match = re.findall(pattern, sample2)
	spin, du, LU, mCut, pTcut, massmin = match[0]
        #print intlumi, "fb-1; LU, du, spin, Mcut: ", LU, du, spin, massmin, ";b: ", b, "; s: ", s, "; sb:", hist2.Integral(), "; P(b, s+b): ", TMath.Poisson(b, s+b)

	h3 = hsigonly.Clone("hsigonly")
	h3.SetDirectory(0)
	#h3.GetBinContent(bin)
	#print h3.GetBinContent(88)
	#print h3.GetBinContent(5)
        #AddDirectory(kFALSE)
        #print "hsigonly type", type(hsigonly), type(hdata), type(hsigonly)
	return h3, match[0]

def makeLegend():
        xpos1, ypos1, xpos2, ypos2 = .55, 0.58, .80, .88
	leg = TLegend(xpos1, ypos1, xpos2, ypos2)
	legendtitle = "#bf{Sensitivity Studies} (EB-EB)"
        leg.SetHeader(legendtitle, "C")
        leg.SetBorderSize(0)
        leg.SetFillColor(0)
        leg.SetFillStyle(0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.035)

	return leg


def addToLegend(leg, hist, match):
        #LU, du, spin, massmin = match
        spin, du, LU, mCut, pTcut, massmin = match
	leglabel = r"#Lambda_{U}=%s, d_{u}=%s, spin-%s" %(LU, du, spin)
        leg.AddEntry(hist, "%s" %(leglabel), "l")

	return leg

def PlotRatio(h1, h2, labels1, labels2):
	c, pad1, pad2 = createCanvasPads()
    	#pad1.SetLogy()
	pad1.cd()
	h1.SetLineColor(kRed)
	h2.SetLineColor(kBlue)
	h1.Draw()
	x1 = h1.GetXaxis()
	y1 = h1.GetYaxis()
	ytitle = r"#scale[1.0]{Events/600GeV}"
	y1.SetTitle(ytitle)
	#x1.SetRangeUser(2000, 4000)
	h2.Draw("same")
        xpos1, ypos1, xpos2, ypos2 = .55, 0.58, .80, .88
	leg = makeLegend()
	leg = addToLegend(leg, h1, labels1)
        leg = addToLegend(leg, h2, labels2)
        leg.Draw()
        spin1, du1, LU1, mCut1, pTcut1, massmin1 = labels1
        spin2, du2, LU2, mCut2, pTcut2, massmin2 = labels2
	pad2.cd()
	hRatio = createRatio(h1, h2)
    	hRatio.Fit("pol0")
    	hRatio.GetFunction("pol0").SetLineColor(kRed)
    	stats = hRatio.FindObject("stats")
	if not stats:
		#continue
		stats.__class__ = ROOT.TPaveStats
    	#gStyle.SetOptFit(1111)
	#hRatio.GetXaxis().SetRangeUser(xmin, xmax)
	y = hRatio.GetYaxis()
	y.SetRangeUser(0, 10)
	y.SetTitle("Ratio")
	y.SetTitleSize(20)
	y.SetTitleFont(43)
	x = hRatio.GetXaxis()
	#x.SetRangeUser(2000, 4000)

        hRatio.Draw("ep")
	print "Theoretical ratio: ", xsecRatio(float(du1.replace("p",".")), float(LU1), float(LU2)), 1.00/xsecRatio(float(du1.replace("p",".")), float(LU1), float(LU2))
        c.Print("Ratio%s_%svs%s.pdf" %(du1, LU1, LU2))

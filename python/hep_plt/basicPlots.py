import glob
import ROOT

def stitchHist(fList, obj):
    hists = []
    # OpenFiles
    for f in fList:
        openFile = ROOT.TFile(f, "READ")
        h = openFile.Get(obj)
        h.SetDirectory(0)
        hists.append(h)
    # Stitch
    h = hists[0].Clone("hist")
    i = 1
    while i < len(hists):
        h.Add(hists[i], 1.0)
        i = i +1
    h.SetDirectory(0)

    return h

def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetTitle("RATIO")
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    return h3

def stitchUnpar(spin, du, LU, obj="diphotonMinv", files="*.root"):
    rootfiles = glob.glob(files)
    toStitchList = []
    for f in rootfiles:
        if ("spin%s" %(spin) in f) and ("du%s" %(du)  in f) and ("LU%s" %(LU) in f):
            toStitchList.append(f)
    #print (toStitchList)
    h = stitchHist(toStitchList, obj)
    return h

def stitchBkg(bkgName, obj="diphotonMinv", files="*.root"):
    rootfiles = glob.glob(files)
    toStitchList=[]
    for f in rootfiles:
        if (bkgName in f):
            toStitchList.append(f)
#     print (toStitchList)
    h = stitchHist(toStitchList, obj)
    return h

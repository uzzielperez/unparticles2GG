import ROOT
import argparse
import re

parser = argparse.ArgumentParser(description='rebin options')
#parser.add_argument('-i','--input', help='Input file to rebin.',default="Minv_histos_BB_2018.root", type=str)
parser.add_argument('-y','--year', help='year',default="2018", type=str)
parser.add_argument('-r','--region', help='region',default="BB", type=str)
parser.add_argument('-p','--path', help='Path to input.',default="public/", type=str)
parser.add_argument('--all', help='Run All Years and Regions')

args = parser.parse_args()
region     = args.region
year       = args.year
inputFile  = args.path + "Minv_histos_%s_%s_filtered_renamed_unpar.root" %(region, year)
yr = year[2:]

def main(region, year, inputFile):

    f = ROOT.TFile.Open(inputFile, "UPDATE")
    h_gg  = f.Get("BB%s__gg" %(yr))
    h_gj  = f.Get("BB%s__gj" %(yr))
    h_jj  = f.Get("BB%s__jj" %(yr))
    h = h_gg.Clone()
    h.Add(h_gj, 1.0)
    h.Add(h_jj, 1.0)

    nbins = h_gg.GetXaxis().GetNbins()
    print (nbins)

    RN = ROOT.TRandom3(0)
    xMin = 0.0
    xMax = 6000
    hPseudoData = ROOT.TH1F("hPseudoData", "hPseudoData", nbins, xMin, xMax)

    for i in range(nbins):
        mcYields = h.GetBinContent(i)
        #print (nEvents)
        n_rdm = RN.Poisson(mcYields) # double check
        #hOut.SetBinContent(nEvents)
        hPseudoData.SetBinContent(i, n_rdm)
        hPseudoData.SetBinError(i, n_rdm**0.5)

    f.WriteObject(hPseudoData, "BB%s__PSEUDODATA" %(yr))

if __name__ == "__main__":

    if args.all:
        region_list = ["BE", "BB"]
        year_list = ["2016", "2017", "2018"]

        for i in year_list:
            for j in region_list:
                #inFile = args.path + "Minv_histos_%s_%s.root" %(j, i)
                inFile = args.path + "Minv_histos_%s_%s_filtered_renamed_unpar.root" %(region, year)
                #print i, j
                print "####################"
                print "Adding pseudoData to %s" %(inFile)
                print "####################"
                main(j, i, inFile)
    else:
        main(region, year, inputFile)

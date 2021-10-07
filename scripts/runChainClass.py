import ROOT
import time
import subprocess
import os
import argparse

# Command line options
parser = argparse.ArgumentParser(description="Run-Chain-Class")
parser.add_argument("-i", "--inputfiles", dest="inputfiles", default="aChainClassInFiles.txt", help="List of input files. A file listing the path to inputfiles.")
parser.add_argument("-s", "--study", dest="study", default="Unparticles", help="Study DirName")
parser.add_argument("-t", "--ttree", dest="ttree", default="diphoton/fTree", help="TTree Name. Default is diphoton/fTree.")
args = parser.parse_args()


#inputfile = 'aInputMerged.txt'
inputfile = args.inputfiles
f = open(inputfile)
lines = f.read().split('\n') #list containing each line
lines = lines[:-1] #to exclude last slot in lines which is white space
print len(lines)
cwd = os.getcwd()

# Timer
sw = ROOT.TStopwatch()
sw.Start()


#------------------------------------------

#chain.Print()
#study = "GGJets"
#study = "DiPhoton"
#study = "GGJetsAdj1"
#study = "DoubleEGData"
#study = "ADDGravToGGSherpa"
study = args.study

classname = "Class%s" %(study)

#------------------------------------------

newfolder = '%sLoop' %(study) # you can always rename this later
os.mkdir(newfolder)
os.chdir(newfolder)

print "Moving to %sStudy/" %(study)

#-----------------------------------------

#tree = "diphoton/fTree"
#tree = "diphoton/fGenTrees"
tree = args.ttree

#-----------------------------------------

# Adding files to TChain
chain = ROOT.TChain(tree)
print "Adding files to %s" %(tree)
for e in lines:
	print e
	chain.Add(e,0) #second argument to add num_entries
print " >> Input evts:",chain.GetEntries()
chain.MakeClass(classname)
f.close()

#------------------------------------------
AN_template = "%s/aChainClassTemplate.C" %(cwd)
AN_file = "analyze.C"
AN = open(AN_file, "w+")
AN.write('#include "%s.C" \n' %(classname))

# Write out code
with open(AN_template, 'r') as f2:
	code = f2.read().replace('ClassNameHere', classname)
	AN.write(code)

print "Created %s to run over files" %(AN_file)
print code
AN.close()

#------------------------------------------

sw.Stop()
print "Real time: " + str(sw.RealTime() / 60.0) + " minutes"
print "CPU time:  " + str(sw.CpuTime() / 60.0) + " minutes"

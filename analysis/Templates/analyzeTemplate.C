#include "${ClassANGGJets}.C"
#include <iostream>
#include "TStopwatch.h"
using namespace std;

int ${analyzefunc}(){
        // start stopwatch
	TStopwatch sw;
	sw.Start();

	TString ntuple_path("root://cmseos.fnal.gov//store/user/cuperez/");
	TChain *chain = new TChain("diphoton/fTree");

	${ClassANGGJets} t;
        t.Loop();

	// stop stopwatch
	sw.Stop();
	cout << "Real Time: " << sw.RealTime()/60.0 << " minutes" << endl;
	cout << "CPU Time: " << sw.CpuTime()/60.0 << " minutes" << endl;
	return 0;

}

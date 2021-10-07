#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include "TSystem.h"
#include "TString.h"
#include "TStopwatch.h"
#include <iostream>

#include "unparticles2GG/UnparticlesLoop/"

#include "ClassUnparticles.C"
#include <iostream>
#include "TStopwatch.h"
using namespace std;

int analyze(){
        // start stopwatch
	TStopwatch sw;
	sw.Start();

	ClassUnparticles t;
        t.Loop();

	// stop stopwatch
	sw.Stop();
	cout << "Real Time: " << sw.RealTime()/60.0 << " minutes" << endl;
	cout << "CPU Time: " << sw.CpuTime()/60.0 << " minutes" << endl;
	return 0;

}

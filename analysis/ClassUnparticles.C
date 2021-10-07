#define ClassUnparticles_cxx
#include "ClassUnparticles.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>

void ClassUnparticles::Loop()
{

   if (fChain == 0) return;

   Long64_t nentries = fChain->GetEntriesFast();

   //counters
   int Ntotal        = 0;
   int NisEBEB       = 0;

   //histograms
   TH1D* gendiphotonMinv         = new TH1D("gendiphotonMinv", "", 100, 500., 13000.);// 100, 0, 10000

   gendiphotonMinv->Sumw2();

   //output settings
   TString fileout_name = "OUTtest.root";

   bool isEBEE = false;
   bool isEEEB = false;
   bool isEBEB = false;

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      // if (Cut(ientry) < 0) continue;

      Ntotal++;
      double weight = Event_weightAll;

      if ( jentry%10000 == 0 ) cout << "Number of processed events: " << jentry << endl;

      if ( std::abs(GenPhoton1_eta)<1.442 && (1.566 < std::abs(GenPhoton2_eta) && std::abs(GenPhoton2_eta) < 2.5) )      isEBEE = true;

      if ( (1.566 < std::abs(GenPhoton1_eta) && std::abs(GenPhoton1_eta) < 2.5) && (std::abs(GenPhoton2_eta) < 1.4442) ) isEEEB = true;

      if ( (std::abs(GenPhoton1_eta)<1.442) && (std::abs(GenPhoton2_eta)<1.442) )                                        isEBEB = true;

      if ( isEBEB ){

        NisEBEB++;
        gendiphotonMinv->Fill(GenDiphoton_Minv, weight);

      }
   }//end event loop

   cout << endl;
   cout << "Total entries            : " << Ntotal    << " " << nentries << endl;
   cout << "NisEBEB  : " << NisEBEB << endl;

   TFile file_out(fileout_name, "RECREATE");
   cout << "Writing file.." << endl;

   gendiphotonMinv->Write();
}

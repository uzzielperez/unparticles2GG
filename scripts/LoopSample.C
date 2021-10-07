//------------------------
//
// This is a loop sample
//
//
//------------------------


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
   int nDiphMinv     = 0;
   int netaCut       = 0;
   int NisEBEB       = 0;
   int NisEBEEorEEEB = 0;
   int NisEEEB       = 0;
   int NisEEEE       = 0;

   //histograms
   TH1D* gendiphotonMinv         = new TH1D("gendiphotonMinv", "", 100, 500., 13000.);// 100, 0, 10000
   TH1D* genphoton1Pt            = new TH1D("genphoton1Pt", "", 100, 0., 7000.);//
   TH1D* genphoton2Pt            = new TH1D("genphoton2Pt", "", 100, 0., 7000.);
   TH1D* genphoton1Eta           = new TH1D("genphoton1Eta", "", 20, -4.0, 4.0);
   TH1D* genphoton2Eta           = new TH1D("genphoton2Eta", "", 20, -4.0, 4.0);
   TH1D* genphoton1Phi           = new TH1D("genphoton1Phi", "", 20, -4.0, 4.5);
   TH1D* genphoton2Phi           = new TH1D("genphoton2Phi", "", 20, -4.0, 4.5);
   TH1D* gendiphotoncosthetastar = new TH1D("gendiphotoncosthetastar", "", 100, -1.0, 1.0);
   TH1D* genchidiphoton          = new TH1D("genchidiphoton", "", 100, 0, 50);

   gendiphotonMinv->Sumw2();
   genphoton1Pt->Sumw2();
   genphoton2Pt->Sumw2();
   genphoton1Eta->Sumw2();
   genphoton2Eta->Sumw2();
   genphoton1Phi->Sumw2();
   genphoton2Phi->Sumw2();
   gendiphotoncosthetastar->Sumw2();
   genchidiphoton->Sumw2();

   TString logfile = "NisEBEBLOG.txt";
   TString fileout_name = "OUT${outputfile}";

   //double xsec = ${xsecvalue};

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

      if ( std::abs(GenPhoton1_eta)<1.442 && (1.566 < std::abs(GenPhoton2_eta) && std::abs(GenPhoton2_eta) < 2.5) ){
         isEBEE = true;
      }

      if ( (1.566 < std::abs(GenPhoton1_eta) && std::abs(GenPhoton1_eta) < 2.5) && (std::abs(GenPhoton2_eta) < 1.4442) ){
         isEEEB = true;
      }

      if ( (std::abs(GenPhoton1_eta)<1.442) && (std::abs(GenPhoton2_eta)<1.442) ){
        isEBEB = true;
      }

      if ( isEBEB ){

        NisEBEB++;

        gendiphotonMinv->Fill(GenDiPhoton_Minv, weight);
        genphoton1Pt->Fill(GenPhoton1_pt, weight);
        genphoton2Pt->Fill(GenPhoton2_pt, weight);
        genphoton1Eta->Fill(GenPhoton1_eta, weight);
        genphoton2Eta->Fill(GenPhoton2_eta, weight);
        genphoton1Phi->Fill(GenPhoton1_phi, weight);
        genphoton2Phi->Fill(GenPhoton2_phi, weight);
        gendiphotoncosthetastar->Fill(GenDiPhoton_cosThetaStar, weight);
        genchidiphoton->Fill(GenDiPhoton_chiDiphoton, weight);

      }

   }

   cout << endl;
   cout << "File: " << fileout_name << endl;
   cout << "Total entries            : " << Ntotal    << " " << nentries << endl;
   cout << "NisEBEB  : " << NisEBEB << endl;
   cout << "NisEBEEorEEEB: " << NisEBEEorEEEB << endl;
   cout << "NisEEEE: " << NisEEEE << endl;

   cout << endl;
   ofstream outfile;
   outfile.open(logfile, ios::app);
   outfile << fileout_name << ", " << Ntotal << ", " << NisEBEB << ", " << NisEBEEorEEEB <<  ", " << NisEEEE << endl;
   outfile.close();

   TFile file_out(fileout_name, "RECREATE");
   cout << "Writing file.." << endl;
   gendiphotonMinv->Write();
   genphoton1Pt->Write();
   genphoton2Pt->Write();
   genphoton1Eta->Write();
   genphoton2Eta->Write();
   genphoton1Phi->Write();
   genphoton2Phi->Write();
   gendiphotoncosthetastar->Write();
   genchidiphoton->Write();

}

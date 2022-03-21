#define ${ClassANGGJets}_cxx
#include "${ClassANGGJets}.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <math.h>


void ${ClassANGGJets}::Loop()
{
   if (fChain == 0) return;

   // Cuts
   // cuts["BB"] = "isGood*(Diphoton.deltaR > 0.45 && Photon1.pt>125 && Photon2.pt>125 && Photon1.isEB && Photon2.isEB)";
   // cuts["BE"] = "isGood*(Diphoton.deltaR > 0.45 && Photon1.pt>125 && Photon2.pt>125 && ( (Photon1.isEB && Photon2.isEE) || (Photon2.isEB &&  Photon1.isEE )))";
   double minDeltaR = 0.45;
   double minPhoPt1 = 125;
   double minPhoPt2 = 125;



   Long64_t nentries = fChain->GetEntriesFast();
   //counters
 	int Ntotal      = 0;
 	int nDiphMinv   = 0;
 	int netaCut     = 0;
  int isEBEB = 0;
  int isEBEEorEEEB = 0;
  int isEEEB = 0;
  int isEEEE = 0;

  int nBins = 120;
  double xMin = 0.0;
  double xMax = 6000.;

  // Reco histograms
  TH1D* diphotonMinv = new TH1D("diphotonMinv", "", nBins, xMin, xMax);// 100, 0, 10000
  TH1D* photon1Pt    = new TH1D("photon1Pt", "", 100, 0., 7000.);//
  TH1D* photon2Pt    = new TH1D("photon2Pt", "", 100, 0., 7000.);
  TH1D* photon1Eta   = new TH1D("photon1Eta", "", 20, -4.0, 4.0);
  TH1D* photon2Eta   = new TH1D("photon2Eta", "", 20, -4.0, 4.0);
  TH1D* photon1Phi   = new TH1D("photon1Phi", "", 20, -4.0, 4.5);
  TH1D* photon2Phi   = new TH1D("photon2Phi", "", 20, -4.0, 4.5);
  TH1D* diphotoncosthetastar = new TH1D("diphotoncosthetastar", "", 100, -1.0, 1.0);
  TH1D* chidiphoton  = new TH1D("chidiphoton", "", 100, 0, 50);

  diphotonMinv->Sumw2();
  photon1Pt->Sumw2();
  photon2Pt->Sumw2();
  photon1Eta->Sumw2();
  photon2Eta->Sumw2();
  photon1Phi->Sumw2();
  photon2Phi->Sumw2();
  diphotoncosthetastar->Sumw2();
  chidiphoton->Sumw2();

  // other histograms
  TH1D* gendiphotonMinv = new TH1D("gendiphotonMinv", "", nBins, xMin, xMax);// 100, 0, 10000
  TH1D* genphoton1Pt    = new TH1D("genphoton1Pt", "", 100, 0., 7000.);//
  TH1D* genphoton2Pt    = new TH1D("genphoton2Pt", "", 100, 0., 7000.);
  TH1D* genphoton1Eta   = new TH1D("genphoton1Eta", "", 20, -4.0, 4.0);
  TH1D* genphoton2Eta   = new TH1D("genphoton2Eta", "", 20, -4.0, 4.0);
  TH1D* genphoton1Phi   = new TH1D("genphoton1Phi", "", 20, -4.0, 4.5);
  TH1D* genphoton2Phi   = new TH1D("genphoton2Phi", "", 20, -4.0, 4.5);
  TH1D* gendiphotoncosthetastar = new TH1D("gendiphotoncosthetastar", "", 100, -1.0, 1.0);
  TH1D* genchidiphoton  = new TH1D("genchidiphoton", "", 100, 0, 50);

  gendiphotonMinv->Sumw2();
  genphoton1Pt->Sumw2();
  genphoton2Pt->Sumw2();
  genphoton1Eta->Sumw2();
  genphoton2Eta->Sumw2();
  genphoton1Phi->Sumw2();
  genphoton2Phi->Sumw2();
  gendiphotoncosthetastar->Sumw2();
  genchidiphoton->Sumw2();

  // gg-initiated or qqbarInit
  TH1D* gg_diphotonMinv = new TH1D("gg_diphotonMinv", "", nBins, xMin, xMax);// 100, 0, 10000
  // TH1D* gg_photon1Pt    = new TH1D("photon1Pt", "", 100, 0., 7000.);//
  // TH1D* gg_photon2Pt    = new TH1D("photon2Pt", "", 100, 0., 7000.);
  // TH1D* gg_photon1Eta   = new TH1D("photon1Eta", "", 20, -4.0, 4.0);
  // TH1D* gg_photon2Eta   = new TH1D("photon2Eta", "", 20, -4.0, 4.0);
  // TH1D* gg_photon1Phi   = new TH1D("photon1Phi", "", 20, -4.0, 4.5);
  // TH1D* gg_photon2Phi   = new TH1D("photon2Phi", "", 20, -4.0, 4.5);
  // TH1D* gg_diphotoncosthetastar = new TH1D("diphotoncosthetastar", "", 100, -1.0, 1.0);
  // TH1D* gg_chidiphoton  = new TH1D("chidiphoton", "", 100, 0, 50);

  gg_diphotonMinv->Sumw2();
  // photon1Pt->Sumw2();
  // photon2Pt->Sumw2();
  // photon1Eta->Sumw2();
  // photon2Eta->Sumw2();
  // photon1Phi->Sumw2();
  // photon2Phi->Sumw2();
  // diphotoncosthetastar->Sumw2();
  // chidiphoton->Sumw2();

  TH1D* qqbar_diphotonMinv = new TH1D("qqbar_diphotonMinv", "", nBins, xMin, xMax);// 100, 0, 10000
  // TH1D* gg_photon1Pt    = new TH1D("photon1Pt", "", 100, 0., 7000.);//
  // TH1D* gg_photon2Pt    = new TH1D("photon2Pt", "", 100, 0., 7000.);
  // TH1D* gg_photon1Eta   = new TH1D("photon1Eta", "", 20, -4.0, 4.0);
  // TH1D* gg_photon2Eta   = new TH1D("photon2Eta", "", 20, -4.0, 4.0);
  // TH1D* gg_photon1Phi   = new TH1D("photon1Phi", "", 20, -4.0, 4.5);
  // TH1D* gg_photon2Phi   = new TH1D("photon2Phi", "", 20, -4.0, 4.5);
  // TH1D* gg_diphotoncosthetastar = new TH1D("diphotoncosthetastar", "", 100, -1.0, 1.0);
  // TH1D* gg_chidiphoton  = new TH1D("chidiphoton", "", 100, 0, 50);

  qqbar_diphotonMinv->Sumw2();
  // photon1Pt->Sumw2();
  // photon2Pt->Sumw2();
  // photon1Eta->Sumw2();
  // photon2Eta->Sumw2();
  // photon1Phi->Sumw2();
  // photon2Phi->Sumw2();
  // diphotoncosthetastar->Sumw2();
  // chidiphoton->Sumw2();

  TString logfile = "log.txt";
  TString fileout_name = "OUT${outputfile}";

   Long64_t nbytes = 0, nb = 0;
   for (Long64_t jentry=0; jentry<nentries;jentry++) {
      Long64_t ientry = LoadTree(jentry);
      if (ientry < 0) break;
      nb = fChain->GetEntry(jentry);   nbytes += nb;
      Ntotal++;
      double weight = Event_weightAll;

      if(jentry%10000 == 0) cout << "Number of processed events: " << jentry << endl;

      // TCut etaCut;
      // if (etaBin == "BB") etaCut = Photon1_isEB && Photon2_isEB;
      // if (etaBin == "BE") etaCut = ( (Photon1_isEB && Photon2_isEE) || (Photon2_isEB &&  Photon1_isEE ));

      // Reco Photons
      if (isGood && Diphoton_Minv > 600 && Diphoton_deltaR > minDeltaR){
        if (Photon1_pt> minPhoPt1 && Photon2_pt > minPhoPt2){
          if (${etaCut}){
              diphotonMinv->Fill(Diphoton_Minv, weight);
              photon1Pt->Fill(Photon1_pt, weight);
              photon2Pt->Fill(Photon2_pt, weight);
              photon1Eta->Fill(Photon1_eta, weight);
              photon2Eta->Fill(Photon2_eta, weight);
              photon1Phi->Fill(Photon1_phi, weight);
              photon2Phi->Fill(Photon2_phi, weight);
              diphotoncosthetastar->Fill(Diphoton_cosThetaStar, weight);
              chidiphoton->Fill(Diphoton_chiDiphoton, weight);

              if (Event_interactingParton2PdgId==21 && Event_interactingParton1PdgId==21){
                gg_diphotonMinv->Fill(Diphoton_Minv, weight);
              }

              // if (Event_interactingParton2PdgId!=21 && Event_interactingParton1PdgId!=21){
              //   qqbar_diphotonMinv->Fill(Diphoton_Minv, weight);
              // }

              if ( abs(Event_interactingParton1PdgId) <= 6 && abs(Event_interactingParton2PdgId) <= 6 ){
                qqbar_diphotonMinv->Fill(Diphoton_Minv, weight);
              }
          } // eta cuts
        }
      }

      // Gen Photons
      if (((std::abs(GenPhoton1_eta)<1.442) && (1.566 < std::abs(GenPhoton2_eta) && std::abs(GenPhoton2_eta) < 2.5)) || ((1.566 < std::abs(GenPhoton1_eta) && std::abs(GenPhoton1_eta) < 2.5) && (std::abs(GenPhoton2_eta) < 1.4442))) isEBEEorEEEB = isEBEEorEEEB + 1;
      if ((1.566 < std::abs(GenPhoton1_eta) && std::abs(GenPhoton1_eta) < 2.5) && (1.566 < std::abs(GenPhoton2_eta) && std::abs(GenPhoton2_eta) < 2.5)) isEEEE = isEEEE + 1;

      if  ((std::abs(GenPhoton1_eta)<1.442) && (std::abs(GenPhoton2_eta)<1.442)){
          isEBEB = isEBEB + 1; //


          gendiphotonMinv->Fill(GenDiphoton_Minv, weight);
          genphoton1Pt->Fill(GenPhoton1_pt, weight);
          genphoton2Pt->Fill(GenPhoton2_pt, weight);
          genphoton1Eta->Fill(GenPhoton1_eta, weight);
          genphoton2Eta->Fill(GenPhoton2_eta, weight);
          genphoton1Phi->Fill(GenPhoton1_phi, weight);
          genphoton2Phi->Fill(GenPhoton2_phi, weight);
          gendiphotoncosthetastar->Fill(GenDiphoton_cosThetaStar, weight);
          genchidiphoton->Fill(GenDiphoton_chiDiphoton, weight);


  }//isEBEB cut

        // if (Cut(ientry) < 0) continue;
   }//end loop over events
   cout << endl;
   cout << "File: " << fileout_name << endl;
   cout << "Total entries            : " << Ntotal    << " " << nentries << endl;
   cout << "isEBEB  : " << isEBEB << endl;
   cout << "isEBEEorEEEB: " << isEBEEorEEEB << endl;
   cout << "isEEEE: " << isEEEE << endl;

   //cout << "Passed DiphMinv cut      : " << nDiphMinv << endl;
   //cout << "Passed etaCut            : " << netaCut   << endl;
   cout << endl;

   ofstream outfile;
   outfile.open(logfile, ios::app);
   // outfile << "Log  : " << fileout_name << "; entries: " << Ntotal << "; isEBEB: " << isEBEB << "; isEBEEorEEEB: " << isEBEEorEEEB << "" endl;
   outfile << fileout_name << ", " << Ntotal << ", " << isEBEB << ", " << isEBEEorEEEB <<  ", " << isEEEE << endl;
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

   diphotonMinv->Write();
   photon1Pt->Write();
   photon2Pt->Write();
   photon1Eta->Write();
   photon2Eta->Write();
   photon1Phi->Write();
   photon2Phi->Write();
   diphotoncosthetastar->Write();
   chidiphoton->Write();

   gg_diphotonMinv->Write();
   qqbar_diphotonMinv->Write();

}// end class

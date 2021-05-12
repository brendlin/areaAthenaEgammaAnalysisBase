
void conversionTuningTRT(TFile* file,std::string key) {

  /* CONFIGURATION */
  bool doNtuple = true;
  /* END CONFIGURATION */

  //float eProbabilityNN_0;
  TFile* outFile = NULL;
  TTree* outTree = NULL;
  float eProbabilityHT_0 = -999;
  float eProbabilityHT_1 = -999;
  float trueR = -999;
  int convType = -1;
  float recoPt = -999;
  float recoEta = -999;
  float truthPt = -999;
  float truthEta = -999;
  int nSi_0 = -1;
  int nSi_1 = -1;
  float mu = -1;

  if (doNtuple) {
    outFile = new TFile(Form("%s_nano.root",key.c_str()), "RECREATE");
    outTree = new TTree("CollectionTree","tuning_tree");
    outTree->Branch("eProbabilityHT_0",&eProbabilityHT_0);
    outTree->Branch("eProbabilityHT_1",&eProbabilityHT_1);
    outTree->Branch("trueR",&trueR);
    outTree->Branch("convType",&convType);
    outTree->Branch("recoPt",&recoPt);
    outTree->Branch("recoEta",&recoEta);
    outTree->Branch("truthPt",&truthPt);
    outTree->Branch("truthEta",&truthEta);
    outTree->Branch("nSi_0",&nSi_0);
    outTree->Branch("nSi_1",&nSi_1);
    outTree->Branch("mu",&mu);
  }

  std::cout << file->GetName() << std::endl;

  xAOD::Init();
  xAOD::TEvent* event = new xAOD::TEvent (xAOD::TEvent::kClassAccess);
  TTree* tree = (TTree*)file->Get("CollectionTree");
  if (!event->readFrom(file).isSuccess()) {
    std::cout << "Read failed." << std::endl;
    return;
  }

  for (Long64_t entry=0;entry<tree->GetEntries();++entry) {

    if (!(entry % 10000)) std::cout << Form("Processed %.3fM events",entry/1000000.) << std::endl;
    //std::cout << Form("Processed %d events",entry) << std::endl;

    event->getEntry(entry);
    //if (entry > 20) break;

    const xAOD::EventInfo* ei = 0;
    if (!event->retrieve(ei,"EventInfo").isSuccess()) {
      std::cout << "Error - could not find EventInfo." << std::endl;
      break;
    }

    mu = ei->averageInteractionsPerCrossing();
    //std::cout << "Mu is " << mu << std::endl;

    const xAOD::TruthParticleContainer* egTruthParticles = 0;
    if (!event->retrieve(egTruthParticles,"egammaTruthParticles").isSuccess()) {
      std::cout << "Error - could not find egamma truth particles." << std::endl;
      break;
    }

    for (auto egtruth : *egTruthParticles) {

      if (!egtruth) continue;

      eProbabilityHT_0 = -999;
      eProbabilityHT_1 = -999;
      trueR = -999;
      convType = -1;
      recoPt = -999;
      recoEta = -999;
      truthPt = egtruth->pt()/1000.;
      truthEta = egtruth->eta();
      nSi_0 = -1;
      nSi_1 = -1;

      bool isTrueConv = xAOD::EgammaHelpers::isTrueConvertedPhoton(egtruth);

      if (isTrueConv) {
        if (egtruth->pdgId() == 22 && egtruth->hasDecayVtx()) {
          float x = egtruth->decayVtx()->x();
          float y = egtruth->decayVtx()->y();
          trueR = std::sqrt( x*x + y*y );
        }
      }
      //std::cout << "True convRadius: " << trueR << std::endl;

      const xAOD::Photon *photon = xAOD::EgammaHelpers::getRecoPhoton(egtruth);
      if (!photon) {
        outTree->Fill();
        continue;
      }

      recoPt = photon->pt()/1000.;
      recoEta = photon->eta()/1000.;
      //std::cout << "Reco photon pt/eta: " << recoPt << " " << recoEta << std::endl;

      bool isRecoConv = xAOD::EgammaHelpers::isConvertedPhoton(photon);
      convType = xAOD::EgammaHelpers::conversionType(photon);
      //std::cout << "Conversion type: " << convType << std::endl;
 
      const xAOD::TrackParticle *trk0 = 0;
      const xAOD::TrackParticle *trk1 = 0;

      const xAOD::Vertex *vx = photon->vertex();
      if (isRecoConv && vx) {
        trk0 = ( vx->nTrackParticles() ? vx->trackParticle(0) : 0 );
        trk1 = ( vx->nTrackParticles() > 1 ? vx->trackParticle(1) : 0 );
      }
        
      if (trk0) {
        eProbabilityHT_0 = xAOD::EgammaHelpers::summaryValueFloat(*trk0, xAOD::eProbabilityHT);
        nSi_0 = xAOD::EgammaHelpers::numberOfSiHits(trk0);
      }
      if (trk1) {
        eProbabilityHT_1 = xAOD::EgammaHelpers::summaryValueFloat(*trk1, xAOD::eProbabilityHT);
        nSi_1 = xAOD::EgammaHelpers::numberOfSiHits(trk1);
      }
      //std::cout << "eProbability: " << eProbabilityHT_0 << ", " << eProbabilityHT_1 << std::endl;

      outTree->Fill();

    } //egtruth Loop

  } // Loop over entries

  if (doNtuple) {
    outFile->Write();
  }

  std::cout << "Succeeded." << std::endl;
  return;
}

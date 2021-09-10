
float eProbabilityHT_trans(float TRT_PID) {
  double trans_TRT_PID(0.0);
  double tau = 15.0;
  double fEpsilon = 1.0e-30;  // to avoid zero division
  double pid_tmp = TRT_PID;
  if (pid_tmp >= 1.0) pid_tmp = 1.0 - 1.0e-15;  //this number comes from TMVA
  else if (pid_tmp <= fEpsilon) pid_tmp = fEpsilon;
  trans_TRT_PID = - log(1.0/pid_tmp - 1.0)*(1./double(tau));
  return trans_TRT_PID;
}

float precisionHitFraction(const xAOD::TrackParticle& track) {
  uint8_t dummy;

  uint8_t nTrtHits(0);
  if( track.summaryValue(dummy, xAOD::numberOfTRTHits))
    nTrtHits = dummy;

  uint8_t nTRTTubeHits(0);
  if(track.summaryValue(dummy, xAOD::numberOfTRTTubeHits))
    nTRTTubeHits = dummy;

  float precHitFrac = -999;
  if (nTrtHits>0 && nTRTTubeHits>=0)
  {
    precHitFrac = (1. - ((float)nTRTTubeHits)/((float)nTrtHits));
  }

  //std::cout << "precHitFrac = " << precHitFrac << std::endl;
  return precHitFrac;
}

int nTRT(const xAOD::TrackParticle& track) {
  uint8_t dummy;

  uint8_t nTrtHits(0);
  if( track.summaryValue(dummy, xAOD::numberOfTRTHits))
    nTrtHits = dummy;
  uint8_t nTrtOutliers(0);
  if(track.summaryValue(dummy, xAOD::numberOfTRTOutliers))
    nTrtOutliers = dummy;

  uint8_t ntrt = nTrtHits + nTrtOutliers;

  return ntrt;
}

int nTRTHoles(const xAOD::TrackParticle& track) {
  uint8_t dummy;

  uint8_t nTrtHoles(0);
  if( track.summaryValue(dummy, xAOD::numberOfTRTHoles))
    nTrtHoles = dummy;

  return nTrtHoles;
}

void conversionTuningTRT(TFile* file,std::string key) {

  /* CONFIGURATION */
  bool doNtuple = true;
  /* END CONFIGURATION */

  //float eProbabilityNN_0;
  TFile* outFile = NULL;
  TTree* outTree = NULL;
  float eProbabilityHT_0 = -999;
  float eProbabilityHT_1 = -999;
  float eProbabilityHT_trans_0 = -999;
  float eProbabilityHT_trans_1 = -999;
  float eProbabilityNN_0 = -999;
  float eProbabilityNN_1 = -999;
  float eProbabilityNN_trans_0 = -999;
  float eProbabilityNN_trans_1 = -999;
  float trueR = -999;
  int convType = -1;
  float recoPt = -999;
  float recoEta = -999;
  float truthPt = -999;
  float truthEta = -999;
  int nSi_0 = -1;
  int nSi_1 = -1;
  int nTRT_0 = -1;
  int nTRT_1 = -1;
  int nTRTHoles_0 = -1;
  int nTRTHoles_1 = -1;
  float trkEta_0 = -999;
  float trkEta_1 = -999;
  float trkPt_0 = -999;
  float trkPt_1 = -999;
  float precHitFrac_0 = -999;
  float precHitFrac_1 = -999;
  float mu = -1;
  int nVertices = -1;

  static const SG::AuxElement::ConstAccessor<float> acc_eProbabilityNN("eProbabilityNN");

  if (doNtuple) {
    outFile = new TFile(Form("%s_nano.root",key.c_str()), "RECREATE");
    outTree = new TTree("CollectionTree","tuning_tree");
    outTree->Branch("eProbabilityHT_0",&eProbabilityHT_0);
    outTree->Branch("eProbabilityHT_1",&eProbabilityHT_1);
    outTree->Branch("eProbabilityHT_trans_0",&eProbabilityHT_trans_0);
    outTree->Branch("eProbabilityHT_trans_1",&eProbabilityHT_trans_1);
    outTree->Branch("eProbabilityNN_0",&eProbabilityNN_0);
    outTree->Branch("eProbabilityNN_1",&eProbabilityNN_1);
    outTree->Branch("eProbabilityNN_trans_0",&eProbabilityNN_trans_0);
    outTree->Branch("eProbabilityNN_trans_1",&eProbabilityNN_trans_1);
    outTree->Branch("trueR",&trueR);
    outTree->Branch("convType",&convType);
    outTree->Branch("recoPt",&recoPt);
    outTree->Branch("recoEta",&recoEta);
    outTree->Branch("truthPt",&truthPt);
    outTree->Branch("truthEta",&truthEta);
    outTree->Branch("nSi_0",&nSi_0);
    outTree->Branch("nSi_1",&nSi_1);
    outTree->Branch("nTRT_0",&nTRT_0);
    outTree->Branch("nTRT_1",&nTRT_1);
    outTree->Branch("nTRTHoles_0",&nTRTHoles_0);
    outTree->Branch("nTRTHoles_1",&nTRTHoles_1);
    outTree->Branch("trkEta_0",&trkEta_0);
    outTree->Branch("trkEta_1",&trkEta_1);
    outTree->Branch("trkPt_0",&trkPt_0);
    outTree->Branch("trkPt_1",&trkPt_1);
    outTree->Branch("precHitFrac_0",&precHitFrac_0);
    outTree->Branch("precHitFrac_1",&precHitFrac_1);
    outTree->Branch("mu",&mu);
    outTree->Branch("nVertices",&nVertices);
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
      eProbabilityHT_trans_0 = -999;
      eProbabilityHT_trans_1 = -999;
      eProbabilityNN_0 = -999;
      eProbabilityNN_1 = -999;
      eProbabilityNN_trans_0 = -999;
      eProbabilityNN_trans_1 = -999;
      trueR = -999;
      convType = -1;
      recoPt = -999;
      recoEta = -999;
      nVertices = -1;
      truthPt = egtruth->pt()/1000.;
      truthEta = egtruth->eta();
      nSi_0 = -1;
      nSi_1 = -1;
      nTRT_0 = -1;
      nTRT_1 = -1;
      nTRTHoles_0 = -1;
      nTRTHoles_1 = -1;
      trkEta_0 = -999;
      trkEta_1 = -999;
      trkPt_0 = -999;
      trkPt_1 = -999;
      precHitFrac_0 = -999;
      precHitFrac_1 = -999;

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
      recoEta = photon->eta();
      nVertices = photon->nVertices();
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
        eProbabilityHT_trans_0 = eProbabilityHT_trans(eProbabilityHT_0);
        eProbabilityNN_0 = acc_eProbabilityNN(*trk0);
        eProbabilityNN_trans_0 = eProbabilityHT_trans(eProbabilityNN_0);
        nSi_0 = xAOD::EgammaHelpers::numberOfSiHits(trk0);
        nTRT_0 = nTRT(*trk0);
        nTRTHoles_0 = nTRTHoles(*trk0);
        precHitFrac_0 = precisionHitFraction(*trk0);
        float tanThetaOver2_0 = std::tan( trk0->theta() / 2.);
        trkEta_0 = (tanThetaOver2_0 == 0) ? -999 : -std::log( tanThetaOver2_0 );
        trkPt_0 = trk0->pt();
        //std::cout << "Track eta is: " << trk0->eta() << " or " << eta << std::endl;
      }
      if (trk1) {
        eProbabilityHT_1 = xAOD::EgammaHelpers::summaryValueFloat(*trk1, xAOD::eProbabilityHT);
        eProbabilityHT_trans_1 = eProbabilityHT_trans(eProbabilityHT_1);
        eProbabilityNN_1 = acc_eProbabilityNN(*trk1);
        eProbabilityNN_trans_1 = eProbabilityHT_trans(eProbabilityNN_1);
        nSi_1 = xAOD::EgammaHelpers::numberOfSiHits(trk1);
        nTRT_1 = nTRT(*trk1);
        nTRTHoles_1 = nTRTHoles(*trk1);
        precHitFrac_1 = precisionHitFraction(*trk1);
        float tanThetaOver2_1 = std::tan( trk1->theta() / 2.);
        trkEta_1 = (tanThetaOver2_1 == 0) ? -999 : -std::log( tanThetaOver2_1 );
        trkPt_1 = trk1->pt();
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


echo "Reco_tf.py --inputRDOFile=rdo.root --outputAODFile=Nightly_AOD_gamma.pool.root --maxEvents=5 --autoConfiguration=\"everything\" --conditionsTag=\"\$CONDITIONSTAG\" --preExec=\"\$PREEXEC\" --postExec \"\$POSTEXEC_A\" \"\$POSTEXEC_B\""
echo "athena -c \"particleType='gamma'\" \$TestArea/../build/\$Athena_PLATFORM/jobOptions/egammaValidation/egamma_art_checker_joboptions.py"

# echo "condor_submit submit INPUT=GridDirectFiles/GridDirect_mc16_13TeV.423001.ParticleGun_single_photon_egammaET.recon.RDO.e3566_s3113_r9388.txt THEDIR=mc16a_outputdir"
# echo "condor_submit submit INPUT=GridDirectFiles/GridDirect_mc16_13TeV.423001.ParticleGun_single_photon_egammaET.recon.RDO.e3566_s3113_r10470.txt THEDIR=mc16d_outputdir"
echo ""
echo "source doSubmit.sh GridDirectFiles/GridDirect_mc16_13TeV.423001.ParticleGun_single_photon_egammaET.recon.RDO.e3566_s3113_r9388.txt mc16a_outputdir"
echo "source doSubmit.sh GridDirectFiles/GridDirect_mc16_13TeV.423001.ParticleGun_single_photon_egammaET.recon.RDO.e3566_s3113_r10470.txt mc16d_outputdir"
echo "for i in \$(ls ../ | grep job); do ln -s ../\$i/Nightly_AOD_gamma.pool.root \${i}_Nightly_AOD_gamma.pool.root; done;"

export CONDITIONSTAG="default:OFLCOND-MC16-SDR-RUN2-04"

export PREEXEC="from ParticleBuilderOptions.AODFlags import AODFlags; AODFlags.ThinGeantTruth.set_Value_and_Lock(False);AODFlags.egammaTrackSlimmer.set_Value_and_Lock(False);AODFlags.ThinInDetForwardTrackParticles.set_Value_and_Lock(False);AODFlags.ThinNegativeEnergyNeutralPFOs.set_Value_and_Lock(False);rec.doTrigger=False; rec.doTau=False ; rec.doMuon=False;rec.doBTagging=False ; from RecExConfig.RecAlgsFlags import recAlgs; recAlgs.doMuonSpShower=False ; recAlgs.doEFlow=False ; recAlgs.doEFlowJet=False ; recAlgs.doMissingET=False ; recAlgs.doMissingETSig=False ; recAlgs.doTrigger=False ; from JetRec.JetRecFlags import jetFlags ; jetFlags.Enabled=False;"

export POSTEXEC_Y="RAWtoESD:ToolSvc.InDetTRT_StandaloneScoringTool.minTRTPrecisionFraction=0.05;"

export POSTEXEC_A="ESDtoAOD:CILMergeAOD.removeItem(\"xAOD::CaloClusterAuxContainer#CaloCalTopoClustersAux.SECOND_R.SECOND_LAMBDA.CENTER_MAG.CENTER_LAMBDA.FIRST_ENG_DENS.ENG_FRAC_MAX.ISOLATION.ENG_BAD_CELLS.N_BAD_CELLS.BADLARQ_FRAC.ENG_POS.AVG_LAR_Q.AVG_TILE_Q.EM_PROBABILITY.BadChannelList\");CILMergeAOD.add(\"xAOD::CaloClusterAuxContainer#CaloCalTopoClustersAux.SECOND_R.LATERAL.ENG_FRAC_EM.SECOND_LAMBDA.CENTER_MAG.CENTER_LAMBDA.FIRST_ENG_DENS.ENG_FRAC_MAX.ISOLATION.ENG_BAD_CELLS.N_BAD_CELLS.BADLARQ_FRAC.ENG_POS.AVG_LAR_Q.AVG_TILE_Q.EM_PROBABILITY.BadChannelList.ENG_CALIB_TOT.ENG_CALIB_OUT_L.ENG_CALIB_EMB0.ENG_CALIB_EME0.ENG_CALIB_TILEG3.ENG_CALIB_DEAD_TOT.ENG_CALIB_DEAD_EMB0.ENG_CALIB_DEAD_TILE0.ENG_CALIB_DEAD_TILEG3.ENG_CALIB_DEAD_EME0.ENG_CALIB_DEAD_HEC0.ENG_CALIB_DEAD_FCAL.ENG_CALIB_DEAD_LEAKAGE.ENG_CALIB_DEAD_UNCLASS.ENG_CALIB_FRAC_EM.ENG_CALIB_FRAC_HAD.ENG_CALIB_FRAC_REST\");StreamAOD.ItemList=CILMergeAOD()"

export POSTEXEC_B="POOLMergeAthenaMPAOD0:CILMergeAOD.removeItem(\"xAOD::CaloClusterAuxContainer#CaloCalTopoClustersAux.SECOND_R.SECOND_LAMBDA.CENTER_MAG.CENTER_LAMBDA.FIRST_ENG_DENS.ENG_FRAC_MAX.ISOLATION.ENG_BAD_CELLS.N_BAD_CELLS.BADLARQ_FRAC.ENG_POS.AVG_LAR_Q.AVG_TILE_Q.EM_PROBABILITY.BadChannelList\");CILMergeAOD.add(\"xAOD::CaloClusterAuxContainer#CaloCalTopoClustersAux.SECOND_R.LATERAL.ENG_FRAC_EM.SECOND_LAMBDA.CENTER_MAG.CENTER_LAMBDA.FIRST_ENG_DENS.ENG_FRAC_MAX.ISOLATION.ENG_BAD_CELLS.N_BAD_CELLS.BADLARQ_FRAC.ENG_POS.AVG_LAR_Q.AVG_TILE_Q.EM_PROBABILITY.BadChannelList.ENG_CALIB_TOT.ENG_CALIB_OUT_L.ENG_CALIB_EMB0.ENG_CALIB_EME0.ENG_CALIB_TILEG3.ENG_CALIB_DEAD_TOT.ENG_CALIB_DEAD_EMB0.ENG_CALIB_DEAD_TILE0.ENG_CALIB_DEAD_TILEG3.ENG_CALIB_DEAD_EME0.ENG_CALIB_DEAD_HEC0.ENG_CALIB_DEAD_FCAL.ENG_CALIB_DEAD_LEAKAGE.ENG_CALIB_DEAD_UNCLASS.ENG_CALIB_FRAC_EM.ENG_CALIB_FRAC_HAD.ENG_CALIB_FRAC_REST\");StreamAOD.ItemList=CILMergeAOD()"


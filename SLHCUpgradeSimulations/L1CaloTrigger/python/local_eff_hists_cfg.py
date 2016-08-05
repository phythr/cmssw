import FWCore.ParameterSet.Config as cms

process = cms.Process("test")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20) )

process.source = cms.Source("PoolSource",
   #fileNames = cms.untracked.vstring('file:/hdfs/store/mc/TTI2023Upg14D/SingleElectronFlatPt0p2To50/GEN-SIM-DIGI-RAW/PU140bx25_PH2_1K_FB_V3-v2/00000/80EE54BB-1EE6-E311-877F-002354EF3BE0.root')
   fileNames = cms.untracked.vstring('file:/hdfs/store/mc/RunIISpring16MiniAODv2/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/MINIAODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_miniAODv2_v0_ext1-v1/00000/00F0B3DC-211B-E611-A6A0-001E67248A39.root')
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'PH2_1K_FB_V3::All', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

#process.load('Configuration.Geometry.GeometryExtended2023TTIReco_cff')
process.load('Configuration.Geometry.GeometryExtended2023simReco_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
#XXX process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
#XXX process.load('Geometry.TrackerGeometryBuilder.StackedTrackerGeometry_cfi')
#XXX process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')
#XXX process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')

process.load('Configuration/StandardSequences/L1HwVal_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
#XXX process.load("SLHCUpgradeSimulations.L1CaloTrigger.SLHCCaloTrigger_cff")

# bug fix for missing HCAL TPs in MC RAW
from SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff import HcalTPGCoderULUT
HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)
process.valRctDigis.hcalDigis             = cms.VInputTag(cms.InputTag('valHcalTriggerPrimitiveDigis'))
#XXX process.L1CaloTowerProducer.HCALDigis =  cms.InputTag("valHcalTriggerPrimitiveDigis")

#XXX process.slhccalo = cms.Path( process.RawToDigi + process.valHcalTriggerPrimitiveDigis+process.SLHCCaloTrigger)
process.slhccalo = cms.Path( process.RawToDigi + process.valHcalTriggerPrimitiveDigis)

# run L1Reco to produce the L1EG objects corresponding
# to the current trigger
process.load('Configuration.StandardSequences.L1Reco_cff')
process.L1Reco = cms.Path( process.l1extraParticles )

###XXX # producer for UCT2015 / Stage-1 trigger objects
###XXX process.load("L1Trigger.UCT2015.emulationMC_cfi")
###XXX process.load("L1Trigger.UCT2015.uctl1extraparticles_cfi")
###XXX process.pUCT = cms.Path(
###XXX     process.emulationSequence *
###XXX     process.uct2015L1Extra
###XXX )

# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

# first you need the ECAL RecHIts :
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.reconstruction_step = cms.Path( process.calolocalreco )

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   EtminForStore = cms.double(0.),
   debug = cms.untracked.bool(False),
   useECalEndcap = cms.bool(True)
)
process.pSasha = cms.Path( process.L1EGammaCrystalsProducer )

# --------------------------------------------------------------------------------------------
#
# ----  Match the L1EG stage-2 objects created by the SLHCCaloTrigger sequence above
#	with the crystal-level clusters.
#	This produces a new collection of L1EG objects, starting from the original
#	L1EG collection. The eta and phi of the L1EG objects is corrected using the
#	information of the xtal level clusters.

###XXX process.l1ExtraCrystalProducer = cms.EDProducer("L1ExtraCrystalPosition",
###XXX    eGammaSrc = cms.InputTag("SLHCL1ExtraParticles","EGamma"),
###XXX    eClusterSrc = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster")
###XXX )
###XXX process.egcrystal_producer = cms.Path(process.l1ExtraCrystalProducer)


# ----------------------------------------------------------------------------------------------
# 
# Do offline reconstruction step to get cluster pt

###XXX process.load('RecoEcal.Configuration.RecoEcal_cff')
###XXX process.ecalClusters = cms.Path(process.ecalClustersNoPFBox)


###XXX # ---------------------------------------------------------------------------
###XXX #
###XXX # --- Create the collection of special tracks for electrons
###XXX #
###XXX 
###XXX process.load("SLHCUpgradeSimulations.L1TrackTrigger.L1TrackingSequence_cfi")
###XXX process.pTracking = cms.Path( process.ElectronTrackingSequence )
###XXX 
###XXX # --- Produce the L1TkPrimaryVertex
###XXX 
###XXX process.load("SLHCUpgradeSimulations.L1TrackTrigger.L1TkPrimaryVertexProducer_cfi")
###XXX process.pL1TkPrimaryVertex = cms.Path( process.L1TkPrimaryVertex )
###XXX 
###XXX 
###XXX ############################################################
###XXX # pixel stuff, uncomment if needed
###XXX ############################################################
###XXX # from ./SLHCUpgradeSimulations/L1TrackTrigger/test/L1TrackNtupleMaker_cfg.py
###XXX 
###XXX #BeamSpotFromSim =cms.EDProducer("VtxSmeared")
###XXX #process.pBeamSpot = cms.Path( process.BeamSpotFromSim )
###XXX #
###XXX ## pixel additions
###XXX #process.load('Configuration.StandardSequences.RawToDigi_cff')
###XXX #process.load('Configuration.StandardSequences.Reconstruction_cff')
###XXX #process.load('SimGeneral.MixingModule.mixNoPU_cfi')
###XXX #
###XXX #
###XXX #from RecoLocalTracker.SiPixelRecHits.SiPixelRecHits_cfi import *
###XXX #process.siPixelRecHits = siPixelRecHits
###XXX #
###XXX #process.L1PixelTrackFit = cms.EDProducer("L1PixelTrackFit")
###XXX #process.pixTrk = cms.Path(process.siPixelRecHits +  process.L1PixelTrackFit)
###XXX #
###XXX #process.pixRec = cms.Path(
###XXX #    process.RawToDigi+
###XXX #    process.siPixelRecHits
###XXX #)
###XXX #
###XXX #process.raw2digi_step = cms.Path(process.RawToDigi)
###XXX 
###XXX 
###XXX 
###XXX # ----------------------------------------------------------------------------------------------
###XXX # 
###XXX # Analyzer starts here
###XXX 
###XXX process.analyzer = cms.EDAnalyzer('L1EGRateStudies',
###XXX    L1EGammaInputTags = cms.VInputTag(
###XXX       # Old stage-2 trigger
###XXX       cms.InputTag("SLHCL1ExtraParticles","EGamma"),
###XXX       # 'dynamic clustering'
###XXX       cms.InputTag("SLHCL1ExtraParticlesNewClustering","EGamma"),
###XXX       # Run 1 algo.
###XXX       cms.InputTag("l1extraParticles", "Isolated"),
###XXX       cms.InputTag("l1extraParticles", "NonIsolated"),
###XXX       # UCT alg.
###XXX       cms.InputTag("l1extraParticlesUCT", "Isolated"),
###XXX       cms.InputTag("l1extraParticlesUCT", "NonIsolated"),
###XXX       # Crystal-level algo.
###XXX       cms.InputTag("L1EGammaCrystalsProducer","EGammaCrystal")
###XXX    ),
###XXX    L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster"),
###XXX    OfflineRecoClustersInputTag = cms.InputTag("correctedHybridSuperClusters"),
###XXX    L1TrackInputTag = cms.InputTag("TTTracksFromPixelDigisLargerPhi","Level1TTTracks"),
###XXX    #L1PixelTrackInputTag = cms.InputTag("L1PixelTrackFit","Level1PixelTracks"),
###XXX    L1TrackPrimaryVertexTag = cms.InputTag("L1TkPrimaryVertex"),
###XXX    doEfficiencyCalc = cms.untracked.bool(True),
###XXX    useOfflineClusters = cms.untracked.bool(False),
###XXX    useEndcap = cms.untracked.bool(False),
###XXX    turnOnThresholds = cms.untracked.vint32(20, 30, 16),
###XXX    histogramBinCount = cms.untracked.int32(60),
###XXX    histogramRangeLow = cms.untracked.double(0),
###XXX    histogramRangeHigh = cms.untracked.double(50),
###XXX    histogramEtaBinCount = cms.untracked.int32(20),
###XXX    genMatchDeltaRcut = cms.untracked.double(0.25),
###XXX    genMatchRelPtcut = cms.untracked.double(0.5)
###XXX )
###XXX 
###XXX process.load("SLHCUpgradeSimulations.L1EGRateStudies.L1EGCrystalsHeatMap_cff")
###XXX process.L1EGCrystalsHeatMap.saveAllClusters = cms.untracked.bool(True)
###XXX process.panalyzer = cms.Path(process.analyzer+process.L1EGCrystalsHeatMap)

process.source.inputCommands = cms.untracked.vstring(
    'keep *',
)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("tmp_eff.root"), 
   closeFileFast = cms.untracked.bool(True)
)

process.dumpPython()




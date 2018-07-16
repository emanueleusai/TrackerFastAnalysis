from CalibTracker.SiStripCommon.shallowTree_test_template import *
process.TFileService.fileName = '/eos/cms/store/user/xcoubez/SiStripNtuples/test_shallowGeneralProducerTTbar.root'

### Making the code run on MC / data and Collisions / Cosmics
from FWCore.ParameterSet.VarParsing import VarParsing

options = VarParsing ('python')

options.register('runOnData', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run on data"
)

options.register('runOnCosmics', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run on cosmics"
)

options.register('eventContent', 'FIXME',
    VarParsing.multiplicity.singleton,
    VarParsing.varType.string,
    "xml file for tuning of the event content, no default value provided"
)

options.register('keepClusters', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Keep clusters"
)

options.register('keepRechits', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Keep rechits (put clusters in global coordinates)"
)

options.register('keepTracks', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Keep tracks"
)

options.register('keepTrackClusters', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Keep tracks"
)

options.register('keepMuons', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Keep muons"
)

options.register('keepSim', False,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Keep SimHits and SimTracks"
)

options.register('CMSGeometry', True,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.bool,
    "Run with CMS Geometry - should be able to run on CRack later"
)

options.register('samplingInCollisions', 1000,
    VarParsing.multiplicity.singleton,
    VarParsing.varType.int,
    "Keep one very N events for collisions"
)

print "==========================="
print "Running on data:         %s"%('True' if options.runOnData            else 'False')
print "Running on cosmics:      %s"%('True' if options.runOnCosmics         else 'False')
print "Running with CMS:        %s"%('True' if options.CMSGeometry          else 'False')
print "Event content from:      " + options.eventContent
print "==========================="
print "Keeping clusters:        %s"%('True' if options.keepClusters         else 'False')
print "Keeping rechits:         %s"%('True' if options.keepRechits          else 'False')
print "Keeping tracks:          %s"%('True' if options.keepTracks           else 'False')
print "Keeping track clusters:  %s"%('True' if options.keepTrackClusters    else 'False')
print "Keeping muons:           %s"%('True' if options.keepMuons            else 'False')
print "Keeping sim:             %s"%('True' if options.keepSim              else 'False')
print "==========================="
print

###
process.load('CalibTracker.SiStripCommon.ShallowEventDataProducer_cfi')


###
process.load('CalibTracker.SiStripCommon.ShallowClustersProducer_cfi')

###
process.load('RecoTracker.TrackProducer.TrackRefitters_cff')
process.load('CalibTracker.SiStripCommon.ShallowRechitClustersProducer_cfi')

###
process.load('CalibTracker.SiStripCommon.ShallowTracksProducer_cfi')
if options.runOnCosmics :
    process.shallowTracks.Tracks = cms.InputTag("ctfWithMaterialTracksP5","")

###
from RecoTracker.TrackProducer.TrackRefitter_cfi import TrackRefitter
process.load('CalibTracker.SiStripCommon.ShallowTrackClustersProducer_cfi')
process.load('RecoTracker.TrackProducer.TrackRefitters_cff')
process.tracksRefit = TrackRefitter.clone()
process.shallowTrackClusters.Tracks = 'tracksRefit'

###
process.testTree = cms.EDAnalyzer(
   "ShallowTree",
   outputCommands = cms.untracked.vstring(
      'drop *',
      'keep *_shallowEventRun_*_*',
      'keep *_shallowClusters_*_*',
      'keep *_shallowRechitClusters_*_*',
      'keep *_shallowTracks_*_*',
      'keep *_shallowTrackClusters_*_*',
      )
   )

###
process.p = cms.Path(process.shallowEventRun*
                     process.shallowClusters*
                     process.siStripMatchedRecHits*process.shallowRechitClusters*
                     process.shallowTracks*
                     #process.MeasurementTrackerEvent*process.tracksRefit*process.shallowTrackClusters*
                     process.testTree)

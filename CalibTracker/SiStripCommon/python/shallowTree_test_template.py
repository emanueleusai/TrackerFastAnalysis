import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.patInputFiles_cff import filesRelValTTbarPileUpGENSIMRECO
import FWCore.Utilities.FileUtils as FileUtils
import das 
#from pdb import set_trace

def add_rawRelVals(process):   
   dataset = das.query('dataset file=%s' % process.source.fileNames[0], verbose=True)
   if not dataset:
      raise RuntimeError(
         'Das returned no dataset parent of the input file: %s \n'
         'The parenthood is needed to add RAW secondary input files' % process.source.fileNames[0]
         )
   raw_dataset = dataset[0].replace('GEN-SIM-RECO','GEN-SIM-DIGI-RAW-HLTDEBUG')
   raw_files = das.query('file dataset=%s' % raw_dataset, verbose=True)
   if not raw_files:
      raise RuntimeError('No files found belonging to the GEN-SIM-DIGI-RAW-HLTDEBUG sample!')
   #convert from unicode into normal string since vstring does not pick it up
   raw_files = [str(i) for i in raw_files]
   process.source.secondaryFileNames = cms.untracked.vstring(*raw_files)
   return process

process = cms.Process('JustATest')
process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load("Configuration.Geometry.GeometryRecoDB_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc')

process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.Services_cff')
process.TFileService = cms.Service( 
   "TFileService",
   fileName = cms.string( 'FIXME' ),
   closeFileFast = cms.untracked.bool(True)  
   ) 



## Maximal Number of Events
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

mylist = FileUtils.loadListFromFile('../python/ListCosmicsReco2017F.txt')
#mylist = FileUtils.loadListFromFile('../python/ListCharmonium.txt')
#mylist = FileUtils.loadListFromFile('../python/FileCRack.txt')
readFiles = cms.untracked.vstring( *mylist)
process.source = cms.Source (
    "PoolSource",
    #fileNames = filesRelValTTbarPileUpGENSIMRECO
    #fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/data/Run2017F/Cosmics/RECO/PromptReco-v1/000/305/018/00000/B49E4FA9-C3B1-E711-81F4-02163E01A1E2.root')
    fileNames = readFiles
    #fileNames = cms.untracked.vstring('root://xrootd-cms.infn.it//store/data/Run2017F/Charmonium/RECO/PromptReco-v1/000/306/460/00000/FC56B23F-9AC8-E711-BF48-02163E01A45E.root')
    )

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.options = cms.untracked.PSet(
    Rethrow = cms.untracked.vstring('OtherCMS', 
        'StdException', 
        'Unknown', 
        'BadAlloc', 
        'BadExceptionType', 
        'ProductNotFound', 
        'DictionaryNotFound', 
        'InsertFailure', 
        'Configuration', 
        'LogicError', 
        'UnimplementedFeature', 
        'InvalidReference', 
        'NullPointerError', 
        'NoProductSpecified', 
        'EventTimeout', 
        'EventCorruption', 
        'ScheduleExecutionFailure', 
        'EventProcessorFailure', 
        'FileInPathError', 
        'FileOpenError', 
        'FileReadError', 
        'FatalRootError', 
        'MismatchedInputFiles', 
        'ProductDoesNotSupportViews', 
        'ProductDoesNotSupportPtr', 
        'NotFound')
)

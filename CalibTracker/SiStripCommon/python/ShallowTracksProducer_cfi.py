import FWCore.ParameterSet.Config as cms

shallowTracks = cms.EDProducer("ShallowTracksProducer",
                               Tracks=cms.InputTag("generalTracks",""),
                               #Tracks=cms.InputTag("ctfWithMaterialTracksP5",""),
                               Prefix=cms.string("track"),
                               Suffix=cms.string(""))


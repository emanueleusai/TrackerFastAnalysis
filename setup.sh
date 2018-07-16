cmsrel CMSSW_9_2_13
cd CMSSW_9_2_13/src

git clone https://github.com/XavierAtCERN/TrackerFastAnalysis.git

mv TrackerFastAnalysis/CalibTracker/ .
rm -r TrackerFastAnalysis

cmsenv

scram b -j4

cd CalibTracker/SiStripCommon/test/

cmsRun test_shallowGeneralProducerMC_cfg.py

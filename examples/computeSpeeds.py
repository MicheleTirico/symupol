from symupol.analysis.spatialMeanSpeed import SpatialMeanSpeed

from symupol.analysis.abstractDF import AbstractDF
from symupol.analysis.analysis import Analysis
from symupol.analysis.sumPollutants import SumPollutants
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools
from symupol.edit.createCsvFromMod import CreateCsvFromMod
from symupol.edit.editFzp import EditFzp
from symupol.edit.mergeDF import MergeDF
from symupol.graph.graph import Graph
from symupol.graph.links import Links

# parameters analysis
test_delete_files=False
runComputeAbstractDF=False
runComputeSpeeds=True

# parameters charts
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP','id_split']
indicator_chart=list_indicators[5]
ts=900
ns=10
list_ts_chart=[_ for _ in range (0,10,9)]

# paths
nameFile="lafayette_ts-{0:0>4}_ns-{1:0>4}_{2}".format(ns,ts,indicator_chart)
pathconfig="/home/mt_licit/project/symupol/scenarios/lafayette_03/config.xml"

# init config
config=Config(pathconfig)

# logger
logger=Logger(config=config,storeLog=True)
logger.setDisplay(True,True,True,True)
logger.storeLocal(True)

# set urls
config.setLogger(logger)
config.initUrl()

#init tools
tools=Tools(config=config)
config.setTools(tools=tools)

# init controller
controller=Controller(config)
controller.deleteTmp(test_delete_files)
controller.deleteOutput(test_delete_files)
controller.initFolder()
logger.initStoreLog()
logger.storeFile()
controller.copyToTmp(True) # copy the setup to the .tmp folder

# analysis
analysis=Analysis(config=config,controller=controller)
adv=AbstractDF(analysis=analysis)
adv.setParams(addRelativePosition=True, addCountVehicles=True,addTimeSlots=True,addPosSegment=True)
adv.getAbstractDF(storeAbstractDF=runComputeAbstractDF,computeIfExist=runComputeAbstractDF) # todo readIfExist

# spatial mean speed
sms=SpatialMeanSpeed(analysis=analysis)
analysis.set_splits(ns=[10])
analysis.set_timeSplots(ts=[900])

sms.compute(run=runComputeSpeeds)

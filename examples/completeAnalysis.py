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
runEditFzp=False
runCreateLinks=False
runCreateCsv=False
runMergeDf=False
runComputeAbstractDF=False
runSumPollutants=True

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

# edit fzp
ef=EditFzp(config=config,run=runEditFzp)
ef.init()
ef.compute(storeFzp=runEditFzp,storeTrajectories=runEditFzp,runIfExist=runEditFzp) # create also trajectories

# create Links
graph=Graph(config=config,controller=controller)
links=Links(graph=graph)
links.createCsv(run=runCreateLinks)
links.addLengthTotrajectories(run=runCreateLinks)
links.splitLinks_ns(run=False)

# create csv from mod
ccfm=CreateCsvFromMod(config=config,controller=controller,run=runCreateCsv)
ccfm.createCsv(runIfExist=runCreateCsv)

# merge DF
mdf=MergeDF(config=config,run=runMergeDf)
mdf.mergeDF(comuteIfExist=runMergeDf,removeLines=runMergeDf)

# analysis
analysis=Analysis(config=config,controller=controller)
adv=AbstractDF(analysis=analysis)
adv.setParams(addRelativePosition=True, addCountVehicles=True,addTimeSlots=True,addPosSegment=True)
adv.getAbstractDF(storeAbstractDF=runComputeAbstractDF,computeIfExist=runComputeAbstractDF) # todo readIfExist

# sum pollutants
sp=SumPollutants(analysis=analysis)
sp.computeSumPerSplitCost(run=runSumPollutants)


from symupol.analysis.abstractDF import AbstractDF
from symupol.analysis.analysis import Analysis
from symupol.analysis.pollutantDistribution import PollutantDistribution
from symupol.analysis.sumPollutants import SumPollutants
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools
from symupol.graph.graph import Graph
from symupol.graph.links import Links

test_delete_files=False
runEditFzp=True
pathconfig="/home/mt_licit/project/symupol/scenarios/lafayette/config.xml"

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

ts=40000
lms=20
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP','id_split']
indicator_chart=list_indicators[2]

nameFile="lafayette_ts-{:0>4}_lms-{:0>4}".format(ts,lms)
pathLinks="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/"+nameFile+".csv"
# pathJpg="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/charts/"+nameFile+"_"+indicator_chart+".jpg"
pathJpg="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/charts/test.jpg"

# create Links
graph=Graph(config=config,controller=controller)
links=Links(graph=graph)
links.setInputXml(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/scenarios/lafayette/CoursLafayette.xml")
links.splitLinks_ns(run=False,listSplit=[10,20,100])

# analysis
analysis=Analysis(config=config,controller=controller)
adv=AbstractDF(analysis=analysis)
adv.setParams(addRelativePosition=True, addCountVehicles=True,addTimeSlots=True,addPosSegment=False)
adv.getAbstractDF(storeAbstractDF=False,computeIfExist=False) # todo readIfExist

# listSplit=[10]
# listTs=[900]

sp=SumPollutants(analysis=analysis)
sp.computeSumPerSplitCost(run=True)

# get chart
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP','id_split']
indicator_chart=list_indicators[0]



pl=PollutantDistribution(analysis=analysis)
# pl.setListTimeSplot(listTs)
# pl.setListSplit(listSplit)

pl.setPathOutputJpg(pathJpg)
pl.compute(run=True)

pl.getSingleDistr_multiTs(run=True,ts=20000,ns=100,list_ts_chart=[1,2],indicator="FC",saveJpg=True)
#pl.gestSingleBar(run=True,ts=900,ns=10,ts_chart=1,indicator="FC",saveJpg=True)



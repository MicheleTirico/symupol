from symupol.analysis.abstractDF import AbstractDF
from symupol.analysis.analysis import Analysis
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
# pathconfig="/home/mt_licit/project/symupol/scenarios/test_grid_01/config.xml"

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

# create Links
graph=Graph(config=config,controller=controller)
links=Links(graph=graph)
links.setInputXml(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/scenarios/lafayette/CoursLafayette.xml")
links.setOutputCsv(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/links.csv")
links.setInputTrajectories(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/trajectoires.csv")
links.setOutputTrajectories(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/trajectoires2.csv")
# links.createCsv(run=True)
# links.addLengthTotrajectories(run=True)
links.splitLinks_ns(run=True)

# analysis
a=Analysis(config=config,controller=controller)
adv=AbstractDF(analysis=a)
adv.setParams(addRelativePosition=True, addCountVehicles=True,addTimeSlots=True,addPosSegment=True)
adv.getAbstractDF(storeAbstractDF=True,computeIfExist=True) # todo readIfExist

sp=SumPollutants(analysis=a)
sp.computeNsplitCost(run=True,compute_df_spi=True,compute_df=True)
# sp.addIdSplit_ns(run=True)
# sp.addGeometryLinks_ns(run=True)

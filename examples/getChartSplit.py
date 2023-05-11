from symupol.analysis.abstractDF import AbstractDF
from symupol.analysis.analysis import Analysis
from symupol.analysis.sumPollutants import SumPollutants
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools
from symupol.graph.computeGeoPandasDf import ComputeGeoPandasDf
from symupol.graph.graph import Graph

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

# graph
pathLinks="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/lafayette_ts-20000_lms-0020_lg.csv"
pathJpg="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/lafayette_ts-20000_lms-0020_lg.jpg"
# init graph
graph=Graph(config=config,controller=controller)
graph.setPathInputLinks(path=pathLinks)
graph.setPathOutputJpg(pathJpg)
graph.initDf()

graph.initGraph()

ggpdf=ComputeGeoPandasDf(graph=graph)
ggpdf.computeSingleGraph(ts=20000,lms=5)


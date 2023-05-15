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
ts=40000
ts_chart=0
ns=20
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP','id_split']
indicator_chart=list_indicators[0]
nameFile="lafayette_ts-{:0>4}_ns-{:0>4}_gl".format(ts,ns)
pathLinks="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/"+nameFile+".csv"
pathJpg="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/"+nameFile+"_"+indicator_chart+".jpg"

# init graph
graph=Graph(config=config,controller=controller)
graph.setPathInputLinks(path=pathLinks)
graph.setPathOutputJpg(pathJpg)
graph.initDf()

graph.initGraph()

ggpdf=ComputeGeoPandasDf(graph=graph)
ggpdf.computeSingleGraph(ts=ts,ts_chart=ts_chart,indicator_chart=indicator_chart)


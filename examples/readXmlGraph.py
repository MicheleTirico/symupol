from symupol.graph.graph import Graph
from symupol.graph.computeGeoPandasDf import ComputeGeoPandasDf
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools

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

pathLinks="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/links.csv"
# init graph
graph=Graph(config=config,controller=controller)
graph.setPathInputLinks(path=pathLinks)
graph.initDf()
graph.initGraph()

# casting files
ggpdf=ComputeGeoPandasDf(graph=graph)
ggpdf.computeGenericGraph()
graph.getInfo()

#ggpdf.test()


# export
graph.plotGeoDf(run=False)
graph.saveGeoDfJpg(run=False)
# graph.saveGeoDf(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/test_cast.geojson")
# ggpdf.test()

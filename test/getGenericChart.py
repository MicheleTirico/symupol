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

#

# init graph
graph=Graph(config=config,controller=controller)
ggpdf=ComputeGeoPandasDf(graph=graph)

mls=[20]
# nameFile="lafayette_ts-{:0>4}_ns-{:0>4}_gl".format(ts,ns)

for m in mls:

    nameFile="lafayette_link_splitted_lms_{:0>4}".format(m)

    pathLinks="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/"+nameFile+".csv"
    graph.setPathInputLinks(path=pathLinks)
    graph.initDf()


    pathJpg="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/charts/"+nameFile+"_generic.jpg"
    ggpdf.setPathOutputJpg(pathJpg)
    ggpdf.getGenericGraph(run=True,saveJpg=True,pathJpg=pathJpg)


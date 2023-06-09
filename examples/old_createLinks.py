from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools
from symupol.graph.graph import Graph
from symupol.graph.links import Links

test_delete_files=False
pathconfig="/home/mt_licit/project/symupol/scenarios/lafayette_02/config.xml"
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
links.setInputXml(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/scenarios/lafayette_02/CoursLafayette.xml")
links.setOutputCsv(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette_02/links.csv")
links.setInputTrajectories(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette_02/trajectoires.csv")
links.setOutputTrajectories(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette_02/trajectoires2.csv")

# links.setInputXml(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/scenarios/test_grid_01/5x5grid.xml")
# links.setOutputCsv(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/test_grid_01/links.csv")
# links.setInputTrajectories(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/test_grid_01/trajectoires.csv")
# links.setOutputTrajectories(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/test_grid_01/trajectoires2.csv")

links.createCsv(run=True)
links.addLengthTotrajectories(run=True)



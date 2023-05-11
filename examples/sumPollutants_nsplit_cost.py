from symupol.analysis.abstractDF import AbstractDF
from symupol.analysis.analysis import Analysis
from symupol.analysis.sumPollutants import SumPollutants
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools

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

# analysis
a=Analysis(config=config,controller=controller)
adv=AbstractDF(analysis=a)
adv.getAbstractDF(storeAbstractDF=False,readIfExist=True) # todo readIfExist
sp=SumPollutants(analysis=a)
sp.compute()
# sp.computeMaxLen()
sp.addIdSplit(run=True)

from symupol.edit.createCsvFromMod import CreateCsvFromMod
from symupol.edit.mergeDF import MergeDF
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

# create csv from mod
ccfm=CreateCsvFromMod(config=config,run=True)
ccfm.setPathInputMod(path="/home/mt_licit/project/symupol/scenarios/lafayette/lafayette_100.mod")
ccfm.setPathOutputCsv(path="/home/mt_licit/project/symupol/outputs/lafayette/lafayette_100.csv")
ccfm.createCsv(runIfExist=False)

# merge DF
mdf=MergeDF(config=config,run=True)
mdf.setPathInputMod(path="/home/mt_licit/project/symupol/outputs/lafayette/lafayette_100.csv")
mdf.setPathInputCsv(path="/home/mt_licit/project/symupol/outputs/lafayette/trajectoires.csv")
mdf.setPathOutputCsv(path="/home/mt_licit/project/symupol/outputs/lafayette/merged.csv")
mdf.mergeDF()


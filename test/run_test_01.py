#from symupy import *
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.edit.editOutputSymupy import EditOutputSymupy
from symupol.edit.editSetupSymuvia import EditSetupSymuvia
from symupol.analysis.mergeTable import MergeTable

test_run=False
test_delete_files=False
computeDriTraj=True
computeFzp=True
computeMergeTable=False

pathconfig="/home/mt_licit/project/symupol/symupol/scenarios/test_grid_01/config.xml"
config=Config(pathconfig)

# logger
logger=Logger(config, True)
logger.setDisplay(True,True,True,True)
logger.storeLocal(True)

config.setLogger(logger)
config.initUrl()

controller=Controller(config)
controller.deleteTmp(test_delete_files)
controller.deleteOutput(test_delete_files)
controller.initFolder()
#controller.initTmp()
logger.initStoreLog()
logger.storeFile()

controller.copyToTmp(True) # copy the setup to the .tmp folder

editSetupSymuvia=EditSetupSymuvia(config)
editSetupSymuvia.editParametersTag(True,"simulation","SIMULATIONS","SIMULATION","edit setup simulation")
editSetupSymuvia.editParametersTag(True,"trafic","TRAFICS","TRAFIC","edit setup trafic")
editSetupSymuvia.editParametersTag(True,"scenario","SCENARIOS","SCENARIO","edit setup scenario")

controller.copyToOutput(True)
controller.initSymupy()
controller.runSymupy(test_run)
controller.moveOutput(True)

#controller.editOutputSymupy()
eos=EditOutputSymupy(computeDriTraj,config=config,logger=logger)
eos.initClass()
#eos.exportTrajectoiresMerged()
eos.exportFzp(computeFzp)

controller.initPhem()
controller.runPhem()

mergeTable=MergeTable(computeMergeTable,config)
mergeTable.compute()





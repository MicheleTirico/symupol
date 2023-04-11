from symupol.analysis.vehicles import Vehicles
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.edit.editFzp import EditFzp
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

# fzp
ef=EditFzp(config=config,run=runEditFzp)
ef.init()
ef.setPathOutputSymuvia(path="/home/mt_licit/project/symupol/outputs/test_grid_01/test_grid_01_output_sy.xml")
ef.setPathOutputCsvVehicles(path="/home/mt_licit/project/symupol/outputs/test/test_output_vehicles.csv")
ef.compute(storeFzp=False,storeCsv=True)

v=Vehicles(config=config,run=True)
v.setPathOutputPhem("/home/mt_licit/project/symupol/outputs/test/test_OutputPhemMod.mod")
v.createVehicles()

#v.setPathFzp("/home/mt_licit/project/symupol/outputs/test/test_OutputPhemMod.mod")
v. addTripVehiclesFromFzp()


from symupol.analysis.vehicles import Vehicles
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.edit.createCsvFromMod import CreateCsvFromMod
from symupol.edit.editFzp import EditFzp
from symupol.control.tools import Tools
from symupol.edit.mergeDF import MergeDF

test_delete_files=False
runEditFzp=True
pathconfig="/home/mt_licit/project/symupol/scenarios/test_martin_01/config.xml"

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
#controller.deleteTmp(test_delete_files)
#ontroller.deleteOutput(test_delete_files)
controller.initFolder()
logger.initStoreLog()
logger.storeFile()
controller.copyToTmp(True) # copy the setup to the .tmp folder

# fzp
# ef=EditFzp(config=config,run=True)
# ef.init()
# ef.setPathOutputSymuvia(path="/home/mt_licit/project/symupol/outputs/test_grid_01/test_grid_01_output_sy.xml")
# ef.setPathOutputCsvVehicles(path="/home/mt_licit/project/symupol/outputs/test_grid_01/test_output_vehicles.csv")
# ef.compute(storeFzp=True,storeCsv=True,runIfExist=True)

# create csv from mod
ccfm=CreateCsvFromMod(config=config,run=True)
ccfm.setPathInputMod(path="/home/mt_licit/project/symupol/scenarios/test_martin_01/test_01_100.mod")
ccfm.setPathOutputCsv(path="/home/mt_licit/project/symupol/outputs/test_martin_01/test_01_100.csv")
ccfm.createCsv(runIfExist=False)

# merge DF
mdf=MergeDF(config=config,run=True)
mdf.setPathInputMod(path="/home/mt_licit/project/symupol/outputs/test_martin_01/test_01_100.csv")
mdf.setPathInputCsv(path="/home/mt_licit/project/symupol/outputs/test_martin_01/speedProfileForPhem_2.fzp")
mdf.setPathOutputCsv(path="/home/mt_licit/project/symupol/outputs/test_martin_01/output_martin.csv")
mdf.mergeDF()

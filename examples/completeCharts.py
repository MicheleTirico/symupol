from symupol.analysis.analysis import Analysis
from symupol.analysis.pollutantDistribution import PollutantDistribution
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools

# parameters analysis
test_delete_files=False
runEditFzp=True
runCreateLinks=True
runCreateCsv=True
runMergeDf=True
runComputeAbstractDF=True
runSumPollutants=False

# parameters charts
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP']
indicator_pos=0
indicator_name=list_indicators[indicator_pos]
ts=900
ns=10
list_ts_chart=[_ for _ in range (0,10,9)]

# paths
nameFile="lafayette_ts-{0:0>4}_ns-{1:0>4}_{2}".format(ns,ts,indicator_name)
pathChart_noExt="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette_03/charts/"+nameFile
pathconfig="/home/mt_licit/project/symupol/scenarios/lafayette_03/config.xml"

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
analysis=Analysis(config=config,controller=controller)

# charts
pl=PollutantDistribution(analysis=analysis)
pl.compute(run=runSumPollutants)
pl.setTimeRange(timeRange=["6:00:00","23:00:00"])   # to complete
for indicator_pos in range(0,6):
    indicator_name=list_indicators[indicator_pos]
    nameFile="lafayette_ts-{0:0>4}_ns-{1:0>4}_{2}".format(ns,ts,indicator_name)
    pathChart_noExt="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette_03/charts/"+nameFile
    pl.getDistributionPollutantsPerSplit(run=True,ts=ts,ns=ns,list_ts_chart=list_ts_chart,indicator_pos=indicator_pos,show=False,saveJpg=True,pathJpg=pathChart_noExt+"_distPolPerSp.jpg")


from symupol.analysis.abstractDF import AbstractDF
from symupol.analysis.analysis import Analysis
from symupol.analysis.pollutantDistribution import PollutantDistribution
from symupol.analysis.sumPollutants import SumPollutants
from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools
from symupol.graph.graph import Graph
from symupol.graph.links import Links
import os

test_delete_files=False
runEditFzp=True
pathconfig="/home/mt_licit/project/symupol/scenarios/lafayette_02/config.xml"

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

# parameters
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP','id_split']
indicator_chart=list_indicators[5]
ts=900
ns=10
list_ts_chart=[_ for _ in range (0,10,9)]
nameFile="lafayette_ts-{0:0>4}_ns-{1:0>4}_{2}".format(ns,ts,indicator_chart)
pathChart_noExt="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette_02/charts/"+nameFile

# # create Links
# graph=Graph(config=config,controller=controller)
# links=Links(graph=graph)
# links.setInputXml(path="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/scenarios/lafayette/CoursLafayette.xml")
# links.splitLinks_ns(run=False,listSplit=[10,20,100])
#
# # analysis
analysis=Analysis(config=config,controller=controller)
# adv=AbstractDF(analysis=analysis)
# adv.setParams(addRelativePosition=True, addCountVehicles=True,addTimeSlots=True,addPosSegment=False)
# adv.getAbstractDF(storeAbstractDF=False,computeIfExist=False) # todo readIfExist
#
# sp=SumPollutants(analysis=analysis)
# sp.computeSumPerSplitCost(run=False)
#
pl=PollutantDistribution(analysis=analysis)
# pl.setPathOutputJpg(pathJpg)
pl.compute(run=False)

# get chart
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP','id_split']
pl.getSingleDistr_multiTs(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,indicator=indicator_chart,show=True,saveJpg=True,pathJpg=pathChart_noExt+"_multiTs.jpg")
pl.getScatterPlot(run=False,ts=ts,list_ts_chart=list_ts_chart,indicator=indicator_chart,show=True,saveJpg=True,pathJpg=pathChart_noExt+"_scatter.jpg")
pl.getBoxPlot(run=True,ts=ts,list_ts_chart=list_ts_chart,indicator=indicator_chart,show=True,saveJpg=True,pathJpg=pathChart_noExt+"_boxplot.jpg")
pl.getScatterPlot_diagonal(run=False,ts=ts,ns=ns,list_ts_chart=[0,5],indicator="PM_TP",show=True,saveJpg=True,pathJpg=pathChart_noExt+"_scatter_diagonal.jpg")




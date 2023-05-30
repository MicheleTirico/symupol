from symupol.analysis.analysis import Analysis
from symupol.analysis.chartTimeSlotDistribution import ChartTimeSlotDistribution
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
ts=1500
ns=10
list_ts_chart=[_ for _ in range (0,10,9)]

# paths
nameFile="lafayette_ts-{0:0>4}_ns-{1:0>4}".format(ts,ns)
path_folder="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette_03/charts_timeSlots/"
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
analysis.readAbstractDF(run=True)
# analysis.computeGroupbyTimeSlot(run=True,ts=ts)

# charts
ctsd=ChartTimeSlotDistribution(analysis=analysis)
ctsd.setTimeSplot(ts=ts)
ctsd.setNumberSplit(ns=ns)
ctsd.readGroupBy(run=False)

# for indicator_pos in [0]:
for indicator_pos in range(len(analysis.pollutants)):
    indicator_name,indicator_print,indicator_measure,indicator_complete_print=analysis.getIndicator(indicator_pos)
    print (indicator_pos,indicator_name,indicator_print,indicator_measure)

    ctsd.getChartTimeSlot_distribution(run=False,indicator_pos=indicator_pos,show=False,pathJpg=path_folder+nameFile+"_"+indicator_name+"_TimeSlotDist.jpg")
    if indicator_name!="nVec": ctsd.getChartTimeSlot_distribution_normNVec(run=False,indicator_pos=indicator_pos,show=True,pathJpg=path_folder+nameFile+"_"+indicator_name+"_TimeSlotDist_normNVec.jpg")
    # ctsd.getChartTimeSlot_distribution_normNVec(run=indicator_name!="nVec",indicator_pos=indicator_pos,show=False,pathJpg=path_folder+nameFile+"_"+indicator_name+"_TimeSlotDist_normNVec.jpg")

    ctsd.getChartTimeSlot_boxPlot(run=True,indicator_pos=indicator_pos,show=False,pathJpg=path_folder+nameFile+"_"+indicator_name+"_TimeSlotDist_boxPlot.jpg")
    ctsd.getChartTimeSlot_violin(run=True,indicator_pos=indicator_pos,show=False,pathJpg=path_folder+nameFile+"_"+indicator_name+"_TimeSlotDist_violin.jpg")
    ctsd.getChartTimeSlot_catplot(run=False,indicator_pos=indicator_pos,show=False,pathJpg=path_folder+nameFile+"_"+indicator_name+"_TimeSlotDist_catplot.jpg")


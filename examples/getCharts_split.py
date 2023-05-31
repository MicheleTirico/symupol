from symupol.analysis.analysis import Analysis
from symupol.analysis.chartSplitDistribution import ChartSplitDistribution
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
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP',"nVec"]
indicator_pos=0
indicator_name=list_indicators[indicator_pos]
ts=900
ns=10
list_ts_chart=[_ for _ in range (0,10,9)]

# paths
nameFile="lafayette_ts-{0:0>4}_ns-{1:0>4}".format(ts,ns)
path_folder= "/home/mt_licit/project/symupol/outputs/lafayette_03/charts_splits_03/"
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
controller.createFolders([path_folder])

# analysis
analysis=Analysis(config=config,controller=controller)

# charts
csd=ChartSplitDistribution(analysis=analysis)
csd.compute(run=runSumPollutants)
csd.setTimeRange(timeRange=["6:00:00","23:00:00"])   # to complete
for indicator_pos in range(0,6):
    indicator_name=list_indicators[indicator_pos]
    nameFile_indicator="lafayette_ts-{0:0>4}_ns-{1:0>4}_{2}".format(ts,ns,indicator_name)

    csd.getDistributionPollutantsPerSplit(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,indicator_pos=indicator_pos,show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_"+indicator_name+"_distPolPerSp.jpg")
    csd.getBoxPlotPerSplit(run=True,ts=ts,ns=ns,list_ts_chart=list_ts_chart,indicator_pos=indicator_pos,show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_"+indicator_name+"_boxPlot.jpg")
    csd.getDistributionPollutantsPerSplit_normNvec(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,indicator_pos=indicator_pos,show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_"+indicator_name+"_distPolPerSp_normnVec.jpg")

    csd.getDistributionPollutantsPerSplit_normLength(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,indicator_pos=indicator_pos,show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_"+indicator_name+"_distPolPerSp_normDst.jpg")
    csd.getDistributionPollutantsPerSplit_normLength_normVeh(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,indicator_pos=indicator_pos,show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_"+indicator_name+"_distPolPerSp_normDstVeh.jpg")

csd.getSumVehicles(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_nVec.jpg")
csd.getMultiPlotDP(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,list_indicator_pos=[1,2,3,4,5,6],show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_multiplotdistPolPerSp.jpg")
csd.getMultiPlotDP_normLength_normVeh(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,list_indicator_pos=[1,2,3,4,5,6],show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_multiplotdistPolPerSp_normLen_normVeh.jpg")
csd.getMultiPlotDP_normLength(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,list_indicator_pos=[1,2,3,4,5,6],show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_multiplotdistPolPerSp_normLen.jpg")
csd.getMultiPlotDP_normVeh(run=False,ts=ts,ns=ns,list_ts_chart=list_ts_chart,list_indicator_pos=[1,2,3,4,5,6],show=False,saveJpg=True,pathJpg=path_folder+nameFile+"_multiplotdistPolPerSp_normVeh.jpg")






# get correlation matrix between a pollutant and a traffic variable
indicator_pos=0
csd.getCorrelationMatrix(run=False,ts=ts,ns=ns,show=True,saveJpg=True,indicator_pos=0,pathJpg=path_folder+nameFile+"_"+list_indicators[indicator_pos]+"_corrMatr.jpg")

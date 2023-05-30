from symupol.control.logger import Logger
from symupol.control.config import Config
from symupol.control.controller import Controller
from symupol.control.tools import Tools
from symupol.graph.computeGeoPandasDf import ComputeGeoPandasDf
from symupol.graph.graph import Graph

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

ts=40000
lms=20
list_indicators=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP','id_split']
indicator_chart=list_indicators[0]

nameFile="lafayette_ts-{:0>4}_lms-{:0>4}".format(ts,lms)
pathLinks="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/"+nameFile+".csv"
pathJpg="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/charts/"+nameFile+"_"+indicator_chart+".jpg"

# graph
graph=Graph(config=config,controller=controller)
graph.setPathInputLinks(path=pathLinks)
graph.initDf()
graph.initGraph()

# get chart
ggpdf=ComputeGeoPandasDf(graph=graph)
ggpdf.setPathOutputJpg(pathJpg)
ggpdf.getChart_lms(ts=ts,ts_chart=10, lms=lms,indicator=indicator_chart,saveJpg=True)

# ggpdf.computeSingleGraph(ts=ts,ts_chart=1,indicator_chart=list_indicators[0],saveJpg=True)


# for t in [900,1500,40000]:
#     for n in [5,10,20]:
#         for i in range(len(list_indicators)):
#             nameFile="lafayette_ts-{:0>4}_ns-{:0>4}_gl".format(t,n)
#             pathLinks="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/"+nameFile+".csv"
#             graph.setPathInputLinks(path=pathLinks)
#             graph.initDf()
#             graph.initGraph()
#             pathJpg="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/charts/"+nameFile+"_"+list_indicators[i]+".jpg"
#             ggpdf.setPathOutputJpg(pathJpg)
#             ggpdf.computeSingleGraph(ts=t,ts_chart=1,indicator_chart=list_indicators[i],saveJpg=True)


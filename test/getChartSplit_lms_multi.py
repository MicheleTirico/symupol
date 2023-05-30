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


# graph
graph=Graph(config=config,controller=controller)



for t in config.paramAnalysisListTimeSlot:
    for lms in config.paramAnalysisLengthMaxSplit:
        for i in range(len(list_indicators)):
            nameFile="lafayette_ts-{:0>4}_lms-{:0>4}".format(ts,lms)
            pathLinks="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/"+nameFile+"_gl.csv"
            graph.setPathInputLinks(path=pathLinks)
            graph.initDf()
            graph.initGraph()
            # get chart
            ggpdf=ComputeGeoPandasDf(graph=graph)
            test =1
            ts_pos=1
            while test !=0 and ts_pos<100:
                pathJpg="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/charts/"+nameFile+"_"+list_indicators[i]+"_ts-pos-{:4>0}".format(ts_pos)+".jpg"

                ggpdf.setPathOutputJpg(pathJpg)

                test=ggpdf.getChart_lms(ts=ts,ts_chart=ts_pos, lms=lms,indicator=list_indicators[i],saveJpg=True)
                ts_pos+=1



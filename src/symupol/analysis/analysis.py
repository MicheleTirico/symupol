from symupol.control.config import Config
from symupol.control.controller import Controller
import sys
import pandas as pd

class Analysis():
    def __init__(self,
                 config:Config,
                 controller:Controller):
        self.config=config
        self.controller=controller
        self.logger=self.config.logger

        self.config.logger.log(cl=self,method=sys._getframe(),message="initialize Analysis")
        self.abstractDF=None

        # paths
        self.pathTableMerged=    self.config.pathOutputMerged
        self.pathAbstractDF=     self.config.pathAbstractDF

        # variables
        self.pollutants=                ['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP',"nVec"]
        self.pollutantsPrint=           ['Fuel consumption', 'CO_2', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP',"n. of vehicles"]
        self.pollutantsCompletePrint=   ['Fuel consumption', 'CO_2 emission', 'NOx_TP emission', 'CO_TP emission', 'HC_TP emission', 'PM_TP emission', 'PN_TP  emission',"n. of vehicles"]
        self.pollutantsMeasure=         ["g/h","g/h","g/h","g/h","g/h","g/h","g/h","-"]


    def set_splits(self,ns):        self.config.paramAnalysisNumberOfSplit=ns
    def set_timeSplots(self,ts):            self.config.paramAnalysisListTimeSlot=ts


    def readAbstractDF(self,run):
        if run:
            self.config.logger.log(cl=self,method=sys._getframe(),message="read abstract df")
            self.abstractDF=pd.read_csv(self.pathAbstractDF,sep=";")

    def saveJpg (self,saveJpg,pathJpg,fig):
        if saveJpg:
            self.config.logger.log(cl=self,method=sys._getframe(),message="figure stored at: "+pathJpg)
            fig.savefig(pathJpg)

    def saveJpg2 (self,pathJpg,fig):
        if pathJpg!=None:
            self.config.logger.log(cl=self,method=sys._getframe(),message="figure stored at: "+pathJpg)
            print (pathJpg)
            fig.savefig(pathJpg)

    def getIndicator(self,indicator_pos):
        return  self.pollutants[indicator_pos], self.pollutantsPrint[indicator_pos], self.pollutantsMeasure[indicator_pos], self.pollutantsCompletePrint[indicator_pos]

    def computeGroupbyTimeSlot(self,run,ts):
        if run:
            self.config.logger.log(cl=self,method=sys._getframe(),message="compute groupby ts: {}".format(ts))
            path_groupby=self.config.folder_output+self.config.scenario+"_groupby"+"_ts-{:0>4}".format(ts)+".csv"

            # get abstract DF
            try:
                assert self.abstractDF!=None
                self.config.logger.warning(cl=self,method=sys._getframe(),message="Abstract DF founded. Do nothing.",doReturn=False,doQuit=False)
            except AssertionError:
                self.config.logger.warning(cl=self,method=sys._getframe(),message="Abstract DF not founded. Read path",doReturn=False,doQuit=False)
                self.readAbstractDF(run=True)

            # group by
            self.config.logger.log(cl=self,method=sys._getframe(),message="Group by ts: {}".format(ts))
            self.__dfGroupby=self.abstractDF.groupby("ts-{:0>4}".format(ts)).sum()

            # reset index
            self.__dfGroupby=self.__dfGroupby.reset_index()

            # remove unusefull columns
            try:
                self.config.logger.log(cl=self,method=sys._getframe(),message="Remove unusefull columns")
                self.__dfGroupby = self.__dfGroupby[["ts-{:0>4}".format(ts),"dst","FC","CO2_TP","NOx_TP","CO_TP","HC_TP","PM_TP","PN_TP","length","nVec"]]
            except KeyError:
                self.config.logger.warning(cl=self,method=sys._getframe(),message="Cannot remove unusefull columns. Do nothing.",doReturn=False,doQuit=False)

            # store
            self.config.logger.log(cl=self,method=sys._getframe(),message="store path: {}".format(path_groupby))
            self.__dfGroupby.to_csv(path_groupby,sep=";")


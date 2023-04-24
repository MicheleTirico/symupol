import sys
import pandas as pd
import numpy as np

class AbstractDF():
    def __init__(self,analysis):
        self.__analysis=analysis



        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="initialize abstract DF")

    def setPathTableMerged(self,path):  self.__analysis.pathTableMerged=path
    def setPathAbstractDF(self,path):   self.__analysis.pathAbstractDF=path

    def getAbstractDF(self,storeAbstractDF,readIfExist):        # TODO readIfExist
        # TODO add test read or create
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  create abstract DF")
        self.__analysis.existAbstractDF,self.__analysis.abstractDF=self.__createAbstractDF()
        self.__addRelativePosition(run=True)
        self.__addCountVehicles(run=True)
        self.__addTimeSlots(run=True)
        self.__addPosSegment(run=True)
        self.__storeAbstractDF(storeAbstractDF=storeAbstractDF,df=self.__analysis.abstractDF)
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish create abstract DF")

    def __createAbstractDF(self):
        df1=pd.read_csv(filepath_or_buffer=self.__analysis.pathTableMerged,sep=";")
        data=df1[['t', 'id',"dst",'tron','type',"vit","z","length","FC","CO2_TP","NOx_TP","CO_TP","HC_TP","PM_TP","PN_TP"]]
        df2=pd.DataFrame(data)
        self.__analysis.abstractDF=df2
        return True,df2

    def __addRelativePosition(self,run):
        if run:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  add relative position of vehicle over the link")
            self.__analysis.abstractDF["dst_rel"]=self.__analysis.abstractDF["dst"]/self.__analysis.abstractDF["length"]           # print (self.__analysis.abstractDF)
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish add relative position of vehicle over the link")

    def __addCountVehicles(self,run):
        if run:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  add count  vehicles")
            self.__analysis.abstractDF["nVec"]=1                           # print (self.__analysis.abstractDF)
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish add count vehicles")

    def __addPosSegment(self,run):
        if run:
            for split in self.__analysis.config.paramAnalysisNumberOfSplit:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  add position of vehicle in the segment for the split: "+split)
                self.__analysis.abstractDF["nSplit_"+str(split)]= self.__analysis.abstractDF["dst_rel"]*int(split)                    # print (self.__analysis.abstractDF)
                self.__analysis.abstractDF["nSplit_"+str(split)]=self.__analysis.abstractDF["nSplit_"+str(split)].apply(np.floor)
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish add position of vehicle in the segment for the split: "+split)

    def __addTimeSlots(self,run):
        if run:
            for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  add time slots")
                self.__analysis.abstractDF["ts_"+str(ts)]= self.__analysis.abstractDF["t"]/int (ts)                         # print (self.__analysis.abstractDF)
                self.__analysis.abstractDF["ts_"+str(ts)]=self.__analysis.abstractDF["ts_"+str(ts)].apply(np.floor)
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish add time slots")

    def __storeAbstractDF(self,storeAbstractDF,df):
        if storeAbstractDF:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  store abstract DF")
            df.to_csv(self.__analysis.pathAbstractDF, header=True)
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish store abstract DF")

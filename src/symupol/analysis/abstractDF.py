import sys
import pandas as pd
import numpy as np
import os

class AbstractDF():
    def __init__(self,analysis):
        self.__analysis=analysis

        self.__runAddRelativePosition=True
        self.__runAddCountVehicles=True
        self.__runAddTimeSlots=True
        self.__runAddPosSegment=True
        
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="initialize abstract DF")

    def setPathTableMerged(self,path):  self.__analysis.pathTableMerged=path
    def setPathAbstractDF(self,path):   self.__analysis.pathAbstractDF=path

    def getAbstractDF(self,storeAbstractDF,computeIfExist):        # TODO readIfExist
        # TODO add test read or create
        try:
            if computeIfExist==False: assert os.path.exists(self.__analysis.pathAbstractDF)!=True
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="abstract DF has not been created. Do it now. ")
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  create abstract DF")
            self.__analysis.existAbstractDF,self.__analysis.abstractDF=self.__createAbstractDF()
            self.__addRelativePosition(run=self.__runAddRelativePosition)
            self.__addCountVehicles(run=self.__runAddCountVehicles)
            self.__addTimeSlots(run=self.__runAddTimeSlots)
            self.__addPosSegment(run=self.__runAddPosSegment)
            self.__checkInfDistRel(run=True)
            self.__checkInfPosSegment(run=True)
            self.__storeAbstractDF(storeAbstractDF=storeAbstractDF,df=self.__analysis.abstractDF)
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish create abstract DF")

        except AssertionError:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="abstract DF exist. Do nothing")

    def setParams (self,addRelativePosition, addCountVehicles,addTimeSlots,addPosSegment):
        self.__runAddRelativePosition=addRelativePosition
        self.__runAddCountVehicles=addCountVehicles
        self.__runAddTimeSlots=addTimeSlots
        self.__runAddPosSegment=addPosSegment
        
    def __createAbstractDF(self):
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  create df")
        df1=pd.read_csv(filepath_or_buffer=self.__analysis.pathTableMerged,sep=";")
        data=df1[['t', 'id',"dst",'tron','type',"vit","z","FC","CO2_TP","NOx_TP","CO_TP","HC_TP","PM_TP","PN_TP","length"]]
        df2=pd.DataFrame(data)
        self.__analysis.abstractDF=df2
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish create df")
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
                self.__analysis.abstractDF["ns-"+"{:0>4}".format(split)]= self.__analysis.abstractDF["dst_rel"]*int(split)                    # print (self.__analysis.abstractDF)
                # self.__analysis.abstractDF["ns-"+"{:0>4}".format(split)]=self.__analysis.abstractDF["ns-"+"{:0>4}".format(split)].apply(np.floor)
                self.__analysis.abstractDF["ns-"+"{:0>4}".format(split)]=self.__analysis.abstractDF["ns-"+"{:0>4}".format(split)].apply(np.ceil)
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish add position of vehicle in the segment for the split: "+split)

    def __addTimeSlots(self,run):
        if run:
            for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  add time slots")
                self.__analysis.abstractDF["ts-"+"{:0>4}".format(ts)]=self.__analysis.abstractDF["t"]/int (ts)                         # print (self.__analysis.abstractDF)
                self.__analysis.abstractDF["ts-"+"{:0>4}".format(ts)]=self.__analysis.abstractDF["ts-"+"{:0>4}".format(ts)].apply(np.floor)
                self.__analysis.abstractDF["ts-"+"{:0>4}".format(ts)].astype(int)
                # print (self.__analysis.abstractDF["dst_rel"])

            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish add time slots")

    def __checkInfDistRel(self,run):
        if run:
            valReplace=-1
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="replace inf with "+str(valReplace)+" in dst_rel")
            self.__analysis.abstractDF.loc[self.__analysis.abstractDF['dst_rel'] ==np.inf, 'dst_rel'] = valReplace

    def __checkInfPosSegment(self,run):
        if run:
            valReplace=0
            for split in self.__analysis.config.paramAnalysisNumberOfSplit:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="replace inf with "+str(valReplace) +" in pos segment of ns-"+"{:0>4}".format(split))
                self.__analysis.abstractDF.loc[self.__analysis.abstractDF["ns-"+"{:0>4}".format(split)] ==np.inf, "ns-"+"{:0>4}".format(split)] = valReplace

    def __storeAbstractDF(self,storeAbstractDF,df):
        if storeAbstractDF:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  store abstract DF")
            df.to_csv(self.__analysis.pathAbstractDF, header=True,sep=";")
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish store abstract DF")




import os
import sys
import pandas as pd
import numpy as np

class SpatialMeanSpeed():
    def __init__(self,analysis):
        self.analysis=analysis
        self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="initialize spatial mean speed")
        self.__pathOutput=self.analysis.config.pathSpeeds

        self.__pathAbstractDf=self.analysis.pathAbstractDF

    def setPathAbstractDF(self,path):   self.analysis.pathAbstractDF=path
    def setPathOutput(self,pathOutput):   self.__pathOutput=pathOutput



    def compute(self,run):
        if run:
            compute_totTime_splits=True
            compute_totDist_splits=True
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="start compute spatial mean speed")

            # read DF
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="start  read DF")
            self.analysis.abstractDF=pd.read_csv(self.__pathAbstractDf,sep=";")
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="finish read DF")

            # compute total time for split
            self.__compute_totTime_splits(run=compute_totTime_splits)

            # compute total distance for split
            self.__compute_totDist_splits(run=compute_totDist_splits)



            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="finish compute spatial mean speed")


    def __compute_totDist_splits (self,run):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="start compute total distance for splits")


            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="finish compute total distance for splits")

    def __compute_totTime_splits (self,run):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="start compute total time for splits")
            # todo loop for splits and time slots

            # compute total time
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="start compute mean speed")
            for split in self.analysis.config.paramAnalysisNumberOfSplit:
                for ts in self.analysis.config.paramAnalysisListTimeSlot:
                    self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="start compute total time for splits for ts: {} and split: {}".format(ts,split))

                    # groupby
                    df1=self.analysis.abstractDF.groupby(["ns-{:0>4}".format(split),"ts-{:0>4}".format(ts)]).count()

                    # resetIndex
                    df1=df1.reset_index()

                    # add column
                    df1["tot_t"]=df1["t"]

                    # get usefully data
                    df1=df1[["ns-{:0>4}".format(split),"ts-{:0>4}".format(ts),"tot_t"]]

                    # store
                    path_store=self.analysis.config.folder_output+self.analysis.config.scenario+"_totTime_ns-{:0>4}".format(split)+"_"+"ts-{:0>4}".format(ts)+".csv"
                    self.analysis.logger.log(cl=self,method=sys._getframe(),message="start  to store file: "+path_store)
                    df1.to_csv(path_store,sep=";")
                    self.analysis.logger.log(cl=self,method=sys._getframe(),message="finish to store file: "+path_store)

                    self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="finish compute total time for splits")



import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class PollutantDistribution():
    def __init__(self,analysis):
        self.analysis=analysis
        self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="initialize pollutant distribution")
        self.pathAbstractDf=self.analysis.config.pathAbstractDF

    def setPathAbstractDF(self,path):   self.analysis.pathAbstractDF=path

    def setPathOutputJpg(self,path):    self.pathOutputJpg=path


    def getChart(self,run,ts,lms,indicator,saveJpg):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get chart")
            #pathSumPollutants=self.analysis.config.folder_output+self.analysis.config.scenario+'_ts-'+'{:0>4}'.format(ts)+'_lms-'+'{:0>4}'.format(lms)+'_gl.csv'
            pathAbstractDf=self.pathAbstractDf
#            df1=pd.read_csv(pathSumPollutants,sep=";")
            df1=pd.read_csv(self.pathAbstractDf,sep=";")

            x=df1["dst_rel"]
            y=df1[indicator]
            # plt.scatter(x,y)
            # plt.hist(y)
            plt.bar(x,y)
            plt.show()
            if saveJpg:        plt.savefig(self.pathOutputJpg)


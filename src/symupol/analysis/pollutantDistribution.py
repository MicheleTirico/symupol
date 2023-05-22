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

    def setListTimeSplot(self,listTs):      self.analysis.config.paramAnalysisListTimeSlot=listTs
    def setListSplit(self,listSplit):       self.analysis.config.paramAnalysisNumberOfSplit=listSplit

    def setPathAbstractDF(self,path):   self.analysis.pathAbstractDF=path

    def setPathOutputJpg(self,path):    self.pathOutputJpg=path

    def compute(self,run):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="start compute")
            # if listSplit==None: listSplit=self.analysis.config.paramAnalysisListTimeSlot
            # if listTs==None:    listTs=self.analysis.config.paramAnalysisListTimeSlot
            for split in self.analysis.config.paramAnalysisNumberOfSplit:
                for ts in self.analysis.config.paramAnalysisListTimeSlot:
                    self.df_sumPerSplit=pd.read_csv(self.analysis.config.folder_output+self.analysis.config.scenario+"_sumPerSplit_ns-{:0>4}".format(split)+"_"+"ts-{:0>4}".format(ts)+".csv",sep=";")
                    # print (self.df_sumPerSplit)
                    self.df_groupby_ns=self.df_sumPerSplit.groupby(["ns-{:0>4}".format(split),"ts-{:0>4}".format(ts)]).sum()

                    # remove multiindex
                    self.df_groupby_ns=self.df_groupby_ns.reset_index(level=[0,1])

                    list_save=  ['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP','PN_TP', 'nVec',"ns-{:0>4}".format(split),"ts-{:0>4}".format(ts)]
                    self.df_groupby_ns=self.df_groupby_ns[list_save]

                    path_store=self.analysis.config.folder_output+self.analysis.config.scenario+"_groupby_"+"ns-{:0>4}".format(split)+"_ts-{:0>4}".format(ts)+".csv"
                    self.analysis.logger.log(cl=self,method=sys._getframe(),message="start  to store file: "+path_store)
                    self.df_groupby_ns.to_csv(path_store,sep=";")
                    self.analysis.logger.log(cl=self,method=sys._getframe(),message="finish to store file: "+path_store)

    def getSingleDistr_multiTs(self,run,ts,ns,list_ts_chart,indicator,saveJpg):

        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get single distribution at different timeslot. Params ts: {0}, ns: {1}, indicator: {2}, and ns_chart: {3}  ".format(str(ts),str(ns),indicator,list_ts_chart))

            path_groupby=self.analysis.config.folder_output+self.analysis.config.scenario+"_groupby_"+"ns-{:0>4}".format(ns)+"_ts-{:0>4}".format(ts)+".csv"
            # print (path_groupby,os.path.exists(path_groupby))
            #
            df1=pd.read_csv(path_groupby,sep=";")
            print (df1)
            y=df1["ts-{:0>4}".format(ts)]
            x=df1["ns-{:0>4}".format(ns)]
            print (x,y)
            df1_y1=df1[df1["ts-{:0>4}".format(ts)]==float(0)]
            print (df1_y1)
            # y2=df1[df1["ts-{:0>4}".format(ts)]==list_ts_chart[1]]
            #
            # indicator="NOx_TP"
            #
            # print (len(x),len(y1),len(y2))
            # df2=pd.DataFrame({"x":x,"y1":y1,"y2":y2})
            #
            # y=df1[indicator]
            #
            # # print (x)
            # print (y)
            #
            # plt.scatter(x,y)
            # plt.bar(x,[df1_01[indicator],df1_02[indicator]])
            # plt.show()


    def getChart(self,run,ts_chart,lms,indicator,saveJpg):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get chart")
            for split in self.analysis.config.paramAnalysisNumberOfSplit:
                for ts in self.analysis.config.paramAnalysisListTimeSlot:
                    path_groupby=self.analysis.config.folder_output+self.analysis.config.scenario+"_groupby_"+"ns-{:0>4}".format(split)+"_ts-{:0>4}".format(ts)+".csv"
                    df1=pd.read_csv(path_groupby,sep=";")
                    df1=df1[df1["ts-{:0>4}".format(ts)]==ts_chart]
                    x=df1["ns-{:0>4}".format(split)]
                    y=df1[indicator]

                    # plt.scatter(x,y)
                    plt.bar(x,y)
                    # plt.show()
                    pathJpg=self.analysis.config.folder_output+"/charts/"+self.analysis.config.scenario+"_ns-{:0>4}".format(split)+"_ts-{:0>4}".format(ts)+"_"+indicator+"_ts_chart-{:0>4}".format(ts_chart)
                    if saveJpg:        plt.savefig(pathJpg)


    def gestSingleBar (self,run,ts,ns,ts_chart,indicator,saveJpg):

        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get single bar for ts: {}, ns: {}, indicator: {}, and ns_chart: {}  ".format(ts,ns,ts_chart,indicator))

            path_groupby=self.analysis.config.folder_output+self.analysis.config.scenario+"_groupby_"+"ns-{:0>4}".format(ns)+"_ts-{:0>4}".format(ts)+".csv"

            df1=pd.read_csv(path_groupby,sep=";")
            # df1=df1[df1["ts-{:0>4}".format(ts)]==ts_chart]
            x=df1["ns-{:0>4}".format(ns)]
            indicator="NOx_TP"
            y=df1[indicator]

            plt.bar(x,y)
            plt.show()

            if saveJpg:
                pathJpg=self.analysis.config.folder_output+"/charts/"+self.analysis.config.scenario+"_ns-{:0>4}".format(ns)+"_ts-{:0>4}".format(ts)+"_"+indicator+"_ts_chart-{:0>4}".format(ts_chart)+".jpg"
                self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="figure stored at: "+pathJpg)
                plt.savefig(pathJpg)



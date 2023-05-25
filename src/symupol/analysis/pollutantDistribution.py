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

        self.__Pollutants=['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP']
        self.__PollutantsPrint=['Fuel consumption', 'CO_2', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP']
        self.__PollutantsMeasure=["g/h","g/h","g/h","g/h","g/h","g/h","g/h"]
    def __getIndicator(self,indicator_pos):         
        return  self.__Pollutants[indicator_pos],\
                self.__PollutantsPrint[indicator_pos],\
                self.__PollutantsMeasure[indicator_pos]

    def setTimeRange(self,timeRange):   self.__timeRange=timeRange

    def __get_seconds(self,time_str):
        hh, mm, ss = time_str.split(':')
        return int(hh) * 3600 + int(mm) * 60 + int(ss)

    def setListTimeSplot(self,listTs):      self.analysis.config.paramAnalysisListTimeSlot=listTs
    def setListSplit(self,listSplit):       self.analysis.config.paramAnalysisNumberOfSplit=listSplit

    def setPathAbstractDF(self,path):   self.analysis.pathAbstractDF=path

    def setPathOutputJpg(self,path):    self.pathOutputJpg=path

    def compute(self,run):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="start compute")
            for split in self.analysis.config.paramAnalysisNumberOfSplit:
                for ts in self.analysis.config.paramAnalysisListTimeSlot:
                    self.df_sumPerSplit=pd.read_csv(self.analysis.config.folder_output+self.analysis.config.scenario+"_sumPerSplit_ns-{:0>4}".format(split)+"_"+"ts-{:0>4}".format(ts)+".csv",sep=";")
                    self.df_groupby_ns=self.df_sumPerSplit.groupby(["ns-{:0>4}".format(split),"ts-{:0>4}".format(ts)]).sum()

                    # remove multiindex
                    self.df_groupby_ns=self.df_groupby_ns.reset_index(level=[0,1])

                    list_save=  ['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP','PN_TP', 'nVec',"ns-{:0>4}".format(split),"ts-{:0>4}".format(ts)]
                    self.df_groupby_ns=self.df_groupby_ns[list_save]

                    path_store=self.analysis.config.folder_output+self.analysis.config.scenario+"_groupby_"+"ns-{:0>4}".format(split)+"_ts-{:0>4}".format(ts)+".csv"
                    self.analysis.logger.log(cl=self,method=sys._getframe(),message="start  to store file: "+path_store)
                    self.df_groupby_ns.to_csv(path_store,sep=";")
                    self.analysis.logger.log(cl=self,method=sys._getframe(),message="finish to store file: "+path_store)

    def getDistributionPollutantsPerSplit(self,run,ts,ns,list_ts_chart,indicator_pos,show,saveJpg,pathJpg):

        if run:
            indicator_name,indicator_print,indicator_measure=self.__getIndicator(indicator_pos)
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get single distribution of pollutant at different timeslot. Params ts: {0}, ns: {1}, indicator: {2}, and ns_chart: {3}  ".format(str(ts),str(ns),indicator_name,list_ts_chart))
            path_groupby=self.analysis.config.folder_output+self.analysis.config.scenario+"_groupby_"+"ns-{:0>4}".format(ns)+"_ts-{:0>4}".format(ts)+".csv"
            df1=pd.read_csv(path_groupby,sep=";")
            sumLinks,sumInt=0,0
            fig, ax = plt.subplots()
            test,i=1,0
            while test==1 and i< len(list_ts_chart):
                df2=df1[df1["ts-{:0>4}".format(ts)]==list_ts_chart[i]]
                x=df2["ns-{:0>4}".format(ns)]
                y=df2[indicator_name]
                ax.set_xticks(x)

                if len(x)!=0:
                    sumLinks,sumInt=sumLinks+sum(list(y)[1:]),sumInt+list(y)[0]
                    self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="add line for ts-"+str(list_ts_chart[i]))
                    ax.plot(x,y,label="ts-"+str(list_ts_chart[i]+1))
                else:test=self.analysis.config.logger.warning(cl=self,method=sys._getframe(),message="Line ts-"+str(list_ts_chart[i])+" has not been added. Ts out of range",doQuit=False,doReturn=True)
                i+=1

            ax.legend(loc="upper center",fontsize="10")
            plt.title("Pollutant: {}, time slots: {}, n. of splits: {}".format(indicator_print,ts,ns))
            plt.xlabel("splits")
            x_ticks_labels=["crossroads"]+[str(_) for _ in range(1,ns+1,1)]
            ax.set_xticklabels(x_ticks_labels, fontsize=10)
            plt.ylabel("{} emission [{}]".format(indicator_print,indicator_measure))

            # text="sum intersection={0:.2f} ({2:.2f}%)\nsum links={1:.2f} ({3:.2f}%)".format(sumInt,sumLinks,sumInt/(sumLinks+sumInt),sumLinks/(sumLinks+sumInt))            # ax.text(x=1,y=ax.get_ylim()[1]-ax.get_ylim()[1]/10,fontsize=10,s=text)
            if show:    plt.show()
            self.analysis.saveJpg(saveJpg=saveJpg,pathJpg=pathJpg,fig=fig)


    def getBoxPlotPerSplit(self,run,ts,ns,list_ts_chart,indicator_pos,show,saveJpg,pathJpg):
        if run:
            indicator_name,indicator_print,indicator_measure=self.__getIndicator(indicator_pos)
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get box plot per split at different timeslot. Params ts: {0}, ns: {1}, indicator: {2}, and ns_chart: {3}  ".format(str(ts),str(ns),indicator_name,list_ts_chart))












    # TEST -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
                    # plt.shw()
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



    def getScatterPlot (self,run,ts,list_ts_chart,indicator,show,saveJpg,pathJpg):

        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get scatter plot. Params ts: {}, indicator: {}, and ns_chart: {}  ".format(str(ts),indicator,list_ts_chart))
            df1=pd.read_csv(self.pathAbstractDf,sep=";")
            fig, ax = plt.subplots()
            test,i=1,0
            while test==1 and i< len(list_ts_chart):
                df2=df1[df1["ts-{:0>4}".format(ts)]==list_ts_chart[i]]
                x=df2["dst_rel"]
                y=df2[indicator]
                if len(x)!=0:
                    self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="add points for ts-"+str(list_ts_chart[i]))
                    ax.scatter(x,y,label="ts-"+str(list_ts_chart[i]), s=2)
                    legend=ax.legend(loc="upper right",fontsize="10")
                else:
                    test=self.analysis.config.logger.warning(cl=self,method=sys._getframe(),message="Line ts-"+str(list_ts_chart[i])+" has not been added. Ts out of range",doQuit=False,doReturn=True)
                i+=1

            plt.xlim(0,1)
            # plt.ylim()
            if show:    plt.show()
            self.analysis.saveJpg(saveJpg=saveJpg,pathJpg=pathJpg)
        # plt.scatter()

    def getScatterPlot_diagonal (self,run,ts,ns,list_ts_chart,indicator,show,saveJpg,pathJpg):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get scatter plot diagonal. Params ts: {}, indicator: {}, and ns_chart: {}  ".format(str(ts),indicator,list_ts_chart))
            path_groupby=self.analysis.config.folder_output+self.analysis.config.scenario+"_groupby_"+"ns-{:0>4}".format(ns)+"_ts-{:0>4}".format(ts)+".csv"
            df1=pd.read_csv(path_groupby,sep=";")
            fig, ax = plt.subplots()
            test,i=1,0
            print(df1)
            x=df1[df1["ts-{:0>4}".format(ts)]==list_ts_chart[0]][indicator]
            y=df1[df1["ts-{:0>4}".format(ts)]==list_ts_chart[1]][indicator]
            print (x.describe())

            ax.scatter(x,y,label="ts-"+str(list_ts_chart[i]), s=20)
            ax.plot(transform=ax.transAxes)
            ax.axline([ax.get_xlim()[0], ax.get_ylim()[0]], [ax.get_xlim()[1], ax.get_ylim()[1]])
            legend=ax.legend(loc="upper right",fontsize="10")

            if show:    plt.show()
            self.analysis.saveJpg(saveJpg=saveJpg,pathJpg=pathJpg)
        # plt.scatter()

    def getBoxPlot (self,run,ts,list_ts_chart,indicator,show,saveJpg,pathJpg):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get box plot. Params ts: {}, indicator: {}, and ns_chart: {}  ".format(str(ts),indicator,list_ts_chart))
            df1=pd.read_csv(self.pathAbstractDf,sep=";")
            data =[]
            test,i=1,0
            while test==1 and i< len(list_ts_chart):
                df2=df1[df1["ts-{:0>4}".format(ts)]==list_ts_chart[i]]
                df2=df2[df2["dst_rel"]>=0]
                x=df2[indicator]                            # print (df2["FC"].describe())                # plt.hist(df2[indicator])                # plt.show()
                if len(x)!=0:
                    self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="add values for ts-"+str(list_ts_chart[i]))
                    data.append(x)
                else:   test=self.analysis.config.logger.warning(cl=self,method=sys._getframe(),message="Line ts-"+str(list_ts_chart[i])+" has not been added. Ts out of range",doQuit=False,doReturn=True)
                i+=1
            plt.boxplot(data)

            if show:    plt.show()
            self.analysis.saveJpg(saveJpg=saveJpg,pathJpg=pathJpg)



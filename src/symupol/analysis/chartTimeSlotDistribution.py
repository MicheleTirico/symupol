import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random as rd
import seaborn as sns

class ChartTimeSlotDistribution():
    def __init__(self,analysis):
        self.analysis=analysis
        self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="initialize chart time slot")
        self.pathAbstractDf=self.analysis.config.pathAbstractDF

    def setTimeSplot(self,ts):      self.__ts=ts
    def setNumberSplit(self,ns):       self.__ns=ns

    def setPathAbstractDF(self,path):   self.analysis.pathAbstractDF=path

    def setPathOutputJpg(self,path):    self.pathOutputJpg=path

    def readGroupBy(self,run):
        if run:
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="read groupby df")
            path_groupby=self.analysis.config.folder_output+self.analysis.config.scenario+"_groupby_ts-{:0>4}".format(self.__ts)+".csv"
            try:
                assert os.path.exists(path_groupby)==True
                self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="path: {} founded. Do nothing".format(path_groupby))
            except AssertionError:
                self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="path: {} not founded. compute groupby".format(path_groupby))
                self.analysis.computeGroupbyTimeSlot(run=True,ts=self.__ts)

            self.__dfGroupby=pd.read_csv(path_groupby,sep=";")

    def getChartTimeSlot_distribution(self,run,show,indicator_pos,pathJpg):
        if run:
            indicator_name,indicator_print,indicator_measure,indicator_complete_print=self.analysis.getIndicator(indicator_pos)
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get distribution of indicators for time split. Params ts: {}, indicator: {}".format(str(self.__ts),indicator_name))

            df2=self.__dfGroupby
            x=df2["ts-{:0>4}".format(self.__ts)]
            y=df2[indicator_name]

            fig, ax = plt.subplots()
            ax.plot(x,y)
            # ax.legend(loc="upper center",fontsize="10")
            plt.title("{}".format(indicator_complete_print))
            plt.xlabel("time slots: {} s".format(self.__ts))
            # x_ticks_labels=["crossroads"]+[str(_) for _ in range(1,ns+1,1)]
            # ax.set_xticklabels(x_ticks_labels, fontsize=10)
            plt.ylabel("{} [{}]".format(indicator_complete_print,indicator_measure))

            if show:    plt.show()
            self.analysis.saveJpg2(pathJpg=pathJpg,fig=fig)

    def getChartTimeSlot_distribution_normNVec(self,run,show,indicator_pos,pathJpg):
        if run:
            indicator_name,indicator_print,indicator_measure,indicator_complete_print=self.analysis.getIndicator(indicator_pos)
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get distribution of indicators for time split. Params ts: {}, indicator: {}".format(str(self.__ts),indicator_name))

            df2=self.__dfGroupby
            x=df2["ts-{:0>4}".format(self.__ts)]
            y=df2[indicator_name]/df2["nVec"]

            fig, ax = plt.subplots()
            ax.plot(x,y)
            # ax.legend(loc="upper center",fontsize="10")
            plt.title("{} normalized by n. vehicle".format(indicator_complete_print))
            plt.xlabel("time slots: {} s".format(self.__ts))
            # x_ticks_labels=["crossroads"]+[str(_) for _ in range(1,ns+1,1)]
            # ax.set_xticklabels(x_ticks_labels, fontsize=10)
            plt.ylabel("{} [{}]".format(indicator_complete_print,indicator_measure))

            if show:    plt.show()
            self.analysis.saveJpg2(pathJpg=pathJpg,fig=fig)
    
    def getChartTimeSlot_boxPlot(self,run,show,indicator_pos,pathJpg):
        if run:
            indicator_name,indicator_print,indicator_measure,indicator_complete_print=self.analysis.getIndicator(indicator_pos)
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get boxplot of indicators for time split. Params ts: {}, indicator: {}".format(str(self.__ts),indicator_name))

            df2=self.analysis.abstractDF
            x=df2["ts-{:0>4}".format(self.__ts)]
            y=df2[indicator_name]
            box_plot=sns.boxplot(x=x,y=y, color="gray")
            nOfThicks=10

            ticks=range(0,int(max(x))+1,int(  (max(x)+1)/nOfThicks))
            labels=[str(_) for _ in range(0,int(max(x))+1,int(  (max(x)+1)/nOfThicks))]
            box_plot.set_xticks(ticks=ticks, labels=labels)#,fontsize=10)

            plt.title("{} boxplot".format(indicator_complete_print))
            plt.ylabel("{} [{}]".format(indicator_complete_print,indicator_measure))
            plt.xlabel("time slots: {} s".format(self.__ts))
            if show:    plt.show()
            self.analysis.saveJpg2(pathJpg=pathJpg,fig=box_plot.get_figure())

    def getChartTimeSlot_violin(self,run,show,indicator_pos,pathJpg):
        if run:
            indicator_name,indicator_print,indicator_measure,indicator_complete_print=self.analysis.getIndicator(indicator_pos)
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get boxplot of indicators for time split. Params ts: {}, indicator: {}".format(str(self.__ts),indicator_name))

            df2=self.analysis.abstractDF
            x=df2["ts-{:0>4}".format(self.__ts)]
            y=df2[indicator_name]
            box_plot=sns.violinplot(x=x,y=y, color="gray")
            nOfThicks=10

            ticks=range(0,int(max(x))+1,int(  (max(x)+1)/nOfThicks))
            labels=[str(_) for _ in range(0,int(max(x))+1,int(  (max(x)+1)/nOfThicks))]
            box_plot.set_xticks(ticks=ticks, labels=labels)#,fontsize=10)

            plt.title("{} boxplot".format(indicator_complete_print))
            plt.ylabel("{} [{}]".format(indicator_complete_print,indicator_measure))
            plt.xlabel("time slots: {} s".format(self.__ts))
            if show:    plt.show()
            self.analysis.saveJpg2(pathJpg=pathJpg,fig=box_plot.get_figure())

    def getChartTimeSlot_catplot(self,run,show,indicator_pos,pathJpg):
        if run:
            indicator_name,indicator_print,indicator_measure,indicator_complete_print=self.analysis.getIndicator(indicator_pos)
            self.analysis.config.logger.log(cl=self,method=sys._getframe(),message="get boxplot of indicators for time split. Params ts: {}, indicator: {}".format(str(self.__ts),indicator_name))

            df2=self.analysis.abstractDF
            x=df2["ts-{:0>4}".format(self.__ts)]
            y=df2[indicator_name]
            box_plot=sns.catplot(x=x,y=y, color="gray")
            nOfThicks=10

            ticks=range(0,int(max(x))+1,int(  (max(x)+1)/nOfThicks))
            labels=[str(_) for _ in range(0,int(max(x))+1,int(  (max(x)+1)/nOfThicks))]
            # box_plot.set_xticks(ticks=ticks, labels=labels)#,fontsize=10)

            plt.title("{} boxplot".format(indicator_complete_print))
            plt.ylabel("{} [{}]".format(indicator_complete_print,indicator_measure))
            plt.xlabel("time slots: {} s".format(self.__ts))
            if show:    plt.show()
            self.analysis.saveJpg2(pathJpg=pathJpg,fig=box_plot.get_figure())


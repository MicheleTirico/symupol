import os
import sys
import csv
import pandas as pd

class MergeDF:
    def __init__(self,config,run):
        self.__config=config
        self.__run=run
        self.__logger=self.__config.logger

        self.__inputMod=""# TODO from config
        self.__inputCsv=""# TODO from config
        self.__outputCsv=path=""# TODO from config

    def setPathInputMod(self,path):self.__inputMod=path
    def setPathInputCsv(self,path):self.__inputCsv=path
    def setPathOutputCsv(self,path):self.__outputCsv=path

    def mergeDF(self):
        if self.__run:
            self.__logger.log(cl=self,method=sys._getframe(),message="start merge dataframes")
            # TODO add assert exist file 1 and 2

            self.__logger.log(cl=self,method=sys._getframe(),message="start read DF")

            df_phem=pd.read_csv(filepath_or_buffer=self.__inputMod,sep=";")
            df_traj=pd.read_csv(filepath_or_buffer=self.__inputCsv,sep=";") # print (df_phem,df_traj)
            lim=100000000000000000000000000
            df_traj=df_traj[:lim]
            df_phem=df_phem[:lim]

            self.__logger.log(cl=self,method=sys._getframe(),message="start  merge")
            df_merged=pd.merge(df_traj,df_phem,on=['t','id'],how="outer")
            self.__logger.log(cl=self,method=sys._getframe(),message="finish merge")

            # print (df3)
            self.__logger.log(cl=self,method=sys._getframe(),message="start  store DF")
            df_merged.to_csv(path_or_buf=self.__outputCsv,sep=";")
            self.__logger.log(cl=self,method=sys._getframe(),message="finish store DF")

            self.__logger.log(cl=self,method=sys._getframe(),message="finish merge dataframes")

    def __getSplitStr(self,input,pos):    return input[pos].split(":")[1].replace(" ","")

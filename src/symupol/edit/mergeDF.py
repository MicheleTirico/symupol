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
            self.__logger.log(cl=self,method=sys._getframe(),message="start merge databases")
            # TODO add assert exist file 1 and 2

            print ("start to read")
            df_phem=pd.read_csv(filepath_or_buffer=self.__inputMod,sep=";")
            df_traj=pd.read_csv(filepath_or_buffer=self.__inputCsv,sep=";")
            print (df_phem,df_traj)
            # df_phem.set_index("id")

            # df_traj.set_index("id")
            lim=100000000000000000000000000
            df_traj=df_traj[:lim]
            df_phem=df_phem[:lim]

            print ("start to merge")

            df3=pd.merge(df_traj,df_phem,on=['id',"t"],how="outer")
            print ("finish to merge")

            print (df3)
            print ("start to store")
            df3.to_csv(path_or_buf=self.__outputCsv,sep=";")

            # df_concat=pd.concat([df_phem,df_traj])
            # print (df_concat)

            # df_merged=pd.merge(df_phem,df_traj,on="id",how="inner")
            # print(df_merged)
            # pd.df_merged.to_csv(path_or_buf=self.__outputCsv,sep=";")

            self.__logger.log(cl=self,method=sys._getframe(),message="finish merge databases")



    def __getSplitStr(self,input,pos):    return input[pos].split(":")[1].replace(" ","")

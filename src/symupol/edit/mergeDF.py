import csv
import os
import sys
import pandas as pd

class MergeDF:
    def __init__(self,config,run):
        self.__config=config
        self.__run=run
        self.__logger=self.__config.logger

        self.__inputMod             =self.__config.getFileExtention(self.__config.folder_output,".mod")[0]# TODO to check
        self.__config.pathOutputMod =self.__inputMod
        self.__inputCsv             =self.__config.pathOutputVehicles
        self.__outputCsv            =self.__config.pathOutputMergedTmp


    def setPathInputMod(self,path):self.__inputMod=path
    def setPathInputCsv(self,path):self.__inputCsv=path
    def setPathOutputCsv(self,path):self.__outputCsv=path

    def mergeDF(self,comuteIfExist,removeLines):
        self.__logger.log(cl=self,method=sys._getframe(),message="start merge dataframes")
        if self.__run:
            if comuteIfExist:
                if os.path.exists(self.__config.pathOutputMergedTmp):  os.system("rm "+self.__config.pathOutputMergedTmp) # remove file if exist

                # TODO add assert exist file 1 and 2
                self.__logger.log(cl=self,method=sys._getframe(),message="start read DF")

                df_phem=pd.read_csv(filepath_or_buffer=self.__inputMod,sep=";")
                df_traj=pd.read_csv(filepath_or_buffer=self.__inputCsv,sep=";")

                self.__logger.log(cl=self,method=sys._getframe(),message="start  merge")
                df_merged=pd.merge(df_traj,df_phem,on=['t','id'],how="outer")
                self.__logger.log(cl=self,method=sys._getframe(),message="finish merge")

                # print (df3)
                self.__logger.log(cl=self,method=sys._getframe(),message="start  store DF")
                df_merged.to_csv(path_or_buf=self.__outputCsv,sep=";")
                self.__logger.log(cl=self,method=sys._getframe(),message="finish store DF")

                self.__logger.log(cl=self,method=sys._getframe(),message="finish merge dataframes")
            else:
                self.__logger.log(cl=self,method=sys._getframe(),message="file exist. We do not compute merge")
        print (self.__outputCsv)
        self.__removeNotCompleteLines(removeLines)
        self.__logger.log(cl=self,method=sys._getframe(),message="finish merge dataframes")

    def __removeNotCompleteLines(self,run):
        if run:
            self.__logger.log(cl=self,method=sys._getframe(),message="start remove uncompleted lines")
            if os.path.exists(self.__config.pathOutputMerged):  os.system("rm "+self.__config.pathOutputMerged) # remove file if exist
            i,stopCondition=0,-100
            with open(self.__config.pathOutputMerged, "a") as f:
                with open(self.__config.pathOutputMergedTmp, "r") as f_tmp:
                    reader=csv.reader(f_tmp)
                    for row in reader:
                        genVal=row[0].split(";")[-1]
                        if genVal=="gen"or genVal!="":
                            f.write(row[0]+"\n")#                            print (len(row[0].split(";")))
                        i+=1
                        if i==stopCondition:break
        else:
            self.__logger.log(cl=self,method=sys._getframe(),message="We do not remove uncompleted lines. We copy the "+self.__config.pathOutputMergedTmp +" file to "+self.__config.pathOutputMerged)
            os.system("cp "+self.__config.pathOutputMergedTmp+" "+self.__config.pathOutputMerged)


    def __getSplitStr(self,input,pos):    return input[pos].split(":")[1].replace(" ","")

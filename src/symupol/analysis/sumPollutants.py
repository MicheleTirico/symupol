import os
import sys
import pandas as pd
import numpy as np

class SumPollutants():
    def __init__(self,analysis):
        self.__analysis=analysis

        self.__analysis.config.logger.log(cl=self,method=sys._getframe(),message="initialize sum pollutants")
        self.__pathInitOutput=self.__analysis.config.folder_output+self.__analysis.config.getNameScenario()
        self.__pathsOfOutputs_nSplit=[]
        self.__pathsOfOutputs_maxLenSplit=[]

        self.__list_files=[]

    def setPathAbstractDF(self,path):   self.__analysis.pathAbstractDF=path

    def setPathInitOutput(self,initOutput):   self.__pathInitOutput=initOutput

    def computeSumPerSplitCost(self,run):
        if run:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  compute sum split cost")

            for split in self.__analysis.config.paramAnalysisNumberOfSplit:
                for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                    path_store=self.__analysis.config.folder_output+self.__analysis.config.scenario+"_sumPerSplit_ns-{:0>4}".format(split)+"_"+"ts-{:0>4}".format(ts)+".csv"
                    self.__analysis.controller.removeIfExist(path_store)
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  compute sum split cost for ns: "+str(split))
                    df_abstract=pd.read_csv(filepath_or_buffer=self.__analysis.config.pathAbstractDF,sep=";")

                    split=int(split)
                    # df_abstract["ns-{:0>4}".format(split)]=df_abstract["dst_rel"]//(1/split)+1
                    df_abstract.loc[df_abstract["dst_rel"] > 1.0 , "dst_rel"] = 0.99999999999999999                # df_abstract["ns-{:0>4}".format(split)].astype(int)
                    df_abstract["ns-{:0>4}".format(split)]=df_abstract["dst_rel"]*split+1
                    df_abstract.loc[df_abstract["ns-{:0>4}".format(split)] >split,"ns-{:0>4}".format(split)] = split
                    df_abstract["ns-{:0>4}".format(split)]=df_abstract["ns-{:0>4}".format(split)].apply(np.floor)
                    df_abstract.loc[df_abstract["ns-{:0>4}".format(split)] == "inf","ns-{:0>4}".format(split)] = 0
                    df_abstract.loc[df_abstract["ns-{:0>4}".format(split)] < 0 , "ns-{:0>4}".format(split)] = 0
                    df_abstract.loc[df_abstract["ns-{:0>4}".format(split)] == np.inf , "ns-{:0>4}".format(split)] = 0                # df_abstract["ns-{:0>4}".format(split)].astype(int)
                    df_abstract["id_link_ns-{:0>4}".format(split)]=df_abstract["tron"]+"_"+df_abstract["ns-{:0>4}".format(split)].astype(str)

                    # groupby sum dataframe
                    df_abstract=df_abstract.groupby(["id_link_ns-{:0>4}".format(split),"ns-{:0>4}".format(split),"ts-{:0>4}".format(ts)]).sum()

                    # remove multiindex
                    df_abstract=df_abstract.reset_index(level=[0,1,2])
                    # print (df_abstract)
                    list_save=  ['FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP','PN_TP', 'nVec']+ \
                                ["ts-{:0>4}".format(_) for _ in self.__analysis.config.paramAnalysisListTimeSlot]+ \
                                ["ns-{:0>4}".format(split)]+ \
                                ["ts-{:0>4}".format(ts)]+ \
                                ["id_link_ns-{:0>4}".format(split),
                                 "dst"]

                    df_abstract=df_abstract[list_save]

                    # store
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  to store file: "+path_store)
                    df_abstract.to_csv(path_store,sep=";")
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish to store file: "+path_store)

            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish compute sum split cost")


    def computeNsplitCost(self,run,compute_df_spi, compute_df):
        if run:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants")

            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  compute sum per instant of pollutants ")
            if compute_df_spi==True:
                df_abstract=pd.read_csv(filepath_or_buffer=self.__analysis.config.pathAbstractDF,sep=";")
                pathTimeStep=self.__analysis.config.folder_output+self.__analysis.config.scenario+"_sumPerInstant.csv"
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="df_sumPerInstant does not exist. Compute now")
                df_sumPerInstant=df_abstract.groupby(["tron","t"],as_index="False").sum() # aggiungi posizione del segmento e hai anche lo spit.
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish compute sum per instant of pollutants ")
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start store df_sumPerInstant")
                df_sumPerInstant.to_csv(pathTimeStep, header=True,sep=";")
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start store df_sumPerInstant")
            else:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="df_sumPerInstant exists. Go through")
            # if listSplit==None: listSplit=self.__analysis.config.paramAnalysisNumberOfSplit

            for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                for split in self.__analysis.config.paramAnalysisNumberOfSplit:
                    path=self.__pathInitOutput+"_ts-"+"{:0>4}".format(ts)+"_ns-"+"{:0>4}".format(split)+".csv"

                    self.__list_files.append(path)
                    if compute_df==True:
                        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants for time slot: "+ts+" and link splitted in: "+str(split))

                        # create df
                        vals=["tron","ts-"+"{:0>4}".format(ts),"ns-"+"{:0>4}".format(split)]
                        df1=df_abstract.groupby(vals).sum()
                        df1=df1[["FC","CO2_TP","NOx_TP","CO_TP","HC_TP","PM_TP","PN_TP"]]
                        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish to create dataframe for time slot: "+ts+" and link splitted in: "+str(split))

                        # store file
                        self.__analysis.controller.removeIfExist(path)
                        df1.to_csv(path,sep=";")
                        self.__pathsOfOutputs_nSplit.append(path)
                        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish to store file: "+path)
                        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish sum pollutants for time slot: "+ts+" and link splitted in: "+str(split))

                        self.__pathsOfOutputs_nSplit.append(path)
                    else:
                        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="not computed sum pollutants for time slot: "+ts+" and link splitted in: "+str(split))

            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish sum pollutants")

    def computeMaxLen(self,run):
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants with max length")
        if run:
            list_save=['t', 'tron','FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP', 'dst_rel','nVec']+["ts-{:0>4}".format(_) for _ in self.__analysis.config.paramAnalysisListTimeSlot]
            df_abstract=pd.read_csv(filepath_or_buffer=self.__analysis.config.pathAbstractDF,sep=";")[list_save]#[['t', 'tron','FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP', 'PN_TP', 'dst_rel','nVec', 'ts-0900', 'ts-1500', 'ts-40000']]
            for lenMaxSp in self.__analysis.config.paramAnalysisLengthMaxSplit:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants with max length of: "+lenMaxSp)

                df1=df_abstract.copy(deep=True)

                # path to store the df after merging
                df2=df_abstract.copy(deep=True)

                # df of links split
                pathCsvLinksSplited=self.__analysis.config.folder_output+self.__analysis.config.scenario+"_link_splitted_lms_{:0>4}.csv".format(lenMaxSp)
                df_split=pd.read_csv(filepath_or_buffer=pathCsvLinksSplited,sep=";")

                # df links
                pathCsvLinks=self.__analysis.config.folder_output+self.__analysis.config.scenario+"_links.csv".format(lenMaxSp)
                df_links=pd.read_csv(filepath_or_buffer=pathCsvLinks,sep=";")

                # merge df
                list_save=  ['t', 'tron', 'FC', 'CO2_TP', 'NOx_TP', 'CO_TP', 'HC_TP', 'PM_TP','PN_TP', 'dst_rel', 'nVec','length']+ \
                            ["ts-{:0>4}".format(_) for _ in self.__analysis.config.paramAnalysisListTimeSlot]+ \
                            ["n_split_{:0>4}".format(_) for _ in self.__analysis.config.paramAnalysisNumberOfSplit]+ \
                            ["length_split_{:0>4}".format(_) for _ in self.__analysis.config.paramAnalysisNumberOfSplit]

                df_m1=pd.merge(df2,df_links,left_on="tron",right_on="id",how="outer")#[list_save]

                # get position of vehicle in the split
                df_m1['pos_{:0>4}'.format(lenMaxSp)]=df_m1['dst_rel']//(1/df_m1['n_split_{:0>4}'.format(lenMaxSp)])+1

                # get sum by split
                df_m1.groupby(["tron","pos_{:0>4}".format(lenMaxSp)],as_index="False").sum()

                # get pos in time split
                df_m1['ts_{:0>4}'.format(lenMaxSp)]=df_m1['dst_rel']//(1/df_m1['n_split_{:0>4}'.format(lenMaxSp)])+1
                for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants with max length of: "+lenMaxSp+ " and time split of: "+ts)

                    pathStore=self.__pathInitOutput+'_ts-'+'{:0>4}'.format(ts)+'_lms-'+'{:0>4}'.format(lenMaxSp)+'.csv'

                    df_m1["pos_ts_{:0>4}".format(ts)]=df_m1["t"]//int(ts)+1
                    df_m2=df_m1.groupby(by=["tron","pos_{:0>4}".format(lenMaxSp),"pos_ts_{:0>4}".format(ts)]).sum()

                    # remove multiindex
                    df_m2=df_m2.reset_index(level=[0,1])

                    # add columns id_split
                    df_m2["id_split_{:0>4}".format(lenMaxSp)]=df_m2["tron"]+"_split-"+df_m2["pos_{:0>4}".format(lenMaxSp)].astype(str)

                    list_save=["tron","t","FC","CO2_TP","NOx_TP","CO_TP","HC_TP","PM_TP","PN_TP","dst_rel","nVec",'pos_{:0>4}'.format(lenMaxSp),'n_split_{:0>4}'.format(lenMaxSp),"id_split_{:0>4}".format(lenMaxSp)]
                    df_m2=df_m2[list_save]

                    #store
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start store: "+pathStore)
                    df_m2.to_csv(pathStore,sep=";")

        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish sum pollutants with max length")


    def addGeometryLinks_ns(self,run):
        if run:
            for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                for ns in self.__analysis.config.paramAnalysisNumberOfSplit:

                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="add geometry of links for time slot: "+ts+" and number of splits of: "+ns)
                    path_sum=self.__pathInitOutput+"_ts-"+"{:0>4}".format(ts)+"_ns-"+"{:0>4}".format(ns)+".csv"
                    df1=pd.read_csv(filepath_or_buffer=path_sum,sep=";")
                    path_split=self.__analysis.config.folder_output+self.__analysis.config.scenario+"_ns_{:0>4}.csv".format(ns)
                    df2=pd.read_csv(filepath_or_buffer=path_split,sep=";")
                    df3=pd.merge(df1,df2,on="id_split",how="outer")
                    pathStore=self.__pathInitOutput+"_ts-"+"{:0>4}".format(ts)+"_ns-"+"{:0>4}_gl".format(ns)+".csv"
                    df3.to_csv(pathStore,sep=";")

    def addGeometryLinks_mls(self,run):
        if run:
            for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                for lenMaxSp in self.__analysis.config.paramAnalysisLengthMaxSplit:
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="add geometry of links for time slot: "+ts+" and max length of split of: "+lenMaxSp)

                    # get df sum pollutants
                    path_sum=self.__pathInitOutput+"_ts-"+"{:0>4}".format(ts)+"_lms-"+"{:0>4}".format(lenMaxSp)+".csv"
                    df1=pd.read_csv(filepath_or_buffer=path_sum,sep=";")

                    # get df split links
                    path_split=self.__analysis.config.folder_output+self.__analysis.config.scenario+"_link_splitted_lms_{:0>4}.csv".format(lenMaxSp)
                    df2=pd.read_csv(filepath_or_buffer=path_split,sep=";")

                    # merge df
                    df3=pd.merge(df1,df2,left_on="id_split_{:0>4}".format(lenMaxSp),right_on="id_split",how="outer")
                    pathStore=self.__pathInitOutput+"_ts-"+"{:0>4}".format(ts)+"_lms-"+"{:0>4}_gl".format(lenMaxSp)+".csv"
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="Path store: "+pathStore)

                    df3.to_csv(pathStore,sep=";")
    def cleanDf(self,run):
        if run:
            for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                for lenMaxSp in self.__analysis.config.paramAnalysisLengthMaxSplit:
                    path=self.__pathInitOutput+'_ts-'+'{:0>4}'.format(ts)+'_lms-'+'{:0>4}'.format(lenMaxSp)+'.csv'
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="clean df: "+path)
                    list_save=["tron","t","FC","CO2_TP","NOx_TP","CO_TP","HC_TP","PM_TP","PN_TP","dst_rel","nVec",'pos_{:0>4}'.format(lenMaxSp),'n_split_{:0>4}'.format(lenMaxSp)]
                    df1=pd.read_csv(path,sep=";")
                    df1=df1[list_save]
                    df1.to_csv(path,sep=";")

    def addIdSplit_mls(self,run):
        if run:
            for ts in self.__analysis.config.paramAnalysisListTimeSlot:
                for lenMaxSp in self.__analysis.config.paramAnalysisLengthMaxSplit:
                    path=self.__pathInitOutput+'_ts-'+'{:0>4}'.format(ts)+'_lms-'+'{:0>4}'.format(lenMaxSp)+'.csv'
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="clean df: "+path)
                    df1=pd.read_csv(path,sep=";")
                    df1["id_split_{:0>4}".format(lenMaxSp)]=df1["tron"]+"_split-"+df1['pos_{:0>4}'.format(lenMaxSp)].astype(str)
                    self.__analysis.logger.log(cl=self,method=sys._getframe(),message="Path store: "+path)
                    df1.to_csv(path,sep=";")

    def addIdSplit_ns(self,run):
        if run:
            self.__analysis.logger.log(cl=self, method=sys._getframe(), message="start  add split link id")
            for path in self.__pathsOfOutputs_nSplit:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="add split link id for table: "+os.path.splitext(path)[0]+os.path.splitext(path)[1])
                listOfSplits=["{:0>4}".format(i) for i in self.__analysis.config.paramAnalysisNumberOfSplit]            # get the right file
                test,pos,pathOk=False,0,""
                while test==False:
                    if "ns-"+listOfSplits[pos] in path:
                        test,pathOk,split=True,path,"ns-"+listOfSplits[pos]
                    pos+=1
                df=pd.read_csv(filepath_or_buffer=pathOk,sep=";")
                df["id_split"]=df["tron"]+"_split-"+df[split].astype(str)
                df.to_csv(pathOk,sep=";")
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish add split link id")
    def __getGroupby(self,vals):
        return self.__analysis.abstractDF.groupby(vals).sum()
    def __setTimeSlots(self,timeSlot):
        df1=self.__analysis.abstractDF.groupby(["tron","t","ts-"+timeSlot]).sum()
        return df1
    def __getSumPerTimeStep(self):
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  compute sum per instant of pollutants ")
        df1=self.__analysis.abstractDF.groupby(["tron","t"],as_index="False").sum() # aggiungi posizione del segmento e hai anche lo spit.
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish compute sum per instant of pollutants ")
        return df1
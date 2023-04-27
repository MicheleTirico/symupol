import os
import sys
import pandas as pd

class SumPollutants():
    def __init__(self,analysis):
        self.__analysis=analysis

        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="initialize sum pollutants")
        self.__pathInitOutput=self.__analysis.config.folder_output+self.__analysis.config.getNameScenario()
        self.__pathsOfOutputs=[]

    def setPathAbstractDF(self,path):   self.__analysis.pathAbstractDF=path

    def setPathInitOutput(self,initOutput):   self.__pathInitOutput=initOutput



    def compute(self):
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants")
        try:                                                                                                            # assert Abstract DF was created
            assert self.__analysis.existAbstractDF==True
        #    print ("--------------------------- abstract df -----------------------------------\n",self.__analysis.abstractDF)
        except AssertionError:
            self.__analysis.config.logger.error(cl=self,method=sys._getframe(),message="Abstract DF not created",error=AssertionError)

        self.__dfPerTimeStep=self.__getSumPerTimeStep()
        pathTimeStep=self.__pathInitOutput+"_sumPerInstant.csv"
        self.__analysis.controller.removeIfExist(path=pathTimeStep)
        self.__dfPerTimeStep.to_csv(pathTimeStep, header=True)

#        print ("--------------------------- df per instant -----------------------------------\n",self.__dfPerTimeStep)

        for ts in self.__analysis.config.paramAnalysisListTimeSlot:
            for split in self.__analysis.config.paramAnalysisNumberOfSplit:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants for time slot: "+ts+" and link splitted in: "+split)

                # create df
                df1=self.__getGroupby(vals=["tron","ts-"+"{:0>4}".format(ts),"ns-"+"{:0>4}".format(split)])
                df1=df1[["FC","CO2_TP","NOx_TP","CO_TP","HC_TP","PM_TP","PN_TP"]]
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish to create dataframe for time slot: "+ts+" and link splitted in: "+split)

                # store file
                path=self.__pathInitOutput+"_ts-"+"{:0>4}".format(ts)+"_ns-"+"{:0>4}".format(split)+".csv"
                self.__analysis.controller.removeIfExist(path)
                df1.to_csv(path,sep=";")
                self.__pathsOfOutputs.append(path)
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish to store file: "+path)
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish sum pollutants for time slot: "+ts+" and link splitted in: "+split)

        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish sum pollutants")

    def addIdSplit(self,run):
        if run:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  add split link id")
            for path in self.__pathsOfOutputs:
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="add split link id for table: "+os.path.splitext(path)[0]+os.path.splitext(path)[1])
                # print (df)
                listOfSplits=["0005","0010"]
                test=False
                pos=0
                pathOk=""
                while test==False:
                    if "ns-"+listOfSplits[pos] in path:
                        test=True
                        pathOk=path
                        split="ns-"+listOfSplits[pos]
                    pos+=1
                print (pathOk,split)
                df=pd.read_csv(filepath_or_buffer=pathOk,sep=";")
                print (df[split])
                # df[split]=2.2
                df["id_split"]=df["tron"]+"_split-"+df[split].astype(str)
                print (df)
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
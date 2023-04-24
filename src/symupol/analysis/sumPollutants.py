import sys
import pandas as pd

class SumPollutants():
    def __init__(self,analysis):
        self.__analysis=analysis

        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="initialize sum pollutants")
        self.__pathInitOutput=self.__analysis.config.folder_output+self.__analysis.config.getNameScenario()

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
                df1=self.__getGroupby(vals=["tron","ts_"+ts,"nSplit_"+split])
                df1=df1[["FC","CO2_TP","NOx_TP","CO_TP","HC_TP","PM_TP","PN_TP"]]
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish to create dataframe for time slot: "+ts+" and link splitted in: "+split)

                # store file
                path=self.__pathInitOutput+"_timeSlot-"+ts+"_splitLink-"+split
                self.__analysis.controller.removeIfExist(path)
                df1.to_csv(path)
                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish to store file: "+path)

                self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants for time slot: "+ts+" and link splitted in: "+split)


        # for timeSlot in self.__analysis.config.paramAnalysisListTimeSlot:
        #     self.__dfPerTimeSlot=self.__setTimeSlots(timeSlot=timeSlot)
        #     print ("--------------------------- df per timeSlot -----------------------------------\n",self.__dfPerTimeSlot)




        # for pollutant in self.__analysis.config.paramAnalysisListPollutants:
        #     for timeSlot in self.__analysis.config.paramAnalysisListTimeSlot:
        #         self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  compute pollutant: "+pollutant +" for the time slot: "+ timeSlot)
        #         df1=self.__getSumTimeSlots(timeSlot=timeSlot,pollutant=pollutant)
        #         self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish compute pollutant: "+pollutant +" for the time slot: "+ timeSlot)

        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish sum pollutants")


    def __getGroupby(self,vals):
        return self.__analysis.abstractDF.groupby(vals).sum()
    def __setTimeSlots(self,timeSlot):
        df1=self.__analysis.abstractDF.groupby(["tron","t","ts_"+timeSlot]).sum()
        return df1
    def __getSumPerTimeStep(self):
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  compute sum per instant of pollutants ")
        df1=self.__analysis.abstractDF.groupby(["tron","t"],as_index="False").sum() # aggiungi posizione del segmento e hai anche lo spit.
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish compute sum per instant of pollutants ")
        return df1
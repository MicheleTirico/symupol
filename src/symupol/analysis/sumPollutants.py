import sys
import pandas as pd

class SumPollutants():
    def __init__(self,analysis):
        self.__analysis=analysis

        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="initialize sum pollutants")

    def setPathAbstractDF(self,path):   self.__analysis.pathAbstractDF=path



    def compute(self):
        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start  sum pollutants")
        try:                                                                                                            # assert Abstract DF was created
            assert self.__analysis.existAbstractDF==True
            print (self.__analysis.abstractDF)
        except AssertionError:
            self.__analysis.config.logger.error(cl=self,method=sys._getframe(),message="Abstract DF not created",error=AssertionError)

        for pollutant in self.__analysis.config.paramAnalysisListPollutants:
            self.__analysis.logger.log(cl=self,method=sys._getframe(),message="start compute pollutant "+pollutant)

            path=self.__analysis.config.folder_output+self.__analysis.config.getNameScenario()+"_"+str(pollutant)+".csv"
            v=self.__analysis.abstractDF.groupby(["tron","t"]).sum() # aggiungi posizione del segmento e hai anche lo spit.
            print (v)
            # ora raggruppa per intervallo di tempo senza il tempo




        self.__analysis.logger.log(cl=self,method=sys._getframe(),message="finish sum pollutants")

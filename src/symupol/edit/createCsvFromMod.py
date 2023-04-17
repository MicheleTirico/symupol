import os
import sys
import csv
import math as mt

class CreateCsvFromMod:
    def __init__(self,config,run):

        self.__config=config
        self.__run=run
        self.__logger=self.__config.logger

        self.__inputMod=""# TODO from config
        self.__outputCsv=""# TODO from config

    def setPathInputMod(self,path):self.__inputMod=path
    def setPathOutputCsv(self,path):self.__outputCsv=path

    def createCsv(self,runIfExist):

        if self.__run:
            self.__logger.log(cl=self,method=sys._getframe(),message="start create the .csv file from the .mod file")
            if runIfExist:
                self.__logger.log(cl=self,method=sys._getframe(),message="remove the existing file and compute it")
                if os.path.exists(self.__outputCsv):  os.system("rm "+self.__outputCsv) # remove file if exist
                with open (self.__inputMod, "r") as f_input:
                    with open (self.__outputCsv, "w") as f_output:
                        keys=["id","gen","t"]
                        dim=["[-]","[-]","[-]"]
                        reader_input=csv.reader(f_input)
                        writer_output=csv.writer(f_output,delimiter=";")
                        fileInfo=[]                                                                                         # remove early lines
                        for i in range (5):fileInfo.append(next(f_input))
                        id=0#                        idInt=0
                        exportFirstHeader=False
                        for line in reader_input:
                            if "VehNr" in line[0]:
                                id=str(self.__getSplitStr(line,0))                          #id=str(idInt)    idInt+=1
                                gen=str(self.__getSplitStr(line,1))
                            elif line[0]!="time" and line[0]!="[s]":                                # t=int(round(float(line[0])))
                                t=float(mt.floor(float(line[0])))
                                line+=[id,gen,t]
                                writer_output.writerow(line)
                            elif exportFirstHeader==False:
                                if line[0]=="time" :
                                    writer_output.writerow(line+keys)
                                    exportFirstHeader=True

    #                        elif line[0]=="[s]"  :       writer_output.writerow(line+dim)
            else:
                self.__logger.log(cl=self,method=sys._getframe(),message="file was not remove and nothing was computed")





            self.__logger.log(cl=self,method=sys._getframe(),message="finish create the .csv file from the .mod file")
    def __getSplitStr(self,input,pos):    return input[pos].split(":")[1].replace(" ","")

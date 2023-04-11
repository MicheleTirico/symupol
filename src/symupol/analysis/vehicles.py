import os
import sys
import xml.etree.ElementTree as ET
import csv

class Vehicles:
    def __init__(self,config,run):
        self.__config=config
        self.__run=run
        self.__logger=self.__config.logger
        self.__vehicles=None
        self.__logger.log(cl=self,method=sys._getframe(),message="init vehicles")

    def setPathOutputPhem(self,path):       self.__config.outputPhemMod=path

    def setPathFzp(self,path):    self.__config.pathFzp=path

    def addTripVehiclesFromFzp(self):
        self.__logger.log(cl=self,method=sys._getframe(),message="start  set path of vehicles")
        with open(self.__config.pathOutputVehicles, "r") as f:
            stop,i=10,0
            reader=csv.reader(f)
            header=next(reader)[0].split(";") # ['t', 'abs', 'acc', 'dst', 'id', 'ord', 'tron', 'type', 'vit', 'voie', 'z']
            for row in reader:
                print (row)
                id=self.__getVal(row,header,"id")[0]
                i+=1
                if i==stop:break
        self.__logger.log(cl=self,method=sys._getframe(),message="finish set path of vehicles")

    def __getVal(self,row,header,name):

        line=row[0].split(";")
        i=header.index(name)

        return line[i]
    def createVehicles(self):
        self.__logger.log(cl=self,method=sys._getframe(),message="start  create vehicles")
        # create vehicles
        if os.path.exists(self.__config.pathDictVehiclesPhem):
            self.__logger.log(cl=self,method=sys._getframe(),message="file: "+self.__config.pathDictVehiclesPhem+" founded. Read the dict")
            self.__vehicles=self.__config.tools.readDictionaryAsFile(self.__config.pathDictVehiclesPhem)
        else:
            self.__logger.log(cl=self,method=sys._getframe(),message="file: "+self.__config.pathDictVehiclesPhem+" not founded. Create objects vehicles")
            self.__vehicles=self.__getVehicles()        #            for id, vehicle in self.__vehicles.items():
            try:
                assert len(self.__vehicles)!=0
                self.__config.tools.saveDictionaryAsFile(dict=self.__vehicles,pathOutput=self.__config.pathDictVehiclesPhem)
            except AssertionError:  self.__logger.warning(cl=self,method=sys._getframe(),message="len of dictionary is 0",doQuit=False,doReturn=False)
        self.__logger.log(cl=self,method=sys._getframe(),message="finish create vehicles")

        print (self.__vehicles[1].getMapVals())

    def __getVehicles (self):
        self.__logger.log(cl=self,method=sys._getframe(),message="start create objects.")

        vehicles={}
        with open (self.__config.outputPhemMod, "r") as f:
            reader=csv.reader(f)
            fileInfo=[]                                                                                                 # remove early lines
            for i in range (5):fileInfo.append(next(f))
            stopCondition=-10                                                                                            # stop condition for test
            previousStep=None                                                                                           # to find first time
            for line in reader:
                if "VehNr" in line[0]:
                    id=int(self.__getSplitStr(line,0))
                    vehicle=Vehicle(id=None)                                                                            # create vehicle
                    vehicle.setId(id)
                    vehicle.setGenFile(self.__getSplitStr(line,1))
                elif line[0]!="time" and line[0]!="[s]":
                    map={}                                                                                              # create and set map of values
                    for i in range(len(line)):map[str(keys[i])]=line[i]
                    vehicle.setMapVals(map)
                    vehicle.incLenTime()                                                                                # set increment of time
                    if previousStep[0]=="[s]": vehicle.setInitTime(line[0])                                             # set init time
                elif line[0]=="time" : keys=line
                elif line[0]=="[s]"  : dim=line

                if int(id)==stopCondition:break
                vehicles[id]=vehicle
                previousStep=line

        self.__keys,self.__dim=keys,dim

        self.__logger.log(cl=self,method=sys._getframe(),message="finish create objects.")
        return vehicles

    def __getSplitStr(self,input,pos):    return input[pos].split(":")[1].replace(" ","")

class Vehicle:
    def __init__(self,id):
        self.__id=id
        self.__time=[]
        self.__lenTime=0
        self.__initTime=None
        self.__genFile=None
        self.__mapVals=None

    def setMapVals(self,map):           self.__mapVals=map

    def getMapVals(self):                   return self.__mapVals
    def setGenFile(self,genFile):   self.__genFile=genFile
    def setId(self,id): self.__id=id

    def incLenTime(self):   self.__lenTime+=1

    def getIncLenTime(self):    return self.__lenTime
    def setTime(self,t):self.__time.append(t)

    def getTime(self):  return self.__time
    def getId(self):    return self.__id
    def setInitTime(self,initTime):  self.__initTime=float(initTime)
    def getMaxTime(self):   return self.__initTime+self.__lenTime
    def getInitTime(self):   return self.__initTime
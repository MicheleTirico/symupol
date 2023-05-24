import sys
import os
import csv
import pickle


from symupol.control.logger import Logger

class Tools:
    def __init__(self,config):
        self.__config=config
        self.logger=self.__config.logger

    def saveDictionaryAsCsv(self,dict,pathOutput):
        self.logger.log(cl=self,method=sys._getframe(),message="start store dict")
        with open(pathOutput, "w", newline="") as fp:        # Open a csv file for writing
            writer = csv.DictWriter(fp, fieldnames=dict.keys())            # Create a writer object
            writer.writeheader()            # Write the header row
            writer.writerow(dict)            # Write the data rows
        self.logger.log(cl=self,method=sys._getframe(),message="finish store dict")

    def saveDictionaryAsFile(self,dict,pathOutput):
        self.logger.log(cl=self,method=sys._getframe(),message="start  store dict as file")
        try:
            assert os.path.splitext(pathOutput)[1]==".pkl"
            with open (pathOutput,"wb") as fp:  pickle.dump(dict,fp)
            self.logger.log(cl=self,method=sys._getframe(),message="finish store dict as file")
        except AssertionError:
            self.logger.warning(cl=self,method=sys._getframe(),message="file " +pathOutput+" cannot be open. Is the extetion .pkl?",doQuit=False,doReturn=False)

    def readDictionaryAsFile(self,pathOutput):
        self.logger.log(cl=self,method=sys._getframe(),message="read dict as file")
        try:
            assert os.path.splitext(pathOutput)[1]==".pkl"
            with open(pathOutput, 'rb') as fp:  return pickle.load(fp)
        except AssertionError:
            self.logger.warning(cl=self,method=sys._getframe(),message="file " +pathOutput+" cannot be open. Is the extention .pkl?",doQuit=False,doReturn=False)

    def getDictPosNodes(self,df):
        # get list of nodes
        pos={}
        for row in df.iterrows():
            n_in=row[1][1]
            if n_in not in pos.keys():   pos[n_in]=tuple(str(row[1][3]).split(" "))
            n_out=row[1][2]
            if n_out not in pos.keys():   pos[n_out]=tuple(str(row[1][4]).split(" "))
        return pos

    def getNameAndExtentionFromPath(self,path):
        return os.path.splitext(path)


    def getDistancePoints(self,line):

        # coord_in=(float(coord_in[0]),float(coord_in[1]))
        # coord_out=(float(coord_out[0]),float(coord_out[1]))
        distX,distY=abs(line[0][0]-line[1][0]),abs(line[0][1]-line[1][1])
        length=pow(pow(distX,2)+pow(distY,2),.5)
        return length
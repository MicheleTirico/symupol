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

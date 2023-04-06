import os
import sys

class CreateNetwork:
    def __init__(self,config,run):
        self.__config=config
        self.__run=run
        self.__logger=self.__config.logger

        self.__links=[]


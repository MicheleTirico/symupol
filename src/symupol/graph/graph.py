import networkx as nx

from symupol.control.config import Config
from symupol.control.controller import Controller
import sys
import matplotlib.pyplot as plt
import pandas as pd

class Graph():
    def __init__(self,
                 config:Config,
                 controller:Controller):

        self.G=None
        self.df_geo = None
        self.config=config
        self.controller=controller
        self.logger=self.config.logger
        self.logger.log(cl=self,method=sys._getframe(),message="initialize Cast graph")

    def initGraph(self):    self.G=nx.DiGraph()

    def getGraph(self):
        if self.G==None:            self.logger.warning(cl=self,method=sys._getframe(),message="None is returned as graph",doQuit=False,doReturn=False)
        return self.G


    # get list of nodes
    def getListNodes (self,df):    return self.config.tools.getDictPosNodes(df=df)

    def setPathInputTsSl(self,path):    self.setPathInputTsSl=path
    def setPathInputLinks(self,path):   self.pathInputLinks=path
    def setPathOutputNx(self,path):       self.pathOutputNx=path
    def setPathOutputJpg(self,path):    self.pathOutputJpg=path
    def initDf(self,path):
        try:
            assert path!=None
            self.df = pd.read_csv(path,sep=";")
        except AssertionError:
            self.logger.warning(cl=self,method=sys._getframe(),message="path is not assigned manually. try with default path",doQuit=False,doReturn=False)
            self.df = pd.read_csv(self.pathInputLinks,sep=";")
    def plotGeoDf(self,run):
        if run:                 self.df_geo.plot()

    def saveGeoDfJpg(self,run):
        if run:                 plt.savefig(self.pathOutputJpg)

    def saveGeoDf(self,path):
        self.df_geo.to_file(path, driver='GeoJSON')

    def getInfo(self):self.df_geo.info()
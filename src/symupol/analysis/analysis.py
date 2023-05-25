from symupol.control.config import Config
from symupol.control.controller import Controller
import sys
import matplotlib.pyplot as plt

class Analysis():
    def __init__(self,
                 config:Config,
                 controller:Controller):
        self.config=config
        self.controller=controller
        self.logger=self.config.logger

        self.config.logger.log(cl=self,method=sys._getframe(),message="initialize Analysis")

        # self.abstractDF=""

        self.pathTableMerged=    self.config.pathOutputMerged
        self.pathAbstractDF=     self.config.pathAbstractDF


    def saveJpg (self,saveJpg,pathJpg,fig):
        if saveJpg:
            self.config.logger.log(cl=self,method=sys._getframe(),message="figure stored at: "+pathJpg)
            fig.savefig(pathJpg)


def test (self,val):
        print (val)
        print (self.config.paramAnalysisInterval)
        print (self.config.paramAnalysisListPollutants)

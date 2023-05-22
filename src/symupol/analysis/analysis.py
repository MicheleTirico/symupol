from symupol.control.config import Config
from symupol.control.controller import Controller
import sys

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

def test (self,val):
        print (val)
        print (self.config.paramAnalysisInterval)
        print (self.config.paramAnalysisListPollutants)

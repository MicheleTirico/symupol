import xml.etree.ElementTree as ET
import glob
import sys

class Config:
    def __init__(self,pathConfig):
        self.__tree = 0              # etree
        self.__root = 0              # etree
        self.pathConfig=pathConfig

    def setLogger(self,logger):
        self.logger=logger
        self.logger.log(cl=self,method=sys._getframe(),message="init config")

    def initUrl(self):
        self.logger.log(cl=self,method=sys._getframe(),message="set paths")

        # init logger
        self.__tree=ET.parse(self.pathConfig)
        self.__data=self.__tree.getroot()

        # path url
        self.pathAbs=                       self.__getValType("urls","url","absPath","dir")+"/"
        self.folder_scenarios=              self.pathAbs+self.__getValType("urls","url","folder_scenarios","dir")+"/"
        self.pathScenario=                  self.folder_scenarios+self.__getValType("urls","url","scenario","dir")+"/"
        self.tmp=                           self.pathAbs+self.__getValType("urls","url","tmp","dir")+"/"
        self.resources=                     self.pathAbs+self.__getValType("urls","url","resources","dir")+"/"
        self.pathConfig=                    self.pathScenario+self.__getValType("urls","url","config","file")+".xml"
        self.setup=                         self.pathScenario+self.__getValType("urls","url","setup","file")+".xml"
        self.folder_outputs=                self.pathAbs+self.__getValType("urls","url","folder_outputs","dir")+"/"
        self.folder_output=                 self.folder_outputs+self.__getValType("urls","url","scenario","dir")+"/"
        self.scenario=                      self.__getValType("urls","url","scenario","dir")
        self.inputSymuvia=                  self.pathScenario+self.__getValType("urls","url","inputSymuvia","file")
        self.folder_charts=                 self.folder_output+"charts/"

        self.setupTmp=                      self.tmp+self.__getValType("urls","url","setup","file")+".xml"
        self.outputTmp=                     self.tmp+"/OUT1/"
#        self.outputPhem=                    self.folder_output+"phem/"
#        self.outputPhemMod=                 self.folder_output+"phem/"+"tmp_400.mod"       # TODO: set the name file
        self.pathOutputSymupy               =self.folder_output+self.__getValType("urls","url","scenario","dir")+"_output_sy.xml"
        self.outputSymuvia=                 self.pathScenario+self.__getValType("urls","url","outputSymuvia","file")

        self.pathLinks=                     self.folder_output+self.scenario+"_links.csv"
        # trajectoires (class editFzp)
        self.pathOutputVehicles=            self.folder_output+self.scenario+"_trajectoires.csv"
        self.pathFzp                        =self.folder_output+self.scenario+"_trajectoiresFzp.fzp"
        self.pathTrajectories2=              self.folder_output+self.scenario+"_trajectoires2.csv"

        self.pathConfigOutput=              self.folder_output+self.__getValType("urls","url","config","file")+".xml"

        self.pathLog                        =self.folder_output + self.__getValType("urls","url","scenario","dir")+".md"
        self.gen                            =self.pathAbs+self.__getValType("urls","url","dir_gen","dir")+"/"

        # dictionary (class editFzp)
        self.pathDictVehicles               =self.folder_output+"dictVehicles.pkl"

        self.pathOutputMod                  =None
        self.pathOutputMergedTmp            =self.tmp+"merged.csv"
        self.pathOutputMerged               =self.folder_output+self.scenario+"_merged.csv"
        self.pathInputMod                   =self.folder_output+self.scenario+".mod"
        self.outputCsvFromMod               =self.folder_output+self.scenario+"_csvFromMod.csv"

    # analysis
        self.pathAbstractDF=                self.folder_output+"abstractDF.csv"
        # parameters
        self.paramAnalysisListTimeSlot=     self.__getListValues("analysis","parameter","timeSlots","list")
        self.paramAnalysisListPollutants=   self.__getListValues("analysis","parameter","pollutants","list")
        self.paramAnalysisNumberOfSplit=    self.__getListValues("analysis","parameter","numberOfSplit","list")
        self.paramAnalysisLengthMaxSplit=   self.__getListValues("analysis","parameter","lengthMaxSplit","list")
        # deprecated
        self.outputPhemDF                   =self.folder_output+"outputPhemDF.csv"      # deprecated
        self.pathTraj                       =self.folder_output+"traj/"                 # deprecated
        self.pathDri                        =self.folder_output+"dri/"                  # deprecated
        self.pathDictVehiclesPhem           =self.folder_output+"dictVehiclesPhem.pkl"  # deprecated
        # self.pathTrajMerged                 =self.folder_output+"trajectoires.csv"      # deprecated


    def getFileExtention(self,path,ext):        return glob.glob(path+"*"+ext)

    def setTools(self,tools):               self.tools=tools

    def __getListValues(self,name_root,name_tag,name,type):
        try:
            tag_root=self.__data.find(name_root)
            for e in tag_root.iter(name_tag):
                if e.get("name")==name and e.get("type")==type:
                    a=e.text.replace(" ","")
                    return a.split(",")
        except AttributeError:
            self.logger.warning(cl=self,method=sys._getframe(),message="no value for "+name_root+", "+name_tag+", "+type,doQuit= False,doReturn=False)
            return ""

    def __getValType(self,name_root,name_tag,name,type):
        try:
            tag_root=self.__data.find(name_root)
            for e in tag_root.iter(name_tag):
                if e.get("name")==name and e.get("type")==type: return e.text.replace(" ","")
        except AttributeError:
            self.logger.warning(cl=self,method=sys._getframe(),message="no value for "+name_root+", "+name_tag+", "+type,doQuit= False,doReturn=False)
            return ""
    def getPathAbs(self): return self.pathAbs

    def getNameScenario(self):  return self.__getValType("urls","url","scenario","dir")


def __test (run):
    if run:
        url="/home/mt_licit/project/symupol/scenarios/test_grid_01/config.xml"
        c=Config(url)

__test(False)

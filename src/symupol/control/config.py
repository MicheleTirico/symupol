import xml.etree.ElementTree as ET
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

        self.setupTmp=                      self.tmp+self.__getValType("urls","url","setup","file")+".xml"
        self.outputTmp=                     self.tmp+"/OUT1/"
        self.outputPhem=                    self.folder_output+"phem/"
        self.outputPhemMod=                 self.folder_output+"phem/"+"tmp_400.mod"       # TODO: set the name file

        self.pathConfigOutput=              self.folder_output+self.__getValType("urls","url","config","file")+".xml"

        self.pathLog                        =self.folder_output + self.__getValType("urls","url","scenario","dir")+".md"
        self.pathOutputSymupy               =self.folder_output+self.__getValType("urls","url","scenario","dir")+"_output_sy.xml"
        self.pathTraj                       =self.folder_output+"traj/"
        self.pathDri                        =self.folder_output+"dri/"
        self.gen=                           self.pathAbs+self.__getValType("urls","url","dir_gen","dir")+"/"
        self.pathTrajMerged                 =self.folder_output+"trajectoires.csv"
        self.pathFzp                        =self.folder_output+"trajectoiresFzp.fzp"

        self.pathDictVehicles               =self.folder_output+"dictVehicles.pkl"


    def setTools(self,tools):               self.tools=tools

    def __getValType(self,name_root,name_tag,name,type):
        tag_root=self.__data.find(name_root)
        for e in tag_root.iter(name_tag):
            if e.get("name")==name and e.get("type")==type: return e.text.replace(" ","")
        self.logger.error(cl=self,method=sys._getframe(),message="no value for "+name_root+", "+name_tag+", "+type)

    def getPathAbs(self): return self.pathAbs

    def getNameScenario(self):  return self.__getValType("urls","url","scenario","dir")
def __test (run):
    if run:
        url="/home/mt_licit/project/symupol/scenarios/test_grid_01/config.xml"
        c=Config(url)

__test(False)

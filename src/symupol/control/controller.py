import sys
import os
import glob

class Controller:
    def __init__(self,config):
        self.__config=config
        self.__config.logger.log(cl=self,method=sys._getframe(),message="init controller")

    def initSymupy(self):
        from symupy.runtime.api import Simulator, Simulation
        self.__config.logger.log(cl=self,method=sys._getframe(),message="init symupy")
        self.__config.logger.log(cl=self,method=sys._getframe(),message="set scenario symupy")
        scenario = os.path.abspath(self.__config.setupTmp)
        self.__config.logger.log(cl=self,method=sys._getframe(),message="set simulator symupy")
        self.simulator=Simulator()
        self.__config.logger.log(cl=self,method=sys._getframe(),message="set register symupy")
        self.simulator.register_simulation(scenario)

    def runSymupy(self,run):
        if run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="start simulation symupy")
            self.simulator.run()
            self.__config.logger.log(cl=self,method=sys._getframe(),message="finish simulation symupy")

    def editOutput(self,run):
        if run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="edit output symuvia")
            file=glob.glob(self.__config.folder_output+"*_traf.xml")
            os.system("mv "+ file[0]+" " +self.__config.pathOutputSymupy )

    def deleteTmp(self,run):
        if run and os.path.exists(self.__config.tmp):
            self.__config.logger.log(cl=self,method=sys._getframe(),message="delete files in folder "+self.__config.tmp)
            os.system("rm -r "+self.__config.tmp)

    def deleteOutput(self,run):
        if run and os.path.exists(self.__config.folder_output)==True:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="delete files in folder "+self.__config.folder_output)
            os.system("rm -r "+self.__config.folder_output)
    
    def copyToTmp(self,run):
        if run:
            os.system("cp "+ self.__config.setup + " "+self.__config.setupTmp)

    def copyToOutput(self,run):
        if run:
            os.system("cp "+ self.__config.setupTmp+" "+self.__config.folder_output)
            os.system("cp "+ self.__config.pathConfig+" "+self.__config.folder_output)

    def initFolder (self):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="create folders")
        paths=[
            self.__config.tmp,
            self.__config.folder_outputs,
            self.__config.folder_output
        ]
        self.__createfolers(paths)

    def initTmp(self):
        files=[self.__config.setup]
        self.__copyFiles(files,self.__config.tmp)

    def moveOutput(self,run):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="move outputs")
        if run:
            if os.path.exists(self.__config.tmp+"OUT1/"):
                os.system("mv "+self.__config.outputTmp+"* "+ self.__config.folder_output )
                os.system("rmdir " +self.__config.outputTmp)

    def __createfolers(self,paths):
        for path in paths :
            if os.path.exists(path)==False:
                self.__config.logger.log(cl=self,method=sys._getframe(),message="create folder in: "+path)
                os.system("mkdir "+path)


    def __copyFiles(self,files, pathDirectoryOutput):
        for file in files :
            if os.path.exists(file)==False:
                self.__config.logger.log(cl=self,method=sys._getframe(),message="copy file in: "+file)
                os.system("cp "+file +" "+pathDirectoryOutput+"/"+os.path.basename(file))

    def initPhem (self):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="init Phem")
        paths=[self.__config.outputPhem]
        self.__createfolers(paths)

    def runPhem(self):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="start Phem analysis")

        self.__config.logger.log(cl=self,method=sys._getframe(),message="finish Phem analysis")

    def editOutputSymupy(self):
        # todo
        self.__config.logger.log(cl=self,method=sys._getframe(),message="start edit output symuvia")
        self.__config.logger.warning(cl=self,method=sys._getframe(),message="TODO: integrate classes in controller",doQuit=False,doReturn=False)


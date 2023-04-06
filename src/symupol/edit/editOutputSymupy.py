import os
import xml.etree.ElementTree as ET
import sys

class EditOutputSymupy:
    def __init__(self,run,config,logger):
        self.__run=run
        self.__config=config
        self.__logger=logger

        self.__vehicles={}
        self.__pathInput=None
        self.__pathOutput=None

    def setFiles(self,pathInput,pathOutput):
        self.__pathInput=pathInput
        self.__pathOutput=pathOutput

    def initClass(self):
        if self.__config!=None:
            self.__folder_output=self.__config.folder_output
            self.__pathOutputSymupy=self.__config.pathOutputSymupy
            self.__pathTraj=self.__config.pathTraj
            self.__pathTrajMerged=self.__config.pathTrajMerged
            self.__pathDri=self.__config.pathDri
            self.__pathFzp=self.__config.pathFzp
        else:
            self.__folder_output=self.__pathOutput
            self.__pathOutputSymupy=self.__pathInput
            print (self.__pathOutputSymupy)
            self.__pathTraj=self.__pathOutput+"traj/"
            self.__pathTrajMerged=self.__pathOutput+"traj_merged.csv"
            self.__pathDri=self.__pathOutput+"dri/"
            self.__pathFzp=self.__pathOutput+"trajectories.fzp"

        if self.__logger==None:
            self.__logger=Logger(self.__config, True)
            self.__logger.setDisplay(True,True,True,True)
            self.__logger.storeLocal(False)

        self.__logger.log(cl=self,method=sys._getframe(),message="init edit output symupy")

        self.initFiles()

    def initFiles (self):
        if self.__run:
            # find file export
            test=True
            for file in os.listdir(self.__folder_output):
                if file.endswith("_traf.xml"):
                    oldPath=os.path.join(self.__folder_output, file)
                    os.system("cp "+oldPath +" "+self.__pathOutputSymupy)
                    test=False
            if test:self.__logger.warning(cl=self,method=sys._getframe(),message="path output symupy does not funded. Cannot go through the analysis.",doQuit=True,doReturn=True)

    #    make a file for each vehicle (header id vehicle, column t,v(m/s),g)
    def exportTrajectories(self):
        if self.__run:
            self.__logger.log(cl=self,method=sys._getframe(),message="start export trajectories")
            self.__createDictVehicles()
            self.__storetrajVehicles(False)
            self.__storetrajAndDri(True,True)
            self.__logger.log(cl=self,method=sys._getframe(),message="finish  export trajectories")

    def exportTrajectoiresMerged(self):
        if self.__run:
            self.__logger.log(cl=self,method=sys._getframe(),message="start export trajectories")
            self.__createDictVehicles()
            self.__storetrajAndDriMerged(True,True)
            self.__logger.log(cl=self,method=sys._getframe(),message="finish sore traj and dri merged")

    def exportFzp(self,computeFzp):
        self.__storeFzp(computeFzp)
        self.__logger.log(cl=self,method=sys._getframe(),message="finish store fzp")

    def __storeFzp(self,run):
        self.__createDictVehicles()
        if run:
            self.__logger.log(cl=self,method=sys._getframe(),message="start store fzp")

            if os.path.exists(self.__config.pathFzp):  os.system("rm "+self.__config.pathFzp)
            open(self.__config.pathFzp, 'a').close()
            headerTraj="time;x;y;vehicle number;speed;road inclination;vehicle type;segment number"

            with open(self.__config.pathFzp, "a") as f:
                f.write(headerTraj+"\n")
                for vehicle in self.__vehicles.items():
                    for item in vehicle:
                        for vals in item:
                            if type(vals) is list:

                                #           print (type(vals),len(vals),vals)
                                l= [vals[0], # time
                                    vals[1], # x
                                    vals[5], # y
                                    vals[4], # vehicle number
                                    vals[8], # speed
                                    vals[10],# road inclination
                                    100,#vals[7],# vehicle type
                                    0#vals[6]# segment number
                                    ]
                    # print (type(vals[0]))
                    # print (float(vals[0]))
                    # print (round(vals[0]))
                    # print (int(vals[0]))
                    #                    a=str(int(float(vals[0])))+";"+vals[1]+";"+";"+vals[4]+";"+vals[8]+";"+vals[10]+";"+"\n"
                    #                   print (a)
                    f.write(str(int(float(vals[0])))+";"+vals[1]+";"+ vals[5]+";"+vals[4]+";"+vals[8]+";"+vals[10]+";100;0\n")#vals[6]# segment number
                    # f.write(";".join(l)+"\n")

                #     list=[item[0],item[1]]                    ]
                #f.write(";".join(list)+"\n")
            # 0                   [inst_val,
            #                    traj.attrib["abs"],
            #   2                 traj.attrib["acc"],
            #                    traj.attrib["dst"],
            #    4                traj.attrib["id"],
            #                    traj.attrib["ord"],
            #     6               traj.attrib["tron"],
            #                    traj.attrib["type"],
            #     8               traj.attrib["vit"],
            #                    traj.attrib["voie"],
            #     10            traj.attrib["z"]]


            # for inst in item[1]: f.write(",".join(inst)+"\n")



            self.__logger.log(cl=self,method=sys._getframe(),message="finish store fzp")


    def __createDictVehicles(self):
        self.__logger.log(cl=self,method=sys._getframe(),message="start create dictionary")
        traj_tree=ET.parse(self.__pathOutputSymupy)
        traj_root=traj_tree.getroot()
        traj_element_simulation=traj_root.find("SIMULATION")
        traj_element_instants=traj_element_simulation.find("INSTANTS")

        for inst in traj_element_instants:
            inst_val=inst.attrib["val"]
            trajs=inst.find("TRAJS")
            for traj in trajs:
                id=traj.attrib["id"]
                try:vehicle=self.__vehicles[id]
                except KeyError: self.__vehicles[id]=[]
                self.__attribs=traj.attrib

                l=self.__vehicles[id]
                l.append([inst_val,traj.attrib["abs"],traj.attrib["acc"],traj.attrib["dst"],
                          traj.attrib["id"],traj.attrib["ord"],traj.attrib["tron"],
                          traj.attrib["type"],traj.attrib["vit"],traj.attrib["voie"],traj.attrib["z"]])
                self.__vehicles[id]=l
        self.__logger.log(cl=self,method=sys._getframe(),message="finish create dictionary")

    def __storetrajVehicles(self,run):
        if run:
            self.__logger.log(cl=self,method=sys._getframe(),message="start store vehicles")
            if os.path.exists(self.__pathTraj):  os.system("rm -r "+self.__pathTraj)
            os.system("mkdir "+self.__pathTraj)
            for item in self.__vehicles.items():
                formatFile=".csv"
                file=self.__config.getNameScenario()+"_traj_"+item[0]
                pathVehicle=self.__pathTraj+file+formatFile
                open(pathVehicle, 'a').close()
                header=item[0]+","+",".join(self.__attribs)
                with open(self.__pathTraj+file+formatFile, "a") as f:
                    f.write(header+"\n")
                    for inst in item[1]: f.write(",".join(inst)+"\n")

            self.__logger.log(cl=self,method=sys._getframe(),message="finish store vehicles")

    def __storetrajAndDriMerged(self,runTraj,runDri):
        self.__logger.log(cl=self,method=sys._getframe(),message="start store traj and dri")

        if runTraj:
            if os.path.exists(self.__pathTraj):  os.system("rm -r "+self.__pathTraj)
            os.system("mkdir "+self.__pathTraj)
        if runDri:
            if os.path.exists(self.__pathDri): os.system("rm -r "+self.__pathDri)
            os.system("mkdir "+self.__pathDri)

        open(self.__pathTrajMerged, 'a').close()

        for item in self.__vehicles.items():
            formatFileTraj,formatFileDri=".csv",".dri"
            nameFile=self.__config.getNameScenario()+"_"+item[0]
            pathDri=self.__pathDri+nameFile+formatFileDri

            if runTraj:
                headerTraj="vehNr: "+item[0]+","+",".join(self.__attribs)
                with open(self.__pathTrajMerged, "a") as f:
                    f.write(headerTraj+"\n")
                    for inst in item[1]: f.write(",".join(inst)+"\n")

            if runDri:
                open(pathDri, 'a').close()
                headerDri=item[0]+","+list (self.__attribs.keys())[7]+","+list (self.__attribs.keys())[9]
                with open(pathDri, "a") as f:
                    if len(headerDri)!=0:f.write(headerDri+"\n")
                    for inst in item[1]: f.write(inst[0]+","+inst[8]+","+inst[10]+"\n")

        self.__logger.log(cl=self,method=sys._getframe(),message="finish store traj and dri")

    def __storetrajAndDri(self,runTraj,runDri):
        self.__logger.log(cl=self,method=sys._getframe(),message="start store traj and dri")

        if runTraj and os.path.exists(self.__pathTraj):os.system("rm -r "+self.__pathTraj+" & mkdir "+self.__pathTraj)
        if runDri and os.path.exists(self.__pathDri):  os.system("rm -r "+self.__pathDri +" & mkdir "+self.__pathDri)

        for item in self.__vehicles.items():
            formatFileTraj,formatFileDri=".csv",".dri"
            nameFile=self.__config.getNameScenario()+"_"+item[0]
            pathTraj,pathDri=self.__pathTraj+nameFile+formatFileTraj,self.__pathDri+nameFile+formatFileDri

            if runTraj:
                open(pathTraj, 'a').close()
                headerTraj=item[0]+","+",".join(self.__attribs)
                with open(pathTraj, "a") as f:
                    if len(headerTraj)!=0:f.write(headerTraj+"\n")
                    for inst in item[1]: f.write(",".join(inst)+"\n")

            if runDri:
                open(pathDri, 'a').close()
                headerDri=item[0]+","+list (self.__attribs.keys())[7]+","+list (self.__attribs.keys())[9]
                with open(pathDri, "a") as f:
                    if len(headerDri)!=0:f.write(headerDri+"\n")
                    for inst in item[1]: f.write(inst[0]+","+inst[8]+","+inst[10]+"\n")

        self.__logger.log(cl=self,method=sys._getframe(),message="finish store traj and dri")

def compute():

    # try: from symupol.control.logger import Logger
    # except ModuleNotFoundError:        pass
    eos=EditOutputSymupy(run=True,config=None,logger=None)
    eos.setFiles(pathInput="/home/mt_licit/project/symupol/symupol/outputs/test_grid_01/test_grid_01_output_sy.xml",               pathOutput="/home/mt_licit/project/symupol/test/")
    eos.initClass()
    # eos.exportFzp(True)

if __name__ == "__main__":
    compute()





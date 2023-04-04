import os
import xml.etree.ElementTree as ET
import sys

class EditOutputSymupy:
    def __init__(self,config,run):
        self.__run=run
        self.__config=config
        self.__config.logger.log(cl=self,method=sys._getframe(),message="init class")
        self.__vehicles={}

    def initFiles (self):
        if self.__run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="init edit output symupy")
            # find file export
            test=True
            for file in os.listdir(self.__config.folder_output):
                if file.endswith("_traf.xml"):
                    oldPath=os.path.join(self.__config.folder_output, file)
                    os.system("cp "+oldPath +" "+self.__config.pathOutputSymupy)
                    test=False
            if test:self.__config.logger.warning(cl=self,method=sys._getframe(),message="path output symupy does not funded. Cannot go through the analysis.",doQuit=True,doReturn=True)

    #    make a file for each vehicle (header id vehicle, column t,v(m/s),g)
    def exportTrajectories(self):
        if self.__run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="start export trajectories")
            self.__createDictVehicles()
            self.__storetrajVehicles(False)
            self.__storetrajAndDri(True,True)
            self.__config.logger.log(cl=self,method=sys._getframe(),message="finish  export trajectories")

    def exportTrajectoiresMerged(self):
        if self.__run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="start export trajectories")
            self.__createDictVehicles()
            self.__storetrajAndDriMerged(True,True)
            self.__config.logger.log(cl=self,method=sys._getframe(),message="finish sore traj and dri merged")

    def exportFzp(self,computeFzp):
        self.__storeFzp(computeFzp)
        self.__config.logger.log(cl=self,method=sys._getframe(),message="finish store fzp")

    def __storeFzp(self,run):
        self.__createDictVehicles()
        if run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="start store fzp")

            if os.path.exists(self.__config.pathFzp):  os.system("rm "+self.__config.pathFzp)
            open(self.__config.pathFzp, 'a').close()
            headerTraj="time;x;y;vehicle number;speed;road inclination;vehicle type;segment number"

            with open(self.__config.pathFzp, "a") as f:
                f.write(headerTraj+"\n")
                print ("peppe",len(self.__vehicles))
                for item in self.__vehicles.items():
                    list=[str(item[0]),str(item[1])

                    ]
                    f.write(list[0]+";"+list[1]+"\n")
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



            self.__config.logger.log(cl=self,method=sys._getframe(),message="finish store fzp")


    def __createDictVehicles(self):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="start create dictionary")
        traj_tree=ET.parse(self.__config.pathOutputSymupy)
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
        self.__config.logger.log(cl=self,method=sys._getframe(),message="finish create dictionary")

    def __storetrajVehicles(self,run):
        if run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="start store vehicles")
            if os.path.exists(self.__config.pathTraj):  os.system("rm -r "+self.__config.pathTraj)
            os.system("mkdir "+self.__config.pathTraj)
            for item in self.__vehicles.items():
                formatFile=".csv"
                file=self.__config.getNameScenario()+"_traj_"+item[0]
                pathVehicle=self.__config.pathTraj+file+formatFile
                open(pathVehicle, 'a').close()
                header=item[0]+","+",".join(self.__attribs)
                with open(self.__config.pathTraj+file+formatFile, "a") as f:
                    f.write(header+"\n")
                    for inst in item[1]: f.write(",".join(inst)+"\n")

            self.__config.logger.log(cl=self,method=sys._getframe(),message="finish store vehicles")

    def __storetrajAndDriMerged(self,runTraj,runDri):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="start store traj and dri")

        if runTraj:
            if os.path.exists(self.__config.pathTraj):  os.system("rm -r "+self.__config.pathTraj)
            os.system("mkdir "+self.__config.pathTraj)
        if runDri:
            if os.path.exists(self.__config.pathDri): os.system("rm -r "+self.__config.pathDri)
            os.system("mkdir "+self.__config.pathDri)

        open(self.__config.pathTrajMerged, 'a').close()

        for item in self.__vehicles.items():
            formatFileTraj,formatFileDri=".csv",".dri"
            nameFile=self.__config.getNameScenario()+"_"+item[0]
            pathDri=self.__config.pathDri+nameFile+formatFileDri

            if runTraj:
                headerTraj="vehNr: "+item[0]+","+",".join(self.__attribs)
                with open(self.__config.pathTrajMerged, "a") as f:
                    f.write(headerTraj+"\n")
                    for inst in item[1]: f.write(",".join(inst)+"\n")

            if runDri:
                open(pathDri, 'a').close()
                headerDri=item[0]+","+list (self.__attribs.keys())[7]+","+list (self.__attribs.keys())[9]
                with open(pathDri, "a") as f:
                    if len(headerDri)!=0:f.write(headerDri+"\n")
                    for inst in item[1]: f.write(inst[0]+","+inst[8]+","+inst[10]+"\n")

        self.__config.logger.log(cl=self,method=sys._getframe(),message="finish store traj and dri")



    def __storetrajAndDri(self,runTraj,runDri):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="start store traj and dri")

        if runTraj:
            if os.path.exists(self.__config.pathTraj):  os.system("rm -r "+self.__config.pathTraj)
            os.system("mkdir "+self.__config.pathTraj)
        if runDri:
            if os.path.exists(self.__config.pathDri): os.system("rm -r "+self.__config.pathDri)
            os.system("mkdir "+self.__config.pathDri)

        for item in self.__vehicles.items():
            formatFileTraj,formatFileDri=".csv",".dri"
            nameFile=self.__config.getNameScenario()+"_"+item[0]
            pathTraj,pathDri=self.__config.pathTraj+nameFile+formatFileTraj,self.__config.pathDri+nameFile+formatFileDri

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

        self.__config.logger.log(cl=self,method=sys._getframe(),message="finish store traj and dri")


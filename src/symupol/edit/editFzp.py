import os
import sys
import xml.etree.ElementTree as ET

class EditFzp:
    def __init__(self,config,run):
        self.__config=config
        self.__run=run
        self.__logger=self.__config.logger
        self.__pathOutputSymupy=self.__config.pathOutputSymupy

    def setInputPath(self,path):        self.__pathOutputSymupy=path

    def init(self):
        self.__logger.log(cl=self,method=sys._getframe(),message="init edit fzp")
        self.__vehicles={}

    def compute(self):
        self.__logger.log(cl=self,method=sys._getframe(),message="start  compute fzp")

        # create dictionary
        if os.path.exists(self.__config.pathDictVehicles):
            self.__logger.log(cl=self,method=sys._getframe(),message="file: "+self.__config.pathDictVehicles+" founded. Read the dict")
            # test if dict already exist
            self.__vehicles=self.__config.tools.readDictionaryAsFile(self.__config.pathDictVehicles)
        else:
            self.__logger.log(cl=self,method=sys._getframe(),message="file: "+self.__config.pathDictVehicles+" cannot be founded. Compute the dict")
            self.__vehicles=self.__createDictVehicles(run=True) # create the dict
            try:                    assert len(self.__vehicles) != 0
            except AssertionError:  self.__logger.warning(cl=self,method=sys._getframe(),message="len of dictionary is 0",doQuit=False,doReturn=False)
            self.__config.tools.saveDictionaryAsFile(dict=self.__vehicles,pathOutput=self.__config.pathDictVehicles)

        # store fzp
        try:
            assert os.path.exists(self.__config.pathDictVehicles)
            self.__storeFzp(run=True)

        # store
        except AssertionError:
            self.__logger.error(cl=self,method=sys._getframe(),message="file: "+self.__config.pathDictVehicles +" not funded. Cannot compute the .fzp file")


        self.__logger.log(cl=self,method=sys._getframe(),message="finish compute fzp")


    def __storeFzp(self,run):
        if run:
            self.__logger.log(cl=self,method=sys._getframe(),message="start  store fzp")
            if os.path.exists(self.__config.pathFzp):  os.system("rm "+self.__config.pathFzp) # remove file if exist
            headerTraj="time;x;y;vehicle number;speed;road inclination;vehicle type;segment number"
            with open(self.__config.pathFzp, "a") as f:
                f.write(headerTraj+"\n")
                for vehicle in self.__vehicles.items():
                    for item in vehicle:
                        for vals in item:
                            if type(vals) is list:
                                line=[int(float(vals[0])),vals[1],vals[5],vals[4],vals[8],vals[10],100,0]
                                #    for i in range(len(line)):                                    line[i]=str(line[i])

                                b=[str(line[i]) for i in range(len(line))]
                                a=";".join(b)+"\n"
                                f.write(a)

            self.__logger.log(cl=self,method=sys._getframe(),message="finish store fzp")


    def __createDictVehicles(self,run):
        if run:
            vehicles={}
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
                    try:vehicle= vehicles[id]
                    except KeyError: vehicles[id]=[]
                    self.__attribs=traj.attrib

                    l=vehicles[id]
                    l.append([inst_val,traj.attrib["abs"],traj.attrib["acc"],traj.attrib["dst"],
                              traj.attrib["id"],traj.attrib["ord"],traj.attrib["tron"],
                              traj.attrib["type"],traj.attrib["vit"],traj.attrib["voie"],traj.attrib["z"]])
                    vehicles[id]=l
            self.__logger.log(cl=self,method=sys._getframe(),message="finish create dictionary")
            return vehicles
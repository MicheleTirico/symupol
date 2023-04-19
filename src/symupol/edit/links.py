import sys
import csv
import xml.etree.ElementTree as ET

class Links:
    def __init__(self,config,run):
        self.__config=config
        self.__run=run
        self.__logger=self.__config.logger
        self.__links={}

        self.__outputCsv="" #TODO
        self.__outputTrajectories="" #TODO
        self.__inputXml="" #TODO
        self.__inputTrajectories="" #TODO

    def setOutputCsv(self,path):            self.__outputCsv=path

    def setOutputTrajectories(self,path):   self.__outputTrajectories=path

    def setInputXml(self,path):             self.__inputXml=path

    def setInputTrajectories(self,path):    self.__inputTrajectories=path

    def createCsv(self):
        self.__logger.log(cl=self,method=sys._getframe(),message="start  create links")
        self.__tree=ET.parse(self.__inputXml)
        self.__data=self.__tree.getroot()

        reseaux=self.__data.find("RESEAUX")
        reseau=reseaux.find("RESEAU")
        troncons=reseau.find("TRONCONS")

#        if os.path.exists(self.__outputCsv):            os.system("rm "+self.__outputCsv) # remove file if exist
        header="id;in;out;coord_in,coord_out,width,id_opp_link,length\n"
        with open(self.__outputCsv, "w") as f:
            f.write(header)
            for tron in troncons.iter():
                if len(tron.attrib.values())!=0:
                    dict=tron.attrib               # handle opposite links
                    if "id_troncon_oppose" not in dict.keys():dict["id_troncon_oppose"]=""
                    l=dict.values()
                    id=tron.attrib["id"]
                    link=Link(id)
                    # compute and add length
                    coord_in,coord_out=tron.attrib["extremite_amont"].split(" "),tron.attrib["extremite_aval"].split(" ")
                    coord_in=(float(coord_in[0]),float(coord_in[1]))
                    coord_out=(float(coord_out[0]),float(coord_out[1]))
                    distX,distY=abs(coord_in[0]-coord_out[0]),abs(coord_in[1]-coord_out[1])
                    length=pow(pow(distX,2)+pow(distY,2),.5)
                    v=";".join(l)+";"+str(length)+"\n"
                    f.write(v)
                    dict["length"]=length
                    link.setListAttribs(dict)
                    self.__links[id]=link

        self.__logger.log(cl=self,method=sys._getframe(),message="finish create links")

    def addLengthTotrajectories(self,run):
        if run:
            try:
                self.__logger.log(cl=self,method=sys._getframe(),message="start  add length at trajectories")
                assert len(self.__links)!=0
                with open(self.__inputTrajectories,"r") as f_reader:
                    reader=csv.reader(f_reader)
                    with open(self.__outputTrajectories,"w") as f_writer:
                        header=next(f_reader).replace("\n","")+";length;isIntersection\n"
                        f_writer.write(header)
                        for row in reader:
                            line=row[0].split(";")
                            link=self.__getLink(line[6])
                            if link!=None:
                                length=str(link.getAttrib(attribName="length"))
                                isIntersection="False"
                            else:
                                length="0"
                                isIntersection="True"
                            line.extend([length,isIntersection])
                            f_writer.write(";".join(line)+"\n")
                self.__logger.log(cl=self,method=sys._getframe(),message="finish add length to links")

            except AssertionError:
                self.__config.logger.error(cl=self,method=sys._getframe(),message="the list of links is empty",error=AssertionError)
        self.__config.pathOutputVehicles=self.__outputTrajectories
        
    def __getLink(self,id):
        try:
            return self.__links[id]
        except KeyError:
            #self.__config.logger.warning(cl=self,method=sys._getframe(),message="link not founded",doQuit=False,doReturn=False)
            return None

class Link:
    def __init__(self,id):
        self.__id=id
        self.__attribs={}
    def setId(self,id): self.__id=id

    def setAttrib(self,attribName,attribVal):        self.__attribs[attribName]=attribVal

    def getAttrib(self,attribName):
        try:                    return self.__attribs[attribName]
        except AttributeError:
            self.__config.logger.warning(cl=self,method=sys._getframe(),message="None value instead of link",doQuit=False,doReturn=False)
            return ""

    def setListAttribs(self,attribs):               self.__attribs=attribs
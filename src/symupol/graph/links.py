import sys
import csv
import xml.etree.ElementTree as ET
import os
from symupol.control import tools_shapely
from shapely.geometry import LineString, Point

from symupol.control.tools_shapely import splitLineStringDistance


class Links:
    def __init__(self,graph):
        self.graph=graph
       # self.graph.logger=self.graph.config.logger
        self.__links={}

        self.__outputCsv="" #TODO
        self.__outputTrajectories="" #TODO
        self.__inputXml="" #TODO
        self.__inputTrajectories="" #TODO
        self.__outputSplitLinks=""  #TODO

    def setOutputCsv(self,path):            self.__outputCsv=path

    def setOutputTrajectories(self,path):   self.__outputTrajectories=path

    def setInputXml(self,path):             self.__inputXml=path

    def setInputTrajectories(self,path):    self.__inputTrajectories=path

    def setOutputSplitLinks(self,path):     self.__outputSplitLinks=path

    def createCsv(self,run):
        if run:
            self.graph.logger.log(cl=self,method=sys._getframe(),message="start  create links")
            self.__tree=ET.parse(self.__inputXml)
            self.__data=self.__tree.getroot()

            reseaux=self.__data.find("RESEAUX")
            reseau=reseaux.find("RESEAU")
            troncons=reseau.find("TRONCONS")

            #if os.path.exists(self.__outputCsv):            os.system("rm "+self.__outputCsv) # remove file if exist
            headerFr="id;id_eltamont;id_eltaval;extremite_amont;extremite_aval"
            headerList=headerFr.split(";")
            header="id;in;out;coord_in;coord_out;int_points;length\n"

            with open(self.__outputCsv, "w") as f:
                f.write(header)
                for tron in troncons.iter():
                    if len(tron.attrib.values())!=0 and tron.tag=="TRONCON":
                        dict=tron.attrib               # handle opposite links
                        l=dict.values()
                        id=tron.attrib["id"]
                        link=Link(id)

                        # compute and add length
                        coord_in,coord_out=tron.attrib["extremite_amont"].split(" "),tron.attrib["extremite_aval"].split(" ")
                        coord_in=(float(coord_in[0]),float(coord_in[1]))
                        coord_out=(float(coord_out[0]),float(coord_out[1]))
                        distX,distY=abs(coord_in[0]-coord_out[0]),abs(coord_in[1]-coord_out[1])
                        length=pow(pow(distX,2)+pow(distY,2),.5)
                        v2=[]
                        for i in headerList:    v2.append(tron.attrib[i])
                        dict["length"]=length

                        # add internal points
                        int_points=tron.find("POINTS_INTERNES")
                        if int_points!=None:
                            p=""
                            for point in int_points:p+=point.attrib["coordonnees"]+" "
                            v2.append(p)
                        else:v2.append(" ")

                        v2.append(str(length))
                        f.write(";".join(v2)+"\n")
                        link.setListAttribs(dict)
                        self.__links[id]=link

            self.graph.logger.log(cl=self,method=sys._getframe(),message="finish create links")

    def addLengthTotrajectories(self,run):
        if run:
            try:
                self.graph.logger.log(cl=self,method=sys._getframe(),message="start  add length at trajectories")
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
                self.graph.logger.log(cl=self,method=sys._getframe(),message="finish add length to links")

            except AssertionError:
                self.graph.config.logger.error(cl=self,method=sys._getframe(),message="the list of links is empty",error=AssertionError)
        self.graph.config.pathOutputVehicles=self.__outputTrajectories
        
    def __getLink(self,id):
        try:
            return self.__links[id]
        except KeyError:
            #self.graph.config.logger.warning(cl=self,method=sys._getframe(),message="link not founded",doQuit=False,doReturn=False)
            return None

    def __getMultiLineString(self):
        self.graph.logger.log(cl=self,method=sys._getframe(),message="start  create multi LineString")
        multiLineString={}
        with open (self.__outputCsv, "r") as f_read:
            next(f_read).replace("\n","")
            for row in  csv.reader(f_read):
                vals=row[0].split(";")
                coord_in,coord_out,coord_int_points=vals[3].split(" "), vals[4].split(" "), vals[5].split(" ")
                coord_int_points.remove('') if '' in coord_int_points else None
                list_int_points=[(float(coord_int_points[i]),float(coord_int_points[i + 1])) for i in range (0,len(coord_int_points)-1,2)]
                point_in=Point(float(coord_in[0]),float(coord_in[1]))
                point_out=Point(float(coord_out[0]),float(coord_out[1]))

                l=[point_in]+[Point(i) for i in list_int_points]+[point_out]

                line=LineString(l)
                id=vals[0].split(" ")[0]
                multiLineString[id]=line
        self.graph.logger.log(cl=self,method=sys._getframe(),message="finish create multi LineString")
        return multiLineString

    def splitLinks_ns(self,run):
        if run:
            self.graph.logger.log(cl=self,method=sys._getframe(),message="start split links")
            mls=self.__getMultiLineString()
            for ns in self.graph.config.paramAnalysisNumberOfSplit:
                with open (self.graph.config.folder_output+self.graph.config.scenario+"_ns_{:0>4}.csv".format(ns), "w") as f_write:
                    self.graph.logger.log(cl=self,method=sys._getframe(),message="split links by max length of: "+ns)

                    header="tron;in;out;coord_in;coord_out;int_points;length;id_split\n"
                    f_write.write(header)
                    for id,lineString in mls.items():
                        nSplit=lineString.length//float(ns)+1
                        splitLine=tools_shapely.splitLineStringNsplit(lineString,nSplit,list())
                        if splitLine!=None:
                            tools_shapely.removeShortLines(splitLine,0.001)
                            i=1
                            for splittedLine in splitLine:
                                id_split=id+"_split-"+str(float(i))            #id+"_{:0>4}".format(i)
                                vals=[id,
                                      "-",
                                      "-",
                                      str(splittedLine.coords[0][0])+" "+str(splittedLine.coords[0][1]),
                                      str(splittedLine.coords[1][0])+" "+str(splittedLine.coords[1][1]),
                                      "-",
                                      str(splittedLine.length),
                                      id_split
                                      ]
                                f_write.write(";".join(vals)+"\n")
                                i+=1

        self.graph.logger.log(cl=self,method=sys._getframe(),message="start split finish")
    def splitLinks_lms(self,run):
        if run:
            self.graph.logger.log(cl=self,method=sys._getframe(),message="start split links")
            mls=self.__getMultiLineString()
            for maxLen in self.graph.config.paramAnalysisLengthMaxSplit:
                with open (self.graph.config.folder_output+"link_splitted_lms_{:0>4}.csv".format(maxLen), "w") as f_write:
                    self.graph.logger.log(cl=self,method=sys._getframe(),message="split links by max length of: "+maxLen)

                    header="tron;in;out;coord_in;coord_out;int_points;length;id_split\n"
                    f_write.write(header)
                    for id,lineString in mls.items():
                        nSplit=lineString.length//float(maxLen)+1
                        splitLine=tools_shapely.splitLineStringNsplit(lineString,nSplit,list())
                        if splitLine!=None:
                            tools_shapely.removeShortLines(splitLine,0.001)
                            i=1
                            for splittedLine in splitLine:
                                id_split=id+"_split-"+str(float(i))            #id+"_{:0>4}".format(i)
                                vals=[id,
                                      "-",
                                      "-",
                                      str(splittedLine.coords[0][0])+" "+str(splittedLine.coords[0][1]),
                                      str(splittedLine.coords[1][0])+" "+str(splittedLine.coords[1][1]),
                                      "-",
                                      str(splittedLine.length),
                                      id_split
                                ]
                                f_write.write(";".join(vals)+"\n")
                                i+=1

        self.graph.logger.log(cl=self,method=sys._getframe(),message="start split finish")

    def __getLineString(self,vals):
        l=[]
        l.append(tuple(vals[3].split(" ")))
        int_points=vals[5].split(" ")
        int_points.remove('') if '' in int_points else None
        list_int_points=[(int_points[i],int_points[i + 1]) for i in range (0,len(int_points)-1,2)]
        for i in list_int_points:l.append(i)
        l.append(tuple(vals[4].split(" ")))
        return l


        # for filename in os.listdir(self.graph.config.folder_output):
        #     f = os.path.join(self.graph.config.folder_output, filename)
        #     # print (filename)
        #     if "ts-" in filename and "np-" in filename:
        #         print(f)

#        self.graph.logger.log(cl=self,method=sys._getframe(),message="start split links in: "+self.graph.config.pa)

class Link:
    def __init__(self,id):
        self.__id=id
        self.__attribs={}

    def setId(self,id): self.__id=id

    def setAttrib(self,attribName,attribVal):        self.__attribs[attribName]=attribVal

    def getAttrib(self,attribName):
        try:                    return self.__attribs[attribName]
        except AttributeError:
            #self.graph.logger.warning(cl=self,method=sys._getframe(),message="None value instead of link",doQuit=False,doReturn=False)
            return ""

    def setListAttribs(self,attribs):               self.__attribs=attribs
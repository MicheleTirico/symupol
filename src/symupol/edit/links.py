import math
import os
import sys
import csv
import xml.etree.ElementTree as ET
import math
import pandas as pd

class Links:
    def __init__(self,config,run):
        self.__config=config
        self.__run=run
        self.__logger=self.__config.logger
    def setOutputCsv(self,path):self.__outputCsv=path
    def setInputXml(self,path):self.__inputXml=path

    def setInputTrajectories(self,path):    self.__inputTrajectories=path

    def createCsv(self):
        self.__logger.log(cl=self,method=sys._getframe(),message="start  create links")
        self.__tree=ET.parse(self.__inputXml)
        self.__data=self.__tree.getroot()

        reseaux=self.__data.find("RESEAUX")
        reseau=reseaux.find("RESEAU")
        troncons=reseau.find("TRONCONS")

#        if os.path.exists(self.__outputCsv):            os.system("rm "+self.__outputCsv) # remove file if exist
        header="tron;in;out;coord_in,coord_out,width,id_opp_link,length\n"
        with open(self.__outputCsv, "w") as f:
            f.write(header)
            for tron in troncons.iter():
                if len(tron.attrib.values())!=0:
                    l=tron.attrib               # handle opposite links
                    if "id_troncon_oppose" not in l.keys():                        l["id_troncon_oppose"]=""
                    l=l.values()

                    # compute and add length
                    coord_in,coord_out=tron.attrib["extremite_amont"].split(" "),tron.attrib["extremite_aval"].split(" ")
                    coord_in=(float(coord_in[0]),float(coord_in[1]))
                    coord_out=(float(coord_out[0]),float(coord_out[1]))
                    distX,distY=abs(coord_in[0]-coord_out[0]),abs(coord_in[1]-coord_out[1])
                    length=pow(pow(distX,2)+pow(distY,2),.5)
                    v=";".join(l)+";"+str(length)+"\n"
                    f.write(v)

        self.__logger.log(cl=self,method=sys._getframe(),message="finish create links")

    def addLengthTotrajectories(self):
        df1=pd.read_csv(filepath_or_buffer=self.__inputTrajectories,sep=";")
        df2=pd.read_csv(filepath_or_buffer=self.__outputCsv,sep=";")

        df3=pd.merge(df1,df2,on=["tron"],how="outer")
        print (df3)
        df3.to_csv(path_or_buf="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/test_grid_01/peppe.csv",sep=";")
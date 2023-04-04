import os.path
import sys
import pandas as pd
import numpy as np

class MergeTable:
    def __init__(self,run,config):
        self.__run=run
        self.__config=config

    def compute (self):
        if self.__run:
            self.__config.logger.log(cl=self,method=sys._getframe(),message="start merge table")
            fileCsv=self.__createCsvFromMod(inputFile=self.__config.outputPhemMod,newExt=".csv")
            df_trj=pd.read_csv(self.__config.pathTrajMerged)
            df_mod=pd.read_table(fileCsv,header=3,skiprows=0,sep=",").dropna()

#            list_df_mod=self.__splitDf("VehNr: 6928,Input File: LB_EU5_SCR.GEN",df_mod)
#             list_df_trj=self.__splitDf("veh 0",df_trj)
#             dic_df_trj=self.__getDic(list_df_trj,"id")

            for date, row in df_mod.T.items():
                print (str(row[0]))
               # print (row,type(row),type(row[0]))
                if "VehNr:" in str(row[0]) :print ("ciao",row,type(row),type(row[0]))

            self.__config.logger.log(cl=self,method=sys._getframe(),message="finish merge table")

    def __getDic(self,listDf,key):
        dic={}
        for df in listDf:                listDf[df[key][0]]=df
        return dic
    def __splitDf(self,field_to_search,df):
        list_df=[]
        header_indices = df.index[pd.to_numeric(df[field_to_search], errors='coerce').isna()].tolist()
        header_indices.append(df.shape[0] + 1)
        # Preallocate output df list with the first chunk (using existing headers).
        list_of_dfs = [df.iloc[0:header_indices[0]]]

        if len(header_indices) > 1:
            for idx in range(len(header_indices) - 1):
                # Extract new header
                header_index = header_indices[idx]
                next_header_index = header_indices[idx + 1]
                current_header = df.iloc[[header_index]].values.flatten().tolist()

                # Make a df from this chunk
                current_df = df[header_index + 1:next_header_index]
                # Apply the new header
                current_df.columns = current_header
                current_df.reset_index(drop=True, inplace=True)
                list_of_dfs.append(current_df)

        # Show output
#        for df_index, current_df in enumerate(list_of_dfs):    print("DF chunk index: {}".format(df_index))            # print(current_df)
        return list_of_dfs

    def delete_empty_rows(file_path, new_file_path):
        data = pd.read_csv(file_path, skip_blank_lines=True)
        data.dropna(how="all", inplace=True)
        data.to_csv(new_file_path, header=True)

    def __createCsvFromMod(self,inputFile,newExt):
        self.__config.logger.log(cl=self,method=sys._getframe(),message="create csv")
        name,ext=os.path.splitext(inputFile)
        newName=name+newExt
        os.system("cp "+self.__config.outputPhemMod+" "+newName)
        return newName
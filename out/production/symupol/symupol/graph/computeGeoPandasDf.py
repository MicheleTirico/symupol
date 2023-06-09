import sys
import pandas as pd
from shapely.geometry import LineString,Point
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

class ComputeGeoPandasDf:
    def __init__(self,graph):
        self.__graph=graph
        self.__graph.logger.log(cl=self,method=sys._getframe(),message="initialize geopandas dataframe")

    def setPathOutputJpg(self,path):    self.pathOutputJpg=path

    def getGenericGraph(self,run,saveJpg,pathJpg):
        if run:
            self.__graph.logger.log(cl=self,method=sys._getframe(),message="start  geopandas dataframe")
            coord_in=self.__graph.df["coord_in"].str.split(" ").apply(pd.Series,1).astype("float64")
            coord_out=self.__graph.df["coord_out"].str.split(" ").apply(pd.Series,1).astype("float64")
            # print (self.__graph.df["coord_int"])
            # coord_int=self.__graph.df["coord_int"].str.split(",").apply(pd.Series,1).astype("float64")

            self.__graph.df["n_in"] = list(zip(coord_in[0], coord_in[1]))
            self.__graph.df["n_out"] = list(zip(coord_out[0], coord_out[1]))
            # self.__graph.df["n_int"] = list(zip(coord_int[0], coord_int[1]))

            self.__graph.df['n_in_geometry'] = self.__graph.df["n_in"].apply(lambda x: Point((x[0], x[1])))
            self.__graph.df['n_out_geometry'] = self.__graph.df["n_out"].apply(lambda x: Point((x[0], x[1])))
            # self.__graph.df['n_int_geometry'] = self.__graph.df["n_int"].apply(lambda x: Point((x[0], x[1])))

            self.__graph.df['Line_geometry'] = self.__graph.df.apply(lambda x: LineString([x['n_in'], x['n_out']]), axis=1)        # nx.draw(G)
            df1_geo = gpd.GeoDataFrame(self.__graph.df, crs = 'epsg:2154', geometry = self.__graph.df['Line_geometry'])

            if saveJpg:
                df1_geo.plot()
                # plt.show()
                plt.savefig(pathJpg)

            self.__graph.logger.log(cl=self,method=sys._getframe(),message="finish geopandas dataframe")

    def getChart_lms(self,ts,ts_chart,lms,indicator,saveJpg):
        self.__graph.logger.log(cl=self,method=sys._getframe(),message="get chart for the indicator: "+indicator+", ts:" +str(ts)+" and lms: "+str(lms) )
        pathSumPollutants=self.__graph.config.folder_output+self.__graph.config.scenario+'_ts-'+'{:0>4}'.format(ts)+'_lms-'+'{:0>4}'.format(lms)+'_gl.csv'

        df1=pd.read_csv(pathSumPollutants,sep=";")
        try:
            print (ts_chart)
            df1=df1[df1['pos_ts_{:0>4}'.format(ts)] ==ts_chart] # "'pos_ts_{:0>4}'.format(ts)
        except KeyError:
            return self.__graph.logger.warning(cl=self,method=sys._getframe(),message="get chart for the indicator: "+indicator+", ts:" +str(ts)+" and lms: "+str(lms), doQuit=False,doReturn=True)

        coord_in=df1["coord_in"].str.split(" ").apply(pd.Series,1).astype("float64")
        coord_out=df1["coord_out"].str.split(" ").apply(pd.Series,1).astype("float64")                                                                      # coord_int=df1["int_points"].str.split(" ").apply(pd.Series,1).astype("float64")

        df1["n_in"] = list(zip(coord_in[0], coord_in[1]))
        df1["n_out"] = list(zip(coord_out[0], coord_out[1]))                                                                                                # df1["n_int"] = list(zip(coord_int[0], coord_int[1]))

        df1['n_in_geometry'] = df1["n_in"].apply(lambda x: Point((x[0], x[1])))
        df1['n_out_geometry'] = df1["n_out"].apply(lambda x: Point((x[0], x[1])))                                                                           # df1['n_inter_geometry']=df1["int_points"].apply(lambda x: Point((x[0], x[1])))
        df1['Line_geometry'] = df1.apply(lambda x: LineString([x['n_in'], x['n_out']]), axis=1)                                                             # nx.draw(G)        # df1['Line_geometry'] = df1.apply(lambda x: LineString([x['n_in'], x['n_int'], x['n_out']]), axis=1)        # nx.draw(G)

        df1_geo = gpd.GeoDataFrame(df1, crs = 'epsg:2154', geometry = df1['Line_geometry'])
        df1_geo.plot(column=indicator)
        # plt.show()
        print (self.pathOutputJpg)
        if saveJpg:        plt.savefig(self.pathOutputJpg)


    def computeSingleGraph(self,ts,ts_chart,indicator_chart,saveJpg):

        """
        ts: time split for the analysis
        lms: max length of links for the analysis
        ts_chart: position of the time split to make chart
        indicator_chart: which indicator should create the chart
        """
        self.__graph.logger.log(cl=self,method=sys._getframe(),message="compute the graph for time slot: "+str(ts) )

        df1=self.__graph.df[self.__graph.df['ts-{:0>4}'.format(ts)] == ts_chart]
        # df1=self.__graph.df
        print (df1)
        coord_in=df1["coord_in"].str.split(" ").apply(pd.Series,1).astype("float64")
        coord_out=df1["coord_out"].str.split(" ").apply(pd.Series,1).astype("float64")                                                                      # coord_int=df1["int_points"].str.split(" ").apply(pd.Series,1).astype("float64")

        df1["n_in"] = list(zip(coord_in[0], coord_in[1]))
        df1["n_out"] = list(zip(coord_out[0], coord_out[1]))                                                                                                # df1["n_int"] = list(zip(coord_int[0], coord_int[1]))

        df1['n_in_geometry'] = df1["n_in"].apply(lambda x: Point((x[0], x[1])))
        df1['n_out_geometry'] = df1["n_out"].apply(lambda x: Point((x[0], x[1])))                                                                           # df1['n_inter_geometry']=df1["int_points"].apply(lambda x: Point((x[0], x[1])))
        df1['Line_geometry'] = df1.apply(lambda x: LineString([x['n_in'], x['n_out']]), axis=1)                                                             # nx.draw(G)        # df1['Line_geometry'] = df1.apply(lambda x: LineString([x['n_in'], x['n_int'], x['n_out']]), axis=1)        # nx.draw(G)

        df1_geo = gpd.GeoDataFrame(df1, crs = 'epsg:2154', geometry = df1['Line_geometry'])
        df1_geo.plot()#(column=indicator_chart)
        # plt.show()
        print (self.pathOutputJpg)
        if saveJpg:        plt.savefig(self.pathOutputJpg)
        # df1.to_csv("/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/lafayette_test.csv",sep=";")


    def test(self):
        pathIn=self.__graph.setPathInputTsSl

        print (pathIn)
        df=pd.read_csv(pathIn,sep=",")
        print(df)

        df.info()

        new_idx=list(df["tron"])
        new_idx=list(dict.fromkeys(new_idx))
        new_idx=pd.Index(new_idx)
        # print (new_idx)
        cols=list(dict.fromkeys(list(df["nSplit_5"])))
        # print (cols)
        # df2 = df.pivot(index=new_idx, columns=cols, values='FC')


        idx = pd.MultiIndex.from_product([[0, 1, 2], ['a', 'b', 'c', 'd']])
        df = pd.DataFrame({'value' : np.arange(12)}, index=idx)
        print (df)

        # pd.crosstab(df.index.get_level_values(0),df.index.get_level_values(1),values=df.value,aggfunc=np.sum)
        df.pivot_table(values="value", index=df.index.get_level_values(0), columns=df.index.get_level_values(1))

        print (df)
        quit()
        df3 =df.unstack(1)
        df3.columns =df3.columns.droplevel(0)
        print(df3)
        df3.info()
        df3.to_csv("/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/lafayette/test.csv")
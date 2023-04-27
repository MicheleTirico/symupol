import sys
import pandas as pd
from shapely.geometry import LineString,Point
import geopandas as gpd
import numpy as np

class ComputeGeoPandasDf:
    def __init__(self,graph):
        self.__graph=graph
        self.__graph.logger.log(cl=self,method=sys._getframe(),message="initialize geopandas dataframe")

    def compute(self):
        self.__graph.logger.log(cl=self,method=sys._getframe(),message="start  geopandas dataframe")

        coord_in=self.__graph.df["coord_in"].str.split(" ").apply(pd.Series,1).astype("float64")
        coord_out=self.__graph.df["coord_out"].str.split(" ").apply(pd.Series,1).astype("float64")
        self.__graph.df["n_in"] = list(zip(coord_in[0], coord_in[1]))
        self.__graph.df["n_out"] = list(zip(coord_out[0], coord_out[1]))
        self.__graph.df['n_in_geometry'] = self.__graph.df["n_in"].apply(lambda x: Point((x[0], x[1])))
        self.__graph.df['n_out_geometry'] = self.__graph.df["n_out"].apply(lambda x: Point((x[0], x[1])))
        self.__graph.df['Line_geometry'] = self.__graph.df.apply(lambda x: LineString([x['n_in'], x['n_out']]), axis=1)        # nx.draw(G)
        self.__graph.df_geo = gpd.GeoDataFrame(self.__graph.df, crs = 'epsg:2154', geometry = self.__graph.df['Line_geometry'])

        self.__graph.logger.log(cl=self,method=sys._getframe(),message="finish geopandas dataframe")


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
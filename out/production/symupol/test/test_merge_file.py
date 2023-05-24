import csv
import os
import sys
import pandas as pd

inputFile="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/test_grid_01/merged.csv"
outputFile="/media/mt_licit/data/licit_lab_dropbox/Michele Tirico/project/symupol/outputs/test/network.csv"

print ("read df")
df=pd.read_csv(filepath_or_buffer=inputFile,sep=";")
print ("start group by")
a=df.groupby(['t','tron','dist'])['FC'].sum()
print (a)
print ("start store")
a.to_csv(path_or_buf=outputFile,sep=";")


#!/usr/bin/env python3

# import the modules you need here
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import wget
import os
import numpy as np
import uptide
import pytz
import math
import glob

filename= "data/1947ABE.txt"
filename1="data/1946ABE.txt"

#open the file name and remove all unnecessary info
def read_tidal_data(filename):
#removing unnecessary information
    data=pd.read_csv(filename , sep=r"\s+", skiprows=[0,1,2,3,4,5,6,7,8,10]) 
#renaming the column as Sea Level
    data=data.rename(columns={data.columns[3] : 'Sea Level'})               
#combining the columsn data and time into one column
    data["Datetime"]= pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
#replace any value in Sea Level that contains M,N,T with Nan (number infront should disappear and M/N/T = Nan)
    data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True,inplace=True)

    return data



    



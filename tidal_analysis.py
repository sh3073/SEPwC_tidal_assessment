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

#open the file name and remove all unnecessary info
def read_tidal_data(filename):
#removing unnecessary information
    data=pd.read_csv(filename , sep="\s+", skiprows=[0,1,2,3,4,5,6,7,8,10]) 
#renaming the column as Sea Level
    data=data.rename(columns={data.columns[3] : 'Sea Level'})               
#combining the columsn data and time into one column
    data["Datetime"]= pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
#M,N,T is not actual data - replace any value in Sea Level that contains M,N,T with Nan (number infront should disappear and M/N/T = Nan)
    data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True,inplace=True)


    return data
    

def extract_section_remove_mean(start, end, data):


    return 


def join_data(data1, data2):

    return 



def sea_level_rise(data):

                                                     
    return 

def tidal_analysis(data, constituents, start_datetime):


    return 

def get_longest_contiguous_data(data):


    return 

#path = '/Users/hill93890/SEPwC_tidal_assessment/data/aberdeen'
#files = glob.glob(path +'/*.txt')
#i = 0
#for f in files:
#    print(read_tidal_data(f))
#    i = i+1
#    print(i)
    
    

#open all the file in aberdeen - not j 2000 
#the size needed = 8670 - number of data 


#print (read_tidal_data("data/aberdeen/2000ABE.txt"))

#if __name__ == '__main__':

    #parser = argparse.ArgumentParser(
                    # prog="UK Tidal analysis",
                     #description="Calculate tidal constiuents and RSL from tide gauge data",
                     #epilog="Copyright 2024, Jon Hill"
                    # )

   # parser.add_argument("directory",
    #                help="the directory containing txt files with data")
    #parser.add_argument('-v', '--verbose',
     #               action='store_true',
      #              default=False,
       #             help="Print progress")

#    args = parser.parse_args()
 #   dirname = args.directory
  #  verbose = args.verbose
    
    #glob = cycle thru the data - give it the path
    
    



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  7 11:06:52 2024

@author: hill93890
"""

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
    data=pd.read_csv(filename , sep="\s+", skiprows=[0,1,2,3,4,5,6,7,8,10]) 
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

#-###########################################################################3


def test_extract_year(self):
   
#this is from test_tides

      gauge_files = ["data/1946ABE.txt", "data/1947ABE.txt"]
  #data1 = 1947, data2 = 1946
      data1 = pd.read_csv(gauge_files[1])
      data2 = pd.read_csv(gauge_files[0])
      combined_data = pd.concat([data1, data2], ignore_index=True)
      data = combined_data
        

def test_extract_single_year(year, data):
#testinf for the year 1947
      #year1947 = extract_single_year_remove_mean("1947",data)
      global year_data
      year_string_start = str(year)+"0101"
      year_string_end = str(year)+"1231"
      year_data = data.loc[year_string_start:year_string_end, ['Sea Level']]
    
      year_data=year_data.apply(pd.to_numeric, errors="raise")
      year_data= (year_data)-(year_data["Sea Level"].mean())
      print(year_data)
      
      return year_data
    
 
#def test_extract_single_year_in_the_minicourse
 #    year_string_start = str(year)+"0101"
 #    year_string_end = str(year)+"1231"
 #    year_data = data.loc[year_string_start:year_string_end, ['Tide']]
    # remove mean to oscillate around zero
 #    mmm = np.mean(year_data['Tide'])
 #    year_data['Tide'] -= mmm

 #    return year_data     
      
      
      
  #renaming the column as Sea Level for year1947
      data=data.rename(columns={data.columns[3] : 'Sea Level'})
  #combining the columsn data and time into one column for year1947
      data["Datetime"]= pd.to_datetime(data['Date'] + ' ' + data['Time'])
      data = data.set_index("Datetime")    
      #check is sea level size is 8760

   #   mean = np.mean(year1947['Sea Level'])
        # check mean is near zero
     # assert mean == pytest.approx(0)

 # check something sensible when a year is given that doesn't exist
        # check something sensible when a year is given that doesn't exist
      return year_data
  
    
  
   #original# 
  
  #  def test_extract_year(self):
        
  #      gauge_files = ['data/1946ABE.txt', 'data/1947ABE.txt']

  #      data1 = read_tidal_data(gauge_files[1])
  #      data2 = read_tidal_data(gauge_files[0])
  #      data = join_data(data1, data2)
        
   #     year1947 = extract_single_year_remove_mean("1947",data)
  #      assert "Sea Level" in year1947.columns
  #      assert type(year1947.index) == pd.core.indexes.datetimes.DatetimeIndex
  #      assert year1947['Sea Level'].size == 8760

  #      mean = np.mean(year1947['Sea Level'])
        # check mean is near zero
  #      assert mean == pytest.approx(0)

        # check something sensible when a year is given that doesn't exist
#-------------------------
def join_data(data1, data2):
    gauge_files = ['data/1946ABE.txt', 'data/1947ABE.txt']

    data1 = read_tidal_data(gauge_files[1])
    data2 = read_tidal_data(gauge_files[0])
#data1 = 1947, data2 = 1946
    data = join_data(data1, data2)
    
    #renaming the column as Sea Level for data 
    data=data.rename(columns={data.columns[3] : 'Sea Level'})
#combining the columsn data and time into one column for year1947
    data["Datetime"]= pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime") 
#    assert data['Sea Level'].size == 8760*2

    # check sorting (we join 1947 to 1946, but expect 1946 to 1947)
    assert data.index[0] == pd.Timestamp('1946-01-01 00:00:00')
    assert data.index[-1] == pd.Timestamp('1947-12-31 23:00:00')

    # check you get a fail if two incompatible dfs are given
    data2.drop(columns=["Sea Level","Time"], inplace=True)
    data = join_data(data1, data2)    

    return data

#-------------------------------------------------------------

def extract_section_remove_mean(start, end, data):
    
      gauge_files = ['data/1946ABE.txt', 'data/1947ABE.txt']

      data1 = read_tidal_data(gauge_files[1])
      data2 = read_tidal_data(gauge_files[0])
      data = join_data(data1, data2)
      
      year1946_47 = extract_section_remove_mean("19461215", "19470310", data)
#renaming the column as Sea Level for year1947
      data=data.rename(columns={data.columns[3] : 'Sea Level'}) 
#combining the columsn data and time into one column for year1947
      data["Datetime"]= pd.to_datetime(data['Date'] + ' ' + data['Time'])
      data = data.set_index("Datetime") 
    #check is sea level size is 2064

      mean = np.mean(year1946_47['Sea Level'])
      # check mean is near zero
   #   assert mean == pytest.approx(0)

      data_segment = extract_section_remove_mean("19470115", "19470310", data1)
      assert "Sea Level" in data_segment.columns
      assert type(data_segment.index) == pd.core.indexes.datetimes.DatetimeIndex
      assert data_segment['Sea Level'].size == 1320

      mean = np.mean(data_segment['Sea Level'])
      # check mean is near zero
 #     assert mean == pytest.approx(0)

      # check something sensible is done when dates are formatted correctly.    
    
      return 


#-------------------------------------------------------------

def sea_level_rise(data):
    #the test is correct_tides
    
    gauge_files = ['data/1946ABE.txt', 'data/1947ABE.txt']
    data1 = read_tidal_data(gauge_files[1])
    data2 = read_tidal_data(gauge_files[0])
    data = join_data(data1, data2)

    data_segment =extract_section_remove_mean("19460115", "19470310", data)

    constituents  = ['M2', 'S2']
    tz = pytz.timezone("utc")
    start_datetime = datetime.datetime(1946,1,15,0,0,0, tzinfo=tz)
    amp,pha = tidal_analysis(data_segment, constituents, start_datetime)

# for Aberdeen, the M2 and S2 amps are 1.307 and 0.441
    #assert amp[0] == pytest.approx(1.307,abs=0.1)
#M2 data = 1.307
    A_m2 = 0.53
    B_m2 = 12.4206012 # hours
    C_m2 = 0

    times = np.arange(0,24*14,0.5) # 14 days in hours
    sin_curve = A_m2*np.sin(2*math.pi/B_m2*times + C_m2)

    plt.plot(times,sin_curve)
    plt.xlabel("Hours")
    plt.ylabel("Water height (m)")
    plt.show()
#    assert amp[1] == pytest.approx(0.441,abs=0.1)
#S2 data = 0.441

    A_s2 = 0.23
    B_s2 = 12
    C_s2 = math.pi/2

    sin_curve = A_m2*np.sin(2*math.pi/B_m2*times + C_m2) + \
        A_s2*np.sin(2*math.pi/B_s2*times + C_s2)
    plt.plot(times,sin_curve)
    plt.xlabel("Hours")
    plt.ylabel("Water height (m)")
    plt.show()

                                                     
    return 
#-----------------------------------------------------------------------------------------------------

def tidal_analysis(data, constituents, start_datetime):
    # the test is lint(self):
    files =  ["tidal_analysis.py"]
    #pylint_options = ["--disable=line-too-long,import-error,fixme"]
    pylint_options = []

 #   report = CollectingReporter()
 #   result = Run(
 #               files,
 #               reporter=report,
  #              exit=False,
   #         )
 #   score = result.linter.stats.global_note
  #  nErrors = len(report.messages)

  #  print("Score: " + str(score))
  #  line_format = "{path}:{line}:{column}: {msg_id}: {msg} ({symbol})"
 #   for error in report.messages:
  #      print(line_format.format(**asdict(error)))   

  #  assert nErrors < 500
  ##  assert nErrors < 400
  #  #assert nErrors < 250
 #  # assert nErrors < 100
  #  assert nErrors < 50
   # assert nErrors < 10
    #assert nErrors == 0
    #assert score > 3
  #  assert score > 5
   # assert score > 7
 #   assert score > 9  

  #  return 

def get_longest_contiguous_data(data):
# test_linear_regression(self):

     gauge_files = ['data/1946ABE.txt', 'data/1947ABE.txt']
     data1 = read_tidal_data(gauge_files[1])
     data2 = read_tidal_data(gauge_files[0])
     data = join_data(data1, data2)

     slope, p_value = sea_level_rise(data)
     
     assert slope == pytest.approx(2.94e-05,abs=1e-7)
     assert p_value == pytest.approx(0.427,abs=0.1)
     

  #  return 


     
 
    
class TestRegression():

    def test_whitby_regression(self):

        from subprocess import run
        result = run(["python3","tidal_analysis.py","-v","data/whitby"], capture_output=True, check=True)
        assert len(result.stdout) > 25

    def test_aberdeen_regression(self):

        from subprocess import run
        result = run(["python3","tidal_analysis.py","--verbose","data/aberdeen"], capture_output=True, check=True)
        assert len(result.stdout) > 25

    def test_dover_regression(self):

        from subprocess import run
        result = run(["python3","tidal_analysis.py","data/dover"], capture_output=True, check=True)
        assert len(result.stdout) > 25


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
    

    
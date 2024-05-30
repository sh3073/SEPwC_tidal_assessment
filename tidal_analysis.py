# import the modules you need here
"""Module providing a tidal analysis on tidal data."""
import datetime
import glob
import argparse
import pandas as pd
import numpy as np
import uptide
#import pytz
from scipy.stats import linregress
import matplotlib.dates as enddates

#open the file name and remove all unnecessary info
def read_tidal_data(filename):
    """Opens the specified file, 1947, and filtering the data"""
#removing unnecessary information
    data=pd.read_csv(filename , sep=r"\s+", skiprows=[0,1,2,3,4,5,6,7,8,10])
#renaming the column as Sea Level
    data=data.rename(columns={data.columns[3] : 'Sea Level'})
#combining the column data and time into one column
    data["Datetime"]= pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
#dropping columns as we aren't using them
    data=data.drop(columns=['Date', 'Cycle','Residual'])
#replace M,N,T with Nan in Sea Level (number infront should disappear)
    data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    #convert sea level values from strings to floats
    data["Sea Level"]=data["Sea Level"].astype(float)
    return data

def extract_single_year_remove_mean(year, data):
    """Opens the specified file and removing the mean from the year"""
#https://www.w3schools.com/python/python_variables_global.asp
#year starts on the 1st of Jan and ends on the 31st of Dec
#month then day
    year_string_start = str(year)+"0101"
    year_string_end = str(year)+"1231"
    year_data = data.loc[year_string_start:year_string_end, ['Sea Level']]
    year_data=year_data.apply(pd.to_numeric, errors="raise")
#removing the mean value
    year_data= (year_data)-(year_data["Sea Level"].mean())
    return year_data

def extract_section_remove_mean(start, end, data):
    """Opens the specified file and removing the mean from the section"""
#same concept as single_year_remove_mean
    section_start = str(start)
    section_end = str(end)
    section_data = data.loc[section_start:section_end,['Sea Level']]
    section_data = section_data.apply(pd.to_numeric,errors="raise")
    section_data= (section_data)-(section_data["Sea Level"].mean())
    return section_data

def join_data(data1, data2):
    """Combining data in ascending year (1946 & 1947)"""
#data1 = 1947, data2 = 1946
#uhttps://www.geeksforgeeks.org/python-pandas-merging-joining-and-concatenating/
#https://www.geeksforgeeks.org/how-to-sort-pandas-dataframe/
    data = pd.concat([data1, data2])
#data for ['Sea Level'].size == 8760*2 = 17,520
#sorting the columns with 1946 then 1947 in ascending order of year and dates by "Datetime"
    data=data.sort_values(by='Datetime',ascending=True)
#https://www.geeksforgeeks.org/how-to-sort-pandas-dataframe/
    return data

def sea_level_rise(data):
    """Creating our sea level to date2num based on 1970"""
#remove NaN values in Sea Level again
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
    data = data.dropna(subset=['Sea Level'])
#stats lin regress turning the index the num
#converting Datetime to num with 1970 as the base year using date2num
#x values are Time (date2num values)
#y values are the Sea Level values
#https://matplotlib.org/stable/api/dates_api.html#matplotlib.dates.date2num
    x = enddates.date2num(data.index)
    y = data['Sea Level'].values
    print(x,y)
#https://www.w3schools.com/python/python_ml_linear_regression.asp
# "_" removes unused data
    slope, _intercept, _r, p, _std_err =linregress(x, y)
    #tidalmodel temp - scripts - analyse tides.py
    return slope, p
   #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html

def tidal_analysis(data, constituents, start_datetime):
    """Creating our tidal constituents using amplitudes and phases"""
# we create a Tides object with a list of the consituents we want
#arranging it in chronological order
#removing Nan values and 15 jan and 10 of mar
    data = data.dropna(subset=['Sea Level'])
    print("HERE")
 #   data = data.drop(index=['1946-01-15 00:00:00', '1947-03-10 00:00:00'])
    print(data)
# We then set out start time. All data must then be in second since this time
    tide = uptide.Tides(constituents)
#use the start_datetime to use it for any data file in aberdeen, dover, whitby
    tide.set_initial_time(start_datetime)
    print(tide.f)
    #print (tide.set_initial_time)
    #  data=pd.date_range(start_datetime='1946,1,1,0,0,0', end_datetime='1947,12,31,0,0,0')
  #  data= pd.date_range(start=pd.to_datetime("01151946"),end=pd.to_datetime("12311947")
#    tide.set_end_time(datetime.datetime(1947,12,31,0,0,0))

# lets change our dates into seconds using 1e9 (int64 secs epoch in numpy)
# We then send the elevation data (our tides) and time in seconds to uptide
# and do the harmonic analysis

    secs = (data.index.astype('int64').to_numpy() / 1e9) - start_datetime.timestamp()

#issue is with this line
    print(tide.f)
    amp, pha = uptide.harmonic_analysis(tide, data["Sea Level"].to_numpy(), secs)
    print(amp, pha)
    #print(uptide.select_constituents(constituents,365*24*60*60)) # This is 365 days in seconds
    #tide = uptide.Tides(constituents)
    #print(tide.get_minimum_Rayleigh_period()/86400.)
    return (amp,pha)

def get_longest_contiguous_data(data):
    data=np.append(np.nan, np.append(data, np.nan))
    nv = np.where(np.isnan(data))[0]
    nvs = np.diff(nv).argmax()
    return nv[[nvs, nvs+1]]+np.array([0,-2])
    #numpy version
    
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
                     prog="UK Tidal analysis",
                     description="Calculate tidal constiuents and RSL from tide gauge data",
                     epilog="Copyright 2024, Jon Hill"
                     )

    parser.add_argument("directory",
                        help="the directory containing txt files with data")
    parser.add_argument('-v', '--verbose',
                    action='store_true',
                    default=False,
                    help="Print progress")

    args = parser.parse_args()
    dirname = args.directory
    verbose = args.verbose
#https://www.geeksforgeeks.org/how-to-pass-a-list-as-a-command-line-argument-with-argparse/
#printed out the arguments
#    print ("args.directory","args.verbose")
#----------------------------------------
# Listing the path for all files in the data directory (dirname)
#https://docs.python.org/3/library/glob.html
#choosing files that end with txt

#dirname = args.directory - the directory name
#A_data_files = glob.glob("data/aberdeen/*.txt")
#globs in the directory you want
    all_files = glob.glob(str(dirname)+ "/*.txt")
# Initialize an empty DataFrame to store data
    formatted_files = []
#for loop that runs through the aberdeen file    
for file in all_files:
 #calls the formattinf unction - read tidal data and gives the first file an       
    format_file = read_tidal_data(file)
#appends it to the empty list (empty list now contains the year 2000 from aberdeen)
    formatted_files.append(format_file)

    
    full_file = join_data(formatted_files[0], formatted_files[1])

#python while loop under "python:the fundamentals" - runs through all files from dirname/ aberdeen 
    COUNTER = 0
    while COUNTER < (len(formatted_files)):
        full_file = join_data(full_file, formatted_files[COUNTER])
        COUNTER = COUNTER + 1
        print(full_file)
    
#    print(data_files)
         
#printing out the station name based on the dirname directory
#print("Station Name: " + (dirname))
#printing out the M2 Amplitude  based on the dirname directory
#create a new variable 
    print (tidal_analysis(full_file, ['M2'], datetime.datetime(2000, 1, 1,0,0,0)))
#printing out the S2 Amplitude  based on the dirname directory
    print (tidal_analysis(full_file, ['S2'], datetime.datetime(2000, 1, 1,0,0,0)))
#printing out the Sea_Level rise based on the dirname directory
    print(sea_level_rise(full_file))
    
    
#printing out the longest_contiguous_data based on the dirname directory
    print ("Longest contiguous data: ")
    print (" ")
    df = full_file["Sea Level"]
    range_df = get_longest_contiguous_data(df)
    RANGE_DF_STR = str(range_df)
    RANGE_DF_STR = RANGE_DF_STR [1:-1]
    RANGE_DF_STR = RANGE_DF_STR.SPLIT()
    start_df = int(RANGE_DF_STR[0])
    end_df = int(RANGE_DF_STR[1])
    print(full_file[start_df:end_df])

    
    
    
    print(get_longest_contiguous_data(full_file))


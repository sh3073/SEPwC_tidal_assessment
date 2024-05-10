# import the modules you need here
"""Module providing a tidal analysis on tidal data."""
import pandas as pd
import numpy as np
import uptide 
import pytz
from scipy.stats import linregress

#open the file name and remove all unnecessary info
def read_tidal_data(filename):
    """Opens the specified file, 1947, and filtering the data"""
#removing unnecessary information
    data=pd.read_csv(filename , sep=r"\s+", skiprows=[0,1,2,3,4,5,6,7,8,10])
#renaming the column as Sea Level
    data=data.rename(columns={data.columns[3] : 'Sea Level'})
#combining the columsn data and time into one column
    data["Datetime"]= pd.to_datetime(data['Date'] + ' ' + data['Time'])
    data = data.set_index("Datetime")
#replace M,N,T with Nan in Sea Level (number infront should disappear)
    data.replace(to_replace=".*M$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    data.replace(to_replace=".*N$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    data.replace(to_replace=".*T$",value={"Sea Level": np.nan}, regex=True,inplace=True)
    return data

def extract_single_year_remove_mean(year, data):
    """Opens the specified file and removing the mean from the year"""
#testinf for the year 1947
    # year1947 = extract_single_year_remove_mean("year",data)
    #the global variable accesses info outside and inside the function
    #https://www.w3schools.com/python/python_variables_global.asp
   # global year_data
    year_string_start = str(year)+"0101"
    year_string_end = str(year)+"1231"
    year_data = data.loc[year_string_start:year_string_end, ['Sea Level']]
    year_data=year_data.apply(pd.to_numeric, errors="raise")
    year_data= (year_data)-(year_data["Sea Level"].mean())
    return year_data

def extract_section_remove_mean(start, end, data):
    """Opens the specified file and removing the mean from the section"""
   # global section_data
    section_start = str(start)
    section_end = str(end)
    section_data = data.loc[section_start:section_end, ['Sea Level']]
    section_data = section_data.apply(pd.to_numeric, errors="raise")
    section_data= (section_data)-(section_data["Sea Level"].mean())
    return section_data

def join_data(data1, data2):
    """Combining data in ascending year (1946 & 1947)"""
    print(data1)
    #gauge_files = ["data/1946ABE.txt", "data/1947ABE.txt"]
#data1 = 1947, data2 = 1946
    #data1 = pd.read_csv(gauge_files[1])
    #data2 = pd.read_csv(gauge_files[0])
    #url = https://www.geeksforgeeks.org/python-pandas-merging-joining-and-concatenating/
    #url : https://www.geeksforgeeks.org/how-to-sort-pandas-dataframe/
    data = pd.concat([data1, data2])
#data for ['Sea Level'].size == 8760*2 = 17,520
    print(data)
    #sorting the columns with 1946 then 1947 in ascending order of year and dates by "Datetime"
    data=data.sort_values(by='Datetime',ascending=True)
    #url : https://www.geeksforgeeks.org/how-to-sort-pandas-dataframe/
  #  data=data.index[0] == pd.Timestamp('1946-01-01 00:00:00')
  #  data = data.index[-1] == pd.Timestamp('1947-12-31 23:00:00')
  #  data2 = pd.Timestamp("1946-01-01 00:00:00")
 #   data1 = pd.Timestamp('1947-12-31 23:00:00')
    # check you get a fail if two incompatible dfs are given
   # data2.drop(columns=["Sea Level","Time"], inplace=True)
 #   data = join_data(data1, data2)
    return data

def sea_level_rise(data):
#1946 data for aberdeen 
#remove nan
#https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
    data = data.dropna(subset=['Sea Level'])
    return data
    print(data)
 #remove the mean (section mean)   
    section_data= (section_data)-(section_data["Sea Level"].mean())
#stats lin regress turning the index the num
    x = ['Sea Level']
    y = ['section_data']
#https://www.w3schools.com/python/python_ml_linear_regression.asp
   slope, intercept, r, p, std_err = stats.linregress(x, y)
   #https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.linregress.html
   scipy.stats.linregress(x, y, alternative='greater')

def myfunc(x):
   return slope * x + intercept

mymodel = list(map(myfunc, x))

plt.scatter(x, y)
plt.plot(x, mymodel)
plt.show()
 #    date2num in matplot loop

 
#The `scipy.stats' module can do the linear regression to work out sea-level rise. You may find it easier to work out the rise per day and multiply by 365 to get metres per year.
#line of best fit 
#    data=([datatime.time(1946,01,01, 00,00,00), datetime.time(1946,01,01, 23:00:00)])
 #   data=rise per day*365
#    return
      
def tidal_analysis(data, constituents, start_datetime):
    """Creating our tidal analysis with 3 components"""
# More on uptide: https://github.com/stephankramer/uptide

# we create a Tides object with a list of the consituents we want.
    data = uptide.Tides(['M2'])
# We then set out start time. All data must then be in second since this time
    data=data_tide.set_initial_time(Datetime.Datetime(1946,1,1,0,0,0))
    
# so let's swap our dates for seconds since midnight 1/1/2008.
# Note the 1e9 (the int64 seconds epoch in numpy is multiplied by this for some reason)
    seconds_since = (data.index.astype('int64').to_numpy()/1e9) - datetime.datetime(1946,1,1,0,0,0).timestamp()
    amp,pha = uptide.harmonic_analysis(tide, FD_2008['Sea Level'].to_numpy()/1000, seconds_since)

# uptide returns the amplitudes as a list (in the order of the constiuents listed above) and the phases (in radians)
    print(amp, pha)

    return

def get_longest_contiguous_data(data):
    return

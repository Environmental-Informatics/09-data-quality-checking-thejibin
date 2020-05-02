#!/bin/env python
"""
Created on 2020-04-30
by Jibin Joseph -joseph57
Assignment 09 - Data Quality Checking
Revision 01-2020-05-01
Modified to add comments
"""
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def ReadData( fileName ):
    """This function takes a filename as input, and returns a dataframe with
    raw data read from that file in a Pandas DataFrame.  The DataFrame index
    should be the year, month and day of the observation.  DataFrame headers
    should be "Date", "Precip", "Max Temp", "Min Temp", "Wind Speed". Function
    returns the completed DataFrame, and a dictionary designed to contain all 
    missing value counts."""
    
    # define column names
    colNames = ['Date','Precip','Max Temp', 'Min Temp','Wind Speed']

    # open and read the file
    DataDF = pd.read_csv("DataQualityChecking.txt",header=None, names=colNames,  
                         delimiter=r"\s+",parse_dates=[0])
    DataDF = DataDF.set_index('Date')
    
    # define and initialize the missing data dictionary
    ReplacedValuesDF = pd.DataFrame(0, index=["1. No Data"], columns=colNames[1:])
     
    return( DataDF, ReplacedValuesDF )
 
def Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF ):
    """This check replaces the defined No Data value with the NumPy NaN value
    so that further analysis does not use the No Data values.  Function returns
    the modified DataFrame and a count of No Data values replaced."""
    
    ## Replace all values of -999 with NumPy NaN values
    DataDF[DataDF==-999.00]=np.nan
    ## For several columns, sum to count the NaN values
    ReplacedValuesDF.loc['1. No Data',:]=DataDF.isna().sum()

    return( DataDF, ReplacedValuesDF )
    
def Check02_GrossErrors( DataDF, ReplacedValuesDF ):
    """This function checks for gross errors, values well outside the expected 
    range, and removes them from the dataset.  The function returns modified 
    DataFrames with data the has passed, and counts of data that have not 
    passed the check."""
 
    ## Applying the threshold
    DataDF.Precip[(DataDF['Precip']<0) | (DataDF['Precip']>25)]=np.nan
    DataDF['Max Temp'][(DataDF['Max Temp']<-25)|(DataDF['Max Temp']>35)]=np.nan
    DataDF['Min Temp'][(DataDF['Min Temp']<-25)|(DataDF['Min Temp']>35)]=np.nan
    DataDF['Wind Speed'][(DataDF['Wind Speed']<0)|(DataDF['Wind Speed']>10)]=np.nan
    ReplacedValuesDF.loc['2. Gross Error',:]=DataDF.isna().sum()-ReplacedValuesDF.sum()
    
    return( DataDF, ReplacedValuesDF )
    
def Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture is less than
    minimum air temperature, and swaps the values when found.  The function 
    returns modified DataFrames with data that has been fixed, and with counts 
    of how many times the fix has been applied."""
    
    ## Count the instances when min temp is greater than maz temp
    count_swap=len(DataDF.loc[DataDF['Min Temp']>DataDF['Max Temp']])
    ## swap the min and max temp temperature
    DataDF.loc[DataDF['Min Temp']>DataDF['Max Temp'],['Min Temp','Max Temp']]=\
              DataDF.loc[DataDF['Min Temp']>DataDF['Max Temp'],['Max Temp','Min Temp']].values
    ## Add the count to the DataFrame
    ReplacedValuesDF.loc['3. Swapped']=[0,count_swap,count_swap,0]

    return( DataDF, ReplacedValuesDF )
    
def Check04_TmaxTminRange( DataDF, ReplacedValuesDF ):
    """This function checks for days when maximum air temperture minus 
    minimum air temperature exceeds a maximum range, and replaces both values 
    with NaNs when found.  The function returns modified DataFrames with data 
    that has been checked, and with counts of how many days of data have been 
    removed through the process."""
    
    ## Count the instances when the difference is greater than 25
    count_range=len(DataDF.loc[(DataDF['Max Temp']-DataDF['Min Temp']>25)])
    ## Replace it with NaN
    DataDF.loc[(DataDF['Max Temp']-DataDF['Min Temp']>25),['Min Temp','Max Temp']]=np.nan
    ReplacedValuesDF.loc['4. Range Fail',:]=[0,count_range,count_range,0]   

    return( DataDF, ReplacedValuesDF )
    

# the following condition checks whether we are running as a script, in which 
# case run the test code, otherwise functions are being imported so do not.
# put the main routines from your code after this conditional check.

if __name__ == '__main__':

    fileName = "DataQualityChecking.txt"
    DataDF, ReplacedValuesDF = ReadData(fileName)
    DataDF_original=DataDF
    
    ## Capture the original values to plot before correction and use later using figure numbering
    ## Precipitation Plot
    plt.figure(1)
    plt.plot(DataDF_original.index,DataDF_original['Precip'],label='Before Correction',color='red')
    ## Max Temp Plot
    plt.figure(2)
    plt.plot(DataDF_original.index,DataDF_original['Max Temp'],label='Before Correction',color='red')
    ## Min Temp Plot
    plt.figure(3)
    plt.plot(DataDF_original.index,DataDF_original['Min Temp'],label='Before Correction',color='red')
    ## Wind Speed Plot
    plt.figure(4)
    plt.plot(DataDF_original.index,DataDF_original['Wind Speed'],label='Before Correction',color='red')
    
    print("\nRaw data.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check01_RemoveNoDataValues( DataDF, ReplacedValuesDF )
    
    print("\nMissing values removed.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check02_GrossErrors( DataDF, ReplacedValuesDF )
    
    print("\nCheck for gross errors complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check03_TmaxTminSwapped( DataDF, ReplacedValuesDF )
    
    print("\nCheck for swapped temperatures complete.....\n", DataDF.describe())
    
    DataDF, ReplacedValuesDF = Check04_TmaxTminRange( DataDF, ReplacedValuesDF )
    
    print("\nAll processing finished.....\n", DataDF.describe())
    print("\nFinal changed values counts.....\n", ReplacedValuesDF)
    
    ## Precipitation Plot
    plt.figure(1)
    plt.plot(DataDF.index,DataDF['Precip'],label='After Correction',color='green')
    plt.xlabel('Date')
    plt.xticks(rotation=50)
    plt.ylabel('Plot of Precipitation (mm)')
    plt.title('Precipitation\n(Before and After Correction)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('A_Precipitation.jpg')
    plt.close(1)
    
    ## Maximum Precipitation Plot
    plt.figure(2)
    plt.plot(DataDF.index,DataDF['Max Temp'],label='After Correction',color='green')
    plt.xlabel('Date')
    plt.xticks(rotation=50)
    #plt.ylabel(r'Temperature ('$^0 C$')')
    plt.ylabel(r'$Temperature\ (^0 C)$')
    plt.title('Plot of Maximum Temperature\n(Before and After Correction)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('B_MaxTemp.jpg')
    plt.close(2)
    
    ## Minimum Precipitation Plot
    plt.figure(3)
    plt.plot(DataDF.index,DataDF['Min Temp'],label='After Correction',color='green')
    plt.xlabel('Date')
    plt.xticks(rotation=50)
    plt.ylabel(r'$Temperature\ (^0 C)$')
    plt.title('Plot of Minimum Temperature\n(Before and After Correction)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('C_MinTemp.jpg')
    plt.close(3)

    ## Wind Speed Plot
    plt.figure(4)
    plt.plot(DataDF.index,DataDF['Wind Speed'],label='After Correction',color='green')
    plt.xlabel('Date')
    plt.xticks(rotation=50)
    #plt.ylabel(r'Temperature ('$^0 C$')')
    plt.ylabel(r'$Wind\ Speed\ (m/s)$')
    plt.title('Plot of Wind Speed\n(Before and After Correction)')
    plt.legend()
    plt.tight_layout()
    plt.savefig('B_WindSpeed.jpg')
    plt.close(4)
    
    ## Output Data and Information
    DataDF.to_csv('data_qualitychecked.csv',sep=' ') ## Same format as input
    ReplacedValuesDF.to_csv('data_failed_check_info.csv',sep='\t') ## Delimiter is tab
    
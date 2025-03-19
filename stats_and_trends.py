# -*- coding: utf-8 -*-
"""
Created on Sun Mar 16 14:09:38 2025

@author: ropaf
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def read_data(filename, skip_rows=4):
    """
    Function will read the data in Worldbank format 
    process the data into two data frames

    Parameters
    ----------
    filename : str
        DESCRIPTION.

    Returns
    df_years_columns: pandas dataframe
    df_countries_columns : pandas dataframe

    """
    df = pd.read_csv(filename)
    df.columns = df.columns.astype(str)
    years_to_remove = [str(year) for year in range(1960, 1990)]  # List of years to drop
    df = df.drop(columns=years_to_remove, errors='ignore')  # Drop years with missing dat
    #to drop rows or columns with NaN values
    df_years_columns = df.dropna(subset=df.columns.difference(['Country Name']), axis=0, how='any')
    df_years_columns = df.set_index('Country Name')
    df_countries_columns = df.set_index('Country Name').T
    
    # Check if 'Country Name' is in the index
    print("Countries in the dataset:", df_years_columns.index.tolist()[:20])
    
    
    return df_years_columns, df_countries_columns

CO2_emissions = 'API_EN.GHG.CO2.IP.MT.CE.AR5_DS2_en_csv_v2_14525.csv'
ren_energy_use = 'API_EG.FEC.RNEW.ZS_DS2_en_csv_v2_4123.csv'

CO2_emissions_years, CO2_emissions_countries = read_data(CO2_emissions)
energy_use_years, energy_use_countries = read_data(ren_energy_use)

print('The columns are: ', CO2_emissions_countries.columns)

print(CO2_emissions_years.describe())
print(CO2_emissions_countries.describe())
print(energy_use_years.describe())
print(energy_use_countries.describe())

#%%

def correlation_calc(df_renewable, df_co2, countries, start_years, end_years):
    correlations = {}
    
    for country in countries:
        # Check if country exists in both DataFrames
        if country not in df_co2.index or country not in df_renewable.index:
            print(f"Data missing for country: {country}")
            continue
        
        # Extract data for the given years
        co2_country_data = df_co2.loc[country, start_years:end_years]
        renewable_country_data = df_renewable.loc[country, start_years:end_years]
        
        # Calculate the correlation using pandas .corr() method
        correlation = co2_country_data.corr(renewable_country_data)
        correlations[country] = correlation

    
    return correlations

selected_countries = ['United States', 'Greece', 'India', 'Brazil', 'Zimbabwe', 'Afghanistan']


energy_use_countries = energy_use_countries.set_index('Country Name')
CO2_emissions_countries = CO2_emissions_countries.set_index('Country Name')

# Check the index to make sure it's set properly
print('the first 20 countries' , energy_use_countries.index[:20])  # Display the first 20 countries in renewable dataset
print(CO2_emissions_countries[:20])  # Display the first 20 countries in CO2 emissions dataset

for country in selected_countries:
    if country in CO2_emissions_countries.index:
        print(f"{country} exists in CO2 dataset")
    else:
        print(f"{country} not found in CO2 dataset")
    if country in energy_use_countries.index:
        print(f"{country} exists in Renewable energy dataset")
    else:
        print(f"{country} not found in Renewable energy dataset")

# Renewable energy only has data from 1990, so we start from 1990
start_years = '1990'
end_years_early = '1999'
recent_years = [str(year) for year in range(2000, 2020)]
early_years = [str(year) for year in range(1990, 1999)]

correlation_early = correlation_calc(energy_use_countries, CO2_emissions_countries, selected_countries, start_years, end_years_early)
correlation_recent = correlation_calc(energy_use_countries, CO2_emissions_countries, selected_countries, recent_years[0], recent_years[-1])

# Display results
print('Correlation between CO2 emissions and Renewable energy use from 1990-1999: ')
for country, corr in correlation_early.items():
    print(f"{country}: {corr}")

print('Correlation between CO2 emissions and Renewable Energy Use from 2000-2020: ')
for country, corr in correlation_recent.items():
    print(f"{country}: {corr}")









        










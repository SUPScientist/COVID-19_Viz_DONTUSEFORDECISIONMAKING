#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:55:09 2020

Data from https://github.com/CSSEGISandData/COVID-19/
Already very clean, it appears, so not much more effort needed there.

curl -o Data/data_20200314.csv https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv

@author: pjb
"""

import pandas as pd
import numpy as np
import os

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# import seaborn as sns
# sns.set_context("notebook", font_scale=1.5, rc={"lines.linewidth": 2.5})

plt.close('all')
plt.style.use('seaborn-colorblind')
#%% Pull in data
filename = 'data_20200315.csv'
filepath = os.path.join('Data', filename)
df = pd.read_csv(filepath)

# Sum by country, get rid of summed, nonsensical lat/lon
df_countrySum = df.groupby('Country/Region').sum()
df_countrySum.drop(columns = ['Lat', 'Long'], inplace = True)

# Average by country to get mean lat/lon
df_countryLatLon = df.groupby('Country/Region').mean()
df_countryLatLon = df_countryLatLon[['Lat', 'Long']]

# Merge to get summed quantities and averaged locations
df_countrySum_goodLatLon = pd.merge(left = df_countrySum, right = df_countryLatLon,
                                    left_index=True, right_index=True)

# Make multiindex for easier manipulations below
df_countrySum_goodLatLon.set_index(['Lat', 'Long'], append = True, inplace = True)


# My brain can't handle dates in columns for some reason
df_T = df_countrySum_goodLatLon.transpose(copy = True)
df_T.fillna(method='ffill', inplace = True)
df_T.rename_axis('Dates', inplace = True)

# Put index into formatted time
df_T.index = pd.to_datetime(df_T.index)

#%% DF with top N case-afflicted countries
n_countries = 10

df_peak = df_T.max(axis = 0)

last_row = df_T.index[-1]

df_T_sorted = df_T.sort_values(by = last_row, axis = 1, ascending = False)
df_T_sorted_top = df_T_sorted.iloc[:, 0:n_countries]
#%% Plot
fig, axs = plt.subplots(figsize = (10, 8))

for i in range(n_countries):
    if i<6:
        axs.semilogy(df_T_sorted_top.iloc[:, i], 
                     '-o',
                     label = df_T_sorted_top.columns.get_level_values('Country/Region')[i])
    else:
        axs.semilogy(df_T_sorted_top.iloc[:, i], 
                     '-v',
                     label = df_T_sorted_top.columns.get_level_values('Country/Region')[i])

axs.set_ylabel('# Confirmed Cases')
fig.legend(loc = 'upper center')
fig.autofmt_xdate()
plt.tight_layout()
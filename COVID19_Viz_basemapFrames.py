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

#%% Basemap
plt.style.use('dark_background')
fig, axs = plt.subplots(figsize=(12, 7))
plt.axis('off')
axs = fig.add_axes([0.05, 0.05, 0.9, 0.85])
map1 = Basemap(projection='moll',lon_0=0)
# map1 = Basemap(llcrnrlon=-180,llcrnrlat=-70,urcrnrlon=180,urcrnrlat=70, epsg=4326)
map1.bluemarble()
# map1.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

#%% Add new data in loop
for i in range(len(df_T)):
    print("{} out of {}".format(i, len(df_T)))
    df_T_sub = df_T.iloc[i, :]
    date = df_T_sub.name
    df_T_sub.rename('Confirmed', inplace = True)
    df_T_sub_reset = df_T_sub.reset_index(level = ['Country/Region', 'Lat', 'Long'])
    
    lon = df_T_sub_reset['Long']
    lat = df_T_sub_reset['Lat']
    size = df_T_sub_reset['Confirmed']/50
    
    x, y = map1(list(lon), list(lat))
    
    sctr = axs.scatter(x, y, c='cyan', s=size, marker='o', edgecolor = 'white')
    
    axs.set_title(df_T.index[i].strftime('%d-%b-%Y'), fontsize = 20)

    plt.tight_layout()
    
    figname = 'Frames/daily_covid_{0:03d}.png'.format(i)
    plt.savefig(figname, dpi = 100)


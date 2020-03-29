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
filename = 'data_global.csv'
filepath = os.path.join('Data', filename)
df = pd.read_csv(filepath)

# Make multiindex for easier manipulations below
df.set_index(['Province/State', 'Country/Region', 'Lat', 'Long'], inplace = True)


# My brain can't handle dates in columns for some reason
df_T = df.transpose(copy = True)
df_T.fillna(method='ffill', inplace = True)
df_T.rename_axis('Dates', inplace = True)

# Put index into formatted time
df_T.index = pd.to_datetime(df_T.index)

#%% Basemap
plt.style.use('dark_background')
fig, axs = plt.subplots(figsize=(12, 7))
plt.axis('off')
axs = fig.add_axes([0.05, 0.05, 0.9, 0.85])
map1 = Basemap(llcrnrlon=-169,llcrnrlat=11,urcrnrlon=-52,urcrnrlat=72, epsg=4326)
map1.bluemarble()
# map1.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

#%% Add new data in loop
for i in range(len(df_T)):
    print("{} out of {}".format(i, len(df_T)))
    df_T_sub = df_T.iloc[i, :]
    date = df_T_sub.name
    df_T_sub.rename('Confirmed', inplace = True)
    df_T_sub_reset = df_T_sub.reset_index(level = ['Province/State', 'Country/Region', 'Lat', 'Long'])
    
    lon = df_T_sub_reset['Long']
    lat = df_T_sub_reset['Lat']
    size = df_T_sub_reset['Confirmed']/5
    
    x, y = map1(list(lon), list(lat))
    
    sctr = axs.scatter(x, y, c='cyan', s=size, marker='o', edgecolor = 'white')
    
    axs.set_title(df_T.index[i].strftime('%d-%b-%Y'), fontsize = 20)

    plt.tight_layout()
    
    figname = 'Frames_US/daily_covid_{0:03d}.png'.format(i)
    plt.savefig(figname, dpi = 100)


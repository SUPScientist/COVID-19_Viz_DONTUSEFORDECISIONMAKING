#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:55:09 2020

Data from https://github.com/CSSEGISandData/COVID-19/
Already very clean, it appears, so not much more effort needed there.

@author: pjb
"""

import pandas as pd
import numpy as np
import os

import plotly
# import chart_studio.plotly as py
import plotly.graph_objs as go
mapbox_access_token = os.environ['MY_MAPBOX_KEY']

#%% Pull in data
filename = 'data_20200314.csv'
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

#%% Start making simple figs
fig = go.Figure()
scale = 500
for i in range(len(df_T)):
    df_T_sub = df_T.iloc[i, :]
    date = df_T_sub.name
    df_T_sub.rename('Confirmed', inplace = True)
    df_T_sub_reset = df_T_sub.reset_index(level = ['Province/State', 'Country/Region', 'Lat', 'Long'])
    
    fig.add_trace(
        go.Scattergeo(
            locationmode = 'USA-states',
            lon = df_T_sub_reset['Long'],
            lat = df_T_sub_reset['Lat'],
            # text = df_T_sub['text'],
            marker = dict(
                size = df_T_sub_reset['Confirmed']/scale,
                line_color='rgb(40,40,40)',
                line_width=0.5,
                sizemode = 'area'
        )
    )
)


# fig.update_layout(
#     title_text = '2014 US city populations<br>(Click legend to toggle traces)',
#     showlegend = True,
#     geo = dict(
#         scope = 'usa',
#         landcolor = 'rgb(217, 217, 217)',
#     )
# )

figname = 'take0'
htmlname = os.path.join('Figures', figname+'.html')
plot_url = plotly.offline.plot(fig, filename=htmlname)

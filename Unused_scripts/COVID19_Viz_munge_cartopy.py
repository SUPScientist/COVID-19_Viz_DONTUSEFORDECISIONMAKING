#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 12:55:09 2020

Data from https://github.com/CSSEGISandData/COVID-19/
Already very clean, it appears, so not much more effort needed there.

Scattermapbox/plotly animation example from https://plot.ly/~empet/14825/scattermapbox-animation-forum-question/#/

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
df.dropna(axis=1, how = 'all', inplace = True)

df = df[0:6]

#%% Make multiindex for easier manipulations below
df.set_index(['Province/State', 'Country/Region', 'Lat', 'Long'], inplace = True)

# My brain can't handle dates in columns for some reason
df_T = df.transpose(copy = True)
df_T.fillna(method='ffill', inplace = True)
df_T.rename_axis('Confirmed', inplace = True)

# Put index into formatted time
df_T.index = pd.to_datetime(df_T.index)

#%%Initialize map
data = [go.Scattermapbox(
               lat=[0],
               lon=[0],
               mode='markers',
               marker=dict(size=5, color='red')
            )
        ]

layout = go.Layout(width=1200,
    autosize=True,
    hovermode='closest',
    mapbox=dict(accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(lat=20,
                            lon=0),
                pitch=0,
                zoom=1,
                style='light'
                )
            )

lats = df_T.columns.get_level_values('Lat')
lons = df_T.columns.get_level_values('Long')

#%% Determine frames
frames = [dict(data= [dict(type='scattermapbox',
                           lat=lats,
                           lon=lons,
               traces= [0],
               name='frame{}'.format(k)       
              ) for k in range(1, len(df))]

#%% Add slider
sliders = [dict(steps= [dict(method= 'animate',
                           args= [[ 'frame{}'.format(k) ],
                                  dict(mode= 'immediate',
                                  frame= dict( duration=100, redraw= True ),
                                           transition=dict( duration= 0)
                                          )
                                    ],
                            label='{:d}'.format(k)
                             ) for k in range(len(df))], 
                transition= dict(duration= 0 ),
                x=0,#slider starting position  
                y=0, 
                currentvalue=dict(font=dict(size=12), 
                                  prefix='Point: ', 
                                  visible=True, 
                                  xanchor= 'center'),  
                len=1.0)
           ]

layout.update(updatemenus=[dict(type='buttons', showactive=False,
                                y=0,
                                x=1.05,
                                xanchor='right',
                                yanchor='top',
                                pad=dict(t=0, r=10),
                                buttons=[dict(label='Play',
                                              method='animate',
                                              args=[None, 
                                                    dict(frame=dict(duration=1000, 
                                                                    redraw=True),
                                                         transition=dict(duration=200),
                                                         fromcurrent=True,
                                                         mode='immediate'
                                                        )
                                                   ]
                                             )
                                        ]
                               )
                          ],
              sliders=sliders);

fig=go.Figure(data=data, layout=layout, frames=frames)


figname = 'take0'
htmlname = os.path.join('Figures', figname+'.html')
plot_url = plotly.offline.plot(fig, filename=htmlname)

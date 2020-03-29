#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 19:08:42 2020

@author: pjb
"""

import subprocess
import os

subprocess.call(['curl',
                 '-o', 
                 'Data/data_new.csv', 
                 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'])

# Before rewriting the main file with the new one, simple check to make sure it is bigger
old_filename = 'data.csv'
old_filepath = os.path.join('Data', old_filename)
old_file_stats = os.stat(old_filepath)
old_file_size = old_file_stats.st_size

new_filename = 'data_new.csv'
new_filepath = os.path.join('Data', new_filename)
new_file_stats = os.stat(new_filepath)
new_file_size = new_file_stats.st_size

if new_file_size >= old_file_size:
    subprocess.call(['cp', new_filepath, old_filepath])
    
    subprocess.call(['python', 'COVID19_Viz_basemapFrames_US.py'])
    subprocess.call(['python', 'COVID19_Viz_makeMovie_US.py'])
    
    subprocess.call(['python', 'COVID19_Viz_basemapFrames.py'])
    subprocess.call(['python', 'COVID19_Viz_makeMovie.py'])
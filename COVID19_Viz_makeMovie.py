#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 17:43:12 2020

@author: pjb
"""

import subprocess
import glob
import os
import moviepy.editor as mpy
from moviepy.config import change_settings

# ../Avg_Sesh_Frames/avg_sessions_temp_slice_{0:03d}.png
image_folder = 'Frames'
n_frames = len([name for name in os.listdir(image_folder)])

# Make list of image names
# image_names = glob.glob(image_folder+'/*.png')

image_names_pre = 'Frames/daily_covid_'
image_names = []
for i in range(0, n_frames-1):
    image_names.append(image_names_pre+'{0:03d}'.format(i)+'.png')

#file_list = glob.glob('*.png') # Get all the pngs in the current directory
#list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case

# Reorder if necessary
# image_order = [0, 1, 2, 4, 5, 3] # force "surf spots" to be last
# image_names = [image_names[i] for i in image_order]

# Make animation
animation_name = 'COVID-19'
fps = 5

mv_name = animation_name+'.mp4'
gif_name = animation_name+'.gif'

# Get rid of old video if there is one
subprocess.call(['rm', '-r', mv_name])
subprocess.call(['rm', '-r', gif_name])

clip = mpy.ImageSequenceClip(image_names, fps=fps)
clip.write_videofile(mv_name, fps=fps)

clip = mpy.ImageSequenceClip(image_names, fps=fps)
clip.write_gif(gif_name, fps=fps)
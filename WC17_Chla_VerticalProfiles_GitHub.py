#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WC17: Generate Line Plots for Tchla vertical profiles

This script is related to the manuscript by Viljoen et al. (Preprint). 
For more details, refer to the project ReadMe: https://github.com/jjviljoen/Winter2017_PhytoNutrients_Python.

### Description
- Before running this script, execute `WC17_01` to process the original data files which creates "WC17_DataComp_update.csv" used here.
- Required data: Two XLSX files available from Zenodo: https://doi.org/10.5281/zenodo.6615070.

### Author
Johan Viljoen - j.j.viljoen@exeter.ac.uk

### Last Updated
20 Jan 2025
"""

#%%

### IMPORT PACKAGES ###

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

# Set the default font to Arial
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial']


#%%

#File name
file = "WC17_DataComp_update.csv"

# Read CSV
tbl = pd.read_csv(file)
tbl.info()

tbl.dropna(subset = ['Cruise'], inplace=True)

# Select Columns

keep_list = ['Station','Station_ID', 'Depth','Tchla']

tbl_chla = tbl[keep_list]

df = tbl_chla.copy()

df['Station_lbl'] = df['Station']
# Replace station codes with labels
station_mapping = {'IO08': 'St. 41.0°S', 'IO07': 'St. 43.0°S', 'IO06': 'St. 45.5°S',
                   'IO05': 'St. 48.0°S', 'IO04': 'St. 50.6°S', 'IO03': 'St. 53.5°S',
                   'IO02': 'St. 56.0°S', 'IO01': 'St. 58.5°S'}
df['Station_lbl'] = df['Station_lbl'].replace(station_mapping)

df.info()

plot_list = ['Station_ID','Station_lbl', 'Depth','Tchla']

df = df[plot_list]

# Plot Vertical line graph #

phyto_tbl_8 = (df[df['Station_ID'] == 8].drop('Station_ID', axis=1))
phyto_tbl_7 = (df[df['Station_ID'] == 7].drop('Station_ID', axis=1))
phyto_tbl_6 = (df[df['Station_ID'] == 6].drop('Station_ID', axis=1))
phyto_tbl_5 = (df[df['Station_ID'] == 5].drop('Station_ID', axis=1))
phyto_tbl_4 = (df[df['Station_ID'] == 4].drop('Station_ID', axis=1))
phyto_tbl_3 = (df[df['Station_ID'] == 3].drop('Station_ID', axis=1))
phyto_tbl_2 = (df[df['Station_ID'] == 2].drop('Station_ID', axis=1))
phyto_tbl_1 = (df[df['Station_ID'] == 1].drop('Station_ID', axis=1))

#%%

fig, axs = plt.subplots(figsize=(7, 9))
labelsize = 16
titlesize = 22
ticksize = 14
textsize = 14
legendsize = 12
# Stations
phyto_tbl_8.plot(ax=axs,x='Tchla', y='Depth', label='St. 41.0°S',
                 kind='line', color='red', marker = 'o', linewidth=1.1)
phyto_tbl_7.plot(ax=axs,x='Tchla', y='Depth', label='St. 43.0°S',
                 kind='line', color='silver', marker = 'D', linewidth=1.1)
phyto_tbl_6.plot(ax=axs,x='Tchla', y='Depth', label='St. 45.5°S',
                 kind='line', color='dimgray', marker = 'o', linewidth=1.1)
phyto_tbl_5.plot(ax=axs,x='Tchla', y='Depth', label='St. 48.0°S',
                 kind='line', color='limegreen', marker = 'o', linewidth=1.1)
phyto_tbl_4.plot(ax=axs,x='Tchla', y='Depth', label='St. 50.6°S',
                 kind='line', color='c', marker = 'o', linewidth=1.1)
phyto_tbl_3.plot(ax=axs,x='Tchla', y='Depth', label='St. 53.5°S',
                 kind='line', color='dodgerblue', marker = 'D', linewidth=1.1)
phyto_tbl_2.plot(ax=axs,x='Tchla', y='Depth', label='St. 56.0°S',
                 kind='line', color='blue', marker = 'o', linewidth=1.1)
phyto_tbl_1.plot(ax=axs,x='Tchla', y='Depth', label='St. 58.5°S',
                 kind='line', color='darkviolet', marker = 'o', linewidth=1.1)
# Set Depth Range
axs.set_ylim(160,0)
# Move x-axis to the top
axs.xaxis.tick_top()
axs.xaxis.set_label_position('top')
# Set x and y labels with font size
axs.set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs.set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
#axs.set_title('a)', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.08)
# Set size of axis tick labels
axs.tick_params(axis='both', which='both', labelsize=ticksize)
# Add custom y-axis ticks
custom_y_ticks = [0, 25, 50, 75, 100, 125, 150]
axs.set_yticks(custom_y_ticks)
# Edit legend
# Edit legend and place it below the plot
axs.legend(loc='lower center', fontsize=legendsize,
           ncol=4, bbox_to_anchor=(0.5, -0.1))

# Save the plot to a PNG file with 300dpi and tight border
plt.savefig('WC17_Chla_Vertical_LinePlot.jpeg', dpi=300, bbox_inches='tight')

plt.show()



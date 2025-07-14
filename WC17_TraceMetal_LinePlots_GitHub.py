"""
WC17: Generate Line Plots with error bars for Mixed layer trace metal concentrations

This script is related to the manuscript by Viljoen et al. 
For more details, refer to the project ReadMe: https://github.com/jjviljoen/Winter2017_PhytoNutrients_Python.

### Description
- Before running this script, execute `WC17_01` to process the original data files which creates "WC17_TM_Comp_update.csv" used here.
- Required data: Two XLSX files available from Zenodo: https://doi.org/10.5281/zenodo.6615070.

### Author
Johan Viljoen - j.j.viljoen@exeter.ac.uk

### Last Updated
14 July 2025
"""

#%%

### IMPORT PACKAGES ###

import pandas as pd
import matplotlib.pyplot as plt

#Use the default Matplotlib style
plt.style.use('default')

# Set the default font to Arial
plt.rcParams['font.family'] = 'Arial'

#%%

#File name
file = "WC17_TM_Comp_update.csv"

# Read CSV
tbl = pd.read_csv(file)
tbl.info()

### Clean & Filter Data ###

# Filter rows where ML is "IN"
tbl_ml = tbl[tbl['ML'] == 'IN']

# Remove Depth and ML columns
tbl_ml = tbl_ml.drop(columns=['Depth', 'ML'])

tbl_ml.info()

tbl_tm = tbl_ml.drop(columns=['Temp', 'Sal','Nitrate','Phosphate', 'Silicate'])

# Add Latitude column and fill based on conditions
tbl_tm['Latitude'] = 41.0  # default value

# Fill Latitude based on Station condition
tbl_tm.loc[tbl_tm['Station'] == 'IO08', 'Latitude'] = 41.0
tbl_tm.loc[tbl_tm['Station'] == 'IO07', 'Latitude'] = 43.0
tbl_tm.loc[tbl_tm['Station'] == 'IO06', 'Latitude'] = 45.5
tbl_tm.loc[tbl_tm['Station'] == 'IO05', 'Latitude'] = 48.0
tbl_tm.loc[tbl_tm['Station'] == 'IO04', 'Latitude'] = 50.6
#tbl_tm.loc[tbl_tm['Station'] == 'IO03', 'Latitude'] = 43.0
tbl_tm.loc[tbl_tm['Station'] == 'IO02', 'Latitude'] = 56.0
tbl_tm.loc[tbl_tm['Station'] == 'IO01', 'Latitude'] = 58.5

TM_df_list = ['Station', 'Latitude','dFe', 'dMn', 'dCo', 'dZn', 'dCd', 'dNi', 'dCu',
              'pFe', 'pMn', 'pCo', 'pZn', 'pCd', 'pNi', 'pCu']

tbl_dTM_df = tbl_tm[TM_df_list]

tbl_dTM_df.info()

tbl_dTM_df['dCd'] = tbl_dTM_df['dCd']/1000
# Convert pMn from nmol to pmol
tbl_dTM_df['pMn'] = tbl_dTM_df['pMn']*1000

#Setup Metal lists for figures
fig1_list = ['dFe', 'dMn']
fig2_list = ['dCo']
fig3_list = ['dZn', 'dCd']
fig4_list = ['dNi', 'dCu']
fig5_list = ['pFe', 'pMn']
fig6_list = ['pCo']
fig7_list = ['pZn', 'pCd']
fig8_list = ['pNi', 'pCu']

#%%

### dTM and pTM Lineplots ###

labelsize = 16
titlesize = 22
ticksize = 14
textsize = 14
legendsize = 14
title_x = -0.08
title_y = 1.01

# Set up figure and axis
fig, ([ax1,ax5],[ax2,ax6],[ax3,ax7],[ax4,ax8]) = plt.subplots(nrows=4, ncols=2, figsize=(17, 15), sharex=True)

# Adjust horizontal space between subplots
#fig.subplots_adjust(wspace=-0.8,hspace=0.5)

def plot_subplot(ax, metals, color_map, y1_min=None, y1_max=None, y2_min=None, y2_max=None,
                 y1_label = None, y2_label = None):
    first_metal = metals[0]
    remaining_metals = metals[1:]
    #Add front lines
    ax.axvline(x=42.4, color='black', linestyle='dashed', linewidth=1, alpha=0.5)
    ax.axvline(x=46.2, color='black', linestyle='dashed', linewidth=1, alpha=0.5)
    ax.axvline(x=49.3, color='black', linestyle='dashed', linewidth=1, alpha=0.5)
    ax.axvline(x=56.5, color='black', linestyle='dashed', linewidth=1, alpha=0.5)
    # Plot the first metal on the left y-axis
    metal_data = tbl_dTM_df.groupby('Latitude')[first_metal].agg(['mean', 'std'])
    ax.plot(metal_data.index, metal_data['mean'],
                label=f'{first_metal}', marker='o', markersize = 7,color=color_map[first_metal],
                linestyle='-', linewidth=2)
    ax.locator_params(axis='y', nbins=5) 
    if y1_label is None:
        y1_label = f'{first_metal} (units)'
    ax.set_ylabel(y1_label, fontsize=labelsize)
    ax.tick_params(axis='y', labelcolor=color_map[first_metal], labelsize=ticksize)
    
    if y1_min is not None and y1_max is not None:
        ax.set_ylim(y1_min, y1_max)  # Set custom y-axis range

    # Plot the remaining metals on the right y-axis (if any)
    if remaining_metals:
        twin_ax = ax.twinx()
        for metal in remaining_metals:
            metal_data = tbl_dTM_df.groupby('Latitude')[metal].agg(['mean', 'std'])
            twin_ax.plot(metal_data.index, metal_data['mean'],
                              label=f'{metal}', marker='o', markersize = 7, color=color_map[metal],
                              linestyle='-.', linewidth=2)
            twin_ax.tick_params(axis='y', labelcolor=color_map[metal], labelsize=ticksize)
            twin_ax.locator_params(axis='y', nbins=5) 
        if y2_label is None:
            y2_label = f'{", ".join(remaining_metals)} (units)' 
        twin_ax.set_ylabel(y2_label, fontsize=labelsize)
        twin_ax.legend(loc='upper right', fontsize=legendsize)
        
        if y2_min is not None and y2_max is not None:
            twin_ax.set_ylim(y2_min, y2_max)  # Set custom y-axis range

    ax.legend(loc='upper left', fontsize=legendsize)

# Create line graphs for fig1_list
color_map1 = {'dFe': 'blue', 'dMn': 'green'}
plot_subplot(ax1, fig1_list, color_map1, y1_min=0.006, y1_max=0.21, y2_min=0.18,y2_max=1.249,
                               y1_label='dFe ($nmol$ $kg^{-1}$)',
                               y2_label='dMn ($nmol$ $kg^{-1}$)')
ax1.set_title('a)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
#axes[0].axvline(x=42.4, color='black', linestyle='dashed', linewidth=1, alpha=0.6)
ax1.text(42.4, 0.211, 'STF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
#axes[0].axvline(x=46.2, color='black', linestyle='dashed', linewidth=1, alpha=0.6)
ax1.text(46.2, 0.211, 'SAF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
#axes[0].axvline(x=49.3, color='black', linestyle='dashed', linewidth=1, alpha=0.6)
ax1.text(49.3, 0.211, 'PF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
#axes[0].axvline(x=56.5, color='black', linestyle='dashed', linewidth=1, alpha=0.6)
ax1.text(56.5, 0.211, 'sAACf', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')

# Create line graphs for fig2_list
color_map2 = {'dCo': 'red'}
plot_subplot(ax2, fig2_list, color_map2, y1_min=8, y1_max=46,
                               y1_label='dCo ($pmol$ $kg^{-1}$)')
ax2.set_title('b)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)

# Create line graphs for fig3_list
color_map3 = {'dZn': 'purple', 'dCd': 'orange'}
plot_subplot(ax3, fig3_list, color_map3,y1_min=-0.4, y1_max=5.9, y2_min=-0.1,y2_max=1.1,
                               y1_label='dZn ($nmol$ $kg^{-1}$)',
                               y2_label='dCd ($nmol$ $kg^{-1}$)')
ax3.set_title('c)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)

# Create line graphs for fig4_list
color_map4 = {'dNi': 'brown', 'dCu': 'm'}
plot_subplot(ax4, fig4_list, color_map4, y1_min=0.5, y1_max=9.1, y2_min=0.2,y2_max=2.4,
             y1_label='dNi ($nmol$ $kg^{-1}$)',
             y2_label='dCu ($nmol$ $kg^{-1}$)')
ax4.set_title('d)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
ax4.set_xlabel('Latitude (°S)', fontsize=labelsize)
ax4.tick_params(axis='x', labelsize=ticksize)

# Reverse x-axis order
# =============================================================================
# axes[0].invert_xaxis()
# axes[1].invert_xaxis()
# axes[2].invert_xaxis()
# =============================================================================
#ax4.invert_xaxis()

# Create line graphs for fig5_list
color_map5 = {'pFe': 'blue', 'pMn': 'green'}
plot_subplot(ax5, fig5_list, color_map5,y1_min=0.04, y1_max=0.22, y2_min=0.001,y2_max=0.099,
                               y1_label='pFe ($nmol$ $kg^{-1}$)',
                               y2_label='pMn ($nmol$ $kg^{-1}$)')
ax5.set_title('e)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
ax5.locator_params(axis='y', nbins=5) 
#axes[0].axvline(x=42.4, color='black', linestyle='dashed', linewidth=1, alpha=0.6)
ax5.text(42.4, 0.221, 'STF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
#axes[0].axvline(x=46.2, color='black', linestyle='dashed', linewidth=1, alpha=0.6)
ax5.text(46.2, 0.221, 'SAF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
#axes[0].axvline(x=49.3, color='black', linestyle='dashed', linewidth=1, alpha=0.6)
ax5.text(49.3, 0.221, 'PF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
#axes[0].axvline(x=56.5, color='black', linestyle='dashed', linewidth=1, alpha=0.6)
ax5.text(56.5, 0.221, 'sAACf', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')

# Create line graphs for fig6_list
color_map6 = {'pCo': 'red'}
plot_subplot(ax6, fig6_list, color_map6,y1_min=0.2, y1_max=3.9,
                               y1_label='pCo ($pmol$ $kg^{-1}$)')
ax6.set_title('f)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)

# Create line graphs for fig7_list
color_map7 = {'pZn': 'purple', 'pCd': 'orange'}
plot_subplot(ax7, fig7_list, color_map7,y1_min=0.01, y1_max=0.16, y2_min=5.5,y2_max=24,
                               y1_label='pZn ($nmol$ $kg^{-1}$)',
                               y2_label='pCd ($pmol$ $kg^{-1}$)')
ax7.set_title('g)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
ax7.locator_params(axis='y', nbins=3) 

# Create line graphs for fig8_list
color_map8 = {'pNi': 'brown', 'pCu': 'm'}
plot_subplot(ax8, fig8_list, color_map8,y1_min=16, y1_max=32.5, y2_min=17.5,y2_max=48.5,
             y1_label='pNi ($pmol$ $kg^{-1}$)',
             y2_label='pCu ($pmol$ $kg^{-1}$)')
ax8.set_title('h)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
ax8.set_xlabel('Latitude (°S)', fontsize=labelsize)
ax8.tick_params(axis='x', labelsize=ticksize)

ax8.invert_xaxis()

plt.tight_layout()

# Save the plot to a PNG file with 300dpi and tight border
plt.savefig('WC17_TM_LinePlot.jpeg', dpi=300, bbox_inches='tight')

plt.show()

#%%

### LINE PLOTS WITH ERROR BARS

from scipy.stats import median_abs_deviation

# Function to calculate MAD
def mad(series):
    return median_abs_deviation(series, scale=1,nan_policy='omit')

# Set up figure and axis
fig, ([ax1,ax5],[ax2,ax6],[ax3,ax7],[ax4,ax8]) = plt.subplots(nrows=4, ncols=2, figsize=(17, 13), sharex=True)

labelsize = 16
titlesize = 22
ticksize = 14
textsize = 13
legendsize = 11
title_x = -0.08
title_y = 1.03

# Modify plot_subplot function to use median and MAD
def plot_subplot(ax, metals, color_map, y1_min=None, y1_max=None, y2_min=None, y2_max=None,
                 y1_label=None, y2_label=None):
    first_metal = metals[0]
    remaining_metals = metals[1:]
    
    # Add vertical lines (for reference)
    ax.axvline(x=42.4, color='black', linestyle='dashed', linewidth=1, alpha=0.5)
    ax.axvline(x=46.2, color='black', linestyle='dashed', linewidth=1, alpha=0.5)
    ax.axvline(x=49.3, color='black', linestyle='dashed', linewidth=1, alpha=0.5)
    ax.axvline(x=56.5, color='black', linestyle='dashed', linewidth=1, alpha=0.5)#58.5
    ax.axvline(x=58.5, color='black', linestyle='dashed', linewidth=1, alpha=0.5)
    # Plot the first metal (left y-axis)
    # Ensure all metals are numeric before aggregation
    metal_data = tbl_dTM_df.groupby('Latitude')[first_metal].agg(['median', mad])
    
    # Check if the metal name starts with 'p' to add the "excess" subscript
    label_first_metal = f'{first_metal}$_{{excess}}$' if first_metal.startswith('p') else first_metal
    
    ax.errorbar(metal_data.index, metal_data['median'], yerr=metal_data['mad'], 
                label=label_first_metal, marker='o', markersize=6, color=color_map[first_metal], 
                linestyle='-', linewidth=2, capsize=5)
    
    ax.locator_params(axis='y', nbins=5)
    ax.grid(False)
    
    if y1_label is None:
        y1_label = f'{first_metal} (units)'
    ax.set_ylabel(y1_label, fontsize=labelsize)
    ax.tick_params(axis='y', labelcolor=color_map[first_metal], labelsize=ticksize, left=True, labelleft=True)

    if y1_min is not None and y1_max is not None:
        ax.set_ylim(y1_min, y1_max)  # Set custom y-axis range

    # Plot the remaining metals (right y-axis)
    if remaining_metals:
        twin_ax = ax.twinx()
        for metal in remaining_metals:
            metal_data = tbl_dTM_df.groupby('Latitude')[metal].agg(['median', mad])
            # Check if the metal name starts with 'p' to add the "excess" subscript
            label_remaining_metal = f'{metal}$_{{excess}}$' if metal.startswith('p') else metal
            twin_ax.errorbar(metal_data.index, metal_data['median'], yerr=metal_data['mad'], 
                             label=label_remaining_metal, marker='o', markersize=6, color=color_map[metal],
                             linestyle='-.', linewidth=2, capsize=5)
            twin_ax.tick_params(axis='y', labelcolor=color_map[metal], labelsize=ticksize)
            twin_ax.locator_params(axis='y', nbins=5)
            twin_ax.grid(False)
        
        if y2_label is None:
            y2_label = f'{", ".join(remaining_metals)} (units)' 
        twin_ax.set_ylabel(y2_label, fontsize=labelsize)
        twin_ax.legend(loc='upper right', fontsize=legendsize)
        
        if y2_min is not None and y2_max is not None:
            twin_ax.set_ylim(y2_min, y2_max)  # Set custom y-axis range

    ax.legend(loc='upper left', fontsize=legendsize)

# Repeat the plot_subplot function call for other figures as in the original code...
# Create line graphs for fig1_list
color_map1 = {'dFe': 'blue', 'dMn': 'green'}
plot_subplot(ax1, fig1_list, color_map1, y1_min=0.006, y1_max=0.21, y2_min=0.18,y2_max=1.249,
                               y1_label='dFe ($nmol$ $kg^{-1}$)',
                               y2_label='dMn ($nmol$ $kg^{-1}$)')
ax1.set_title('a)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)

ax1.text(42.4, 0.211, 'STF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax1.text(46.2, 0.211, 'SAF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax1.text(49.3, 0.211, 'PF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax1.text(56.5, 0.211, 'sAACf', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax1.text(58.5, 0.211, 'SBdy', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')

# Create line graphs for fig2_list
color_map2 = {'dCo': 'red'}
plot_subplot(ax2, fig2_list, color_map2, y1_min=8, y1_max=46,
                               y1_label='dCo ($pmol$ $kg^{-1}$)')
ax2.set_title('b)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)

# Create line graphs for fig3_list
color_map3 = {'dZn': 'purple', 'dCd': 'orange'}
plot_subplot(ax3, fig3_list, color_map3,y1_min=-0.4, y1_max=5.9, y2_min=-0.1,y2_max=1.1,
                               y1_label='dZn ($nmol$ $kg^{-1}$)',
                               y2_label='dCd ($nmol$ $kg^{-1}$)')
ax3.set_title('c)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)

# Create line graphs for fig4_list
color_map4 = {'dNi': 'brown', 'dCu': 'm'}
plot_subplot(ax4, fig4_list, color_map4, y1_min=0.5, y1_max=9.1, y2_min=0.2,y2_max=2.4,
             y1_label='dNi ($nmol$ $kg^{-1}$)',
             y2_label='dCu ($nmol$ $kg^{-1}$)')
ax4.set_title('d)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
ax4.set_xlabel('Latitude (°S)', fontsize=labelsize)
ax4.tick_params(axis='x', labelsize=ticksize, bottom=True, labelbottom=True)

# Create line graphs for fig5_list
color_map5 = {'pFe': 'blue', 'pMn': 'green'}
plot_subplot(ax5, fig5_list, color_map5,y1_min=-0.005, y1_max=0.28, y2_min=-0.005,y2_max=99.9,
                               y1_label='pFe ($nmol$ $kg^{-1}$)',
                               y2_label='pMn ($pmol$ $kg^{-1}$)')
ax5.set_title('e)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
ax5.locator_params(axis='y', nbins=5) 

ax5.text(42.4, 0.281, 'STF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax5.text(46.2, 0.281, 'SAF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax5.text(49.3, 0.281, 'PF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax5.text(56.5, 0.281, 'sAACf', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax5.text(58.5, 0.281, 'SBdy', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')

# Create line graphs for fig6_list
color_map6 = {'pCo': 'red'}
plot_subplot(ax6, fig6_list, color_map6,y1_min=0.2, y1_max=4.9,
                               y1_label='pCo ($pmol$ $kg^{-1}$)')
ax6.set_title('f)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)

# Create line graphs for fig7_list
color_map7 = {'pZn': 'purple', 'pCd': 'orange'}
plot_subplot(ax7, fig7_list, color_map7,y1_min=0.01, y1_max=0.18, y2_min=5.5,y2_max=23,
                               y1_label='pZn ($nmol$ $kg^{-1}$)',
                               y2_label='pCd ($pmol$ $kg^{-1}$)')
ax7.set_title('g)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
ax7.locator_params(axis='y', nbins=3) 

# Create line graphs for fig8_list
color_map8 = {'pNi': 'brown', 'pCu': 'm'}
plot_subplot(ax8, fig8_list, color_map8,y1_min=1, y1_max=49, y2_min=14,y2_max=55,
             y1_label='pNi ($pmol$ $kg^{-1}$)',
             y2_label='pCu ($pmol$ $kg^{-1}$)')
ax8.set_title('h)', loc='left', fontweight='bold', fontsize=titlesize, x=title_x, y=title_y)
ax8.set_xlabel('Latitude (°S)', fontsize=labelsize)
ax8.tick_params(axis='x', labelsize=ticksize, length=5, bottom=True, labelbottom=True)
#ax8.locator_params(axis='y', nbins=5)

ax8.invert_xaxis()

plt.tight_layout()

# Save the plot to a PNG file with 300dpi and tight border
plt.savefig('WC17_TM_LinePlot_TM_all_MedianMAD.jpeg', dpi=300, bbox_inches='tight')
plt.savefig('WC17_TM_LinePlot_TM_all_MedianMAD.pdf', dpi=300, format = 'pdf',bbox_inches='tight')

plt.show()


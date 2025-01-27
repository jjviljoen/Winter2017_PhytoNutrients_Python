"""
WC17: Generate Bar Plots for Phytoplankton composition - Concentration and Percentage

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
from matplotlib.ticker import FuncFormatter

# Use the default Matplotlib style
plt.style.use('default')

# Set the default font to Arial
plt.rcParams['font.family'] = 'Arial'

#%%

### 100% STACKED BARPLOT ML AVERAGE ###

#File name
file = "WC17_DataComp_update.csv"

# Read CSV
tbl = pd.read_csv(file)
tbl.info()

tbl['Cyanobacteria'] = tbl['Synechococcus'] + tbl['Prochlorococcus']
tbl.info()

# Define the column you want to move and its target position
column_to_move = 'Cyanobacteria'
target_column = 'Prochlorococcus'

# Move the specified column after the target column
df = tbl
columns = df.columns.tolist()
columns.remove(column_to_move)
columns.insert(columns.index(target_column) + 1, column_to_move)

# Reorder the columns in the DataFrame
tbl = df[columns]
tbl.info()
tbl.head()

tbl.dropna(subset = ['Cruise'], inplace=True)

# Select Columns
# Filter rows where ML is "IN"
tbl_ml = tbl[tbl['ML'] == 'IN']

df = tbl_ml.copy()
# Replace 'IO08' with 'St. 41.0°S' in the 'Station' column
df['Station'] = df['Station'].replace('IO08', 'St. 41.0°S')
df['Station'] = df['Station'].replace('IO07', 'St. 43.0°S')
df['Station'] = df['Station'].replace('IO06', 'St. 45.5°S')
df['Station'] = df['Station'].replace('IO05', 'St. 48.0°S')
df['Station'] = df['Station'].replace('IO04', 'St. 50.6°S')
df['Station'] = df['Station'].replace('IO03', 'St. 53.5°S')
df['Station'] = df['Station'].replace('IO02', 'St. 56.0°S')
df['Station'] = df['Station'].replace('IO01', 'St. 58.5°S')

tbl_ml = df.copy()

tchla_list = ['Station','Tchla']

phyto_list = ['Station','Diatoms', 'Coccolithophores','Phaeocystis', 'Dinoflagellates',
              'Cryptophytes', 'Pelagophytes', 'Prasinophytes', 'Chlorophytes',
              'Synechococcus', 'Prochlorococcus']

selected_df = tbl_ml[phyto_list]

# Grouping by 'Station' and calculating median
grouped_df = selected_df.groupby('Station').median()

# Reverse the order of stations
grouped_df = grouped_df[::-1]

Tchla_df = tbl_ml[tchla_list]

# Grouping by 'Station' and calculating mean
Tchla_df = Tchla_df.groupby('Station').median()

# Reverse the order of stations
Tchla_df = Tchla_df[::-1]

# Define legend items and corresponding colors
legend_items = ['Diatoms', 'Coccolithophores','Phaeocystis', 'Dinoflagellates',
              'Cryptophytes', 'Pelagophytes', 'Prasinophytes', 'Chlorophytes',
              'Synechococcus', 'Prochlorococcus']
phyto_colours = ['saddlebrown', 'dimgray', 'darkgray', 'darkorange',
                 'darkolivegreen','goldenrod',  'limegreen', 'lawngreen',
                 'red', '#6633CC']

labelsize = 15
#titlesize = 22
ticksize = 13
textsize = 11
legendsize = 12

# Plotting a 100% stacked bar plot with specific colors
ax = grouped_df.div(grouped_df.sum(1), axis=0).plot(
    kind='bar', stacked=True, color=phyto_colours * len(grouped_df.columns),
    figsize=(10, 6), edgecolor='black', linewidth=0.5, zorder=2)
# Disable all gridlines
ax.grid(False)

# Plotting a 100% stacked bar plot with specific colors
twin_ax = ax.twinx()
twin_ax.plot(Tchla_df.index, Tchla_df['Tchla'],
    color='mediumorchid', linewidth=1.5, marker= 'o'
)
# Disable all gridlines
twin_ax.grid(False)
twin_ax.set_ylabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize, color='mediumorchid')
twin_ax.tick_params(axis='y',labelsize=ticksize, labelcolor='mediumorchid')
# Setting y-axis limits for the twin y-axis
twin_ax.set_ylim(0, 0.31)

# Adding dashed vertical lines after bars 4, 5, and 7
ax.axvline(x=0, color='black', linestyle='dashed', linewidth=1, zorder=1)
ax.axvline(x=0.5, color='black', linestyle='dashed', linewidth=1)
ax.axvline(x=3.5, color='black', linestyle='dashed', linewidth=1)
ax.axvline(x=4.5, color='black', linestyle='dashed', linewidth=1)
ax.axvline(x=6.5, color='black', linestyle='dashed', linewidth=1)

# Adding labels for each vertical line
ax.text(0, 1.05, 'SBdy', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax.text(0.5, 1.05, 'sAACf', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax.text(3.5, 1.05, 'PF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax.text(4.5, 1.05, 'SAF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')
ax.text(6.5, 1.05, 'STF', ha='center', va='bottom', color='black', fontsize=textsize, weight= 'bold')

# Format y-axis tick labels as percentages
ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{int(y*100)}%'))

# Make x-axis tick labels horizontal
#ax.xticks(rotation=0,fontsize = ticksize)
ax.tick_params(axis='x',rotation=0,labelsize=ticksize, bottom=True, labelbottom=True)
#ax.yticks(fontsize = ticksize)
ax.tick_params(axis='y',labelsize=ticksize)

# Adding labels and title
ax.set_xlabel('Station',fontsize = labelsize)
ax.set_ylabel('Percentage',fontsize = labelsize)

plt.plot

#plt.title('100% Stacked Bar Plot of Phytoplankton Species per Station')

# Creating a legend with custom colors
legend_labels = {item: color for item, color in zip(legend_items, phyto_colours)}
handles = [plt.Rectangle((0, 0), 1, 1, color=legend_labels[label]) for label in legend_items]
ax.legend(handles, legend_items, loc='upper center', fontsize=legendsize,
           bbox_to_anchor=(0.5, -0.13), ncol=len(legend_items)/2)


# Save the plot to a PNG file with 300dpi and tight border
plt.savefig('WC17_stacked_bar_plot.png', dpi=300, bbox_inches='tight')
plt.savefig('WC17_stacked_bar_plot.pdf', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

#%%

### VERTICAL BARPLOT AVERAGE PER ZONE ###

phyto_list = ['Station_ID', 'Depth','Diatoms', 'Coccolithophores','Phaeocystis', 'Dinoflagellates',
              'Cryptophytes', 'Pelagophytes', 'Prasinophytes', 'Chlorophytes',
              'Synechococcus', 'Prochlorococcus']

phyto_tbl1 = tbl[phyto_list].copy()

# Assuming phyto_tbl1 is a DataFrame
phyto_tbl1['Depth'] = phyto_tbl1['Depth'].astype(int)

# Assuming phyto_tbl1 is a DataFrame
new_row = pd.DataFrame([[8, 25] + [0] * (len(phyto_list) - 2)], columns=phyto_list)

# Insert the new row as the second row
phyto_tbl1 = pd.concat([phyto_tbl1.iloc[:1], new_row, phyto_tbl1.iloc[1:]], ignore_index=True)

# Add depth 50 and 150m to station 2
new_row_50 = pd.DataFrame([[2, 50] + [0] * (len(phyto_list) - 2)], columns=phyto_list)
new_row_150 = pd.DataFrame([[2, 150] + [0] * (len(phyto_list) - 2)], columns=phyto_list)

# Insert the new row as the second row
new_row_df = pd.concat([new_row_50, new_row_150])

# Insert the new row as the second row
phyto_tbl1 = pd.concat([phyto_tbl1, new_row_df])

phyto_tbl1 = phyto_tbl1.sort_values(['Station_ID', 'Depth'], ascending=True)


phyto_tbl_stz = (phyto_tbl1[phyto_tbl1['Station_ID'] == 8].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])

phyto_tbl_sub = (phyto_tbl1[(phyto_tbl1['Station_ID'] < 8) & (phyto_tbl1['Station_ID'] > 4)]
                 .groupby(['Depth']).mean().reset_index().drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])

phyto_tbl_aaz = (phyto_tbl1[phyto_tbl1['Station_ID'] < 5]
                 .groupby(['Depth']).mean().reset_index().drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])

# Define legend items and corresponding colors
legend_items = ['Diatoms', 'Coccolithophores','Phaeocystis', 'Dinoflagellates',
              'Cryptophytes', 'Pelagophytes', 'Prasinophytes', 'Chlorophytes',
              'Synechococcus', 'Prochlorococcus']
phyto_colours = ['saddlebrown', 'dimgray', 'darkgray', 'darkorange',
                 'darkolivegreen','goldenrod',  'limegreen', 'lawngreen',
                 'red', '#6633CC']

# PLOTS ################################################
fig, axs = plt.subplots(1, 3, figsize=(15, 5.5))

# Adjust horizontal space between subplots
fig.subplots_adjust(wspace=0.3)

labelsize = 16
titlesize = 22
ticksize = 14
textsize = 16
legendsize = 14

#Subtropical
phyto_tbl_stz.plot(ax=axs[0],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[0].xaxis.tick_top()
axs[0].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[0].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[0].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[0].set_title('a)', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.08)
# Set size of axis tick labels
axs[0].tick_params(axis='both', which='both', labelsize=ticksize)
# Remove legend
axs[0].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[0].text(0.98, 0.02, 'Subtropical', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[0].transAxes)
#Subantarcitc
phyto_tbl_sub.plot(ax=axs[1],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[1].xaxis.tick_top()
axs[1].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[1].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[1].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[1].set_title('b)', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.08)
# Set size of axis tick labels
axs[1].tick_params(axis='both', which='both', labelsize=ticksize)
# Remove legend
axs[1].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[1].text(0.98, 0.02, 'Subantarctic', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[1].transAxes)
# Antarctic
phyto_tbl_aaz.plot(ax=axs[2],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[2].xaxis.tick_top()
axs[2].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[2].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[2].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[2].set_title('c)', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.08)
# Set size of axis tick labels
axs[2].tick_params(axis='both', which='both', labelsize=ticksize)
# Remove legend
axs[2].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[2].text(0.98, 0.02, 'Antarctic', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[2].transAxes)


# Creating a legend with custom colors
legend_labels = {item: color for item, color in zip(legend_items, phyto_colours)}
handles = [plt.Rectangle((0, 0), 1, 1, color=legend_labels[label]) for label in legend_items]
axs[1].legend(handles, legend_items, loc='lower center', fontsize=legendsize,
           bbox_to_anchor=(0.5, -0.2), ncol=len(legend_items) // 2)



# Save the plot to a PNG file with 300dpi and tight border
plt.savefig('WC17_Phyto_Vertical_BarPlot_ZoneAvg.jpeg', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

#%%

### VERTICAL BARPLOT FOR EACH STATION ###

phyto_tbl_8 = (phyto_tbl1[phyto_tbl1['Station_ID'] == 8].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])
phyto_tbl_7 = (phyto_tbl1[phyto_tbl1['Station_ID'] == 7].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])
phyto_tbl_6 = (phyto_tbl1[phyto_tbl1['Station_ID'] == 6].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])
phyto_tbl_5 = (phyto_tbl1[phyto_tbl1['Station_ID'] == 5].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])
phyto_tbl_4 = (phyto_tbl1[phyto_tbl1['Station_ID'] == 4].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])
phyto_tbl_3 = (phyto_tbl1[phyto_tbl1['Station_ID'] == 3].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])
phyto_tbl_2 = (phyto_tbl1[phyto_tbl1['Station_ID'] == 2].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])
phyto_tbl_1 = (phyto_tbl1[phyto_tbl1['Station_ID'] == 1].drop('Station_ID', axis=1)
                 .set_index('Depth').loc[::-1])

# Define legend items and corresponding colors
legend_items = ['Diatoms', 'Coccolithophores','Phaeocystis', 'Dinoflagellates',
              'Cryptophytes', 'Pelagophytes', 'Prasinophytes', 'Chlorophytes',
              'Synechococcus', 'Prochlorococcus']
phyto_colours = ['saddlebrown', 'dimgray', 'darkgray', 'darkorange',
                 'darkolivegreen','goldenrod',  'limegreen', 'lawngreen',
                 'red', '#6633CC']

# PLOTS ################################################
fig, axs = plt.subplots(2, 4, figsize=(17, 13))

# Adjust horizontal space between subplots
fig.subplots_adjust(wspace=0.35,hspace=0.3)

labelsize = 16
titlesize = 22
ticksize = 14
textsize = 15
legendsize = 16

# Flatten axs to a 1D array
axs = axs.flatten()

#Station 8
phyto_tbl_8.plot(ax=axs[0],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
axs[0].grid(False)
# Move x-axis to the top
axs[0].xaxis.tick_top()
axs[0].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[0].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[0].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[0].set_title('a) St. 41.0°S', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.14)
# Set size of axis tick labels
axs[0].tick_params(axis='both', which='both', labelsize=ticksize, left=True)
# Remove legend
axs[0].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[0].text(0.98, -0.006, 'STZ', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[0].transAxes)
# Adding dashed horizontal line for MLD
axs[0].axhline(y=0.6, color='b', linestyle='dashed', linewidth=1)
axs[0].text(0.25, 0.58, '113m', ha='center', va='top', color='b', fontsize=12)
#Station 7
phyto_tbl_7.plot(ax=axs[1],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[1].xaxis.tick_top()
axs[1].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[1].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[1].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[1].set_title('b) St. 43.0°S', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.14)
# Set size of axis tick labels
axs[1].tick_params(axis='both', which='both', labelsize=ticksize, left=True)
# Remove legend
axs[1].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[1].text(0.98, -0.006, 'SAZ', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[1].transAxes)

# Station 6
phyto_tbl_6.plot(ax=axs[2],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[2].xaxis.tick_top()
axs[2].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[2].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[2].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[2].set_title('c) 45.5°S', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.14)
# Set size of axis tick labels
axs[2].tick_params(axis='both', which='both', labelsize=ticksize, left=True)
# Remove legend
axs[2].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[2].text(0.98, -0.006, 'SAZ', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[2].transAxes)
# Station 5
phyto_tbl_5.plot(ax=axs[3],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[3].xaxis.tick_top()
axs[3].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[3].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[3].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[3].set_title('d) St. 48.0°S', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.14)
# Set size of axis tick labels
axs[3].tick_params(axis='both', which='both', labelsize=ticksize, left=True)
# Remove legend
axs[3].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[3].text(0.98, -0.006, 'PFZ', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[3].transAxes)
# Adding dashed horizontal line for MLD
axs[3].axhline(y=0.3, color='b', linestyle='dashed', linewidth=1)
axs[3].text(0.18, 0.28, '146m', ha='center', va='top', color='b', fontsize=12)
# Station 4
phyto_tbl_4.plot(ax=axs[4],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[4].xaxis.tick_top()
axs[4].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[4].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[4].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[4].set_title('e) St. 50.6°S', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.14)
# Set size of axis tick labels
axs[4].tick_params(axis='both', which='both', labelsize=ticksize, left=True)
# Remove legend
axs[4].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[4].text(0.98, -0.006, 'AAZ', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[4].transAxes)
# Adding dashed horizontal line for MLD
axs[4].axhline(y=0.35, color='b', linestyle='dashed', linewidth=1)
axs[4].text(0.12, 0.33, '136m', ha='center', va='top', color='b', fontsize=12)
# Station 3
phyto_tbl_3.plot(ax=axs[5],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[5].xaxis.tick_top()
axs[5].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[5].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[5].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[5].set_title('f) St. 53.5°S', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.14)
# Set size of axis tick labels
axs[5].tick_params(axis='both', which='both', labelsize=ticksize, left=True)
# Remove legend
axs[5].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[5].text(0.98, -0.006, 'AAZ', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[5].transAxes)
# Adding dashed horizontal line for MLD
axs[5].axhline(y=1.5, color='b', linestyle='dashed', linewidth=1)
axs[5].text(0.11, 1.48, '82m', ha='center', va='top', color='b', fontsize=12)
# Station 2
phyto_tbl_2.plot(ax=axs[6],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
# Move x-axis to the top
axs[6].xaxis.tick_top()
axs[6].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[6].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[6].set_ylabel('Depth (m)', fontsize=labelsize)
# Add plot title with adjusted position
axs[6].set_title('g) St. 56.0°S', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.14)
# Set size of axis tick labels
axs[6].tick_params(axis='both', which='both', labelsize=ticksize, left=True)
# Remove legend
axs[6].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[6].text(0.98,-0.006, 'AAZ', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[6].transAxes)
# Station 1
phyto_tbl_1.plot(ax=axs[7],
    kind='barh', stacked=True, color=phyto_colours * len(legend_items),
    edgecolor='black', linewidth=0.5)
axs[7].grid(False)
# Move x-axis to the top
axs[7].xaxis.tick_top()
axs[7].xaxis.set_label_position('top')
# Set x and y labels with font size
axs[7].set_xlabel('Tchl-a ($µg$  $L^{-1}$)', fontsize=labelsize)
axs[7].set_ylabel(None, fontsize=labelsize)
# Add plot title with adjusted position
axs[7].set_title('h) St. 58.5°S', loc='left', fontweight='bold', fontsize=titlesize, x=-0.14, y=1.14)
# Set size of axis tick labels
axs[7].tick_params(axis='both', which='both', labelsize=ticksize, left=True)
# Remove legend
axs[7].legend().set_visible(False)
# Add text to the right bottom corner in bold for axs[0] subplot
axs[7].text(0.98, -0.006, 'AAZ', fontsize=textsize, fontweight='bold', ha='right',
            va='bottom', transform=axs[7].transAxes)

# Creating a legend with custom colors
legend_labels = {item: color for item, color in zip(legend_items, phyto_colours)}
handles = [plt.Rectangle((0, 0), 1, 1, color=legend_labels[label]) for label in legend_items]
fig.legend(handles, legend_items, loc='lower center', fontsize=legendsize,
           bbox_to_anchor=(0.5, 0.03), ncol=len(legend_items) // 2)

# Save the plot to a PNG file with 300dpi and tight border
plt.savefig('WC17_Phyto_Vertical_BarPlot_Stations.jpeg', dpi=300, bbox_inches='tight')

# Display the plot
plt.show()

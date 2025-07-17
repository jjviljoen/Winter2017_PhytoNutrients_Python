"""
WC17: Generate Summary Statistics for Phytoplankton & Pigments in upper 150m

This script is related to the manuscript by Viljoen et al. (Preprint). 
For more details, refer to the project ReadMe: https://github.com/jjviljoen/Winter2017_PhytoNutrients_Python.

### Description
- This script generates tables with Medians and Median Absolute deviation (MAD) based on processed data.
- Before running this script, execute `WC17_01` to process the original data files which creates "WC17_DataComp_update.csv" used here.
- Required data: Two XLSX files available from Zenodo: https://doi.org/10.5281/zenodo.6615070.

### Author
Johan Viljoen - j.j.viljoen@exeter.ac.uk

### Last Updated
17 July 2025
"""

#%%

### IMPORT PACKAGES ###

import pandas as pd
from scipy.stats import describe, median_abs_deviation

#%%

#File name
file = "WC17_DataComp_update.csv"

# Read CSV
tbl = pd.read_csv(file)
tbl.info()

#%%

# Filter rows where ML is "IN"
tbl_ml = tbl[tbl['ML'] == 'IN']

# Remove Depth and ML columns
tbl_ml = tbl_ml.drop(columns=['ML'])

#%%

### SETUP FUNCTIONS ###

def sig_digits(x, d):
    z = format(x, f'.{d}f')
    if '.' not in z:
        return z
    return z.rstrip('0')

def dec_place(x, d):
    if d == 0:
        return int(round(x))  # Return as integer with no decimal places
    else:
        return f'{x:.{d}f}'  # Format to specified number of decimal places

def mean_range(data, d):
    m, s, a, b = describe(data).mean, describe(data).stddev, describe(data).minmax[0], describe(data).minmax[1]
    val = f'{dec_place(m, d)} ± {dec_place(s, d)} ({dec_place(a, d)} - {dec_place(b, d)})'
    return val

def mean_only(data, d):
    m = data.mean(skipna=True)
    val = f'{dec_place(m, d)}'
    return val

def mean_sd(data, d):
    m = data.mean(skipna=True)
    s = data.std(skipna=True)
    val = f'{dec_place(m, d)} ± {dec_place(s, d)}'
    return val

def median_tbl(data, d):
    m = data.median(skipna=True)
    mad = median_abs_deviation(data, nan_policy='omit')
    
    val = f'{dec_place(m, d)} ± {dec_place(mad, d)}'
    return val

def median_tbl_n(data, d):
    # Calculate median and MAD
    m = data.median(skipna=True)
    mad = median_abs_deviation(data, nan_policy='omit')
    # Count the number of valid values (excluding NaNs)
    n = data.count()
    
    # Format the result to include the median, MAD, and count
    val = f'{dec_place(m, d)} ± {dec_place(mad, d)} ({n})'
    return val

def av_table(df,summary_type='mean', d=2):
    # Read CSV file
    data = df
    # Calculate mean and standard deviation per column
    #d = 6  # Number of decimal places
    
    if summary_type =='mean':
        data_av = data.groupby('Station').agg(lambda x: mean_only(x, d))
    elif summary_type =='mean_sd':
        data_av = data.groupby('Station').agg(lambda x: mean_sd(x, d))
    elif summary_type =='median':
        data_av = data.groupby('Station').agg(lambda x: median_tbl(x, d))
    elif summary_type =='median_n':
        data_av = data.groupby('Station').agg(lambda x: median_tbl_n(x, d))
    else:
        raise ValueError("Invalid summary_type. Choose 'mean' or 'median'.")
    # Reverse the order of rows based on the 'Station' column
    data_av = data_av.sort_values(by='Station', ascending=True).reset_index(drop=False)

    return data_av

#%%

# Convert dCd from pmol to nmol
tbl_ml['dCd'] = tbl_ml['dCd']/1000

# Convert pMn from nmol to pmol
tbl_ml['pMn'] = tbl_ml['pMn']*1000

# Remove Depth columns
tbl_ml2 = tbl_ml.drop(columns=['Depth'])

# Replace station codes with labels
tbl_ml2['Station_lbl'] = tbl_ml2['Station']
station_mapping = {'IO08': 'St. 41.0°S', 'IO07': 'St. 43.0°S', 'IO06': 'St. 45.5°S',
                   'IO05': 'St. 48.0°S', 'IO04': 'St. 50.6°S', 'IO03': 'St. 53.5°S',
                   'IO02': 'St. 56.0°S', 'IO01': 'St. 58.5°S'}
tbl_ml2['Station'] = tbl_ml2['Station_lbl'].replace(station_mapping)
tbl_ml2.drop(columns=['Station_lbl','Station Label'], inplace=True)

tbl_ml2.info()
#%%

# MainText Table1
list_1 = ['Station','Temp', 'Tchla', 'POC', 'Nitrate', 'Phosphate', 'Silica']
tbl_ml2_stats =  av_table(tbl_ml2[list_1],summary_type='median')
#Save df
output_filename = 'WC17_DataComp_Table1_median.xlsx'
tbl_ml2_stats.to_excel(output_filename, index=False)

tbl_ml2['PhaeoTotal'] = tbl_ml2['Phorb_a'] + tbl_ml2['Phytin_a']
tbl_ml2['Phaeo_Chla'] = tbl_ml2['PhaeoTotal']/tbl_ml2['Tchla']

# Tchla & Fchla for Table S3
list_1 = ['Station','Tchla', 'Fl_Chla', 'Phaeo_Chla']
tbl_ml2_stats =  av_table(tbl_ml2[list_1],summary_type='median')
#Save df
output_filename = 'WC17_DataComp_TchlaFchla_median.xlsx'
tbl_ml2_stats.to_excel(output_filename, index=False)

#%%

# Calculate Percentage Phytoplankton for Mixed layer

# Select stations and Phytoplankton columns
tbl_ml2_phyto = tbl_ml2.loc[:, ['Station', 'Tchla'] + list(tbl_ml2.loc[:, 'Diatoms':'Prochlorococcus'].columns)]

# Sum Cyano columns
tbl_ml2_phyto['Cyanobacteria'] = tbl_ml2_phyto['Synechococcus'] + tbl_ml2_phyto['Prochlorococcus']

# Drop Syn and Prochloro
tbl_ml2_phyto.drop(columns=['Synechococcus', 'Prochlorococcus'], inplace=True)

# Calculate percentage of each group in Tchla and create new columns
for col in tbl_ml2_phyto.columns:
    if col not in ['Station', 'Tchla']:
        tbl_ml2_phyto[f"{col}_P"] = tbl_ml2_phyto[col] / tbl_ml2_phyto['Tchla'] * 100
        
# Select stations and Phytoplankton columns
tbl_ml2_phyto_P = tbl_ml2_phyto.loc[:, ['Station'] + list(tbl_ml2_phyto.loc[:, 'Diatoms_P':'Cyanobacteria_P'].columns)]
tbl_ml2_phyto_P.info()


tbl_ml2_phyto_P_stats =  av_table(tbl_ml2_phyto_P,summary_type='median', d=1)
#Save df
output_filename = 'WC17_DataComp_PhytoPercent_median.xlsx'
tbl_ml2_phyto_P_stats.to_excel(output_filename, index=False)

#%%

# Calculate Percentage Phytoplankton for upper 150m

# Select stations and Phytoplankton columns
tbl_phyto = tbl.loc[:, ['Station', 'Depth','Tchla'] + list(tbl_ml2.loc[:, 'Diatoms':'Prochlorococcus'].columns)]

# Replace station codes with labels
tbl_phyto['Station_lbl'] = tbl_phyto['Station']
station_mapping = {'IO08': 'St. 41.0°S', 'IO07': 'St. 43.0°S', 'IO06': 'St. 45.5°S',
                   'IO05': 'St. 48.0°S', 'IO04': 'St. 50.6°S', 'IO03': 'St. 53.5°S',
                   'IO02': 'St. 56.0°S', 'IO01': 'St. 58.5°S'}
tbl_phyto['Station'] = tbl_phyto['Station_lbl'].replace(station_mapping)
tbl_phyto.drop(columns=['Station_lbl'], inplace=True)

# Sum Cyano columns
tbl_phyto['Cyanobacteria'] = tbl_phyto['Synechococcus'] + tbl_phyto['Prochlorococcus']

# Drop Syn and Prochloro
tbl_phyto.drop(columns=['Synechococcus', 'Prochlorococcus'], inplace=True)

# Calculate percentage of each group in Tchla and create new columns
for col in tbl_phyto.columns:
    if col not in ['Station', 'Tchla']:
        tbl_phyto[f"{col}_P"] = tbl_phyto[col] / tbl_phyto['Tchla'] * 100
        
# Select stations and Phytoplankton columns
tbl_phyto_P = tbl_phyto.loc[:, ['Station', 'Depth'] + list(tbl_phyto.loc[:, 'Diatoms_P':'Cyanobacteria_P'].columns)]
tbl_phyto_P.info()

#Save df
output_filename = 'WC17_DataComp_PhytoPercent_150m.xlsx'
tbl_phyto_P.to_excel(output_filename, index=False)


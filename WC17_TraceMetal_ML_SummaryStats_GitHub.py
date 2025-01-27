"""
WC17: Generate Summary Statistics for Mixed Layer Trace Metals & Metal Star

This script is related to the manuscript by Viljoen et al. (Preprint). 
For more details, refer to the project ReadMe: https://github.com/jjviljoen/Winter2017_PhytoNutrients_Python.

### Description
- This script generates tables with Medians and Median Absolute deviation (MAD) based on processed data.
- Before running this script, execute `WC17_01` to process the original data files which creates "WC17_TM_Comp_update.csv" used here.
- Required data: Two XLSX files available from Zenodo: https://doi.org/10.5281/zenodo.6615070.

### Author
Johan Viljoen - j.j.viljoen@exeter.ac.uk

### Last Updated
20 Jan 2025
"""

# %%

### IMPORT PACKAGES ###

import pandas as pd
from scipy.stats import describe, median_abs_deviation

# %%

# File name
file = "WC17_TM_Comp_update.csv"
# Read CSV
tbl = pd.read_csv(file)
tbl.info()

# %%

# Filter rows where ML is "IN"
tbl_ml = tbl[tbl['ML'] == 'IN']

# Remove Depth and ML columns
tbl_ml = tbl_ml.drop(columns=['ML'])

tbl_ml.info()

tbl_tm = tbl_ml.drop(
    columns=['Temp', 'Sal', 'Nitrate', 'Phosphate', 'Silicate'])

# %%

### SETUP TABLE FUNCTIONS ###


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
    m, s, a, b = describe(data).mean, describe(data).stddev, describe(
        data).minmax[0], describe(data).minmax[1]
    val = f'{dec_place(m, d)} ± {dec_place(s, d)} ({dec_place(a, d)} - {dec_place(b, d)})'
    return val


def mean_only(data, d):
    m = data.mean(skipna=True)
    # s = data.std(skipna=True)
    # val = f'{dec_place(m, d)} ± {dec_place(s, d)}'
    val = f'{dec_place(m, d)}'
    return val


def mean_sd(data, d):
    m = data.mean(skipna=True)
    s = data.std(skipna=True)
    val = f'{dec_place(m, d)} ± {dec_place(s, d)}'
    # val = f'{dec_place(m, d)}'
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


def av_table(df, summary_type='mean', d=2):
    # Read CSV file
    data = df
    # Calculate mean and standard deviation per column
    # d = 6  # Number of decimal places

    if summary_type == 'mean':
        data_av = data.groupby('Station').agg(lambda x: mean_only(x, d))
    elif summary_type == 'mean_sd':
        data_av = data.groupby('Station').agg(lambda x: mean_sd(x, d))
    elif summary_type == 'median':
        data_av = data.groupby('Station').agg(lambda x: median_tbl(x, d))
    elif summary_type == 'median_n':
        data_av = data.groupby('Station').agg(lambda x: median_tbl_n(x, d))
    else:
        raise ValueError("Invalid summary_type. Choose 'mean' or 'median'.")
    # Reverse the order of rows based on the 'Station' column
    data_av = data_av.sort_values(
        by='Station', ascending=True).reset_index(drop=False)

    return data_av

# %%


# Convert all columns (except 'Station') to float
for col in tbl_tm.columns:
    if col != 'Station':
        tbl_tm[col] = pd.to_numeric(tbl_tm[col], errors='coerce')

tbl_tm.info()

# Convert dCd from pmol to nmol
tbl_tm['dCd'] = tbl_tm['dCd']/1000

# Convert pMn from nmol to pmol
tbl_tm['pMn'] = tbl_tm['pMn']*1000

pTM_df = tbl_tm.copy()

# Reset index if needed
pTM_df = pTM_df.reset_index(drop=True)

# Remove Depth columns
tbl_tm = tbl_tm.drop(columns=['Depth', 'Latitude','Longitude','Cruise', 'Station Label',
                     'Station_ID', 'Sampling_date_UTC', 'Sampling_time_UTC'])
pTM_df = pTM_df.drop(columns=['Depth', 'Latitude','Longitude', 'Cruise', 'Station Label',
                     'Station_ID', 'Sampling_date_UTC', 'Sampling_time_UTC'])

# Replace station codes with labels
tbl_tm['Station_lbl'] = tbl_tm['Station']
pTM_df['Station_lbl'] = pTM_df['Station']
station_mapping = {'IO08': 'St. 41.0°S', 'IO07': 'St. 43.0°S', 'IO06': 'St. 45.5°S',
                   'IO05': 'St. 48.0°S', 'IO04': 'St. 50.6°S', 'IO03': 'St. 53.5°S',
                   'IO02': 'St. 56.0°S', 'IO01': 'St. 58.5°S'}
tbl_tm['Station'] = tbl_tm['Station_lbl'].replace(station_mapping)
tbl_tm.drop(columns=['Station_lbl'], inplace=True)
pTM_df['Station'] = pTM_df['Station_lbl'].replace(station_mapping)
pTM_df.drop(columns=['Station_lbl'], inplace=True)


tbl_summary_median = av_table(tbl_tm, summary_type='median')
#tbl_summary_mean_sd = av_table(tbl_tm, summary_type='mean_sd')
tbl_summary_mean = av_table(tbl_tm, summary_type='mean')

# %%
# pTM Summary Table
list_ratios = ['Station', 'pFe', 'pMn', 'pCo', 'pNi', 'pCu', 'pZn', 'pCd', 'pP']

tbl_pTm = av_table(pTM_df[list_ratios], summary_type='median_n')

# Save df
output_filename = 'WC17_TM_pTM_median.xlsx'
tbl_pTm.to_excel(output_filename, index=False)

# dTM Summary Table
list_ratios = ['Station', 'dFe', 'dMn', 'dCo', 'dNi', 'dCu', 'dZn', 'dCd']

tbl_dTm = av_table(pTM_df[list_ratios], summary_type='median_n')
# Save df
output_filename = 'WC17_TM_dTM_median.xlsx'
tbl_dTm.to_excel(output_filename, index=False)

# Select %pTM Lith
list_ratios = ['Station', '%pFe_lith', '%pMn_lith', '%pCo_lith',
               '%pNi_lith', '%pCu_lith', '%pZn_lith', '%pCd_lith']
tbl_pTm_lith = av_table(pTM_df[list_ratios], summary_type='median', d=0)
tbl_pTm_lith.info()

# Save df
output_filename = 'WC17_TM_pTM_Lith%_median.xlsx'
tbl_pTm_lith.to_excel(output_filename, index=False)

# %%

### METAL STAR TABLE ###

pTM_df.info()

tbl_summary_median = av_table(pTM_df, summary_type='median', d=1)

tbl_summary_median.info()


tbl_star = tbl_summary_median[['Station']].join(tbl_summary_median.iloc[:, 17:43])


## Create Metal Star Table for Paper
# stack results into one column
star_tbl_stack = pd.melt(tbl_star, id_vars=['Station'], var_name='Region/Phyto', value_name='TM*')

star_tbl_stack = star_tbl_stack.sort_values(
    ['Station', 'Region/Phyto'], ascending=[False, True])

# Unstack columns based on Metal
metal_list = ['Fe', 'Mn', 'Co', 'Ni', 'Cu', 'Zn', 'Cd']

# Create an empty dictionary to store the results for each metal
metal_results = {}

# Loop through each metal in metal_list
for metal in metal_list:
    # Filter columns for the current metal
    tbl_star_metal = tbl_star[['Station']].join(tbl_star.filter(like=metal))

    # Stack the data
    metal_stack = pd.melt(tbl_star_metal, id_vars=[
                          'Station'], var_name='Region/Phyto', value_name=f'{metal}*')

    # Sort the data
    metal_stack = metal_stack.sort_values(['Station'], ascending=[False])

    # Remove the metal prefix from column names
    metal_stack['Region/Phyto'] = metal_stack['Region/Phyto'].str.replace(
        f"{metal}*-", "")

    # Store the results in the dictionary
    metal_results[metal] = metal_stack

# Access the results for each metal using metal_results dictionary
# For example, metal_results['Fe'] will give the results for iron
# Access and create each metal DataFrame
star_Fe_stack = metal_results['Fe']
star_Mn_stack = metal_results['Mn']
star_Co_stack = metal_results['Co']
star_Ni_stack = metal_results['Ni']
star_Cu_stack = metal_results['Cu']
star_Zn_stack = metal_results['Zn']
star_Cd_stack = metal_results['Cd']

# Perform an outer join on 'Station' and 'Region/Phyto' columns
result_df = metal_results[metal_list[0]]
for metal in metal_list[1:]:
    result_df = result_df.merge(metal_results[metal], on=[
                                'Station', 'Region/Phyto'], how='outer')

# Print the resulting DataFrame
print(result_df.head(10))

# Drop rows where 'Region/Phyto' is "NA Bulk Flagellates"
result_df = result_df[result_df['Region/Phyto'] != "NA Bulk Flagellates"]

result_df = result_df.sort_values(
    ['Station', 'Region/Phyto'], ascending=[True, True])

# Reset the index
result_df = result_df.reset_index(drop=True)

# Save Metal Star Table to Excel
output_filename = 'WC17_TM_MetalStar_Table.xlsx'
result_df.to_excel(output_filename, index=False)

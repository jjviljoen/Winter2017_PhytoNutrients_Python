"""
WC17: Generate Correlation Tables for Winter 2017 phytoplankton & trace metal paralel sampled in upper 150m

This script analyzes data related to the manuscript by Viljoen et al. LINK 
For more details, refer to the project ReadMe: https://github.com/jjviljoen/Winter2017_PhytoNutrients_Python.

### Description
- This script generates correlation tables based on processed data.
- Before running this script, execute `WC17_01` to process the original data files which creates "WC17_DataComp_update.csv" used here.
- Required data: Two XLSX files available from Zenodo: https://doi.org/10.5281/zenodo.6615070.

### Author
Johan Viljoen - j.j.viljoen@exeter.ac.uk

### Last Updated
14 July 2025
"""

#%%

### IMPORT PACKAGES ###

import pandas as pd

from scipy.stats import kendalltau

#%%

#File name
file = "WC17_DataComp_update.csv"

# Read CSV
tbl = pd.read_csv(file)
tbl.info()

# Add a new column 'Cyanobacteria' as the sum of 'Synechococcus' and 'Prochlorococcus'
tbl['Cyanobacteria'] = tbl['Synechococcus'] + tbl['Prochlorococcus']

# Move the 'Cyanobacteria' column to be positioned after 'Prochlorococcus'
column_to_move = 'Cyanobacteria'
target_column = 'Prochlorococcus'

# Reorder the columns
columns = tbl.columns.tolist()
columns.remove(column_to_move)
columns.insert(columns.index(target_column) + 1, column_to_move)
tbl = tbl[columns]

# Display the updated DataFrame structure
print("Updated DataFrame structure:")
tbl.info()

# Select columns from 'Temp' to 'pAl' and create a new DataFrame
tbl_n = tbl.loc[:, 'Temp':'pAl']
tbl_n.info()

# Ensure only numeric columns are selected
tbl_numeric = tbl_n.select_dtypes(include='number')

# Remove rows with NaN values in the 'Tchla' column
tbl_numeric.dropna(subset=['Tchla'], inplace=True)

# Display the final numeric DataFrame
print("\nFinal numeric DataFrame after removing rows with NaN in 'Tchla':")
print(tbl_numeric.info())

#%%

df = tbl_numeric

# Calculate the Kendall correlation matrix and p-values
corr_matrix = df.corr(method=lambda x, y: kendalltau(x, y)[0], min_periods=1)
p_values = df.corr(method=lambda x, y: kendalltau(x, y)[1], min_periods=1)

# Save the correlation matrix dataframe to a CSV file
corr_matrix.to_csv("WC17_corr_kendall_matrix.csv", index=False)
p_values.to_csv("WC17_corr_kendall_P_values.csv", index=False)

# Initialize an empty dataframe for correlation counts
correlation_count = pd.DataFrame(index=df.columns, columns=df.columns)

# Calculate the Kendall correlation matrix and counts
for col1 in df.columns:
    for col2 in df.columns:
        if col1 != col2:
            correlation_count.loc[col1, col2] = df[[col1, col2]].dropna().shape[0]

# Save the sample count dataframe to a CSV file
correlation_count.to_csv('sample_count.csv')

# Create a stacked dataframe with Kendall correlation and p-values
corr_stacked_df = pd.DataFrame({
    'Variable 1': [var for var in corr_matrix.columns for _ in corr_matrix.columns],
    'Variable 2': [var for _ in corr_matrix.columns for var in corr_matrix.columns],
    'Kendall Correlation': corr_matrix.values.flatten(),
    'P-Value': p_values.values.flatten()
})

# Save the stacked dataframe to a CSV file
#corr_stacked_df.to_csv("WC17_corr_kendall_stacked.csv", index=False)

#Filter matrix columns for Table
tbl_numeric.info()
# List of columns to keep
columns_to_keep = ['Tchla', 'Diatoms','Phaeocystis','Coccolithophores','Dinoflagellates',
                   'Cryptophytes', 'Pelagophytes', 'Prasinophytes',
                   'Chlorophytes', 'Cyanobacteria']

# List of row indices to keep
rows_to_keep = ['Nitrate', 'Phosphate', 'Silica', 'dFe', 'pFe', 'dMn', 'pMn',
                'dCo', 'pCo', 'dZn', 'pZn', 'dCd', 'pCd', 'dNi', 'pNi',
                'dCu', 'pCu', 'pP']

# Filter DataFrame based on columns and rows
corr_tbl_paper = corr_matrix.loc[rows_to_keep, columns_to_keep]
p_tbl_paper = p_values.loc[rows_to_keep, columns_to_keep]
count_tbl_paper = correlation_count.loc[rows_to_keep, 'Tchla']

### Format table for significance ###
# Apply stars based on significance ranges

# Round all values in the significant matrix to 2 decimal places
significant_matrix = corr_tbl_paper.round(2).copy()

# Ensure the DataFrame can handle mixed data types (numeric and strings)
significant_matrix = significant_matrix.astype('object')

# Apply significance stars based on p-value ranges
significant_matrix = significant_matrix.mask(p_tbl_paper < 0.001, significant_matrix.where(p_tbl_paper < 0.001).map(lambda x: f'{x:.2f}***'))
significant_matrix = significant_matrix.mask((p_tbl_paper >= 0.001) & (p_tbl_paper < 0.01), significant_matrix.where((p_tbl_paper >= 0.001) & (p_tbl_paper < 0.01)).map(lambda x: f'{x:.2f}**'))
significant_matrix = significant_matrix.mask((p_tbl_paper >= 0.01) & (p_tbl_paper < 0.05), significant_matrix.where((p_tbl_paper >= 0.01) & (p_tbl_paper < 0.05)).map(lambda x: f'{x:.2f}*'))

#Below original code used for manuscript, but df.applymap depreciated, therefore placed with .where and .map functions above to achieve the same
# =============================================================================
# # Apply significance stars based on p-value ranges
# significant_matrix[p_tbl_paper < 0.001] = significant_matrix[p_tbl_paper < 0.001].applymap(lambda x: f'{x:.2f}***')
# significant_matrix[(p_tbl_paper >= 0.001) & (p_tbl_paper < 0.01)] = significant_matrix[(p_tbl_paper >= 0.001) & (p_tbl_paper < 0.01)].applymap(lambda x: f'{x:.2f}**')
# significant_matrix[(p_tbl_paper >= 0.01) & (p_tbl_paper < 0.05)] = significant_matrix[(p_tbl_paper >= 0.01) & (p_tbl_paper < 0.05)].applymap(lambda x: f'{x:.2f}*')
# significant_matrix.info()
# =============================================================================

print("Correlation matrix:")
print(significant_matrix)

#add cout to table
significant_matrix['n'] = count_tbl_paper

# Add a new column 'Nutrients' with the original index
significant_matrix['Nutrients'] = significant_matrix.index
# Reset the index of the dataframe and keep the original index as 'Nutrients'
significant_matrix = significant_matrix.reset_index(drop=True)

# Move 'Nutrients' column to the first position
significant_matrix = significant_matrix[['Nutrients'] + [col for col in significant_matrix.columns if col != 'Nutrients']]

#Save Table to Excel
output_filename = 'WC17_kendall_PaperTable.xlsx'
significant_matrix.to_excel(output_filename, index=False)

#%%

### TABLE WITH CORR HEATMAP ###

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === User‑tweakable settings ===
annotation_textsize = 11   # size for the τ+stars annotations
label_textsize      = 12   # size for tick labels
cbar_tick_textsize       = 12   # size for the colorbar label & ticks
cbar_title_textsize = 14      # size for the colorbar title (the τ symbol)
# Custom short names for the 10 columns (phytoplankton groups)
custom_columns = [
    'Tchla', 'Diatoms', 'Phaeo', 'Cocco', 'Dino',
    'Crypto', 'Pelago', 'Prasino', 'Chloro', 'Cyano'
]
# ================================

# --- assume corr_tbl_paper and p_tbl_paper are already defined ---

# 1) Build your annotation strings (τ rounded + stars)
def significance_stars(p):
    if pd.isnull(p):       return ''
    if p < 0.001:          return '***'
    if p < 0.01:           return '**'
    if p < 0.05:           return '*'
    return ''

stars = p_tbl_paper.applymap(significance_stars)
annot = corr_tbl_paper.round(2).astype(str).replace('nan','') + stars
annot = annot.fillna('')

# 2) Plot the heatmap without seaborn’s annot
fig, ax = plt.subplots(figsize=(12, 8))
sns.heatmap(
    corr_tbl_paper,
    cmap='vlag',
    center=0,
    annot=False,
    linewidths=0.5,
    cbar_kws={
        'label': r"Kendall’s $\tau$",
        'pad': 0.02
    },
    ax=ax
)

# 3) Manually annotate each cell
n_rows, n_cols = corr_tbl_paper.shape
for i in range(n_rows):
    for j in range(n_cols):
        txt = annot.iat[i, j]
        if not txt:
            continue
        weight = 'bold' if '*' in txt else 'normal'
        ax.text(
            j + 0.5,
            i + 0.5,
            txt,
            ha='center', va='center',
            color='black',
            fontsize=annotation_textsize,
            fontweight=weight
        )

# 4) Move x‑labels to top and set custom labels + sizes
ax.xaxis.tick_top()
ax.set_xticks(np.arange(n_cols) + 0.5)
ax.set_xticklabels(custom_columns, rotation=0, ha='center', fontsize=label_textsize)

# 5) Y‑labels
ax.set_yticklabels(corr_tbl_paper.index, rotation=0, fontsize=label_textsize)

# 6) Adjust colorbar font sizes
cbar = ax.collections[0].colorbar
cbar.ax.yaxis.set_tick_params(labelsize=cbar_tick_textsize)
cbar.ax.yaxis.label.set_size(cbar_title_textsize)

plt.tight_layout()

# 7) Save outputs
plt.savefig('kendall_correlation_heatmap.jpeg', dpi=300, format='jpeg', bbox_inches='tight')
plt.savefig('kendall_correlation_heatmap.pdf',  dpi=300, format='pdf', bbox_inches='tight')
plt.show()





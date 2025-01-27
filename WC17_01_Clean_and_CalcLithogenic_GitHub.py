"""
WC17: Import and Prepare XLSX Files for Analysis

This script processes XLSX files related to the manuscript by Viljoen et al., (Preprint) - see ReadMe at https://github.com/jjviljoen/Winter2017_PhytoNutrients_Python.

### Description
- Download the two xlsx files from Zenodo: https://doi.org/10.5281/zenodo.6615070

### Author
Johan Viljoen - j.j.viljoen@exeter.ac.uk

### Last Updated
20 Jan 2025
"""

#%%

### IMPORT PACKAGES ###

import pandas as pd

#%%

### TRACE METAL DATA (250m) - CLEAN & CALCULATE LITHOGENIC ###

# Import Trace Metal data xlsx file downloaded from Zenodo

# Specify the data file and sheet name
file_name = "WC17_TraceMetal_Comp_250m_Viljoen_Zenodo.xlsx"
sheet_name = "WC17_TM_Data_250m"

# Load the data
try:
    tbl = pd.read_excel(file_name, sheet_name=sheet_name)
    print("First few rows of the dataset:")
except FileNotFoundError:
    print(f"Error: File '{file_name}' not found. Ensure the file is in the script's directory or provide the correct path.")
    raise
except ValueError as e:
    print(f"Error loading the file: {e}")
    raise

# Display dataset structure
print("Dataset Information:")
tbl.info()

# Clean column names: Remove units, parentheses, and trailing spaces
tbl.columns = tbl.columns.str.replace(r'\s*\([^)]*\)\s*', '', regex=True)  # Remove content within parentheses
tbl.columns = tbl.columns.str.strip()  # Remove leading and trailing spaces

# Display updated dataset structure and column names
print("Cleaned Dataset Information:")
tbl.info()

#%%

### Calculate Lithogenic Fractions ###


# Equation for Lithogenic pTM calculation using crustal ratios
#pTM_lith_p = (pAl * ratio)/pTM * 100

def calc_pTM_lith(pAl, ratio_metal, pTM, result_type='percent'):
    """
    Calculate lithogenic particulate trace metal (pTM) fractions using pAl and crustal ratios 
    based on Rudnick and Gao (2013).

    Parameters:
    - pAl (float): Aluminum concentration in particulate matter.
    - ratio_metal (str): Metal for which lithogenic fraction is calculated. Options: 'Fe', 'Zn', 'Cd', 'Mn', 'Cu', 'Co', 'Ni'.
    - pTM (float): Total particulate trace metal concentration.
    - result_type (str): 'percent' to calculate lithogenic percentage, 'lith' for lithogenic fraction. Defaults to 'percent'.

    Returns:
    - float: Calculated lithogenic percentage or fraction, depending on `result_type`.

    Raises:
    - ValueError: If an invalid `ratio_metal` or `result_type` is provided.
    """
    ratios = {
        'Fe': 0.2323,
        'Zn': 0.00163,
        'Cd': 0.000001,
        'Mn': 0.00948, #Goa = 0.00948, Taylor & McLenna 1985 = 0.0034
        'Cu': 0.00034,
        'Co': 0.00021,
        'Ni': 0.00058
    }

    if ratio_metal not in ratios:
        raise ValueError(f"Invalid ratio element. Choose from: {', '.join(ratios.keys())}")

    selected_ratio = ratios[ratio_metal]

    # Step 1: Calculate the percentage lithogenic contribution
    percent_lith = (pAl * selected_ratio) / pTM * 100
    
    # Step 2: Cap the percentage at 100%
    percent_lith = min(percent_lith, 100)
    
    if result_type == 'percent':
        return percent_lith
    elif result_type == 'lith':
        # Step 3: Calculate lithogenic fraction, capped at total pTM
        lith_fraction = min(pAl * selected_ratio, pTM)
        return lith_fraction
    else:
        raise ValueError("Invalid result_type. Choose 'percent' or 'lith'.")

    #return result

#%%

# Calc Percent lithogenic vs total pTM
tbl['%pFe_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Fe', row['pFe'], result_type='percent'), axis=1)
tbl['%pMn_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Mn', row['pMn'], result_type='percent'), axis=1)
tbl['%pCo_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Co', row['pCo'], result_type='percent'), axis=1)
tbl['%pZn_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Zn', row['pZn'], result_type='percent'), axis=1)
tbl['%pCd_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Cd', row['pCd'], result_type='percent'), axis=1)
tbl['%pNi_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Ni', row['pNi'], result_type='percent'), axis=1)
tbl['%pCu_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Cu', row['pCu'], result_type='percent'), axis=1)

# Calc lithogenic pTM
tbl['pFe_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Fe', row['pFe'], result_type='lith'), axis=1)
tbl['pMn_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Mn', row['pMn'], result_type='lith'), axis=1)
tbl['pCo_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Co', row['pCo'], result_type='lith'), axis=1)
tbl['pZn_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Zn', row['pZn'], result_type='lith'), axis=1)
tbl['pCd_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Cd', row['pCd'], result_type='lith'), axis=1)
tbl['pNi_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Ni', row['pNi'], result_type='lith'), axis=1)
tbl['pCu_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Cu', row['pCu'], result_type='lith'), axis=1)

tbl.info()

#%%

### Subtract Lithogenic from total pTM

# First copy all pTM columns and rename to pTM_T for total pTM
tbl['pFe_T'] = tbl['pFe']
tbl['pMn_T'] = tbl['pMn']
tbl['pCo_T'] = tbl['pCo']
tbl['pZn_T'] = tbl['pZn']
tbl['pCd_T'] = tbl['pCd']
tbl['pNi_T'] = tbl['pNi']
tbl['pCu_T'] = tbl['pCu']
tbl.info()

# Subtract lithogenic from total pTM
tbl['pFe'] = tbl['pFe_T'] - tbl['pFe_lith'] 
tbl['pMn'] = tbl['pMn_T'] - tbl['pMn_lith'] 
tbl['pCo'] = tbl['pCo_T'] - tbl['pCo_lith'] 
tbl['pZn'] = tbl['pZn_T'] - tbl['pZn_lith']
tbl['pCd'] = tbl['pCd_T'] - tbl['pCd_lith']
tbl['pNi'] = tbl['pNi_T'] - tbl['pNi_lith']
tbl['pCu'] = tbl['pCu_T'] - tbl['pCu_lith']

tbl.info()

# =============================================================================
# #Recalculate pTM/P ratios
# tbl['pFe_P'] = tbl['pFe']/tbl['P']*1000
# tbl['pMn_P'] = tbl['pMn']/tbl['P']*1000
# tbl['pCo_P'] = tbl['pCo']/tbl['P']
# tbl['pZn_P'] = tbl['pZn']/tbl['P']*1000
# tbl['pCd_P'] = tbl['pCd']/tbl['P']
# tbl['pNi_P'] = tbl['pNi']/tbl['P']
# tbl['pCu_P'] = tbl['pCu']/tbl['P']
# =============================================================================

#%%
#Save df
output_filename = 'WC17_TM_Comp_update.csv'
tbl.to_csv(output_filename, index=False)

#%%

### DATA COMP (150m) - CLEAN & CALCULATE LITHOGENIC ###

# Import Trace Metal data xlsx file downloaded from Zenodo

# Specify the file name
file_name = "WC17_DataComp_150m_Viljoen_Zenodo.xlsx"

# Load the specific tab
sheet_name = "WC17_Data_150m"
try:
    tbl = pd.read_excel(file_name, sheet_name=sheet_name)
except FileNotFoundError:
    print(f"File '{file_name}' not found. Make sure it's in the same directory or provide the correct path.")
except ValueError as e:
    print(f"Error: {e}")
    
tbl.info()

# Clean column names: Remove units, brackets, and trailing spaces
tbl.columns = tbl.columns.str.replace(r'\s*\([^)]*\)\s*', '', regex=True)  # Remove content within parentheses
tbl.columns = tbl.columns.str.strip()  # Remove leading and trailing spaces

# Reset index if needed
tbl = tbl.reset_index(drop=True)

# Display the updated column
tbl.info()

#%%

# Calc Percent lithogenic vs total pTM
tbl['%pFe_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Fe', row['pFe'], result_type='percent'), axis=1)
tbl['%pMn_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Mn', row['pMn'], result_type='percent'), axis=1)
tbl['%pCo_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Co', row['pCo'], result_type='percent'), axis=1)
tbl['%pZn_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Zn', row['pZn'], result_type='percent'), axis=1)
tbl['%pCd_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Cd', row['pCd'], result_type='percent'), axis=1)
tbl['%pNi_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Ni', row['pNi'], result_type='percent'), axis=1)
tbl['%pCu_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Cu', row['pCu'], result_type='percent'), axis=1)

# Calc lithogenic pTM
tbl['pFe_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Fe', row['pFe'], result_type='lith'), axis=1)
tbl['pMn_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Mn', row['pMn'], result_type='lith'), axis=1)
tbl['pCo_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Co', row['pCo'], result_type='lith'), axis=1)
tbl['pZn_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Zn', row['pZn'], result_type='lith'), axis=1)
tbl['pCd_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Cd', row['pCd'], result_type='lith'), axis=1)
tbl['pNi_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Ni', row['pNi'], result_type='lith'), axis=1)
tbl['pCu_lith'] = tbl.apply(lambda row: calc_pTM_lith(row['pAl'], 'Cu', row['pCu'], result_type='lith'), axis=1)

tbl.info()

#%%

### Subtract Lithogenic from total pTM

# First copy all pTM columns and rename to pTM_T for total pTM
tbl['pFe_T'] = tbl['pFe']
tbl['pMn_T'] = tbl['pMn']
tbl['pCo_T'] = tbl['pCo']
tbl['pZn_T'] = tbl['pZn']
tbl['pCd_T'] = tbl['pCd']
tbl['pNi_T'] = tbl['pNi']
tbl['pCu_T'] = tbl['pCu']

# Subtract lithogenic from total pTM
tbl['pFe'] = tbl['pFe_T'] - tbl['pFe_lith'] 
tbl['pMn'] = tbl['pMn_T'] - tbl['pMn_lith'] 
tbl['pCo'] = tbl['pCo_T'] - tbl['pCo_lith'] 
tbl['pZn'] = tbl['pZn_T'] - tbl['pZn_lith']
tbl['pCd'] = tbl['pCd_T'] - tbl['pCd_lith']
tbl['pNi'] = tbl['pNi_T'] - tbl['pNi_lith']
tbl['pCu'] = tbl['pCu_T'] - tbl['pCu_lith']
tbl.info()

#%%

#Save df
output_filename = 'WC17_DataComp_update.csv'
tbl.to_csv(output_filename, index=False)

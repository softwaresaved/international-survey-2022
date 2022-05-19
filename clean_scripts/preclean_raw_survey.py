"""Cleans raw survey data (as a 'preclean' step) by correcting invalid characters and deleting
   unnecessary or sensitive columns. This step is done prior to a second cleaning step and analysis,
   with a confidential raw survey dataset that isn't present in this repository.
"""

import os
import sys
import re
import uuid
import numpy as np
import pandas as pd

# So we can load the prepare, survey and lib modules
sys.path.insert(1, '.')

from clean_scripts.cleaning import apply_actions
from survey.overview_and_sampling import read_salary


if not os.path.exists('data/2022-raw.csv'):
    print("Error: please ensure raw 2022 survey data file '2022-raw.csv' is present in 'data'")
    sys.exit(1)

# Clean characters of raw survey data
if not os.path.exists('cache'):
    os.makedirs('cache')

if not os.path.exists('data/intermediate'):
    os.makedirs('data/intermediate')

with open('data/intermediate/2022-clean-characters.csv', 'w') as fout:
    with open('data/2022-raw.csv', 'r') as fin:
        for line in fin:
            line = line.replace('&amp;', '&')
            fout.write(line)

# The precleaned new (2022) survey data
fix_df = pd.read_csv('data/intermediate/2022-clean-characters.csv', dtype=str, encoding='utf-8')
fix_df['Year'] = 2022

# The reference (2018) data to use
# We need to assemble it from its different parts
ref_df = pd.read_csv('data/2018.csv', encoding='utf-8')
ref_df = ref_df.merge(read_salary('data/2018_salary.csv'), on='startdate. Date started')

# Column processing
# Load mapping CSV which indicates what to do with each 2022 column
# to make the 2022 data compatible with the 2018 data
mapping_df = pd.read_csv('clean_scripts/survey_column_mapping.csv')

# Export salary data into separate CSV
# We need to fix the 'startdate' column to be unique, which it isn't,
# to ensure the salary data is merged correctly into the main dataset
# when preparing the data for analysis
STARTDATE_COL = 'startdate. Date started'
fix_df[STARTDATE_COL] = fix_df[STARTDATE_COL].map(lambda x: x + '==' + str(uuid.uuid4()))
sal_df = fix_df.loc[:, (fix_df.columns.str.startswith("socio4") | fix_df.columns.str.startswith(STARTDATE_COL))]
sal_df = sal_df.rename(columns={STARTDATE_COL: 'startdate._.Date started'})
sal_df.to_csv('data/2022_salary.csv', index=False)

# Focus on only deleting unnecessary or sensitive columns in this preclean step
actions_delete_df = mapping_df[mapping_df['Action'] == 'Delete']
apply_actions(fix_df, ref_df, actions_delete_df)

# The precleaned data, ready for the secondary cleaning step
fix_df.to_csv('data/intermediate/2022-precleaned.csv', index=False)

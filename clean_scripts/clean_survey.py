"""Prepare survey data (which has already been precleaned) so it is suitable for processing by the analysis code."""

import os
import sys
import numpy as np
import pandas as pd

# So we can load the prepare, survey and lib modules
sys.path.insert(1, '.')

from clean_scripts.cleaning import apply_actions

from survey.overview_and_sampling import read_salary
from survey.sociodemography import read_anonymised_data


SALARY_COL = 'socio4. Please select the range of your salary'
DEVEXP_COL = 'soft1can. How many years of software development experience do you have?'
PREVEMP1_COL = 'prevEmp1. Where was your previous job based?'
PREVEMP1_DE_COL = 'prevEmp1qde. Where was your previous job based?'
CURRENTEMP2_COL = 'currentEmp2. Which university do you work for?'

if not os.path.exists('data/intermediate/2022-precleaned.csv'):
    print("Error: please run 'clean_scripts/preclean_raw_survey.py' on raw survey data first")
    sys.exit(1)


# The cleaned new (2022) survey data
fix_df = pd.read_csv('data/intermediate/2022-precleaned.csv', encoding='utf-8')
fix_df['Year'] = 2022

# The reference (2018) data to use
# We need to assemble it from its different parts
ref_df = pd.read_csv('data/2018.csv', encoding='utf-8')
ref_df = ref_df.merge(read_salary('data/2018_salary.csv'), on='startdate. Date started')

# Column processing
# Go through mapping CSV which indicates what to do with each 2022 column
# to make the 2022 data compatible with the 2018 data
# For each 2022 column, this could be Ignore it, Rename it with a given name, or SearchReplace it
# which renames the column to match one in the 2018 data
mapping_df = pd.read_csv('clean_scripts/survey_column_mapping.csv')

# Apply the column processing actions (not the delete ones, since they would have been
# done during the prior preclean step)
actions_other_df = mapping_df[mapping_df['Action'] != 'Delete']
apply_actions(fix_df, ref_df, actions_other_df)


# Further cleaning - merging columns and other cleaning to match 2018 data format

# Drop all nan's in software dev experience column
fix_df[DEVEXP_COL] = fix_df[DEVEXP_COL].replace({'15+': '15'})

# Merge prevEmp1 into single column, as per 2018.csv
fix_df[PREVEMP1_COL] = (
    fix_df.loc[:, [PREVEMP1_COL, PREVEMP1_DE_COL]]
    .fillna("")
    .agg("".join, axis=1)
    .map(str.strip)
)
fix_df = fix_df.loc[:, ~fix_df.columns.str.startswith(PREVEMP1_DE_COL)]

# Merge currentEmp2 into single column, as per 2018.csv
fix_df[CURRENTEMP2_COL] = (
    fix_df.loc[:, fix_df.columns.str.startswith("currentEmp2q")]
    .fillna("")
    .agg("".join, axis=1)
    .map(str.strip)
)
fix_df = fix_df.loc[:, ~fix_df.columns.str.startswith("currentEmp2q")]

# Clean all prefer not to answer type answers
fix_df.replace('Prefer not to answer', np.NaN, inplace=True)
fix_df.replace('Do not wish to declare', np.NaN, inplace=True)
fix_df.replace('Do not wish to answer', np.NaN, inplace=True)
fix_df.replace("I don't know", np.NaN, inplace=True)
fix_df.replace("Don't want to answer", np.NaN, inplace=True)

# Clean all 'Other' answers, collapse them all into 'Yes'
# This also applies to a single socio5usqus question
# Applies to multiple-choice and single answer style questions
for col in fix_df.columns:
    if col[-7:] == '[Other]':
        # Replace all the values with 'Yes'
        fix_df[col] = fix_df[col].apply(lambda x: 'Yes' if not pd.isnull(x) else np.nan)

# The final, precleaned and cleaned data ready for analysis
fix_df.to_csv('data/2022.csv', index=False)

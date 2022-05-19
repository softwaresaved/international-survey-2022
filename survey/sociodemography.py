# Sociodemography
import sys
import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lib.analysis import get_previous_survey_year, count_diff, plot_cat_comparison
from lib.report import (
    slugify,
    make_report,
    read_cache,
    table_country,
    figure_country,
    COUNTRIES_WITH_WORLD,
)

age = ["socio3. Please select your age"]

age_order = [
    "18 to 24 years",
    "25 to 34 years",
    "35 to 44 years",
    "45 to 54 years",
    "55 to 64 years",
    "Age 65 or older",
    "Prefer not to say",
]

gender = ["socio2._.Please select your gender"]

ethn_us = ["socio5usqus._.Do you consider yourself Hispanic or Latino"]

disability = [
    "disa1._.Do you have a condition that is defined as a disability by your country?"
]


def read_anonymised_data(survey_year, data, fillna=None):
    df = pd.read_csv(data)
    if fillna:
        df = df.fillna(fillna)
    df["socio1._.In which country do you work?"].replace(
        {
            "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
            "United States of America": "United States",
        },
        inplace=True,
    )

    df['Year'] = survey_year
    return df.rename({'socio1._.In which country do you work?': 'Country'}, axis=1)


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):

    survey_prev_year = get_previous_survey_year(survey_year)

    ethnicity_df_year = read_anonymised_data(survey_year, 'data/' + str(survey_year) + '_ethnicity.csv')
    ethnicity_df_prev_year = read_anonymised_data(survey_prev_year, 'data/' + str(survey_prev_year) + '_ethnicity.csv')
    ethnicity_df = pd.concat([ethnicity_df_year, ethnicity_df_prev_year], ignore_index=True)
    # Fix: collapse multi-choice for socio5usqus into 'Yes' or 'No'
    ethnicity_df[ethn_us[0]] = ethnicity_df[ethn_us[0]].apply(lambda x: 'Yes' if not pd.isnull(x) and x.startswith('Yes,') else x)
    ethnicity_df[ethn_us[0]] = ethnicity_df[ethn_us[0]].apply(lambda x: 'No' if not pd.isnull(x) and x.startswith('No,') else x)
    ethnicity_df[ethn_us[0]] = ethnicity_df[ethn_us[0]].apply(lambda x: np.nan if not pd.isnull(x) and x == 'Do not wish to answer' else x)

    disability_df_year = read_anonymised_data(survey_year, 'data/' + str(survey_year) + '_disability.csv', fillna='No')
    disability_df_prev_year = read_anonymised_data(survey_prev_year, 'data/' + str(survey_prev_year) + '_disability.csv', fillna='No')
    disability_df = pd.concat([disability_df_year, disability_df_prev_year], ignore_index=True)

    gender_df_year = read_anonymised_data(survey_year, 'data/' + str(survey_year) + '_gender.csv')
    gender_df_prev_year = read_anonymised_data(survey_prev_year, 'data/' + str(survey_prev_year) + '_gender.csv')
    gender_df = pd.concat([gender_df_year, gender_df_prev_year], ignore_index=True)

    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        results = count_diff(
            gender_df, gender, country, "Gender", survey_year,
            order_index=False, disable_past_year=True
        )
        countries[-1].update(table_country(country, "gender", results))
        plot_cat_comparison(
            results, country=country, category="Gender", order_index=False
        )
        countries[-1].update(figure_country(country, "gender", plt))
        if country == "United Kingdom":
            category = 'Ethnicity'
            ethnicity_data = count_diff(
                ethnicity_df,
                [x for x in ethnicity_df.columns if x.startswith('socio5quk')],
                country, category, survey_year, multi_choice=True, disable_past_year=True
            )
            countries[-1].update(table_country(country, "ethnicity", ethnicity_data))
            plot_cat_comparison(ethnicity_data, country=country, category=category)
            countries[-1].update(figure_country(country, "ethnicity", plt))

            disability_data = count_diff(
                disability_df,
                disability,
                country,
                "Officially recognised disability",
                survey_year,
                y_n=True,
                disable_past_year=True
            )
            plot_cat_comparison(disability_data, country=country, category=category)
            countries[-1].update(figure_country(country, "disability", plt))
        if country == "United States":
            category = 'Whether Hispanic or Latino'
            hispanic_latino_data = count_diff(
                ethnicity_df, ethn_us, country, category, survey_year, y_n=True
            )
            countries[-1].update(
                table_country(country, "hispanic-or-latino", hispanic_latino_data)
            )
            plot_cat_comparison(
                hispanic_latino_data, country=country, category=category
            )
            countries[-1].update(figure_country(country, "hispanic-or-latino", plt))
    return {"countries": countries}


if __name__ == "__main__":
    run()

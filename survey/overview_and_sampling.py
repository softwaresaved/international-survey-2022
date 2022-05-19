#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from lib.analysis import get_previous_survey_year
from lib.report import table, figure, make_report, convert_time, write_cache, COUNTRIES


US_SALARY_COL = 'socio4qus._.Please select the range of your salary'
SALARY_COL = 'socio4. Please select the range of your salary'

PROJ5ZAF_GIT1_COL = 'proj5zaf. Which version control tools do you use for software development?. [Git]'
PROJ5ZAF_GIT2_COL = 'proj5zaf. Which version control tools do you use for software development?. [GIT]'

PREVEMP2_COLS = [
    'prevEmp2. Rank the following factors dependent on how strongly they influenced your decision to accept your current position. [Rank 6]',
    'prevEmp2. Rank the following factors dependent on how strongly they influenced your decision to accept your current position. [Rank 7]',
    'prevEmp2. Rank the following factors dependent on how strongly they influenced your decision to accept your current position. [Rank 8]',
]

EDU1_COL = "edu1. What is the highest level of education you have attained?"
EDU2_COL = "edu2. In which discipline is your highest academic qualification?"


def read_salary(data):
    """Converts any US 2018-style salary ranges to 2022 format and merges salary information from countries into a single column"""
    df = pd.read_csv(data, dtype=str)
    if US_SALARY_COL in df.columns:
        df[US_SALARY_COL].replace(
            {
                "Less than $30,000":         "< $30,000",
                "From $30,000 to $49,999":   "≥ $30,000 and < $49,999",
                "From $50,000 to $69,999":   "≥ $50,000 and < $69,999",
                "From $70,000 to $89,999":   "≥ $70,000 and < $89,999",
                "From $90,000 to $109,999":  "≥ $90,000 and < $109,999",
                "From $110,000 to $129,999": "≥ $110,000 and < $129,999",
                "From $130,000 to $149,999": "≥ $130,000 and < $149,999",
                "From $150,000 to $199,999": "≥ $150,000 and < $199,999",
                "More than $150,000":        "≥ $150,000",
            },
            inplace=True
        )
    df["socio4"] = (
        df.loc[:, df.columns.str.startswith("socio4")]
        .fillna("")
        .agg("".join, axis=1)
        .map(str.strip)
    )
    df = df[['startdate._.Date started', 'socio4']]
    df.columns = ['startdate. Date started', SALARY_COL]

    return df


@make_report(__file__)
def run(survey_year, data_year="data/2022.csv", data_prev_year="data/2018.csv"):
    """Prepares overview report and sampling.

    This function creates the figures and tables, as well as doing data
    transformations that are used in the other sections.
    """

    survey_prev_year = get_previous_survey_year(survey_year)

    df_year = pd.read_csv(data_year)
    df_year = df_year.merge(read_salary(data_year[:-4] + '_salary.csv'), on='startdate. Date started')

    # Fix: for 2022 data, remove uuid from startdate column (needed for prior salary data re-merging step)
    df_year['startdate. Date started'] = df_year['startdate. Date started'].map(lambda x: x[:x.index('==')])

    df_prev_year = pd.read_csv(data_prev_year)
    df_prev_year = df_prev_year.merge(read_salary(data_prev_year[:-4] + '_salary.csv'), on='startdate. Date started')
    df = pd.concat([df_year, df_prev_year], ignore_index=True)

    # The cleaning is about renaming some countries and create a globa category
    # for all countries that are not from one of the participating countries.

    # Rename the Uk and US
    df["socio1. In which country do you work?"].replace(
        {
            "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
            "United States of America": "United States",
        },
        inplace=True,
    )
    df = df[df["socio1. In which country do you work?"] != "Canada"]

    # Fix: extra cleaning, to move a duplicated column's contents into the actual column
    #df[PROJ5ZAF_GIT1_COL] = df[PROJ5ZAF_GIT1_COL] + df[PROJ5ZAF_GIT2_COL]
    df.drop(columns=[PROJ5ZAF_GIT2_COL], inplace=True)

    # Fix: remove superfluous previous employment ranking options
    df = df.drop(PREVEMP2_COLS, axis=1)

    # Create a category world

    # As said, we are concerned about some countries specifically. However, we
    # collected information about other countries as well. To avoid any
    # confusion and having too much countries to plot, we group all of them
    # into one category "world"

    # Create a new columns if "World" if the country is not in the list
    df["Country"] = df["socio1. In which country do you work?"].apply(
        lambda x: x if x in COUNTRIES else "World"
    )

    # This is the total of participants. A participants is defined as a person
    # that have reached, at least the second section in the survey.

    report = {"n_participants": len(df[df["Year"] == survey_year])}

    # Repartition per country

    # We developed specific questions for the following countries:
    # * Australia
    # * Canada (but host their own version of the survey so they will not be analysed here)
    # * Germany
    # * Netherlands
    # * New Zealand
    # * South Africa
    # * United Kingdom
    # * United States
    #
    # We can see the distribution of participants among the countries as follow

    country_of_work_c = "socio1. In which country do you work?"
    df_countries = (
        df[df["Year"] == survey_year][country_of_work_c]
        .value_counts()
        .to_frame()
        .reset_index()
        .sort_values([country_of_work_c, "index"], ascending=[False, True])
        # ^^ Sort descending by counts, but then ascending by country
        #    This makes the CSV reproducible
    )
    df_countries.columns = ["Country", "Count"]
    report.update(table("participant", df_countries, index=False))
    df_countries.columns = ["name", "count"]

    df["Date"] = df["startdate. Date started"].apply(lambda x: convert_time(x))
    df_submission_per_country = df[["Country", "Date"]]  # .dropna()
    total_per_country = (
        df_submission_per_country.groupby(["Country"])["Date"].value_counts().to_frame()
    )
    total_per_country.columns = ["Count"]
    total_per_country = total_per_country.reset_index().sort_values(
        ["Date", "Country"], ascending=True
    )

    fig, axes = plt.subplots(len(set(df.Country)), 1, figsize=(7, 9), sharex=True)
    fig.tight_layout()
    fig.subplots_adjust(left=0.1, bottom=0.15)
    list_plots = list()
    for i, name in enumerate(total_per_country["Country"].unique()):
        axes[i] = total_per_country[total_per_country.Country == name].plot(
            x="Date", y="Count", legend=False, ax=axes[i]
        )
        axes[i].set_title("{}".format(name))
        # axes[a, b].set_xticklabels(labels=idx)

        axes[i].xaxis.set_major_locator(mdates.DayLocator(interval=30))  # every 10 days
        axes[i].xaxis.set_minor_locator(mdates.DayLocator(interval=7))  # every day
        for label in axes[i].get_xticklabels():
            label.set_rotation(90)
        list_plots.append(axes[i])

    for ax in list_plots:
        ax.set(xlabel="Date of submission", ylabel="Count")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)

    report.update(figure("participation_date", plt))

    # Difference with the previous year

    # Several countries did the survey last year, here a summary of the
    # difference in the amount of participants.

    results = dict()
    for country in df[df["Year"] == survey_prev_year]["Country"].unique():
        current_year = df[df["Year"] == survey_year]["Country"].value_counts()[country]
        previous_year = df[df["Year"] == survey_prev_year]["Country"].value_counts()[
            country
        ]
        results[country] = {
            "%d" % survey_prev_year: previous_year,
            "%d" % survey_year: current_year,
        }
    diff_year_participants = pd.DataFrame.from_dict(results, orient="index")
    diff_year_participants[
        "Difference between %d and %d" % (survey_prev_year, survey_year)
    ] = (
        diff_year_participants["%d" % survey_year]
        - diff_year_participants["%d" % survey_prev_year]
    )
    report.update(table("difference_with_previous_year", diff_year_participants))

    # Plotting the difference
    fig, ax = plt.subplots()
    fig.subplots_adjust(left=0.2, bottom=0.125)
    ax = diff_year_participants.plot(kind="barh", ax=ax)
    ax.legend(loc="lower center", ncol=3, bbox_to_anchor=(0.5, -0.18))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    report.update(figure("difference_with_previous_year", plt))

    # Subsetting: selecting valid participants only

    # On the total of participants, we only want the participants that code
    # software during their work. We had a specific question for this purpose.
    # We asked the participants if they are writing software or if they are
    # leading a group of software developers. Each of these questions had the
    # possibility of Yes/No answer. Here the exact wording of the questions:
    #
    # * Do you write software for academic research as part of your job
    #
    # * Does the majority of your role comprise leading a group of software
    # developers or RSEs?
    #
    # We will only select the participants who answered `Yes` to at least one
    # question.

    # Get the count of Y/N for the software developers

    soft_dev = (
        df.groupby(["Year"])[
            "rse1. Do you write software for academic research as part of your job"
        ]
        .value_counts()
        .to_frame()
    )
    # Get the count of Y/N for the leader developers
    soft_lead = (
        df.groupby(["Year"])[
            "rse4de. Does the majority of your role comprise leading a group of software developers or RSEs?"
        ]
        .value_counts()
        .to_frame()
    )
    # Get the count for Y/N to any of the question
    df["any_rse"] = np.where(
        (
            df["rse1. Do you write software for academic research as part of your job"]
            == "Yes"
        )
        | (
            df[
                "rse4de. Does the majority of your role comprise leading a group of software developers or RSEs?"
            ]
        ),
        "Yes",
        "No",
    )
    soft_any = df.groupby(["Year"])["any_rse"].value_counts().to_frame()
    # Create one df
    result = pd.concat([soft_dev, soft_lead, soft_any], axis=1, sort=False)

    # Rename columns
    result.columns = [
        "Write software",
        "Lead a team of software developers",
        "At least one of the two",
    ]
    report.update(table("valid_participants", result))

    # For any further analysis, we remove the participants that answered 'No'
    # at both of the question to only keep the ones that have work involving
    # software development for both year to ensure a proper comparison.

    # Filtering the df
    df = df[df["any_rse"] == "Yes"]
    # drop the column `any_rse` as no use anymore
    df.drop(["any_rse"], axis=1, inplace=True)

    write_cache("processed_data", df)

    # This brings the number of participants analysed to:
    results = pd.DataFrame.from_dict(
        [
            {
                "Participants in %d"
                % (survey_prev_year): len(df[df["Year"] == survey_prev_year]),
                "Participants in %d" % survey_year: len(df[df["Year"] == survey_year]),
            }
        ]
    )
    report.update(table("participant_analysed", results))

    return report


if __name__ == "__main__":
    run()

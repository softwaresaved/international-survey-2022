# How time is spent
import sys
import collections
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # non-interactive
import matplotlib.pyplot as plt

from lib.analysis import plotting_time_likert
from lib.report import make_report, read_cache, figure_country, COUNTRIES_WITH_WORLD


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    # Information about time spent
    df_time_spent = df[df["Year"] == survey_year][
        [
            "Country",
            "time1can. On average, how much of your time is spent developing software?",
            "time2can. On average, how much of your time is spent on research",
            "time3can. On average, how much of your time is spent on management",
            "time4can. On average, how much of your time is spent on teaching",
            "time5can. On average, how much of your time is spent on other activities",
        ]
    ].copy()
    # Information about the time they wish to spend
    df_time_wish = df[df["Year"] == survey_year][
        [
            "Country",
            "timeLike6zaf. In an average month, how much time would you like to spend on software development?",
            "timeLike7zaf. In an average month, how much time would you like to spend on research",
            "timeLike8zaf. In an average month, how much time would you like to spend on management",
            "timeLike9zaf. In an average month, how much time would you like to spend on teaching",
            "timeLike10zaf. In an average month, how much time would you like to spend on other activities",
        ]
    ].copy()

    # Replace the value 1 (None at all) and 10 (all my time) into int
    df_time_spent.replace(
        {"\ufeff1 (None at all)": 1, "10 (All my time)": 10}, inplace=True
    )
    df_time_wish.replace(
        {"\ufeff1 (None at all)": 1, "10 (All my time)": 10}, inplace=True
    )

    # Create a new dataframe with the difference between what they do and what they wish
    # Create a dataframe to show the difference
    dict_time_diff = collections.OrderedDict()
    dict_time_diff["Country"] = df_time_spent["Country"]
    dict_time_diff["Software Development difference"] = df_time_wish[
        "timeLike6zaf. In an average month, how much time would you like to spend on software development?"
    ].astype(float) - df_time_spent[
        "time1can. On average, how much of your time is spent developing software?"
    ].astype(
        float
    )
    dict_time_diff["Research difference"] = df_time_wish[
        "timeLike7zaf. In an average month, how much time would you like to spend on research"
    ].astype(float) - df_time_spent[
        "time2can. On average, how much of your time is spent on research"
    ].astype(
        float
    )
    dict_time_diff["Management difference"] = df_time_wish[
        "timeLike8zaf. In an average month, how much time would you like to spend on management"
    ].astype(float) - df_time_spent[
        "time3can. On average, how much of your time is spent on management"
    ].astype(
        float
    )
    dict_time_diff["Teaching difference"] = df_time_wish[
        "timeLike9zaf. In an average month, how much time would you like to spend on teaching"
    ].astype(float) - df_time_spent[
        "time4can. On average, how much of your time is spent on teaching"
    ].astype(
        float
    )
    dict_time_diff["Other activity difference"] = df_time_wish[
        "timeLike10zaf. In an average month, how much time would you like to spend on other activities"
    ].astype(float) - df_time_spent[
        "time5can. On average, how much of your time is spent on other activities"
    ].astype(
        float
    )
    df_time_diff = pd.DataFrame.from_dict(dict_time_diff)

    renaming_col = [
        "Country",
        "Developing software",
        "Research",
        "Management",
        "Teaching",
        "Other activities",
    ]
    df_time_spent.columns = renaming_col
    df_time_wish.columns = renaming_col
    df_time_diff.columns = renaming_col

    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        plotting_time_likert(
            country, df_time_spent, df_time_wish, df_time_diff, dict_time_diff
        )
        countries[-1].update(figure_country(country, "how-time-is-spent", plt))
    return {"countries": countries}


if __name__ == "__main__":
    run()

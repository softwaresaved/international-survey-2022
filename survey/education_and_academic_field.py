import sys
import numpy as np
import matplotlib.pyplot as plt

from lib.analysis import count_diff, plot_cat_comparison, plot_wordcloud
from lib.report import (
    table,
    figure,
    make_report,
    read_cache,
    table_country,
    figure_country,
    COUNTRIES,
)

EDU1_COL = "edu1. What is the highest level of education you have attained?"
EDU2_COL = "edu2. In which discipline is your highest academic qualification?"

@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    plt.rcParams["figure.figsize"] = [20.0, 10.0]
    report = {}

    education_column = "edu1. What is the highest level of education you have attained?"
    education_level_category = "Highest level of education"
    education_level = []
    df = read_cache("processed_data")

    # Fix: merge multiple 2022 edu1 by-country columns into singular edu1 column, like 2018
    df[EDU1_COL] = (
        df.loc[:, df.columns.str.startswith("edu1")]
        .fillna("")
        .agg("".join, axis=1)
        .map(str.strip)
    )

    # Fix: merge both edu2 columns, to ensure Australia data is included in analysis
    df[EDU2_COL] = (
        df.loc[:, df.columns.str.startswith("edu2")]
        .fillna("")
        .agg("".join, axis=1)
        .map(str.strip)
    )

    for country in COUNTRIES:
        education_level.append({"country": country})
        result = count_diff(
            df,
            columns=education_column,
            category=education_level_category,
            country=country,
            survey_year=survey_year
        )
        education_level[-1].update(table_country(country, "education_level", result))
        plot_cat_comparison(result, country, education_level_category)
        education_level[-1].update(figure_country(country, "education_level", plt))

    # Rest of the World
    education_level.append({"country": "Rest of the World"})

    # For the rest of the world, the question is a `free text` type.
    # Therefore, some cleaning are needed to render the results
    # intelligible. After manually cleaning the data, it appears that a
    # vast majority of participants hold a PhD (64%), while 14% have a
    # Master degree and only 9% have an Undergraduate degree.

    clean_education_levels = {
        "phd": "Doctorate",
        "phd in progress": "Doctorate",
        "mphil to phd transfer": "Doctorate",
        "dr phil": "Doctorate",
        "master of science": "Master degree",
        "master": "Master degree",
        "masters": "Master degree",
        "master in science": "Master degree",
        "postgraduate": "Master degree",
        "msc": "Master degree",
        "bachelors degree": "Undergraduate degree",
        "bachelors  in computer science": "Undergraduate degree",
        "bachelor": "Undergraduate degree",
        "bachelors": "Undergraduate degree",
        "nan": np.NaN,
    }
    df.loc[df["Country"] == "World", education_column] = (
        df.loc[df["Country"] == "World", education_column]
        .str.replace(".", "", regex=False)
        .str.replace("'", "", regex=False)
        .str.replace("degree", "", regex=False)
        .str.strip()
        .str.lower()
    )
    df.loc[df["Country"] == "World", education_column] = df.loc[
        df["Country"] == "World", education_column
    ].replace(clean_education_levels)

    result = count_diff(
        df, columns=education_column, category=education_level_category, country="World",
        survey_year=survey_year
    )
    education_level[-1].update(table_country("World", "education_level", result))
    plot_cat_comparison(result, "World", education_level_category)
    education_level[-1].update(figure_country("World", "education_level", plt))
    report["education_level"] = education_level

    # Comparison between countries

    # Even if the countries have different education levels, it is possible
    # to match them on the common "Doctorate" and "Master degree".
    # Therefore we compare them with these two equivalent levels and merge
    # all others under the category "other".

    # Create dictionary to replace values. These values may not be present
    # in the current df but are present in the potential answers

    dict_values = {
        "PhD": "Doctorate",
        "AQF 10 - Doctoral Degree": "Doctorate",
        "HBO (Hoger beroepsonderwijs) Master": "Master degree",
        "WO (Wetenschappelijk onderwijs) Master": "Master degree",
        "AQF 9 - Masters Degree": "Master degree",
    }
    list_value_to_keep = ["Doctorate", "Master degree", np.NaN]

    # Replace the value in education
    df["education comparison"] = df[education_column].replace(dict_values)

    # Create a new columns if "World" if the country is not in the list
    def merge_edu(x):
        if x in list_value_to_keep:
            return x
        elif x == np.NaN:
            return x
        else:
            return "Other"

    # Apply the function to a new columns
    df["education comparison"] = df["education comparison"].apply(merge_edu)

    # Count the values per countries
    df_edu_comparison = (
        df[["Country", "education comparison"]]
        .groupby("Country")["education comparison"]
        .value_counts()
        .rename("Total count")
        .reset_index()
    )

    # Add a percentage of each type of diploma per countries
    df_edu_comparison["Percentage per countries"] = (
        df_edu_comparison["Total count"]
        / df_edu_comparison.groupby("Country")["Total count"].transform("sum")
        * 100
    ).round(2)

    # Display the results
    report.update(table("compare_education_level", df_edu_comparison))

    # In[22]:
    fig, ax = plt.subplots(figsize=(6, 8))
    df_plot = df_edu_comparison.pivot(
        index="Country",
        columns="education comparison",
        values="Percentage per countries",
    )
    df_plot.plot(
        kind="barh",
        title="Percentage of Doctorate and Master per country",
        grid=False,
        ax=ax,
    ).legend(loc='lower center', ncol=3, bbox_to_anchor=(0.5, -0.15))

    ax.set(xlabel="Percentage", ylabel="Country")

    ax.invert_yaxis()  # when barh option, the bars are inverted
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    for p in ax.patches:
        if int(round(p.get_width())) > 0:
            ax.annotate(
                str(int(round(p.get_width()))),
                (p.get_x() + p.get_width(), p.get_y() + p.get_height() / 2 - 0.1),
                xytext=(5, -9), fontsize=8,
                textcoords="offset points",
            )
    report.update(figure("compare_education_level", plt))

    # Academic field for education and professional development

    # Alongside of question about education level we also asked the
    # participants in which field they finished their highest level of
    # education. Here again the propositions were specific to each
    # countries so the comparison is difficult despite lot of overlapping
    # in the categories.

    # There are numbers in some of the fields, removing them as they are not needed

    academic_field_edu = []
    academic_field_q = (
        "edu2. In which discipline is your highest academic qualification?"
    )

    def remove_digit(s):
        try:
            return "".join([i for i in s if not i.isdigit()])
        except TypeError:
            return s

    df["Academic field"] = df[academic_field_q].apply(remove_digit)
    academic_field_edu_col = "Academic field"
    academic_field_edu_cat = "Field of education"

    prof_qual = [
        "edu4. List any professional qualifications you hold (eg. P. Eng, PMP, …)?"
    ]

    for country in COUNTRIES + ["World"]:
        academic_field_edu.append({"country": country})
        result = count_diff(
            df,
            columns=academic_field_edu_col,
            category=academic_field_edu_cat,
            country=country,
            survey_year=survey_year
        )
        academic_field_edu[-1].update(
            table_country(country, "academic_field_edu", result)
        )
        if len(result.index) > 0:
            plot_cat_comparison(result, country, academic_field_edu_cat)
            academic_field_edu[-1].update(
                figure_country(country, "academic_field_edu", plt)
            )
        plot_wordcloud(
            df,
            country=country,
            category="Professional qualification",
            columns=prof_qual,
            survey_year=survey_year
        )
        academic_field_edu[-1].update(
            figure_country(country, "academic_field_edu_wordcloud", plt)
        )

    # Academic field of work

    # Getting all the questions about the academic field of the current employment.
    academic_field_work_cols = [x for x in df.columns if x[:12] == "currentEmp13"]
    academic_field_work_cat = "field of work"

    academic_field_work = []
    for country in COUNTRIES + ["World"]:
        academic_field_work.append({"country": country})
        result = count_diff(
            df,
            columns=academic_field_work_cols,
            category=academic_field_work_cat,
            country=country,
            survey_year=survey_year,
            multi_choice=True,
        )
        academic_field_work[-1].update(
            table_country(country, "academic_field_work", result)
        )
        plot_cat_comparison(result, country, academic_field_work_cat)
        academic_field_work[-1].update(
            figure_country(country, "academic_field_work", plt)
        )

    report.update(
        {
            "education_level": education_level,
            "academic_field_edu": academic_field_edu,
            "academic_field_work": academic_field_work,
        }
    )
    return report


if __name__ == "__main__":
    run()

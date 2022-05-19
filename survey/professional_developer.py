# Professional development
import sys
import matplotlib.pyplot as plt

from lib.analysis import count_diff, plot_cat_comparison, plot_density_func, describe_diff
from lib.report import (
    make_report,
    read_cache,
    table_country,
    figure_country,
    COUNTRIES_WITH_WORLD,
)


prof_dev = ["soft2can. Do you consider yourself a professional software developer?"]
year_dev = ["soft1can. How many years of software development experience do you have?"]

prof_dev_cat = "Professional developer"
year_dev_cat = "How many years of software development experience"


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        prof_dev_data = count_diff(
            df,
            prof_dev,
            category=prof_dev_cat,
            country=country,
            survey_year=survey_year,
            y_n=True,
        )
        countries[-1].update(
            table_country(country, "proportion-professional-developer", prof_dev_data)
        )
        plot_cat_comparison(prof_dev_data, country, prof_dev_cat)
        countries[-1].update(
            figure_country(country, "proportion-professional-developer", plt)
        )

        countries[-1].update(
            table_country(
                country,
                "summary-years-professional-developer",
                describe_diff(
                    df,
                    year_dev,
                    country=country,
                    category=year_dev_cat,
                    survey_year=survey_year,
                ),
            )
        )
        plot_density_func(
            df,
            year_dev,
            country=country,
            category=year_dev_cat,
            survey_year=survey_year,
        )
        countries[-1].update(
            figure_country(country, "density-years-professional-developer", plt)
        )
    return {"countries": countries}


if __name__ == "__main__":
    run()

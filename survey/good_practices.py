# Good practices
import sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lib.analysis import count_diff, plot_cat_comparison, plot_wordcloud
from lib.report import (
    slugify,
    make_report,
    read_cache,
    table_country,
    figure_country,
    COUNTRIES_WITH_WORLD,
)

bus_factor = [
    "stability1. What is the bus factor of your most important software project? (The bus factor designates the minimal number of developers that have to be hit by a bus (or quit) before a project is incapacitated)"
]

transition_plan = [
    "stability2. Do the projects you work on typically have a plan to cope with developers leaving the group?"
]

order_testing = [
    "No formal testing",
    "No formal testing but users provide feedback",
    "The developers do their own testing",
    "Test engineers conduct testing",
    "Automated testing with continuous integration",
    "Don't know",
]

repo_tool = [
    "proj6zaf. Which online collaboration tools and open repositories do you use for software development?"
]


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")

    version_control = [x for x in df.columns if x[:8] == "proj5zaf"]
    testing = [x for x in df.columns if x[:8] == "proj4can"]
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        for category, columns, kwargs in [
            ("Bus factor", bus_factor, {"order_index": True}),
            ("Presence of transition plan", transition_plan, {"y_n": True}),
            ("Use of version control", version_control, {"multi_choice": True}),
            (
                "Testing strategies",
                testing,
                {"multi_choice": True, "order_index": order_testing},
            ),
        ]:
            results = count_diff(df, columns, country, category, survey_year, **kwargs)
            countries[-1].update(table_country(country, slugify(category), results))
            plot_cat_comparison(
                results,
                country=country,
                category=category,
                order_index=kwargs.get("order_index", False),
            )
            countries[-1].update(figure_country(country, slugify(category), plt))

        plot_wordcloud(df, repo_tool, country, "Repository", survey_year)
        countries[-1].update(figure_country(country, "repository-wordcloud", plt))
    return {"countries": countries}


if __name__ == "__main__":
    run()

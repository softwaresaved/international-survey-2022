# Tools and programming languages
import sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lib.analysis import count_diff, plot_cat_comparison
from lib.report import (
    slugify,
    make_report,
    read_cache,
    table_country,
    figure_country,
    COUNTRIES_WITH_WORLD,
)


os = ["tool2. Which operating system do you primarily use for development?"]


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    prog_lang = [x for x in df.columns if x[:8] == "tool4can"]
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        for category, columns, kwargs in [
            ("Programming languages", prog_lang, {"multi_choice": True}),
            ("Operating systems", os, {}),
        ]:
            results = count_diff(df, columns, country, category, survey_year, **kwargs)
            countries[-1].update(table_country(country, slugify(category), results))
            plot_cat_comparison(results, country=country, category=category, width=8)
            countries[-1].update(figure_country(country, slugify(category), plt))
    return {"countries": countries}


if __name__ == "__main__":
    run()

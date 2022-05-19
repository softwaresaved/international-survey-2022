# Open source and DOI
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

# Open source and DOI
open_use = ["open1can. How often do you use an open-source licence for your software?"]

order_open = [
    "1 (None at all)",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10 (All the time)",
]

ref_soft = [
    "open2de. How often do you reference software directly or the papers describing the software?"
]

doi = [
    "open3can. How often do you associate your software with a Digital Object Identifier (DOI)?"
]

doi_tools = [
    "open3de. Which tools do you use to mint a DOI (e.g. local library, Zenodo)?"
]

orcid = ["open1de. Do you have an ORCID ID?"]


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        for category, columns in [
            ("Open source use", open_use),
            ("Citation of software", ref_soft),
            ("Use of Digital Object Identifier", doi),
        ]:
            results = count_diff(
                df, columns, country, category, survey_year, order_index=order_open
            )
            countries[-1].update(table_country(country, slugify(category), results))
            plot_cat_comparison(
                results, country=country, category=category, order_index=order_open
            )
            countries[-1].update(figure_country(country, slugify(category), plt))

            plot_wordcloud(
                df,
                doi_tools,
                country,
                "Which tool is used for Digital Object Identifier",
                survey_year,
            )
            countries[-1].update(
                figure_country(country, "tool-used-for-doi-wordcloud", plt)
            )

            results = count_diff(
                df, orcid, country, "Using ORCID", survey_year, y_n=True
            )
            countries[-1].update(table_country(country, "using-orcid", results))
            plot_cat_comparison(results, country=country, category="Using ORCID")
            countries[-1].update(figure_country(country, "using-orcid", plt))
    return {"countries": countries}


if __name__ == "__main__":
    run()

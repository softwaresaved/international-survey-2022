# Collaboration and training
import sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lib.analysis import (
    count_diff,
    plot_cat_comparison,
    plot_density_func,
    describe_diff,
    plot_wordcloud,
)
from lib.report import (
    make_report,
    read_cache,
    table_country,
    figure_country,
    COUNTRIES_WITH_WORLD,
)


people_code = ["rse3. Who uses the code that you write?"]

same_researcher = [
    "currentWork1. Do you always work with the same researchers, or do you regularly change the researchers you work with?"
]
dedicated_research = [
    "currentWork2. Are you part of a dedicated research software group within your institution?"
]

nbr_proj_soft = ["proj1can. How many software projects are you currently involved in?"]

nbr_dev_proj = [
    "proj2can. How many software developers typically work on your projects?"
]

training_time = [
    "train2. On average, how many times a year do you take part in providing training?"
]
training_name = [
    "train3. What training programs are you involved with (comma separated list, e.g., Software Carpentry, local university training, etc.)"
]


training_time_category = "Number of time per year providing training"


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        for category, columns in [
            ("developing code for others", people_code),
            ("Working with same researchers", same_researcher),
            ("member of a dedicated group", dedicated_research),
            ("Number of software projects", nbr_proj_soft),
            ("Number of software developers per projects", nbr_dev_proj),
        ]:
            slug = category.lower().replace(" ", "-")
            result = count_diff(
                df, columns, country, category, survey_year, order_index=True
            )
            countries[-1].update(table_country(country, slug, result))
            plot_cat_comparison(
                result, country=country, category=category, order_index=True
            )
            countries[-1].update(figure_country(country, slug, plt))

        training_time_cat = "Number of time per year providing training"
        training_time_data = describe_diff(
            df, training_time, country, training_time_cat, survey_year
        )
        countries[-1].update(
            table_country(country, "training-frequency", training_time_data)
        )
        plot_density_func(
            df,
            training_time,
            country=country,
            category=training_time_cat,
            survey_year=survey_year,
        )
        countries[-1].update(figure_country(country, "training-frequency", plt))
        plot_wordcloud(df, training_name, country, training_time_cat, survey_year)
        countries[-1].update(figure_country(country, "training-name-wordcloud", plt))
    return {"countries": countries}


if __name__ == "__main__":
    run()

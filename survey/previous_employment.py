# Professional development
import sys
import matplotlib

matplotlib.use("Agg")  # non-interactive
import matplotlib.pyplot as plt

from lib.analysis import count_diff, plot_cat_comparison, plot_ranking, count_ranking
from lib.report import (
    make_report,
    read_cache,
    table_country,
    figure_country,
    COUNTRIES_WITH_WORLD,
)


prev_work = ["prevEmp1. Where was your previous job based?"]


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    reason_choice = [x for x in df.columns if x[:8] == "prevEmp2"]
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        where_prev_job_cat = "Where the previous job was based"
        where_prev_job = count_diff(
            df, prev_work, country, where_prev_job_cat, survey_year
        )
        if where_prev_job.empty:  # no data collected for this country, skip
            countries.pop()
            continue
        countries[-1].update(
            table_country(country, "where-previous-job-based", where_prev_job)
        )
        plot_cat_comparison(
            where_prev_job, country=country, category=where_prev_job_cat
        )
        countries[-1].update(figure_country(country, "where-previous-job-based", plt))
        ranking_cat = "Reasons to choose current job"
        ranking = count_ranking(df, reason_choice, country, ranking_cat, survey_year)

        countries[-1].update(
            table_country(country, "reasons-to-choose-current-job", ranking)
        )
        if len(ranking.index) > 0:
            plot_ranking(ranking, ranking_cat, country)
            countries[-1].update(
                figure_country(country, "reasons-to-choose-current-job", plt)
            )
    return {"countries": countries}


if __name__ == "__main__":
    run()

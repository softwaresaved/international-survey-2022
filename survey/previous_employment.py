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
reasons_choose_job = "prevEmp2. Rank the following factors dependent on how strongly they influenced your decision to accept your current position. [Rank 1]"


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
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

        # Fix: change overcomplicated ranking char to simple bar chart
        reasons_cat = "Top reason to choose current job"
        reasons = count_diff(df, reasons_choose_job, country, reasons_cat, survey_year)

        countries[-1].update(
            table_country(country, "reasons-to-choose-current-job", reasons)
        )
        if len(reasons.index) > 0:
            #plot_ranking(ranking, ranking_cat, country)
            plot_cat_comparison(reasons, country=country, category=reasons_cat)
            countries[-1].update(
                figure_country(country, "reasons-to-choose-current-job", plt)
            )
    return {"countries": countries}


if __name__ == "__main__":
    run()

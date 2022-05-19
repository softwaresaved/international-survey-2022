# Publications and citations
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

paper = [
    "paper2mod. In general, when your software contributes to a paper, are you acknowledged in that paper?"
]
order_paper = [
    "Not mentioned at all",
    "Acknowledged in the main text",
    "Acknowledged in acknowledgements section",
    "Named as co-author",
    "Named as main author",
]

conf1 = ["conf1can. Have you presented your software work at a conference or workshop?"]

conf2 = [
    "conf2can. At which conference(s)/workshop(s) have you presented your software work?"
]

ack_paper_cat = "Acknowledgment in paper"
did_you_participate_cat = "Did you participate in conference"


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})

        ack_paper = count_diff(
            df, paper, country, ack_paper_cat, survey_year, order_index=order_paper
        )
        countries[-1].update(table_country(country, slugify(ack_paper_cat), ack_paper))
        plot_cat_comparison(
            ack_paper, country=country, category=ack_paper_cat, order_index=order_paper
        )
        countries[-1].update(figure_country(country, slugify(ack_paper_cat), plt))

        did_you_participate = count_diff(
            df, conf1, country, did_you_participate_cat, survey_year, y_n=True
        )
        countries[-1].update(
            table_country(
                country, slugify(did_you_participate_cat), did_you_participate
            )
        )
        plot_cat_comparison(
            did_you_participate, country=country, category=did_you_participate_cat
        )
        countries[-1].update(
            figure_country(country, slugify(did_you_participate_cat), plt)
        )
        plot_wordcloud(df, conf2, country, did_you_participate_cat, survey_year)
        countries[-1].update(figure_country(country, "conference-name-wordcloud", plt))
    return {"countries": countries}


if __name__ == "__main__":
    run()

# Professional development
import sys
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


rse_member = [
    "ukrse1. Are you a member of an association of Research Software Developers (e.g. AUS-RSE, CANARIE, DE-RSE, NZ_RSE, UK RSE, …)?"
]
rse_joining = ["org1can. Would you be interested in joining such an organisation?"]
rse_conf = [
    "ukrse12de. Would you like to attend a conference about software development in academia?"
]
skill_learn = [
    "ukrse3. How did you learn the skills you need to become an Research Software Engineer / Research Software Developer?"
]
skill_improve = [
    "skill2. What three skills would you like to acquire or improve to help your work as a Research Software Engineer/ Research Software Developer? The skills can be technical and non-technical."
]


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    orga_wish = [x for x in df.columns if x[:7] == "org2can"]
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        for category, columns, kwargs in [
            ("RSE Member", rse_member, {"y_n": True}),
            ("Joining a RSE/RSD association", rse_joining, {"y_n": True}),
            (
                "What is important for such an organisation",
                orga_wish,
                {"multi_choice": True},
            ),
            ("Attending a national conference of RSE/RSD", rse_conf, {"y_n": True}),
        ]:
            results = count_diff(df, columns, country, category, survey_year, **kwargs)
            countries[-1].update(table_country(country, slugify(category), results))
            if len(results.columns) > 0:
                plot_cat_comparison(results, country=country, category=category)
                countries[-1].update(figure_country(country, slugify(category), plt))

        plot_wordcloud(
            df, skill_learn, country, "Learning skill to become a RSE/RSD", survey_year
        )
        countries[-1].update(
            figure_country(country, "learning-skills-rse-rsd-wordcloud", plt)
        )
        plot_wordcloud(
            df, skill_improve, country, "Which skill to improve as RSE/RSD", survey_year
        )
        countries[-1].update(
            figure_country(country, "which-skills-to-improve-rse-rsd-wordcloud", plt)
        )
    return {"countries": countries}


if __name__ == "__main__":
    run()

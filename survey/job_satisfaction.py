# Job satisfaction
import sys
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from lib.analysis import plotting_likert
from lib.report import (
    slugify,
    make_report,
    read_cache,
    figure_country,
    COUNTRIES_WITH_WORLD,
)

satis_gen = [
    "satisGen1. In general, how satisfied are you with your current position",
    "satisGen2. In general, how satisfied are you with your career",
]

recog = [
    "recog1. Do you feel that your contribution to research is recognised by your supervisor/line manager",
    "recog2. Do you feel that your contribution to research is recognised by the researchers you work with",
    "recog3. Do you feel that your contribution to research is recognised by your institution?",
]

turn_over1 = ["turnOver3. How often do you consider leaving your job?"]
turn_over2 = ["turnOver6. I would accept another job at the same compensation level if I was offered it"]

perc_emp = [
    "percEmp1. It would not be very difficult for me to get an equivalent job in a different institution",
    "percEmp3. My experience is in demand on the labour market",
]

prog_rse = [
    "progRSE1. It is likely that I will gain a promotion within my current group",
    "progRSE2. The process I have to complete to gain a promotion is clear and understandable",
    "progRSE3. There are many opportunities within my chosen career plan",
    "progRSE5. It is likely that my next position will be an Research Software Engineer / Research Software Developer role",
]

agree_scale = [
    "Strongly disagree",
    "Disagree",
    "Neither agree or disagree",
    "Agree",
    "Strongly Agree",
]

number_scale = [str(i) for i in range(11)[1:]]


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    countries = []
    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        for category, columns, order_scale in [
            ("General satisfaction", satis_gen, number_scale),
            ("Recognition", recog, agree_scale),
            ("Consider leaving job", turn_over1, number_scale),
            ("Would accept another job at same compensation", turn_over2, agree_scale),
            ("Perceived employability", perc_emp, agree_scale),
            ("Progression in the current role", prog_rse, agree_scale),
        ]:
            # Fix: always assumed a number_scale and satis_gen columns, set to loop variables
            plotting_likert(
                df, country, category, columns, survey_year, order_scale=order_scale
            )
            countries[-1].update(figure_country(country, slugify(category), plt))
    return {"countries": countries}


if __name__ == "__main__":
    run()

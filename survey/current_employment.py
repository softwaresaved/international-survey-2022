# Current employment
import sys
import matplotlib.pyplot as plt

from lib.analysis import (
    count_diff,
    plot_cat_comparison,
    plot_wordcloud,
    plot_density_func,
    describe_diff,
    get_sampled_df,
)
from lib.report import (
    slugify,
    make_report,
    read_cache,
    table_country,
    figure_country,
    COUNTRIES_WITH_WORLD,
)


current_emp = ["currentEmp1. Please select your organization type"]

which_uni = ["currentEmp2. Which university do you work for?"]

title_job = ["currentEmp5. What is your official job title?"]
diff_title = ["currentEmp6. Are you known in your group by a different job title?"]

contract_time = ["currentEmp12. Do you work full time or part time"]

nature_contract = ["currentEmp10. What is the nature of your current employment?"]

start_contract = ["currentEmp9. When did you start your current position?"]

duration_contract = [
    "currentEmp11. What is the expected duration (in years) of your current position (in total)?"
]

# Note: not used
german_orga = [
    "currentEmp20de. Which Fraunhofer institute do you work for?",
    "currentEmp21de. Which Helmholtz institute do you work for?",
    "currentEmp22de. Which Leibniz institute do you work for?",
    "currentEmp23de. Which Max-Planck institute do you work for?",
    "currentEmp24de. Which University of Applied Sciences?",
]

salary = ["socio4. Please select the range of your salary"]

salary_de = [
    "socio10de. Please select your renumeration group according to your collective bargaining agreement"
]

# Note: not used
salary_ausnzl = [
    "socio11ausnzl. What is the category of your pay-scale?",
    "socio12ausnzl. What is your academic pay-level?",
    "socio13ausnzl. What is your pay-level?",
    "socio14ausnzl. What is your government pay-level?",
]

germany_netherlands_salary_range = [
    "Less than 27.499 EUR",
    "Between 27.500 and 32.999 EUR",
    "Between 33.000 and 38.499 EUR",
    "Between 38.500 and 43.999 EUR",
    "Between 44.000 and 49.999 EUR",
    "Between 50.000 and 54.999 EUR",
    "Between 55.000 and 65.999 EUR",
    "Between 66.000 and 76.999 EUR",
    "Between 77.000 and 109.999 EUR",
    "More than 110.000 EUR",
    "Prefer not to say",
]

salary_ranges = {
    "Australia": [
        "< AUD 45,000",
        "≥ AUD 45,000 and < AUD 65,000",
        "≥ AUD 65,000 and < AUD 85,000",
        "≥ AUD 85,000 and < AUD 105,000",
        "≥ AUD 105,000 and < AUD 120,000",
        "≥ AUD 120,000",
    ],
    "Germany": germany_netherlands_salary_range,
    "Netherlands": germany_netherlands_salary_range,
    "New Zealand": [
        "< NZD 45,000",
        "≥ NZD 45,000 and < NZD 65,000",
        "≥ NZD 65,000 and < NZD 85,000",
        "≥ NZD 85,000 and < NZD 105,000",
        "≥ NZD 105,000 and < NZD 120,000",
        "≥ NZD 120,000",
    ],
    "South Africa": [
        "Less than R 189 880",
        "Between R 189 881 and R 296 540",
        "Between R 296 541 and R 410 460",
        "Between R 410 461 and R 555 600",
        "Between R 555 601 and R 708 310",
        "Between R 708 311 and R 1 500 000",
        "More than R 1 500 000",
        "Prefer not to say",
    ],
    "United Kingdom": [
        "< £18,031",
        "≥ £18,031 and < £24,057",
        "≥ £24,057 and < £32,277",
        "≥ £32,277 and < £43,325",
        "≥ £43,325 and < £58,172",
        "≥ £58,172",
    ],
    "United States": [
        "< $30,000",
        "≥ $30,000 and < $49,999",
        "≥ $50,000 and < $69,999",
        "≥ $70,000 and < $89,999",
        "≥ $90,000 and < $109,999",
        "≥ $110,000 and < $129,999",
        "≥ $130,000 and < $149,999",
        "≥ $150,000 and < $199,999",
        "≥ $150,000",
        "Prefer not to say",
    ],
}


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    df = read_cache("processed_data")
    countries = []

    current_field = [
        x for x in df.columns if x[: len("currentEmp13")] == "currentEmp13"
    ]
    # Get the funding information
    fund = [x for x in df.columns if x[:5] == "fund2"]

    for country in COUNTRIES_WITH_WORLD:
        countries.append({"country": country})
        for columns, category in [
            (current_emp, "Organisation type"),
            (current_field, "in which field"),
            (which_uni, "Which university"),
            (contract_time, "Contract type"),
            (nature_contract, "Nature of employment"),
            (duration_contract, "Duration of contract in year"),
            (salary, "Salary"),
            (fund, "Type of funding"),
            (title_job, "Official job title"),
            (diff_title, "Different job title"),
        ]:
            name = slugify(category)
            # Disable salary and type of funding sections for world
            if country == "World" and category in ["Salary", "Type of funding"]:
                continue
            multi_choice = category in ["in which field", "Type of funding"]
            if category == "Salary":
                order_question = salary_ranges[country]
                try:
                    df_salary = get_sampled_df(df, salary)
                    sl = df_salary[df_salary["Country"] == country]["socio4. Please select the range of your salary"].unique()
                    assert (
                        len(order_question)
                        - len(
                            df_salary[df_salary["Country"] == country][
                                "socio4. Please select the range of your salary"
                            ].unique()
                        )
                        in [-2, -1, 0]
                    )
                except AssertionError:
                    print(
                        set(
                            df_salary[df_salary["Country"] == country][
                                "socio4. Please select the range of your salary"
                            ].unique()
                        )
                        - set(order_question)
                    )
                    raise
                result = count_diff(
                    df,
                    salary,
                    category=category,
                    country=country,
                    order_index=order_question,
                    multi_choice=multi_choice,
                    survey_year=survey_year
                )
                countries[-1].update(table_country(country, name, result))
                plot_cat_comparison(result, country, category, order_index=order_question)
                countries[-1].update(figure_country(country, name, plt))

            elif category == "Duration of contract in year":
                result = describe_diff(
                    df,
                    duration_contract,
                    category=category,
                    country=country,
                    survey_year=survey_year,
                )
                countries[-1].update(table_country(country, name, result))
                plot_density_func(
                    df,
                    columns=duration_contract,
                    country=country,
                    category=category,
                    survey_year=survey_year,
                    remove_outliers=True,
                )
                countries[-1].update(figure_country(country, name, plt))

            else:  # general case
                result = count_diff(
                    df,
                    columns,
                    category=category,
                    country=country,
                    survey_year=survey_year,
                    multi_choice=multi_choice,
                )
                try:
                    countries[-1].update(table_country(country, name, result))
                    if not result.empty:
                        plot_cat_comparison(result, country, category)
                        countries[-1].update(figure_country(country, name, plt))
                except KeyError:
                    pass
    return {"countries": countries}


if __name__ == "__main__":
    run()

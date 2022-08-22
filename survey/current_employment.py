# Current employment
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from lib.analysis import (
    get_previous_survey_year,
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
    COUNTRIES,
    COUNTRIES_WITH_WORLD,
)
from survey.sociodemography import read_anonymised_data


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
salary_col = salary[0]
us_salary_col = 'socio4qus._.Please select the range of your salary'

salary_de = [
    "socio10deqde. Please select your remuneration group according to your collective bargaining agreement"
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
        "Prefer not to say",
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


def prepare_salary_data(df):
    """Converts any US 2018-style salary ranges to 2022 format and merges salary information from countries into a single column"""
    if us_salary_col in df.columns:
        df[us_salary_col].replace(
            {
                "Less than $30,000":         "< $30,000",
                "From $30,000 to $49,999":   "≥ $30,000 and < $49,999",
                "From $50,000 to $69,999":   "≥ $50,000 and < $69,999",
                "From $70,000 to $89,999":   "≥ $70,000 and < $89,999",
                "From $90,000 to $109,999":  "≥ $90,000 and < $109,999",
                "From $110,000 to $129,999": "≥ $110,000 and < $129,999",
                "From $130,000 to $149,999": "≥ $130,000 and < $149,999",
                "From $150,000 to $199,999": "≥ $150,000 and < $199,999",
                "More than $150,000":        "≥ $150,000",
            },
            inplace=True
        )
    df["socio4"] = (
        df.loc[:, df.columns.str.startswith("socio4")]
        .fillna("")
        .agg("".join, axis=1)
        .map(str.strip)
    )
    df = df[['Country', 'Year', 'socio4']]
    df.columns = ['Country', 'Year', salary_col]

    return df


@make_report(__file__)
def run(survey_year, data="data/public_merged.csv"):
    survey_prev_year = get_previous_survey_year(survey_year)

    df = read_cache("processed_data")

    # Import salary data
    # NB fix: changed from 2018 method, where salary data for both years was imported within overview_and_sampling.py,
    #         since we're dealing with this now as a separated CSV (similarly to how other sensitive data types are
    #         handled). As a result, 2018_salary.csv has been reformatted (data itself unchanged) to also adopt the
    #         new method and format used for 2022
    salary_df_year = prepare_salary_data(read_anonymised_data(survey_year, 'data/' + str(survey_year) + '_salary.csv'))
    salary_df_prev_year = prepare_salary_data(read_anonymised_data(survey_prev_year, 'data/' + str(survey_prev_year) + '_salary.csv'))
    df_salary = pd.concat([salary_df_year, salary_df_prev_year], ignore_index=True)

    # Ensure we re-label countries not in targeted countries as 'World'
    df_salary["Country"] = df_salary["Country"].apply(lambda x: x if x in COUNTRIES else "World")

    # Drop all records with empty strings in salary column
    df_salary[salary_col] = df_salary[salary_col].replace('', np.nan)
    df_salary = df_salary[df_salary[salary_col].notna()]

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
            (current_field, "In which field"),
            (which_uni, "Which university"),
            (contract_time, "Contract type"),
            (nature_contract, "Nature of employment"),
            (duration_contract, "Duration of contract in years"),
            (salary, "Annual salary"),
            (fund, "Type of funding"),
            (title_job, "Official job title"),
            (diff_title, "Are you known in your group by a different job title"),
        ]:
            name = slugify(category)
            # Disable salary and type of funding sections for world
            if country == "World" and category in ["Annual salary", "Type of funding"]:
                continue
            multi_choice = category in ["In which field", "Type of funding"]

            # Fix: process salary, unless the country isn't defined in the salary_ranges data,
            # in which case just do it using default method
            if category == "Annual salary" and country in salary_ranges:
                order_question = salary_ranges[country]
                try:
                    sl = df_salary[df_salary["Country"] == country][salary_col].unique()
                    assert (
                        len(order_question)
                        - len(
                            df_salary[df_salary["Country"] == country][salary_col].unique()
                        )
                        in [-2, -1, 0]
                    )
                except AssertionError:
                    print(
                        set(
                            df_salary[df_salary["Country"] == country][salary_col].unique()
                        )
                        - set(order_question)
                    )
                    raise
                result = count_diff(
                    df_salary,
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

            elif category == "Duration of contract in years":
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
                    unit_label="Contract duration in years",
                    remove_outliers=True,
                )
                countries[-1].update(figure_country(country, name, plt))

            else:  # general case
                # Fix: special case: use salary df, not general one, since we deal with salaries as protected now
                use_df = df_salary if category == "Annual salary" else df
                result = count_diff(
                    use_df,
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

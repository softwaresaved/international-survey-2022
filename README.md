[![Python 3.9](https://github.com/softwaresaved/international-survey-2018/actions/workflows/python-package.yml/badge.svg)](https://github.com/softwaresaved/international-survey-2018/actions/workflows/python-package.yml)

# RSE International Survey Analysis

This repository is used to analyse international surveys conducted by the Software Sustainability Institute.

In **2016** the Software Sustainability Institute ran the first survey of Research Software Engineers (RSEs) - the people who write code in academia. This produced the first insight into the demographics, job satisfaction, and practices of RSEs. To support and broaden this work, the Institute will run the UK survey every year and - it is hoped - will expand the survey so that insight and comparison can be made across different countries. Ultimately, we hope that these results, the anonymised version of which will all be open licensed, will act as a valuable resource to understand and improve the working conditions for RSEs.

In **2017** we also surveyed Canadian RSEs and we added four further countries, Germany, Netherlands, South Africa and USA.
Our thanks to our partners: Scott Henwood (Canada), Stephan Janosch and Martin Hammitzsch (Germany), Ben van Werkhoven and Tom Bakker (Netherlands), Anelda van der Walt (South Africa) and Daniel Katz and Sandra Gesing (USA).

In **2018** we have worked differently and created a survey for all countries (rather than one survey for each ones).

## Setup

This repository is only for the survey analysis. Here's how to reproduce the analysis on your own computer. The following instructions only apply for the 2018 and 2021 survey.

Due to a quirk of how we host the survey using [Github Pages](https://pages.github.com),
the survey analysis data has to be stored in the [docs](docs) folder of the main
repository.

To reproduce the results on your machine, first clone the repository and setup
the Python virtual environment:
```bash
git clone --recurse-submodules https://github.com/softwaresaved/international-survey-2018
cd international-survey-2018
python -m venv venv  # use python3 if your default python is still Python 2
source venv/bin/activate
python -m pip install -r requirements.txt
```

The survey analysis configuration is
via optional environment variables. If you have cloned this repository, then you shouldn't need to set any configuration, as the defaults are fine.

Use the following to set the environment variables on macOS and Linux. If you are on Windows, use the documentation linked [here](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/set_1).

```bash
export RSE_SURVEY_YEAR=2018  # optional, this is detected automatically if in a folder like *-2018
export RSE_SURVEY_YEAR_PREV=2017  # optional, only needed if previous year != current year - 1
export RSE_SURVEY_FIGURE_TYPE=svg  # optional, set to pdf or png to generate figures in that format
export RSE_SURVEY_FIGURE_DPI=300  # optional, set dpi for png or pdf output formats
```

You can generate the full report (other than the country specific reports) by running:

```bash
python run.py
```

Country reports should be generated _after_ the section specific reports (do not replace `country` with a specific country, this will generate all country reports):

```bash
python run.py country
```

To generate sections individually, first ensure that you have run the initialisation (which is the overview and sampling section) that is required by other sections. This can be done by passing `init` to run.py:

```bash
python run.py init
```

This should create a `cache/processed_data.csv` file within the `docs` folder. Once this is generated, you can run any of the sections in any order:

```bash
python run.py <section>
```

So for example to generate the current-employment section: `python run.py current-employment`


* The section reports utilise templates from an [international survey lib submodule repo](https://github.com/softwaresaved/international-survey-lib/tree/main/templates) corresponding to each section; the country report template is at [templates/country_report.md](https://github.com/softwaresaved/international-survey-lib/tree/main/templates/country_report.md).
  The template file uses the [Mustache](https://mustache.github.io) templating language via the [chevron](https://pypi.org/project/chevron/) module.
* Two types of reports are generated: section reports and country reports. Section reports are useful for comparing countries for a particular section of the survey,
such as demographics or job satisfaction. Country reports give an overview of a country across the different sections of the survey.
* Section reports are generated in [_section](_section)
* Country reports are generated in [_country](_country)
* Each table in the report has a corresponding CSV in [csv](csv)
* Each figure in the report has a corresponding SVG in [fig](fig)
* The source data used for the analysis is at [data](data)

## Software survey website

* We use [Jekyll](https://jekyllrb.com) and [Github Pages](https://pages.github.com) to build the website hosted at https://softwaresaved.github.io/international-survey-2018.
* Stylesheets for the site are at [_sass](_sass)
* Configuration of the site is at [_config.yml](_config.yml)
* The hosted site can be viewed locally by using the command `bundle exec jekyll serve` in the docs folder and following the localhost URL. If this is the first time setting up Jekyll on your computer, ensure that you have Ruby and Bundle installed (`gem install bundler`).

## Creating a survey for the next year

- [ ] Rename the docs folder to the previous year using git. Thus to develop the survey for 2022, we would rename the docs folder to 2021: `git mv docs 2021`, followed by a commit.
- [ ] Copy the previous year's folder to a new docs folder: `cp -R 2021 docs`.
- [ ] The analysis for each is contained in their respective folder, except for the common functions in [include](include). Any changes to sections, or creating new graphs and tables can be done now. Keep commiting your changes to the code as usual.
- [ ] Once you are done, set the configuration variables as above (remember to point RSE_SURVEY_YEAR and RSE_SURVEY_YEAR_PREV to the correct years!) and generate the section and country reports.
- [ ] View the website using `bundle exec jekyll serve`. Iterate the previous two steps as needed.
- [ ] Add the docs folder to git and commit: `git add docs && git add -f docs/csv`. All CSVs are excluded in [.gitignore](.gitignore) to prevent accidental commit of personally identifiable information, so have a look before pushing the commit to the main repository.
- [ ] After a push to Github, the Jekyll configuration should automatically generate the survey analysis website for the new year!
- [ ] Update copyright (`footer_content:` in [docs/_config.yml](docs/_config.yml)), author information and steps to reproduce in the [README](README.md).

## Published results for previous years
We publish the results under the form of notebooks. All surveys have an attached 'public.csv' file. Theses files have been cleaned of all sensitive data. Therefore, the jupyter notebooks show some results that are not contained in the 'public.csv'.

<table>
    <thead>
      <tr>
            <th>Country</th>
            <th>2016</th>
            <th>2017</th>
            <th>2018</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Australia</td>
            <td>N/A</td>
            <td>N/A</td>
            <td rowspan=8><a href="https://github.com/softwaresaved/international-survey-analysis/tree/master/analysis/2018">Analysis</a> / <a href="https://github.com/softwaresaved/international-survey/blob/master/analysis/2018/data/public_data.csv">Public data</a></td>
        </tr>
        <tr>
            <td>Canada</td>
            <td>N/A</td>
            <td><a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/results_can.ipynb">Analysis</a> / <a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/can/data/public_data.csv">Public data</a></td>
        </tr>
        <tr>
            <td>Germany</td>
            <td>N/A</td>
            <td><a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/results_de_narrative.ipynb">Analysis</a> / <a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/de/data/public_data.csv">Public data</a></td>
        </tr>
        <tr>
            <td>Netherlands</td>
            <td>N/A</td>
            <td><a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/results_nl_narrative.ipynb">Analysis</a> / <a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/nl/data/public_data.csv">Public data</a></td>
        </tr>
        <tr>
            <td>New Zealand</td>
            <td>N/A</td>
            <td>N/A</td>
        </tr>
        <tr>
            <td>United Kingdom</td>
            <td><a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2016/results_uk_narrative.ipynb">Analysis</a> / <a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2016/uk/data/public_data.csv">Public data</a></td>
            <td><a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/results_uk_narrative.ipynb">Analysis</a> / <a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/uk/data/public_data.csv">Public data</a></td>
        </tr>
        <tr>
            <td>United States</td>
            <td>N/A</td>
            <td><a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/results_us_narrative.ipynb">Analysis</a> / <a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/us/data/public_data.csv">Public data</a></td>
        </tr>
        <tr>
            <td>South Africa</td>
            <td>N/A</td>
            <td><a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/results_zaf_narrative.ipynb">Analysis</a> / <a href="https://github.com/softwaresaved/international-survey-analysis/blob/master/analysis/2017/zaf/data/public_data.csv">Public data</a></td>
        </tr>
    </tbody>
</table>

## Composition of the survey
The [base questions](https://github.com/softwaresaved/international-survey/blob/master/survey_creation/2018/questions.csv) for the survey were tailored to meet the requirements of each country. They covered ten subjects:
   1. **Demographics**: traditional social and economic questions, such as gender, age, salary and education.
   1. **Coding**: how much code do RSEs write, how often, and for whom.
   1. **Employment**: questions about where RSEs work and in which disciplines.
   1. **Current contract**: understanding stability of employment by questioning the type of employment contract RSEs receive.
   1. **Previous employment**: understanding routes into the profession the reasons for choosing it.
   1. **Collaboration and training**: who RSEs work with, how many people they work with, and the training they conduct.
   1. **Publications**: do RSEs contribute to publications and are they acknowledged?
   1. **Sustainability and tools**: testing, bus factor, technical handover. Also which tools they are using
   1. **Job satisfaction**: what do RSEs think about their job and their career?
   1. **Network**: how do RSEs meet and gain representation?
These subjects are not necessarily  investigated under this order, neither published with that order. 

## Contributors

Here is a list of contributors for the 2017/2018 version of the survey (alphabetic order). They are also mentioned in the [.zenodo.json](https://github.com/softwaresaved/international-survey/blob/master/.zenodo.json) to be automatically added to the DOI.
* Stephan Druskat
* Sandra Gesing
* Martin Hammitzsch
* Scott Henwood
* Simon Hettrick
* Stephan Janosch
* Katrin Leinweber
* Olivier Philippe
* Nooriyah P. Lohani
* Nicholas R. May
* Manodeep Sinha
* Daniel S. Katz
* Anelda van der Walt
* Ben van Werkhoven

## Licence 

This repository contains code and public data. We have different licence for each
* The code is released under [BSD 3-Clause License](https://github.com/softwaresaved/international-survey/blob/master/LICENSE.md).
* The data stored in this repository is under the [CC BY 2.5 SCOTLAND](https://github.com/softwaresaved/international-survey/blob/master/LICENSE_FOR_DATA).

The repository is also archived on zenodo: https://doi.org/10.5281/zenodo.1194668.
If you want to cite this work and need a citation in a specific format, you can use the citation service on the zenodo.

## Citations
The citation for the 2018 version is:
> Olivier Philippe, Martin Hammitzsch, Stephan Janosch, Anelda van der Walt, Ben van Werkhoven, Simon Hettrick, … Manodeep Sinha. (2019, March 6). softwaresaved/international-survey: Public release for 2018 results (Version 2018-v.1.0.2). Zenodo. http://doi.org/10.5281/zenodo.2585783

The citation for the 2017 version is:
> Olivier Philippe, Martin Hammitzsch, Stephan Janosch, Anelda van der Walt, Ben van Werkhoven, Simon Hettrick, … Scott Henwood. (2018, March 27). softwaresaved/international-survey: Public release for 2017 results (Version 2017-v1.2). Zenodo. http://doi.org/10.5281/zenodo.2574123

## Funders
The Software Sustainability Institute is supported by EPSRC grant EP/H043160/1 and EPSRC/ESRC/BBSRC grant EP/N006410/1, with additional project funding from Jisc and NERC. Collaboration between the universities of Edinburgh, Manchester, Oxford and Southampton.

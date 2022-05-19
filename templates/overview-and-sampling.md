---
layout: page
title: Overview
nav_order: 1
---
# Overview

1. TOC
{:toc}

This page gives an overview of the participants per country. From where they come from and when they started the survey. It also gives the difference with the previous year for the countries that participated in 2018.

Alongside this information, it also subset the relevant participants for future analysis. Only the participants that have finished at least the first section and the ones that report to develop program for their work, or lead research developers, are kept.

## Total participants

There were a total of {{n_participants}} in the survey.

## Repartition per country

We developed specific questions for the following countries:
* Australia
* Canada (but host their own version of the survey so they will not be analysed here)
* Germany
* Netherlands
* New Zealand
* South Africa
* United Kingdom
* United States

We can see the distribution of participants among the countries as follows:

{{t_participant}}


## Visual representation of countries repartition   

{{{f_participant}}}

## Date of participation

{{{f_participation_date}}}

## Difference with the previous year

Several countries did the survey in the previous 2018 survey - here are the difference in the amount of participants:

{{t_difference_with_previous_year}}

{{{f_difference_with_previous_year}}}

## Subsetting

### Selecting valid participants only

On the total of participants, we only want the participants that code software during their work. 
We had a specific question for this purpose. We asked the participants if they are writing software or if they are leading a group of software developers. Each of these questions had the possibility of Yes/No answer. Here the exact wording of the questions:

* Do you write software for academic research as part of your job
* Does the majority of your role comprise leading a group of software developers or RSEs?

We will only select the participants who answered `Yes` to at least one question.

{{t_valid_participants}}

For any further analysis, we remove the participants that answered 'No' at both of the question to only keep the ones that have work involving software development for both year to ensure a proper comparison. This brings the number of participants analysed to:

{{t_participant_analysed}}

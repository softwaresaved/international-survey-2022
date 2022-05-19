---
layout: page
title: {{country}}
---
# {{country}}

1. TOC
{:toc}

## Education and academic field

This section contains the information about the type of education the
participants have, as well as their highest degree obtained.

We asked the participants, in which field they are working. With that question,
it is possible to see which current field employed the most of RSE/RSD. The
questions was specific to each country and was multiple choice. Each
participant could choose several fields. We then calculate the different
proportion by dividing each field by the total of participants that have
selected at least one option. 

### Questions in this section

* What is the highest level of education you have attained? (one choice list)
* In which discipline is your highest academic qualification? (one choice list)
* List any professional qualifications you hold (free text)

### Levels of education 

{{t_education_level}}

{{{f_education_level}}}

### Academic field for education and professional development

Alongside of question about education level we also asked the participants in
which field they finished their highest level of education. Here again the
propositions were specific to each countries so the comparison is difficult
despite lot of overlapping in the categories. 

{{t_academic_field_edu}}

{{{f_academic_field_edu}}}

{{{f_academic_field_edu_wordcloud}}}


### Academic field of work

{{t_academic_field_work}}

{{{f_academic_field_work}}}


## Professional developer

In this section we investigate the relationship between RSEs/RSDs and their own
experience in software development Understandably, we expect them having
several years of software development experience. However, as shown in previous
years, it is not necessarily reflected upon their own feeling of being
considered as professional.

Questions in this section:

* Do you consider yourself a professional software developer? (Yes/No)
* How many years of software development experience do you have? (integer)

### How many professional developers?

{{t_proportion-professional-developer}}

{{{f_proportion-professional-developer}}}

### Years of software development experience

{{t_summary-years-professional-developer}}

{{{f_density-years-professional-developer}}}


## How time is spent

RSE/RSE are supposed to be an hybrid role, compared to pure software developer.
They bring a knowledge from their field but also are developing software. To
capture this different tasks they may do during their work, we asked them how
they spend their time but also how they wish to spend their time to investigate
any difference between what they do and what they want to do.

### How to read the plots

Respondents were asked how much time is spent in a particular activity using
a Likert scale from from *1 (None at all)* to *10 (All my time)*.

The same questions asked them how much time they wanted to spend on these
activities. With that it was possible to see if discrepancies exist between
what they actually do and what they want to do. 

To read the results, when the bars shift to the right (in blue), it means they
reported positive values (from 6 to 10); when the bars are on the left (in
red), it means they reported more negative values (relative to the scale). Each
bar has a number that represents the percentage of participants that selected
that value. The total bar represents 100%.

To calculate the difference between what they want and what they do, we
subtract the answers to the the time that they *wished to have spent* from the
the answer to *actual time spent*. It is therefore possible to understand the
results as:

1. The result is **zero**: The time spent matches, they do as much as they want.
2. The result is **negative**: They wish to spend **less time** to do that activity
3. The result is **positive**: They wish to spend **more time** to do that activity

### Questions in this section

All questions were asked on a 1 to 10 Likert scale.

* On average, how much of your time is spent developing software?
* On average, how much of your time is spent on research?
* On average, how much of your time is spent on management?
* On average, how much of your time is spent on teaching?
* On average, how much of your time is spent on other activities?

{{{f_how-time-is-spent}}}


## Previous employment

Several questions were about the participants' previous job. The idea is to
collect insights of their career path and understand what their motivations are
to be an RSE.

We also asked the participants to rank the reasons why they chose their actual
position among 8 different ones:

* Desire to work in a research environment
* Freedom to choose own working practices
* Desire to advance research
* I want to learn new skills
* Opportunity to develop software
* Flexible working hours
* Ability to work across disciplines
* Opportunity for career advancement
* The salary

### Questions in this section

* Where was your previous job based? (single choice)
* Rank the following factors dependent on how strongly they influenced your decision to accept your current position (ranking)

### Where the previous job was based

{{t_where-previous-job-based}}

{{{f_where-previous-job-based}}}

### What were the reasons to choose the current job

{{t_reasons-to-choose-current-job}}

{{{f_reasons-to-choose-current-job}}}


## Collaboration and training

Questions in this section:

* Who uses the code that you write? (one choice)
* Do you always work with the same researchers, or do you regularly change the
  researchers you work with? (one choice)
* Are you part of a dedicated research software group within your institution?
  (yes-no)
* How many software projects are you currently involved in? (numeric)
* How many people who develop software typically work on your projects? (numeric)
* On average, how many times a year do you take part in providing training?
  (numeric)
* What training programs are you involved with? (free text)

### Developing code for others

{{t_developing-code-for-others}}

{{{f_developing-code-for-others}}}

### Working with same researchers

{{t_working-with-same-researchers}}

{{{f_working-with-same-researchers}}}

### Part of dedicated group

{{t_member-of-a-dedicated-group}}

{{{f_member-of-a-dedicated-group}}}

### Number of projects

{{t_number-of-software-projects}}

{{{f_number-of-software-projects}}}

{{t_number-of-software-developers-per-projects}}

{{{f_number-of-software-developers-per-projects}}}

### Training

{{t_training-frequency}}

{{{f_training-frequency}}}

{{{f_training-name-wordcloud}}}

## Publications and citations

RSEs is an hybrid role between a researcher and a software developer. We
investigated both of these aspects concerning publication and dissemination of
their work, one on the traditional aspect of it (publications and conference).

One essential aspect of career in academia is the publications and the
conferences to gain recognition. However, the role of RSE being less about
writing articles than creating the infrastructure and the software for the
article to exist, there is some fear that they will fail to have recognition
through the papers and conferences.

Questions in the section:

* In general, when your software contributes to a paper, are you acknowledged
  in that paper? (one choice)
* Have you presented your software work at a conference or workshop? (yes-no)
* At which conference(s)/workshop(s) have you presented your software work?
  (free text)

### Acknowledgment in paper

{{t_acknowledgment-in-paper}}

{{{f_acknowledgment-in-paper}}}

### Participation in conferences

{{t_did-you-participate-in-conference}}

{{{f_did-you-participate-in-conference}}}

### Conference name

{{{f_conference-name-wordcloud}}}


## Open source and DOI

RSEs is an hybrid role between a researcher and a software developer. We
investigated both of these aspects concerning publication and dissemination of
their work, one on the traditional aspect of it (publications and conference)
and, as developed here, on the more software aspect (open source and DOI).

We asked the participants if they have ever released their work under open
source licence but also questions about the referencing system. We asked them
how often they reference software, and if they use DOI for it, and which tools
for it.

We also asked them if they have an ORCID ID, a system that gives a unique
reference ID for the researcher.

Questions in this section:

* How often do you use an open-source licence for your software? (likert scale)
* How often do you reference software directly or the papers describing the software? (likert scale)
* How often do you associate your software with a Digital Object Identifier (DOI)? (likert scale)
* Which tools do you use to mint a DOI (e.g. local library, Zenodo)? (free text)
* Do you have an ORCID ID? (yes-no)


### Open source use

{{t_open-source-use}}

{{{f_open-source-use}}}

### Referencing software

{{t_citation-of-software}}

{{{f_citation-of-software}}}

### Use of Digital Object Identifier (DOI)

{{t_use-of-digital-object-identifier}}

{{{f_use-of-digital-object-identifier}}}

### Tools used for DOI

{{{f_tool-used-for-doi-wordcloud}}}

### ORCID

{{t_using-orcid}}

{{{f_using-orcid}}}


## Good practices

This section comprises sections that focus on the technical and development
aspects of the RSEs' work. They aim to understand good practices in developing
software.

We chose two broad measures to provide an insight into sustainability: the
**bus factor** and **technical hand over planning**.

*   The bus factor is a measure of the number of developers who understand
    a specific software project and could, with only a cursory review of the
    project, maintain or extend the code. A project with a bus factor of 1 is
    completely reliant on only one developer. If this developer finds new
    employment, becomes ill or is hit by the titular bus, then the project will
    fail. A high bus factor provides some confidence that the project can be
    sustained even if a developer leaves.

*  A technical hand over plan is used to introduce a new developer to
   a software project. These plans cover basic information, such as the license
   and location of the software, a repository, a description of the software
   architecture, a summary of development plans and any other information that
   a new developer would need to understand the software. A project that has
   written (and maintained) a technical hand over plan can withstand the
   departure of a developer, even a key developer, significantly better than
   one without such a plan.

Developing software requires a set of good practices to ensure the quality of
the subsequent analysis as well as the robustness of the developed software, to
name a few of important aspects. We wanted to see if the implementation of some
simple but essential good practices were a reality beside the bus factor and
technical hand over planning.

When developing software, **version control** and **testing** can be seen as
tool to enhance the quality of the developed software, especially considering
the importance of code review and sharing in public funded places such as
academia.

For testing, we asked the participants to choose any of the following testing
methods:

* Automated testing with continuous integration
* Test engineers conduct testing
* Developers conduct own testing
* No formal testing but users provide feedback
* No formal testing

Test engineers conducting testing is the most robust testing method
but may not be possible in smaller projects while no formal testing should not
occur in any ideal scenario, regardless of the size of the project.

We also asked the participants if they use any version control tools through
a list of choice. And finally we asked them which repository they are currently
using for their most important project.

### Bus factor

{{t_bus-factor}}

{{{f_bus-factor}}}

### Presence of transition plan

{{t_presence-of-transition-plan}}

{{{f_presence-of-transition-plan}}}

### Use of version control

{{t_use-of-version-control}}

{{{f_use-of-version-control}}}

### Testing strategies

{{t_testing-strategies}}

{{{f_testing-strategies}}}

### Repository

{{{f_repository-wordcloud}}}


## Tools and programming languages

On technical details we wanted to know which of the programming languages are mostly used by the RSEs. We give them a multi-choice list inspired by the [results published by Stackoverflow](https://insights.stackoverflow.com/survey/2017#most-popular-technologies).

We also wanted to know which operating system they use for work.

Questions in this section:

* Which operating system do you primarily use for development? (one choice)
* What programming languages do you use at work? Please select all that apply.
  (multiple choice)

### Programming languages

{{t_programming-languages}}

{{{f_programming-languages}}}

### Operating systems

{{t_operating-systems}}

{{{f_operating-systems}}}


## Job satisfaction

Job satisfaction is an essential pulse to take about a community's health.
It helps to track the evolution and the current state of the RSEs within their
role and to catch any sign of structural or organisational dysfunction that are
translated into well-being. There are a lot of different metrics to measure the
quality of a job on a personal and psychological level [1]. Several models
exist to understand the link between different factors of job satisfaction and
turnover intention [2]–[6]. Turnover intention is an important measure that is
highly associated with the risk of employees leaving the organisation [3]. Job
satisfaction is important in retaining RSEs. Perceived employability provides
information on how workers values their own skills in regard of the market. To
measure the different attitudes toward the RSE role, we used scales that have
been created in [5], [6], [7], [8]. These are Likert scale [7], which are
5 point ordinal scales graduated from Strongly disagree to Strongly agree. Each
scale is composed of several so called items (i.e. questions) that each measure
one attitude.

Beside these specific concepts we asked more general question about their
satisfaction in their current position and their satisfaction with their career
in general with a range of answers from 0 (not at all satisfied) to 10
(completely satisfied).

The specific questions about their job satisfaction reflect, in general, the
same opinion as the two more generic questions. However, the granularity helps
to identify a couple of issues that would not appears with generic questions:

* **Recognition**: These questions ask if the RSEs feel that they receive
  enough information about their work and their performance.
* **The turnover intention**: These questions aim to measure the desire to quit
  their current position.
* **The perceived employability**: This concept is linked to the previous one.
  People may not have the intention to leave their jobs, not because they like
  it, but because they fear they are not employable.
* **The possibility of progression**: This question aims to study the
  possibility of evolution for the RSEs, if information is available and if
  they see a possibility of evolution within their current career. This is the
  only questions that clearly received negative answers.

Questions in this section:

All questions were asked in a Likert scale.

* In general, how satisfied are you with your current position?
* In general, how satisfied are you with your career?
* Do you feel that your contribution to research is recognised by your supervisor/line manager?
* Do you feel that your contribution to research is recognised by the researchers you work with?
* Do you feel that your contribution to research is recognised by your institution?
* How often do you consider leaving your job?
* I would accept another job at the same compensation level if I was offered it
* It would not be very difficult for me to get an equivalent job in a different institution
* My experience is in demand on the labour market
* It is likely that I will gain a promotion within my current group
* The process I have to complete to gain a promotion is clear and understandable
* There are many opportunities within my chosen career plan
* It is likely that my next position will be an Research Software Engineer / Research

/References/

1. B. Aziri, “Job satisfaction: A literature review,” vol. 3, no. 4, pp. 77–86.
2. N. De Cuyper, S. Mauno, U. Kinnunen, and A. Mkikangas, “The role of job resources in the relation
   between perceived employability and turnover intention: A prospective two-sample study,” vol. 78, no. 2, pp. 253–263.
3. A. B. Bakker and E. Demerouti, “The job demands-resources model: State of the art,” vol. 22, no. 3, pp. 309–328.
4. G. H. L. Cheng and D. K. S. Chan, “Who Suffers More from Job Insecurity? A Meta-Analytic Review.” vol. 57, no. 2, p. 272.
5. E. R. Thompson and F. T. Phua, “A brief index of affective job satisfaction,” vol. 37, no. 3, pp. 275–307.
6. L. Greenhalgh and Z. Rosenblatt, “Job insecurity: Toward conceptual clarity,” pp. 438–448.
7. R. Likert, “A technique for the measurement of attitudes.” vol. 22, no. 140, p. 55.


### General satisfaction

{{{f_general-satisfaction}}}

### Recognition

{{{f_recognition}}}

### Turn-over intention

{{{f_consider-leaving-job}}}

{{{f_would-accept-another-job-at-same-compensation}}}

### Perceived employability

{{{f_perceived-employability}}}

### Progression in the current role

{{{f_progression-in-the-current-role}}}

## Research software engineer

In this section we wanted to know if the participants are member or not of
local organisations and if they are interested to participate to conference
specific for RSE. 

We also asked them to tell them which skills is important as RSE and which they
and to acquire for their current role.

### Questions in this section

* Are you a member of an association of Research Software Developers (e.g.
  AUS-RSE, CANARIE, DE-RSE, NZ_RSE, UK RSE, …)? (yes-no)
* Would you be interested in joining such an organisation? (yes-no)
* What is important for such an organisation? (multiple choice)
* Would you like to attend a conference about software development in academia?
  (yes-no)
* How did you learn the skills you need to become an Research Software Engineer
  / Research Software Developer? (free text)
* What three skills would you like to acquire or improve to help your work as
  a Research Software Engineer/ Research Software Developer? The skills can be
  technical and non-technical (free text)
  
### RSE member

{{t_rse-member}}

{{{f_rse-member}}}

### Joining a RSE/RSD association

{{t_joining-a-rse-rsd-association}}

{{{f_joining-a-rse-rsd-association}}}

### What is important for such an organisation

{{t_what-is-important-for-such-an-organisation}}

{{{f_what-is-important-for-such-an-organisation}}}

### Attending a national conference of RSE/RSD

{{t_attending-a-national-conference-of-rse-rsd}}

{{{f_attending-a-national-conference-of-rse-rsd}}}

### Learning skills for RSE/RSD

{{{f_learning-skills-rse-rsd-wordcloud}}}

### Which skills to improve

{{{f_which-skills-to-improve-rse-rsd-wordcloud}}}

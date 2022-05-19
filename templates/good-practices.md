---
layout: page
title: Good practices
nav_order: 10
---
# Good practices

1. TOC
{:toc}

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

{{#countries}}
## {{country}}

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



{{/countries}}

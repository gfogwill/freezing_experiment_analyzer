# Freezing Experiment Analyzer

Python package to analyze collected data from freezing experiments to estimate INP concentration as function of the activation temperature in the immersion freezing mode.

This project can be used from the command line with `brr` command or can be imported into other python modules. 



## Prerequisites

Requirements for the software and other tools to build, test and push

- [Python 3](https://www.python.org)
- [Git](https://git-scm.com/)

## Installing

Clone the repository

```console
$ git clone https://gitlab.fmi.fi/perezfo/freezing_experiment_analyzer
$ cd freezing_experiment_analyzer
```

Now let's install the requirements. But before we do that, we **strongly**
recommend creating a virtual environment with a tool such as
[virtualenv](https://virtualenv.pypa.io/en/stable/):

```console
$ python -m venv my_venv
$ source my_venv/bin/activate
$ python -m pip install -r requirements.txt
```

**Note**: Every time you start a new session you need to activate the virtual environment.

```console
$ source my_venv/bin/activate
```

This can also be done with Conda. Create a new Conda virtual environment named `my_venv`

The command below will create a new folder called `my_venv`.

```console
$ conda create --name my_venv
```

Activating the environment named `my_venv` in Conda

```console
$ conda activate environment_name
```

## Testing the installation

```console
$ brr info
```

If everything is OK you should see the program logo.

## Getting started






## Project Organization


    ├── LICENSE
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── external       <- Data from third party sources.
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final data sets.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── docs               <- A default Sphinx project; see sphinx-doc.org for details
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1.0-jqp-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   ├── circles.py     <- Scripts to detect circles in images
    │   ├── cli.py         <- Scripts for the Command Line Interface (CLI)
    │   ├── localdata.py   <- Scripts to load raw data from experiments
    │   ├── paths.py       <- Definition of the paths of the package
    │   ├── prompts.py     <- Prompts used by cli.py
    │   ├── reports.py     <- Scripts to generate reports and plots after the data analysis
    │
    └── setup.py           <- makes project pip installable (pip install -e .) so src can be imported

--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

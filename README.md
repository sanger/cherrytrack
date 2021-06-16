# Cherrytrack

![CI](https://github.com/sanger/cherrytrack/workflows/CI/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![codecov](https://codecov.io/gh/sanger/cherrytrack/branch/develop/graph/badge.svg)](https://codecov.io/gh/sanger/cherrytrack)

A microservice which defines the database used to store automation system run information and
exposes endpoints to ease querying.

## Table of Contents

<!-- toc -->

- [Requirements for Development](#requirements-for-development)
- [Getting Started](#getting-started)
  * [Setup Steps](#setup-steps)
- [Running](#running)
- [Testing](#testing)
  * [Testing Requirements](#testing-requirements)
  * [Running Tests](#running-tests)
- [Formatting, Linting and Type Checking](#formatting-linting-and-type-checking)
  * [Formatting](#formatting)
  * [Linting](#linting)
  * [Type Checking](#type-checking)
- [Deployment](#deployment)
- [Miscellaneous](#miscellaneous)
  * [Updating the Table of Contents [Mandatory]](#updating-the-table-of-contents-mandatory)

<!-- tocstop -->

## Requirements for Development

The following tools are required for development:

- python (use `pyenv` or something similar to install the python version specified in the `Pipfile`)
- mySQL 8.0 (a `docker-compose.yml` is included to easily get the database server up and running)

## Getting Started

### Setup Steps

Install the require dependencies:

    pipenv install --dev

Create the following database (currently manually):

- `psd_cherrytrack_dev`

## Running

To run the application:

    flask run

## Testing

### Testing Requirements

Create the following database (currently manually):

- `psd_cherrytrack_test`

### Running Tests

To run the test suite:

    python -m pytest

## Formatting, Linting and Type Checking

### Formatting

This project is formatted using [black](https://github.com/psf/black). To run formatting checks,
run:

    pipenv run black .

### Linting

This project is linted using [flake8](https://github.com/pycqa/flake8). To lint the code, run:

    pipenv run flake8

### Type Checking

This project uses static type checking using the [mypy](https://github.com/python/mypy) library, to
run:

    pipenv run mypy .

## Deployment

This project uses a Docker image as the unit of deployment. To create a release for deployment,
create a release in GitHub and wait for the GitHub action to create the Docker image.

The release version should align with the [standards](./standards.md).

## Miscellaneous

### Updating the Table of Contents [Mandatory]

To update the table of contents after adding things to this README you can use the [markdown-toc](https://github.com/jonschlinkert/markdown-toc)
node module. To run:

    npx markdown-toc -i README.md

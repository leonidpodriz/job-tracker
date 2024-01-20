### Job Trackers

[![Django CI](https://github.com/leonidpodriz/job-tracker/actions/workflows/django.yml/badge.svg)](https://github.com/leonidpodriz/job-tracker/actions/workflows/django.yml)

## Introduction

This Readme provides detailed instructions for building, running, and testing a Docker-based application. It uses Docker
Compose for managing containerized services.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Possible improvements and future work](#possible-improvements-and-future-work)
- [Steps to Build and Run the Application](#steps-to-build-and-run-the-application)
- [Running Migrations](#running-migrations)
- [Testing the Application](#testing-the-application)
- [Code Quality Tools](#code-quality-tools)
- [Building and Starting the Application in One Command](#building-and-starting-the-application-in-one-command)

## Possible improvements and future work

I was limited by the time and decided to focus on the core functionality. There are a lot of possible improvements and
future work that can be done to make this application more useful and user-friendly. I will list some of them below.

### Functional improvements

- Implement authorization endpoints
- Add vacancy functionality and link applications to vacancies
- Make notes foreign model to applications to allow multiple notes per application with different authors, timestamps
  and attachments. Technical remark: it also fits better to Django permission system and provides more flexibility
- Add files (e.g. CVs) to applications
- Add tags to applications
- Add email notifications once application status changes
- Add additional Django groups with fields (e.g. HR, Candidates, etc.) to allow user tack his own applications (in case
  of candidates) or applications of his vacancies (in case of HR)

### Technical improvements

- Refactor all tests to use client instead of using view directly (delivers better integration testing)
- Select test's code blocks that can be moved to separate functions or fixtures
- Parameterize more tests to test different scenarios
- Implement Swagger documentation or similar (Postman, etc.) to allow easy testing of API endpoints and provide
  clear documentation to the frontend developers. Swagger documentation is preferable:
    - It is easy to implement and maintain
    - It is generated automatically based on the code
    - Documentation is near the code and is always up to date (no need to maintain separate documentation)

## Prerequisites

- Docker and Docker Compose installed on your system.
- Basic understanding of Docker and command-line interface usage.

## Steps to Build and Run the Application

1. **Building Docker Images**
    - Command: `make build`
    - This command builds the Docker images as defined in the `docker/compose-base.yml` file.
    - Expected output: Messages indicating the progress and completion of the Docker image building process.

2. **Starting Docker Containers**
    - Command: `make up`
    - This starts the Docker containers as defined in both `docker/compose-base.yml` and `docker/compose-db.yml` files.
    - The containers will run in detached mode.
    - Expected output: Messages indicating the containers are starting.

3. **Stopping Docker Containers**
    - Command: `make down`
    - This stops and removes the Docker containers and networks.
    - Expected output: Messages indicating the containers are stopping.

4. **Restarting Docker Containers**
    - Command: `make restart`
    - This restarts all the running Docker containers.
    - Expected output: Messages indicating the containers are restarting.

5. **Viewing Docker Logs**
    - Command: `make logs`
    - This command tails the logs of all running containers.
    - Expected output: Continuous stream of log outputs from the containers.

## Running Migrations

- Command: `make migrate`
- This runs the database migrations inside the Docker container.
- Note: The database container keeps running after migrations. Use `make down` to stop it.

## Testing the Application

1. **Running Tests**
    - Command: `make test`
    - This runs the application tests using pytest inside the Docker container.
    - Expected output: Test results showing the number of tests passed/failed.

## Code Quality Tools

1. **Formatting Code**
    - Command: `make format`
    - This formats the code using the `black` formatter.

2. **Linting Code**
    - Command: `make lint`
    - This lints the code using `flake8`.

3. **Type Checking**
    - Command: `make type-check`
    - This performs type checking using `mypy`.

4. **Running All Scans**
    - Command: `make scan`
    - This runs linting, type-checking, and tests all together.

## Building and Starting the Application in One Command

- Command: `make build-up`
- This will build the Docker images and then start the Docker containers.
- Note: Don't forget to run migrations before starting the application with command `make migrate`.

## LLMs usage

I haven't used large language models (LLMs) to generate code exceeding 10 lines of code, as I prefer to test my own
skills. However, I've utilized GitHub Copilot to enhance my code completion experience and to handle some templated
parts of the code. Additionally, I've employed ChatGPT for generating build and run instructions (I've review it and add
some additional information) in this file. The Makefile is sufficiently self-explanatory.
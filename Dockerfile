FROM python:3.12.0-bullseye

WORKDIR /app

ARG ENV

COPY Pipfile Pipfile.lock ./

RUN if [ "$ENV" = "dev" ];  \
    then pip install pipenv && pipenv install --system --deploy --dev;  \
    else pip install pipenv && pipenv install --system --deploy;  \
    fi

COPY . .

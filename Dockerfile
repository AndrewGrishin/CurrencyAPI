FROM ubuntu:22.04
FROM python:3.11.8-slim-bookworm
# Setting up description
LABEL author="Andrey Grishin"
LABEL group="M05-318a"
LABEL title="Central Bank currency exchange scrapper"
LABEL description="Construct the env. suitable for currency scrapping problem solution."
# Setting up env. variables
ARG YOUR_ENV
ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry's configuration:
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.1

# Updating distribution
RUN apt-get update -y
RUN apt-get install python3 -y
RUN apt-get install curl -y

# Installing poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy project files
COPY currencyapi /home/currencyapi/
COPY main.py /home/
COPY poetry.lock /home/
COPY pyproject.toml /home/
COPY README.md /home/

# Changing working directory
WORKDIR /home/
RUN poetry install

# Execute bash command
ENTRYPOINT ["/bin/bash"]
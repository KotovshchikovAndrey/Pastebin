FROM python:3.11

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install poetry

COPY ./src ./src

RUN poetry config virtualenvs.create false && poetry install --only main
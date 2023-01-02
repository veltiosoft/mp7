ARG PYTHON_ENV=python:3.11-slim

FROM $PYTHON_ENV as build

RUN pip install poetry && poetry config virtualenvs.in-project true

RUN mkdir -p /app
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main


FROM $PYTHON_ENV as prod

COPY --from=build /app/.venv /app/.venv

COPY src /app
WORKDIR /app

EXPOSE 8080
ENTRYPOINT ["./.venv/bin/python"]
CMD ["main.py"]

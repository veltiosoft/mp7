ARG PYTHON_ENV=python:3.11-slim

FROM $PYTHON_ENV as build

RUN pip install poetry

RUN mkdir -p /app
WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry export --only main --without-hashes -f requirements.txt -o /requirements.txt


FROM $PYTHON_ENV as prod

COPY --from=build /requirements.txt .
RUN pip install -r requirements.txt

COPY src /app
WORKDIR /app

EXPOSE 8080
ENTRYPOINT ["python"]
CMD ["main.py"]

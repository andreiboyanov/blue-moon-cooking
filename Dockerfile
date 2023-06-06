FROM python:3-slim as python
ENV PYTHONUNBUFFERED=true
WORKDIR /app


FROM python as poetry
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN python -c 'from urllib.request import urlopen; print(urlopen("https://install.python-poetry.org").read().decode())' | python -
COPY . ./
RUN poetry install --no-interaction --no-ansi -vvv
RUN cat

FROM python as runtime
RUN apt update
RUN apt install --yes postgresql-client
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=poetry /app /app
CMD uvicorn --host 0.0.0.0 bmcook.main:app

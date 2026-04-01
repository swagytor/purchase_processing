FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE=1

RUN mkdir /app/
WORKDIR /app/

ENV VIRTUAL_ENV=/.venv \
    PATH="/.venv/bin:$PATH"

RUN pip install --no-cache-dir poetry
COPY app/pyproject.toml app/poetry.lock* ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

COPY ./app/ ./

COPY entrypoint.sh /entrypoint.sh

ENTRYPOINT ["bash", "/entrypoint.sh"]
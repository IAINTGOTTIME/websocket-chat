FROM python:3.12-alpine AS build

RUN pip install pipenv

# COPY . .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

ENV PATH="/.venv/bin:$PATH"

CMD ["alembic upgrade head && uvicorn chat:app"]


FROM python:3.12

RUN pip install pipenv

COPY . .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

ENV PATH="/.venv/bin:$PATH"

CMD ["sh", "-c", "alembic upgrade head && uvicorn chat:app --host 0.0.0.0 --port 8000"]

EXPOSE 8080
FROM python:3.7-alpine

WORKDIR /usr/src/app
RUN pip install -U pip pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install
COPY . .

ENV PYTHONUNBUFFERED TRUE
EXPOSE 8000
ENTRYPOINT [ "pipenv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "app:app" ]

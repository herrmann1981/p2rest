FROM python:3.7

ARG DATABASE_URI

COPY . /app
WORKDIR /app

COPY ./requirements.txt ../requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8080

ENV GUNICORN_CMD_ARGS="--log-level=debug"

ENTRYPOINT ["gunicorn", "-w", "2", "-b", ":8080", "wsgi:app"]
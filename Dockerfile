FROM python:3.7-slim

WORKDIR /home/code
RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc libmariadbclient-dev

RUN mkdir files

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY ./Hypercorn-PROD.toml ./Hypercorn.toml
COPY ./.env ./.env
COPY ./alembic.ini ./alembic.ini

COPY ./templates ./templates
COPY ./static ./static
COPY ./app ./app

RUN STARTLETTE_CONFIG=.env alembic upgrade head

CMD STARTLETTE_CONFIG=.env hypercorn app/main.py:app -c Hypercorn.toml --access-log - --error-log -
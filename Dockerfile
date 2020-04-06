FROM python:3.7-slim

WORKDIR /home/code
RUN apt-get update && apt-get upgrade -y && apt-get install -y wget build-essential libffi-dev libssl-dev libmariadbclient-dev

RUN wget https://cdn.cub3d.pw/auth/public.pem

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

COPY ./Hypercorn-PROD.toml ./Hypercorn.toml
COPY ./alembic.ini ./alembic.ini

COPY ./templates ./templates
COPY ./static ./static
COPY ./app ./app

CMD alembic upgrade head && hypercorn app.main:app -c Hypercorn.toml --access-log - --error-log -

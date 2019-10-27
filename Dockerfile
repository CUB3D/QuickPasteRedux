FROM python:3.7-slim

WORKDIR /home/code

RUN mkdir files

RUN apt-get update && apt-get upgrade -y && apt-get install -y gcc libmariadbclient-dev

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

CMD alembic upgrade head && hypercorn app/main.py:app -c $HYPERCORN_CONFIG --access-log - --error-log -
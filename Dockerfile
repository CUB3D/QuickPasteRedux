FROM python:3.7-slim

WORKDIR /home/code

RUN mkdir files

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

CMD alembic upgrade head && hypercorn app/main.py:app -c $HYPERCORN_CONFIG --access-log - --error-log -
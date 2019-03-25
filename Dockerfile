FROM python:3.7-slim

WORKDIR /home/code

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

EXPOSE 8080

CMD alembic upgrade head && hypercorn app/main.py:app -c $HYPERCORN_CONFIG --access-log - --error-log -
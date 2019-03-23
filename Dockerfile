FROM python:3.7-slim

WORKDIR /home/code

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

EXPOSE 8080

CMD hypercorn app/main.py:app -c Hypercorn-DEV.toml --access-log - --error-log -
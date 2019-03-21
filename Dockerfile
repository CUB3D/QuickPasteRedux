FROM python:3.7-slim

WORKDIR /home/code

COPY ./requirements.txt ./
RUN pip install -r ./requirements.txt

EXPOSE 8080

COPY ./style/ ./style/
COPY ./app/ ./app/
COPY ./templates/ ./templates/

CMD python app/main.py
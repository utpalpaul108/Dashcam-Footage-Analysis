FROM python:3.8-slim-buster

RUN apt update -y && apt install awscli -y
WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py"]
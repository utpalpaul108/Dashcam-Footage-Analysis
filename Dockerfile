FROM python:3.8-slim-buster

RUN apt-get update -y && apt-get install awscli libgl1 -y 
WORKDIR /app

COPY . /app
RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
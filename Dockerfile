FROM python:3.10-slim-buster

# Expose port want to run app on
EXPOSE 8000

# Set working directory and copy app code 
WORKDIR /app
COPY . /app

# Upgrade pip and install requirements
RUN apt-get update -y && apt-get install -y  libgl1 libglib2.0-0
RUN pip install -U pip
RUN pip install -r requirements.txt

# Run
ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
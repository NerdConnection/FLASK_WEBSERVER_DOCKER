FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt . 
COPY src /app/src

RUN pip install -r requirements.txt

CMD ["python3", "src/app.py"]

FROM python:3.12.7-alpine
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
CMD python /usr/src/burger/main.py

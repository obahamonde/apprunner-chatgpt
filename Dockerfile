FROM python:3.7

ARG LOCAL_PATH

COPY $LOCAL_PATH /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]


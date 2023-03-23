FROM python:3.7

ARG LOCAL_PATH

WORKDIR /app

COPY requirements.txt /app

RUN pip install --upgrade pip \
    pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "main.py"]
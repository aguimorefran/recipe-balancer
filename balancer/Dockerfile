
FROM python:3.11.5

WORKDIR /app

COPY ./app/requirements.txt /app/requirements.txt

RUN cat /app/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

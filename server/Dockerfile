FROM python:3.9-bullseye

RUN mkdir /model_backend

WORKDIR /model_backend

COPY . .

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "34.69.232.63", "--port", "8000"]


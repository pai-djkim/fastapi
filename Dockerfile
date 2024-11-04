FROM python:3.9

WORKDIR /home

COPY ./requirements.txt /home/requirements.txt

RUN pip install -r /home/requirements.txt

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
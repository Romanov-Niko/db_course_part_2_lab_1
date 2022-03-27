FROM python:3.8

WORKDIR /application
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./code ./code
CMD cd code && python main.py
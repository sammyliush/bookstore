FROM python:3

RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data/

RUN pip install --no-cache-dir -r requirements.txt

ADD . /data

EXPOSE 8080

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
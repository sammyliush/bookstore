FROM python:3

RUN mkdir /data
WORKDIR /data
ADD requirements.txt /data/

RUN pip install --no-cache-dir -r requirements.txt

ADD . /data

EXPOSE 8083

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8083"]
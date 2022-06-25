FROM python:3.9

RUN mkdir -p /home/api
WORKDIR /var/www

COPY requirements.txt /var/www/
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . /var/www/
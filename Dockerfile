FROM tiangolo/uwsgi-nginx-flask:python3.6


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
 
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
 
COPY ./app /usr/src/app
COPY prod.env /usr/src/app/
COPY stagging.env /usr/src/app/

# to configure nginx anf uwsgi serve
COPY ./nginx.conf /app
COPY ./uwsgi.ini /app
ENV UWSGI_INI /app/uwsgi.ini

# to use queue with the server uncomment this
# COPY ./prestart.sh /app

# comment this to use http server
# CMD [ "python", "-u", "task.py" ]

# ENV LISTEN_PORT 3000
# EXPOSE 3000





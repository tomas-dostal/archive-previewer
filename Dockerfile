FROM python:3.10

RUN mkdir /app
COPY . /app
COPY pyproject.toml /app
WORKDIR /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
    RUN poetry install --no-dev

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
   # && apt-get -y install python3-dev \
    && apt-get -y install build-essential

COPY nginx.conf /etc/nginx
RUN chmod +x ./start.sh
EXPOSE 5000

CMD ["./start.sh"]

#
## configure the container to run in an executed manner
#ENTRYPOINT [ "poetry" ]
#
#CMD ["run", "flask", "run", "main.py"]

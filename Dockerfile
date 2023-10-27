FROM python:3.8

RUN apt-get update && apt-get -y install cron vim

# set the working directory in the container
WORKDIR /app

# copy the dependencies file to the working directory

COPY crontab /etc/cron.d/crontab

RUN chmod 0644 /etc/cron.d/crontab

# install dependencies

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip install MechanicalSoup

# copy the content of the local src directory to the working directory
COPY src/ ./

RUN /usr/bin/crontab /etc/cron.d/crontab

CMD ["cron", "-f"]
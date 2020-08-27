FROM python:3.8-slim-buster

COPY . .

RUN apt update && \
    apt install -y tcpdump cron net-tools && \
    pip3 install -r requirements.txt

COPY crontab /etc/cron.d/monitor-cron
RUN chmod 644 /etc/cron.d/monitor-cron

RUN chmod +x entrypoint.sh
CMD ["/bin/bash", "entrypoint.sh"] 
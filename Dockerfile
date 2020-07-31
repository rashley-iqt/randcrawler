FROM python:3.8-slim-buster

COPY . .

RUN apt update && \
    apt install -y tcpdump && \
    pip3 install -r requirements.txt

CMD tcpdump -ne -w /pcaps/randcrawler.pcap -C 100 &  python3 randcrawler.py
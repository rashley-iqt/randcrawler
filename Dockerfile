FROM python:3.8-slim-buster

COPY . .

RUN apt update && \
    apt install -y tcpdump watch && \
    pip3 install -r requirements.txt
RUN chmod +x entrypoint.sh
CMD ["/bin/sh", "entrypoint.sh"] 
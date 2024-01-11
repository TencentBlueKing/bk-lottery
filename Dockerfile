FROM python:3.6.8

WORKDIR ./lottery

ADD . .

RUN chmod +x ./startup.sh

CMD ["./startup.sh"]

FROM python:3.9-slim AS app
RUN pip3 install --no-cache-dir torch numpy

FROM pwn.red/jail:0.3.0
COPY --from=app / /srv
COPY arson.py /srv/app/run
COPY flag.txt /srv/app
RUN mv /srv/app/flag.txt /srv/app/flag.$RANDOM$RANDOM.txt

ENV JAIL_MEM=100M
ENV JAIL_PIDS=50
ENV JAIL_TMP_SIZE=500M
ENV JAIL_CPU=500

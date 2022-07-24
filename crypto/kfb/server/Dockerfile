FROM python:3.10-slim-bullseye AS app

RUN pip3 install --no-cache-dir more-itertools pycryptodome

FROM pwn.red/jail:0.3.0

COPY --from=app / /srv
COPY flag.txt /srv/app/
COPY server.py /srv/app/run

ENV JAIL_MEM=30M JAIL_CPU=500

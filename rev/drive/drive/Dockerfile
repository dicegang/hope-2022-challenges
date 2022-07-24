FROM pwn.red/jail:0.3.0
COPY --from=python:slim / /srv
COPY run.py /srv/app/run
COPY drive flag.txt /srv/app/

ENV JAIL_MEM=30M

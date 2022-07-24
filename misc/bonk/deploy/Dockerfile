FROM pwn.red/jail:0.3.0

COPY --from=python:3.10 / /srv
COPY bonk.py /srv/app/run
COPY flag.txt /srv/app
RUN mv /srv/app/flag.txt /srv/app/flag.$RANDOM$RANDOM.txt

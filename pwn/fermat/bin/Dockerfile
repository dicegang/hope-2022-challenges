FROM pwn.red/jail:0.3.0
COPY --from=ubuntu:22.10 / /srv
COPY challenge /srv/app/run
COPY flag.txt /srv/app/

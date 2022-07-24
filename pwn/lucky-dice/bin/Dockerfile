FROM pwn.red/jail:0.3.0

COPY --from=ubuntu:focal-20220426 / /srv
COPY luckydice /srv/app/run
COPY flag.txt /srv/app/

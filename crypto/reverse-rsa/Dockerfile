FROM python:slim AS app

RUN pip install pycryptodome

FROM redpwn/jail
COPY --from=app / /srv
COPY --chmod=755 reverse-rsa.py /srv/app/run
COPY flag.txt ciphertext.txt /srv/app/

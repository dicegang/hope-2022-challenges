FROM python:3.9.2-slim-buster

RUN pip install flask gunicorn --no-cache-dir

WORKDIR /app
COPY app.py flag.txt ./
RUN mv flag.txt flag-$(cat /proc/sys/kernel/random/uuid).txt
USER nobody

CMD ["gunicorn", "-w5", "-t5", "--graceful-timeout", "0", "-unobody", "-gnogroup", "-b0.0.0.0", "app:app"]

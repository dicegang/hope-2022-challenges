FROM python:3.9.2-slim-buster

RUN pip install aiohttp --no-cache-dir

WORKDIR /app
COPY app.py server.py ./

USER nobody

ENV FLAG hope{ecid_gnivlovni_semordnilap_fo_kniht_ton_dluoc}

EXPOSE 3000

CMD ["python", "app.py"]

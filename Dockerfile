FROM python:3.8

WORKDIR /app

RUN pip install --no-cache-dir discord.py

COPY phillipa/ ./phillipa/
COPY good.txt ./
COPY bad.txt ./


CMD ["python", "-m", "phillipa"]

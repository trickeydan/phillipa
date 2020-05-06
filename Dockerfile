FROM python:3.8

COPY phillipa.py ./

RUN pip install --no-cache-dir discord.py

CMD ["python", "phillipa.py"]

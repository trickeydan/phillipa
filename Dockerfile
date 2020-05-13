FROM python:3.8

COPY phillipa.py ./
COPY good.txt ./
COPY bad.txt ./

RUN pip install --no-cache-dir discord.py

ENV DISCORD_TOKEN="NzA3NjYyNjEwMTk5MzQ3Mjgx.Xrxglg.Qk9sxvW0e33JpS8MttUfYuVrUqQ"

CMD ["python", "phillipa.py"]

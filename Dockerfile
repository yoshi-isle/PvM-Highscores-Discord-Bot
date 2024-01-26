FROM --platform=linux/amd64 ghcr.io/owl-corp/python-poetry-base:3.11-slim

# set working directory to bot
WORKDIR /bot

ARG BOT_TOKEN
ENV BOT_TOKEN ${BOT_TOKEN}

ARG MONGODB_CONNECTION_STRING
ENV MONGODB_CONNECTION_STRING ${MONGODB_CONNECTION_STRING}

# some environment stuff to prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt 

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Copy the source code in last to optimize rebuilding the image
COPY . .

# set working directory to src so that the pathing to the json file works
WORKDIR /bot/src

CMD ["python3", "bot.py"]
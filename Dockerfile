FROM --platform=linux/arm64/v8 ghcr.io/owl-corp/python-poetry-base:3.11-slim

# set working directory to bot
WORKDIR /bot

ARG BOT_TOKEN
ENV BOT_TOKEN ${BOT_TOKEN}

ARG MONGODB_CONNECTION_STRING
ENV MONGODB_CONNECTION_STRING ${MONGODB_CONNECTION_STRING}

ARG WOM_TOKEN
ENV WOM_TOKEN ${WOM_TOKEN}

ARG CLIENT_ID
ENV CLIENT_ID ${CLIENT_ID}

ARG CLIENT_SECRET
ENV CLIENT_SECRET ${CLIENT_SECRET}

ARG ACCESS_TOKEN
ENV ACCESS_TOKEN ${ACCESS_TOKEN}

ARG REFRESH_TOKEN
ENV REFRESH_TOKEN ${REFRESH_TOKEN}

# some environment stuff to prevent .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt 

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Copy the source code in last to optimize rebuilding the image
COPY . .

CMD ["python3", "src/bot.py"]
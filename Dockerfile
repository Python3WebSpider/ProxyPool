FROM alpine:3.7
WORKDIR /app
RUN apk add --no-cache --virtual .build-deps g++ python3-dev libffi-dev \
    openssl-dev libxml2-dev libxslt-dev gcc musl-dev py3-pip && \
    apk add --no-cache --update python3 && \
    pip3 install --upgrade pip setuptools
COPY requirements.txt .
RUN pip3 install -r requirements.txt && \
apk del g++ gcc musl-dev libxml2-dev
COPY . .
# RUN pip install -r requirements.txt  -i https://pypi.douban.com/simple
VOLUME ["/app/proxypool/crawlers/private"]
CMD ["supervisord", "-c", "supervisord.conf"]

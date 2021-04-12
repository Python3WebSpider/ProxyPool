FROM python:3.6-alpine
WORKDIR /app
COPY . .
# RUN pip install -r requirements.txt  -i https://pypi.douban.com/simple
RUN apk add --no-cache libxml2-dev libxslt-dev gcc musl-dev && \
pip install -r requirements.txt && \
apk del gcc musl-dev libxml2-dev
VOLUME ["/app/proxypool/crawlers/private"]
CMD ["supervisord", "-c", "supervisord.conf"]

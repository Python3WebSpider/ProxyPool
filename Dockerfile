FROM python:3.6
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt  -i https://pypi.douban.com/simple
VOLUME ["/app/proxypool/crawlers/private"]
CMD ["supervisord", "-c", "supervisord.conf"]

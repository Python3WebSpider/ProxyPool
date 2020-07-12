FROM python:3.6
WORKDIR /app
COPY . .
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
VOLUME ["/app/proxypool/crawlers/private"]
CMD ["supervisord", "-c", "supervisord.conf"]

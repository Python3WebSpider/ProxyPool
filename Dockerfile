FROM python:3.6
WORKDIR /app
COPY . .
RUN pip install -U pip && pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
VOLUME ["/app/proxypool/crawlers/private"]
CMD ["supervisord", "-c", "supervisord.conf"]

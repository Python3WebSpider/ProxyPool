FROM python:3.6
WORKDIR /app
COPY . .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt
VOLUME ["/app/proxypool/crawlers/private"]
CMD ["supervisord", "-c", "supervisord.conf"]

FROM python:3.6
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
VOLUME ["/app/proxypool/crawlers"]
CMD ["supervisord", "-c", "supervisord.conf"]

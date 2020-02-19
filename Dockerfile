FROM python:3.6
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["supervisord", "-c", "supervisord.conf"]

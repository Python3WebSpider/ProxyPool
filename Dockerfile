FROM python:3.11-slim AS build
COPY requirements.txt .
RUN apt-get update &&\
    apt-get install -y --no-install-recommends gcc g++ libxml2-dev libxslt1-dev &&\
    pip install -U pip &&\
    pip install --timeout 60 --user --no-cache-dir --no-warn-script-location -r requirements.txt &&\
    rm -rf /var/lib/apt/lists/*

FROM python:3.11-slim
ENV APP_ENV=prod
ENV LOCAL_PKG="/root/.local"
COPY --from=build ${LOCAL_PKG} ${LOCAL_PKG}
RUN ln -sf ${LOCAL_PKG}/bin/* /usr/local/bin/
WORKDIR /app
COPY . .
EXPOSE 5555
VOLUME ["/app/proxypool/crawlers/private"]
ENTRYPOINT ["supervisord", "-c", "supervisord.conf"]
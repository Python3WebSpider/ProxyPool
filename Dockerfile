FROM python:3.7-alpine AS build
COPY requirements.txt .
RUN apk update &&\
    apk add --no-cache gcc g++ libffi-dev openssl-dev libxml2-dev libxslt-dev build-base musl-dev &&\
    pip install -U pip &&\
    pip install --timeout 30 --user --no-cache-dir --no-warn-script-location -r requirements.txt

FROM python:3.7-alpine
ENV APP_ENV=prod
ENV LOCAL_PKG="/root/.local"
COPY --from=build ${LOCAL_PKG} ${LOCAL_PKG}
RUN apk update && apk add --no-cache libffi-dev openssl-dev libxslt-dev &&\
    ln -sf ${LOCAL_PKG}/bin/* /usr/local/bin/
WORKDIR /app
COPY . .
EXPOSE 5555
VOLUME ["/app/proxypool/crawlers/private"]
ENTRYPOINT ["supervisord", "-c", "supervisord.conf"]
# ProxyPool

## Requirements

* Docker 

  or 

* Python: >=3.6
* Redis
* Environment: Virtual Env

## Run with Docker

```shell script
docker-compose up
```

## Run without Docker

Here are steps to run ProxyPool.

### Install Redis

You need to install Redis locally or get a Redis server firstly.

Next set Redis environment:

```shell script
export REDIS_HOST='localhost'
export REDIS_PORT=6379
export REDIS_PASSWORD='foobar'
```

Also you can just set the Redis Connection String:

```shell script
export REDIS_CONNECTION_STRING='redis://[password]@host:port'
```

You can choose one method of above to set Redis environment.

### Clone ProxyPool

```shell script
https://github.com/Python3WebSpider/ProxyPool
cd ProxyPool
```

### Install Requirements

```shell script
pip3 install -r requirements.txt
```

### Run ProxyPool

You can run all of the processors including Getter、Tester、
Server:

```shell script
python3 run.py
```

or run with args to run specific processor:

```shell script
python3 run.py --processor getter
python3 run.py --processor tester
python3 run.py --processor server
```

### Usage

After running the ProxyPool, you can visit 
[http://localhost:5555/random](http://localhost:5555/) to access random proxy.  
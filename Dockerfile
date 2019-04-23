FROM ubuntu:18.04
COPY . /app
COPY ./sources.list /etc/apt/sources.list
WORKDIR /app
RUN apt update
RUN apt-get install -y redis python3 python3-pip 
RUN python3 -m pip install -i https://pypi.mirrors.ustc.edu.cn/simple -r requirements.txt
EXPOSE 5555
CMD bash -c "(redis-server; echo redis started) & (python3 run.py)"

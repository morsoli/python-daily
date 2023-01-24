FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG C.UTF-8

RUN sed -i 's@http://archive.ubuntu.com/ubuntu/@http://mirrors.aliyun.com/ubuntu/@g' /etc/apt/sources.list

RUN mkdir -p /root/demo
WORKDIR /root/demo

#COPY requirements.txt requirements.txt
#COPY . /root/directory


RUN apt-get clean && \
    apt-get update && \
    apt-get install -y libmysqlclient-dev tzdata wget curl ffmpeg flac \
    python3 python3-dev python3-pip libpcre3 libpcre3-dev  uwsgi-plugin-python3 \
    && apt-get clean \
    && apt-get autoclean \
    && ln -sf /usr/bin/pip3 /usr/bin/pip && ln -sf /usr/bin/python3 /usr/bin/python

# pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# ENTRYPOINT [ "/root/demo/docker_init.sh" ] # 执行shell脚本

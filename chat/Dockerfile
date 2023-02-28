FROM python:3.10-slim

RUN sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list && \
    rm -Rf /var/lib/apt/lists/* && apt update && apt install git wget make -y

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn && pip install --upgrade pip

WORKDIR /langchain
COPY . .
RUN pip install -r requirements.txt

EXPOSE 9000

ENTRYPOINT ["uvicorn", "main:app", "--reload"]
FROM continuumio/miniconda3:4.11.0

RUN sed -i -e "s/deb.debian.org/mirrors.tuna.tsinghua.edu.cn/" /etc/apt/sources.list && sed -i -e "s/security.debian.org/mirrors.tuna.tsinghua.edu.cn/" /etc/apt/sources.list

RUN apt update && \
    apt install ffmpeg libgl1-mesa-glx && \
    apt autoremove -y

RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

RUN conda install -y pytorch

RUN pip3 install --upgrade torch==1.9.0 torchvision==0.10.0

RUN pip install towhee
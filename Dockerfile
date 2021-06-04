FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /workspace
COPY . /workspace/
WORKDIR /workspace/

# install package
RUN echo "nameserver 8.8.8.8" > /etc/resolv.conf && pip install pipenv && pipenv sync

# genenv
RUN VERSION=PROD python genenv.py

# time
RUN echo "Asia/Taipei" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

CMD ["/bin/bash"]

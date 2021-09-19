FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /workspace
COPY . /workspace/
WORKDIR /workspace/

# install package
RUN pip install pipenv && pipenv sync

# genenv
RUN --mount=type=secret,id=MYSQL_HOST \
  --mount=type=secret,id=MYSQL_USER \
  --mount=type=secret,id=MYSQL_PASSWORD \
  --mount=type=secret,id=MYSQL_PORT \
  export MYSQL_HOST=$(cat /run/secrets/MYSQL_HOST) && \
  export MYSQL_USER=$(cat /run/secrets/MYSQL_USER) && \
  export MYSQL_PASSWORD=$(cat /run/secrets/MYSQL_PASSWORD) && \
  export MYSQL_PORT=$(cat /run/secrets/MYSQL_PORT) && \
  VERSION=PROD python genenv.py

# time
RUN echo "Asia/Taipei" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

CMD ["/bin/bash"]

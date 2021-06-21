FROM continuumio/miniconda3:4.3.27

RUN apt-get update

RUN mkdir /workspace
COPY . /workspace/
WORKDIR /workspace/

# install package
RUN pip install pipenv && pipenv sync

# genenv
RUN python genenv.py

# time
RUN echo "Asia/Taipei" > /etc/timezone
RUN dpkg-reconfigure -f noninteractive tzdata

CMD ["/bin/bash"]

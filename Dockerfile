FROM python:3.8
#FROM ubuntu:22.04

WORKDIR /app
#ARG DEBIAN_FRONTEND=noninteractive
#RUN apt-get update && \
#    apt-get install -y software-properties-common && \
#    add-apt-repository -y ppa:deadsnakes/ppa && \
#    apt-get update && \
#    apt install -y python3.8

#RUN apt-get -y install python3-pip

COPY requirements.txt requirements.txt
#RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
COPY . .

RUN apt-get update && apt-get install -y tdsodbc unixodbc-dev \
 && apt install unixodbc -y  \
 && apt-get clean -y
RUN ls -l /usr/lib/x86_64-linux-gnu/odbc/

#RUN ./driver.sh
#run ["python", "process_data.py"]
#run ["python", "train_model.py"]
#run ["python", "test_model.py"]
#run ["python", "test/test_cat.py"]
#run ["python", "test/test_len.py"]
#run ["python", "test/test_type.py"]
CMD ["python3", "main.py"]

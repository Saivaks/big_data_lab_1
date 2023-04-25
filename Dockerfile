FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "big-data.py"]
CMD ["python3", "test/test_cat.py"]
CMD ["python3", "test/test_len.py"]
CMD ["python3", "test/test_type.py"]

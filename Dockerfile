FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
run ["python", "process_data.py"]
run ["python", "train_model.py"]
run ["python", "test_model.py"]
run ["python", "test/test_cat.py"]
run ["python", "test/test_len.py"]
run ["python", "test/test_type.py"]

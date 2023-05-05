FROM python:3.8

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
#run ["sudo", "su"]
run wget "https://gallery.technet.microsoft.com/ODBC-Driver-13-for-Ubuntu-b87369f0/file/154097/2/installodbc.sh" -y
run ["sh", "installodbc.sh"]
#run ["python", "process_data.py"]
#run ["python", "train_model.py"]
#run ["python", "test_model.py"]
#run ["python", "test/test_cat.py"]
#run ["python", "test/test_len.py"]
#run ["python", "test/test_type.py"]
CMD ["python", "main.py"]

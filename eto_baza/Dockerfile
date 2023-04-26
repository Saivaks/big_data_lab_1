FROM mcr.microsoft.com/mssql/server:2019-latest

docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=12345And" `
   -p 1433:1433  --name trash --hostname baza `
   -d `
   mcr.microsoft.com/mssql/server:2019-latest
#-v sqlvolume:/data
#WORKDIR /app
#
#COPY requirements.txt requirements.txt
#RUN pip3 install -r requirements.txt
#COPY . .
#run ["python", "process_data.py"]
#run ["python", "train_model.py"]
#run ["python", "test_model.py"]
#run ["python", "test/test_cat.py"]
#run ["python", "test/test_len.py"]
#run ["python", "test/test_type.py"]

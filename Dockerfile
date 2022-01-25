FROM salomaosan/python-mssql-odbc

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./zabbix.py" ]
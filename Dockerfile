FROM salomaosan/python-mssql-odbc

WORKDIR /usr/src/app

COPY . .

CMD [ "python", "./update_clientes.py" ]
import sys
import os
import pymssql
from zabbix_api import ZabbixAPI


# Acessos ao qualitor
QUALITOR_SERVER = os.environ['QUALITOR_SERVER']
QUALITOR_DATABASE = os.environ['QUALITOR_DATABASE']
QUALITOR_USER = os.environ['QUALITOR_USER']
QUALITOR_PASS = os.environ['QUALITOR_PASS']

# Acessos ao ZABBIX
ZBX_URL = os.environ['ZBX_URL']
ZBX_USER = os.environ['ZBX_USER']
ZBX_PASS = os.environ['ZBX_PASS']
ZBX_GROUPID = os.environ['ZBX_GROUPID']

def qlt_connection():
    print("\n\tCarregando query SQL.")
    with open("./conf/clientes_mv_onpremise.sql") as file:
        strfile = file.read()
    
    print("\tConectando no Qualitor")
    try:
        conn = pymssql.connect(server=QUALITOR_SERVER, user=QUALITOR_USER, password=QUALITOR_PASS, database=QUALITOR_DATABASE)
        print("\tConectado!")
        cursor = conn.cursor(as_dict=True)
        print("\tBuscando clientes MV sem contrato Cloud.")
        cursor.execute(strfile)
        list_clients = []
        
        for row in cursor:
            row['cod_qualitor'] = str(row['cdcliente']).rjust(5, '0')
            row.pop('cdcliente')
            list_clients.append(row)
        conn.close()
        print("\tConexão encerrada com o banco.")
        print("\tRetornando lista de clientes.\n")
        return list_clients
    except ValueError:
        print("\tAlgum erro na conexão com o Qualitor")
        sys.exit()

def zbx_connection():
    try:
        print("\tConectando na API do Zabbix...")
        zapiConn = ZabbixAPI(server=ZBX_URL, timeout=120)
        zapiConn.login(ZBX_USER,ZBX_PASS)
        print("\tConectado!\n")
        return zapiConn
    except ValueError:
        print("\tAlgum erro na conexão com o Zabbix")
        sys.exit()


# Listando hosts que tenham o codigo do qualitor defiinido'
def zbx_get_hosts_by_name(zconn, q_code):
    print("\tListando hosts do cliente")
    hosts = zconn.host.get({
        "output": ["hostid"],
        "filter":{
            "status": 0
        },
        "search": {
            "host": f"*{q_code}*"
        },
        "searchWildcardsEnabled": "true"
    })
    return hosts

# Atualizando hosts para o grupo
def zbx_mu_hosts(zconn, hosts):
    print("\tAtualizando hosts encontrado para o grupo MV on-premise")
    zconn.hostgroup.massupdate({
        "groups": [
            {
                "groupid": ZBX_GROUPID
            }
        ],
        "hosts": hosts
    })

def main():
    print("# INICIANDO O PROCESSO DE ATUALIZAÇÃO DOS CLIENTES MV PARA O GRUPO ON-PREMISE #")
    list_clients = qlt_connection()
    zapi = zbx_connection()

    hosts = []
    for client in list_clients:
        print(f" >> Atualizando cliente: {client['nmcliente']}")
        hosts.extend(zbx_get_hosts_by_name(zapi, client['cod_qualitor']))
    
    zbx_mu_hosts(zapi, hosts)
    
    print()

    zapi.logout()
    print("\t\nConexão com Zabbix encerrada")
    print("# ATUALIZAÇÃO ENCERRADA #")

if __name__ == '__main__':
    main()
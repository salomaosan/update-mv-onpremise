import json
import sys
import pymssql
from zabbix_api import ZabbixAPI

# Acessos ao qualitor
SERVER ='oci-db-qualitor.flowti.com.br'
USER_QUALITOR ='svc_zabbix_mon'
PASS_QUALITOR ='1QAZ0okm2021'
DATABASE ='Qualitor_PRD'

# Acessos ao ambiente de homologação ZABBIX
URL = 'http://192.168.9.13/zabbix/api_jsonrpc.php'
USER_ZABBIX = 'Admin'
PASS_ZABBIX = 'zabbixhomol'
GROUPID = "361"

# Acessos ao ambiente de produção ZABBIX
# URL = 'https://xcnj.myz.cloud/zabbix/api_jsonrpc.php'
# USER_ZABBIX = 'zscript'
# PASS_ZABBIX = 'UyHaDP6SLAmjsj#'

def qlt_connection():
    with open("clientes_mv_onpremise.sql") as file:
        strfile = file.read()
    
    try:
        conn = pymssql.connect(server=SERVER, user=USER_QUALITOR, password=PASS_QUALITOR, database=DATABASE)
        cursor = conn.cursor(as_dict=True)
        cursor.execute(strfile)
        list_clients = []
        
        for row in cursor:
            row['cod_qualitor'] = 'q' + str(row['cdcliente']).rjust(5, '0')
            row.pop('cdcliente')
            list_clients.append(row)
        conn.close()
        return list_clients
    except ValueError:
        print("Erro na conexão com o Zabbix")
        sys.exit()

def zbx_connection():
    try:
        print("Conectando na API do Zabbix...")
        zapiConn = ZabbixAPI(server=URL, timeout=120)
        zapiConn.login(USER_ZABBIX,PASS_ZABBIX)
        return zapiConn
    except ValueError:
        print("Erro na conexão com o Zabbix")
        sys.exit()


# Listando hosts que tenham o codigo do qualitor defiinido'
def zbx_get_hosts_by_name(zconn, q_code):
    print(f"Procurando hosts {q_code}")
    groups = zconn.host.get({
        "output": ["hostid"],
        "filter":{
            "status": 0
        },
        "search": {
            "host": f"*{q_code}"
        },
        "searchWildcardsEnabled": "true"
    })
    return groups

# Atualizando hosts para o grupo
def zbx_mu_hosts(zconn, hosts):
    print(f"Atualizando hosts")
    mi = zconn.hostgroup.massupdate({
        "groups": [
            {
                "groupid": GROUPID
            }
        ],
        "hosts": hosts
    })
    return mi

def main():
    list_clients = qlt_connection()
    zapi = zbx_connection()

    for client in list_clients:
        hosts = zbx_get_hosts_by_name(zapi, client['cod_qualitor'])
        print(zbx_mu_hosts(zapi, hosts))

    zapi.logout()

if __name__ == '__main__':
    main()
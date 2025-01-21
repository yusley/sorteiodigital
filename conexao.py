import cx_Oracle

#def createConnectionCaixa(host, user, password, database):  

  #  dsn = cx_Oracle.makedsn(host, "1521", service_name=database)       
 #   conexao = cx_Oracle.connect(user=user, password=password, dsn=dsn)
#
 #   return conexao

def createConnectionCaixa(host, user, password, database):  

    cx_Oracle.init_oracle_client(lib_dir=r"c:\\instantclient_11_2")

    conexao = cx_Oracle.connect("CAIXA/CAIXA@127.0.0.1/xe")
    return conexao

conexao = createConnectionCaixa('LOCALHOST','CAIXA','CAIXA','XEPDB1')
cursor = conexao.cursor()
cursor.execute('''

SELECT
            TO_CHAR("DATA", 'DD-MON-YYYY') AS "DTVENDA",
            NUMPEDECF,
            NUMCAIXA,
            PROTOCOLONFCE,
            VLTOTAL
        FROM
            PCPEDCECF p
        INNER JOIN PCCLIENT C ON (P.CODCLI = C.CODCLI)
        WHERE
            "DATA" = trunc(SYSDATE)
            AND VLTOTAL >= 1
        
''')

dados = cursor.fetchall()

print(dados)

import win32print
import win32api
import os
import cx_Oracle
import ast
from main import readConfig
from oracle import createConnection

#cx_Oracle.init_oracle_client(lib_dir=r"C:\\instantclient_11_2")

def createConnectionCaixa(host, user, password, database):  

    dsn = cx_Oracle.makedsn(host, "1521", service_name=database)       
    conexao = cx_Oracle.connect(user=user, password=password, dsn=dsn)

    return conexao


def pegaUltimaVenda(conexao, valorCupom):
    dados = ()

    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT MAX(IDCUPOM) FROM MSSORTEIO@dblservidor
        """)
        
        dados = cursor.fetchone()
                
    except Exception as f:
        print("Erro ao pegar última venda\n{}.".format(f))
    
    finally:
        return dados


#print(pegaUltimaVenda(createConnectionCaixa('LOCALHOST','CAIXA','CAIXA','XE'),'100'))


arquivo = r"C:\Users\yusley\Desktop\imprimir\cupom.txt"
caminho = r"C:\Users\yusley\Desktop\imprimir"


def adicionarFonecs(cupom):

    listadeDados = readConfig()[9]

    
    listadeDados = ast.literal_eval(listadeDados)
    

    conexao = createConnection()

    cursor = conexao.cursor()

    cursor.execute(f'''
        SELECT distinct(SELECT DISTINCT(CODFORNEC)  FROM PCPRODUT WHERE p.CODPROD = CODPROD ) fornecedor  FROM PCPEDIECF p WHERE NUMPEDECF = {cupom}
    ''')

    dados = cursor.fetchall()
   
    qtdCupons = 0

    for produt in dados:
        
        if produt[0] in listadeDados:
            
            qtdCupons +=1
            break

    return qtdCupons

print(adicionarFonecs(1900000203))
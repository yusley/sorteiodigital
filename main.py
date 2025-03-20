import cx_Oracle
import win32print
import os
import re
import Funcoes
from time import sleep
from GeraPDF import gera_pdf
from criarcupom import *
import ast
import traceback
# from oracle import createConnection, createConnection2


def readConfig():
    file = open("C:\\SORTEIODIGITAL\\config\\config.txt", 'r', encoding='ANSI')
    txt = file.readlines()
    host = (re.sub('\n', '', str(txt[0]))).split("=")[1]
    user = (re.sub('\n', '', str(txt[1]))).split("=")[1]
    password = (re.sub('\n', '', str(txt[2]))).split("=")[1]
    database = (re.sub('\n', '', str(txt[3]))).split("=")[1]
    impressora = (re.sub('\n', '', str(txt[4]))).split("=")[1]
    img = (re.sub('\n', '', str(txt[5]))).split("=")[1]
    valor_cupom = (re.sub('\n', '', str(txt[6]))).split("=")[1]
    codfilial = (re.sub('\n', '', str(txt[7]))).split("=")[1]
    fornecs =  (re.sub('\n', '', str(txt[9]))).split("=")[1]
    listaFornecs = (re.sub('\n', '', str(txt[10]))).split("=")[1]
    rateiafornec =  (re.sub('\n', '', str(txt[11]))).split("=")[1]
    listaprods = (re.sub('\n', '', str(txt[12]))).split("=")[1]
    lista = []

    lista.append(host)
    lista.append(user)
    lista.append(password)
    lista.append(database)
    lista.append(impressora)
    lista.append(img)
    lista.append(valor_cupom)
    lista.append(codfilial)
    lista.append(fornecs)
    lista.append(listaFornecs)
    lista.append(rateiafornec)
    lista.append(listaprods)
    
    
    return lista    

# def createConnection():
    
#     user = "LGBRASIL"
#     password = "LS16BR"
#     db = "WINT"
    
#     conexao = cx_Oracle.connect("{}/{}@{}".format(user, password, db))

#     return conexao


def createConnectionCaixa(host, user, password, database):  

    cx_Oracle.init_oracle_client(lib_dir=r"c:\\instantclient_11_2")

    conexao = cx_Oracle.connect("CAIXA/CAIXA@127.0.0.1/xe")
    return conexao


# def createConnectionCaixa(host, user, password, database):  

#     cx_Oracle.init_oracle_client(lib_dir=r"c:\\instantclient_18_5")

#     conexao = cx_Oracle.connect("CAIXA/CAIXA@127.0.0.1/xe")
#     return conexao


def adicionarFonecs(cupom,conexao):

    listadeDados = readConfig()[9]
    
    listadeDados = ast.literal_eval(listadeDados)

    cursor = conexao.cursor()

    cursor.execute(f'''
        SELECT distinct(SELECT DISTINCT(CODFORNEC)  FROM PCPRODUT WHERE p.CODPROD = CODPROD ) fornecedor  FROM PCPEDIECF p WHERE NUMPEDECF = {cupom}
    ''')

    dados = cursor.fetchall()
   
    qtdCupons = 0

    for produt in dados:
        
        if produt[0] in listadeDados:
            if qtdCupons < 2:
                qtdCupons +=1
                print('Testando...')
                break

    print(f'''AQUI OS FORNECEDORES DOS PRODUTOS {dados}''')
    print(f'''AQUI OS FORNECEDORES DA PROMOCAO {listadeDados}''')

    return qtdCupons


def insereParticipacao(conexao, dtvenda, numcupom, numcaixa, protocolo, vltotal, qtdCupons):
    
    listaNumerosCupons = []
    try:    
        cursor = conexao.cursor()
        for c in range(qtdCupons):
            cursor.execute("INSERT INTO MSSORTEIO@dblservidor VALUES ((SEQ_IDCUPOM.NEXTVAL@dblservidor),'{}', {}, {}, '{}', {})".format(dtvenda, numcupom, numcaixa, protocolo, vltotal))
            conexao.commit()
            cursor.execute("SELECT MAX(IDCUPOM) FROM MSSORTEIO@dblservidor")
            cupom = cursor.fetchone()[0]
            listaNumerosCupons.append(numcupom)

    except Exception as f:
        print("Erro ao inserir participação.\n{}".format(f))

    finally:    
        return listaNumerosCupons

def pegaUltimaVenda(conexao, valorCupom):
    dados = ()

    try:
        cursor = conexao.cursor()
        cursor.execute("""
            SELECT
                TO_CHAR("DATA", 'DD-MON-YYYY') AS "DTVENDA",
                NUMPEDECF,
                NUMCAIXA,
                PROTOCOLONFCE,
                numcupom,
                VLTOTAL
            FROM
                PCPEDCECF p
            WHERE
                "DATA" = trunc(SYSDATE)
                AND VLTOTAL >= {}
                AND NUMPEDECF = (
                SELECT MAX(NUMPEDECF) FROM PCPEDCECF WHERE LENGTH(NUMPEDECF) < 10) and numped is null

        """.format(float(valorCupom)))
        
        dados = cursor.fetchone()
                
    except Exception as f:
        print("Erro ao pegar última venda\n{}.".format(f))
    
    finally:
        return dados

def pegaDadosFilial(conexao, codfilial):
    dados = ()

    try:
        cursor = conexao.cursor()
        cursor.execute("""
        SELECT
            FANTASIA,
            substr(cgc, 1, 2) || '.' || substr(cgc, 3, 3) || '.' || substr(cgc, 6, 3) || '/' || substr(cgc, 9, 4) || '-' || substr(cgc, 13, 2) AS CNPJ,
            ENDERECO,
            '(' || substr(TELEFONE, 1,2) || ')' || ' ' || substr(TELEFONE,3,4) || '-' || substr(TELEFONE,5,4) AS FONE 
        FROM
            PCFILIAL@dblservidor p
        WHERE 
            CODIGO = {}
        """.format(codfilial))
        
        dados = cursor.fetchone()
                
    except Exception as f:
        print("Erro ao pegar dados filial.\n{}".format(f))
    
    finally:
        return dados

def qtdLinhas(conexao):
    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM PCPEDCECF WHERE DATA = TRUNC(SYSDATE)")

        dados = cursor.fetchall()
        linhas = cursor.rowcount

        return int(linhas)
    
    except Exception as f:
        print("Erro pegar qtd de linhas.{}".format(f))

def atualizaUltimoCupom(conexao):
        file = open("C:\\SORTEIODIGITAL\\config\\ultimoCupom.txt", 'r', encoding='ANSI')
        cupom = file.readlines()
        ultimo = cupom[0]
        file.close()

        conexao = createConnectionCaixa("localhost", "caixa", "caixa", "xe")
        dados = pegaUltimaVenda(conexao,1)    
        cupomVenda= dados[1]

        if str(ultimo) != str(cupomVenda):
            print("Diferente")
            file = open("C:\\SORTEIODIGITAL\\config\\ultimoCupom.txt", 'w', encoding='ANSI')
            file.write(str(cupomVenda))
            file.close()
            
        else:
            print("Igual")


if __name__ == '__main__':
    os.environ["PATH"] = r"C:\\SORTEIODIGITAL\\instantclient_18_5;" + os.environ["PATH"]
    # cx_Oracle.init_oracle_client(lib_dir=r"C:\\SORTEIODIGITAL\\instantclient_18_5")
    
    data_cupom = Funcoes.dataFormatada()
    lista = readConfig()

    linhas_inicio = 0

    host = lista[0]
    user = lista[1]
    password = lista[2]
    database = lista[3]
    impressora = lista[4]
    img = lista[5]
    valor_cupom = lista[6]
    codfilial = lista[7]
    fornecs = lista[9]
    print(lista)
    rateio = lista[10]
    prods = lista[11]

    win32print.SetDefaultPrinter(impressora)
    
    conexao = createConnectionCaixa(host, user, password, database)
    #conexao = createConnection2()

    dadosEmpresa = pegaDadosFilial(conexao,codfilial)

    razao = dadosEmpresa[0]
    cnpj = dadosEmpresa[1]
    endereco = dadosEmpresa[2]
    fone = dadosEmpresa[3]

    while True:
        try:
            dados = pegaUltimaVenda(conexao,valor_cupom)

            if dados != None:
              
                linhas_result = qtdLinhas(conexao)

                if linhas_result > linhas_inicio:
                    
                    
                    data = dados[0]
                    numpedecf = dados[1]
                    numcupom = dados[4]
                    numcaixa = dados[2]
                    vltotal = dados[5]
                    protocolo = dados[3]

                    file = open("C:\\SORTEIODIGITAL\\config\\ultimoCupom.txt", 'r', encoding='ANSI')
                    cupom = file.readlines()
                    valorTxt = cupom[0]
                    file.close()
                    print(valorTxt)
                    print(numcupom)
                    print(str(valorTxt) != str(numcupom))
                    if str(valorTxt) != str(numcupom):
                        print('IMPRIMINDO O CUPOM')
                        file = open("C:\\SORTEIODIGITAL\\config\\ultimoCupom.txt", 'w', encoding='ANSI')
                        file.write(str(numcupom))
                        file.close()
                        print('readconfig8')

                        if str(readConfig()[8]) == 'S':
                            print('')
                            print(dados[6])
                            cuponsFornec = adicionarFonecs(numpedecf,conexao)
                            if dados[6] is not None:
                                qtdCupons = dados[6]
                            else:
                                qtdCupons = int(vltotal/int(valor_cupom))
                            
                            if int(cuponsFornec) > 0:
                                qtdCupons = qtdCupons + qtdCupons
                        else:
                            
                            qtdCupons = int(vltotal/int(valor_cupom))
                            

                        listaCupons = insereParticipacao(conexao, data, numcupom, numcaixa, protocolo, vltotal, qtdCupons)
                        print(listaCupons)
                        for i in listaCupons:
                            print(i)
                            criar_cupom(i,i,razao,cnpj,endereco,fone)
                            #gera_pdf(i,img, i, razao, cnpj, endereco, fone)
                            os.startfile("C:\\SORTEIODIGITAL\\cupons\\Cupom_{}.txt".format(i), "print")
                            linhas_inicio = linhas_result
                    else:
                        print("Não existe uma nova venda")
                else:
                    print("Não existe uma nova venda")
            else:
                print("Não tem nenhuna venda")
            sleep(2)
        except Exception as f:
            traceback.print_exc()
            print("Erro while\n{}".format(f))

    

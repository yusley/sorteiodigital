from datetime import date, datetime
import os

def dataFormatada():
    """Retorna a data do dia atual no formato DD/MM/YYYY"""
    hoje = datetime.today()
    dt = str(hoje).split(" ")[0].split("-")
    dia = dt[2]
    mes = dt[1]
    ano = dt[0]
    
    return "{}/{}/{}".format(dia, mes, ano)

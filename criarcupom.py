

def ler_Filial():
    arquivo =  open(r"C:\Users\yusley\Documents\SORTEIODIGITAL-OK-20220411T130042Z-001\SORTEIODIGITAL-OK\config\FILIAL.txt",'r+')
    percorrer = arquivo.readlines()
    print(percorrer)
    razao = percorrer[0].split(':')[1]
    razao = razao.replace('\n','')
    cnpj = percorrer[1].split(':')[1]
    cnpj = cnpj.replace('\n','')
    end = percorrer[2].split(':')[1]
    end = end.replace('\n','')
    cont = percorrer[3].split(':')[1]
    cont = cont.replace('\n','')

    lista = []
    lista.append(razao)
    lista.append(cnpj)
    lista.append(end)
    lista.append(cont)

    return lista

def criar_cupom(nome,numcupom,razao, cnpj, endereco, fone):

    path = f"C:\\SORTEIODIGITAL\\cupons\\"

    arquivo = open(path+'Cupom_'+str(nome)+'.txt','w+')
    
    arquivo.writelines('RAZÃO :'+str(razao)+'\n')
    arquivo.writelines('CNPJ : '+str(cnpj)+'\n')
    arquivo.writelines('END : '+str(endereco)+'\n')
    arquivo.writelines('CONTATO : '+str(fone)+'\n\n')
    arquivo.writelines('***CUPOM PROMOCIONAL***'+'\n\n')
    arquivo.writelines('ANIVERSÁRIO DE 3 ANOS ATACAMIX ' +'\n')
    arquivo.writelines('CAMPANHA DE PRÊMIOS PROMOVIDA PELO ATACAMIX COMERCIO ATACADISTA E VAREJISTA DE ALIMENTOS LTDA. '+'\n')
    arquivo.writelines('PERÍODO: 22/01/2025 A 30/04/2025' +'\n\n')
    arquivo.writelines('PRÊMIOS:' +'\n')
    arquivo.writelines('1 FIAT MOBI LIKE 1.0 2025' +'\n')
    arquivo.writelines('3 POP 110i ES 2025' +'\n')
    arquivo.writelines('1 CAMINHÃO DE PREMIOS' +'\n')
    arquivo.writelines('50 VALE DE COMPRAS R$500,00' +'\n\n')
    arquivo.writelines('PARA PARTICIPAR, É OBRIGATÓRIO SEGUIR NOSSO INSTAGRAM: @ATACAMIXOFICAL.' +'\n\n')
    arquivo.writelines('A CADA R$ 100,00 EM COMPRAS NO ATACAMIX DURANTE O PERÍODO DA CAMPANHA,\nO CONSUMIDOR TEM DIREITO A RECEBER UM CUPOM PARA CONCORRER AOS SORTEIOS.' +'\n\n')
    arquivo.writelines('CONSULTE O REGULAMENTO COMPLETO NO SITE.'+'\n\n')
    arquivo.writelines('QUAL O MELHOR ATACAREJO DA REGIÃO?\n\nRESPOSTA : _______________________' +'\n\n')
    arquivo.writelines("Cupom : "+str(numcupom)+"\n\n")
    arquivo.writelines("Nome :     ____________________________________\n\n")
    arquivo.writelines("CPF :      ____________________________________\n\n")
    arquivo.writelines("Endereço : ____________________________________\n\n")
    arquivo.writelines("Telefone : ____________________________________\n\n")

    arquivo.close()



-- Cria a sequência idcupom
create sequence seq_idcupom 
start with 1
increment by 1

-- Cria a tabela para gravar os cupons entregues
CREATE TABLE sorteiodigital (
	
	idcupom number(6,2),
	dtvenda DATE,
	numcupomvenda number(7,0),
	numcaixa number(3,0),
	protocolonfce varchar2(50),
	vltotal number(7,2),
)

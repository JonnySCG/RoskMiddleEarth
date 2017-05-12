import socket
import os
from urlparse import urlparse
from urlparse import parse_qs
from classiServah import Partita
from classiServah import Giocatore
import utilities as u


t="",2471 #80

sok=socket.socket(socket.AF_INET , socket.SOCK_STREAM)
sok.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR,1)
sok.bind(t)
sok.listen(1)

print("forza roma")

p=Partita(2)

while True:
	p.soCKET,p.cliente=sok.accept()
	p.request=p.soCKET.recv(1024)
	p.path=u.estrapola(u.estrapola(p.request,"\r\n",0)," ",1)
	p.up=urlparse(p.path)
	p.query=parse_qs(p.up.query)

	def DummyFunction():
		u.response("I am a Teapot","418 OK")

	switch={
	0: p.analizzaPrimaRequest ,
	0.1: p.attesaAltriPlayers ,
	0.2: p.analizzaRichiesteOK ,
	1.1: p.confermePrepartita ,
	1.5: p.disArmy ,
	2: p.inizioPartita ,
	2.1:
	

	}
	
	switch[p.STATO]()

	print(p.STATO, p.numP)
	print(p.cliente,p.listaIP)
	#print(query)
	p.soCKET.close()
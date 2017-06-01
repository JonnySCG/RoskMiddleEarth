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
	2.1: p.incassareArmate ,
	2.15:p.distribuzioneArmateDuranteIlTurno ,
	2.2: p.vuoiCombattere ,
	2.21:p.dimmiDestinazione ,
	2.22:p.conQuanteArmate ,
	2.23:DummyFunction ,
	2.3: DummyFunction
	
	}
	
	switch[p.STATO]()
	
	p.soCKET.close()
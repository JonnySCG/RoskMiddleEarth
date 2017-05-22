import utilities as u

import json

class Partita():

	"""Partita: oggetto che rappresenta il gioco vero e proprio"""
	def __init__(self,numPmax):

		self.numPmax=numPmax
		self.STATO=0
		self.giocatori=[] #lista di oggetti del tipo Giocatore
		self.numP=0
		self.listaIP=[]

		self.colori=["blu","rosso","giallo","nero","verde","viola"]
		self.obiettivi=[]
		self.carteTerritori=[]
		self.carteTerritoriFisse=self.carteTerritori

		self.giocatoreDelTurno=None

	def aggiungiP(self,player):

		self.numP+=1
		self.giocatori.append(player)

	def rispostina(self):
		self.soCKET.sendall(u.responseHTTP("Partita non disponibile","200 OK"))

	def response(self, risposta, codice="200 OK"):
		self.soCKET.sendall(u.responseHTTP(risposta,codice))

	def DistribuzioneRoba(self,Lista,listina1,listina2,listina3=None,listina4=None,listina5=None,listina6=None,totale=False):

		a=Lista
		from random import shuffle
		shuffle(a)

		if totale==True:

			if numPmax==2:
				lista=[listina1,listina2]

			elif numPmax==3:
				lista=[listina1,listina2,listina3]

			elif numPmax==4:
				lista=[listina1,listina2,listina3,listina4]

			elif numPmax==5:
				lista=[listina1,listina2,listina3,listina4,listina5]

			elif numPmax==6:
				lista=[listina1,listina2,listina3,listina4,listina5,listina6]

			else:
				self.response("Parametri partita sballati")

			for i,val in enumerate(a):
				lista[i%self.numPmax].append(val)

		else:

			listina1=a[0]
			listina2=a[4]

			if numPmax>=3:
				listina3=a[5]

				if numPmax>=4:
					listina4=a[2]

					if numPmax>=5:
						listina5=a[3]

						if numPmax==6:
							listina6=a[1]

	def controllaRequest(self):

		if self.cliente[0] in self.giocatori and self.query:

			self.response("Azione non disponibile.")


#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000


	def analizzaPrimaRequest(self):

		if not self.query:

			if self.numP==0:
				player=Giocatore(1,self.cliente) #creazione giocatore
				permesso=self.aggiungiP(player)
				self.soCKET.sendall(u.responseHTTP("benvenuto nella partita, in attesa di altri giocatori","200 OK"))
				u.debug("sto cambiando stato",4)
				self.giocatoreDelTurno=self.giocatori[0]
				self.STATO=0.1
				
		else:
		 	self.soCKET.sendall(u.responseHTTP(None,"404 NOTFOUND"))

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

	def attesaAltriPlayers(self):
		
		self.listaIP=[a.IP for a in self.giocatori]
		
		if not self.query:

			if self.cliente[0] not in self.listaIP:

				player=Giocatore(self.numP,self.cliente)
				self.listaIP.append(player.IP)
				permesso=self.aggiungiP(player)
				
				if self.numP==self.numPmax:
	 				self.soCKET.sendall(u.responseHTTP("Numero giocatori raggiunto. Confermare di voler iniziare la partita","200 OK"))	
	 				self.STATO=0.2

	 			else:
	 				self.soCKET.sendall(u.responseHTTP("benvenuto nella partita, in attesa di altri giocatori","200 OK"))

	 		else:
	 			self.soCKET.sendall(u.responseHTTP("Sei gia entrato nella lista dei giocatori della partita. In attesa di altri giocatori.","200 OK"))

	 	else:

	 		if self.cliente[0] in self.listaIP:

	 			if self.query["attesa"]==["1"]:
	 				
	 					self.soCKET.sendall(u.responseHTTP("benvenuto nella partita, in attesa di altri giocatori","200 OK"))
	 			
	 		
	 		else:

	 			self.soCKET.sendall(u.responseHTTP(None,"404 NOTFOUND"))

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

	def analizzaRichiesteOK(self):

		#distribuzione territori
		self.DistribuzioneRoba(self.carteTerritori, self.giocatori[0].territori, self.giocatori[1].territori,True)
		
		#distribuzione obiettivo
		self.DistribuzioneRoba(self.obiettivi, self.giocatori[0].obiettivoGiocatore , self.giocatori[1].obiettivoGiocatore , False)

		#distribuzione colore
		self.DistribuzioneRoba(self.colori, self.giocatori[0].colore , self.giocatori[1].colore , False)		


		u.debug("sto analizzando richieste",4)

		if self.cliente[0] in self.listaIP:

			player=None

			for g in self.giocatori:
				
				if g.IP==self.cliente[0]:

					player=g

			u.debug("sto verificando il cliente nella listaIP",4)
			print(self.query)

			if "conferma" in self.query and self.query["conferma"]==["OK"]:

				u.debug("sto analizzando la conferma",4)

				player.conferma=True

				if self.verificaOK()==True:

					self.response("Benvenuto nella Terra di Mezzo. Il tuo colore e il {}".format(player.colore))
					

					self.STATO=1.1

				else:

					self.soCKET.sendall(u.responseHTTP("Aspettare la conferma degli altri giocatori.","200 OK"))
					
			elif "attesa" in self.query:

				if self.query["attesa"]==["1"]:

	 				self.soCKET.sendall(u.responseHTTP("Numero giocatori raggiunto. Confermare di voler iniziare la partita","200 OK"))

	 			elif self.query["attesa"]==["2"]:

	 				self.response("Attendere la conferma degli altri giocatori")

	 			else:

					if player.conferma==True:

						self.soCKET.sendall(u.responseHTTP("Azione non disponibile. Aspettare la conferma degli altri giocatori.","200 OK"))

					else:

						self.soCKET.sendall(u.responseHTTP("Azione non disponibile. Inviare la conferma.","200 OK"))


			else:

				if player.conferma==True:

						self.soCKET.sendall(u.responseHTTP("Azione non disponibile. Aspettare la conferma degli altri giocatori.","200 OK"))

				else:

						self.soCKET.sendall(u.responseHTTP("Azione non disponibile. Inviare la conferma.","200 OK"))

		else:
			self.rispostina()


	def verificaOK(self):

		var=True

		for g in self.giocatori:

			if g.conferma==False:

				var=False
				
				break		

		return var

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

	def confermePrepartita(self):

		if self.cliente[0] in self.listaIP:

			player=None

			for g in self.giocatori:
				
				if g.IP==self.cliente[0]:

					player=g

			if self.query:
				
				if "conferma" in self.query and self.query["conferma"]==["OK"]:

					if player.colorSelect==True:

						if player.obiettivoDist==True:

							if player.disTerritori==True:

								self.response("Azione non disponibile.")
								self.response("In attesa degli altri giocatori.")

							else:

								player.disTerritori=True

								if verificaDisTerritori()==True:

									self.STATO=1.5
									self.response("Distribuisci le armate sui tuoi territori.")

								else:

									self.response("In attesa degli altri giocatori.")

						else:

							player.obiettivoDist=True

					else:

						player.colorSelect=True

				elif "attesa" in self.query:

					if self.query["attesa"]==["2"]:

						self.response("Benvenuto nella Terra di Mezzo")
						self.response("Il tuo colore e il {}".format(player.colore))

					elif self.query["attesa"]==["3"]:

						self.response("Attendere gli altri giocatori")

					else:

						self.response("Azione non disponibile")

				else:

					self.response("Azione non disponibile")

			else:

				self.response("Azione non disponibile")

		else:

			self.rispostina()



	def verificaDisTerritori(self):

		var=True

		for g in self.giocatori:

			if g.disTerritori==False:

				var=False
				
				break		

		return var

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

	def disArmy(self):

		if self.passaAllaPartita()==True:

			self.STATO=2

		#distribuzione armate sui territori

		if self.cliente[0] in self.listaIP:

			if self.query:

				if "aggiorna" in self.query and self.query["aggiorna"]==["1"]:

					self.response()#TODO

				else:

					if player.finitoDisArmy==True:

						if "ritorna" in self.query and self.query["ritorna"]==[1]:

							player.finitoDisArmy=False
							self.response("Puoi ricominciare a distribuire le tue armate")

						elif "aggiornami" in self.query and self.query["aggiornami"]==["1"]:

							pass
							#TODO rispondi qualcosa

						else:

							self.response("Azione non disponibile, attendere gli altri giocatori")

					else:

						if player.NumArmy==0:

							if "finito" in self.query and self.query["finito"]==["true"]:

								player.finitoDisArmy=True
								self.response("Attendere gli altri giocatori")

							elif "azione" in self.query and "territorio" in self.query and self.query["azione"]==["remove"] and self.query["territorio"] in player.nomiTerritori:

								territorio=None

								for g in player.territori:
									if g.nomeT==self.query["territorio"]:
										territorio=g

								territorio.numArmyT=territorio.numArmyT-1
								player.NumArmy=player.NumArmy+1
								self.response(self.tutto)

							else:

								self.response("Azione non disponibile")

						else:

							if "azione" in self.query and "territorio" in self.query and self.query["territorio"] in player.nomiTerritori:

								territorio=None

								for g in player.territori:
									if g.nomeT==self.query["territorio"]:
										territorio=g

								if self.query["azione"]==["add"]:

									territorio.numArmyT=territorio.numArmyT+1
									self.response(self.tutto)
									player.NumArmy=player.NumArmy-1

								elif self.query["azione"]==["remove"]:

									territorio.numArmyT=territorio.numArmyT-1
									self.response(self.tutto)
									player.NumArmy=player.NumArmy+1

								else:

									self.response("Azione non disponibile")

							elif "attesa" in self.query and self.query["attesa"]==["3"]:

								self.response("Distribuisci le armate sui tuoi territori.")

							else:

								self.response("Azione non disponibile")
			else:

				self.response("Azione non disponibile")

		else:

			self.rispostina()


	def passaAllaPartita(self):

		var=True

		for g in self.giocatori:

			if g.finitoDisArmy==False:

				var=False
				
				break		

		return var

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def incassareArmate(self):

		self.controllaRequest()

		if self.cliente[0] == giocatoreDelTurno.IP:

			if "aggiornami" in self.query and self.query["aggiornami"]==["1"]:
				
				self.response("E' il tuo turno")

			elif "carta1" in self.query and "carta2" in self.query and "carta3" in self.query:

				codiciQuery=[]

				codiciQuery.append(self.query["carta1"])
				codiciQuery.append(self.query["carta2"])
				codiciQuery.append(self.query["carta3"])

				self.ArmyDaCarte(self.estrapolaCarte(codiciQuery))

				x=len(self.giocatoreDelTurno.territori)/3
				y=0

				if x<=3: y=0
				elif x>=4 and x<=9: y=1
				elif x>=10 and x<=15: y=2
				elif x=16: y=3
				else: self.response("Azione non disponibile")

				self.giocatoreDelTurno.NumArmy+=(x+y)

				self.response("Combinazione analizzata: {} armate da distribuire" .format(self.giocatoreDelTurno.NumArmy))

			elif "fine2.1" in self.query and self.query["fine2.1"]==["OK"]:
				
				self.STATO=2.2

			else:
				self.response("Azione non disponibile")
		else:
			self.response("Azione non disponibile")


##0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

	def estrapolaCarte(self,codici):

		codiciGenerali=[]
		carteDaRitornare=[]
		combinazioneBuona=True

		for x in self.giocatoreDelTurno.carteCombinazioni:

			codiciGenerali.append(x.code)

		for x in codici:

			if x not in codiciGenerali:

				return False

		for ogniCarta in self.giocatoreDelTurno.carteCombinazioni:

			if ogniCarta.code in codici:

				carteDaRitornare.append(ogniCarta)

		return carteDaRitornare

	def ArmyDaCarte(self,carteCombo):

		c1=carteCombo[0].figura
		c2=carteCombo[1].figura
		c3=carteCombo[2].figura

		if c1==c2 and c1==c3:

			if c1=="troll":

				self.giocatoreDelTurno.NumArmy+=8

				if c1.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			elif c1=="balrog":

				self.giocatoreDelTurno.NumArmy+=10

				if c1.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			elif c1=="drago":

				self.giocatoreDelTurno.NumArmy+=12

				if c1.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			else:

				self.response("Azione non disponibile")

		elif c1!=c2 and c1!=c3 and c2!=c3:

			self.giocatoreDelTurno.NumArmy+=14

			if c1.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			if c2.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			if c3.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

		elif c1 =="jolly" or c2=="jolly" or c3=="jolly":

			if c1 =="jolly" and c2==c3:

				self.giocatoreDelTurno.NumArmy+=15

				if c1.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			elif c2 =="jolly" and c1==c3:

				self.giocatoreDelTurno.NumArmy+=15

				if c1.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			elif c3 =="jolly" and c2==c1:			

				self.giocatoreDelTurno.NumArmy+=15

				if c1.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			else:

				self.response("Combinazione non valida")

		else:

			self.response("Combinazione non valida")




class Giocatore(object):

	def __init__(self,ordine,socket):
	
		self.ordine=ordine
		self.socket=socket
		self.IP=self.socket[0]
		self.colore=""
		self.obiettivoGiocatore=None
		self.conferma=False
		self.colorSelect=False
		self.obiettivoDist=False
		self.disTerritori=False
		self.NumArmy=0
		self.finitoDisArmy=False
		self.territori=[]
		self.carteCombinazioni=[]
		self.eliminato=False

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

class Territorio(object):
	"""docstring for Territorio"""

	def __init__(self,json):
		self.nomeT=nome
		self.numArmyT=0
		self.codiceTerritorio=""
		self.continente=""
		self.proprietarioT=None
		self.coloreTerritorio=colore

class Carta(object):
	"""docstring for Carta"""
	def __init__(self,json):

		self.figura=figura
		self.code=""
		self.codiceTerritorio=""
		self.continente=nomeContinente
		self.proprietario=None
		self.armateExtra=False

		for x in self.proprietario.territori:
			
			if x.code == self.code:

				self.armateExtra=True




class CartaObiettivo(object):
	"""docstring for Obiettivi"""
	def __init__(self,json):
		self.stringa=json["obiettivi"]["stringa"]
		self.proprietario=None
		self.ID=json["obiettivi"]["ID"]
		self.obCompletato=False

		if json["obiettivi"]["ID"]=="ob24" and len(self.proprietario.territori)>=24:
			
			self.obCompletato=True

		elif json["obiettivi"]["ID"]=="ob18" and len(self.proprietario.territori)>=18:

			arrayno=[]

			for x in self.proprietario.territori:

				if x.numArmyT<2:

					arrayno.append(x)

			if len(arrayno)==0

				self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obT1":

			c1="Beleriand"
			c2="Nord Endor"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==14:

				self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obT2":

			c1="Sud Aman"
			c2="Nord Endor"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==14:

				self.obCompletato=True	

		elif json["obiettivi"]["ID"]=="obT3":

			c1="Sud Aman"
			c2="Nord Aman"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==15:

				self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obT4":

			c1="Beleriand"
			c2="Sud Aman"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==18:

				self.obCompletato=True	

		elif json["obiettivi"]["ID"]=="obT5":

			c1="Beleriand"
			c2="Endor Orientale"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==19:

				self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obT6":

			c1="Sud Endor"
			c2="Endor Orientale"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==20:

				self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obA1":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "rosso":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				playerDaSconfiggere.eliminato==True:

					self.obCompletato=True

			else:

				if len(self.proprietario.territori)>=24:
			
					self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obA2":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "giallo":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				playerDaSconfiggere.eliminato==True:

					self.obCompletato=True

			else:

				if len(self.proprietario.territori)>=24:
			
					self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obA3":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "blu":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				playerDaSconfiggere.eliminato==True:

					self.obCompletato=True

			else:

				if len(self.proprietario.territori)>=24:
			
					self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obA4":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "verde":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				playerDaSconfiggere.eliminato==True:

					self.obCompletato=True

			else:

				if len(self.proprietario.territori)>=24:
			
					self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obA5":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "nero":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				playerDaSconfiggere.eliminato==True:

					self.obCompletato=True

			else:

				if len(self.proprietario.territori)>=24:
			
					self.obCompletato=True

		elif json["obiettivi"]["ID"]=="obA6":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "viola":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				playerDaSconfiggere.eliminato==True:

					self.obCompletato=True

			else:

				if len(self.proprietario.territori)>=24:
			
					self.obCompletato=True

			


if __name__=="__main__":

	with open('json.json') as data_file:    

		data = json.load(data_file)

		a= u.parser(CartaObiettivo,data["obiettivi"])
		b= u.parser(Carta,data["carte"])
		c= u.parser(Territorio,data["territori"])



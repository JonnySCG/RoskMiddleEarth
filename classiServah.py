import utilities as u

class Partita():

	"""Partita: oggetto che rappresenta il gioco vero e proprio"""
	def __init__(self,numPmax):
		self.numPmax=numPmax
		self.STATO=0
		self.numP=0
		self.giocatori=[] #lista di oggetti del tipo Giocatore
		self.listaIP=[]

		self.giocatoreDelTurno=None

		self.tutto=[]

	def aggiungiP(self,player):

		self.numP+=1
		self.giocatori.append(player)
		u.debug("sto aggiungendo giocatori",5)

	def rispostina(self):
		self.soCKET.sendall(u.responseHTTP("Partita non disponibile","200 OK"))

	def response(self, risposta, codice="200 OK"):
		self.soCKET.sendall(u.responseHTTP(risposta,codice))

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

	 		if cliente[0] in listaIP:

	 			if self.query["attesa"]==["1"]:
	 				
	 					self.soCKET.sendall(u.responseHTTP("benvenuto nella partita, in attesa di altri giocatori","200 OK"))
	 			
	 		
	 		else:

	 			self.soCKET.sendall(u.responseHTTP(None,"404 NOTFOUND"))

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

	def analizzaRichiesteOK(self):

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

				if self.verificaOK()==True:

					self.response("Benvenuto nella Terra di Mezzo")
					self.response("Il tuo colore e il {}".format(player.colore))
					
					self.STATO=1.1

				else:

					self.soCKET.sendall(u.responseHTTP("Aspettare la conferma degli altri giocatori.","200 OK"))

			elif "attesa" in self.query:

				if self.query["attesa"]==["1"]:

	 				self.soCKET.sendall(u.responseHTTP("Numero giocatori raggiunto. Confermare di voler iniziare la partita","200 OK"))

	 			elif self.query["attesa"]==["2"]:

	 				pass
	 				#TODO rispondi qualcosa

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

			print(g.conferma)

			if g.conferma==False:

				var=False
				
				break		

		return var

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

	def confermePrepartita(self):

		if cliente[0] in listaIP:

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

						pass
						#TODO rispondi qualcosa

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

		if cliente[0] in listaIP:

			if self.query:

				if "aggiorna" in self.query and self.query["aggiorna"]==["1"]:

					self.response(self.tutto)

				else:

					if player.finitoDisArmy==True:

						if "ritorna" in self.query and self.query["ritorna"]==[1]:

							player.finitoDisArmy=False
							self.response("Puoi ricominciare a distribuire le tue armate")

						elif "attesa" in self.query and self.query["attesa"]==["4"]:

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

def TurnoGiocatore(self,player):

	self.player=player
	
	if "attesa" in self.query and self.query["attesa"]==["4"]:

		self.response("Inizio della partita.")


##0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

class Giocatore(object):

	def __init__(self,ordine,socket):
	
		self.ordine=ordine
		self.socket=socket
		self.IP=self.socket[0]
		self.colore=""
		self.conferma=False
		self.colorSelect=False
		self.obiettivoDist=False
		self.disTerritori=False
		self.NumArmy=0
		self.finitoDisArmy=False
		self.territori=[]
		self.nomiTerritori=[territori.nomeT]

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

class Territorio(object):
	"""docstring for Territorio"""

	def __init__(self):
		self.nomeT=""
		self.carta=None
		self.numArmyT=0
		self.proprietarioT=None
		self.proprietarioC=None
		self.armateExtra=False

		if self.proprietarioC==self.proprietarioT:
			self.armateExtra=True

#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000
#0000000000000000000000000000000000000000000000000000000000000000000000000

class Carta(object):
	"""docstring for Carta"""
	def __init__(self, figura, Territorio, nomeContinente):

		self.figura=figura
		self.territorioC=Territorio.nomeT
		self.continente=nomeContinente
		self.proprietario=Territorio.proprietarioC


				
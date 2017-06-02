import utilities as u
import json
from oggettiRisiko import Giocatore
from oggettiRisiko import Territorio
from oggettiRisiko import CartaObiettivo
from oggettiRisiko import Carta
from random import randint

class Partita(object):

	def __init__(self,numPmax):

		self.obiettivi=[]
		self.carte=[]
		self.territoriGenerali=[]
		self.territoriFissi=[]


		with open('json.json') as data_file:

			data = json.load(data_file)

			self.obiettivi=u.parser(CartaObiettivo,data["obiettivi"],self)
			self.territoriGenerali=u.parser(Territorio,data["territori"],self)
			self.territoriFissi=self.territoriGenerali[:]
			self.carte=u.parser(Carta,data["carte"],self)

		self.numPmax=numPmax
		self.STATO=0
		self.numP=0
		self.giocatori=[]
		self.listaIP=[]

		self.colori=["blu","rosso","giallo","nero","verde","viola"]

		self.giocatoreDelTurno=None

	def aggiungiP(self,player):

		self.numP+=1
		self.giocatori.append(player)

	def rispostina(self):

		self.soCKET.sendall(u.responseHTTP("Partita non disponibile","200 OK"))

	def response(self, risposta, codice="200 OK"):

		self.soCKET.sendall(u.responseHTTP(risposta,codice))

	def DistribuzioneTerritori(self,Listona):

		#Listona contains all the objects (like Territori, colori, ecc)
		a=Listona
		from random import shuffle
		shuffle(a)

		#Let's create a container where we will put the list of each player
		lista=[]

		#Shall we distribute all the compoenents of Listona, or only one for each player?
		if totale==True:

			if numPmax==2:

				listina1=self.giocatori[0].territori
				listina2=self.giocatori[1].territori

				lista=[listina1,listina2]

			elif numPmax==3:

				listina1=self.giocatori[0].territori
				listina2=self.giocatori[1].territori
				listina3=self.giocatori[2].territori

				lista=[listina1,listina2,listina3]

			elif numPmax==4:

				listina1=self.giocatori[0].territori
				listina2=self.giocatori[1].territori
				listina3=self.giocatori[2].territori
				listina4=self.giocatori[3].territori

				lista=[listina1,listina2,listina3,listina4]

			elif numPmax==5:

				listina1=self.giocatori[0].territori
				listina2=self.giocatori[1].territori
				listina3=self.giocatori[2].territori
				listina4=self.giocatori[3].territori
				listina5=self.giocatori[4].territori

				lista=[listina1,listina2,listina3,listina4,listina5]

			elif numPmax==6:

				listina1=self.giocatori[0].territori
				listina2=self.giocatori[1].territori
				listina3=self.giocatori[2].territori
				listina4=self.giocatori[3].territori
				listina5=self.giocatori[4].territori
				listina6=self.giocatori[5].territori

				lista=[listina1,listina2,listina3,listina4,listina5,listina6]

			else:
				self.response("Parametri partita sballati")

			#distribution magic !!! <<< --- QUI
			for i,val in enumerate(a):
				lista[i%self.numPmax].append(val)

	def DistribuzioneRoba(Listona):
		
		a=Listona

		if a==self.obiettivi:

			self.giocatori[0].obiettivoGiocatore=a[0]
			self.giocatori[1].obiettivoGiocatore=a[4]

			if numPmax>=3:
				self.giocatori[2].obiettivoGiocatore=a[5]

				if numPmax>=4:
					self.giocatori[3].obiettivoGiocatore=a[2]

					if numPmax>=5:
						self.giocatori[4].obiettivoGiocatore=a[3]

						if numPmax==6:
							self.giocatori[5].obiettivoGiocatore=a[1]


		elif a==self.colori:

			self.giocatori[0].colore=a[0]
			self.giocatori[1].colore=a[4]

			if numPmax>=3:
				self.giocatori[2].colore=a[5]

				if numPmax>=4:
					self.giocatori[3].colore=a[2]

					if numPmax>=5:
						self.giocatori[4].colore=a[3]

						if numPmax==6:
							self.giocatori[5].colore=a[1]

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 0      OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

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

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 0.1    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

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

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 0.2    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def analizzaRichiesteOK(self):

		#distribuzione territori
		self.DistribuzioneTerritori()
		
		#distribuzione obiettivo
		self.DistribuzioneRoba(self.obiettivi)

		#distribuzione colore
		self.DistribuzioneRoba(self.colori)		

		for x in self.territoriGenerali:

			x.addTConfinanti()

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

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 1.1    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def confermePrepartita(self):

		if self.cliente[0] in self.listaIP:

			player=None

			for g in self.giocatori:
				
				if g.IP==self.cliente[0]:

					player=g

			if self.query:
				
				if "conferma" in self.query and self.query["conferma"]==["OK"]:

					if verificaDisTerritori()==True:
						
						self.STATO=1.5
						self.response("Distribuisci le armate sui tuoi territori.")

					else:

						self.response("In attesa degli altri giocatori.")


				elif "attesa" in self.query:

					if self.query["attesa"]==["2"]:

						#TODO Inviare tuttos
						self.response("")

					elif self.query["attesa"]==["3"]:

						self.response("In attesa degli altri giocatori.")

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

			if g.conferma2==False:

				var=False
				
				break		

		return var

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 1.5    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def disArmy(self):

		#distribuzione armate sui territori

		if self.cliente[0] in self.listaIP:

			player=None

			for x in self.giocatori:
				
				if x.IP == self.cliente[0]:
					
					player=x

			if self.query:

				if "aggiorna" in self.query and self.query["aggiorna"]==["1"]:

					self.response("")#TODO

				else:

					if player.finitoDisArmy==True:

						if "ritorna" in self.query and self.query["ritorna"]==[1]:

							player.finitoDisArmy=False
							self.response("Puoi ricominciare a distribuire le tue armate")

						elif "aggiornami" in self.query and self.query["aggiornami"]==["1"]:

							self.response("")
							#TODO rispondi tuttos


						elif "attesa" in self.query and self.query["attesa"]==["4"]:

							self.response("Attendere gli altri giocatori")

						else:

							self.response("Azione non disponibile, attendere gli altri giocatori")

					else:

						if player.NumArmy==0:

							if "finito" in self.query and self.query["finito"]==["true"]:

								player.finitoDisArmy=True

								if self.passaAllaPartita()==True:

									self.STATO=2.1
									self.response("Le armate sono distribuite: BUONA PARTITA!")

								else:

									self.response("Attendere gli altri giocatori")

							elif "azione" in self.query and "territorio" in self.query and self.query["azione"]==["remove"] and self.query["territorio"]:									

								for g in self.territoriFissi:
									
									if g.code==self.query["territorio"]:
										territorio=g

								if territorio in player.territori:

									if territorio.numArmyT>=2:

										territorio.numArmyT=territorio.numArmyT-1
										player.NumArmy=player.NumArmy+1
										self.response(self.tutto)

									else:

										self.response("Azione non disponibile.")

								else:

									self.response("Azione non disponibile.")

							else:

								self.response("Azione non disponibile")

						else:

							if "azione" in self.query and "territorio" in self.query and self.query["territorio"]:

								territorio=None

								for g in self.territoriFissi:
									if g.nomeT==self.query["territorio"]:
										territorio=g

								if territorio in player.territori:
									
									if self.query["azione"]==["add"]:

										territorio.numArmyT=territorio.numArmyT+1
										self.response(self.tutto)
										player.NumArmy=player.NumArmy-1

									elif self.query["azione"]==["remove"]:

										if territorio.numArmyT>=2:

											territorio.numArmyT=territorio.numArmyT-1
											self.response(self.tutto)
											player.NumArmy=player.NumArmy+1

										else:

											self.response("Azione non disponibile.")

									else:

										self.response("Azione non disponibile")

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
#  STATO 2.1    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def incassareArmate(self):

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
				
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
					elif x==16: y=3
					else: self.response("Azione non disponibile")

					arrayno1=[]
					arrayno2=[]
					arrayno3=[]
					arrayno4=[]
					arrayno5=[]
					arrayno6=[]

					for x in self.giocatoreDelTurno.territori:
					
						if x.continente =="Beleriand":

							arrayno1.append(x)

						if x.continente =="Endor Orientale":

							arrayno2.append(x)

						if x.continente =="Nord Aman":

							arrayno3.append(x)

						if x.continente =="Nord Endor":

							arrayno4.append(x)

						if x.continente =="Sud Aman":

							arrayno5.append(x)

						if x.continente =="Sud Endor":

							arrayno6.append(x)

					if len(arrayno1)==9:
					
						self.giocatoreDelTurno.NumArmy+=6

					if len(arrayno2)==10:
					
						self.giocatoreDelTurno.NumArmy+=8

					if len(arrayno3)==6:
					
						self.giocatoreDelTurno.NumArmy+=4

					if len(arrayno4)==5:
					
						self.giocatoreDelTurno.NumArmy+=3

					if len(arrayno5)==9:
					
						self.giocatoreDelTurno.NumArmy+=5

					if len(arrayno6)==10:
					
						self.giocatoreDelTurno.NumArmy+=7


					self.giocatoreDelTurno.NumArmy+=(x+y)

					self.response("Combinazione analizzata: {} armate da distribuire" .format(self.giocatoreDelTurno.NumArmy))
					self.STATO=2.15

				elif "DistLeArmy" in self.query and self.query["DistLeArmy"]==["OK"]:

					x=len(self.giocatoreDelTurno.territori)/3
					y=0

					if x<=3: y=0
					elif x>=4 and x<=9: y=1
					elif x>=10 and x<=15: y=2
					elif x==16: y=3

					self.giocatoreDelTurno.NumArmy+=(x+y)

					self.STATO=2.15
					self.response("Distribuisci le armate guadagnate:{} armate da distribuire" .format(self.giocatoreDelTurno.NumArmy))

				else:
					self.response("Azione non disponibile")
		
			else:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
					
					self.response("E' il turno di {}. Ti faremo sapere se e quando attacchera' un tuo territorio.".format(self.giocatoreDelTurno))
				else:

					self.response("Azione non disponibile")		
		
		else:
			self.rispostina()

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

		c1x=carteCombo[0]
		c2x=carteCombo[1]
		c3x=carteCombo[2]

		if c1==c2 and c1==c3:

			if c1=="troll":

				self.giocatoreDelTurno.NumArmy+=8

				if c1x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			elif c1=="balrog":

				self.giocatoreDelTurno.NumArmy+=10

				if c1x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			elif c1=="drago":

				self.giocatoreDelTurno.NumArmy+=12

				if c1x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			else:

				self.response("Azione non disponibile")

		elif c1!=c2 and c1!=c3 and c2!=c3:

			self.giocatoreDelTurno.NumArmy+=14

			if c1x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			if c2x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			if c3x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

		elif c1 =="jolly" or c2=="jolly" or c3=="jolly":

			if c1 =="jolly" and c2==c3:

				self.giocatoreDelTurno.NumArmy+=15

				if c1x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			elif c2 =="jolly" and c1==c3:

				self.giocatoreDelTurno.NumArmy+=15

				if c1x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			elif c3 =="jolly" and c2==c1:			

				self.giocatoreDelTurno.NumArmy+=15

				if c1x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c2x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

				if c3x.armateExtra==True:
					self.giocatoreDelTurno.NumArmy+=2

			else:

				self.response("Combinazione non valida")

		else:

			self.response("Combinazione non valida")

	def distribuzioneArmateDuranteIlTurno(self):
	
		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if player.NumArmy==0:

					if "finito" in self.query and self.query["finito"]==["true"]:

						self.STATO=2.2
						self.response("Battagliaaaaa!!!...o no?")

					elif "azione" in self.query and "territorio" in self.query and self.query["azione"]==["remove"] and self.query["territorio"]:									

						for g in self.territoriFissi:
							
							if g.code==self.query["territorio"]:
								territorio=g

						if territorio in self.giocatoreDelTurno.territori:

							if territorio.numArmyT>=2:

								territorio.numArmyT=territorio.numArmyT-1
								self.giocatoreDelTurno.NumArmy=player.NumArmy+1

							else:

								self.response("Azione non disponibile.")

						else:

							self.response("Azione non disponibile.")

					else:

						self.response("Azione non disponibile")

				else:

					if "azione" in self.query and "territorio" in self.query and self.query["territorio"]:

						territorio=None

						for g in self.territoriFissi:
							if g.nomeT==self.query["territorio"]:
								territorio=g

						if territorio in self.giocatoreDelTurno.territori:
							
							if self.query["azione"]==["add"]:

								territorio.numArmyT=territorio.numArmyT+1
								self.giocatoreDelTurno.NumArmy=player.NumArmy-1

							elif self.query["azione"]==["remove"]:

								if territorio.numArmyT>=2:

									territorio.numArmyT=territorio.numArmyT-1
									self.giocatoreDelTurno.NumArmy=player.NumArmy+1

								else:

									self.response("Azione non disponibile.")

							else:

								self.response("Azione non disponibile")

						else:

							self.response("Azione non disponibile")

					else:

						self.response("Azione non disponibile")

			else:
				
				if "attesa" in self.query and self.query["attesa"]==["4"]:
					
					self.response("E' il turno di {}. Ti faremo sapere se e quando attacchera' un tuo territorio.".format(self.giocatoreDelTurno))
				else:

					self.response("Azione non disponibile")		

		else:
			self.rispostina()

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 2.2    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def vuoiCombattere(self):

		self.territorioAttacco=None

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "territorio" in self.query:

					territorio=None

					for g in self.territoriFissi:
						if g.nomeT==self.query["territorio"]:
							territorio=g

					if territorio in self.giocatoreDelTurno.territori and territorio.numArmyT>=2:

						self.territorioAttacco=territorio
						self.STATO=2.21
						self.response("Scegli quale territorio attaccare.")

					else:

						self.response("Azione non disponibile")

				elif "avanti" in self.query and self.query["avanti"]==["OK"]:

					self.STATO=2.3
					self.response("Ultima fase del turno. Sposta delle armate da un territorio a un altro.")

				else:

					self.response("Azione non disponibile.")

			else:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
					
					self.response("E' il turno di {}. Ti faremo sapere se e quando attacchera' un tuo territorio.".format(self.giocatoreDelTurno))
				else:

					self.response("Azione non disponibile")
		
		else:
			self.rispostina()

	def dimmiDestinazione(self):
		
		self.territorioDifesa=None
		self.difensore=None

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "territorio" in self.query:

					territorio=None

					for g in self.territoriFissi:
						if g.nomeT==self.query["territorio"]:
							territorio=g

					if territorio in self.territorioAttacco.territoriConfinanti and territorio not in self.giocatoreDelTurno.territori:

						self.territorioDifesa=territorio

						for g in self.giocatori:
							
							if self.territorioDifesa in g.territori:
								
								self.difensore=g

						self.STATO=2.22
						self.response("Scegli con quante armate attaccare.")

					else:

						self.response("Azione non disponibile")

				else:

					self.response("Azione non disponibile.")

			else:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
					
					self.response("E' il turno di {}. Ti faremo sapere se e quando attacchera' un tuo territorio.".format(self.giocatoreDelTurno))
				else:

					self.response("Azione non disponibile")		
		
		else:
			self.rispostina()

	def conQuanteArmate(self):

		self.NumArmyATTACCO=0

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "armate" in self.query and self.query["armate"]<=3 and self.query["armate"]>=1 and self.query["armate"]<self.territorioAttacco.numArmyT:
					
					self.NumArmyATTACCO=self.query["armate"]
					self.STATO=2.23
					self.response("Aspetta la risposta del difensore.")

				else:

					self.response("Azione non disponibile")					

			else:

				if self.cliente[0]==self.difensore.IP:

					if "attesa" in self.query and self.query["attesa"]==["4"]:

						if self.NumArmyATTACCO==0:
					
							self.response("{} ti sta attaccando. Territorio attaccante: {}. Territorio difensore (di tua proprieta): {}. Aspetta che scelga con quante armate.".format(self.giocatoreDelTurno,self.territorioAttacco,self.territorioDifesa))
			
						elif self.NumArmyATTACCO>0 and self.NumArmyATTACCO<=3:

							self.response("{} ha deciso di attaccarti con {} armate".format(self.giocatoreDelTurno,self.NumArmyATTACCO))

						else:

							self.response("Azione non disponibile")

					else:

						self.response("Azione non disponibile")

				else:

					if "attesa" in self.query and self.query["attesa"]==["4"]:
					
						self.response("{}({}) sta attaccando {}({}). Tra poco potrai assistere alla battaglia.".format(self.territorioAttacco,self.giocatoreDelTurno,self.territorioDifesa,self.difensore))
				
					else:

						self.response("Azione non disponibile")
		
		else:

			self.rispostina()

	def difensoreNumArmy(self):

		self.NumArmyDIFESA=0

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.difensore.IP:

				if "armate" in self.query:

					if self.query["armate"]>=1 and self.query["armate"]<=3 and self.query["armate"]<self.territorioDifesa.numArmyT:

						if self.query["armate"]<=NumArmyATTACCO:

							self.NumArmyDIFESA=self.query["armate"]
							self.response("Inizio della battaglia.")
							self.STATO=2.24

						else:

							self.response("Azione non disponibile")

					else:

						self.response("Azione non disponibile")

				else:

					self.response("Azione non disponibile")

			else:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
				
					self.response("{} sta scegliendo il numero di armate con cui difendersi.".format(self.difensore))

				else:

					self.response("Azione non disponibile.")

		else:

			self.rispostina()

	def battaglia(self):

		arraynoATT=[]
		arraynoDEF=[]

		arraynoATT,arraynoDEF=self.dadi()

	def dadi(self):
		dadoA1=None
		dadoA2=None
		dadoA3=None

		dadoD1=None
		dadoD2=None
		dadoD3=None

		arraynoATT=[]
		arraynoDEF=[]

		if self.NumArmyATTACCO==1:

			dadoA1=randint(1,6)
			dadoA2=0
			dadoA3=0

		elif self.NumArmyATTACCO==2:

			dadoA1=randint(1,6)
			dadoA2=randint(1,6)
			dadoA3=0

		elif self.NumArmyATTACCO==3:

			dadoA1=randint(1,6)
			dadoA2=randint(1,6)
			dadoA3=randint(1,6)

		if self.NumArmyDIFESA==1:

			dadoD1=randint(1,6)
			dadoD2=0
			dadoD3=0

		elif self.NumArmyDIFESA==2:

			dadoD1=randint(1,6)
			dadoD2=randint(1,6)
			dadoD3=0

		elif self.NumArmyDIFESA==3:

			dadoD1=randint(1,6)
			dadoD2=randint(1,6)
			dadoD3=randint(1,6)

		arraynoATT.append(dadoA1,dadoA2,dadoA3)
		arraynoDEF.append(dadoD1,dadoD2,dadoD3)

		sorted(arraynoATT,key=int,reverse=True)
		sorted(arraynoDEF,key=int,reverse=True)

		return arraynoATT,arraynoDEF

	def fineOinizio(self):

		self.difensore=None
		self.territorioDifesa=None
		self.territorioAttacco=None
		self.NumArmyATTACCO=None
		self.NumArmyDIFESA=None

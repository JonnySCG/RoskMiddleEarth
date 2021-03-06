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
		self.carteUsate=[]

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

	def DistribuzioneTerritori(self):

		#Listona contains all the objects (like Territori, colori, ecc)
		from random import shuffle
		shuffle(self.territoriGenerali)

		#Let's create a container where we will put the list of each player
		lista=[]

		#Shall we distribute all the compoenents of Listona, or only one for each player?

		if self.numPmax==2:

			listina1=self.giocatori[0].territori
			listina2=self.giocatori[1].territori

			lista=[listina1,listina2]

		elif self.numPmax==3:

			listina1=self.giocatori[0].territori
			listina2=self.giocatori[1].territori
			listina3=self.giocatori[2].territori

			lista=[listina1,listina2,listina3]

		elif self.numPmax==4:

			listina1=self.giocatori[0].territori
			listina2=self.giocatori[1].territori
			listina3=self.giocatori[2].territori
			listina4=self.giocatori[3].territori

			lista=[listina1,listina2,listina3,listina4]

		elif self.numPmax==5:

			listina1=self.giocatori[0].territori
			listina2=self.giocatori[1].territori
			listina3=self.giocatori[2].territori
			listina4=self.giocatori[3].territori
			listina5=self.giocatori[4].territori

			lista=[listina1,listina2,listina3,listina4,listina5]

		elif self.numPmax==6:

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
		for i,val in enumerate(self.territoriGenerali):
			lista[i%self.numPmax].append(val)

	def DistribuzioneRoba(self,Listona):
		
		a=Listona

		if a==self.obiettivi:

			self.giocatori[0].obiettivoGiocatore=a[0]
			self.giocatori[1].obiettivoGiocatore=a[4]

			if self.numPmax>=3:
				self.giocatori[2].obiettivoGiocatore=a[5]

				if self.numPmax>=4:
					self.giocatori[3].obiettivoGiocatore=a[2]

					if self.numPmax>=5:
						self.giocatori[4].obiettivoGiocatore=a[3]

						if self.numPmax==6:
							self.giocatori[5].obiettivoGiocatore=a[1]


		elif a==self.colori:

			self.giocatori[0].colore=a[0]
			self.giocatori[1].colore=a[4]

			if self.numPmax>=3:
				self.giocatori[2].colore=a[5]

				if self.numPmax>=4:
					self.giocatori[3].colore=a[2]

					if self.numPmax>=5:
						self.giocatori[4].colore=a[3]

						if self.numPmax==6:
							self.giocatori[5].colore=a[1]

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 0      OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def analizzaPrimaRequest(self):

		if not self.query:

			if self.numP==0:
				player=Giocatore(1,self.cliente) #creazione giocatore
				permesso=self.aggiungiP(player)
				self.response("benvenuto nella partita, in attesa di altri giocatori")
				u.debug("sto cambiando stato",4)
				self.giocatoreDelTurno=self.giocatori[self.numeroGiocatoreDelTurno]
				self.STATO=0.1
				
		else:

		 	self.response(None,"404 NOTFOUND")

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
					self.response("Numero giocatori raggiunto. Confermare di voler iniziare la partita")	
					self.STATO=0.2

				else:
					self.response("benvenuto nella partita, in attesa di altri giocatori")

			else:
				self.response("benvenuto nella partita, in attesa di altri giocatori.")

		else:

			if self.cliente[0] in self.listaIP:

				if self.query["attesa"]==["1"]:
					
					self.response("benvenuto nella partita, in attesa di altri giocatori")
				
				else:

					self.response("benvenuto nella partita, in attesa di altri giocatori")

			else:

				self.response(None,"404 NOTFOUND")

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 0.2    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def analizzaRichiesteOK(self):

		#distribuzione territori
		self.DistribuzioneTerritori()
		
		#distribuzione obiettivo
		self.DistribuzioneRoba(self.obiettivi)

		#distribuzione colore
		self.DistribuzioneRoba(self.colori)

		if self.numPmax==3:

			for x in self.giocatori:
				
				x.numArmy=41
				x.numArmyDisponibili-=41

		if self.numPmax==4:

			for x in self.giocatori:
				
				x.numArmy=35			
				x.numArmyDisponibili-=35

		if self.numPmax==5:

			for x in self.giocatori:
				
				x.numArmy=29
				x.numArmyDisponibili-=29

		if self.numPmax==6:

			for x in self.giocatori:
				
				x.numArmy=23
				x.numArmyDisponibili-=23

		for x in self.territoriFissi:

			x.addTConfinanti()

		for x in self.giocatori:

			if x.obiettivoGiocatore in self.obiettivi:

				x.obiettivoGiocatore.proprietario=x

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

					self.response("Benvenuto nella Terra di Mezzo. Colore della tua armata: {}, Il tuo obiettivo: {}, Armate da distribuire: {}. Lista dei tuoi territori: {}. Vai alla distribuzione delle armate sui territori".format(player.colore , player.obiettivoGiocatore.code , player.numArmy , ([x.code for x in player.territori])))

					self.STATO=1.1

				else:

					self.response("Aspettare la conferma degli altri giocatori.","200 OK")
					
			elif "attesa" in self.query:

				if self.query["attesa"]==["1"]:

	 				self.response("Numero giocatori raggiunto. Confermare di voler iniziare la partita","200 OK")

	 			elif self.query["attesa"]==["2"]:

	 				self.response("Attendere la conferma degli altri giocatori")

	 			else:

					if player.conferma==True:

						self.response("Azione non disponibile. Aspettare la conferma degli altri giocatori.","200 OK")

					else:

						self.response("Azione non disponibile. Inviare la conferma.","200 OK")


			else:

				if player.conferma==True:

						self.response("Azione non disponibile. Aspettare la conferma degli altri giocatori.","200 OK")

				else:

						self.response("Azione non disponibile. Inviare la conferma.","200 OK")

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
				
				if "conferma2" in self.query and self.query["conferma2"]==["OK"]:

					if verificaDisTerritori()==True:
						
						self.STATO=1.5
						self.response("Distribuisci le armate sui tuoi territori.")

					else:

						self.response("In attesa degli altri giocatori.")


				elif "attesa" in self.query:

					if self.query["attesa"]==["2"]:

						self.response("Benvenuto nella Terra di Mezzo. Colore della tua armata: {}, Il tuo obiettivo: {}, Armate da distribuire: {}. Lista dei tuoi territori: {}. Vai alla distribuzione delle armate sui territori".format(player.colore , player.obiettivoGiocatore.code , player.numArmy , [x.code for x in player.territori]))

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

					self.response(self.inviaTutto())

				else:

					if player.finitoDisArmy==True:

						if "ritorna" in self.query and self.query["ritorna"]==[1]:

							player.finitoDisArmy=False
							self.response("Puoi ricominciare a distribuire le tue armate")

						elif "aggiornami" in self.query and self.query["aggiornami"]==["1"]:

							self.response(self.inviaTutto())


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

		self.prossimoGiocatoreTurno=None

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
				
					x=len(self.giocatoreDelTurno.territori)/3
					y=0
					z=0

					if x<=3: y=0
					elif x>=4 and x<=9: y=1
					elif x>=10 and x<=15: y=2
					elif x==16: y=3

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
					
						z+=6

					if len(arrayno2)==10:
					
						z+=8

					if len(arrayno3)==6:
					
						z+=4

					if len(arrayno4)==5:
					
						z+=3

					if len(arrayno5)==9:
					
						z+=5

					if len(arrayno6)==10:
					
						z+=7

					self.STATO=2.15
					self.response("E' il tuo turno. Armate guadagnate grazia al numero dei territori posseduti:{}. Armate guadagnate grazie al monopolio su interi continenti: {}. Decidi se inviare una combinazione di carte, o se passare direttamente alla disposizione delle armate." .format((x+y),z))

					self.giocatoreDelTurno.numArmy+=(x+y+z)

				elif "carta1" in self.query and "carta2" in self.query and "carta3" in self.query:

					codiciQuery=[]

					codiciQuery.append(self.query["carta1"])
					codiciQuery.append(self.query["carta2"])
					codiciQuery.append(self.query["carta3"])

					w=self.ArmyDaCarte(self.estrapolaCarte(codiciQuery))

					self.giocatoreDelTurno.numArmy+=w

					#self.giocatoreDelTurno.numArmyDisponibili-=numArmy
					self.response("Combinazione analizzata: {} armate guadagnate con le tre carte. Totale armate da distribuire: {}" .format(w,self.giocatoreDelTurno.NumArmy))
					self.STATO=2.15

				elif "DistLeArmy" in self.query and self.query["DistLeArmy"]==["OK"]:

					#self.giocatoreDelTurno.numArmyDisponibili-=numArmy
					response("Distribuisci le armate guadagnate.")
					self.STATO=2.15

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

		c1x.proprietario=None
		c2x.proprietario=None
		c3x.proprietario=None

		numeroDaRitornare=0

		if c1==c2 and c1==c3:

			if c1=="troll":

				numeroDaRitornare+=8

				if c1x.armateExtra==True:
					numeroDaRitornare+=2

				if c2x.armateExtra==True:
					numeroDaRitornare+=2

				if c3x.armateExtra==True:
					numeroDaRitornare+=2

				self.giocatoreDelTurno.carteCombinazioni.remove(c1x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c2x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c3x)

				c1x.proprietario=None
				c2x.proprietario=None
				c3x.proprietario=None

				self.carteUsate.append(c1x)
				self.carteUsate.append(c2x)
				self.carteUsate.append(c3x)

				return numeroDaRitornare

			elif c1=="balrog":

				numeroDaRitornare+=10

				if c1x.armateExtra==True:
					numeroDaRitornare+=2

				if c2x.armateExtra==True:
					numeroDaRitornare+=2

				if c3x.armateExtra==True:
					numeroDaRitornare+=2

				self.giocatoreDelTurno.carteCombinazioni.remove(c1x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c2x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c3x)

				c1x.proprietario=None
				c2x.proprietario=None
				c3x.proprietario=None

				self.carteUsate.append(c1x)
				self.carteUsate.append(c2x)
				self.carteUsate.append(c3x)

				return numeroDaRitornare

			elif c1=="drago":

				numeroDaRitornare+=12
				

				if c1x.armateExtra==True:
					numeroDaRitornare+=2

				if c2x.armateExtra==True:
					numeroDaRitornare+=2

				if c3x.armateExtra==True:
					numeroDaRitornare+=2

				self.giocatoreDelTurno.carteCombinazioni.remove(c1x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c2x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c3x)

				c1x.proprietario=None
				c2x.proprietario=None
				c3x.proprietario=None

				self.carteUsate.append(c1x)
				self.carteUsate.append(c2x)
				self.carteUsate.append(c3x)

				return numeroDaRitornare

			else:

				self.response("Azione non disponibile")

		elif c1!=c2 and c1!=c3:

			if c1x.armateExtra==True:
					numeroDaRitornare+=2

			if c2x.armateExtra==True:
					numeroDaRitornare+=2

			if c3x.armateExtra==True:
					numeroDaRitornare+=2

			self.giocatoreDelTurno.carteCombinazioni.remove(c1x)
			self.giocatoreDelTurno.carteCombinazioni.remove(c2x)
			self.giocatoreDelTurno.carteCombinazioni.remove(c3x)

			c1x.proprietario=None
			c2x.proprietario=None
			c3x.proprietario=None

			self.carteUsate.append(c1x)
			self.carteUsate.append(c2x)
			self.carteUsate.append(c3x)

			return numeroDaRitornare

		elif c1 =="jolly" or c2=="jolly" or c3=="jolly":

			if c1 == "jolly" and c2==c3:
				numeroDaRitornare+=15

				if c1x.armateExtra==True:
					numeroDaRitornare+=2

				if c2x.armateExtra==True:
					numeroDaRitornare+=2

				if c3x.armateExtra==True:
					numeroDaRitornare+=2

				self.giocatoreDelTurno.carteCombinazioni.remove(c1x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c2x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c3x)

				c1x.proprietario=None
				c2x.proprietario=None
				c3x.proprietario=None

				self.carteUsate.append(c1x)
				self.carteUsate.append(c2x)
				self.carteUsate.append(c3x)

				return numeroDaRitornare

			elif c2 == "jolly" and c1==c3:
				numeroDaRitornare+=15

				if c1x.armateExtra==True:
					numeroDaRitornare+=2

				if c2x.armateExtra==True:
					numeroDaRitornare+=2

				if c3x.armateExtra==True:
					numeroDaRitornare+=2

				self.giocatoreDelTurno.carteCombinazioni.remove(c1x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c2x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c3x)

				c1x.proprietario=None
				c2x.proprietario=None
				c3x.proprietario=None

				self.carteUsate.append(c1x)
				self.carteUsate.append(c2x)
				self.carteUsate.append(c3x)

				return numeroDaRitornare

			elif c3 =="jolly" and c1==c2:

				numeroDaRitornare+=15

				if c1x.armateExtra==True:
					numeroDaRitornare+=2

				if c2x.armateExtra==True:
					numeroDaRitornare+=2

				if c3x.armateExtra==True:
					numeroDaRitornare+=2

				self.giocatoreDelTurno.carteCombinazioni.remove(c1x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c2x)
				self.giocatoreDelTurno.carteCombinazioni.remove(c3x)

				c1x.proprietario=None
				c2x.proprietario=None
				c3x.proprietario=None

				self.carteUsate.append(c1x)
				self.carteUsate.append(c2x)
				self.carteUsate.append(c3x)

				return numeroDaRitornare

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

		self.almenoUnaConquista=False

		self.territorioAttacco=None

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "territorio" in self.query:

					territorio=None

					for g in self.territoriFissi:
						if g.code==self.query["territorio"]:
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

			elif self.cliente[0]==self.difensore.IP:

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

					if self.query["armate"]>=1 and self.query["armate"]<=3 and self.query["armate"]<=self.territorioDifesa.numArmyT:

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

		confermap1=False
		confermap2=False

		armateDaTrasportare=0

		conquistaRiuscita=False

		armatePerseATT=0
		armatePerseDEF=0

		arraynoATT,arraynoDEF=self.dadi()

		armatePerseATT,armatePerseDEF=self.armatePerse(arraynoATT,arraynoDEF,self.NumArmyATTACCO,self.NumArmyDIFESA)

		if armatePerseDEF==self.territorioDifesa.numArmyT:
			
			self.difensore.territori.remove(self.territorioDifesa)
			self.giocatoreDelTurno.territori.add(self.territorioDifesa)
			conquistaRiuscita=True
			armateDaTrasportare=self.NumArmyATTACCO-armatePerseATT
			self.territorioAttacco.numArmyT=self.territorioAttacco.numArmyT-self.NumArmyATTACCO
			self.territorioDifesa.numArmyT=armateDaTrasportare

		if conquistaRiuscita==True and len(self.difensore.territori)==0:
			
			self.difensore.eliminato=True
			self.giocatori.remove(self.difensore)
			self.giocatoreDelTurno.giocatoriEliminati.append(self.difensore)

		#00000000000000000000000000000000000000000000000000000

		if self.cliente[0] in self.listaIP:

			self.response("Dadi attaccante:{},{},{}. Dadi difensore:{},{},{}".format(arraynoATT[0],arraynoATT[1],arraynoATT[2],arraynoDEF[0],arraynoDEF[1],arraynoDEF[2]))

			if self.cliente[0] == self.giocatoreDelTurno.IP:	

				if "attesa" in self.query and self.query["attesa"]==["4"]:

					if conquistaRiuscita==True:

						if self.difensore.eliminato==True:
							
							self.response("Hai conquistato {}, eliminando {}, e perdendo {} armate. {} delle armate che hai usato in battaglia ora occupano il territorio. Conferma di voler concludere la battaglia.".format(armatePerseATT,self.difensore,self.difensore,armatePerseDEF))

						else:

							self.almenoUnaConquista=True
							self.response("Hai conquistato {}, perdendo {} armate. {} delle armate che hai usato in battaglia ora occupano il territorio. Conferma di voler concludere la battaglia.".format(self.territorioDifesa,armatePerseATT,armateDaTrasportare))

					else:

						self.response("Bilancio battaglia >> Tu: {} armate perse. {}: {} armate perse".format(armatePerseATT,self.difensore,armatePerseDEF))

				elif "conferma" in self.query and self.query["conferma"]==["OK"]:

					if confermap2==True:

						if self.giocatoreDelTurno.obiettivoGiocatore.obCompletato:
						
							self.response("Complimenti, hai raggiunto il tuo obiettivo. Goditi la gloria eterna!" )
							self.STATO=3

						else:

							self.response("Conclusione battaglia. Vuoi iniziarne un'altra o concludere il tuo turno?")
							self.STATO=2.25
					else:

						confermap1=True
						self.response("In attesa della conferma dell'avversario.")

				else:

					self.response("Azione non disponibile.")

			elif self.cliente[0]==self.difensore.IP:

				if "attesa" in self.query and self.query["attesa"]==["4"]:

					if conquistaRiuscita==True:

						if self.difensore.eliminato==True:
							
							self.response("Sei stato eliminato.")

						else:

							self.response("Hai perso {}, insieme a tutte le armate con cui ti sei difeso. Conferma di voler concludere la battaglia.".format(self.territorioDifesa))

					else:

						self.response("Bilancio battaglia >> {}: {} armate perse. Tu: {} armate perse".format(self.giocatoreDelTurno,armatePerseATT,armatePerseDEF))

				elif "conferma" in self.query and self.query["conferma"]==["OK"]:

					if confermap1==True:

						self.STATO=2.25
						self.response("Conclusione battaglia. Vuoi iniziarne un'altra o concludere il tuo turno?")

					else:

						confermap2=True
						self.response("In attesa della conferma dell'avversario.")

				else:

					self.response("Azione non disponibile")

			else:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
				
					if conquistaRiuscita==True:
					
						self.response("{} ha conquistato {}.".format(self.giocatoreDelTurno,self.territorioDifesa))

					else:

						self.response("Bilancio battaglia >> {}: {} armate perse. {}: {} armate perse".format(self.giocatoreDelTurno,armatePerseATT,self.difensore,armatePerseDEF))
			
				else:

					self.response("Azione non disponibile")
	
		else:

			self.rispostina()

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

	def armatePerse(self,list1,list2,nA,nD):

		apA=None
		apD=None

		if nA==nD:

			if nA==1:

				if list2[0]>=list1[0]:
					apA=apA+1

				else:
					apD=apD+1

			elif nA==2:

				if list2[0]>=list1[0]:
					apA=apA+1

				else:
					apD=apD+1

				if list2[1]>=list1[1]:
					apA=apA+1

				else:
					apD=apD+1

			elif nA==3:

				if list2[0]>=list1[0]:
					apA=apA+1

				else:
					apD=apD+1

				if list2[1]>=list1[1]:
					apA=apA+1

				else:
					apD=apD+1

				if list2[2]>=list1[2]:
					apA=apA+1

				else:
					apD=apD+1


				
		elif nA>nD:

			if nA==2:

				if list2[0]>=list1[0]:
					apA=apA+1

				else:
					apD=apD+1

			elif nA==3:

				if nD==1:

					if list2[0]>=list1[0]:
						apA=apA+1

					else:
						apD=apD+1

				else:

					if list2[0]>=list1[0]:
						apA=apA+1

					else:
						apD=apD+1

					if list2[1]>=list1[1]:
						apA=apA+1

					else:
						apD=apD+1



		elif nA<nD:

			if nD==2:

				if list2[0]>=list1[0]:
					apA=apA+1

				else:
					apD=apD+1

			elif nD==3:

				if nA==1:

					if list2[0]>=list1[0]:
						apA=apA+1

					else:
						apD=apD+1

				else:

					if list2[0]>=list1[0]:
						apA=apA+1

					else:
						apD=apD+1

					if list2[1]>=list1[1]:
						apA=apA+1

					else:
						apD=apD+1

		return apA,apD

	def fineOinizio(self):

		self.difensore=None
		self.territorioDifesa=None
		self.territorioAttacco=None
		self.NumArmyATTACCO=None
		self.NumArmyDIFESA=None

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "conferma" in self.query and self.query["conferma"]==["OK"]:

					self.giocatoreDelTurno.obiettivoGiocatore.controllaObCompletato()

					if self.giocatoreDelTurno.obiettivoGiocatore.obCompletato== True:
					
						self.response("Complimenti, hai raggiunto il tuo obiettivo. Goditi la gloria eterna!" )
						self.STATO=3

					else:

						self.response("Conclusione battaglia. Vuoi iniziarne un'altra o concludere il tuo turno?")

				elif "territorio" in self.query:

					territorio=None

					for g in self.territoriFissi:
						if g.code==self.query["territorio"]:
							territorio=g

					if territorio in self.giocatoreDelTurno.territori and territorio.numArmyT>=2:

						self.territorioAttacco=territorio
						self.response("Scegli quale territorio attaccare.")
						self.STATO=2.21

					else:

						self.response("Azione non disponibile")

				elif "avanti" in self.query and self.query["avanti"]==["OK"]:

					if self.almenoUnaConquista==True:

						self.response("Puoi pescare una carta.")
						self.STATO=2.31

					else:

						self.response("Ultima fase del turno. Sposta delle armate da un territorio a un altro.")
						self.STATO=2.32

				else:

					self.response("Azione non disponibile.")

			else:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
					
					self.response("E' il turno di {}. Ti faremo sapere se e quando attacchera' un tuo territorio.".format(self.giocatoreDelTurno))
				else:

					self.response("Azione non disponibile")
		
		else:
			self.rispostina()		

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 2.3    OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def pescareCarta(self):

		if self.numeroGiocatoreDelTurno<=self.numP-1:

			self.prossimoGiocatoreTurno=self.giocatori[self.giocatoreDelTurno.ordine+1]

		else:

			self.prossimoGiocatoreTurno=self.giocatori[0]

		#00000000000000000000000000000000000000000000000000000000000000000

		if len(self.carte)==0:
			
			self.carte=self.carteUsate[:]
			self.carteUsate=[]

		cartaPescata=None


		#00000000000000000000000000000000000000000000000000000000000000000

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "pesca" in self.query and self.query["pesca"]==["OK"]:

					shuffle(carte)
					cartaPescata=carte[0]
					cartaPescata.proprietario=self.giocatoreDelTurno
					self.giocatoreDelTurno.carteCombinazioni.append(cartaPescata)
					self.carte.remove(cartaPescata)
					self.STATO=2.32

				else:

					self.response("Azione non disponibile.")


			elif self.cliente[0] == self.prossimoGiocatoreTurno.IP:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
					
					self.response("{} sta per concludere il suo turno. Preparati, il prossimo sei tu.".format(self.giocatoreDelTurno))
				else:

					self.response("Azione non disponibile")

			else:

				if "attesa" in self.query and self.query["attesa"]==["4"]:
					
					self.response("{} sta per concludere il suo turno. Il prossimo e' {}".format(self.giocatoreDelTurno,self.prossimoGiocatoreTurno))

				else:

					self.response("Azione non disponibile")
		
		else:

			self.rispostina()

	def spostareArmy(self):

		if self.cliente[0] in self.listaIP:

			if self.cliente[0] == self.giocatoreDelTurno.IP:

				if "territorio1" in self.query and "num" in self.query and "territorio2" in self.query:

					territorio1=None
					territorio2=None
					numArmateDaSpostare=self.query["num"]

					for g in self.territoriFissi:

						if g.code==self.query["territorio1"]:
							territorio1=g

						if g.code==self.query["territorio2"]:
							territorio2=g

					if territorio1 in self.giocatoreDelTurno.territori and territorio1.numArmyT-numArmateDaSpostare>=1:

						if territorio2 in territorio1.territoriConfinanti and territorio2 in self.giocatoreDelTurno.territori:

							territorio1.numArmyT-=numArmateDaSpostare
							territorio2.numArmyT+=numArmateDaSpostare
							self.giocatoreDelTurno=self.prossimoGiocatoreTurno
							self.STATO=2.1

						else:

							self.response("Azione non disponibile.")

					else:

						self.response("Azione non disponibile")

				elif "avanti" in self.query and self.query["avanti"]==["OK"]:

					self.giocatoreDelTurno=self.prossimoGiocatoreTurno
					self.STATO=2.1

				else:

					self.response("Azione non disponibile.")

			else:

				if "attesa" in self.query and self.query["attesa"]==["4"]:

					self.response(self.inviaTutto())					
					self.response("{} sta concludendo il suo turno.".format(self.giocatoreDelTurno))

				else:

					self.response("Azione non disponibile")
		
		else:
			self.rispostina()

#OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO
#  STATO 3      OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO

	def finePartita(self):

		if self.cliente[0] in self.listaIP:

			player=None

			for g in self.giocatori:
					
				if g.IP==self.cliente[0]:

					player=g

			if "attesa" in self.query and self.query["attesa"]==["4"]:

				self.response("{} ha raggiunto il suo obiettivo ({}). La partita e' terminata".format(self.giocatoreDelTurno,self.giocatoreDelTurno.obiettivoGiocatore.stringa))
				self.giocatori.remove(player)

				if len(self.giocatori)==0:
				
					self.obiettivi=[]
					self.carte=[]
					self.territoriGenerali=[]
					self.territoriFissi=[]
					self.carteUsate=[]##########quasi sempre
					with open('json.json') as data_file:
						data = json.load(data_file)
						self.obiettivi=u.parser(CartaObiettivo,data["obiettivi"],self)
						self.territoriGenerali=u.parser(Territorio,data["territori"],self)
						self.territoriFissi=self.territoriGenerali[:]
						self.carte=u.parser(Carta,data["carte"],self)
					self.numPmax=numPmax
					self.numP=0
					self.giocatori=[]######solo qualche variabile
					self.listaIP=[]
					self.colori=["blu","rosso","giallo","nero","verde","viola"]
					self.giocatoreDelTurno=None##########quasi sempre

					self.STATO=0


		else:

			self.response("La partita in corso sta terminando.")

	def inviaTutto(self):

		toReturn={}

		if self.numPmax==3:
			# To indent properly a multi-line dictionaty see:
			# https://stackoverflow.com/questions/6388187/what-is-the-proper-way-to-format-a-multi-line-dict-in-python

			toReturn={
				"cUsate":[x.code for x in self.carteUsate],
				"pTurno":self.giocatoreDelTurno,	
				"p1":{

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,

				},	
				"p2":{

					"coloreP":self.giocatori[1].colore,
					"codezTerritori":[x.code for x in self.giocatori[1].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[1].territori],
					"eliminatez":self.giocatore[1].eliminato,

				},	
				"p1":{

					"coloreP":self.giocatori[2].colore,
					"codezTerritori":[x.code for x in self.giocatori[2].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[2].territori],
					"eliminatez":self.giocatore[2].eliminato,

				}	

			}

		elif self.numPmax==4:

			toReturn={

				"cUsate":[x.code for x in self.carteUsate],
				"pTurno":self.giocatoreDelTurno,

				"p1":{

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,

				},	
				"p2":{

					"coloreP":self.giocatori[1].colore,
					"codezTerritori":[x.code for x in self.giocatori[1].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[1].territori],
					"eliminatez":self.giocatore[1].eliminato,

				},	
				"p3":{

					"coloreP":self.giocatori[2].colore,
					"codezTerritori":[x.code for x in self.giocatori[2].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[2].territori],
					"eliminatez":self.giocatore[2].eliminato,

				},	
				"p4":{

					"coloreP":self.giocatori[3].colore,
					"codezTerritori":[x.code for x in self.giocatori[3].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[3].territori],
					"eliminatez":self.giocatore[3].eliminato,

				}

			}

		elif self.numPmax==5:

			toReturn={

				"cUsate":[x.code for x in self.carteUsate],
				"pTurno":self.giocatoreDelTurno,

				"p1":{

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,

				},	
				"p2":{

					"coloreP":self.giocatori[1].colore,
					"codezTerritori":[x.code for x in self.giocatori[1].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[1].territori],
					"eliminatez":self.giocatore[1].eliminato,

				},	
				"p3":{

					"coloreP":self.giocatori[2].colore,
					"codezTerritori":[x.code for x in self.giocatori[2].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[2].territori],
					"eliminatez":self.giocatore[2].eliminato,

				},
				"p4":{

					"coloreP":self.giocatori[3].colore,
					"codezTerritori":[x.code for x in self.giocatori[3].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[3].territori],
					"eliminatez":self.giocatore[3].eliminato,

				},	
				"p5":{

					"coloreP":self.giocatori[4].colore,
					"codezTerritori":[x.code for x in self.giocatori[4].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[4].territori],
					"eliminatez":self.giocatore[4].eliminato,

				}					

			}

		elif self.numPmax==6:

			toReturn={

				"cUsate":[x.code for x in self.carteUsate],
				"pTurno":self.giocatoreDelTurno,

				"p1":{ #ATENZIONE!! qua tutti i pN, ritornano propiet'a del giocatore [0]!!!
						# TODO: FIX

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,

				},	
				"p2":{

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,

				},	
				"p3":{

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,

				},
				"p4":{

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,

				},	
				"p5":{

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,

				},	
				"p6":{

					"coloreP":self.giocatori[0].colore,
					"codezTerritori":[x.code for x in self.giocatori[0].territori],
					"numATerritori":[x.numArmy for x in self.giocatori[0].territori],
					"eliminatez":self.giocatore[0].eliminato,
				}


			}

		return json.dumps(toReturn)






		

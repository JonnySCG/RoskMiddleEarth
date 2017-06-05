import utilities as u
import json

class Giocatore(object):

	def __init__(self,ordine,socket):
	
		self.ordine=ordine#
		self.socket=socket
		self.IP=self.socket[0]
		self.colore=""
		self.obiettivoGiocatore=None
		self.conferma=False
		self.conferma2=False
		self.NumArmy=0
		#self.NumArmyDisponibili=135
		self.finitoDisArmy=False
		self.territori=[]
		self.carteCombinazioni=[]
		self.eliminato=False
		self.giocatoriEliminati=[]

class Territorio(object):

	def __init__(self,json,match):
		self.nomeT=json["nome"]
		self.numArmyT=0
		self.codiceTerritorio=json["codice"]
		self.continente=json["continente"]
		self.proprietarioT=None
		self.coloreTerritorio=json["colore"]
		self.nomiTconfinanti=json["tConfinanti"]
		self.territoriConfinanti=[]
		self.match=match

	def addTConfinanti(self):
	
		for x in self.match.territoriFissi: 
			
			if x.codiceTerritorio in self.nomiTconfinanti: # TODO sostitute nomeT with code

				self.territoriConfinanti.append(x)
		
class Carta(object):

	def __init__(self,json,match):

		self.figura=json["figura"]
		self.codiceTerritorio=json["codice"]
		self.cartaT=None
		self.proprietario=None
		self.armateExtra=False
		self.match=match

		for x in self.match.territoriFissi:

			if x.codiceTerritorio==self.codiceTerritorio:

				self.cartaT=x

	def controllaArmateExtra(self):

		if self.proprietario == None:

			print "QUESTA CARTA NON HA PROPRIETARIO"

		for x in self.proprietario.territori:
			
			if x.code == self.code:

				self.armateExtra=True

class CartaObiettivo(object):

	def __init__(self,json,match):

		self.stringa=json["stringa"]
		self.proprietario=None
		self.ID=json["ID"]
		self.obCompletato=False
		self.match=match

	def controllaObCompletato(self):

		for x in match.giocatori:

			if x.obiettivoGiocatore == self:
				
				self.proprietario=x
	
		if self.ID=="ob28" and len(self.proprietario.territori)>=28:
			
			self.obCompletato=True

		elif self.ID=="ob21" and len(self.proprietario.territori)>=21:

			arrayno=[]

			for x in self.proprietario.territori:

				if x.numArmyT<2:

					arrayno.append(x)

			if len(arrayno)==0:

				self.obCompletato=True

		elif self.ID=="obT1":

			c1="Beleriand"
			c2="Nord Endor"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==14:

				self.obCompletato=True

		elif self.ID=="obT2":

			c1="Sud Aman"
			c2="Nord Endor"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==14:

				self.obCompletato=True	

		elif self.ID=="obT3":

			c1="Sud Aman"
			c2="Nord Aman"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==15:

				self.obCompletato=True

		elif self.ID=="obT4":

			c1="Beleriand"
			c2="Sud Aman"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==18:

				self.obCompletato=True	

		elif self.ID=="obT5":

			c1="Beleriand"
			c2="Endor Orientale"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==19:

				self.obCompletato=True

		elif self.ID=="obT6":

			c1="Sud Endor"
			c2="Endor Orientale"

			list1=[]

			for x in self.proprietario.territori:
				
				if x.continente == c1 or x.continente == c2:

					list1.append(x)

			if len(list1)==20:

				self.obCompletato=True

		elif self.ID=="obA1":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "rosso":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				if playerDaSconfiggere.eliminato==True:

					if playerDaSconfiggere in proprietario.giocatoriEliminati:
						
						self.obCompletato=True

					else:

						self.ID="ob28"

			else:

				self.ID="ob28"

		elif self.ID=="obA2":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "giallo":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				if playerDaSconfiggere.eliminato==True:

					if playerDaSconfiggere in proprietario.giocatoriEliminati:
						
						self.obCompletato=True

					else:

						self.ID="ob28"
			else:

				self.ID="ob28"

		elif self.ID=="obA3":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "blu":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				if playerDaSconfiggere.eliminato==True:

					if playerDaSconfiggere in proprietario.giocatoriEliminati:
						
						self.obCompletato=True

					else:

						self.ID="ob28"

			else:

				self.ID="ob28"

		elif self.ID=="obA4":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "verde":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				if playerDaSconfiggere.eliminato==True:

					if playerDaSconfiggere in proprietario.giocatoriEliminati:
						
						self.obCompletato=True

					else:

						self.ID="ob28"

			else:

				self.ID="ob28"

		elif self.ID=="obA5":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "nero":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				if playerDaSconfiggere.eliminato==True:

					if playerDaSconfiggere in proprietario.giocatoriEliminati:
						
						self.obCompletato=True

					else:

						self.ID="ob28"

			else:

				self.ID="ob28"

		elif self.ID=="obA6":

			colorePresente=False
			playerDaSconfiggere=None

			for x in giocatori:
				
				if x.colore == "viola":

					colorePresente=True
					playerDaSconfiggere=x

			if colorePresente==True:

				if playerDaSconfiggere.eliminato==True:

					if playerDaSconfiggere in proprietario.giocatoriEliminati:
						
						self.obCompletato=True

					else:

						self.ID="ob28"

			else:

				self.ID="ob28"

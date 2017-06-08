import unittest
import sys
from classiServah import Partita
from classiServah import Giocatore

import json

#0000000000000000000000000000000000000000000000000000000000
#	Ciao Jonny, ho fatto vari cambiamenti , e aggiunto alcuni commenti spiegandoli
#	il tuo compito adesso e aggiugere i commenti che mancano spiegando i cambiamenti che ho fatto
#	 :)
# 
#0000000000000000000000000000000000000000000000000000000000

class JonnyTester (unittest.TestCase):

	def setUp(self):
		self.data = ""
		with open('json.json') as data_file:
			self.data = json.load(data_file)

		self.Partita=Partita(3)

		# Creating some fake users
		fakeSocket = ("256,256,256,256", 99999)
		self.Partita.giocatori = [Giocatore(1,fakeSocket), Giocatore(2,fakeSocket), Giocatore(3,fakeSocket)]
		


############################################
class distributionTester(JonnyTester):

	# The testing functions must start width "test"
	def test_arrayLen_obiettivi(self):
		number = len(self.data['obiettivi'])
		
		self.assertEqual(len(self.Partita.obiettivi), number, 
			"Wrong number of 'obiettivi' in 'Partita'")
	
		# Note: the assert* functions accept a last argument in which to pass 
		# the message that will be displayed in case of failure (really usefull)

	def test_arrayLen_territori(self):	
		number = len(self.data['territori'])
		
		self.assertEqual(len(self.Partita.territoriFissi), number, 
			"Wrong number of 'territori' in 'Partita'")
		
	def test_arrayLen_carte(self):
		number = len(self.data['carte'])
		
		self.assertEqual(len(self.Partita.carte), number, 
			"Wrong number of 'Carte' in 'Partita'")


############################################

def isTroll(carta): return carta.figura == "troll"
def isBarlog(carta): return carta.figura == "balrog"
def isDrago(carta): return carta.figura == "drago"

class roundFunctionalityTester(JonnyTester):

	def setUp(self):
		# Perche ho fatto questo????
		super(roundFunctionalityTester, self).setUp()
		
		self.Partita.giocatoreDelTurno = self.Partita.giocatori[0] 
		self.Partita.giocatoreDelTurno.carteCombinazioni = self.Partita.carte[:] # a fake copy off all the cards


	def test_ArmyDaCarte_trolls(self):
		combo=filter(isTroll, self.Partita.carte)[:3] #The first 3 items of the filtered list ;) 
		print [x.figura for x in combo] #this prints the figures on the list
		
		result= self.Partita.ArmyDaCarte(combo)
		
		self.assertEqual(result, 8,
			"Wrong result: {}, when passing all trolls".format(result))

	def test_ArmyDaCarte_Balrog(self):
		# TODO
		self.assertEqual(1,0) #Dummy function to fail the test 


	def test_ArmyDaCarte_Drago(self):
		# TODO
		self.assertEqual(1,0) #Dummy function to fail the test


	def test_ArmyDaCarte_Mix(self):
		# TODO
		self.assertEqual(1,0) #Dummy function to fail the test

	# 

# Run the test only when this module is executed as the main script
if __name__ == '__main__':
	unittest.main(verbosity=2)
	 
		
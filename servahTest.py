import unittest
from classiServah import Partita

class JonnyTester (unittest.TestCase):

	def setUp(self):
		
		self.Partita=Partita(3)


class partitaTester(JonnyTester):

	def runTest(self):

		self.testareArrays()

#0000000000000000000000000000000000000000000000000000000000

	def testareArrays(self):

		self.assertEqual(len(self.Partita.obiettivi),14)
		self.assertEqual(len(self.Partita.territoriFissi),49)
		self.assertEqual(len(self.Partita.carte),51)

	def testArmyDaCarte(self):
		pass

unittest.main()
		
		
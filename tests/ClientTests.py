'''
Created on Aug 9, 2013

@author: Alejandro Riveros Cruz <lariverosc@gmail.com>
'''
import unittest
from elibom.Client import ElibomClient,ElibomClientException

class ElibomClientTests(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def testName(self):
		pass
	
	def test_send_message_args(self):
		elibom = ElibomClient('','')
		self.assertRaises(ElibomClientException, elibom.send_message,'573017897304', 'test')

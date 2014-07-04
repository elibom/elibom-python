'''
Created on Aug 9, 2013

@author: Alejandro Riveros Cruz <lariverosc@gmail.com>
'''
import unittest
import json
from elibom.Client import ElibomClient, ElibomClientException 
from mock import patch
	
class MockResponse(object):
	pass

def mock_post(url, data=None, **kwargs):
	if url.endswith('messages'):
		response = MockResponse()
		response.ok = True
		payload = json.loads(data, encoding='utf-8')
		if 'scheduledDate' in payload:
			response.content = json.dumps({'scheduleId':456})
		else:
			response.content = json.dumps({'deliveryToken':123})
		return response
	

def mock_get(url, data=None, **kwargs):
	if url.endswith('messages/123'):
		response = MockResponse()
		response.ok = True
		response.content = json.dumps({'deliveryId': 123, 'status': 'finished', 'numSent': 1, 'numFailed': 0})
		return response
	elif url.endswith('schedules/456'):
		response = MockResponse()
		response.ok = True
		response.content = json.dumps({'id': 456, 'status': 'scheduled', 'isFile': True, 'fileName': 'test.xls', 'fileHasText':False, 'text':'test'})
		return response
	elif url.endswith('schedules/scheduled'):
		response = MockResponse()
		response.ok = True
		response.content = json.dumps([{ 'id': 456,'isFile': True,'fileName': 'test.xls','fileHasText': False,'text': 'test' },{ 'id': 457,'isFile': True,'fileName': 'test.xls','fileHasText': False,'text': 'test'}])
		return response
	elif url.endswith('account'):
		response = MockResponse()
		response.ok = True
		response.content = json.dumps({'name':'test','credits':10.0})
		return response
	elif  url.endswith('users/1'):
		response = MockResponse()
		response.ok = True
		response.content = json.dumps({'id':1,'name':'testUser','email':'test@dominio.com','status':'active'})
		return response
	elif  url.endswith('users'):
		response = MockResponse()
		response.ok = True
		response.content = json.dumps([{'id':1,'name':'testUser','email':'test@dominio.com','status':'active'},{'id':2,'name':'testUser2','email':'test2@dominio.com','status':'active'}])
		return response
	
def mock_delete(url, data=None, **kwargs):
	if url.endswith('schedules/456'):
		response = MockResponse()
		response.ok = True
		return response
		
class ElibomClientTests(unittest.TestCase):

	def setUp(self):
		pass
	def tearDown(self):
		pass
	
	def test_send_message_args(self):
		elibom = ElibomClient('', '')
		self.assertRaises(ElibomClientException, elibom.send_message, '573097304', 'test')

	def test_should_fail_because_invalid_destination(self):
		elibom = ElibomClient('', '')
		self.assertRaises(ElibomClientException, elibom.send_message, '', '')
		self.assertRaises(ElibomClientException, elibom.send_message, 'cc', '')
		self.assertRaises(ElibomClientException, elibom.send_message, 'gg', '')
		self.assertRaises(ElibomClientException, elibom.send_message, '123', '')
		self.assertRaises(ElibomClientException, elibom.send_message, 'g123 33', '')
	
	@patch('elibom.Client.requests')
	def test_should_send_message(self, mock_requests):
		mock_requests.post = mock_post 
		elibom = ElibomClient('user@domain.com', 'password')
		deliveryToken = elibom.send_message('573017897304', 'test')
		self.assertEqual(123, deliveryToken, 'deliveryToken must be equal to 123')
		deliveryToken = elibom.send_message('573017897304,573017897304', 'test')
		self.assertEqual(123, deliveryToken, 'deliveryToken must be equal to 123')
		deliveryToken = elibom.send_message('g123', 'test')
		self.assertEqual(123, deliveryToken, 'deliveryToken must be equal to 123')
		deliveryToken = elibom.send_message('c123', 'test')
		self.assertEqual(123, deliveryToken, 'deliveryToken must be equal to 123')

		
	@patch('elibom.Client.requests')
	def test_should_schedule_message(self, mock_requests):
		mock_requests.post = mock_post 
		elibom = ElibomClient('user@domain.com', 'password')
		scheduleId = elibom.schedule_message('573017897304', 'test message', '2015-09-27 23:00')
		self.assertEqual(456, scheduleId, 'scheduleId must be equal to 456')
		
	@patch('elibom.Client.requests')
	def test_should_show_delivery(self, mock_requests):
		mock_requests.get = mock_get 
		elibom = ElibomClient('user@domain.com', 'password')
		delivery = elibom.show_delivery(123)
		self.assertEqual(123, delivery['deliveryId'], 'deliveryId must be equal to 123')
		self.assertEqual('finished', delivery['status'], 'status must be equal to finished')
		self.assertEqual(1, delivery['numSent'], 'numSent must be equal to 1')
		self.assertEqual(0, delivery['numFailed'], 'numFailed must be equal to 0')
		
	@patch('elibom.Client.requests')
	def test_should_show_schedule(self, mock_requests):
		mock_requests.get = mock_get 
		elibom = ElibomClient('user@domain.com', 'password')
		delivery = elibom.show_schedule(456)
		self.assertEqual(456, delivery['id'], 'id must be equal to 456')
		self.assertEqual('scheduled', delivery['status'], 'status must be equal to scheduled')
		self.assertEqual(True, delivery['isFile'], 'isFile must be equal to True')
		self.assertEqual('test.xls', delivery['fileName'], 'fileName must be equal to test.xls')
		self.assertEqual(False, delivery['fileHasText'], 'fileHasText must be equal to False')
		self.assertEqual('test', delivery['text'], 'text must be equal to test')
		
	@patch('elibom.Client.requests')
	def test_should_list_schedules(self, mock_requests):
		mock_requests.get = mock_get 
		elibom = ElibomClient('user@domain.com', 'password')
		deliveries = elibom.list_schedules()
		self.assertEqual(2, len(deliveries), 'deliveries length must be equal to 2')
		self.assertEqual(456, deliveries[0]['id'], 'id must be equal to 456')
		self.assertEqual(True, deliveries[0]['isFile'], 'isFile must be equal to True')
		self.assertEqual('test.xls', deliveries[0]['fileName'], 'fileName must be equal to test.xls')
		self.assertEqual(False, deliveries[0]['fileHasText'], 'fileHasText must be equal to False')
		self.assertEqual('test', deliveries[0]['text'], 'text must be equal to test')
		
	@patch('elibom.Client.requests')
	def test_should_delete_delivery(self, mock_requests):
		mock_requests.delete = mock_delete 
		elibom = ElibomClient('user@domain.com', 'password')
		deliveryId = elibom.cancel_schedule(456)
		self.assertEqual(456, deliveryId, 'deliveryId must be equal to 456')
		
	@patch('elibom.Client.requests')
	def test_should_show_account(self, mock_requests):
		mock_requests.get = mock_get
		elibom = ElibomClient('user@domain.com', 'password')
		account = elibom.show_account()
		self.assertEqual('test', account['name'], 'name must be equal to test')
		self.assertEqual(10.0, account['credits'], 'credits must be equal to 10.0')
		
	@patch('elibom.Client.requests')
	def test_should_show_user(self, mock_requests):
		mock_requests.get = mock_get
		elibom = ElibomClient('user@domain.com', 'password')
		user = elibom.show_user(1)
		self.assertEqual(1, user['id'], 'id must be equal to 1')
		self.assertEqual('testUser', user['name'], 'name must be equal to testUser')
		self.assertEqual('test@dominio.com', user['email'], 'email must be equal to test@dominio.com')
		self.assertEqual('active', user['status'], 'status must be equal to active')
	
	@patch('elibom.Client.requests')
	def test_should_show_users(self, mock_requests):
		mock_requests.get = mock_get
		elibom = ElibomClient('users@domain.com', 'password')
		users = elibom.show_users()
		self.assertEqual(2, len(users), 'users length must be equal to 2')
		self.assertEqual(1, users[0]['id'], 'id must be equal to 1')
		self.assertEqual('testUser', users[0]['name'], 'name must be equal to testUser')
		self.assertEqual('test@dominio.com', users[0]['email'], 'email must be equal to test@dominio.com')
		self.assertEqual('active', users[0]['status'], 'status must be equal to active')

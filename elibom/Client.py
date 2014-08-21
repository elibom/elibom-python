'''
Created on Aug 5, 2013

@author: Alejandro Riveros Cruz<lariverosc@gmail.com>
'''
import requests
import json
import re
from datetime import datetime


class ElibomClient(object):
	"""
	 Python Elibom API client
	"""
	__api_base_url = 'https://www.elibom.com/'
	__headers = {'X-API-Source': 'python-1.2'}
	
	def __init__(self, user, password):
		"""
		Attributes:
		 user: the user name
		 password: the user password or API token
		"""
		self.user = user
		self.password = password
		
		
	def send_message(self, destination, text):
		"""
		Method for send a message
		Attributes:
		 destination: one or more comma separated valid destination numbers,
					  valid destination are numbers of a least 10 digits,
					  contacts or groups in the form 'c#' or 'g#' respectively
					  where # corresponds to a valid id
		 text: the message text
		"""
		if not self.__is_valid_destination(destination):
			raise ElibomClientException('Invalid destination, cannot be None, and must be separated with commas')
		if not self.__is_valid_text(text):
			raise ElibomClientException('Invalid text, cannot be None, and must not be empty')
		
		payload = json.dumps({'destination':destination, 'text':text}) 
		response = requests.post(self.__api_base_url + 'messages', payload, auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			response_content = json.loads(response.content, encoding='utf-8')
			return response_content['deliveryToken']
		else:
			self.__manage_error_response(response)
	
	
	def schedule_message(self, destination, text, scheduled_date):
		"""
		Method for schedule a message send
		Attributes:
		 destination: one or more comma separated valid destination numbers
		 text: the message text
		 scheduled_date: the scheduled date
		"""
		if not self.__is_valid_destination(destination):
			raise ElibomClientException('Invalid destination, cannot be None, and must be composed of a least 10 digits.')
		if not self.__is_valid_text(text):
			raise ElibomClientException('Invalid text, cannot be None, and must not be empty')
		if not self.__is_valid_date(scheduled_date):
			raise ElibomClientException('Invalid schedule_date format, the format must be yyyy-mm-dd hh:mm')
		if not self.__is_schedule_on_range(scheduled_date):
			raise ElibomClientException('Invalid schedule_date cannot be in the past')
			
		payload = json.dumps({'destination':destination, 'text':text, 'scheduledDate':scheduled_date}) 
		response = requests.post(self.__api_base_url + 'messages', payload, auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			response_content = json.loads(response.content, encoding='utf-8')
			return response_content['scheduleId']
		else:
			self.__manage_error_response(response)

	
	def show_delivery(self, deliveryToken):
		"""
			Method used to query the delivery information.
			Attributes:
			 deliveryToken: the delivery identification token
		"""
		response = requests.get(self.__api_base_url + 'messages/' + str(deliveryToken), auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			return json.loads(response.content, encoding='utf-8')
		else:
			self.__manage_error_response(response)
	
	def show_schedule(self, scheduleId):
		"""
			Method used to query the details of a scheluded delivery
			Attributes:
		 	  scheduleId: the schedule identifier. 
		"""
		response = requests.get(self.__api_base_url + 'schedules/' + str(scheduleId), auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			return json.loads(response.content, encoding='utf-8')
		else:
			self.__manage_error_response(response)
	
	def list_schedules(self):
		"""
		Method used to list the available schedules.
		"""
		response = requests.get(self.__api_base_url + 'schedules/scheduled', auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			return json.loads(response.content, encoding='utf-8')
		else:
			self.__manage_error_response(response)
	
	
	def cancel_schedule(self, scheduleId):
		"""
		Method used to cancel an scheduled delivery.
		Attributes:
		   scheduleId: the schedule identifier.
		"""
		response = requests.delete(self.__api_base_url + 'schedules/' + str(scheduleId), auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			return scheduleId
		else:
			self.__manage_error_response(response)
	
	def show_account(self):
		"""
			Method used to query the account details.
		"""
		response = requests.get(self.__api_base_url + 'account',  auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			return json.loads(response.content, encoding='utf-8')
		else:
			self.__manage_error_response(response)
	
	def show_user(self, userId):
		"""
		  Method used to query the user details.
		  Attributes:
		 	  userId: the user identifier.
		"""
		response = requests.get(self.__api_base_url + 'users/' + str(userId), auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			return json.loads(response.content, encoding='utf-8')
		else:
			self.__manage_error_response(response)
	
	def show_users(self):
		"""
		  Method used to list the users associated to the current account.
		"""
		response = requests.get(self.__api_base_url + 'users', auth=(self.user, self.password),headers=self.__headers)
		if response.ok:
			return json.loads(response.content, encoding='utf-8')
		else:
			self.__manage_error_response(response)
			
	def __manage_error_response(self, response):
		if response.status_code == 400:
			raise ElibomClientException('Bad request: ' + response.reason)
		elif response.status_code == 401:
			raise ElibomClientException('Unauthorized, check your credentials')
		elif response.status_code == 404:
			raise ElibomClientException('Resource Not found')
		elif response.status_code >= 500:
			raise ElibomClientException('Server error, try later')
		else:
			raise ElibomClientException('Unknow error: ' + response.reason)
	
	def __is_valid_destination(self, destination):
		if destination is None:
			return False
		destination_splited = destination.split(',')
		for dest in destination_splited:
			dest = dest.strip()
			if not (re.match('(c|g)[0-9]+',dest) or re.match('[0-9]{10,}',dest)):
				return False
		return True
	
	def __is_valid_text(self, text):
		if text is None:
			return False
		if len(text.strip()) > 0:
			return True
		else:
			return False
		
	def __is_valid_date(self, date):
		try:
			datetime.strptime(date, '%Y-%m-%d %H:%M')
			return True
		except ValueError:
			return False
		
	def __is_schedule_on_range(self, date):
			now = datetime.now()
			if datetime.strptime(date, '%Y-%m-%d %H:%M') > now:
				return True
			else:
				return False	
	
	
class ElibomClientException(Exception):
	"""
	Exception raised for errors in the ElibomClient.
	Attributes:
		value  -- cause of the exception
	"""
	def __init__(self, value):
		self.value = value
		
	def __str__(self):
		return repr(self.value)
	
def prettyPrint(jsonObj):
	print json.dumps(jsonObj, sort_keys=True, indent=4, separators=(',', ': '))
		
if __name__ == '__main__':
	elibom = ElibomClient('XXX', 'XXX')
	# deliveryToken = elibom.send_message('57XXX', 'test message')
	deliveryToken = '5077137650034425759'
	delivery = elibom.show_delivery(deliveryToken);
	prettyPrint(delivery)  
	scheduleId = elibom.schedule_message('57XXX', 'test message', '2013-08-14 23:00')
	schedules = elibom.list_schedules()
	prettyPrint(schedules)
	elibom.cancel_schedule(scheduleId)
	account = elibom.show_account()
	prettyPrint(account)
	users = elibom.show_users()
	prettyPrint(users)
	user = elibom.show_user(users[0]['id'])
	prettyPrint(user)
	
		
				

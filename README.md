Elibom Python API Client
===========

A python client of the Elibom REST API. [The full API reference is here](http://www.elibom.com/developers/reference).


## Getting Started

1\. Install the egg

```python
python setup.py build
python setup.py install
```

2\. Configure the `ElibomClient` object passing your credentials.

```python
from elibom.Client import *

elibom = ElibomClient('your@user.com', 'your_api_password')
```
*Note*: You can find your api password at http://www.elibom.com/api-password (make sure you are logged in).

You are now ready to start calling the API methods!

## API methods

* [Send SMS](#send-sms)
* [Schedule SMS](#schedule-sms)
* [Show Delivery](#show-delivery)
* [List Scheduled SMS Messages](#list-scheduled-sms-messages)
* [Show Scheduled SMS Message](#show-scheduled-sms-message)
* [Cancel Scheduled SMS Message](#cancel-scheduled-sms-message)
* [List Users](#list-users)
* [Show User](#show-user)
* [Show Account](#show-account)

### Send SMS
```python
deliveryToken = elibom.send_message('573017897304', 'test message')
# all methods return a hash or raise exceptions if there is a error response
```

### Schedule SMS 
```python
scheduleId = elibom.schedule_message('573017897304', 'test message', '2013-08-14 23:00')
```

### Show Delivery
```python
delivery = elibom.show_delivery(deliveryToken);
```

### List Scheduled SMS Messages
```python
schedules = elibom.list_schedules()
```

### Cancel Scheduled SMS Message
```python
elibom.cancel_schedule(scheduleId)
```

### List Users
```python
users = elibom.show_users()
```

### Show User
```python
user = elibom.show_user(usersId)
```

### Show Account
```python
account = elibom.show_account()
```

### ISE
Python module to manage Cisco ISE via the REST API

#### Enable REST API
http://www.cisco.com/c/en/us/td/docs/security/ise/2-0/api_ref_guide/api_ref_book/ise_api_ref_ers1.html#pgfId-1079790
Need to add an ISE Administrator with the "ERS-Admin" or "ERS-Operator" group assignment is required to use the API.

#### Installation
```bash
mkdir path/to/ise
cd path/to/ise
git clone https://github.com/bobthebutcher/ise.git
```

#### Add to path
```python
import sys
sys.path.append('/path/to/ise/')
```

#### Usage
```python
from ise.cream import ERS
ise = ERS(ise_node='192.168.200.13', ers_user='user', ers_pass='pass', verify=False, disable_warnings=True)
```

#### Methods return a result dictionary
```python
{
    'success': True/False,
    'response': 'Response from request',
    'error': 'Error if any',
}
```

#### Testing
Testing has been completed on ISE v2.0

#### Get a list of identity groups
```python
ise.get_identity_groups()['response']

[('ALL_ACCOUNTS (default)',
  '10ac3e70-6d90-11e5-978e-005056bf2f0a',
  'Default ALL_ACCOUNTS (default) User Group'),
 ('Employee',
  '10a42820-6d90-11e5-978e-005056bf2f0a',
  'Default Employee User Group'),
 ...]
```

#### Get details about an identity group
```python
ise.get_identity_group(group='Employee')['response']

{'@xmlns:ns4': 'identity.ers.ise.cisco.com',
 'parent': 'NAC Group:NAC:IdentityGroups:User Identity Groups',
 '@xmlns:ers': 'ers.ise.cisco.com',
 'link': {'@href': 'https://192.168.200.13:9060/ers/config/identitygroup/10a42820-6d90-11e5-978e-005056bf2f0a',
  '@rel': 'self',
  '@type': 'application/xml'},
 '@xmlns:xs': 'http://www.w3.org/2001/XMLSchema',
 '@id': '10a42820-6d90-11e5-978e-005056bf2f0a',
 '@description': 'Default Employee User Group',
 '@name': 'Employee'}
```

#### Get details about an endpoint
```python
ise.get_endpoint_group(group='Android')['response']

{'systemDefined': 'true',
 'link': {'@href': 'https://192.168.200.13:9060/ers/config/endpointgroup/265079a0-6d8e-11e5-978e-005056bf2f0a',
  '@type': 'application/xml',
  '@rel': 'self'},
 '@id': '265079a0-6d8e-11e5-978e-005056bf2f0a',
 '@xmlns:ns4': 'identity.ers.ise.cisco.com',
 '@xmlns:xs': 'http://www.w3.org/2001/XMLSchema',
 '@description': 'Identity Group for Profile: Android',
 '@xmlns:ers': 'ers.ise.cisco.com',
 '@name': 'Android'}
```

#### Get endpoint identity groups
```python
ise.get_endpoint_groups()['response']

[('Android',
  '265079a0-6d8e-11e5-978e-005056bf2f0a',
  'Identity Group for Profile: Android'),
 ('Apple-iDevice',
  '32c8eb40-6d8e-11e5-978e-005056bf2f0a',
  'Identity Group for Profile: Apple-iDevice'),
  ...]
```

#### Get a list of internal users
```python
ise.get_users()['response']

[('Test2', '85fd1eb0-c6fa-11e5-b6b6-000c297b78b4')]
```

#### Get details about an internal user
```python
ise.get_user(user_id='Test2')['response']

{'enablePassword': '*******',
 'enabled': 'true',
 'changePassword': 'true',
 'password': '*******',
 'lastName': None,
 '@xmlns:xs': 'http://www.w3.org/2001/XMLSchema',
 '@description': '',
 'email': None,
 '@name': 'Test2',
 '@xmlns:ers': 'ers.ise.cisco.com',
 '@id': '85fd1eb0-c6fa-11e5-b6b6-000c297b78b4',
 '@xmlns:ns4': 'identity.ers.ise.cisco.com',
 'firstName': None,
 'customAttributes': None,
 'identityGroups': '10ac3e70-6d90-11e5-978e-005056bf2f0a',
 'link': {'@type': 'application/xml',
  '@href': 'https://192.168.200.13:9060/ers/config/internaluser/85fd1eb0-c6fa-11e5-b6b6-000c297b78b4',
  '@rel': 'self'}}
```

#### Add an internal user
```python
ise.add_user(user_id='Test1', password='Testing1', user_group_oid='10ac3e70-6d90-11e5-978e-005056bf2f0a')

{'success': True, 'response': 'Test1 Added Successfully', 'error': ''}
```

#### Delete an internal user
```python
ise.delete_user(user_id='Test1')

{'response': 'Test1 Deleted Successfully', 'error': '', 'success': True}
```

#### Get a list of devices
```python
ise.get_devices()['response']

[('TEST_R3', '3d52aca0-c5bc-11e5-a0ed-000c297b78b4'),
 ('TEST_R4', '2d80d6d0-c5bc-11e5-a0ed-000c297b78b4')]
```

#### Get details about a device
```python
ise.get_device(device='TEST_R3')['response']

{'@xmlns:ers': 'ers.ise.cisco.com',
 '@xmlns:ns4': 'network.ers.ise.cisco.com',
 'coaPort': '0',
 '@name': 'TEST_R3',
 'link': {'@type': 'application/xml',
  '@href': 'https://192.168.200.13:9060/ers/config/networkdevice/3d52aca0-c5bc-11e5-a0ed-000c297b78b4',
  '@rel': 'self'},
 '@id': '3d52aca0-c5bc-11e5-a0ed-000c297b78b4',
 'profileName': 'Cisco',
 'NetworkDeviceGroupList': {'NetworkDeviceGroup': ['TEST_NDG_TYPE#TEST_NDG',
   'Location#All Locations#TEST_LOC',
   'Device Type#All Device Types']},
 '@xmlns:xs': 'http://www.w3.org/2001/XMLSchema',
 'authenticationSettings': {'enableKeyWrap': 'false',
  'networkProtocol': 'RADIUS',
  'radiusSharedSecret': '******',
  'keyInputFormat': 'ASCII'},
 'NetworkDeviceIPList': {'NetworkDeviceIP': {'mask': '32',
   'ipaddress': '1.1.1.5'}},
 'snmpsettings': {'linkTrapQuery': 'true',
  'originatingPolicyServicesNode': 'Auto',
  'roCommunity': 'blah',
  'version': 'TWO_C',
  'macTrapQuery': 'true',
  'pollingInterval': '28800'}}
```

#### Get a list of device groups
```python
ise.get_device_groups()['response']

[('Device Type#All Device Types', 'dbf56650-6d8c-11e5-978e-005056bf2f0a'),
 ('Device Type#All Device Types#TEST_DEV_TYPE', '21be2c40-c4ee-11e5-a0ed-000c297b78b4'),
 ('Location#All Locations', 'db800f40-6d8c-11e5-978e-005056bf2f0a'),
 ('Location#All Locations#TEST_LOC', 'db804ce0-c4ed-11e5-a0ed-000c297b78b4'),
 ('TEST_NDG_TYPE#TEST_NDG', 'c33127e0-c4ed-11e5-a0ed-000c297b78b4')]
```

#### Add a device
```python
ise.add_device(name='TEST_R1', 
               ip_address='1.1.1.1', 
               radius_key='blah', 
               snmp_ro='blah', 
               dev_group='TEST_NDG_TYPE#TEST_NDG', 
               dev_location='Location#All Locations#TEST_LOC', 
               dev_type='Device Type#All Device Types')

{'response': 'TEST_R1 Added Successfully', 'success': True, 'error': ''}
```

#### Delete a device
```python
ise.delete_device(device='TEST_R1')['response']

{'response': 'TEST_R1 Deleted Successfully', 'error': '', 'success': True}
``` 
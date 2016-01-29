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
ise = ERS(ise_node='192.168.200.13', ers_user='user', ers_pass='pass', verify=False, disable_warnings=False)
```

#### Methods return a result dictionary
```python
{
    'success': True/False,
    'response': 'Response from request',
    'error': 'Error if any',
}
```

#### Get a list of identity groups
```python
ise.get_identity_groups()

{'response': [('ALL_ACCOUNTS (default)',
   '10ac3e70-6d90-11e5-978e-005056bf2f0a',
   'Default ALL_ACCOUNTS (default) User Group'),
  ('Employee',
   '10a42820-6d90-11e5-978e-005056bf2f0a',
   'Default Employee User Group'),
  ...],
 'success': True,
 'error': ''}
```

#### Get details about an identity group
```python
ise.get_identity_group('10ac3e70-6d90-11e5-978e-005056bf2f0a')

{'response': {'@xmlns:xs': 'http://www.w3.org/2001/XMLSchema',
  'link': {'@rel': 'self',
   '@href': 'https://192.168.200.13:9060/ers/config/identitygroup/10ac3e70-6d90-11e5-978e-005056bf2f0a',
   '@type': 'application/xml'},
  '@description': 'Default ALL_ACCOUNTS (default) User Group',
  'parent': 'NAC Group:NAC:IdentityGroups:User Identity Groups',
  '@id': '10ac3e70-6d90-11e5-978e-005056bf2f0a',
  '@name': 'ALL_ACCOUNTS (default)',
  '@xmlns:ns4': 'identity.ers.ise.cisco.com',
  '@xmlns:ers': 'ers.ise.cisco.com'},
 'success': True,
 'error': ''}
```

#### Get a list of devices
```python
ise.get_devices()

{'response': [('TEST_R3', '3d52aca0-c5bc-11e5-a0ed-000c297b78b4'),
  ('TEST_R4', '2d80d6d0-c5bc-11e5-a0ed-000c297b78b4')],
 'success': True,
 'error': ''}
```

### Add a device
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

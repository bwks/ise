### ISE
Python module to manage Cisco ISE via the REST API

#### Enable REST API
http://www.cisco.com/c/en/us/td/docs/security/ise/2-0/api_ref_guide/api_ref_book/ise_api_ref_ers1.html#pgfId-1079790
Need to add an ISE Administrator with the "ERS-Admin" or "ERS-Operator" group assignment is required to use the API.


#### Installation
```
mkdir path/to/ise
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

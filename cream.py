"""
Class to configure Cisco ISE via the ERS API

Required:
requests
 - http://docs.python-requests.org/en/latest/
xmltodict
 - https://github.com/martinblech/xmltodict

Version: 0.1.2
"""
import json
import os

import requests
import xmltodict

base_dir = os.path.dirname(__file__)


class ERS(object):
    def __init__(self, ise_node, ers_user, ers_pass, verify=False, disable_warnings=False, timeout=2):
        """
        Class to interact with Cisco ISE via the ERS API
        :param ise_node: IP Address of the primary admin ISE node
        :param ers_user: ERS username
        :param ers_pass: ERS password
        :param verify: Verify SSL cert
        :param disable_warnings: Disable requests warnings
        :param timeout: Query timeout
        """
        self.ise_node = ise_node
        self.user_name = ers_user
        self.user_pass = ers_pass

        self.url_base = 'https://{0}:9060/ers'.format(self.ise_node)
        self.ise = requests.session()
        self.ise.auth = (self.user_name, self.user_pass)
        self.ise.verify = verify  # http://docs.python-requests.org/en/latest/user/advanced/#ssl-cert-verification
        self.disable_warnings = disable_warnings
        self.timeout = timeout
        self.ise.headers.update({'Connection': 'keep_alive'})

        if self.disable_warnings:
            requests.packages.urllib3.disable_warnings()

    @staticmethod
    def _to_json(content):
        """
        ISE API uses xml, this method will convert the xml to json.
        Why? JSON when you can, XML when you must!
        :param content: xml to convert to json
        :return: json result
        """
        return json.loads(json.dumps(xmltodict.parse(content)))

    def get_identity_groups(self):
        """
        Get all identity groups
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.identity.identitygroup.1.0+xml'})

        resp = self.ise.get('{0}/config/identitygroup'.format(self.url_base))

        if resp.status_code == 200:
            result['success'] = True
            result['response'] = [(i['@name'], i['@id'], i['@description'])
                                  for i in ERS._to_json(resp.text)['ns3:searchResult']['resources']['resource']]
            return result
        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def get_identity_group(self, group):
        """
        Get identity group details
        :param group: Name of the identity group
        :return: result dictionary
        """
        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.identity.identitygroup.1.0+xml'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        resp = self.ise.get('{0}/config/identitygroup?filter=name.EQ.{1}'.format(self.url_base, group))
        found_group = ERS._to_json(resp.text)

        if found_group['ns3:searchResult']['@total'] == '1':
            resp = self.ise.get('{0}/config/identitygroup/{1}'.format(
                    self.url_base, found_group['ns3:searchResult']['resources']['resource']['@id']))
            if resp.status_code == 200:
                result['success'] = True
                result['response'] = ERS._to_json(resp.text)['ns4:identitygroup']
                return result
            elif resp.status_code == 404:
                result['response'] = 'Unknown Group'
                result['error'] = resp.status_code
                return result
            else:
                result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
                result['error'] = resp.status_code
                return result
        elif found_group['ns3:searchResult']['@total'] == '0':
            return '{0} not found'.format(group)
        else:
            result['response'] = 'Unknown error'
            result['error'] = resp.status_code
            return result

    def get_users(self):
        """
        Get all internal users
        :return: List of tuples of user details
        """
        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.identity.internaluser.1.1+xml'})

        resp = self.ise.get('{0}/config/internaluser'.format(self.url_base))

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        json_res = ERS._to_json(resp.text)['ns3:searchResult']

        if resp.status_code == 200 and int(json_res['@total']) > 1:
            result['success'] = True
            result['response'] = [(i['@name'], i['@id'])
                                  for i in json_res['resources']['resource']]
            return result

        elif resp.status_code == 200 and int(json_res['@total']) == 1:
            result['success'] = True
            result['response'] = [(json_res['resources']['resource']['@name'],
                                   json_res['resources']['resource']['@id'])]
            return result

        elif resp.status_code == 200 and int(json_res['@total']) == 0:
            result['success'] = True
            result['response'] = []
            return result

        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def get_user(self, user_id):
        """
        Get user detailed info
        :param user_id: User ID
        :return: result dictionary
        """
        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.identity.internaluser.1.0+xml'})

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        resp = self.ise.get('{0}/config/internaluser?filter=name.EQ.{1}'.format(self.url_base, user_id))
        found_user = ERS._to_json(resp.text)

        if found_user['ns3:searchResult']['@total'] == '1':
            resp = self.ise.get('{0}/config/internaluser/{1}'.format(
                    self.url_base, found_user['ns3:searchResult']['resources']['resource']['@id']))
            if resp.status_code == 200:
                result['success'] = True
                result['response'] = ERS._to_json(resp.text)['ns4:internaluser']
                return result
            elif resp.status_code == 404:
                result['response'] = 'Unknown User'
                result['error'] = resp.status_code
                return result
            else:
                result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
                result['error'] = resp.status_code
                return result
        elif found_user['ns3:searchResult']['@total'] == '0':
            return '{0} not found'.format(user_id)
        else:
            result['response'] = 'Unknown error'
            result['error'] = resp.status_code
            return result

    def add_user(self,
                 user_id,
                 password,
                 user_group_oid,
                 enable='',
                 first_name='',
                 last_name='',
                 email='',
                 description=''):
        """
        Add a user to the local user store
        :param user_id: User ID
        :param password: User password
        :param user_group_oid: OID of group to add user to
        :param enable: Enable password used for Tacacs
        :param first_name: First name
        :param last_name: Last name
        :param email: email address
        :param description: User description
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update({'Content-Type': 'application/vnd.com.cisco.ise.identity.internaluser.1.0+xml'})

        data = open(os.path.join(base_dir, 'xml/user_add.xml'), 'r').read().format(
                user_id, password, enable, first_name, last_name, email, description, user_group_oid)

        resp = self.ise.post('{0}/config/internaluser'.format(self.url_base), data=data, timeout=self.timeout)

        if resp.status_code == 201:
            result['success'] = True
            result['response'] = '{0} Added Successfully'.format(user_id)
            return result
        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def delete_user(self, user_oid):
        """
        Delete a user
        :param user_oid: User oid
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.identity.internaluser.1.0+xml'})

        resp = self.ise.delete('{0}/config/internaluser/{1}'.format(self.url_base, user_oid), timeout=self.timeout)

        if resp.status_code == 204:
            result['success'] = True
            result['response'] = '{0} Deleted Successfully'.format(user_oid)
            return result
        elif resp.status_code == 404:
            result['response'] = '{0} Unknown user'.format(user_oid)
            return result
        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def get_device_groups(self):
        """
        Get a list tuples of device groups
        :return:
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.network.networkdevicegroup.1.0+xml'})

        resp = self.ise.get('{0}/config/networkdevicegroup'.format(self.url_base))

        if resp.status_code == 200:
            result['success'] = True
            result['response'] = [(i['@name'], i['@id'])
                                  for i in ERS._to_json(resp.text)['ns3:searchResult']['resources']['resource']]
            return result
        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def get_device_group(self, device_group_oid):
        """
        Get a device group details
        :param device_group_oid: oid of the device group
        :return: result dictionary
        """
        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.network.networkdevicegroup.1.0+xml'})

        resp = self.ise.get('{0}/config/networkdevicegroup/{1}'.format(self.url_base, device_group_oid))

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        if resp.status_code == 200:
            result['success'] = True
            result['response'] = ERS._to_json(resp.text)['ns4:networkdevicegroup']
            return result
        elif resp.status_code == 404:
            result['response'] = 'Unknown User'
            result['error'] = resp.status_code
            return result
        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def get_devices(self):
        """
        Get a list of devices
        :return: result dictionary
        """
        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.network.networkdevice.1.0+xml'})

        resp = self.ise.get('{0}/config/networkdevice'.format(self.url_base))

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        json_res = ERS._to_json(resp.text)['ns3:searchResult']

        if resp.status_code == 200 and int(json_res['@total']) > 1:
            result['success'] = True
            result['response'] = [(i['@name'], i['@id'])
                                  for i in json_res['resources']['resource']]
            return result

        elif resp.status_code == 200 and int(json_res['@total']) == 1:
            result['success'] = True
            result['response'] = [(json_res['resources']['resource']['@name'],
                                   json_res['resources']['resource']['@id'])]
            return result

        elif resp.status_code == 200 and int(json_res['@total']) == 0:
            result['success'] = True
            result['response'] = []
            return result

        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def get_device(self, device_oid):
        """
        Get a device details
        :param device_oid: oid of the device
        :return: result dictionary
        """
        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.network.networkdevice.1.0+xml'})

        resp = self.ise.get('{0}/config/networkdevice/{1}'.format(self.url_base, device_oid))

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        if resp.status_code == 200:
            result['success'] = True
            result['response'] = ERS._to_json(resp.text)['ns4:networkdevice']
            return result
        elif resp.status_code == 404:
            result['response'] = 'Unknown User'
            result['error'] = resp.status_code
            return result
        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def add_device(self,
                   name,
                   ip_address,
                   radius_key,
                   snmp_ro,
                   dev_group,
                   dev_location,
                   dev_type,
                   description='',
                   dev_profile='Cisco'):
        """
        Add a device
        :param name: name of device
        :param ip_address: IP address of device
        :param radius_key: Radius shared secret
        :param snmp_ro: SNMP read only community string
        :param dev_group: Device group name
        :param dev_location: Device location
        :param dev_type: Device type
        :param description: Device description
        :param dev_profile: Device profile
        :return: Result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update({'Content-Type': 'application/vnd.com.cisco.ise.network.networkdevice.1.0+xml'})

        data = open(os.path.join(base_dir, 'xml/device_add.xml'), 'r').read().format(
            name, ip_address, radius_key, snmp_ro, dev_group, dev_location, dev_type, description, dev_profile
        )

        resp = self.ise.post('{0}/config/networkdevice'.format(self.url_base), data=data, timeout=self.timeout)

        if resp.status_code == 201:
            result['success'] = True
            result['response'] = '{0} Added Successfully'.format(name)
            return result
        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

    def delete_device(self, device_oid):
        """
        Delete a user
        :param device_oid: Device oid
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        self.ise.headers.update({'Accept': 'application/vnd.com.cisco.ise.network.networkdevice.1.0+xml'})

        resp = self.ise.delete('{0}/config/networkdevice/{1}'.format(self.url_base, device_oid), timeout=self.timeout)

        if resp.status_code == 204:
            result['success'] = True
            result['response'] = '{0} Deleted Successfully'.format(device_oid)
            return result
        elif resp.status_code == 404:
            result['response'] = '{0} Unknown device'.format(device_oid)
            return result
        else:
            result['response'] = ERS._to_json(resp.text)['ns3:ersResponse']['messages']['message']['title']
            result['error'] = resp.status_code
            return result

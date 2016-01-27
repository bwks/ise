"""
Class to configure Cisco ISE via the ERS API

Required:
requests
 - http://docs.python-requests.org/en/latest/
xmltodict
 - https://github.com/martinblech/xmltodict
"""
import json
import os
dir = os.path.dirname(__file__)

import requests
import xmltodict


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
        convert xml to json
        :param content: xml to convert to json
        :return: json result
        """
        return json.loads(json.dumps(xmltodict.parse(content)))

    def get_users(self):
        """
        Get all internal users
        :return: List of tuples of user details
        """
        self.ise.headers.update({
            'Accept': 'application/vnd.com.cisco.ise.identity.internaluser.1.1+xml',
            'Connection': 'keep_alive',
        })

        resp = self.ise.get('{0}/config/internaluser'.format(self.url_base))

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        if resp.status_code == 200:
            result['success'] = True
            result['response'] = [(i['@name'], i['@id'])
                                  for i in ERS._to_json(resp.text)['ns3:searchResult']['resources']['resource']]
            return result
        else:
            result['response'] = resp.text
            result['error'] = resp.status_code
            return result

    def get_user(self, user_oid):
        """
        Get an internal users details
        :param user_oid: oid of the user
        :return: result dictionary
        """
        self.ise.headers.update({
            'Accept': 'application/vnd.com.cisco.ise.identity.internaluser.1.1+xml',
            'Connection': 'keep_alive',
        })

        resp = self.ise.get('{0}/config/internaluser/{1}'.format(self.url_base, user_oid))

        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        if resp.status_code == 200:
            result['success'] = True
            result['response'] = ERS._to_json(resp.text)['ns4:internaluser']
            return result
        elif resp.status_code == 404:
            result['response'] = 'Unknown User'
            result['error'] = resp.status_code
            return result
        else:
            result['response'] = resp.text
            result['error'] = resp.status_code
            return result

    def add_user(self,
                 user_id,
                 password,
                 enable='',
                 first_name='',
                 last_name='',
                 email='',
                 description='',
                 user_group_oid=''):
        """
        Add a user to the local user store
        :param user_id: User ID
        :param password: User password
        :param enable: Enable password used for Tacacs
        :param first_name: First name
        :param last_name: Last name
        :param email: email address
        :param description: User description
        :param user_group_oid: OID of group to add user to
        :return: result dictionary
        """
        result = {
            'success': False,
            'response': '',
            'error': '',
        }

        headers = {'Content-Type': 'application/vnd.com.cisco.ise.identity.internaluser.1.1+xml; charset=utf-8'}

        data = open(os.path.join(dir, 'xml/user_add.xml'), 'r').read().format(
                user_id, password, enable, first_name, last_name, email, description, user_group_oid)

        url = '{0}/config/internaluser'.format(self.url_base)

        resp = self.ise.post(url, data=data, headers=headers, timeout=self.timeout)

        if resp.status_code == 201:
            result['success'] = True
            result['response'] = '{0} Added Successfully'.format(user_id)
            return result
        else:
            result['response'] = resp.text
            result['error'] = resp.status_code
            return result

"""
Class to configure Cisco ISE via the ERS API

Required:
requests
 - http://docs.python-requests.org/en/latest/
xmltodict
 - https://github.com/martinblech/xmltodict
"""

import json
import requests
import xmltodict


class ERS(object):

    def __init__(self, ise_node, user_name, user_pass, verify=False, disable_warnings=False, timeout=2):
        """

        :param ise_node:
        :param user_name:
        :param user_pass:
        :param verify:
        :param disable_warnings:
        :param timeout:
        :return:
        """
        self.ise_node = ise_node
        self.user_name = user_name
        self.user_pass = user_pass

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
        :param content:
        :return:
        """
        return json.loads(json.dumps(xmltodict.parse(content)))

    def get_users(self):

        self.ise.headers.update({
            'Accept': 'application/vnd.com.cisco.ise.identity.internaluser.1.1+xml',
            'Connection': 'keep_alive',
        })

        resp = self.ise.get('{0}/config/internaluser'.format(self.url_base))
        result = [(i['@name'], i['@id']) for i in ERS._to_json(resp.text)['ns3:searchResult']['resources']['resource']]
        return result



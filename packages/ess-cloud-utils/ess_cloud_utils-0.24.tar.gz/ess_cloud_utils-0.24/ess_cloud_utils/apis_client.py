#!/usr/bin/env python
import requests
from .eureka import Eureka


class ApisClient(object):
    session = requests.session()

    @staticmethod
    def get(service_name, endpoint, headers=None, timeout=None):
        base_url = Eureka.get_application_address(service_name)
        url = base_url + endpoint
        response = ApisClient.session.get(url, headers=headers, timeout=timeout)
        return response

    @staticmethod
    def post(service_name, endpoint, body=None, headers=None, json=None, files=None):
        base_url = Eureka.get_application_address(service_name)
        url = base_url + endpoint
        response = ApisClient.session.post(url, data=body, headers=headers, json=json, files=files)
        return response

    @staticmethod
    def put(service_name, endpoint, body=None, headers=None, json=None):
        base_url = Eureka.get_application_address(service_name)
        url = base_url + endpoint
        response = ApisClient.session.put(url, data=body, headers=headers, json=json)
        return response

    @staticmethod
    def delete(service_name, endpoint, body=None, headers=None, json=None):
        base_url = Eureka.get_application_address(service_name)
        url = base_url + endpoint
        response = ApisClient.session.delete(url, data=body, headers=headers, json=json)
        return response


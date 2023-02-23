#
#  Broadpeak 2023 demo script for Broadpeak.io
#  
#  Original author: Pierre Fosse
#
#  This script is provided for demo purpose
#

import sys
import requests
import json

class bpkio:

    def __init__(self):

        self.token = None
        self.endpoint = None
        self.headers = None
        self.session = None

    def __init__(self, token):

        self.token = token
        self.endpoint = "https://api.broadpeak.io/v1"
        self.headers = {
                        "accept": "application/json",
                        "content-type": "application/json",
                        "Authorization": "Bearer " + token
                    }

        self.session = requests.session()

    def log_request(self, name, response):
        print(f"---> Request {name}: {response.request.url} {response.request.body}")
        print(
            f"<--- Response {name} {len(response.content)} bytes in {round(response.elapsed.microseconds / 1000)} ms: "
            f"HTTP {response.status_code} {response.text}")

    def return_response(self, response):
        try:
            return json.loads(response.text)
        except ValueError as exception:
            print(f"Exception: {exception} : {sys.exc_info()}")
            return response.status_code

    def create_live_source(self, name_source, desc, source_url, bck_ip):
        url = self.endpoint + "/sources/live"

        if(bck_ip is None):
            payload = {
                "name": name_source,
                "description": desc,
                "url": source_url
            }
        else:
             payload = {
                "name": name_source,
                "description": desc,
                "url": source_url,
                "backupIp": bck_ip
            }           

        response = self.session.post(url, json=payload, headers=self.headers)
        self.log_request("create_live_source", response)
        return self.return_response(response)

    def create_asset_source(self, name_source, desc, source_url, bck_ip):
        url = self.endpoint + "/sources/asset"

        if(bck_ip is None):
            payload = {
                "name": name_source,
                "description": desc,
                "url": source_url
            }
        else:
             payload = {
                "name": name_source,
                "description": desc,
                "url": source_url,
                "backupIp": bck_ip
            }  

        response = self.session.post(url, json=payload, headers=self.headers)
        self.log_request("create_asset_source", response)
        return self.return_response(response)

    def create_virtual_channel(self, name_channel, env_tag, live_source_id):
        url = self.endpoint + "/services/virtual-channel/"

        payload = {
            "environmentTags": [
                env_tag
            ],
            "baseLive": {
                "id": live_source_id
            },
            "name": name_channel
        }

        response = self.session.post(url, json=payload, headers=self.headers)
        self.log_request("create_virtual_channel", response)
        return self.return_response(response)


    def create_slot(self, name_slot, service_id, start_time, duration, replacement_id):
        url = self.endpoint + "/services/virtual-channel/" + str(service_id) + "/slots"
        payload = {
            "replacement": {"id": replacement_id},
            "name": str(name_slot),
            "startTime": str(start_time),
            "duration": duration,
        }
        response = self.session.post(url, json=payload, headers=self.headers)
        self.log_request("create_slot", response)
        return self.return_response(response)


    def get_all_slots(self, service_id, limit=None, from_date=None, to_date=None):
        url = self.endpoint + "/services/virtual-channel/" + str(service_id) + "/slots"
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if from_date is not None:
            query_params["from"] = from_date
        if to_date is not None:
            query_params["to"] = to_date
        response = self.session.get(url, headers=self.headers, params=query_params)
        self.log_request("get_all_slots", response)
        return self.return_response(response)


    def delete_slot(self, service_id, slot_id):
        url = self.endpoint + "/services/virtual-channel/" + str(service_id) + "/slots/" + str(slot_id)
        response = self.session.delete(url, headers=self.headers)
        self.log_request("delete_slot", response)
        return self.return_response(response)


    def get_slot(self, service_id, slot_id):
        url = self.endpoint + "/services/virtual-channel/" + str(service_id) + "/slots/" + str(slot_id)
        response = self.session.get(url, headers=self.headers)
        self.log_request("get_slot", response)
        return self.return_response(response)


    def get_all_services(self, offset=None, limit=None):
        url = self.endpoint + "/services"
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if offset is not None:
            query_params["offset"] = offset
        response = self.session.get(url, headers=self.headers, params=query_params)
        self.log_request("get_all_services", response)
        return self.return_response(response)


    def get_all_sources(self, offset=None, limit=None):
        url = self.endpoint + "/sources"
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if offset is not None:
            query_params["offset"] = offset
        response = self.session.get(url, headers=self.headers, params=query_params)
        self.log_request("get_all_sources", response)
        return self.return_response(response)


    def get_source_status(self, type, source_url):
        url = self.endpoint + "/sources/" + type + "/check"
        query_params = {}
        if source_url is not None:
            query_params["url"] = source_url
        response = self.session.get(url, headers=self.headers, params=query_params)
        self.log_request("get_source_status", response)
        return self.return_response(response)


    def get_source_asset(self, asset_source_id):
        url = self.endpoint + "/sources/asset/" + str(asset_source_id)

        response = self.session.get(url, headers=self.headers)
        self.log_request("get_source_asset", response)
        return self.return_response(response)

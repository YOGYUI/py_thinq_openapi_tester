import json
import os.path
import random
import requests
from typing import List
from OpenSSL import crypto
import paho.mqtt.client as mqtt
from ThinqCommon import ThinqException


class ThinqAPI(object):
    def __init__(self):
        super().__init__()
        # todo: load config from here
        self._session: requests.sessions.Session = requests.Session()
        self._session.hooks['response'] = self.hook_func_response
        self._base_url: str = "https://api-kic.lgthinq.com"
        self._personal_access_token: str = ""
        self._client_id: str = "yogyui-thinq-api-tester"
        self._api_key: str = "v6GFvkweNo7DK7yD3ylIZ9w52aKBU0eJ7wLXkSR3"
        self._request_header: dict = {}
        self._generate_api_header()
        self._domain_names: dict = {
            "apiServer": "",
            "mqttServer": "",
            "webSocketServer": "",
        }
        self._query_domain_names()

        self._mqtt_client = mqtt.Client(client_id=self._client_id)
        self._mqtt_client.on_connect = self.onMqttClientConnect
        self._mqtt_client.on_disconnect = self.onMqttClientDisconnect
        self._mqtt_client.on_message = self.onMqttClientMessage
        self._mqtt_client.on_subscribe = self.onMqttClientSubscribe

    def release(self):
        if self._mqtt_client.is_connected():
            self._mqtt_client.loop_stop()
            self._mqtt_client.disconnect()
        self._session.close()

    def hook_func_response(self, response: requests.models.Response, *args, **kwargs):
        pass

    @staticmethod
    def _generate_random_string(length: int) -> str:
        characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
        result = ''
        for i in range(length):
            result += characters[random.randint(0, len(characters) - 1)]
        return result

    def _generate_api_header(self):
        self._request_header["Authorization"] = "Bearer " + self._personal_access_token
        self._request_header["x-message-id"] = self._generate_random_string(22)
        self._request_header["x-country"] = "KR"
        self._request_header["x-client-id"] = self._client_id
        self._request_header["x-api-key"] = self._api_key
        self._session.headers.update(self._request_header)

    def _query_domain_names(self, verbose: bool = False):
        url = self._base_url + "/route"
        response = self._session.get(url, headers={
            "x-message-id": self._generate_random_string(22),
            "x-country": "KR",
            "x-service-phase": "OP"
        })
        if not response.status_code == 200:
            raise ThinqException(f"[Domain Names] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO
        result = obj.get("response")
        self._domain_names["apiServer"] = result.get("apiServer")
        self._domain_names["mqttServer"] = result.get("mqttServer")
        self._domain_names["webSocketServer"] = result.get("webSocketServer")

    def query_device_list(self, verbose: bool = False) -> List[dict]:
        url = self._base_url + "/devices"
        response = self._session.get(url)
        if not response.status_code == 200:
            raise ThinqException(f"[Device List] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO
        dev_list = obj.get("response")
        result = list()
        for d in dev_list:
            try:
                dev_info = d.get("deviceInfo")
                result.append({
                    "deviceType": dev_info.get("deviceType"),
                    "deviceId": d.get("deviceId"),
                    "modelName": dev_info.get("modelName"),
                    "alias": dev_info.get("alias"),
                    "reportable": dev_info.get("reportable"),
                })
            except Exception as e:
                raise ThinqException(f"Failed to query device list ({e})")
        return result

    def query_device_profile(self, device_id: str, verbose: bool = False) -> dict:
        url = self._base_url + f"/devices/{device_id}/profile"
        response = self._session.get(url)
        if not response.status_code == 200:
            raise ThinqException(f"[Device Profile] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO
        return obj.get("response")

    def query_device_state(self, device_id: str, verbose: bool = False) -> dict:
        url = self._base_url + f"/devices/{device_id}/state"
        response = self._session.get(url)
        if not response.status_code == 200:
            raise ThinqException(f"[Device State] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO
        return obj.get("response")

    def query_device_push_subscription_list(self, verbose: bool = False) -> List[str]:
        url = self._base_url + f"/push"
        response = self._session.get(url)
        if not response.status_code == 200:
            raise ThinqException(f"[Push List] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO
        dev_id_list = list()
        for elem in obj.get('response'):
            dev_id_list.append(elem.get('deviceId'))
        return dev_id_list

    def subscribe_device_push(self, device_id: str, verbose: bool = False):
        url = self._base_url + f"/push/{device_id}/subscribe"
        response = self._session.post(url)
        if not response.status_code == 200:
            raise ThinqException(f"[Subscribe Push] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO

    def unsubscribe_device_push(self, device_id: str, verbose: bool = False):
        url = self._base_url + f"/push/{device_id}/unsubscribe"
        response = self._session.delete(url)
        if not response.status_code == 200:
            raise ThinqException(f"[Unsubscribe Push] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO

    def query_device_event_subscription_list(self, verbose: bool = False) -> List[str]:
        url = self._base_url + f"/event"
        response = self._session.get(url)
        if not response.status_code == 200:
            raise ThinqException(f"[Event List] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO
        dev_id_list = list()
        for elem in obj.get('response'):
            dev_id_list.append(elem.get('deviceId'))
        return dev_id_list

    def subscribe_device_event(self, device_id: str, expire_hour: int = 1, verbose: bool = False):
        url = self._base_url + f"/event/{device_id}/subscribe"
        payload = {
            "expire": {
                "unit": "HOUR",
                "timer": max(1, min(24, expire_hour))
            }
        }
        response = self._session.post(url, json=payload)
        if not response.status_code == 200:
            raise ThinqException(f"[Subscribe Event] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO

    def unsubscribe_device_event(self, device_id: str, verbose: bool = False):
        url = self._base_url + f"/event/{device_id}/unsubscribe"
        response = self._session.delete(url)
        if not response.status_code == 200:
            raise ThinqException(f"[Unsubscribe Event] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO

    @staticmethod
    def _generate_csr():
        csr_pem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csr.pem")
        if not os.path.isfile(csr_pem_path):
            keypair = crypto.PKey()
            keypair.generate_key(crypto.TYPE_RSA, 2048)
            req = crypto.X509Req()
            req.get_subject().CN = "AWS IoT Certificate"
            req.get_subject().O = "Amazon"
            req.set_pubkey(keypair)
            req.sign(keypair, "sha256")
            csr = crypto.dump_certificate_request(crypto.FILETYPE_PEM, req).decode(encoding='utf-8')
            with open(csr_pem_path, 'w') as fp:
                fp.write(csr)

    def issue_client_certificate(self, verbose: bool = False):
        url = self._base_url + f"/client/certificate"
        self._generate_csr()
        csr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csr.pem")
        if not os.path.isfile(csr_path):
            raise ThinqException(f"[Issue Certificate] Request certificate file is not exist")
        with open(csr_path, 'r') as fp:
            csr = fp.read()
        payload = {
            "body": {
                "service-code": "SVC202",
                "csr": csr
            }
        }
        response = self._session.post(url, json=payload)
        if not response.status_code == 200:
            raise ThinqException(f"[Issue Certificate] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO
        obj_response = obj.get('response')
        resultCode = obj_response.get('resultCode')
        obj_result = obj_response.get('result')
        certificatePem = obj_result.get('certificatePem')
        subscriptions = obj_result.get('subscriptions')
        publications = obj_result.get('publications')
        print(certificatePem)
        print(subscriptions)
        print(publications)

    def register_client(self, verbose: bool = False):
        url = self._base_url + f"/client"
        payload = {
            "body": {
                "type": "MQTT",
                "service-code": "SVC202",
                "device-type": "607"
            }
        }
        response = self._session.post(url, json=payload)
        if not response.status_code == 200:
            raise ThinqException(f"[Register Client] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO

    def unregister_client(self, verbose: bool = False):
        url = self._base_url + f"/client"
        payload = {
            "body": {
                "type": "MQTT",
                "service-code": "SVC202"
            }
        }
        response = self._session.delete(url, json=payload)
        if not response.status_code == 200:
            raise ThinqException(f"[Unregister Client] Request Failed({response.status_code}): {response.reason}")
        obj = json.loads(response.content.decode())
        if verbose:
            message_id = obj.get("messageId")
            timestamp = obj.get("timestamp")
            pass  # TODO

    def _connect_mqtt_broker(self):
        pass

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, url: str):
        self._base_url = url

    @property
    def personal_access_token(self) -> str:
        return self._personal_access_token

    @personal_access_token.setter
    def personal_access_token(self, token: str):
        self._personal_access_token = token
        self._generate_api_header()

    @property
    def client_id(self) -> str:
        return self._client_id

    @client_id.setter
    def client_id(self, client_id: str):
        self._client_id = client_id
        self._generate_api_header()

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, key: str):
        self._api_key = key
        self._generate_api_header()

    @property
    def request_header(self) -> dict:
        return self._request_header

    @property
    def domain_names(self) -> dict:
        return self._domain_names

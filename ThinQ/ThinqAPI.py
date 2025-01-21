import json
import os.path
import random
import requests
from typing import List
from OpenSSL import crypto
import paho.mqtt.client as mqtt
from ThinqCommon import ThinqException


class ThinqAPI(object):
    def __init__(self, config_file_path: str = None):
        super().__init__()
        self._config_file_path: str = config_file_path if config_file_path is not None else (
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json"))

        self._config: dict = {
            "personal_access_token": "",
            "client_id": "yogyui-thinq-api-tester",
            "api_key": "v6GFvkweNo7DK7yD3ylIZ9w52aKBU0eJ7wLXkSR3"
        }
        self._request_header: dict = {}
        self._session: requests.sessions.Session = requests.Session()
        self._session.hooks['response'] = self.hook_func_response
        self._base_url: str = "https://api-kic.lgthinq.com"
        self._generate_api_header()
        self._domain_names: dict = {
            "apiServer": "",
            "mqttServer": "",
            "webSocketServer": "",
        }

        self._mqtt_client = mqtt.Client(client_id=self.client_id)
        self._mqtt_client.on_connect = self._on_mqtt_client_connect
        self._mqtt_client.on_disconnect = self._on_mqtt_client_disconnect
        self._mqtt_client.on_subscribe = self._on_mqtt_client_subscribe
        self._mqtt_client.on_message = self._on_mqtt_client_message
        self._mqtt_topic_subscriptions: List[str] = list()
        self._mqtt_topic_publications: List[str] = list()

        self._load_config()
        self._query_domain_names()

    def release(self):
        self.disconnect_mqtt_broker()
        self._session.close()

    def _load_config(self):
        if not os.path.isfile(self._config_file_path):
            self._save_config()
        with open(self._config_file_path, 'r') as fp:
            load_obj = json.load(fp)
        if isinstance(load_obj, dict):
            self.personal_access_token = load_obj.get("personal_access_token", "")
            self.client_id = load_obj.get("client_id", "yogyui-thinq-api-tester")
            self.api_key = load_obj.get("api_key", "v6GFvkweNo7DK7yD3ylIZ9w52aKBU0eJ7wLXkSR3")

    def _save_config(self):
        if os.path.isfile(self._config_file_path):
            with open(self._config_file_path, 'r') as fp:
                save_obj = json.load(fp)
        else:
            save_obj = dict()
        save_obj.update(self._config)
        with open(self._config_file_path, 'w') as fp:
            json.dump(save_obj, fp, indent=4)

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
        self._request_header["Authorization"] = "Bearer " + self.personal_access_token
        self._request_header["x-message-id"] = self._generate_random_string(22)
        self._request_header["x-country"] = "KR"
        self._request_header["x-client-id"] = self.client_id
        self._request_header["x-api-key"] = self.api_key
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
        privkey_pem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "privkey.pem")
        if not os.path.isfile(csr_pem_path):
            keypair = crypto.PKey()
            keypair.generate_key(crypto.TYPE_RSA, 2048)
            privkey_pem = crypto.dump_privatekey(crypto.FILETYPE_PEM, keypair).decode(encoding='utf-8')
            with open(privkey_pem_path, 'w') as fp:
                fp.write(privkey_pem)
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
        cert_pem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aws_cert.pem')
        with open(cert_pem_path, 'w') as fp:
            fp.write(certificatePem)
        self._get_aws_root_ca_certificate()
        self._mqtt_topic_subscriptions.clear()
        self._mqtt_topic_subscriptions.extend(subscriptions)
        self._mqtt_topic_publications.clear()
        self._mqtt_topic_publications.extend(publications)

    @staticmethod
    def _get_aws_root_ca_certificate():
        rootca_pem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aws_root_ca.pem')
        if not os.path.isfile(rootca_pem_path):
            url = 'https://www.amazontrust.com/repository/AmazonRootCA1.pem'
            res = requests.get(url)
            if not res.status_code == 200:
                raise ThinqException(f"[AWS Root CA Cert]Request Failed ({res.status_code}): {res.reason}, {res.text}")
            rootca_pem = res.text
            with open(rootca_pem_path, 'w') as fp:
                fp.write(rootca_pem)

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

    def connect_mqtt_broker(self):
        rootca_pem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'aws_root_ca.pem')
        privkey_pem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "privkey.pem")
        csr_pem_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csr.pem")
        self._mqtt_client.tls_set(ca_certs=rootca_pem_path, certfile=csr_pem_path, keyfile=privkey_pem_path)

    def disconnect_mqtt_broker(self):
        if self._mqtt_client.is_connected():
            self._mqtt_client.loop_stop()
            self._mqtt_client.disconnect()

    def _on_mqtt_client_connect(self, _, userdata, flags, rc):
        pass

    def _on_mqtt_client_disconnect(self, _, userdata, rc):
        pass

    def _on_mqtt_client_subscribe(self, _, userdata, mid, granted_qos):
        pass

    def _on_mqtt_client_message(self, _, userdata, message):
        pass

    @property
    def base_url(self) -> str:
        return self._base_url

    @base_url.setter
    def base_url(self, url: str):
        self._base_url = url

    @property
    def personal_access_token(self) -> str:
        return self._config.get("personal_access_token")

    @personal_access_token.setter
    def personal_access_token(self, token: str):
        self._config["personal_access_token"] = token
        self._generate_api_header()

    @property
    def client_id(self) -> str:
        return self._config.get("client_id")

    @client_id.setter
    def client_id(self, client_id: str):
        self._config["client_id"] = client_id
        self._generate_api_header()

    @property
    def api_key(self) -> str:
        return self._config.get("api_key")

    @api_key.setter
    def api_key(self, key: str):
        self._config["api_key"] = key
        self._generate_api_header()

    @property
    def request_header(self) -> dict:
        return self._request_header

    @property
    def domain_names(self) -> dict:
        return self._domain_names

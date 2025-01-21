import os
import json
from typing import List, Union
from ThinqAPI import ThinqAPI
from ThinqDevice import ThinqDevice, createThinqDevice
from ThinqCommon import Callback


class ThinqCore(object):
    def __init__(self):
        super().__init__()
        self._config_file_path: str = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
        self._api = ThinqAPI(self._config_file_path)
        self._load_config()
        self._device_list: List[ThinqDevice] = list()
        self.sig_device_list_changed = Callback()
        self.initialize()

    def initialize(self):
        pass

    def release(self):
        self._api.release()
        self._save_config()

    def _load_config(self):
        pass

    def _save_config(self):
        pass

    def set_api_personal_access_token(self, token: str):
        self._api.personal_access_token = token
        self._save_config()

    def _find_device_by_id(self, device_id: str) -> Union[ThinqDevice, None]:
        find = list(filter(lambda x: x.id == device_id, self._device_list))
        if len(find) == 1:
            return find[0]
        return None

    def query_device_list(self):
        self._device_list.clear()
        dev_info_list = self._api.query_device_list()
        for info in dev_info_list:
            device = createThinqDevice(
                info.get('deviceType'),
                info.get('deviceId'),
                info.get('modelName'),
                info.get('alias'),
                info.get('reportable'),
                self._api
            )
            self._device_list.append(device)
        self.sig_device_list_changed.emit()

    def query_device_push_subscription_list(self) -> List[ThinqDevice]:
        dev_id_list = self._api.query_device_push_subscription_list()
        result = list()
        for dev_id in dev_id_list:
            dev = self._find_device_by_id(dev_id)
            if dev is not None:
                result.append(dev)
        return result

    def query_device_event_subscription_list(self) -> List[ThinqDevice]:
        dev_id_list = self._api.query_device_event_subscription_list()
        result = list()
        for dev_id in dev_id_list:
            dev = self._find_device_by_id(dev_id)
            if dev is not None:
                result.append(dev)
        return result

    def issue_client_certificate(self):
        self._api.issue_client_certificate()

    def register_client(self):
        self._api.register_client()

    def unregister_client(self):
        self._api.unregister_client()

    def connect_mqtt_broker(self):
        self._api.connect_mqtt_broker()

    def disconnect_mqtt_broker(self):
        self._api.disconnect_mqtt_broker()

    @property
    def device_list(self) -> List[ThinqDevice]:
        return self._device_list


if __name__ == '__main__':
    # test codes
    core_ = ThinqCore()
    core_.unregister_client()
    core_.register_client()
    core_.issue_client_certificate()
    core_.connect_mqtt_broker()
    import time
    time.sleep(5)
    core_.disconnect_mqtt_broker()
    """
    core_.query_device_list()
    
    core_.device_list[0].subscribe_push()
    core_.query_device_push_subscription_list()
    core_.device_list[0].unsubscribe_push()
    core_.query_device_push_subscription_list()
    
    # core_.device_list[0].subscribe_event()
    for dev in core_.device_list:
        dev.subscribe_event()
    print(core_.query_device_event_subscription_list())
    # core_.device_list[0].unsubscribe_event()
    # print(core_.query_device_event_subscription_list())
    """

    core_.release()

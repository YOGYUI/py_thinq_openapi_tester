from abc import abstractmethod
from typing import Union, List, Tuple
from enum import IntEnum, unique, auto
from ThinqAPI import ThinqAPI
from ThinqCommon import ThinqException


@unique
class DeviceType(IntEnum):
    REFRIGERATOR = auto()  # 냉장고
    WASHER = auto()  # 세탁기
    DRYER = auto()  # 건조기
    AIR_CONDITIONER = auto()  # 에어컨
    AIR_PURIFIER = auto()  # 공기청정기
    ROBOT_CLEANER = auto()  # 로봇청소기
    OVEN = auto()  # 오븐
    DISH_WASHER = auto()  # 식기세척기
    STYLER = auto()  # 스타일러
    WATER_PURIFIER = auto()  # 정수기
    DEHUMIDIFIER = auto()  # 제습기
    CEILING_FAN = auto()  # 실링팬
    WINE_CELLAR = auto()  # 와인셀러
    KIMCHI_REFRIGERATOR = auto()  # 김치냉장고
    HOME_BREW = auto()  # 홈브루
    PLANT_CULTIVATOR = auto()  # 식물재배기
    WASHTOWER_WASHER = auto()  # 워시타워(세탁기)
    WASHTOWER_DRYER = auto()  # 워시타워(건조기)
    WASHTOWER = auto()  # 워시타워
    COOKTOP = auto()  # 쿡탑
    HOOD = auto()  # 후드
    MICROWAVE_OVEN = auto()  # 전자레인지
    SYSTEM_BOILER = auto()  # 시스템 보일러
    AIR_PURIFIER_FAN = auto()  # 공기청정팬
    STICK_CLEANER = auto()  # 스틱청소기
    WATER_HEATER = auto()  # 온수기
    WASHCOMBO_MAIN = auto()  # 워시콤보 (메인)
    WASHCOMBO_MINI = auto()  # 워시콤보 (미니)
    HUMIDIFIER = auto()  # 가습기


class DeviceProperty(object):
    name: str = ""
    type: str = ""
    mode: str = ""
    value: object = None

    def __repr__(self) -> str:
        return ""


class DeviceProfile(object):
    def __init__(self):
        super().__init__()
        self.notification_pushes: List[Tuple[str, str]] = list()
        self.properties: List[DeviceProperty] = list()
        self.errors: List[Tuple[str, str]] = list()

    def __repr__(self) -> str:
        return ""


class ThinqDevice(object):
    def __init__(
            self, dev_id: str, dev_type: DeviceType, model_name: str, alias: str, reportable: bool, api: ThinqAPI
    ):
        super().__init__()
        self._id: str = dev_id
        self._type: DeviceType = dev_type
        self._model_name: str = model_name
        self._alias: str = alias
        self._reportable: bool = reportable
        self._api: ThinqAPI = api

        self._profile: DeviceProfile = DeviceProfile()
        self._initialize_profile_schema()
        # print(f'{self} Created')  # TODO
        # self.query_profile()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}::{self._type.name}::{self._model_name}::{self._alias}>"

    @abstractmethod
    def _initialize_profile_schema(self):
        pass

    def query_profile(self, verbose: bool = False):
        result = self._api.query_device_profile(self._id, verbose)
        """
        print(result.get('notification'))
        print(result.get('property'))

        error = result.get('error', [])
        self._profile.errors.clear()
        self._profile.errors.extend(error)
        """

    def query_state(self, verbose: bool = False):
        result = self._api.query_device_state(self._id, verbose)

    def subscribe_push(self, verbose: bool = False):
        result = self._api.subscribe_device_push(self._id, verbose)

    def unsubscribe_push(self, verbose: bool = False):
        result = self._api.unsubscribe_device_push(self._id, verbose)

    def subscribe_event(self, verbose: bool = False):
        result = self._api.subscribe_device_event(self._id, verbose)

    def unsubscribe_event(self, verbose: bool = False):
        result = self._api.unsubscribe_device_event(self._id, verbose)

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> DeviceType:
        return self._type

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def reportable(self) -> bool:
        return self._reportable

    @property
    def alias(self) -> str:
        return self._alias

    @property
    def property(self) -> DeviceProfile:
        return self._profile


class ThinqDeviceRefrigerator(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.REFRIGERATOR, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        self._profile.notification_pushes.extend([
            ("FROZEN_IS_COMPLETE", "냉동이 완료되었습니다."),
            ("DOOR_IS_OPEN", "문이 열렸습니다."),
            ("TIME_TO_CHANGE_FILTER", "필터 교체 시기입니다."),
            ("TIME_TO_CHANGE_WATER_FILTER", "정수 필터 교체 시기입니다.")
        ])


class ThinqDeviceWasher(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WASHER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceDryer(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.DRYER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceAirConditioner(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.AIR_CONDITIONER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceAirPurifier(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.AIR_PURIFIER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceRobotCleaner(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.ROBOT_CLEANER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceOven(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.OVEN, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceDishWasher(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.DISH_WASHER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceStyler(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.STYLER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceWaterPurifier(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WATER_PURIFIER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceDehumidifier(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.DEHUMIDIFIER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceCeilingFan(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.CEILING_FAN, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceWineCellar(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WINE_CELLAR, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceKimchiRefrigerator(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.KIMCHI_REFRIGERATOR, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceHomeBrew(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.HOME_BREW, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDevicePlantCultivator(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.PLANT_CULTIVATOR, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceWashtowerWasher(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WASHTOWER_WASHER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceWashtowerDryer(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WASHTOWER_DRYER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceWashtower(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WASHTOWER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceCooktop(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.COOKTOP, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceHood(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.HOOD, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceMicrowaveOven(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.MICROWAVE_OVEN, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceSystemBoiler(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.SYSTEM_BOILER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceAirPurifierFan(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.AIR_PURIFIER_FAN, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceStickCleaner(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.STICK_CLEANER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceWaterHeater(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WATER_HEATER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceWashcomboMain(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WASHCOMBO_MAIN, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceWashcomboMini(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.WASHCOMBO_MINI, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


class ThinqDeviceHumidifier(ThinqDevice):
    def __init__(self, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI):
        super().__init__(dev_id, DeviceType.HUMIDIFIER, model_name, alias, reportable, api)

    def _initialize_profile_schema(self):
        pass


def createThinqDevice(
        device_type_str: str, dev_id: str, model_name: str, alias: str, reportable: bool, api: ThinqAPI
) -> ThinqDevice:
    if device_type_str == "DEVICE_REFRIGERATOR":
        return ThinqDeviceRefrigerator(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WASHER":
        return ThinqDeviceWasher(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_DRYER":
        return ThinqDeviceDryer(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_AIR_CONDITIONER":
        return ThinqDeviceAirConditioner(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_AIR_PURIFIER":
        return ThinqDeviceAirPurifier(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_ROBOT_CLEANER":
        return ThinqDeviceRobotCleaner(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_OVEN":
        return ThinqDeviceOven(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_DISH_WASHER":
        return ThinqDeviceDishWasher(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_STYLER":
        return ThinqDeviceStyler(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WATER_PURIFIER":
        return ThinqDeviceWaterPurifier(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_DEHUMIDIFIER":
        return ThinqDeviceDehumidifier(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_CEILING_FAN":
        return ThinqDeviceCeilingFan(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WINE_CELLAR":
        return ThinqDeviceWineCellar(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_KIMCHI_REFRIGERATOR":
        return ThinqDeviceKimchiRefrigerator(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_HOME_BREW":
        return ThinqDeviceHomeBrew(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_PLANT_CULTIVATOR":
        return ThinqDevicePlantCultivator(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WASHTOWER_WASHER":
        return ThinqDeviceWashtowerWasher(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WASHTOWER_DRYER":
        return ThinqDeviceWashtowerDryer(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WASHTOWER":
        return ThinqDeviceWashtower(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_COOKTOP":
        return ThinqDeviceCooktop(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_HOOD":
        return ThinqDeviceHood(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_MICROWAVE_OVEN":
        return ThinqDeviceMicrowaveOven(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_SYSTEM_BOILER":
        return ThinqDeviceSystemBoiler(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_AIR_PURIFIER_FAN":
        return ThinqDeviceAirPurifierFan(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_STICK_CLEANER":
        return ThinqDeviceStickCleaner(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WATER_HEATER":
        return ThinqDeviceWaterHeater(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WASHCOMBO_MAIN":
        return ThinqDeviceWashcomboMain(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_WASHCOMBO_MINI":
        return ThinqDeviceWashcomboMini(dev_id, model_name, alias, reportable, api)
    elif device_type_str == "DEVICE_HUMIDIFIER":
        return ThinqDeviceDehumidifier(dev_id, model_name, alias, reportable, api)
    else:
        raise ThinqException(f"Invalid device type name: {device_type_str}")

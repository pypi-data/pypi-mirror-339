from dataclasses import dataclass, field
from enum import auto
from typing import Optional, Dict, List, Union

from coiote.utils import AutoNamedEnum


@dataclass
class DeviceDirectGroupData:
    manufacturer: str
    model: str
    version: Optional[str] = None


@dataclass
class DeviceDirectGroup:
    DeviceDirectGroup: DeviceDirectGroupData

    @staticmethod
    def create(manufacturer: str, model: str, version: Optional[str] = None):
        return DeviceDirectGroup(DeviceDirectGroupData(manufacturer, model, version))


@dataclass
class RawDirectGroupData:
    value: str


@dataclass
class RawDirectGroup:
    RawDirectGroup: RawDirectGroupData

    @staticmethod
    def create(group: str):
        return RawDirectGroup(RawDirectGroupData(group))


ResourceGroup = Union[DeviceDirectGroup, RawDirectGroup]


@dataclass
class InternalLocationData:
    fileName: str
    staticContent: bool = False


@dataclass
class ExternalLocationData:
    fileUrl: str
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class InternalLocation:
    InternalLocation: InternalLocationData

    @staticmethod
    def create(file: str, static: bool):
        return InternalLocation(InternalLocationData(file, static))


@dataclass
class ExternalLocation:
    ExternalLocation: ExternalLocationData


class ResourceCategory(AutoNamedEnum):
    FIRMWARE = auto()
    SOFTWARE = auto()
    UNKNOWN = auto()
    IMAGE = auto()


class ResourceExpirationTime(AutoNamedEnum):
    ONE_DAY = auto()
    ONE_WEEK = auto()
    ONE_MONTH = auto()
    FOREVER = auto()


class DownloadProtocol(AutoNamedEnum):
    HTTP = auto()
    HTTPS = auto()
    COAP = auto()
    COAPS = auto()
    COAP_TCP = auto()
    COAP_TLS = auto()


@dataclass
class DownloadOptions:
    protocol: DownloadProtocol


@dataclass
class ResourceDownloadData:
    address: str


@dataclass
class Resource:
    name: str
    domain: str
    location: Union[InternalLocation, ExternalLocation]
    category: ResourceCategory
    expirationTime: ResourceExpirationTime
    visibleForSubtenants: bool = False
    description: Optional[str] = None
    id: Optional[str] = None
    device: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    directGroups: List[ResourceGroup] = field(default_factory=list)


@dataclass
class FileData:
    pass


@dataclass
class Base64FileData(FileData):
    data: str

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, TypedDict, Literal

MessageType = Literal[
    "text", "file", "attachment", "banner", "message_edit", "transient_message"
]
ButtonType = Literal["+", "-"]
OrganizationType = Literal["company", "network"]
ChatType = Literal[
    "channel",
    "bot",
    "dm",
    "chat",
    "crossproduct_custom_chat",
    "entity_chat",
    "guests",
    "threads",
    "thread",
]
ChannelOperation = Literal[
    "added",
    "removed",
    "message_sent",
    "message_edited",
    "message_deleted",
    "auto_followed_thread",
    "added_in_thread",
    "removed_from_thread",
    "thread_closed",
    "thread_reopened",
]
BotAlertOperation = Literal[
    "default_state",
    "busy",
    "ringing",
    "answered",
    "ended",
    "declined",
    "missed",
    "offline",
]


@dataclass
class Organization:
    type: OrganizationType
    id: int


@dataclass
class Access:
    zoho_user_id: int
    user_id: int
    user_agent: str
    chat_id: str
    organization: Organization
    message_id: str
    platform_version: Optional[str]
    parent_chat_id: Optional[str]


@dataclass
class AppInfo:
    current_version: str
    existing_version: str
    type: Literal["install", "upgrade"]


@dataclass
class Attachment:
    name: str
    comment: str
    id: str
    url: str
    contenttype: str


@dataclass
class BotDetails:
    name: str
    image: str


@dataclass
class MessageStyles:
    highlight: bool


@dataclass
class ActionData:
    name: Optional[str]
    owner: Optional[str]
    web: Optional[str]
    windows: Optional[str]
    # pylint: disable=invalid-name
    iOS: Optional[str]
    android: Optional[str]
    api: Optional[str]


@dataclass
class Confirm:
    title: Optional[str]
    description: Optional[str]
    input: Optional[str]
    button_text: Optional[str]


@dataclass
class Action:
    type: Optional[str]
    data: Optional[ActionData]
    confirm: Optional[Confirm]


@dataclass
class ButtonObject:
    id: Optional[str]
    button_id: Optional[str]
    label: Optional[str]
    name: Optional[str]
    hint: Optional[str]
    type: Optional[ButtonType]
    key: Optional[str]
    action: Optional[Action]
    url: Optional[str]


@dataclass
class Button:
    type: Literal["button"]
    object: ButtonObject

    def __init__(self, button: ButtonObject):
        self.object = button


@dataclass
class ButtonArguments:
    key: str


@dataclass
class Member:
    id: str
    first_name: str
    last_name: str
    email: str
    status: str


@dataclass
class Sender:
    name: str
    id: str


@dataclass
class RecentMessage:
    sender: Sender
    time: int
    text: str
    id: str
    type: str


@dataclass
class Chat:
    owner: int
    id: str
    type: str
    title: str
    members: List[Member]
    recent_messages: List[RecentMessage]
    channel_unique_name: str
    chat_type: ChatType
    channel_id: str
    entity_id: str


@dataclass
class Dimension:
    size: int
    width: int
    height: int


@dataclass
class FileContent:
    name: str
    id: str
    type: str
    dimensions: Dimension


@dataclass
class Thumbnail:
    width: str
    blur_data: str
    height: str


@dataclass
class Content:
    thumbnail: Thumbnail
    file: FileContent
    comment: str
    text: str


@dataclass
class DateTimeObject:
    date_time: str
    time_zone_id: str


@dataclass
class ExtensionDetails:
    version: str


@dataclass
class Environment:
    data_center: str
    base_url: str
    tld: str
    extension: ExtensionDetails


@dataclass
class File:
    name: str
    id: str
    type: str
    url: str


@dataclass
class FormRequestParam:
    name: str
    action: str
    values: Any


@dataclass
class FormValue:
    label: Optional[str]
    value: Optional[str]


@dataclass
class FormTarget:
    name: str
    value: Any
    query: str


@dataclass
class Location:
    latitude: int
    longitude: int
    accuracy: int
    altitude: int
    status: Literal["granted", "prompt", "denied", "failed"]


@dataclass
class LocationValue:
    latitude: int
    longitude: int


@dataclass
class Mention:
    name: str
    dname: str
    id: str
    type: str


@dataclass
class Message:
    type: str
    mentions: Optional[List[Mention]]
    text: Optional[str]
    file: Optional[File]
    comment: Optional[str]
    status: Optional[str]


@dataclass
class MessageDetails:
    time: int
    message: Message


@dataclass
class User:
    id: str
    first_name: str
    last_name: str
    email: str
    admin: bool
    organization_id: int
    timezone: str
    country: str
    language: str
    name: str
    zoho_user_id: int


@dataclass
class MessageObject:
    sender: User
    time: int
    type: MessageType
    text: str
    is_read: bool
    ack_key: str
    id: str
    content: Content


@dataclass
class Messages:
    count: int
    list: List[MessageObject]


@dataclass
class SuggestionObject:
    text: str
    icon: str


@dataclass
class CommandSuggestion:
    title: Optional[str]
    description: Optional[str]
    imageurl: Optional[str]


class ICliqReqHandler(TypedDict):
    type: str
    name: Optional[str]


class ICliqReqBody(TypedDict):
    name: str
    unique_name: str
    handler: ICliqReqHandler
    response_url: str
    type: str
    timestamp: int
    params: Dict[str, Any]

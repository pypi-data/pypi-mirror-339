from dataclasses import dataclass
from typing import Any, Callable, List, Tuple

from requests import Response

from . import _constants as Constants
from ._constants import Handlers
from ._handler import Handler
from ._utils import send_request
from .error import CatalystError
from .handler_response import HandlerResponse
from .request_types import (
    User,
    Environment,
    Access,
    Attachment,
    MessageObject,
    Location,
    Mention,
    Chat,
    Messages
)


@dataclass
class MessageActionHandlerRequest:
    name: str
    mentions: List[Mention]
    user: User
    chat: Chat
    environment: Environment
    access: Access
    message: MessageObject
    messages: Messages
    attachments: List[Attachment]
    location: Location


def execution_handler(
        func: Callable[
            [MessageActionHandlerRequest, HandlerResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.MESSAGEACTION,
        Handlers.MessageActionHandler.EXECUTION_HANDLER,
        func,
        HandlerResponse
    )


def new_handler_response():
    return HandlerResponse()

class Util:
    @staticmethod
    def get_attached_file(attachments: List[Attachment]):
        result: list[bytes] = []
        try:
            for attachment in attachments:
                resp: Response = send_request('GET', attachment.url, stream=True)
                result.append(resp.content)
        except Exception as er:
            raise CatalystError('Error when getting the attached file', 0, er) from er
        return result

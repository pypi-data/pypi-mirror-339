from dataclasses import dataclass
from typing import Any, Callable, Tuple

from . import _constants as Constants
from ._constants import Handlers
from ._handler import Handler
from .request_types import (
    Access,
    Environment,
    User,
    Chat,
    Location
)
from .response_types import WidgetEvent, WidgetResponse, WidgetTarget


@dataclass
class WidgetRequest:
    user: User
    environment: Environment
    access: Access
    chat: Chat

@dataclass
class WidgetExecutionHandlerRequest(WidgetRequest):
    target: WidgetTarget
    event: WidgetEvent
    location: Location



def view_handler(
        func: Callable[
            [WidgetExecutionHandlerRequest, WidgetResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.WIDGET,
        Handlers.WidgetHandler.VIEW_HANDLER,
        func,
        WidgetResponse
    )

def new_widget_response():
    return WidgetResponse()

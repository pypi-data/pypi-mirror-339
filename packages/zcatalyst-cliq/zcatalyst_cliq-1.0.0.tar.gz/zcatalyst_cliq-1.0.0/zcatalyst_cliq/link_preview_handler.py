from dataclasses import dataclass
from typing import Any, Callable, Dict, List

from . import _constants as Constants
from ._constants import Handlers
from ._handler import Handler
from .handler_response import HandlerResponse
from .request_types import (
    Access,
    Environment,
    User,
    Chat
)
from .response_types import (
    UnfurlResponse, OembedActions, VoidResponse
)


@dataclass
class LinkPreviewHandlerRequest:
    user: User
    chat: Chat
    environment: Environment
    access: Access
    url: str
    domain: str
    target: Dict[str,Any]

def preview_handler(
        func: Callable[
            [LinkPreviewHandlerRequest, UnfurlResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.LINKPREVIEW,
        Handlers.LinkPreviewHandler.PREVIEW_HANDLER,
        func,
        UnfurlResponse
    )

def action_handler(
        func: Callable[
            [LinkPreviewHandlerRequest, HandlerResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.LINKPREVIEW,
        Handlers.LinkPreviewHandler.ACTION_HANDLER,
        func,
        HandlerResponse
    )

def menu_handler(
        func: Callable[
            [LinkPreviewHandlerRequest, List[OembedActions], tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.LINKPREVIEW,
        Handlers.LinkPreviewHandler.MENU_HANDLER,
        func,
        list
    )

def after_send_handler(
        func: Callable[
            [LinkPreviewHandlerRequest, HandlerResponse, tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.LINKPREVIEW,
        Handlers.LinkPreviewHandler.AFTER_SEND_HANDLER,
        func,
        HandlerResponse
    )

def new_unfurl_response():
    return UnfurlResponse()

def new_oembed_actions():
    return OembedActions()

def new_handler_response():
    return HandlerResponse()

def new_void_response():
    return VoidResponse()

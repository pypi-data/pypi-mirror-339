from dataclasses import dataclass
from typing import Callable, Optional, Tuple, Any

from . import _constants as Constants
from ._constants import Handlers
from ._handler import Handler
from .request_types import (
    Access,
    Environment,
    User, AppInfo,
)
from .response_types import Form
from .response_types import (InstallationResponse, VoidResponse)


@dataclass
class ExtensionHandlerRequest:
    user: User
    access: Access
    environment: Environment
    authtoken: str
    app_info: AppInfo
    form: Form

def handle_installation(
        func: Callable[
            [ExtensionHandlerRequest, InstallationResponse, Tuple],
            Optional[InstallationResponse]
        ]
):
    Handler.register_hanlder(
        Constants.EXTENSION,
        Handlers.ExtensionHandler.INSTALLATION_HANDLER,
        func,
        InstallationResponse
    )

def validate_installation(
        func: Callable[
            [ExtensionHandlerRequest, InstallationResponse, Tuple],
            Optional[InstallationResponse]
        ]
):
    Handler.register_hanlder(
        Constants.EXTENSION,
        Handlers.ExtensionHandler.INSTALLATION_VALIDATOR,
        func,
        InstallationResponse
    )

def handle_uninstallation(
        func: Callable[
            [ExtensionHandlerRequest, VoidResponse, Tuple],
            Any
        ]
):
    Handler.register_hanlder(
        Constants.EXTENSION,
        Handlers.ExtensionHandler.UNINSTALLATION_HANDLER,
        func,
        VoidResponse
    )

def new_installation_response():
    return InstallationResponse()

def new_void_response():
    return VoidResponse()

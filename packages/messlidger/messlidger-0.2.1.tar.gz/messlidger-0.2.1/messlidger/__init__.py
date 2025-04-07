# DO NOT EDIT
# Generated from .copier-answers.yml

import sys
from importlib.metadata import PackageNotFoundError, version

import maufbapi.http.api
from maufbapi.types.graphql import OwnInfo
from slidge import entrypoint

# import everything for automatic subclasses discovery by slidge core
from . import command, config, contact, gateway, group, session

try:
    __version__ = version("messlidger")
except PackageNotFoundError:
    # package is not installed
    __version__ = "dev"


def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--version":
        print("messlidger version", __version__)
        exit(0)
    entrypoint("messlidger")


# workaround until https://github.com/mautrix/facebook/pull/318 is merged and
# released
maufbapi.http.api.OwnInfo = OwnInfo


__all__ = (
    "__version__",
    "command",
    "config",
    "contact",
    "gateway",
    "group",
    "main",
    "session",
)

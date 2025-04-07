import random
from typing import Optional

import maufbapi.http
from maufbapi import AndroidAPI, AndroidState
from mautrix.util.proxy import ProxyHandler
from slidge import BaseGateway, FormField, GatewayUser
from slidge.command.register import RegistrationType, TwoFactorNotRequired
from slixmpp import JID
from slixmpp.exceptions import XMPPError

from .util import save_state


class Gateway(BaseGateway):
    REGISTRATION_INSTRUCTIONS = "Enter facebook credentials"
    REGISTRATION_FIELDS = [
        FormField(var="email", label="Email", required=True),
        FormField(var="password", label="Password", required=True, private=True),
    ]
    REGISTRATION_MULTISTEP = True
    REGISTRATION_TYPE = RegistrationType.TWO_FACTOR_CODE

    ROSTER_GROUP = "Facebook"

    COMPONENT_NAME = "Facebook (slidge)"
    COMPONENT_TYPE = "facebook"
    COMPONENT_AVATAR = (
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/be/"
        "Facebook_Messenger_logo_2020.svg/640px-Facebook_Messenger_logo_2020.svg.png"
    )

    SEARCH_TITLE = "Search in your facebook friends"
    SEARCH_INSTRUCTIONS = (
        "Enter something that can be used to search for one of your friends, eg, a"
        " first name"
    )
    SEARCH_FIELDS = [FormField(var="query", label="Search term(s)", required=True)]

    GROUPS = True

    LEGACY_CONTACT_ID_TYPE = int

    def __init__(self):
        super().__init__()
        self._pending_reg = dict[str, AndroidAPI]()

    async def validate(
        self, user_jid: JID, registration_form: dict[str, Optional[str]]
    ):
        s = AndroidState()
        x = ProxyHandler(None)
        api = AndroidAPI(state=s, proxy_handler=x)
        s.generate(random.randbytes(30))  # type: ignore
        await api.mobile_config_sessionless()
        try:
            await api.login(
                email=registration_form["email"], password=registration_form["password"]
            )
        except maufbapi.http.errors.TwoFactorRequired:
            self._pending_reg[user_jid.bare] = api
        except maufbapi.http.errors.OAuthException as e:
            raise XMPPError("not-authorized", text=str(e))
        else:
            save_state(user_jid.bare, api.state)
            raise TwoFactorNotRequired

    async def validate_two_factor_code(self, user: GatewayUser, code):
        api = self._pending_reg.pop(user.jid.bare)
        try:
            await api.login_2fa(email=user.legacy_module_data["email"], code=code)
        except maufbapi.http.errors as e:
            raise XMPPError("not-authorized", text=str(e))
        save_state(user.jid.bare, api.state)

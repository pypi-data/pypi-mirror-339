import asyncio
import logging
from shutil import rmtree
from typing import TYPE_CHECKING, Optional

from nio.responses import LoginError
from slidge import BaseGateway, FormField, global_config
from slixmpp import JID
from slixmpp.exceptions import XMPPError

from . import config, reactions
from .matrix import AuthenticationClient
from .util import Credentials

if TYPE_CHECKING:
    from .session import Session


class Gateway(BaseGateway):
    REGISTRATION_FIELDS = [
        FormField(var="homeserver", label="Home Server", required=True),
        FormField(var="username", label="User name", required=True),
        FormField(var="password", label="Password", required=True, private=True),
        FormField(
            var="device",
            label="Device name",
            value=f"matridge on {getattr(global_config, 'JID', 'dev')}",
            required=True,
        ),
    ]
    REGISTRATION_INSTRUCTIONS: str = "Enter your credentials"

    COMPONENT_NAME = "Matrix (slidge)"
    COMPONENT_TYPE = "matrix"

    COMPONENT_AVATAR = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7c/Matrix_icon.svg/209px-Matrix_icon.svg.png"

    ROSTER_GROUP: str = "matrix"

    MARK_ALL_MESSAGES = False

    PROPER_RECEIPTS = True

    GROUPS = True

    DB_PURGE_SLEEP = 3600 * 24

    PREFERENCES = BaseGateway.PREFERENCES + [
        FormField(
            var="trust_everything",
            label="Always trust new encryption keys. "
            "This is unsafe if you need perfect bridge to end encryption.",
            value="false",
            required=True,
            type="boolean",
        )
    ]

    def __init__(self):
        super().__init__()
        if not config.NIO_VERBOSE:
            logging.getLogger("peewee").setLevel(logging.WARNING)
            logging.getLogger("nio.responses").setLevel(logging.FATAL)
            logging.getLogger("nio.rooms").setLevel(logging.WARNING)
        self._db_purge_task = self.loop.create_task(self._db_purge())

    async def _db_purge(self):
        await asyncio.sleep(self.DB_PURGE_SLEEP)
        reactions.purge_old_messages(config.REACTION_CACHE_SIZE)

    async def validate(
        self, user_jid: JID, registration_form: dict[str, Optional[str]]
    ) -> Credentials:
        client = AuthenticationClient(
            registration_form["homeserver"],  # type:ignore
            registration_form["username"],  # type:ignore
            user_jid,
        )
        await client.fix_homeserver()
        resp = await client.login(
            registration_form["password"],  # type:ignore
            registration_form["device"],  # type:ignore
        )
        if isinstance(resp, LoginError):
            log.debug("Failed login: %r", resp)
            raise XMPPError("not-authorized", f"Could not login: {resp}")
        return client.get_credentials(resp)

    async def unregister(self, user):
        session: "Session" = self.get_session_from_user(user)  # type: ignore
        session.matrix.stop_listen()
        await session.matrix.logout()
        rmtree(session.matrix.store_path)


log = logging.getLogger(__name__)

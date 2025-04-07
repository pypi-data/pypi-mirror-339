import asyncio
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import nio
from aiohttp import ClientConnectionError
from slidge import LegacyContact, LegacyRoster
from slixmpp.exceptions import XMPPError

if TYPE_CHECKING:
    from .session import Session


class Contact(LegacyContact[str]):
    """
    We don't implement direct messages but the what's parsed here will propagate
    to MUC participants.
    """

    session: "Session"

    async def update_info(self):
        # Because of slidge core's design, at this point we don't know which room
        # the contact is in, so we have to iterate over rooms, which is better than
        # issuing a full profile fetch
        for _, room in self.session.matrix.rooms.items():
            user = room.users.get(self.legacy_id)
            if user is not None:
                break
        else:
            raise XMPPError("item-not-found", "We don't know this user")

        self.name = user.display_name
        if mxc := user.avatar_url:
            self.avatar = await self.session.matrix.mxc_to_http(mxc)
        else:
            self.avatar = None

    async def fetch_vcard(self):
        try:
            resp = await self.session.matrix.get_profile(self.legacy_id)
        except (ClientConnectionError, TimeoutError, asyncio.TimeoutError) as e:
            raise XMPPError("remote-server-timeout", str(e))
        if not isinstance(resp, nio.ProfileGetResponse):
            raise XMPPError("internal-server-error", str(resp))

        if resp.other_info:
            self.set_vcard(note=str(resp.other_info))

    def update_presence(self, p: nio.PresenceEvent):
        kw = dict(status=p.status_msg)
        if last := p.last_active_ago is not None:
            kw["last_seen"] = datetime.now() - timedelta(seconds=last)
        if p.currently_active:
            self.online(**kw)
        else:
            self.away(**kw)


class Roster(LegacyRoster[str, Contact]):
    session: "Session"

    async def jid_username_to_legacy_id(self, jid_username: str):
        u = await super().jid_username_to_legacy_id(jid_username)
        if not u.startswith("@"):
            raise XMPPError(
                "bad-request",
                f"'{jid_username}' is not a valid matrix username. "
                "Matrix usernames starts with @",
            )
        return u

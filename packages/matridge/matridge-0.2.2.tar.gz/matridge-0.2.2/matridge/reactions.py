from asyncio import Lock
from collections import namedtuple
from contextlib import contextmanager
from datetime import datetime
from typing import TYPE_CHECKING, AsyncIterator, Iterator, Literal, overload

import nio
import sqlalchemy as sa
from sqlalchemy import orm

if TYPE_CHECKING:
    from matridge.matrix import Client

ReactionTarget = namedtuple("ReactionTarget", ["room", "event"])


class Base(orm.DeclarativeBase):
    pass


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (sa.Index("rooms_room_id", "room_id", unique=True),)

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    room_id: orm.Mapped[str] = orm.mapped_column()

    messages: orm.Mapped[list["Message"]] = orm.relationship(
        "Message", back_populates="room"
    )


class Message(Base):
    __tablename__ = "messages"
    __table_args__ = (
        sa.Index("messages_event_id", "room_id", "event_id", unique=True),
    )

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    event_id: orm.Mapped[str] = orm.mapped_column()
    added: orm.Mapped[datetime] = orm.mapped_column(default=sa.func.now())

    room_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("rooms.id"))

    room: orm.Mapped[Room] = orm.relationship("Room", back_populates="messages")
    reactions: orm.Mapped[list["Reaction"]] = orm.relationship(
        "Reaction", back_populates="message", cascade="all, delete-orphan"
    )


class Reaction(Base):
    __tablename__ = "reactions"
    __table_args__ = (
        sa.Index("reactions_event_id", "event_id", "message_id", unique=True),
    )

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    event_id: orm.Mapped[str] = orm.mapped_column()
    sender: orm.Mapped[str] = orm.mapped_column()
    emoji: orm.Mapped[str] = orm.mapped_column()

    message_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("messages.id"))
    message: orm.Mapped[Message] = orm.relationship(
        "Message", back_populates="reactions"
    )


class ReactionCache:
    """
    To avoid fetching history on each matrix reaction event, we store the
    "reaction state" per message.

    This is because matrix reaction events are atomic, unlike XMPP reactions
    which contain the full state in each event.
    """

    def __init__(self, client: "Client"):
        self.matrix = client
        self.log = client.session.log

    @contextmanager
    def session(self) -> Iterator[orm.Session]:
        with Session() as session:
            yield session

    async def _fetch_if_needed(
        self, session: orm.Session, target: ReactionTarget
    ) -> tuple[Message, bool]:
        # we use a lock to prevent parallel calls to _fetch for the same target
        if target in _locks:
            del_lock = False
            lock = _locks[target]
        else:
            del_lock = True
            lock = _locks[target] = Lock()
        async with lock:
            room = session.scalar(sa.select(Room).filter_by(room_id=target.room))

            if room is None:
                room = Room(room_id=target.room)
                session.add(room)

            message = session.scalar(
                sa.select(Message).filter_by(room=room, event_id=target.event)
            )
            fetch = message is None
            if fetch:
                message = Message(room=room, event_id=target.event)
                session.add(message)
                async for reaction in self._fetch(target.room, target.event):
                    reaction.message = message
                    session.add(reaction)
        if del_lock:
            del _locks[target]
        assert message is not None
        return message, fetch

    async def _fetch(self, room: str, event_id: str) -> AsyncIterator[Reaction]:
        self.log.debug("fetching reactions for %s", event_id)
        async for event in self.matrix.room_get_event_relations(
            room, event_id, nio.api.RelationshipType.annotation
        ):
            if not isinstance(event, nio.ReactionEvent):
                self.log.warning("got a non-reaction event: %s", event)
                continue
            if not event.reacts_to == event_id:
                self.log.warning(
                    "request reaction on %s but got reaction on %s",
                    event_id,
                    event.reacts_to,
                )
                continue
            yield Reaction(
                event_id=event.event_id, sender=event.sender, emoji=event.key
            )

    async def add(
        self,
        session: orm.Session,
        room: str,
        msg: str,
        sender: str,
        emoji: str,
        reaction_event: str,
    ) -> None:
        target = ReactionTarget(room=room, event=msg)
        message, fetched = await self._fetch_if_needed(session, target)
        if fetched:
            # no need to add the reaction if we fetched, because we fetched the reaction
            # we want to add already
            return
        reaction = Reaction(
            event_id=reaction_event, sender=sender, emoji=emoji, message=message
        )
        session.add(reaction)

    @overload
    async def get(
        self,
        session: orm.Session,
        room: str,
        msg: str,
        sender: str,
        with_event_ids: Literal[False],
    ) -> set[str]: ...

    @overload
    async def get(
        self, session: orm.Session, room: str, msg: str, sender: str
    ) -> set[str]: ...

    @overload
    async def get(
        self,
        session: orm.Session,
        room: str,
        msg: str,
        sender: str,
        with_event_ids: Literal[True],
    ) -> dict[str, str]: ...

    async def get(
        self,
        session: orm.Session,
        room: str,
        msg: str,
        sender: str,
        with_event_ids=False,
    ):
        message, _ = await self._fetch_if_needed(
            session, ReactionTarget(room=room, event=msg)
        )
        stmt = sa.select(Reaction).filter_by(message=message, sender=sender)
        reactions = session.scalars(stmt).all()

        if with_event_ids:
            return {r.emoji: r.event_id for r in reactions}
        else:
            return set(r.emoji for r in reactions)

    @staticmethod
    def remove(
        session: orm.Session, room_id: str, event_id: str
    ) -> ReactionTarget | None:
        room = session.scalar(sa.select(Room).filter_by(room_id=room_id))
        if room is None:
            return None

        stmt = (
            sa.select(Reaction)
            .options(orm.joinedload(Reaction.message))
            .join(Reaction.message)
            .filter(Message.room_id == room.id, Reaction.event_id == event_id)
        )
        reaction = session.scalar(stmt)
        if reaction is None:
            return None
        session.delete(reaction)
        return ReactionTarget(room=room.room_id, event=reaction.message.event_id)


def purge_old_messages(limit: int):
    with Session() as session:
        current_message_count = session.query(Message).count()

        if current_message_count <= limit:
            return

        stmt = sa.delete(Message).where(
            Message.id.in_(
                sa.select(Message.id)
                .order_by(Message.added)
                .limit(current_message_count - limit)
            )
        )
        session.execute(stmt)
        session.commit()


__all__ = ("ReactionCache", "purge_old_messages")

_locks = dict[ReactionTarget, Lock]()

engine = sa.create_engine(f"sqlite:///:memory:")
Base.metadata.create_all(engine)
Session = orm.sessionmaker(engine)

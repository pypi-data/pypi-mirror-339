from collections import defaultdict
import logging

import nio
import pytest

from matridge.reactions import ReactionCache, purge_old_messages


class MockMatrix:
    class session:
        log = logging.getLogger()

    @staticmethod
    async def room_get_event_relations(room, event_id, rel_type):
        if room == "bad":
            return

        yield nio.ReactionEvent(
            reacts_to="msg_id",
            key="<3",
            source=mock_source(
                {
                    "event_id": "1",
                    "sender": "someone",
                    "content": {"m.relates_to": {"event_id": "msg_id", "key": "<3"}},
                }
            ),
        )

        yield nio.ReactionEvent(
            reacts_to="msg_id",
            key="+1",
            source=mock_source(
                {
                    "event_id": "2",
                    "sender": "someone",
                    "content": {"m.relates_to": {"event_id": "msg_id", "key": "+1"}},
                }
            ),
        )
        yield nio.ReactionEvent(
            reacts_to="other_msg_id",
            key="-1",
            source=mock_source(
                {
                    "event_id": "3",
                    "sender": "someone",
                    "content": {
                        "m.relates_to": {
                            "event_id": "other_msg_id",
                            "key": "-1",
                        }
                    },
                }
            ),
        )

    @staticmethod
    async def sync(sync_filter):
        return nio.SyncResponse(None, None, None, None, None, None)

    @staticmethod
    async def get_original_id(room, event_id):
        return event_id


def mock_source(data):
    x = defaultdict(str)
    x.update(data)
    return x


@pytest.mark.asyncio
async def test_no_response():
    cache = ReactionCache(MockMatrix)
    with cache.session() as s:
        assert await cache.get(s, "bad", "msg_id", "sender") == set()


@pytest.mark.asyncio
async def test_remove_unknown_event():
    cache = ReactionCache(MockMatrix)
    with cache.session() as s:
        cache.remove(s, "bad", "unknown")


@pytest.mark.asyncio
async def test_fetch():
    cache = ReactionCache(MockMatrix)
    with cache.session() as s:
        assert await cache.get(s, "good", "msg_id", "someone") == {"<3", "+1"}


@pytest.mark.asyncio
async def test_fetch_add_remove():
    cache = ReactionCache(MockMatrix)
    target = "good", "msg_id", "someone"
    with cache.session() as s:
        await cache.add(s, *target, "prout", "4")
        assert await cache.get(s, *target) == {"<3", "+1", "prout"}
        cache.remove(s, "good", "2")
        assert await cache.get(s, *target) == {"<3", "prout"}


@pytest.mark.asyncio
async def test_fetch_add_remove():
    cache = ReactionCache(MockMatrix)
    with cache.session() as s:
        start = await cache.get(s, "good", "msg_id", "someone")
        for i in range(10):
            await cache.add(s, "good", "msg_id", "someone", str(i), f"whatevs{i}")
        s.commit()

    purge_old_messages(10)
    with cache.session() as s:
        for i in range(10):
            await cache.add(s, str(i), str(i), "someone", "emoji", f"whatevs2-{i}")

        expected = set(str(x) for x in range(10)) | start

        assert await cache.get(s, "good", "msg_id", "someone") == expected
        s.commit()

    purge_old_messages(10)
    with cache.session() as s:
        # triggers a refetch which only returns the
        assert await cache.get(s, "good", "msg_id", "someone") == start

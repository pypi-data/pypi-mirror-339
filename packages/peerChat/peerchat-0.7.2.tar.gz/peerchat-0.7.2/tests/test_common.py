"""Test module for common code."""

from pathlib import Path
from shutil import rmtree
from json import dumps, loads

from peer_chat.common import Message, Conversation, MessageStore


def test_message_de_serialization():
    """Test (de-)serialization of `Message`."""
    m = Message("0")
    assert m.json == Message.from_json(loads(dumps(m.json))).json


def test_conversation_de_serialization(tmp: Path):
    """Test (de-)serialization of `Conversation`."""
    c = Conversation("0.0.0.0", "c-0", path=tmp, messages={"0": Message("0")})
    assert c.json == Conversation.from_json(loads(dumps(c.json))).json


def test_message_store_loading_and_caching_conversation(
    tmp: Path, fake_conversation
):
    """Test loading and caching of conversations in `MessageStore`."""
    store = MessageStore(tmp)

    # check behavior for missing data
    assert store.load_conversation("unknown-id") is None

    # prepare and load test-data
    faked_conversation = fake_conversation(tmp)
    conversation = store.load_conversation(faked_conversation.path.name)
    assert conversation is not None
    assert faked_conversation.json == conversation.json

    # test caching
    rmtree(conversation.path)
    conversation = store.load_conversation(faked_conversation.id_)
    assert conversation is not None


def test_message_store_loading_and_caching_messages(
    tmp: Path, fake_conversation
):
    """Test loading and caching of messages in `MessageStore`."""
    store = MessageStore(tmp)

    # prepare and load test-data
    faked_conversation = fake_conversation(tmp)

    # check behavior for missing data
    assert store.load_message(faked_conversation.id_, 999) is None

    message = store.load_message(faked_conversation.id_, 0)
    assert message is not None
    assert faked_conversation.messages[0].json == message.json

    # test caching
    (faked_conversation.path / "0.json").unlink()
    message = store.load_message(faked_conversation.id_, 0)
    assert message is not None


def test_message_store_load_conversations(tmp: Path, fake_conversation):
    """Test method `list_conversations` of `MessageStore`."""
    store = MessageStore(tmp)

    assert not store.list_conversations()

    faked_conversation1 = fake_conversation(tmp)
    faked_conversation2 = fake_conversation(tmp)
    (tmp / "another-directory").mkdir()
    (tmp / "another-file").touch()

    assert set(store.list_conversations()) == set(
        [faked_conversation1.id_, faked_conversation2.id_]
    )

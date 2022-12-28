import pytest
from pygame.event import Event

from pharcobial.types import KeyBinding, UserInput


@pytest.fixture
def key_binding():
    return KeyBinding()


@pytest.fixture
def left_pressed(key_binding):
    return press(key_binding.left)


@pytest.fixture
def left_released(key_binding):
    return release(key_binding.left)


@pytest.fixture
def right_pressed(key_binding):
    return press(key_binding.right)


@pytest.fixture
def right_released(key_binding):
    return release(key_binding.right)


@pytest.fixture
def up_pressed(key_binding):
    return press(key_binding.up)


@pytest.fixture
def up_released(key_binding):
    return release(key_binding.up)


@pytest.fixture
def down_pressed(key_binding):
    return press(key_binding.down)


@pytest.fixture
def down_released(key_binding):
    return release(key_binding.down)


def press(key: int) -> Event:
    return Event(UserInput.KEY_UP, {"key": key})


def release(key: int) -> Event:
    return Event(UserInput.KEY_UP, {"key": key})

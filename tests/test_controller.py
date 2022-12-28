import pytest

from pharcobial.controller import Controller


@pytest.fixture
def controller(key_binding):
    return Controller(key_binding)


def test_left(controller, left_pressed, left_released):
    controller.handle_key_down(left_pressed)
    assert controller.x == -1
    assert controller.y == 0
    controller.handle_key_up(left_released)
    assert controller.x == 0
    assert controller.y == 0


def test_right(controller, right_pressed, right_released):
    controller.handle_key_down(right_pressed)
    assert controller.x == 1
    assert controller.y == 0
    controller.handle_key_up(right_released)
    assert controller.x == 0
    assert controller.y == 0


def test_up(controller, up_pressed, up_released):
    controller.handle_key_down(up_pressed)
    assert controller.x == 0
    assert controller.y == -1
    controller.handle_key_up(up_released)
    assert controller.x == 0
    assert controller.y == 0


def test_down(controller, down_pressed, down_released):
    controller.handle_key_down(down_pressed)
    assert controller.x == 0
    assert controller.y == 1
    controller.handle_key_up(down_released)
    assert controller.x == 0
    assert controller.y == 0

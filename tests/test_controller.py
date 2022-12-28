import pytest

from pharcobial.controller import Controller

"""
Had to add these tests because it was way too difficult to test
the controller normalization logic manually while actually knowing
if it was correct or not; kept getting odd errors where direction
axis values would be unexpected. Finally, things seem to be working!
Thanks tests!
"""


@pytest.fixture
def controller(key_binding):
    return Controller(key_binding)


def test_left(controller, left_pressed, left_released):
    controller.handle_key_down(left_pressed)
    assert controller.direction == (-1, 0)
    controller.handle_key_up(left_released)
    assert controller.direction == (0, 0)


def test_right(controller, right_pressed, right_released):
    controller.handle_key_down(right_pressed)
    assert controller.direction == (1, 0)
    controller.handle_key_up(right_released)
    assert controller.direction == (0, 0)


def test_up(controller, up_pressed, up_released):
    controller.handle_key_down(up_pressed)
    assert controller.direction == (0, -1)
    controller.handle_key_up(up_released)
    assert controller.direction == (0, 0)


def test_down(controller, down_pressed, down_released):
    controller.handle_key_down(down_pressed)
    assert controller.direction == (0, 1)
    controller.handle_key_up(down_released)
    assert controller.direction == (0, 0)


def test_left_up_release_left_first(
    controller, left_pressed, left_released, up_pressed, up_released
):
    # Handling two keys diagonally causes vector normalization.
    controller.handle_key_down(left_pressed)
    controller.handle_key_down(up_pressed)
    assert controller.direction == (-0.707107, -0.707107)

    # Lifting only 1 finger up should cause the only axis to go to -1.
    controller.handle_key_up(left_released)
    assert controller.direction == (0, -1)

    controller.handle_key_up(up_released)
    assert controller.direction == (0, 0)


def test_left_down_release_left_first(
    controller, left_pressed, left_released, down_pressed, down_released
):
    # Handling two keys diagonally causes vector normalization.
    controller.handle_key_down(left_pressed)
    controller.handle_key_down(down_pressed)
    assert controller.direction == (-0.707107, 0.707107)

    # Lifting only 1 finger up should cause the only axis to go to 1.
    controller.handle_key_up(left_released)
    assert controller.direction == (0, 1)

    controller.handle_key_up(down_released)
    assert controller.direction == (0, 0)


def test_left_up_release_up_first(controller, left_pressed, left_released, up_pressed, up_released):
    controller.handle_key_down(left_pressed)
    controller.handle_key_down(up_pressed)
    controller.handle_key_up(up_released)
    assert controller.direction == (-1, 0)

    controller.handle_key_up(left_released)
    assert controller.direction == (0, 0)


def test_left_down_release_down_first(
    controller, left_pressed, left_released, down_pressed, down_released
):
    controller.handle_key_down(left_pressed)
    controller.handle_key_down(down_pressed)
    controller.handle_key_up(down_released)
    assert controller.direction == (-1, 0)

    controller.handle_key_up(left_released)
    assert controller.direction == (0, 0)


def test_right_up_release_right_first(
    controller, right_pressed, right_released, up_pressed, up_released
):
    # Handling two keys diagonally causes vector normalization.
    controller.handle_key_down(right_pressed)
    controller.handle_key_down(up_pressed)
    assert controller.direction == (0.707107, -0.707107)

    # Lifting only 1 finger up should cause the only axis to go to -1.
    controller.handle_key_up(right_released)
    assert controller.direction == (0, -1)

    controller.handle_key_up(up_released)
    assert controller.direction == (0, 0)


def test_right_down_release_right_first(
    controller, right_pressed, right_released, down_pressed, down_released
):
    # Handling two keys diagonally causes vector normalization.
    controller.handle_key_down(right_pressed)
    controller.handle_key_down(down_pressed)
    assert controller.direction == (0.707107, 0.707107)

    # Lifting only 1 finger up should cause the only axis to go to 1.
    controller.handle_key_up(right_released)
    assert controller.direction == (0, 1)

    controller.handle_key_up(down_released)
    assert controller.direction == (0, 0)


def test_right_up_release_up_first(
    controller, right_pressed, right_released, up_pressed, up_released
):
    controller.handle_key_down(right_pressed)
    controller.handle_key_down(up_pressed)
    controller.handle_key_up(up_released)
    assert controller.direction == (1, 0)

    controller.handle_key_up(right_released)
    assert controller.direction == (0, 0)


def test_right_down_release_down_first(
    controller, right_pressed, right_released, down_pressed, down_released
):
    controller.handle_key_down(right_pressed)
    controller.handle_key_down(down_pressed)
    controller.handle_key_up(down_released)
    assert controller.direction == (1, 0)

    controller.handle_key_up(right_released)
    assert controller.direction == (0, 0)


def test_left_pressed_twice(controller, left_pressed):
    # Not really possible but to just to ensure safety.
    controller.handle_key_down(left_pressed)
    controller.handle_key_down(left_pressed)

    # Is unable to go past -1
    assert controller.direction == (-1, 0)


def test_right_pressed_twice(controller, right_pressed):
    # Not really possible but to just to ensure safety.
    controller.handle_key_down(right_pressed)
    controller.handle_key_down(right_pressed)

    # Is unable to go past 1
    assert controller.direction == (1, 0)


def test_up_pressed_twice(controller, up_pressed):
    # Not really possible but to just to ensure safety.
    controller.handle_key_down(up_pressed)
    controller.handle_key_down(up_pressed)

    # Is unable to go past 1
    assert controller.direction == (0, -1)


def test_down_pressed_twice(controller, down_pressed):
    # Not really possible but to just to ensure safety.
    controller.handle_key_down(down_pressed)
    controller.handle_key_down(down_pressed)

    # Is unable to go past 1
    assert controller.direction == (0, 1)


def test_left_released_twice(controller, left_released):
    # Not really possible but to just to ensure safety.
    controller.handle_key_up(left_released)
    controller.handle_key_up(left_released)

    # Is unable to go past -1
    assert controller.direction == (1, 0)


def test_right_released_twice(controller, right_released):
    # Not really possible but to just to ensure safety.
    controller.handle_key_up(right_released)
    controller.handle_key_up(right_released)

    # Is unable to go past -1
    assert controller.direction == (-1, 0)


def test_up_released_twice(controller, up_released):
    # Not really possible but to just to ensure safety.
    controller.handle_key_up(up_released)
    controller.handle_key_up(up_released)

    # Is unable to go past -1
    assert controller.direction == (0, 1)


def test_down_released_twice(controller, down_released):
    # Not really possible but to just to ensure safety.
    controller.handle_key_up(down_released)
    controller.handle_key_up(down_released)

    # Is unable to go past -1
    assert controller.direction == (0, -1)

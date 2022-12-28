from pharcobial.types import Position


class TestPosition:
    def test_decouple(self):
        position = Position(123, 444)
        x, y = position
        assert x == 123
        assert y == 444

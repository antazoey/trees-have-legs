from pharcobial._types import RandomlyAppearing


class Monster(RandomlyAppearing):
    def draw(self):
        self.display.draw_image("bush-monster", self.coordinates)

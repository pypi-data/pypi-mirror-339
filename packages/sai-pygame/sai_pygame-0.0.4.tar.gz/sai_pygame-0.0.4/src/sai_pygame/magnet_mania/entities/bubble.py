from sai_pygame.utils.animation import AnimationBase

frame_frequencies = [8, 6, 6, 4, 3, 3, 3, 3]


class Bubble(AnimationBase):
    def __init__(self, sprites, position, size=40):
        super().__init__(sprites, position, size, 8, frame_frequencies)

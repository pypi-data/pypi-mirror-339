from ..entities.death_bubbles import DeathBubbles
from .player_display import PlayerDisplay
from .game_over_screen import GameOverScreen
from ..constants import SCREEN_HEIGHT, SCREEN_WIDTH

DISPLAY_PADDING = 50

POSITIONS = [
    (DISPLAY_PADDING, DISPLAY_PADDING),
    (SCREEN_WIDTH - DISPLAY_PADDING, DISPLAY_PADDING),
    (SCREEN_WIDTH - DISPLAY_PADDING, SCREEN_HEIGHT - DISPLAY_PADDING),
    (DISPLAY_PADDING, SCREEN_HEIGHT - DISPLAY_PADDING),
]


class HUD:
    def __init__(self, players, bubble_sprites):
        self.players = players
        self.bubble_sprites = bubble_sprites
        self.game_over_screen = GameOverScreen()
        self.displays = [
            PlayerDisplay("P{}".format(i + 1), POSITIONS[i], i)
            for i in range(len(players))
        ]

    def update(self, screen, done):
        death_bubbles = []
        if done:
            self.game_over_screen.render(screen)
        else:
            for display in self.displays:
                display.render(screen)
                if (
                    self.players[display.id].drowned
                    and not self.displays[display.id].dead
                ):
                    self.displays[display.id].grayscale()
                    death_bubbles.append(
                        DeathBubbles(
                            self.bubble_sprites, self.players[display.id].rect.center
                        )
                    )
        return death_bubbles

    def reset(self):
        for display in self.displays:
            display.reset()

import arcade
import math

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Shooter"

PLAYER_SCALE = 0.5   # ✅ Added this

class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_angle = 0
        self.player_radius = 150 * PLAYER_SCALE

    def on_draw(self):
        self.clear()

        arcade.draw_triangle_filled(
            self.player_x + math.cos(math.radians(self.player_angle)) * self.player_radius * 1.5,
            self.player_y + math.sin(math.radians(self.player_angle)) * self.player_radius * 1.5,

            self.player_x + math.cos(math.radians(self.player_angle + 150)) * self.player_radius,
            self.player_y + math.sin(math.radians(self.player_angle + 150)) * self.player_radius,

            self.player_x + math.cos(math.radians(self.player_angle - 150)) * self.player_radius,
            self.player_y + math.sin(math.radians(self.player_angle - 150)) * self.player_radius,

            arcade.color.WHITE
        )

def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()
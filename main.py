import arcade
import math

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Shooter"

PLAYER_SCALE = 0.2
PLAYER_SPEED = 5   # ✅ Added speed

class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_angle = 0
        self.player_radius = 150 * PLAYER_SCALE

        self.keys_pressed = set()

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

    def on_update(self, delta_time):

        if arcade.key.W in self.keys_pressed:
            self.player_y += PLAYER_SPEED
        if arcade.key.S in self.keys_pressed:
            self.player_y -= PLAYER_SPEED
        if arcade.key.A in self.keys_pressed:
            self.player_x -= PLAYER_SPEED
        if arcade.key.D in self.keys_pressed:
            self.player_x += PLAYER_SPEED

        # Keep player inside screen
        self.player_x = max(self.player_radius,
                            min(SCREEN_WIDTH - self.player_radius, self.player_x))
        self.player_y = max(self.player_radius,
                            min(SCREEN_HEIGHT - self.player_radius, self.player_y))

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)   # ✅ should ADD

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_motion(self, x, y, dx, dy):
        dx = x - self.player_x
        dy = y - self.player_y
        self.player_angle = math.degrees(math.atan2(dy, dx))

def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()
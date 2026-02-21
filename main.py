import arcade
import math
import random

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Shooter"

PLAYER_SCALE = 0.3
PLAYER_SPEED = 5
PLAYER_SHOOT_COOLDOWN = 0.2
PLAYER_MAX_HEALTH = 5

BULLET_SPEED = 10
BULLET_SCALE = 0.8

ENEMY_SPAWN_RATE = 1
ENEMY_SPEED_MIN = 1
ENEMY_SPEED_MAX = 3
ENEMY_SCALE = 0.3
ENEMY_SHOOT_COOLDOWN = 1.5


class Bullet:
    def __init__(self, x, y, angle, is_enemy=False):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.radius = 4 * BULLET_SCALE
        self.is_enemy = is_enemy

    def update(self):
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

    def draw(self):
        color = arcade.color.RED if self.is_enemy else arcade.color.YELLOW
        arcade.draw_circle_filled(self.x, self.y, self.radius, color)

    def is_off_screen(self):
        return (
            self.x < 0 or self.x > SCREEN_WIDTH or
            self.y < 0 or self.y > SCREEN_HEIGHT
        )


class Enemy:
    def __init__(self):
        side = random.choice(["top", "right", "bottom", "left"])

        if side == "top":
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.y = SCREEN_HEIGHT + 20
        elif side == "right":
            self.x = SCREEN_WIDTH + 20
            self.y = random.uniform(0, SCREEN_HEIGHT)
        elif side == "bottom":
            self.x = random.uniform(0, SCREEN_WIDTH)
            self.y = -20
        else:
            self.x = -20
            self.y = random.uniform(0, SCREEN_HEIGHT)

        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        self.angle = 0
        self.radius = 150 * ENEMY_SCALE
        self.health = 3
        self.shoot_timer = ENEMY_SHOOT_COOLDOWN

    def update(self, player_x, player_y, delta_time, bullet_list):
        dx = player_x - self.x
        dy = player_y - self.y

        self.angle = math.degrees(math.atan2(dy, dx))

        # Move toward player
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        # Shooting
        self.shoot_timer -= delta_time
        if self.shoot_timer <= 0:
            bullet_list.append(Bullet(self.x, self.y, self.angle, True))
            self.shoot_timer = ENEMY_SHOOT_COOLDOWN

    def draw(self):
        arcade.draw_triangle_filled(
            self.x + math.cos(math.radians(self.angle)) * self.radius * 2,
            self.y + math.sin(math.radians(self.angle)) * self.radius * 2,

            self.x + math.cos(math.radians(self.angle + 140)) * self.radius,
            self.y + math.sin(math.radians(self.angle + 140)) * self.radius,

            self.x + math.cos(math.radians(self.angle - 140)) * self.radius,
            self.y + math.sin(math.radians(self.angle - 140)) * self.radius,

            arcade.color.RED
        )


class GameWindow(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 2
        self.player_angle = 0
        self.player_radius = 150 * PLAYER_SCALE

        self.player_health = PLAYER_MAX_HEALTH

        self.bullets = []
        self.enemies = []
        self.enemy_spawn_timer = ENEMY_SPAWN_RATE

        self.shoot_cooldown = 0
        self.keys_pressed = set()
        self.score = 0

    def on_draw(self):
        self.clear()

        # Draw player
        arcade.draw_triangle_filled(
            self.player_x + math.cos(math.radians(self.player_angle)) * self.player_radius * 1.5,
            self.player_y + math.sin(math.radians(self.player_angle)) * self.player_radius * 1.5,

            self.player_x + math.cos(math.radians(self.player_angle + 150)) * self.player_radius,
            self.player_y + math.sin(math.radians(self.player_angle + 150)) * self.player_radius,

            self.player_x + math.cos(math.radians(self.player_angle - 150)) * self.player_radius,
            self.player_y + math.sin(math.radians(self.player_angle - 150)) * self.player_radius,

            arcade.color.WHITE
        )

        for bullet in self.bullets:
            bullet.draw()

        for enemy in self.enemies:
            enemy.draw()

        arcade.draw_text(
            f"Score: {self.score}   Health: {self.player_health}",
            20,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20
        )

    def on_update(self, delta_time):

        self.shoot_cooldown -= delta_time
        self.enemy_spawn_timer -= delta_time

        # Spawn enemies
        if self.enemy_spawn_timer <= 0:
            self.enemies.append(Enemy())
            self.enemy_spawn_timer = ENEMY_SPAWN_RATE

        # Shooting
        if arcade.key.SPACE in self.keys_pressed:
            self.shoot()

        # Move forward
        if arcade.key.W in self.keys_pressed:
            self.player_x += math.cos(math.radians(self.player_angle)) * PLAYER_SPEED
            self.player_y += math.sin(math.radians(self.player_angle)) * PLAYER_SPEED

        # Keep player inside screen
        self.player_x = max(self.player_radius,
                            min(SCREEN_WIDTH - self.player_radius, self.player_x))
        self.player_y = max(self.player_radius,
                            min(SCREEN_HEIGHT - self.player_radius, self.player_y))

        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()

            # Enemy bullet hits player
            if bullet.is_enemy:
                if math.hypot(bullet.x - self.player_x, bullet.y - self.player_y) < self.player_radius:
                    self.player_health -= 1
                    self.bullets.remove(bullet)
                    continue

            if bullet.is_off_screen():
                self.bullets.remove(bullet)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player_x, self.player_y, delta_time, self.bullets)

        # Player bullets hit enemies
        for enemy in self.enemies[:]:
            for bullet in self.bullets[:]:
                if not bullet.is_enemy:
                    if math.hypot(enemy.x - bullet.x, enemy.y - bullet.y) < enemy.radius:
                        enemy.health -= 1
                        self.bullets.remove(bullet)
                        if enemy.health <= 0:
                            self.enemies.remove(enemy)
                            self.score += 1
                        break

        # Game Over
        if self.player_health <= 0:
            arcade.close_window()

    def shoot(self):
        if self.shoot_cooldown <= 0:
            bullet_x = self.player_x + math.cos(math.radians(self.player_angle)) * self.player_radius
            bullet_y = self.player_y + math.sin(math.radians(self.player_angle)) * self.player_radius

            self.bullets.append(Bullet(bullet_x, bullet_y, self.player_angle))
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def on_mouse_motion(self, x, y, dx, dy):
        dx = x - self.player_x
        dy = y - self.player_y
        self.player_angle = math.degrees(math.atan2(dy, dx))


def main():
    GameWindow()
    arcade.run()


if __name__ == "__main__":
    main()
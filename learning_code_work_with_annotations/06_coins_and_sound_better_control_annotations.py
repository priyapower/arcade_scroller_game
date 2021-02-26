"""
Platformer Game
"""
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Priya's 2D Funhouse"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
# NEW CONSTANT FOR COIN SCALING
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 3
GRAVITY = 0.8
PLAYER_JUMP_SPEED = 15

LEFT_VIEWPORT_MARGIN = 250
RIGHT_VIEWPORT_MARGIN = 250
BOTTOM_VIEWPORT_MARGIN = 50
TOP_VIEWPORT_MARGIN = 100


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # New Coin List Variable Setup
        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        self.player_sprite = None

        self.physics_engine = None

        # MY USER CONTROL UPDATES
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.view_bottom = 0
        self.view_left = 0

        # Creates a variable that holds our sound for coin collection
        # .load_sound: https://arcade.academy/arcade.html?highlight=.load_sound#arcade.load_sound
            # Loads a sound for use with .play_sound later
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        # Creates a variable that holds our sound for player jumping
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        arcade.set_background_color(arcade.csscolor.MEDIUM_VIOLET_RED)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        self.view_bottom = 0
        self.view_left = 0

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        # New Coin Sprite List
        self.coin_list = arcade.SpriteList()

        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        for x in range(0, 1250, 64):
            image_source2 = ":resources:images/tiles/grassMid.png"
            wall = arcade.Sprite(image_source2, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[256, 96],
                           [512, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            image_source3 = ":resources:images/tiles/boxCrate_double.png"
            wall = arcade.Sprite(image_source3, TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # Adds a new sprite: the coin
        # Use a loop to place some coins for our character to pick up
        for x in range(128, 1250, 256):
            image_source4 = ":resources:images/items/coinGold.png"
            coin = arcade.Sprite(image_source4, COIN_SCALING)
            coin.center_x = x
            # Makes the coin float a little off the ground
            coin.center_y = 96
            # Adds coin to coin list
            self.coin_list.append(coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # MY USER CONTROL UPDATES
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        # MY USER CONTROL UPDATES
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def update(self, delta_time):
        """ Movement and game logic """
        # MY USER CONTROL UPDATES
        self.player_sprite.change_x = 0

        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                # NEW INFO FROM SOUNDS
                # This plays the sound from jump_sound which was set in __init__
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        self.player_list.update()
        self.physics_engine.update()

        # The code for what happens when a player collides with a coin
        # Checks the coin sprite list for collisions AND saves to a new variable "coin_hit_list"
        # .check_for_collision_with_list: https://arcade.academy/arcade.html?highlight=check_for_collision_with_list#arcade.check_for_collision_with_list
            # Check for a collision between a sprite, and a list of sprites
            # 2 Parameters: (sprite_to_check, sprite_to_check_AGAINST)
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # For every coin sprite in the coin HIT list
        for coin in coin_hit_list:
            # Remove the coin from any sprite list it belongs to
            coin.remove_from_sprite_lists()
            # Play the sound set in __init__
            arcade.play_sound(self.collect_coin_sound)

        # --- Manage Scrolling ---
        changed = False

        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        if changed:
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
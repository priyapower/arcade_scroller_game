"""
Platformer Game
"""
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Priya's 2D Funhouse"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

PLAYER_MOVEMENT_SPEED = 5
# New constant for gravity
GRAVITY = 1
# New constant for player_jump_speed
PLAYER_JUMP_SPEED = 20

class Player(arcade.Sprite):
    # Creates boundaries so the player doesn't walk off the edge of the screen
    def update(self):
        """ Move the player """
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None
        self.physics_engine = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        arcade.set_background_color(arcade.csscolor.MEDIUM_VIOLET_RED)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        # This time we've saved the image source to it's own variable for use in the next line
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = Player(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        for x in range(0, 1250, 64):
            # Saving the image source in a separate variable for readability
            image_source2 = ":resources:images/tiles/grassMid.png"
            wall = arcade.Sprite(image_source2, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        coordinate_list = [[256, 96],
                           [512, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Again, saving the image source in a separate variable for readability
            image_source3 = ":resources:images/tiles/boxCrate_double.png"
            wall = arcade.Sprite(image_source3, TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

        # UPDATE TO PHYSICS ENGINE
        # https://arcade.academy/arcade.html?highlight=physicsengineplatformer#arcade.PhysicsEnginePlatformer
        # Create a physics engine for a platformer.
        # Has 4 possible parameters
            # player_sprite (Sprite) – The moving sprite
            # platforms (SpriteList) – The sprites it can’t move through
            # gravity_constant (float) – Downward acceleration per frame
            # ladders (SpriteList) – Ladders the user can climb on
        # We are using the player, the wall, and the gravity constant
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()

        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        # Sets key directional_presses to true depending if user presses certain keys
        # This accounts for the arrow pad, the AWDS set, and the space bar
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

        # Sets key directional_presses to False if user releases specific key
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Calculate speed based on the keys pressed
        # We only need to reset the x value (left and right), since the y value now has a gravity component
        self.player_sprite.change_x = 0

        # If up is triggered
        if self.up_pressed and not self.down_pressed:
            # First check if the physics engine can_jump: https://arcade.academy/arcade.html?highlight=can_jump#arcade.PhysicsEnginePlatformer.can_jump
            # Method that looks to see if there is a floor under the player_sprite.
            # If there is a floor, the player can jump and we return a True.
            if self.physics_engine.can_jump():
                # Change the y velocity for the player jump
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        if self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

        # Call update to move the sprite
        # If using a physics engine, call update player to rely on physics engine
        # for movement, and call physics engine here.
        self.player_list.update()
        self.physics_engine.update()

def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
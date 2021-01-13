"""
Platformer Game
"""
import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.player_sprite = None

        # Our physics engine
        # Currently it is just a variable, but the engine will be set below
        self.physics_engine = None

        arcade.set_background_color(arcade.csscolor.MEDIUM_VIOLET_RED)

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png",
                                           CHARACTER_SCALING)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.player_list.append(self.player_sprite)

        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Create the 'physics engine'
        # https://arcade.academy/arcade.html#arcade.PhysicsEngineSimple
            # Simplistic physics engine for use in games without gravity, such as top-down games.
            # It is easier to get started with this engine than more sophisticated engines like PyMunk.
            # Note, it does not currently handle rotation.
        # This engine is what keeps our player from being able to walk through walls or solid objects or fall through the ground
        # Noticed that I can walk off the edge of the screen, so that safeguard isn't in place yet
            # The PhysicsEngineSimple class takes two parameters: The moving sprite, and a list of sprites the moving sprite can’t move through.
            # So we either need to set another engine with params for the edges, or there is another method coming later
            # We are allowed to have more than one simple physics engine
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        coordinate_list = [[256, 96],
                           [512, 96],
                           [768, 96]]

        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            wall.position = coordinate
            self.wall_list.append(wall)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    # on_key_press: https://arcade.academy/arcade.html#arcade.View.on_key_press
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        # If a user presses Up, W, or Space
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            # change_y: https://arcade.academy/arcade.html?highlight=change_y#arcade.Sprite.change_y
            # Increases the velocity in the y-plane by the players set speed
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        # If a user presses Down or S
        elif key == arcade.key.DOWN or key == arcade.key.S:
            # Decreases the velocity in the y-plane by the players set speed
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        # If a user presses Left or A
        elif key == arcade.key.LEFT or key == arcade.key.A:
            # change_x: https://arcade.academy/arcade.html?highlight=change_y#arcade.Sprite.change_x
            # Decreases the velocity in the x-plane by the players set speed
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        # If a user presses Right or D
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            # Increases the velocity in the x-plane by the players set speed
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    # on_key_release: https://arcade.academy/arcade.html#arcade.View.on_key_release
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """
        # This allows a user to press and hold a key because if you release the key, it will reset the velocity to 0
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    # on_update: https://arcade.academy/arcade.html?highlight=on_update#arcade.Sprite.on_update
    def on_update(self, delta_time):
        """ Movement and game logic """
        # Move the player with the physics engine
        self.physics_engine.update()

def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
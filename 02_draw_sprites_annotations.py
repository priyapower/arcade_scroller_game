"""
Platformer Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Priya's 2D Funhouse"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5


class MyGame(arcade.Window):
    """
    Main application class.
    """

    # The __init__ creates the variables.
    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        # The None keyword is used to define a null value, or no value at all.
        # Basically, we are just setting up these variables on self, but they currently have no value

        # For coins we pick up
        self.coin_list = None
        # For walls we can't move through
        self.wall_list = None
        # For our player
        self.player_list = None
        # Separate variable that holds the single player sprite
        self.player_sprite = None
        # We are still filling in background color with a pretty purple/red/pink color
        arcade.set_background_color(arcade.csscolor.MEDIUM_VIOLET_RED)

    # The setup actually creates the object instances, such as graphical sprites.
    # WHY keep init separate from setup?
        # With a setup method split out, later on we can easily add “restart/play again” functionality to the game.
        # A simple call to setup will reset everything.
        # Later, we can expand our game with different levels, and have functions such as setup_level_1 and setup_level_2.
    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        # Create the Sprite lists
        # The player_list saves the entire SpriteList()
        # The SpriteList class optimizes drawing, movement, and collision detection.
        self.player_list = arcade.SpriteList()
        # The wall_list and coin_list use spatial hashing
        # Spatial hashing speeds the time it takes to find collisions, but increases the time it takes to move a sprite.
        # Since we don’t expect the walls or coins to move, we'll turn on spatial hashing for these lists.
        # This doesn't apply to player because a player will move a lot
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)
        self.coin_list = arcade.SpriteList(use_spatial_hash=True)

        # Set up the player, specifically placing it at these coordinates.
        # Our resource lives in the images folder
        # The optional second parameter will scale the sprite up or down
            # Example: if scaling is set to 0.5, and the the sprite is 128x128, then both width and height will be scaled down 50% for a 64x64 sprite.
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png", 
                                           CHARACTER_SCALING)
        # Where is the sprite on the screen?
        # Options for setting:
            # Sprite attribute center_x and center_y (https://arcade.academy/arcade.html?highlight=sprite%20top#arcade.Sprite.top)
            # Sprite attribute top, bottom, left, and right (https://arcade.academy/arcade.html?highlight=sprite%20top#arcade.Sprite.top)
            # Sprite attribute position (https://arcade.academy/arcade.html?highlight=sprite%20top#arcade.Sprite.top)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        # Add the player_sprite to the player_list
        self.player_list.append(self.player_sprite)

        # Create the ground
        # This shows using a loop to place multiple sprites horizontally
            # This range is static, how would we update this for a resizable window?
        for x in range(0, 1250, 64):
            # Grab the wall picture from our images folder
            # Set scaling
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            # Set the x value to be dynamic for the loop
            wall.center_x = x
            # Set the y value to be static (the ground will only be so tall)
            wall.center_y = 32
            # Add this wall sprite to the wall list
            self.wall_list.append(wall)

        # Put some crates on the ground
        # This shows using a coordinate list to place sprites
        # This is static information - how would this be updated if we had a resizable window?
        coordinate_list = [[256, 96],
                           [512, 96],
                           [768, 96]]

        # For each coordinate in the list above
        for coordinate in coordinate_list:
            # Add a crate on the ground
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
            # This uses position which takes both an x and y
            wall.position = coordinate
            # Add this crate sprite to the wall list
            self.wall_list.append(wall)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw our sprites
        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()